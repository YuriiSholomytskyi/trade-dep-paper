"""Riskiness of trade: ranking partners and countries by the insurance quality of demand.

The risk-sharing model says demand from a partner is a good hedge when it is steady, growing, and
uncorrelated with the client's own cycle. The relevant object is the partner's DEMAND FOR IMPORTS,
not its GDP: measured by GDP growth China looks like a fine anchor, but it grew as a producer, so
its import demand, what actually pulls a client's exports, is what matters.

Two outputs:
  1. Partner-quality table: for the major hubs, mean growth and volatility of import demand, and
     the quality ratio (mean/volatility). Contrasted with the GDP-growth ratio that misleads.
  2. Country resilience index: each country's export-share-weighted partner quality, a ranking of
     which economies' trade portfolios best insure them against their own downturns.

Outputs: output/tables_partner_quality.tex, output/figure_resilience.png.
Run: python scripts/trade_resilience.py
"""
import os

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

DATA = os.path.join(os.path.dirname(__file__), "..", "data")
OUT = os.path.join(os.path.dirname(__file__), "..", "output")
EU = ["DEU", "FRA", "ITA", "ESP", "NLD", "BEL", "POL", "AUT", "SWE", "IRL"]
COL = {"US": "tab:blue", "EU": "tab:orange", "CN": "tab:red"}


def import_demand_annual():
    m = pd.read_csv(os.path.join(DATA, "imts_china_share_monthly.csv"))
    m["y"] = m["TIME_PERIOD"].str.slice(0, 4).astype(int)
    return m.groupby(["COUNTRY", "y"])["MG_CIF_USD_G001"].sum().reset_index(name="imp")


def quality(imp, iso, lo=2010, hi=2024):
    """Mean and volatility of annual import-demand growth (percent), excluding the 2020 outlier."""
    if iso == "EU":
        s = (imp[imp.COUNTRY.isin(EU) & imp.y.between(lo, hi)]
             .groupby("y")["imp"].sum())
    else:
        s = imp[(imp.COUNTRY == iso) & imp.y.between(lo, hi)].set_index("y")["imp"]
    s = s[s.index != 2020].sort_index()
    s = s[s > 0]
    if len(s) < 6:
        return np.nan, np.nan
    g = s.pct_change().dropna() * 100
    if len(g) < 5:
        return np.nan, np.nan
    return g.mean(), g.std()


def main():
    imp = import_demand_annual()
    weo = pd.read_csv(os.path.join(DATA, "weo_realgdp_annual.csv"))

    # ---- 1. partner-quality table for the major hubs ----
    hubs = [("United States", "USA"), ("European Union", "EU"), ("China", "CHN"),
            ("Japan", "JPN")]
    qual = {}
    rows = []
    for name, iso in hubs:
        mu, sd = quality(imp, iso)
        qual[iso] = mu / sd if sd and not np.isnan(sd) else np.nan
        # GDP growth ratio for contrast
        if iso == "EU":
            gg = weo[weo.COUNTRY.isin(EU) & weo.year.between(2010, 2024)
                     & (weo.year != 2020)].groupby("year")["ngdp_rpch"].mean()
        else:
            gg = weo[(weo.COUNTRY == iso) & weo.year.between(2010, 2024)
                     & (weo.year != 2020)]["ngdp_rpch"]
        gdp_ratio = gg.mean() / gg.std()
        rows.append((name, mu, sd, mu / sd, gdp_ratio))

    tex = [
        r"\begin{table}[H]", r"\centering\small",
        r"\caption{Insurance quality of the major hubs' demand. Import demand, what pulls a "
        r"client's exports, is steadiest and growing for the United States; China's grows but is "
        r"twice as volatile. Ranking hubs by GDP growth instead (last column) misleads, placing "
        r"China first, because China grew as a producer rather than a consumer.}",
        r"\label{tab:partnerquality}",
        r"\begin{tabularx}{\textwidth}{@{}lYYYY@{}}", r"\toprule",
        r"Hub & Import-demand & Volatility & Quality & GDP-growth \\",
        r" & growth, \% & of demand, \% & (mean/vol.) & ratio \\ \midrule",
    ]
    for name, mu, sd, r, gdpr in rows:
        tex.append(f"{name} & {mu:.1f} & {sd:.1f} & {r:.2f} & {gdpr:.2f} \\\\")
    tex += [
        r"\bottomrule", r"\end{tabularx}",
        r"\\[2pt]\footnotesize{\emph{Source:} IMF IMTS (import demand, total goods imports from the "
        r"world) and WEO (real GDP growth), 2010--2024 excluding the 2020 pandemic outlier. Import "
        r"demand for the European Union aggregates its ten largest members. Quality is mean annual "
        r"growth divided by its standard deviation.}",
        r"\end{table}",
    ]
    with open(os.path.join(OUT, "tables_partner_quality.tex"), "w", encoding="utf-8") as f:
        f.write("\n".join(tex) + "\n")
    print("partner quality (import-demand mean / vol / ratio / GDP-ratio):")
    for name, mu, sd, r, gdpr in rows:
        print(f"  {name:16s} g={mu:5.1f} sd={sd:5.1f} q={r:4.2f}  gdp_ratio={gdpr:4.2f}")

    # ---- 2. country resilience index: export-share-weighted partner quality ----
    # partner quality q_p for every partner with enough import data
    allq = {}
    for p in imp.COUNTRY.unique():
        mu, sd = quality(imp, p)
        if sd and not np.isnan(sd) and sd > 0:
            allq[p] = mu / sd
    b = pd.read_csv(os.path.join(DATA, "imts_bilateral_exports_annual.csv"))
    b = b[b.year.between(2017, 2019)]
    shares = b.groupby(["COUNTRY", "partner"])["exp_usd"].sum().reset_index()
    shares["q"] = shares["partner"].map(allq)
    shares = shares.dropna(subset=["q"])
    res = (shares.groupby("COUNTRY")
           .apply(lambda d: np.average(d["q"], weights=d["exp_usd"]))
           .rename("resilience"))

    hub = pd.read_csv(os.path.join(DATA, "hub_panel.csv"))
    cty_hub = hub.groupby("iso3").hub.agg(lambda s: s.mode().iat[0])
    d = pd.DataFrame({"resilience": res}).join(cty_hub, how="inner").dropna()
    d = d.sort_values("resilience")

    fig, ax = plt.subplots(figsize=(8, 10))
    ax.barh(d.index, d.resilience, color=[COL.get(h, "gray") for h in d.hub])
    ax.set_title("Resilience of the export portfolio:\nexport-share-weighted quality of partner demand")
    ax.set_xlabel("resilience index (higher = better insured against own downturns)")
    ax.tick_params(axis="y", labelsize=6)
    for h, c in COL.items():
        ax.plot([], [], "s", color=c, label={"US": "US hub", "EU": "EU hub", "CN": "China hub"}[h])
    ax.legend(fontsize=8, loc="lower right")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "figure_resilience.png"), dpi=130)
    print("\nsaved output/tables_partner_quality.tex and output/figure_resilience.png")
    print("Most resilient:", list(d.tail(5).index))
    print("Least resilient:", list(d.head(5).index))


if __name__ == "__main__":
    main()
