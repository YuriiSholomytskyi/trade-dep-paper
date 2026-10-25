"""Global- and regional-cycle controls for the US-demand result (referee point II.2 / X).

The identification worry is that the US-demand pull proxies for the common global cycle rather than
for demand specific to a country's US exposure. This script re-estimates the full-cycle horse race
with, in turn:

  (a) baseline (reproduces the full-cycle column of Table~\\ref{tab:main});
  (b) + world real-GDP growth excluding the United States (GDP-weighted, same peak..peak+2 window);
  (c) + own-region growth (GDP-weighted, leave-own-country-out, same window);
  (d) + peak-year fixed effects (common episode-onset effects: these absorb ALL factors common
      across countries in a given year -- world growth, global financial conditions, commodity
      prices, the 2009 and 2020 shocks -- so the US pull is identified purely off the cross-country
      variation in US export shares); and
  (e) all controls together.

If the US pull survives (b)-(e), the estimate is not merely the global cycle re-labelled.

Output: prints the US full-cycle coefficient under each control; writes output/tables_globalctrl.tex.
Run: python scripts/global_controls.py
"""
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(__file__))
from build_horserace_hp import build_episodes, ols, DATA  # noqa: E402

OUT = os.path.join(os.path.dirname(__file__), "..", "output")
XS = ["us_pull", "otheradv_pull", "emer_pull", "china_pull", "trade_open", "depth_gap", "program"]

# Region map for the 34 sample economies (leave-own-out regional growth is built from these).
REGION = {
    "CRI": "LAC", "ECU": "LAC", "SLV": "LAC", "PRY": "LAC", "SUR": "LAC", "DOM": "LAC",
    "PAN": "LAC", "COL": "LAC", "PER": "LAC", "ARG": "LAC", "NIC": "LAC", "MEX": "LAC",
    "CHL": "LAC",
    "POL": "ECA", "KGZ": "ECA", "MDA": "ECA", "SRB": "ECA", "ARM": "ECA", "LVA": "ECA",
    "BLR": "ECA", "BIH": "ECA", "UKR": "ECA", "ROU": "ECA", "HUN": "ECA",
    "RWA": "SSA", "MOZ": "SSA", "SYC": "SSA", "SEN": "SSA",
    "TUN": "MENA", "EGY": "MENA", "JOR": "MENA",
    "BGD": "SAS", "PAK": "SAS",
    "MNG": "EAP",
}


def us_coef(ep, extra):
    res = ols(ep, "t_full", XS + extra)
    if not res:
        return None
    d = {k: (b, s) for k, b, s in res[0]}
    b, s = d["us_pull"]
    return b, b / s, res[2], res[3]


def main():
    ep = build_episodes()
    cw = pd.read_csv(os.path.join(DATA, "ifs_iso3_crosswalk.csv"))
    real = set(cw.iso3)
    weo = pd.read_csv(os.path.join(DATA, "weo_realgdp_annual.csv"))
    weo = weo[weo.COUNTRY.isin(real)].copy()

    # ---- world growth excluding the US: GDP-weighted mean of ngdp_rpch by calendar year ----
    def wmean(df, gcol="ngdp_rpch", wcol="ngdpd_usd"):
        d = df.dropna(subset=[gcol, wcol])
        d = d[d[wcol] > 0]
        return np.average(d[gcol], weights=d[wcol]) if len(d) else np.nan

    exus = weo[weo.COUNTRY != "USA"]
    world_ex_us = {y: wmean(exus[exus.year == y]) for y in range(2000, 2028)}

    # region-year GDP-weighted growth, and per-country GDP weight, for leave-own-out
    weo["region"] = weo.COUNTRY.map(REGION)
    g = weo.set_index(["COUNTRY", "year"])["ngdp_rpch"]
    wt = weo.set_index(["COUNTRY", "year"])["ngdpd_usd"]

    def window_avg(series_by_year, yr):
        vals = [series_by_year.get(y, np.nan) for y in (yr, yr + 1, yr + 2)]
        vals = [v for v in vals if v == v]
        return float(np.mean(vals)) if vals else np.nan

    def regional_growth(iso, yr):
        reg = REGION.get(iso)
        if reg is None:
            return np.nan
        peers = [c for c, r in REGION.items() if r == reg and c != iso]
        if not peers:
            return np.nan
        yr_vals = []
        for y in (yr, yr + 1, yr + 2):
            num = den = 0.0
            for c in peers:
                gv, wv = g.get((c, y), np.nan), wt.get((c, y), np.nan)
                if gv == gv and wv == wv and wv > 0:
                    num += gv * wv
                    den += wv
            if den > 0:
                yr_vals.append(num / den)
        return float(np.mean(yr_vals)) if yr_vals else np.nan

    ep["world_ex_us"] = [window_avg(world_ex_us, int(r.peak_year)) for _, r in ep.iterrows()]
    ep["region_growth"] = [regional_growth(r.iso3, int(r.peak_year)) for _, r in ep.iterrows()]

    # peak-year fixed effects (drop the first year to avoid collinearity with the constant)
    yrs = sorted(ep.peak_year.unique())[1:]
    yr_dummies = []
    for y in yrs:
        c = f"yr_{y}"
        ep[c] = (ep.peak_year == y).astype(float)
        yr_dummies.append(c)

    specs = [
        ("Baseline (Table 1 full cycle)", []),
        ("+ world growth ex-US", ["world_ex_us"]),
        ("+ own-region growth", ["region_growth"]),
        ("+ peak-year fixed effects", yr_dummies),
        ("+ all controls", ["world_ex_us", "region_growth"] + yr_dummies),
    ]

    print("US-demand pull on the full negative cycle, with global/regional controls")
    print(f"{'specification':32s} {'US beta':>9s} {'t':>7s} {'n':>5s} {'clu':>5s}")
    rows = []
    for label, extra in specs:
        r = us_coef(ep, extra)
        if r is None:
            print(f"{label:32s}   (insufficient obs)")
            continue
        b, t, n, G = r
        print(f"{label:32s} {b:9.2f} {t:7.2f} {n:5d} {G:5d}")
        star = "***" if abs(t) > 2.58 else "**" if abs(t) > 1.96 else "*" if abs(t) > 1.64 else ""
        val = f"${b:.1f}^{{{star}}}$" if star else f"${b:.1f}$"
        rows.append(f"{label} & {val} {{\\scriptsize$({t:.1f})$}} & {n} \\\\")

    tex = [
        r"\begin{table}[H]", r"\centering\small",
        r"\caption{The US-demand result under global- and regional-cycle controls. The dependent "
        r"variable is the full negative cycle in months; each cell is the US-demand coefficient with "
        r"its country-clustered $t$-statistic, from the four-partner horse race of "
        r"Table~\ref{tab:main} augmented with the control shown. World growth ex-US and own-region "
        r"growth are GDP-weighted over the same peak-to-peak$+2$ window; own-region growth leaves "
        r"the country out. Peak-year fixed effects absorb every factor common across countries in a "
        r"year, so the US pull is then identified only off the cross-country variation in US export "
        r"shares.}",
        r"\label{tab:globalctrl}",
        r"\begin{tabularx}{\textwidth}{@{}lYc@{}}", r"\toprule",
        r"Specification & US-demand pull & Episodes \\ \midrule",
        *rows,
        r"\bottomrule", r"\end{tabularx}",
        r"\\[2pt]\footnotesize{All specifications also include the other-advanced, emerging, and "
        r"China pulls, trade openness, shock depth, and the active-arrangement indicator. "
        r"$^{*}$, $^{**}$, $^{***}$: significance at 10, 5, 1 percent.}",
        r"\end{table}",
    ]
    with open(os.path.join(OUT, "tables_globalctrl.tex"), "w", encoding="utf-8") as f:
        f.write("\n".join(tex) + "\n")
    print("\nsaved output/tables_globalctrl.tex")


if __name__ == "__main__":
    main()
