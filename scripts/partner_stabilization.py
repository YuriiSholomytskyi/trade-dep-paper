"""Partner stabilisation quality: do well-stabilised partners shorten your downturn?

Idea: a good partner is one that stabilises its own economy, so its demand rebounds quickly
from its own downturns and keeps buying through yours. Measure each partner's rebound
strength as the average of its real GDP growth in the year AFTER a negative-growth year,
using only information available up to the episode's peak year (expanding window, WEO data).
Then weight by the client's pre-crisis export shares:

  partner_rebound = sum_p w_p * rebound_p(t<=peak)

This is fully predetermined (weights pre-crisis, rebound history pre-peak), so it is free of
the window-overlap concern that attaches to the demand pulls.

Output: printed regressions + output/tables_stabilization.tex.
Run: python scripts/partner_stabilization.py
"""
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(__file__))
from build_horserace_hp import build_episodes, ols, DATA  # noqa: E402

OUT = os.path.join(os.path.dirname(__file__), "..", "output")


def main():
    ep = build_episodes()
    cw = pd.read_csv(os.path.join(DATA, "ifs_iso3_crosswalk.csv"))
    real = set(cw.iso3)
    bx = pd.read_csv(os.path.join(DATA, "imts_bilateral_sa.csv"))
    bx = bx[bx.partner.isin(real)]
    weo = pd.read_csv(os.path.join(DATA, "weo_realgdp_annual.csv"))
    weo = weo[weo.COUNTRY.isin(real)]
    g = weo.pivot_table(index="year", columns="COUNTRY", values="ngdp_rpch")
    print(f"WEO growth: {g.index.min()}-{g.index.max()}, {g.shape[1]} countries")

    def rebound(iso, upto):
        s = g[iso].loc[:upto - 1].dropna() if iso in g.columns else pd.Series(dtype=float)
        if len(s) < 10:
            return np.nan
        neg = s[s < 0].index
        nxt = [s.get(y + 1, np.nan) for y in neg]
        nxt = [v for v in nxt if pd.notna(v)]
        return float(np.mean(nxt)) if len(nxt) >= 2 else np.nan

    def wavg_rebound(iso, yr):
        w = bx[(bx.iso3 == iso) & (bx.year.between(yr - 3, yr - 1))].groupby("partner").exp.mean()
        w = w[(w.index != iso) & (w > 0)]
        if w.empty:
            return np.nan
        rb = pd.Series({p: rebound(p, yr) for p in w.index})
        v = rb.notna()
        if not v.any():
            return np.nan
        wn = w[v] / w[v].sum()
        return float((wn * rb[v]).sum())

    ep["partner_rebound"] = [wavg_rebound(r.iso3, int(r.peak_year)) for _, r in ep.iterrows()]
    print(f"coverage: {ep.partner_rebound.notna().sum()}/{len(ep)}; "
          f"median={ep.partner_rebound.median():.2f}; "
          f"corr with us_pull={ep[['partner_rebound', 'us_pull']].corr().iloc[0, 1]:.2f}, "
          f"with partner_vol={ep[['partner_rebound', 'partner_vol']].corr().iloc[0, 1]:.2f}")

    parts = ["us_pull", "otheradv_pull", "emer_pull", "china_pull"]
    LBL = {"partner_rebound": "Partner rebound strength", "us_pull": "US demand",
           "otheradv_pull": "Other advanced demand", "emer_pull": "Emerging demand (excl.\\ China)",
           "china_pull": "China demand", "trade_open": "Trade openness",
           "partner_vol": "Partner volatility", "depth_gap": "Depth of downturn"}

    specs = [
        ("Depth", "depth_gap", ["partner_rebound", "partner_vol", "trade_open", "program"]),
        ("Full cycle (alone)", "t_full", ["partner_rebound", "trade_open", "depth_gap", "program"]),
        ("Full cycle (with demand)", "t_full",
         ["partner_rebound"] + parts + ["trade_open", "depth_gap", "program"]),
        ("Climb (with demand)", "t_climb",
         ["partner_rebound"] + parts + ["trade_open", "depth_gap", "program"]),
    ]
    rows = ["partner_rebound"] + parts + ["partner_vol", "trade_open", "depth_gap"]
    cols = []
    for name, y, xs in specs:
        res = ols(ep, y, xs)
        d = {nm: (b, se) for nm, b, se in res[0]}
        cols.append((name, d, res[2], res[3]))
        print(f"\n== {name} (n={res[2]}, clusters={res[3]})")
        for nm, (b, se) in d.items():
            if nm != "const":
                print(f"  {nm:16s} {b:8.2f}  (t={b/se:5.1f})")

    def cell(b, se):
        t = b / se
        star = "^{***}" if abs(t) > 2.6 else "^{**}" if abs(t) > 1.96 else "^{*}" if abs(t) > 1.64 else ""
        return f"${b:.2f}{star}$ {{\\scriptsize$({t:.1f})$}}"

    # split "Full cycle (with demand)" into a two-line header so the table fits the page
    tops, bots = [], []
    for c in cols:
        if " (" in c[0]:
            t, b = c[0].split(" (", 1)
            tops.append(t)
            bots.append("(" + b)
        else:
            tops.append(c[0])
            bots.append("")
    s = ["\\begin{table}[H]", "\\centering", "\\footnotesize",
         "\\setlength{\\tabcolsep}{4pt}",
         "\\caption{Partner stabilisation quality. Partner rebound strength is the export-share-"
         "weighted average of partners' real GDP growth in the year after their own "
         "negative-growth years, computed on data through the episode's peak year only, so the "
         "measure is fully predetermined.}", "\\label{tab:stabilization}",
         "\\begin{tabular}{l" + "c" * len(cols) + "}", "\\toprule",
         " & " + " & ".join(tops) + " \\\\",
         " & " + " & ".join(bots) + " \\\\", "\\midrule"]
    for r in rows:
        cells = [cell(*c[1][r]) if r in c[1] else "" for c in cols]
        s.append(f"{LBL.get(r, r)} & " + " & ".join(cells) + " \\\\")
    s += ["\\midrule",
          "Episodes & " + " & ".join(str(c[2]) for c in cols) + " \\\\",
          "Countries & " + " & ".join(str(c[3]) for c in cols) + " \\\\",
          "\\bottomrule\\end{tabular}",
          "\\\\[2pt]\\footnotesize{Country-clustered $t$-statistics in parentheses. All columns "
          "also track an indicator for an active IMF-supported arrangement. "
          "$^{*},^{**},^{***}$: significant at 10, 5, 1 percent.}",
          "\\end{table}"]
    with open(os.path.join(OUT, "tables_stabilization.tex"), "w", encoding="utf-8") as f:
        f.write("\n".join(s) + "\n")
    print("\nsaved output/tables_stabilization.tex")


if __name__ == "__main__":
    main()
