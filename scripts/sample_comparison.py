"""Sample-selection diagnostic (referee: the 34-economy sample conditions on a history of IMF
arrangements and on usable monthly data, so it may differ systematically from other EMDEs).

We compare three groups on predetermined observables over 2005-2024:
  (1) Included    : the 34 economies in the estimation sample (a qualifying downturn + monthly data);
  (2) MONA, excl. : the other MONA economies (an arrangement 2005-2025) not in the estimation sample;
  (3) Other EMDE  : emerging and developing economies with no MONA arrangement in the window.
Observables: economy size (GDP, USD bn), trade openness (trade/GDP), mean real GDP growth, growth
volatility (SD of annual growth), and the share that are commodity exporters. A final column reports
the included-vs-other-EMDE difference with a two-sample t-statistic, so the reader can see on which
dimensions the sample is and is not special.
Run: python scripts/sample_comparison.py
"""
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(__file__))
from build_horserace_hp import ADVANCED, COMMODITY  # noqa: E402

DATA = os.path.join(os.path.dirname(__file__), "..", "data")
OUT = os.path.join(os.path.dirname(__file__), "..", "output")
Y0, Y1 = 2005, 2024


def country_panel():
    weo = pd.read_csv(os.path.join(DATA, "weo_realgdp_annual.csv"))
    weo = weo[(weo.year >= Y0) & (weo.year <= Y1)]
    tw = pd.read_csv(os.path.join(DATA, "imts_world_annual.csv"))
    tw = tw[(tw.year >= Y0) & (tw.year <= Y1)]
    cw = pd.read_csv(os.path.join(DATA, "ifs_iso3_crosswalk.csv"))
    real = set(cw.iso3)

    m = weo.merge(tw, on=["COUNTRY", "year"], how="left")
    m = m[m.COUNTRY.isin(real)]
    m["open"] = m.trade_world_usd / m.ngdpd_usd
    g = m.groupby("COUNTRY").agg(
        gdp_usd=("ngdpd_usd", "mean"),
        open=("open", "mean"),
        g_mean=("ngdp_rpch", "mean"),
        g_vol=("ngdp_rpch", "std"),
    ).reset_index().rename(columns={"COUNTRY": "iso3"})
    g = g.dropna(subset=["gdp_usd", "g_mean"])
    g = g[g.gdp_usd > 0]
    g["commodity"] = g.iso3.isin(COMMODITY).astype(int)
    return g


def main():
    g = country_panel()

    included = set(pd.read_csv(os.path.join(DATA, "horserace_hp.csv")).iso3.unique())
    cw = pd.read_csv(os.path.join(DATA, "ifs_iso3_crosswalk.csv"))
    ifs2iso = dict(zip(cw.ifs.astype(str), cw.iso3))
    mona = pd.read_csv(os.path.join(DATA, "mona_arrangements.csv"))
    mona_iso = set(mona.country_code.astype("Int64").astype(str).map(ifs2iso).dropna())

    def group(iso):
        if iso in included:
            return "Included (34)"
        if iso in mona_iso:
            return "MONA, excluded"
        if iso not in ADVANCED:
            return "Other EMDE"
        return "Advanced"

    g["grp"] = g.iso3.map(group)
    g = g[g.grp != "Advanced"]

    # crisis severity for the included group (episode depth), reported in text/footnote
    hp = pd.read_csv(os.path.join(DATA, "horserace_hp.csv"))
    incl_depth = hp.depth_gap.mean()

    VARS = [("Economies", None), ("GDP (USD bn)", "gdp_usd"), ("Trade openness", "open"),
            ("Real GDP growth (\\%)", "g_mean"), ("Growth volatility", "g_vol"),
            ("Commodity exporters (\\%)", "commodity")]
    order = ["Included (34)", "MONA, excluded", "Other EMDE"]

    def stat(sub, var):
        if var == "gdp_usd":
            return sub[var].median() / 1e9   # median size, USD bn
        if var == "commodity":
            return 100 * sub[var].mean()
        return sub[var].median()

    print(f"{'Variable':26s}" + "".join(f"{o:>18s}" for o in order) + f"{'Incl - OtherEMDE':>22s}")
    rows = {o: g[g.grp == o] for o in order}
    texrows = []
    for label, var in VARS:
        if var is None:
            cells = [f"{len(rows[o])}" for o in order]
            print(f"{label:26s}" + "".join(f"{c:>18s}" for c in cells) + f"{'':>22s}")
            texrows.append(f"{label} & " + " & ".join(cells) + " & \\\\")
            continue
        cells = [f"{stat(rows[o], var):.1f}" for o in order]
        a, b = rows["Included (34)"][var].dropna(), rows["Other EMDE"][var].dropna()
        # size is right-skewed (non-MONA EMDEs include China, India), so test it in logs;
        # commodity is a 0/1 share reported in percentage points.
        if var == "gdp_usd":
            a, b = np.log10(a), np.log10(b)
        elif var == "commodity":
            a, b = a * 100, b * 100
        diff = a.mean() - b.mean()
        sp = np.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b))
        t = diff / sp if sp else 0
        star = "***" if abs(t) > 2.58 else "**" if abs(t) > 1.96 else "*" if abs(t) > 1.64 else ""
        print(f"{label:26s}" + "".join(f"{c:>18s}" for c in cells)
              + f"{diff:>14.1f} (t={t:4.1f}){star}")
        texrows.append(f"{label} & " + " & ".join(cells)
                       + f" & ${diff:.1f}^{{{star}}}$ ".replace("^{}", "")
                       + f"{{\\scriptsize$({t:.1f})$}} \\\\")
    print(f"\nIncluded-group mean episode depth (HP gap, %): {incl_depth:.1f}")

    tex = [
        r"\begin{table}[H]", r"\centering\small",
        r"\caption{Sample selection: the estimation sample against other MONA economies and other "
        r"emerging and developing economies. Entries are group medians over 2005--2024 (shares in "
        r"percent); the last column is the difference in means between the included economies and "
        r"other EMDEs, with a two-sample $t$-statistic. The sample resembles other EMDEs in average "
        r"growth and trade openness, is modestly larger, and is if anything slightly less "
        r"growth-volatile, so it is not a selection of the most crisis-prone economies. It does "
        r"over-represent "
        r"commodity exporters, which the analysis controls for directly.}",
        r"\label{tab:samplecomp}",
        r"\begin{tabularx}{\textwidth}{@{}lYYYr@{}}", r"\toprule",
        r"& Included (34) & MONA, excl. & Other EMDE & Incl.$-$Other \\ \midrule",
        *texrows,
        r"\bottomrule", r"\end{tabularx}",
        r"\\[2pt]\footnotesize{GDP is the period-median nominal dollar GDP; trade openness is "
        r"goods trade over GDP; growth volatility is the standard deviation of annual real GDP "
        r"growth. Commodity exporters are fuel, metals, or agricultural exporters; the size "
        r"difference is tested in $\log_{10}$ dollars because the other-EMDE group includes very "
        r"large economies. Advanced "
        r"economies are excluded. The included group's mean episode depth is "
        f"{incl_depth:.1f}"
        r"~percent of the output gap. $^{*}$, $^{**}$, $^{***}$: 10, 5, 1 percent.}",
        r"\end{table}",
    ]
    with open(os.path.join(OUT, "tables_samplecomp.tex"), "w", encoding="utf-8") as f:
        f.write("\n".join(tex) + "\n")
    print("\nsaved output/tables_samplecomp.tex")


if __name__ == "__main__":
    main()
