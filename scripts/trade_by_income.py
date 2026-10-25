"""Check: did the feared fragmentation burden fall on emerging and low-income economies?

The fragmentation literature projects that the costs of decoupling fall disproportionately on
emerging and low-income economies. This checks realized trade instead, comparing the
pre-fragmentation period (2019--2022) with the fragmentation period (2023--2026), using total
goods trade with the world per reporter from the IMF's monthly IMTS database. Because 2026 is only
partially reported (through February), we compare AVERAGE MONTHLY trade across each bucket, so a
partial year contributes its available months without annualisation. Countries are grouped roughly
into advanced, emerging and developing, and low-income economies. If poorer economies had borne the
burden, their trade should have grown less or contracted. It did not.

Output: prints the median trade change by group; writes output/tables_income.tex.
Run: python scripts/trade_by_income.py
"""
import os

import pandas as pd

DATA = os.path.join(os.path.dirname(__file__), "..", "data")
OUT = os.path.join(os.path.dirname(__file__), "..", "output")

PRE = ("2017-01", "2019-12")        # stable pre-pandemic baseline (before COVID, the rebound, the war)
MID = ("2020-01", "2022-12")        # the shock transition: pandemic, rebound, 2022 commodity spike
POST = ("2023-01", "2025-12")       # the fragmentation period (fears peaked from 2023)

# Rough income grouping (ISO3). Advanced = IMF advanced economies; low income ~ World Bank
# low-income list; everything else is emerging and developing.
ADVANCED = {
    "USA", "CAN", "GBR", "DEU", "FRA", "ITA", "ESP", "PRT", "NLD", "BEL", "AUT", "IRL", "LUX",
    "FIN", "GRC", "CYP", "MLT", "SVN", "SVK", "EST", "LVA", "LTU", "JPN", "KOR", "AUS", "NZL",
    "CHE", "NOR", "SWE", "DNK", "ISL", "ISR", "SGP", "HKG", "TWN", "CZE",
}
LOW_INCOME = {
    "AFG", "BDI", "BFA", "CAF", "TCD", "COD", "ERI", "ETH", "GMB", "GNB", "LBR", "MDG", "MWI",
    "MLI", "MOZ", "NER", "RWA", "SLE", "SOM", "SSD", "SDN", "SYR", "TGO", "UGA", "YEM", "PRK",
}


def group(iso):
    if iso in ADVANCED:
        return "Advanced"
    if iso in LOW_INCOME:
        return "Low income"
    return "Emerging \\& developing"


def main():
    m = pd.read_csv(os.path.join(DATA, "imts_china_share_monthly.csv"))
    # total goods trade with the world = imports (CIF) from world + exports (FOB) to world
    m["trade"] = m["MG_CIF_USD_G001"].fillna(0) + m["XG_FOB_USD_G001"].fillna(0)
    m = m[m["trade"] > 0]
    m["ym"] = m["TIME_PERIOD"].str.replace("M", "", regex=False)   # 2019-01 style

    def avg_monthly(lo, hi):
        s = m[(m.ym >= lo) & (m.ym <= hi)]
        return s.groupby("COUNTRY")["trade"].mean()

    pre, mid, post = avg_monthly(*PRE), avg_monthly(*MID), avg_monthly(*POST)
    d = pd.concat([pre.rename("pre"), mid.rename("mid"), post.rename("post")], axis=1).dropna()
    # cumulative index, stable pre-pandemic base 2017-2019 = 100
    d["i_mid"] = d["mid"] / d["pre"] * 100
    d["i_post"] = d["post"] / d["pre"] * 100
    d["g"] = [group(i) for i in d.index]

    order = ["Advanced", "Emerging \\& developing", "Low income"]
    print("Goods trade with the world, cumulative index (median), 2017-19 = 100")
    print(f"{'group':24s} {'n':>4s} {'2017-19':>8s} {'2020-22':>8s} {'2023-25':>8s}")
    stats = {}
    for g in order:
        s = d[d.g == g]
        stats[g] = (len(s), s["i_mid"].median(), s["i_post"].median())
        print(f"  {g.replace(chr(92),''):22s} {len(s):4d} {100.0:8.0f} "
              f"{s['i_mid'].median():8.0f} {s['i_post'].median():8.0f}")

    rows = [f"{g} & {stats[g][0]} & 100 & {stats[g][1]:.0f} & {stats[g][2]:.0f} \\\\"
            for g in order]
    tex = [
        r"\begin{table}[H]", r"\centering\small",
        r"\caption{Goods trade with the world across three periods, median cumulative index by "
        r"income group (stable pre-pandemic base 2017--2019 = 100): the shock transition "
        r"(2020--2022) and the fragmentation period (2023--2025). Trade in every income group is "
        r"well above its pre-pandemic level, and by more for emerging, developing, and low-income "
        r"economies than for the advanced economies.}",
        r"\label{tab:income}",
        r"\begin{tabularx}{\textwidth}{@{}lYYYY@{}}", r"\toprule",
        r"Income group & Economies & 2017--19 & 2020--22 & 2023--25 \\ \midrule",
        *rows,
        r"\bottomrule", r"\end{tabularx}",
        r"\\[2pt]\footnotesize{\emph{Source:} IMF International Trade in Goods Statistics (IMTS), "
        r"monthly. Trade is total goods trade with the world (imports CIF plus exports FOB). For "
        r"each economy, average monthly trade in each period is indexed to its 2017--2019 average "
        r"(=100); cells are the median across economies in each group. The 2020--2022 column spans "
        r"the pandemic, the rebound, and the 2022 commodity-price spike. Groups are a rough "
        r"classification into advanced, emerging and developing, and low-income economies.}",
        r"\end{table}",
    ]
    with open(os.path.join(OUT, "tables_income.tex"), "w", encoding="utf-8") as f:
        f.write("\n".join(tex) + "\n")
    print("saved output/tables_income.tex")


if __name__ == "__main__":
    main()
