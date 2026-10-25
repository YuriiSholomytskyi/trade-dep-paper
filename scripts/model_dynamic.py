"""Dynamic core-periphery illustration for the revised theory section (Appendix H).

Solves the small linear model of the appendix as a perfect-foresight (first-order) rational-
expectations system and produces output/model_layer2_irf.png. The point of the figure is the
composition result: two core expansions normalized to the SAME impact rise in core output generate
different import paths (because import-intensive absorption has higher import content, eta_c>eta_q),
and therefore different recovery speeds abroad, larger where bilateral exposure gamma is high.

Core block (deviations from steady state; hats dropped):
    q_t  = rho_q q_{t-1} + eps^q_t                         (import-light domestic activity, AR1)
    c_t  = E_t c_{t+1} - sigma r_t - chi q_t + eps^c_t      (import-intensive absorption, forward)
    r_t  = phi_y y^C_t                                      (reduced-form stabilization rule)
    y^C_t = omega_c c_t + omega_q q_t                       (core output)
    m_t  = eta_c c_t + eta_q q_t,  eta_c > eta_q            (core imports)
Periphery:
    x_{i,t}  = gamma_i m_t
    y^P_{i,t} = rho_P y^P_{i,t-1} + alpha x_{i,t} + eps^P_{i,t}

The forward-looking absorption equation is solved by backward recursion on the linearized system:
substituting the rule and output into the Euler equation gives
    c_t (1 + sigma phi_y omega_c) = E_t c_{t+1} - (sigma phi_y omega_q + chi) q_t + eps^c_t,
i.e.  c_t = a [ c_{t+1} + d_t ],  a = 1/(1 + sigma phi_y omega_c),
      d_t = eps^c_t - (sigma phi_y omega_q + chi) q_t,
which is solved forward with a zero terminal condition on a long horizon.

Both core expansions are persistent AR(1) pushes (rho=0.8) so the impulse responses are smooth; the
qualitative ranking does not depend on the persistence. Run: python scripts/model_dynamic.py
"""
import os

import numpy as np
import matplotlib.pyplot as plt

OUT = os.path.join(os.path.dirname(__file__), "..", "output")

# --- calibration (quarterly) ---
RHO_Q = 0.70    # import-light persistence
RHO_C = 0.70    # import-intensive expansion persistence (of the exogenous push)
SIGMA = 1.00    # intertemporal elasticity
CHI = 0.05      # import-light displaces import-intensive absorption (modest)
PHI_Y = 0.15    # reduced-form stabilization rule
OMEGA_C, OMEGA_Q = 0.55, 0.45   # output shares
ETA_C, ETA_Q = 0.60, 0.25       # import content: import-intensive > import-light
RHO_P = 0.70    # periphery persistence
ALPHA = 0.80    # export pass-through to periphery output
GAMMA_LO, GAMMA_HI = 0.10, 0.35  # bilateral exposure (low / high), from US export-share range
DEPTH = 1.0     # size of the periphery downturn shock (eps^P_0 = -DEPTH)

H = 24          # horizon shown (quarters)
LONG = 400      # internal horizon for the forward solution


def ar1_path(rho, n=LONG):
    """Unit impulse at t=0 following an AR(1)."""
    return rho ** np.arange(n)


def solve_core(eps_c, q):
    """Backward-recursion solution for import-intensive absorption c given driving paths."""
    a = 1.0 / (1.0 + SIGMA * PHI_Y * OMEGA_C)
    d = eps_c - (SIGMA * PHI_Y * OMEGA_Q + CHI) * q
    c = np.zeros(len(d) + 1)
    for t in range(len(d) - 1, -1, -1):
        c[t] = a * (c[t + 1] + d[t])
    return c[:-1]


def experiment(kind):
    """Return (y_core, imports) for an 'intensive' or 'light' core expansion, normalized to y_core[0]=1."""
    n = LONG
    if kind == "intensive":
        eps_c, q = ar1_path(RHO_C, n), np.zeros(n)
    else:  # import-light
        eps_c, q = np.zeros(n), ar1_path(RHO_Q, n)
    c = solve_core(eps_c, q)
    y_core = OMEGA_C * c + OMEGA_Q * q
    scale = 1.0 / y_core[0]          # normalize impact core output to 1
    return y_core * scale, (ETA_C * c + ETA_Q * q) * scale


def periphery(imports, gamma):
    """Periphery output starting from a downturn (eps^P_0 = -DEPTH), given a core import path."""
    y = np.zeros(len(imports))
    y[0] = -DEPTH + ALPHA * gamma * imports[0]
    for t in range(1, len(imports)):
        y[t] = RHO_P * y[t - 1] + ALPHA * gamma * imports[t]
    return y


def recovery_time(y):
    idx = np.where(y >= 0)[0]
    return int(idx[0]) if len(idx) else None


def main():
    yC_c, m_c = experiment("intensive")
    yC_q, m_q = experiment("light")

    # periphery recovery under the import-intensive expansion, low vs high exposure
    yP_lo = periphery(m_c, GAMMA_LO)
    yP_hi = periphery(m_c, GAMMA_HI)
    t = np.arange(H)

    fig, ax = plt.subplots(1, 3, figsize=(15, 4.2))

    ax[0].axhline(0, color="0.6", lw=0.8)
    ax[0].plot(t, yC_q[:H], color="tab:orange", lw=2.4, label="import-light expansion")
    ax[0].plot(t, yC_c[:H], color="tab:blue", ls="--", lw=1.6, label="import-intensive expansion")
    ax[0].set_title("Equal-sized core expansions: core output")
    ax[0].set_xlabel("quarters")
    ax[0].legend(frameon=False, fontsize=9)

    ax[1].axhline(0, color="0.6", lw=0.8)
    ax[1].plot(t, m_c[:H], color="tab:blue", label="import-intensive expansion")
    ax[1].plot(t, m_q[:H], color="tab:orange", label="import-light expansion")
    ax[1].set_title("Core imports differ by composition")
    ax[1].set_xlabel("quarters")
    ax[1].legend(frameon=False, fontsize=9)

    ax[2].axhline(0, color="0.6", lw=0.8)
    ax[2].plot(t, yP_hi[:H], color="tab:green", label=f"high exposure ($\\gamma={GAMMA_HI}$)")
    ax[2].plot(t, yP_lo[:H], color="tab:red", label=f"low exposure ($\\gamma={GAMMA_LO}$)")
    for y, col in [(yP_hi, "tab:green"), (yP_lo, "tab:red")]:
        r = recovery_time(y[:H])
        if r is not None:
            ax[2].axvline(r, color=col, ls=":", lw=1.0)
    ax[2].set_title("Peripheral recovery by exposure")
    ax[2].set_xlabel("quarters")
    ax[2].legend(frameon=False, fontsize=9)

    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "model_layer2_irf.png"), dpi=140, bbox_inches="tight")

    print("core imports on impact:  intensive=%.3f  light=%.3f" % (m_c[0], m_q[0]))
    print("cumulative core imports (H): intensive=%.3f  light=%.3f" % (m_c[:H].sum(), m_q[:H].sum()))
    print("periphery recovery time: high gamma=%s  low gamma=%s"
          % (recovery_time(yP_hi[:H]), recovery_time(yP_lo[:H])))
    print("saved output/model_layer2_irf.png")


if __name__ == "__main__":
    main()
