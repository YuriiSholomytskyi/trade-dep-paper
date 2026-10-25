"""State-dependent regime split vs. functional-coefficient (smooth) specification,
on the trade-recovery episode data.

Question a referee could ask: does the US-demand pull speed recovery MORE in deep
downturns? That is a state-dependence question with the depth of the downturn as
the state. Two ways to answer it:

  (1) REGIME SPLIT (state-dependent LP): interact us_pull with 1{depth > c}, read
      off b_shallow, b_deep, and the "state-dependence" gap b_deep - b_shallow.
      We sweep the threshold c to show the gap is an artifact of where you cut.

  (2) FUNCTIONAL-COEFFICIENT (smooth): let the us_pull effect be a smooth function
      theta(depth) = c0 + c1*depth + c2*depth^2, interacting us_pull with a
      quadratic in depth. Plot theta(depth) with a cluster-robust band and test
      whether it is flat (no genuine state-dependence).

Outcome: t_full (full-cycle recovery, months). SEs clustered by country.
Writes output/sdlp_trade_compare.png. Run: python scripts/sdlp_trade_compare.py
"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

sys.path.insert(0, os.path.dirname(__file__))
from build_horserace_hp import build_episodes  # noqa: E402

OUT = os.path.join(os.path.dirname(__file__), "..", "output")
BLUE, RED, GREY, GREEN = "#2f6f9f", "#c0392b", "#7f8c8d", "#27ae60"

BASE = ["otheradv_pull", "emer_pull", "china_pull", "trade_open", "program"]


def ols_cluster(d, y, cols, cluster="iso3"):
    """OLS with country-clustered covariance. Returns coefficients, full vcov, names."""
    d = d.dropna(subset=[y] + cols + [cluster])
    X = np.column_stack([np.ones(len(d))] + [d[c].values.astype(float) for c in cols])
    yv = d[y].values.astype(float)
    names = ["const"] + cols
    XtX_inv = np.linalg.inv(X.T @ X)
    b = XtX_inv @ (X.T @ yv)
    u = yv - X @ b
    groups = d[cluster].values
    meat = np.zeros((X.shape[1], X.shape[1]))
    for g in np.unique(groups):
        s = X[groups == g].T @ u[groups == g]
        meat += np.outer(s, s)
    G, n, k = len(np.unique(groups)), len(d), X.shape[1]
    corr = (G / (G - 1)) * ((n - 1) / (n - k))
    V = corr * XtX_inv @ meat @ XtX_inv
    return {"b": b, "V": V, "names": names, "n": n, "G": G}


def idx(r, name):
    return r["names"].index(name)


def main():
    ep = build_episodes().dropna(subset=["t_full", "us_pull", "depth_gap"] + BASE).copy()
    depth = ep.depth_gap.values.astype(float)
    m, sd = depth.mean(), depth.std()
    ep["dz"] = (depth - m) / sd                     # standardized state (numerical stability)
    ep["dz2"] = ep.dz**2
    ep["us_dz"] = ep.us_pull * ep.dz
    ep["us_dz2"] = ep.us_pull * ep.dz2
    ep["us2"] = ep.us_pull**2                       # for the shock-size check
    pct = lambda q: float(np.percentile(depth, q))
    uspct = lambda q: float(np.percentile(ep.us_pull.values, q))

    # ---------- baseline: linear (state-independent) ----------
    lin = ols_cluster(ep, "t_full", ["us_pull"] + BASE + ["depth_gap"])
    j = idx(lin, "us_pull")
    b_lin, se_lin = lin["b"][j], np.sqrt(lin["V"][j, j])

    # ---------- (2) functional-coefficient: theta(depth) ----------
    sm = ols_cluster(ep, "t_full",
                     ["us_pull", "us_dz", "us_dz2"] + BASE + ["dz", "dz2"])
    ci = [idx(sm, n) for n in ("us_pull", "us_dz", "us_dz2")]
    bth, Vth = sm["b"][ci], sm["V"][np.ix_(ci, ci)]

    def theta(dep):
        z = (dep - m) / sd
        a = np.array([np.ones_like(z), z, z**2])
        val = a.T @ bth
        var = np.einsum("ij,jk,ik->i", a.T, Vth, a.T)
        return val, np.sqrt(var)

    # Wald test that the interactions are jointly zero (is there ANY state-dependence?)
    Ri = np.array([[0, 1, 0], [0, 0, 1]])
    wald = float(bth @ Ri.T @ np.linalg.inv(Ri @ Vth @ Ri.T) @ Ri @ bth)
    pw = stats.chi2.sf(wald, 2)

    # ---------- (2b) size-dependence: marginal effect vs the pull's OWN magnitude ----------
    szm = ols_cluster(ep, "t_full", ["us_pull", "us2"] + BASE + ["depth_gap"])
    g1i, g2i = idx(szm, "us_pull"), idx(szm, "us2")
    g1, g2 = szm["b"][g1i], szm["b"][g2i]
    Vs = szm["V"][np.ix_([g1i, g2i], [g1i, g2i])]

    def size_marg(s):                               # marginal effect at pull level s
        s = np.atleast_1d(s).astype(float)
        grad = np.vstack([np.ones_like(s), 2 * s])
        M = g1 + 2 * g2 * s
        var = np.einsum("ij,ik,jk->k", Vs, grad, grad)
        return M, np.sqrt(np.maximum(var, 0))

    wald_s = g2**2 / Vs[1, 1]                        # H0: effect is linear in pull size
    pws = float(stats.chi2.sf(wald_s, 1))

    # ---------- (1) regime split: sweep the threshold ----------
    cgrid = np.linspace(pct(25), pct(80), 25)
    gap, gse = [], []
    for c in cgrid:
        hi = (depth > c).astype(float)
        ep["_hi"], ep["_usH"], ep["_usL"] = hi, ep.us_pull * hi, ep.us_pull * (1 - hi)
        r = ols_cluster(ep, "t_full", ["_hi", "_usL", "_usH"] + BASE + ["depth_gap"])
        iL, iH = idx(r, "_usL"), idx(r, "_usH")
        g = r["b"][iH] - r["b"][iL]
        s = np.sqrt(r["V"][iH, iH] + r["V"][iL, iL] - 2 * r["V"][iH, iL])
        gap.append(g); gse.append(s)
    gap, gse = np.array(gap), np.array(gse)

    def regime(c):
        hi = (depth > c).astype(float)
        ep["_hi"], ep["_usH"], ep["_usL"] = hi, ep.us_pull * hi, ep.us_pull * (1 - hi)
        r = ols_cluster(ep, "t_full", ["_hi", "_usL", "_usH"] + BASE + ["depth_gap"])
        iL, iH = idx(r, "_usL"), idx(r, "_usH")
        return r["b"][iL], r["b"][iH]

    c_med, c_p75 = pct(50), pct(75)
    bL_med, bH_med = regime(c_med)
    bL_p75, bH_p75 = regime(c_p75)

    # ---------- figure ----------
    lo, hi = pct(2.5), pct(90)
    dg = np.linspace(lo, hi, 200)
    tv, ts = theta(dg)

    fig, (axA, axB, axC) = plt.subplots(1, 3, figsize=(16.5, 4.4))

    axA.axhline(b_lin, color="k", lw=1.4, ls="-",
                label=f"linear (no state): {b_lin:.1f}")
    axA.fill_between(dg, tv - 1.96 * ts, tv + 1.96 * ts, color=BLUE, alpha=.18)
    axA.plot(dg, tv, color=BLUE, lw=2.2,
             label="functional-coeff.  $\\hat\\theta(\\mathrm{depth})$")
    for (c, bL, bH), col, ls in [((c_med, bL_med, bH_med), RED, "-"),
                                 ((c_p75, bL_p75, bH_p75), GREEN, "--")]:
        axA.hlines(bL, lo, c, color=col, ls=ls, lw=1.6)
        axA.hlines(bH, c, hi, color=col, ls=ls, lw=1.6,
                   label=f"regime split at depth$={c:.1f}$  (gap ${bH-bL:.1f}$)")
        axA.axvline(c, color=col, ls=":", lw=0.8, alpha=.5)
    axA.plot(depth[depth <= hi], np.full((depth <= hi).sum(), axA.get_ylim()[0]),
             "|", color=GREY, ms=6, alpha=.5)
    axA.set_xlabel("state: depth of downturn (%)")
    axA.set_ylabel("effect of US-demand pull on $t_{\\mathrm{full}}$ (months)")
    axA.set_title("Effect of US demand vs. depth of downturn")
    axA.legend(fontsize=8, frameon=False, loc="upper right")
    axA.grid(alpha=.25)

    axB.axhline(0, color=GREY, lw=1)
    axB.fill_between(cgrid, gap - 1.96 * gse, gap + 1.96 * gse, color=RED, alpha=.15)
    axB.plot(cgrid, gap, "o-", color=RED, lw=1.8, ms=4)
    axB.axvline(c_med, color=GREY, ls=":", lw=0.8)
    axB.axvline(c_p75, color=GREY, ls=":", lw=0.8)
    axB.set_xlabel("regime threshold $c$ on depth (%)")
    axB.set_ylabel("regime gap  $b_{\\mathrm{deep}}-b_{\\mathrm{shallow}}$")
    axB.set_title("The regime gap depends on the arbitrary cut")
    axB.grid(alpha=.25)

    us = ep.us_pull.values.astype(float)
    ulo, uhi = uspct(2.5), uspct(95)
    sg = np.linspace(ulo, uhi, 200)
    Msz, Mse = size_marg(sg)
    axC.axhline(b_lin, color="k", lw=1.4, label=f"linear: {b_lin:.1f}")
    axC.fill_between(sg, Msz - 1.96 * Mse, Msz + 1.96 * Mse, color=GREEN, alpha=.18)
    axC.plot(sg, Msz, color=GREEN, lw=2.2, label="marginal effect  $M(\\mathrm{pull})$")
    inb = (us >= ulo) & (us <= uhi)
    axC.plot(us[inb], np.full(inb.sum(), axC.get_ylim()[0]), "|", color=GREY, ms=6, alpha=.5)
    axC.set_xlabel("size: US-demand pull (%)")
    axC.set_ylabel("marginal effect on $t_{\\mathrm{full}}$ (months)")
    axC.set_title(f"Effect vs. size of the pull (curvature $p={pws:.2f}$)")
    axC.legend(fontsize=8, frameon=False, loc="best")
    axC.grid(alpha=.25)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "sdlp_trade_compare.png"), dpi=150)
    plt.close(fig)

    # ---------- console summary ----------
    print("=" * 70)
    print(f"episodes n={lin['n']}  countries={lin['G']}   "
          f"depth: median={c_med:.1f}%  p75={c_p75:.1f}%  max={depth.max():.1f}%")
    print("=" * 70)
    print(f"LINEAR (state-independent) US-demand effect on t_full: "
          f"{b_lin:.2f}  (t={b_lin/se_lin:.2f})")
    print(f"\nFUNCTIONAL-COEFFICIENT theta(depth):")
    for q in (25, 50, 75, 90):
        v, s = theta(np.array([pct(q)]))
        print(f"   at depth p{q:>2}={pct(q):5.1f}%:  theta={v[0]:6.2f}  (t={v[0]/s[0]:5.2f})")
    print(f"   Wald test  H0: theta(depth) is flat  ->  chi2(2)={wald:.2f}  p={pw:.3f}"
          f"   {'(no state-dependence detected)' if pw > 0.1 else '(state-dependence)'}")
    print(f"\nSIZE-DEPENDENCE (marginal effect vs pull magnitude):")
    for q in (25, 50, 75, 90):
        sv = uspct(q)
        Mv, Ms = size_marg(sv)
        print(f"   at pull p{q:>2}={sv:5.2f}%:  M={Mv[0]:6.2f}  (t={Mv[0]/Ms[0]:5.2f})")
    print(f"   Wald test  H0: effect linear in pull size  ->  chi2(1)={wald_s:.2f}  p={pws:.3f}"
          f"   {'(no size-dependence)' if pws > 0.1 else '(size-dependence)'}")
    print(f"\nREGIME SPLIT b_deep - b_shallow:")
    print(f"   cut at median {c_med:.1f}%: {bH_med-bL_med:+.2f}    "
          f"cut at p75 {c_p75:.1f}%: {bH_p75-bL_p75:+.2f}")
    print(f"   gap over thresholds [{cgrid[0]:.1f}, {cgrid[-1]:.1f}]%: "
          f"ranges {gap.min():+.2f} to {gap.max():+.2f}; "
          f"significant at any cut: {'yes' if (np.abs(gap/gse)>1.96).any() else 'no'}")
    print("\nsaved output/sdlp_trade_compare.png")


if __name__ == "__main__":
    main()
