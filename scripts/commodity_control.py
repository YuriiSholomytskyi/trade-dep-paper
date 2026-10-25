"""Commodity-cycle robustness for the partner-demand result.

A referee's worry: commodity prices co-move with global (and US) growth, so the US-demand
pull could be standing in for the commodity price cycle rather than for demand. We control
for each country's own commodity terms-of-trade impulse using the IMF's Commodity Terms of
Trade database (CTOT, IMF.RES): the Commodity Net Export Price Index weighted by net exports
to GDP with FIXED weights (CEMPI_CTOTXM_GDP, R_FW_IX). Fixed weights are predetermined,
world commodity prices are exogenous to these economies, so the impulse has the same
shift-share logic as the demand measure.

ctot_g = average annual growth (%) of the country's CTOT index over the same window as the
demand measure (peak year and the two years following). ctot_g_comm interacts it with the
commodity-exporter indicator (the index is near-flat for non-commodity economies).

Data: data/ctot_raw_monthly.csv (pull via imf_sdmx: IMF.RES/CTOT *.CEMPI_CTOTXM_GDP.*.M).
Output: printed regressions + output/tables_commodity.tex.
Run: python scripts/commodity_control.py
"""
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(__file__))
from build_horserace_hp import build_episodes, ols  # noqa: E402

DATA = os.path.join(os.path.dirname(__file__), "..", "data")
OUT = os.path.join(os.path.dirname(__file__), "..", "output")


def load_ctot():
    raw = pd.read_csv(os.path.join(DATA, "ctot_raw_monthly.csv"), low_memory=False)
    raw = raw[raw.WGT_TYPE == "R_FW_IX"]
    raw["year"] = raw.TIME_PERIOD.str.slice(0, 4).astype(int)
    ann = raw.groupby(["COUNTRY", "year"]).OBS_VALUE.mean().rename("ctot")
    g = 100 * ann.groupby(level=0).apply(
        lambda s: np.log(s.droplevel(0)).diff()).rename("ctot_g")
    return g  # (COUNTRY, year) -> yoy log growth in percent


def main():
    ep = build_episodes()
    g = load_ctot()

    def impulse(iso, yr):
        vals = [g.get((iso, y), np.nan) for y in range(yr, yr + 3)]
        vals = [v for v in vals if pd.notna(v)]
        return np.mean(vals) if vals else np.nan

    ep["ctot_g"] = [impulse(r.iso3, int(r.peak_year)) for _, r in ep.iterrows()]
    ep["ctot_g_comm"] = ep.ctot_g * ep.commodity
    print(f"CTOT coverage: {ep.ctot_g.notna().sum()}/{len(ep)} episodes; "
          f"corr(ctot_g, us_pull) = {ep[['ctot_g', 'us_pull']].corr().iloc[0, 1]:.2f}")

    parts = ["us_pull", "otheradv_pull", "emer_pull", "china_pull"]
    LBL = {"us_pull": "US demand", "otheradv_pull": "Other advanced demand",
           "emer_pull": "Emerging demand (excl.\\ China)", "china_pull": "China demand",
           "ctot_g": "Commodity terms of trade", "ctot_g_comm": "Commodity ToT $\\times$ commodity exporter",
           "trade_open": "Trade openness", "partner_vol": "Partner volatility",
           "depth_gap": "Depth of downturn"}

    specs = [("Depth", "depth_gap", parts + ["ctot_g", "ctot_g_comm", "trade_open", "partner_vol", "program"]),
             ("Contraction", "t_contraction", parts + ["ctot_g", "ctot_g_comm", "trade_open", "depth_gap", "program"]),
             ("Climb", "t_climb", parts + ["ctot_g", "ctot_g_comm", "trade_open", "depth_gap", "program"]),
             ("Full cycle", "t_full", parts + ["ctot_g", "ctot_g_comm", "trade_open", "depth_gap", "program"])]

    rows = parts + ["ctot_g", "ctot_g_comm", "trade_open", "partner_vol", "depth_gap"]
    cols = []
    for name, y, xs in specs:
        res = ols(ep, y, xs)
        d = {nm: (b, se) for nm, b, se in res[0]}
        cols.append((name, d, res[2], res[3]))
        print(f"\n== {name} (n={res[2]}, clusters={res[3]})")
        for nm, (b, se) in d.items():
            if nm != "const":
                print(f"  {nm:14s} {b:8.2f}  (t={b/se:5.1f})")

    def cell(b, se):
        t = b / se
        star = "^{***}" if abs(t) > 2.6 else "^{**}" if abs(t) > 1.96 else "^{*}" if abs(t) > 1.64 else ""
        return f"${b:.2f}{star}$ {{\\scriptsize$({t:.1f})$}}"

    s = ["\\begin{table}[H]", "\\centering", "\\footnotesize",
         "\\setlength{\\tabcolsep}{4pt}",
         "\\caption{Partner demand and the commodity price cycle. The baseline decomposition "
         "with each country's own commodity terms-of-trade impulse added: the average growth of "
         "the IMF Commodity Net Export Price Index (fixed weights, scaled by GDP) over the same "
         "window as the demand measure, alone and interacted with the commodity-exporter "
         "indicator.}", "\\label{tab:commodity}",
         "\\begin{tabular}{l" + "c" * len(cols) + "}", "\\toprule",
         " & " + " & ".join(c[0] for c in cols) + " \\\\", "\\midrule"]
    for r in rows:
        cells = [cell(*c[1][r]) if r in c[1] else "" for c in cols]
        s.append(f"{LBL.get(r, r)} & " + " & ".join(cells) + " \\\\")
    s += ["\\midrule",
          "Episodes & " + " & ".join(str(c[2]) for c in cols) + " \\\\",
          "Countries & " + " & ".join(str(c[3]) for c in cols) + " \\\\",
          "\\bottomrule\\end{tabular}",
          "\\\\[2pt]\\footnotesize{Country-clustered $t$-statistics in parentheses. All columns "
          "also track an indicator for an active IMF-supported arrangement. Commodity terms-of-"
          "trade data: IMF CTOT (Gruss and Kebhaj, 2019). "
          "$^{*},^{**},^{***}$: significant at 10, 5, 1 percent.}",
          "\\end{table}"]
    with open(os.path.join(OUT, "tables_commodity.tex"), "w", encoding="utf-8") as f:
        f.write("\n".join(s) + "\n")
    print("\nsaved output/tables_commodity.tex")


if __name__ == "__main__":
    main()
