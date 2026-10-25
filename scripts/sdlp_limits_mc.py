"""Limits of state-dependent local projections: two Monte Carlo demonstrations.

The state-dependent LP fits a step (two regimes A/B) to a response that, in the
data-generating process, either is genuinely two-valued (Part A) or is a smooth
nonlinear function of the state with no break at all (Part B). Two failures:

Part A  WEAK IDENTIFICATION (the variance blade).
  DGP is a correctly specified two-regime mixture with genuinely different slopes
  beta_A != beta_B. The transition weight is F(z)=logistic(gamma*z). The regime
  contrast b_A - b_B is identified ONLY through Var(F): we prove
        Var(b_A - b_B) = sigma_u^2 / (n * sigma_s^2 * Var(F)),
  so as the transition flattens (gamma small => Var(F)->0) the test of b_A=b_B
  loses all power and two truly different processes become indistinguishable.

Part B  APPROXIMATION BIAS + BIAS-VARIANCE TRADEOFF (the bias blade).
  DGP has a SMOOTH response g(z)=exp(theta*z) (a convex-Phillips-curve slope that
  rises continuously with the gap, no threshold). A two-regime split at c returns
  b_A=E[g|z>c], b_B=E[g|z<=c]: regional averages of a smooth curve, biased for the
  local response and dependent on the arbitrary cut c. Refining the partition to K
  bins lowers approximation bias like 1/K^2 but raises estimation variance like
  K/n (the same Var(F) mechanism), so total error is U-shaped and the two-regime
  model sits at the high-bias end.

Writes output/sdlp_varF_channel.png and output/sdlp_smooth_bias.png.
Run: python scripts/sdlp_limits_mc.py
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = os.path.join(os.path.dirname(__file__), "..", "output")
RNG = np.random.default_rng(20260803)

BLUE, RED, GREY, GREEN = "#2f6f9f", "#c0392b", "#7f8c8d", "#27ae60"


def ols(X, y):
    """Classic (homoskedastic) OLS: returns coefficients and their covariance."""
    XtX_inv = np.linalg.inv(X.T @ X)
    b = XtX_inv @ (X.T @ y)
    resid = y - X @ b
    s2 = (resid @ resid) / (len(y) - X.shape[1])
    return b, s2 * XtX_inv


# ======================================================================
# PART A -- weak identification (variance blade)
# ======================================================================
def part_a():
    n, R = 500, 2000
    bA_true, bB_true = 2.0, 0.5
    sig_s, sig_u = 1.0, 1.0
    gammas = np.geomspace(0.02, 10.0, 14)

    # high-accuracy Var(F) for each gamma from a large z sample (marginal only)
    zbig = RNG.standard_normal(4_000_000)
    varF = np.array([np.var(1.0 / (1.0 + np.exp(-g * zbig))) for g in gammas])

    rej = np.zeros_like(gammas)
    mc_sd = np.zeros_like(gammas)       # Monte Carlo sd of (b_A - b_B)
    mean_se = np.zeros_like(gammas)     # mean OLS se of (b_A - b_B)
    for i, g in enumerate(gammas):
        diffs, ses, rejs = np.empty(R), np.empty(R), np.empty(R)
        for r in range(R):
            z = RNG.standard_normal(n)
            F = 1.0 / (1.0 + np.exp(-g * z))
            shock = sig_s * RNG.standard_normal(n)
            u = sig_u * RNG.standard_normal(n)
            y = F * (bA_true * shock) + (1 - F) * (bB_true * shock) + u
            X = np.column_stack([F, 1 - F, F * shock, (1 - F) * shock])
            b, V = ols(X, y)
            d = b[2] - b[3]
            se = np.sqrt(V[2, 2] + V[3, 3] - 2 * V[2, 3])
            diffs[r], ses[r], rejs[r] = d, se, (abs(d / se) > 1.96)
        rej[i], mc_sd[i], mean_se[i] = rejs.mean(), diffs.std(), ses.mean()

    theo_se = sig_u / np.sqrt(n * sig_s**2 * varF)

    fig, (axL, axR) = plt.subplots(1, 2, figsize=(11, 4.2))
    axL.semilogx(varF, rej, "o-", color=BLUE, lw=1.8, ms=5)
    axL.axhline(0.05, color=GREY, ls="--", lw=1)
    axL.text(varF[0] * 1.4, 0.08, "nominal 5%", color=GREY, fontsize=9)
    axL.set_xlabel("Var$(F)$  (transition flattens $\\rightarrow$)")
    axL.set_ylabel("reject $H_0:\\ \\beta_A=\\beta_B$  (rate)")
    axL.set_title("Power collapses although $\\beta_A=2\\neq0.5=\\beta_B$")
    axL.set_ylim(-0.03, 1.05)
    axL.invert_xaxis()
    axL.grid(alpha=.25)

    axR.loglog(varF, mc_sd, "o", color=RED, ms=6, label="Monte Carlo sd of $b_A-b_B$")
    axR.loglog(varF, mean_se, "x", color=BLUE, ms=7, mew=1.6, label="mean OLS se")
    axR.loglog(varF, theo_se, "-", color="k", lw=1.4,
               label="$\\sigma_u/\\sqrt{n\\,\\sigma_s^2\\,\\mathrm{Var}(F)}$")
    axR.set_xlabel("Var$(F)$")
    axR.set_ylabel("std. error of  $b_A-b_B$")
    axR.set_title("Exact variance law verified")
    axR.legend(fontsize=8.5, frameon=False)
    axR.grid(alpha=.25, which="both")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "sdlp_varF_channel.png"), dpi=150)
    plt.close(fig)

    return dict(varF=varF, rej=rej, mc_sd=mc_sd, mean_se=mean_se, theo_se=theo_se)


# ======================================================================
# PART B -- smooth nonlinearity: approximation bias + bias-variance tradeoff
# ======================================================================
def g_true(z, theta=0.55):
    """Smooth, break-free, convex response of the outcome to a shock (slope rises
    continuously with the state z; a stylized convex-Phillips-curve slope)."""
    return np.exp(theta * z)


def part_b():
    n, R = 1000, 300
    sig_s, sig_u = 1.0, 1.0

    # population objects from a large z sample
    zbig = RNG.standard_normal(4_000_000)
    gbig = g_true(zbig)

    # ---- panel (a): the arbitrary two-regime step ----
    cuts = [0.0, 0.8]
    steps = []
    for c in cuts:
        hi = gbig[zbig > c].mean()
        lo = gbig[zbig <= c].mean()
        steps.append((c, lo, hi, hi - lo))

    # the correct alternative: functional-coefficient LP -- interact the shock
    # with a smooth (degree-4 polynomial) basis in z, so theta(z) recovers g(z).
    deg = 4
    nf = 4000
    zf = RNG.standard_normal(nf)
    sf = sig_s * RNG.standard_normal(nf)
    uf = sig_u * RNG.standard_normal(nf)
    yf = g_true(zf) * sf + uf
    P = np.column_stack([zf**k for k in range(deg + 1)])       # level basis
    Xf = np.column_stack([P, P * sf[:, None]])                 # + shock interaction
    cf = np.linalg.lstsq(Xf, yf, rcond=None)[0][deg + 1:]      # theta(z) coefficients
    zgrid = np.linspace(-2.6, 2.6, 300)
    theta_hat = np.column_stack([zgrid**k for k in range(deg + 1)]) @ cf

    # ---- panel (b): K-bin bias and variance ----
    Ks = np.array([2, 3, 4, 6, 8, 12, 16, 24, 32, 48])
    bias2 = np.zeros(len(Ks))
    var_slope = np.zeros(len(Ks))
    for j, K in enumerate(Ks):
        edges = np.quantile(zbig, np.linspace(0, 1, K + 1))
        edges[0], edges[-1] = -np.inf, np.inf
        # population approximation error of the K-bin step vs the smooth curve
        binid = np.clip(np.digitize(zbig, edges[1:-1]), 0, K - 1)
        step_means = np.array([gbig[binid == k].mean() for k in range(K)])
        approx = step_means[binid]
        bias2[j] = np.mean((approx - gbig) ** 2)

        # Monte Carlo estimation variance of a bin slope (averaged over bins)
        slopes = np.full((R, K), np.nan)
        for r in range(R):
            z = RNG.standard_normal(n)
            shock = sig_s * RNG.standard_normal(n)
            u = sig_u * RNG.standard_normal(n)
            y = g_true(z) * shock + u
            e = np.quantile(z, np.linspace(0, 1, K + 1))
            e[0], e[-1] = -np.inf, np.inf
            bid = np.clip(np.digitize(z, e[1:-1]), 0, K - 1)
            D = np.zeros((n, K))
            D[np.arange(n), bid] = 1.0
            X = np.column_stack([D, D * shock[:, None]])
            try:
                b = np.linalg.lstsq(X, y, rcond=None)[0]
                slopes[r] = b[K:]
            except np.linalg.LinAlgError:
                pass
        var_slope[j] = np.nanmean(np.nanvar(slopes, axis=0))

    total = bias2 + var_slope
    kstar = Ks[np.argmin(total)]

    fig, (axA, axB) = plt.subplots(1, 2, figsize=(11, 4.2))

    zg = np.linspace(-2.6, 2.6, 400)
    axA.plot(zg, g_true(zg), color="k", lw=2.4, label="true smooth response $g(z)$")
    axA.plot(zgrid, theta_hat, color=GREEN, lw=2.0, ls=(0, (1, 1)),
             label="functional-coeff. LP  $\\hat\\theta(z)$")
    sty = [("-", RED), ("--", BLUE)]
    for (c, lo, hi, gap), (ls, col) in zip(steps, sty):
        axA.hlines(lo, -2.6, c, color=col, ls=ls, lw=1.6)
        axA.hlines(hi, c, 2.6, color=col, ls=ls, lw=1.6,
                   label=f"2-regime step, cut $c={c}$  ($b_A-b_B={gap:.2f}$)")
        axA.axvline(c, color=col, ls=":", lw=0.8, alpha=.5)
    # same regime (z<0), very different true response
    for zp in (-0.4, -2.0):
        axA.plot(zp, g_true(zp), "o", color="k", ms=5)
    axA.annotate("", xy=(-2.0, g_true(-2.0)), xytext=(-0.4, g_true(-0.4)),
                 arrowprops=dict(arrowstyle="<->", color=GREY, lw=1.1))
    axA.text(-2.55, 0.72, "one regime,\n$g(-0.4)=%.2f$ vs $g(-2)=%.2f$"
             % (g_true(-0.4), g_true(-2.0)), color=GREY, fontsize=8)
    axA.set_xlabel("state $z$  (output gap)")
    axA.set_ylabel("response of outcome to shock")
    axA.set_title("Embed the function; do not split into states")
    axA.legend(fontsize=8, frameon=False, loc="upper left")
    axA.grid(alpha=.25)

    axB.loglog(Ks, bias2, "o-", color=RED, lw=1.8, ms=5, label="approximation bias$^2$")
    axB.loglog(Ks, var_slope, "s-", color=BLUE, lw=1.8, ms=5, label="estimation variance")
    axB.loglog(Ks, total, "^-", color="k", lw=2.0, ms=5, label="total error")
    axB.axvline(2, color=GREY, ls="--", lw=1)
    axB.text(2.1, total.max() * 0.5, "two-regime\nmodel", color=GREY, fontsize=8.5)
    axB.axvline(kstar, color=GREEN, ls=":", lw=1.4)
    axB.text(kstar * 1.05, total.min() * 1.1, f"$K^*={kstar}$", color=GREEN, fontsize=9)
    axB.set_xlabel("number of regime bins $K$  (partition refines $\\rightarrow$)")
    axB.set_ylabel("error (response units$^2$)")
    axB.set_title("Bias-variance tradeoff: cannot win")
    axB.legend(fontsize=8.5, frameon=False)
    axB.grid(alpha=.25, which="both")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "sdlp_smooth_bias.png"), dpi=150)
    plt.close(fig)

    return dict(steps=steps, Ks=Ks, bias2=bias2, var_slope=var_slope, kstar=kstar)


def main():
    print("=" * 74)
    print("PART A  weak identification -- Var(b_A - b_B) = sigma_u^2/(n sigma_s^2 Var F)")
    print("=" * 74)
    a = part_a()
    print(f"{'Var(F)':>10}{'reject':>9}{'MC sd':>9}{'OLS se':>9}{'theory se':>11}")
    for vF, rj, sd, se, th in zip(a["varF"], a["rej"], a["mc_sd"], a["mean_se"], a["theo_se"]):
        print(f"{vF:10.5f}{rj:9.3f}{sd:9.3f}{se:9.3f}{th:11.3f}")
    print(f"\n  steep F: reject={a['rej'][-1]:.2f} (truth detected).  "
          f"flat F: reject={a['rej'][0]:.2f} (~size; two different processes look identical).")

    print("\n" + "=" * 74)
    print("PART B  smooth nonlinearity g(z)=exp(0.55 z): bias + bias-variance tradeoff")
    print("=" * 74)
    b = part_b()
    for c, lo, hi, gap in b["steps"]:
        print(f"  cut c={c:>4}:  b_B={lo:.3f}  b_A={hi:.3f}  regime gap b_A-b_B = {gap:.3f}")
    print("  -> same DGP, no break, yet the reported state-dependence moves with the arbitrary cut.")
    i2 = list(b["Ks"]).index(2)
    ik = list(b["Ks"]).index(b["kstar"])
    print(f"\n  two-regime (K=2):  bias^2={b['bias2'][i2]:.4f}  var={b['var_slope'][i2]:.4f}  "
          f"total={b['bias2'][i2]+b['var_slope'][i2]:.4f}")
    print(f"  optimum  (K={b['kstar']}):  bias^2={b['bias2'][ik]:.4f}  var={b['var_slope'][ik]:.4f}  "
          f"total={b['bias2'][ik]+b['var_slope'][ik]:.4f}")
    print("\n  saved output/sdlp_varF_channel.png and output/sdlp_smooth_bias.png")


if __name__ == "__main__":
    main()
