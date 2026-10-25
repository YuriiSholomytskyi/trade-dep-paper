"""Layer-1 stylized core-periphery model: trade as risk-sharing, and how the US AI/energy
investment tilt withdraws the world's "extra stability."

Mechanism (log-linear). A small open periphery economy i produces for two markets:
    y_i = (1 - s_i) * eps_i  +  s_i * mu          (output = domestic demand + export demand)
  - eps_i : idiosyncratic periphery shock,  Var = sig_e^2   (volatile, country-specific)
  - mu    : core (US) demand shock,         Var = sig_m^2   (STABLE: sig_m < sig_e), eps_i _|_ mu
  - s_i   : export share to the core = exposure.

So output is a PORTFOLIO of a volatile own-income source and a stable core-demand source.
=> Var(y_i) = (1-s_i)^2 sig_e^2 + s_i^2 sig_m^2.
Selling to a big, uncorrelated, stable buyer diversifies risk: Var falls in s_i up to
s* = sig_e^2 / (sig_e^2 + sig_m^2). This is the empirical us_pull/adv_pull result in theory.

US AI/energy tilt = theta: share of US absorption going to LOW-IMPORT-CONTENT domestic capital
(AI data centers, onshore chips, energy). Higher theta cuts US import demand, so the periphery's
effective export share shrinks:  s_i(theta) = omega_i * (1 - theta).
=> a rise in theta lowers s_i, RAISING Var(y_i): the world loses "extra stability" even though
the US keeps growing (composition, not level).

Output: output/model_layer1.png + printed comparative statics.
Run: python scripts/model_layer1.py
"""
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = os.path.join(os.path.dirname(__file__), "..", "output")

# calibration (std devs in % of output)
SIG_E = 5.0    # periphery idiosyncratic volatility
SIG_M = 2.0    # core (US) demand volatility  (stable: < SIG_E)
se2, sm2 = SIG_E ** 2, SIG_M ** 2


def var_y(s):
    """output variance given export-to-core share s."""
    return (1 - s) ** 2 * se2 + s ** 2 * sm2


def s_of_theta(omega, theta):
    """effective export share when US directs share theta of absorption to domestic AI/energy."""
    return omega * (1 - theta)


def main():
    s_star = se2 / (se2 + sm2)                       # variance-minimizing exposure
    print(f"Calibration: sig_e={SIG_E}, sig_m={SIG_M} (core is the stable anchor)")
    print(f"Variance-minimizing export share s* = {s_star:.2f}")
    print(f"Autarky variance (s=0): {var_y(0):.1f}  ;  at s* : {var_y(s_star):.1f}  "
          f"(max stabilization {100*(1-var_y(s_star)/var_y(0)):.0f}%)\n")

    # --- comparative static: Var(y) vs AI/energy tilt theta, by exposure omega ---
    theta = np.linspace(0, 0.8, 200)
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.3))

    for omega, lbl in [(0.10, "low exposure (ω=.10)"),
                       (0.30, "med exposure (ω=.30)"),
                       (0.55, "high exposure (ω=.55, US bloc)")]:
        s = s_of_theta(omega, theta)
        ax[0].plot(theta, var_y(s), label=lbl)
        # extra stability = variance reduction vs autarky
        ax[1].plot(theta, var_y(0) - var_y(s), label=lbl)
    ax[0].axhline(var_y(0), ls=":", c="grey", lw=1)
    ax[0].set_title("Periphery output variance rises with US AI/energy tilt")
    ax[0].set_xlabel(r"AI/energy tilt  $\theta$  (US absorption diverted home)")
    ax[0].set_ylabel("Var(output)")
    ax[0].legend(fontsize=8)
    ax[1].set_title('"Extra stability" the US exports — withdrawn as θ rises')
    ax[1].set_xlabel(r"AI/energy tilt  $\theta$")
    ax[1].set_ylabel("variance reduction vs autarky")
    ax[1].legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "model_layer1.png"), dpi=130)
    print("saved output/model_layer1.png")

    # --- the punchline comparative static, signed ---
    # dVar/dtheta = dVar/ds * ds/dtheta ; ds/dtheta = -omega < 0
    # dVar/ds = -2(1-s)se2 + 2 s sm2  (<0 in the stabilization region s<s*)
    for omega in (0.30, 0.55):
        for th in (0.2, 0.5):
            s = s_of_theta(omega, th)
            dVar_ds = -2 * (1 - s) * se2 + 2 * s * sm2
            dVar_dth = dVar_ds * (-omega)
            print(f"omega={omega}, theta={th}: s={s:.2f}, dVar/dtheta={dVar_dth:+.1f} "
                  f"({'DESTABILIZING' if dVar_dth > 0 else 'stabilizing'})")

    # world (average periphery) volatility under a baseline vs high-AI/energy regime
    omegas = np.array([0.05, 0.10, 0.15, 0.20, 0.30, 0.40, 0.55])  # cross-section of spokes
    for th0, th1 in [(0.2, 0.5)]:
        v0 = np.mean([var_y(s_of_theta(o, th0)) for o in omegas])
        v1 = np.mean([var_y(s_of_theta(o, th1)) for o in omegas])
        print(f"\nWorld avg periphery variance: theta {th0}->{th1} : {v0:.1f} -> {v1:.1f} "
              f"(+{100*(v1/v0-1):.0f}% volatility = lost stability)")


if __name__ == "__main__":
    main()
