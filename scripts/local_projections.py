"""State-dependent local projections: the dynamic twin of the DSGE.

How does a country's activity respond to a US-demand impulse, and is the pull stronger in
recessions (the recovery channel)? Jorda LPs with country fixed effects and country-clustered
SEs, estimated separately by state (HP output gap < 0 vs >= 0).

Shock (Bartik):  s_{i,t} = us_share_i * (US IP, 12m log growth)_t   -- a common US-demand
shock scaled by each country's export exposure to the US, standardized to unit sd.
Outcome at horizon h:  100*(log activity_{i,t+h} - log activity_{i,t-1}).

Output: output/local_projections.png + printed peak responses.
Run: python scripts/local_projections.py
"""
import os
import sys

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from statsmodels.tsa.filters.hp_filter import hpfilter

DATA = os.path.join(os.path.dirname(__file__), "..", "data")
OUT = os.path.join(os.path.dirname(__file__), "..", "output")
H = 18
LAMB = 129600
# A month counts as "in recession" only if it belongs to a CONTINUOUS spell of negative-gap
# months whose length lies in [MIN_RUN, MAX_RUN]. BASELINE = business-cycle band of 1-7 years
# (12-84 months): transitory dips below zero are noise, not a downturn state, and implausibly
# long spells reflect trend mismeasurement rather than a cycle. Set LP_MIN_RUN=1 and a large
# LP_MAX_RUN to recover the plain sign-of-the-gap rule (kept as a robustness variant).
MIN_RUN = int(os.environ.get("LP_MIN_RUN", "12"))
MAX_RUN = int(os.environ.get("LP_MAX_RUN", "84"))
BAND = float(os.environ.get("LP_BAND", "0.2"))  # dead zone (%) around zero gap


def rec_state(gap, min_run=MIN_RUN, max_run=MAX_RUN, band=BAND):
    """Classify months into cyclical states.
    rec=1  : gap < -band, inside a continuous below-band spell of [min_run, max_run] months
             (a genuine downturn phase of business-cycle length);
    rec=0  : gap > +band (clearly normal/above trend);
    excl=1 : everything ambiguous -- |gap| <= band (on trend, neither state), or below-band
             months in spells shorter than min_run (transitory dips) or longer than max_run
             (trend mismeasurement). Excluded months are dropped, not relabelled."""
    neg = (gap < -band).astype(int)
    run_id = (neg.diff().fillna(0) != 0).cumsum()
    run_len = neg.groupby(run_id).transform("size")
    rec = ((neg == 1) & (run_len >= min_run) & (run_len <= max_run)).astype(int)
    excl = (((neg == 1) & (rec == 0)) | (gap.abs() <= band)).astype(int)
    return rec, excl


def clustered_ols(d, y, xs, cluster):
    d = d.dropna(subset=[y] + xs + [cluster])
    X = np.column_stack([np.ones(len(d))] + [d[x].values.astype(float) for x in xs])
    yv = d[y].values.astype(float)
    XtXi = np.linalg.inv(X.T @ X)
    b = XtXi @ X.T @ yv
    u = yv - X @ b
    meat = np.zeros((X.shape[1], X.shape[1]))
    for g in np.unique(d[cluster].values):
        Xg = X[d[cluster].values == g]; ug = u[d[cluster].values == g]
        s = Xg.T @ ug; meat += np.outer(s, s)
    G, n, k = len(np.unique(d[cluster].values)), len(d), X.shape[1]
    V = (G / (G - 1)) * ((n - 1) / (n - k)) * XtXi @ meat @ XtXi
    return b, np.sqrt(np.diag(V))


def main():
    # activity panel re-keyed to ISO3
    sa = pd.read_csv(os.path.join(DATA, "haver_activity_sa.csv"), index_col=0)
    sa.index = pd.PeriodIndex(sa.index, freq="M")
    cw = pd.read_csv(os.path.join(DATA, "ifs_iso3_crosswalk.csv"))
    mona = pd.read_csv(os.path.join(DATA, "mona_arrangements.csv"))
    name2ifs = dict(zip(mona.country_name, mona.country_code.astype("Int64").astype(str)))
    ifs2iso = dict(zip(cw.ifs.astype(str), cw.iso3))
    sa = sa.rename(columns={n: ifs2iso.get(name2ifs.get(n)) for n in sa.columns})
    sa = sa.loc[:, [c for c in sa.columns if isinstance(c, str)]]

    # US demand shock: US IP 12m log growth, standardized
    us = pd.read_csv(os.path.join(DATA, "us_ip_monthly.csv"), index_col=0)
    us.index = pd.PeriodIndex(us.index, freq="M")
    usip = np.log(us["us_ip"])
    us_shock = 100 * (usip - usip.shift(12))
    us_shock = (us_shock - us_shock.mean()) / us_shock.std()

    # US export share per country (avg over sample) from bilateral exports
    bx = pd.read_csv(os.path.join(DATA, "imts_bilateral_sa.csv"))
    tot = bx[bx.partner.isin(set(cw.iso3))].groupby(["iso3", "year"]).exp.sum()
    usx = bx[bx.partner == "USA"].groupby(["iso3", "year"]).exp.sum()
    us_share = (usx / tot).groupby(level=0).mean().dropna()

    # build long panel
    recs = []
    for iso in sa.columns:
        if iso not in us_share.index:
            continue
        a = np.log(sa[iso].dropna())
        if len(a) < 60:
            continue
        gap = 100 * hpfilter(a, lamb=LAMB)[0]                 # cyclical gap, in percent
        rec01, excl01 = rec_state(gap)                         # persistence-filtered state
        g1 = 100 * a.diff()                                    # monthly growth
        for t in a.index:
            if t not in us_shock.index:
                continue
            if excl01.get(t, 0):                               # ambiguous months: drop
                continue
            recs.append({"iso3": iso, "t": t,
                         "shock": us_share[iso] * us_shock[t],
                         "rec": int(rec01.get(t, 0)), "gap": gap.get(t, np.nan),
                         "a": a.get(t), "g1": g1.get(t),
                         "g1_l1": g1.get(t - 1), "g1_l2": g1.get(t - 2)})
    p = pd.DataFrame(recs)
    p["shock"] = (p["shock"] - p["shock"].mean()) / p["shock"].std()   # standardize exposure-shock
    p["shk_rec"] = p["shock"] * p["rec"]
    p["shk_norm"] = p["shock"] * (1 - p["rec"])

    # local projections: cumulative activity response by horizon and state
    rows = {"rec": [], "norm": []}
    a_wide = np.log(sa)
    for h in range(0, H + 1):
        yv = []
        for iso in sa.columns:
            s = a_wide[iso].dropna()
            yy = 100 * (s.shift(-h) - s.shift(1))             # log a_{t+h} - log a_{t-1}
            yv.append(pd.DataFrame({"iso3": iso, "t": yy.index, "y": yy.values}))
        Y = pd.concat(yv, ignore_index=True)
        d = p.merge(Y, on=["iso3", "t"], how="inner")
        # country FE via within demeaning; control for gap level + state (absorbs the
        # mechanical "recessions are followed by recovery/decline" baseline)
        ctrls = ["shk_rec", "shk_norm", "gap", "rec", "g1_l1", "g1_l2"]
        for c in ["y"] + ctrls:
            d[c] = d[c] - d.groupby("iso3")[c].transform("mean")
        b, se = clustered_ols(d, "y", ctrls, "iso3")
        rows["rec"].append((b[1], se[1]))
        rows["norm"].append((b[2], se[2]))

    # plot IRFs
    hs = np.arange(H + 1)
    fig, ax = plt.subplots(figsize=(7, 4.5))
    for st, col, lbl in [("rec", "tab:red", "in recession (negative gap, downturn of 1-7 years)"),
                         ("norm", "tab:blue", "in normal times")]:
        bs = np.array([x[0] for x in rows[st]]); ses = np.array([x[1] for x in rows[st]])
        ax.plot(hs, bs, color=col, label=lbl)
        ax.fill_between(hs, bs - 1.64 * ses, bs + 1.64 * ses, color=col, alpha=0.15)
    ax.axhline(0, c="grey", lw=.7)
    ax.set_xticks(range(0, H + 1, 3))
    ax.set_xlim(0, H)
    ax.set_title("Activity response to a US-demand impulse (Bartik), by state")
    ax.set_xlabel("months after the shock"); ax.set_ylabel("cumulative activity, %")
    ax.legend()
    fig.tight_layout()
    sfx = "" if (MIN_RUN == 12 and MAX_RUN == 84) else f"_run{MIN_RUN}_{min(MAX_RUN, 999)}"
    fig.savefig(os.path.join(OUT, f"local_projections{sfx}.png"), dpi=130)
    print(f"saved output/local_projections{sfx}.png  (MIN_RUN={MIN_RUN})")
    pk_r = max(rows["rec"], key=lambda x: x[0])
    pk_n = max(rows["norm"], key=lambda x: x[0])
    print(f"peak response IN RECESSION = {pk_r[0]:.2f} (t={pk_r[0]/pk_r[1]:.1f}) at h={rows['rec'].index(pk_r)}")
    print(f"peak response NORMAL       = {pk_n[0]:.2f} (t={pk_n[0]/pk_n[1]:.1f}) at h={rows['norm'].index(pk_n)}")

    # full horizon path
    print("\n h |   normal (b, se, t)   |  recession (b, se, t)")
    for h in range(H + 1):
        bn, sn = rows["norm"][h]; br, sr = rows["rec"][h]
        print(f"{h:2d} | {bn:6.3f} {sn:5.3f} {bn/sn:5.1f} | {br:6.3f} {sr:5.3f} {br/sr:5.1f}")

    # LaTeX table at selected horizons
    sel = [0, 3, 6, 12, 18]
    def cell(b, se):
        st = "***" if abs(b/se) > 2.58 else "**" if abs(b/se) > 1.96 else "*" if abs(b/se) > 1.64 else ""
        return f"{b:.2f}$^{{{st}}}$" if st else f"{b:.2f}"
    lines = [
        r"\begin{table}[H]", r"\centering\small",
        r"\caption{State-dependent local projections: cumulative activity response to a "
        r"one-standard-deviation US-demand (Bartik) impulse, by horizon and state. Country "
        r"fixed effects; standard errors clustered by country in parentheses. "
        r"$^{*}/^{**}/^{***}$: 10/5/1\%.}",
        r"\label{tab:lp}",
        r"\begin{tabularx}{\textwidth}{@{}l" + "Y" * len(sel) + r"@{}}", r"\toprule",
        "Horizon (months) & " + " & ".join(str(h) for h in sel) + r" \\ \midrule",
        "Normal times & " + " & ".join(cell(*rows["norm"][h]) for h in sel) + r" \\",
        " & " + " & ".join(f"({rows['norm'][h][1]:.2f})" for h in sel) + r" \\",
        "In recession & " + " & ".join(cell(*rows["rec"][h]) for h in sel) + r" \\",
        " & " + " & ".join(f"({rows['rec'][h][1]:.2f})" for h in sel) + r" \\",
        r"\bottomrule", r"\end{tabularx}", r"\end{table}",
    ]
    with open(os.path.join(OUT, f"tables_lp{sfx}.tex"), "w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"saved output/tables_lp{sfx}.tex")


if __name__ == "__main__":
    main()
