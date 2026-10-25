"""Two-way (country x peak-year) clustered inference for the full-cycle US-demand result.

Referee point (updated review, "proportionate treatment"): country clustering handles repeated
episodes within a country and peak-year fixed effects absorb common year shocks, but neither
automatically captures cross-country dependence induced by the common shifters (the same US growth
enters every episode with that peak year). The Cameron-Gelbach-Miller two-way estimator clusters on
country AND peak year at once:

    V_2way = V_country + V_peakyear - V_(country x peakyear),

each component cluster-robust with the paper's finite-sample correction. If the US coefficient's
t-statistic survives, dependence across countries sharing a peak year is not driving the result.

Prints the US full-cycle coefficient with one-way (country), one-way (peak-year), and two-way
standard errors. Run: python scripts/twoway_cluster.py
"""
import os
import sys

import numpy as np
from scipy import stats

sys.path.insert(0, os.path.dirname(__file__))
from build_horserace_hp import build_episodes  # noqa: E402

XS = ["us_pull", "otheradv_pull", "emer_pull", "china_pull", "trade_open", "depth_gap", "program"]


def _meat(X, u, groups):
    m = np.zeros((X.shape[1], X.shape[1]))
    for g in np.unique(groups):
        s = X[groups == g].T @ u[groups == g]
        m += np.outer(s, s)
    return m, len(np.unique(groups))


def vcov(X, u, XtX_inv, groups, n, k):
    meat, G = _meat(X, u, groups)
    corr = (G / (G - 1)) * ((n - 1) / (n - k))
    return corr * XtX_inv @ meat @ XtX_inv, G


def main():
    ep = build_episodes().dropna(subset=["t_full"] + XS + ["iso3"]).copy()
    ep["peak_year"] = ep.peak_year.astype(int)
    ep["cell"] = ep.iso3.astype(str) + "_" + ep.peak_year.astype(str)

    X = np.column_stack([np.ones(len(ep))] + [ep[x].values.astype(float) for x in XS])
    y = ep.t_full.values.astype(float)
    names = ["const"] + XS
    n, k = X.shape
    XtX_inv = np.linalg.inv(X.T @ X)
    b = XtX_inv @ X.T @ y
    u = y - X @ b
    j = names.index("us_pull")

    V_c, Gc = vcov(X, u, XtX_inv, ep.iso3.values, n, k)          # country
    V_y, Gy = vcov(X, u, XtX_inv, ep.peak_year.values, n, k)     # peak year
    V_cy, Gcy = vcov(X, u, XtX_inv, ep.cell.values, n, k)        # intersection
    V_2 = V_c + V_y - V_cy

    def report(label, V, dfg):
        se = np.sqrt(V[j, j])
        t = b[j] / se
        p = 2 * stats.t.sf(abs(t), dfg - 1)
        print(f"{label:34s} beta={b[j]:6.2f}  se={se:5.2f}  t={t:6.2f}  p={p:.4f}  (df={dfg-1})")

    print(f"n={n}  countries={Gc}  peak-years={Gy}  country-year cells={Gcy}\n")
    report("one-way: country", V_c, Gc)
    report("one-way: peak year", V_y, Gy)
    report("two-way: country x peak year", V_2, min(Gc, Gy))
    print(f"\ntwo-way US diagonal variance = {V_2[j, j]:.4f} "
          f"({'PSD ok' if V_2[j, j] > 0 else 'NEGATIVE -- not PSD'})")


if __name__ == "__main__":
    main()
