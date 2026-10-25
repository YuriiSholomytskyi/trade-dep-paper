"""Estimation diagnostics for the headline US-demand result (full negative cycle).
Addresses: few-clusters inference (wild cluster bootstrap), influence (leave-one-country-out
and drop the US-dependent bloc), bad-control (drop the depth control), and the overlapping
partner-growth window (pre-crisis vs recovery-window demand).
Run: python scripts/estimation_diagnostics.py
"""
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(__file__))
from build_horserace_hp import build_episodes, ADVANCED  # noqa: E402

Y = "t_full"
XS = ["us_pull", "otheradv_pull", "emer_pull", "china_pull", "trade_open", "depth_gap"]
KEY = "us_pull"


def fit(d, y, xs, cluster="iso3"):
    d = d.dropna(subset=[y] + xs + [cluster])
    X = np.column_stack([np.ones(len(d))] + [d[x].values.astype(float) for x in xs])
    yv = d[y].values.astype(float)
    XtXi = np.linalg.inv(X.T @ X)
    b = XtXi @ X.T @ yv
    u = yv - X @ b
    g = d[cluster].values
    meat = np.zeros((X.shape[1], X.shape[1]))
    for gg in np.unique(g):
        s = X[g == gg].T @ u[g == gg]; meat += np.outer(s, s)
    G, n, k = len(np.unique(g)), len(d), X.shape[1]
    V = (G / (G - 1)) * ((n - 1) / (n - k)) * XtXi @ meat @ XtXi
    return b, np.sqrt(np.diag(V)), X, yv, g, list(["const"] + xs)


def wild_cluster_bootstrap(d, y, xs, key, B=1999, seed_stream=None):
    """Restricted (impose H0: beta_key=0) wild cluster bootstrap p-value, Rademacher weights."""
    d = d.dropna(subset=[y] + xs + ["iso3"]).reset_index(drop=True)   # align all rows
    names = ["const"] + xs
    ki = names.index(key)
    b, se, X, yv, g, _ = fit(d, y, xs)
    t0 = b[ki] / se[ki]
    # restricted model: drop key regressor
    xs_r = [x for x in xs if x != key]
    br, ser, Xr, _, _, names_r = fit(d, y, xs_r)
    yhat_r = Xr @ br
    ur = yv - yhat_r
    clusters = np.unique(g)
    # deterministic Rademacher draws (no RNG state needed): vary by (b, cluster) via hashing
    tb = []
    for bi in range(B):
        w = {}
        for j, c in enumerate(clusters):
            w[c] = 1.0 if ((bi * 2654435761 + j * 40503) % 2 == 0) else -1.0
        ystar = yhat_r + np.array([w[gi] for gi in g]) * ur
        dstar = d.copy(); dstar[y] = ystar
        bb, seb, *_ = fit(dstar, y, xs)
        tb.append(bb[ki] / seb[ki])
    tb = np.array(tb)
    p = np.mean(np.abs(tb) >= np.abs(t0))
    return t0, p, b[ki], se[ki]


def main():
    ep = build_episodes()
    print(f"episodes={len(ep)} countries={ep.iso3.nunique()}\n")

    # (0) baseline
    b, se, X, yv, g, names = fit(ep, Y, XS)
    ki = names.index(KEY)
    print(f"[Baseline] {KEY}={b[ki]:.2f}  cluster-SE={se[ki]:.2f}  t={b[ki]/se[ki]:.2f}")

    # (4) wild cluster bootstrap (few-clusters valid inference)
    t0, pwcb, bk, sek = wild_cluster_bootstrap(ep, Y, XS, KEY, B=999)
    print(f"[Wild cluster bootstrap, 34 clusters] t={t0:.2f}  p={pwcb:.3f}  "
          f"({'survives' if pwcb < 0.05 else 'FAILS'} at 5%)")

    # (6a) leave-one-country-out
    loo = []
    for c in ep.iso3.unique():
        bb, *_ = fit(ep[ep.iso3 != c], Y, XS)
        loo.append((c, bb[ki]))
    loo = pd.DataFrame(loo, columns=["drop", KEY]).sort_values(KEY)
    print(f"\n[Leave-one-country-out] {KEY} range {loo[KEY].min():.2f} to {loo[KEY].max():.2f}; "
          f"all negative: {bool((loo[KEY] < 0).all())}")
    print("  most influential drops:", loo.head(3).to_records(index=False).tolist(),
          loo.tail(2).to_records(index=False).tolist())

    # (6b) drop the US-dependent bloc (top US export-share countries)
    ushare = ep.groupby("iso3").us_w.mean().sort_values(ascending=False)
    for k in (3, 6):
        drop = set(ushare.head(k).index)
        bb, seb, *_ = fit(ep[~ep.iso3.isin(drop)], Y, XS)
        print(f"[Drop top-{k} US-dependent ({sorted(drop)})] {KEY}={bb[ki]:.2f} "
              f"t={bb[ki]/seb[ki]:.2f}")

    # (3) bad control: drop depth_gap from the duration regression
    xs_nd = [x for x in XS if x != "depth_gap"]
    bb, seb, *_ = fit(ep, Y, xs_nd)
    kj = (["const"] + xs_nd).index(KEY)
    print(f"\n[No depth control (avoids bad-control bias)] {KEY}={bb[kj]:.2f} t={bb[kj]/seb[kj]:.2f}")

    # (2) overlapping window: does the result survive using CONTRACTION (pre-trough) as outcome,
    #     where the partner-growth window less mechanically overlaps the rebound?
    bb, seb, *_ = fit(ep, "t_contraction", XS)
    print(f"[Outcome=contraction (peak->trough)] {KEY}={bb[ki]:.2f} t={bb[ki]/seb[ki]:.2f}")


if __name__ == "__main__":
    main()
