"""Partner-portfolio counterfactual: what is partner choice worth in months of downturn?

For each episode we rebuild the pre-crisis export-share vector and the partners' growth over
the episode window, then rebalance the portfolio and price the change with the estimated
full-cycle coefficients (the Table 1 specification):

  A. "toward hub":  move DELTA of export share to the country's own hub (proportionally
     within the hub's members), funded proportionally from all non-hub partners.
  B. "China to hub": move min(DELTA, China share) specifically from China to the hub.

Delta(months) = sum over partner types of beta_type * Delta(pull_type). This is an accounting
exercise with local, partial-equilibrium coefficients, not a general-equilibrium prediction;
it sizes the estimates, nothing more.

Output: printed distribution + output/tables_counterfactual.tex.
Run: python scripts/counterfactual_rebalance.py
"""
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(__file__))
from build_horserace_hp import build_episodes, ols, ADVANCED, DATA  # noqa: E402
from hub_decomposition import HUBS  # noqa: E402

OUT = os.path.join(os.path.dirname(__file__), "..", "output")
DELTA = 0.05


def ptype(p):
    if p == "USA":
        return "us_pull"
    if p == "CHN":
        return "china_pull"
    return "otheradv_pull" if p in ADVANCED else "emer_pull"


def main():
    ep = build_episodes()

    # betas from the full sample, the exact Table 1 full-cycle specification
    parts = ["us_pull", "otheradv_pull", "emer_pull", "china_pull"]
    res = ols(ep, "t_full", parts + ["trade_open", "depth_gap", "program"])
    beta = {nm: b for nm, b, se in res[0]}
    print("full-cycle betas:", {k: round(beta[k], 2) for k in parts})

    hub = pd.read_csv(os.path.join(DATA, "hub_panel.csv"))[["iso3", "peak_year", "hub", "hub_share"]]
    hub = hub.drop_duplicates(["iso3", "peak_year"])
    ep = ep.drop_duplicates(["iso3", "peak_year"]).merge(hub, on=["iso3", "peak_year"], how="left")

    cw = pd.read_csv(os.path.join(DATA, "ifs_iso3_crosswalk.csv"))
    real = set(cw.iso3)
    bx = pd.read_csv(os.path.join(DATA, "imts_bilateral_sa.csv"))
    bx = bx[bx.partner.isin(real)]
    weo = pd.read_csv(os.path.join(DATA, "weo_realgdp_annual.csv"))
    growth = weo[weo.COUNTRY.isin(real)].set_index(["COUNTRY", "year"])["ngdp_rpch"]

    def episode_portfolio(iso, yr):
        w = bx[(bx.iso3 == iso) & (bx.year.between(yr - 3, yr - 1))].groupby("partner").exp.mean()
        w = w[(w.index != iso) & (w > 0)]
        if w.empty:
            return None, None
        yrs = list(range(yr, yr + 3))
        pg = pd.Series({p: growth.reindex([(p, y) for y in yrs]).mean() for p in w.index})
        v = pg.notna()
        if not v.any():
            return None, None
        return w[v] / w[v].sum(), pg[v]

    def price(dw, pg):
        """Months from a share change dw (Series over partners) at partner growth pg."""
        dpull = {}
        for p, d in dw.items():
            dpull[ptype(p)] = dpull.get(ptype(p), 0.0) + d * pg[p]
        return sum(beta[t] * v for t, v in dpull.items())

    rows = []
    for _, r in ep.iterrows():
        if r.hub not in HUBS:
            continue
        wn, pg = episode_portfolio(r.iso3, int(r.peak_year))
        if wn is None:
            continue
        hub_set = wn.index.isin(HUBS[r.hub])
        w_hub = wn[hub_set].sum()
        if w_hub <= 0 or w_hub >= 1 - DELTA:
            continue
        # A: DELTA toward hub, funded proportionally from all non-hub partners
        dw = pd.Series(0.0, index=wn.index)
        dw[hub_set] = DELTA * wn[hub_set] / w_hub
        dw[~hub_set] = -DELTA * wn[~hub_set] / (1 - w_hub)
        m_hub = price(dw, pg)
        # B: from China specifically to the hub
        w_chn = float(wn.get("CHN", 0.0))
        m_chn = np.nan
        if w_chn > 0.005 and "CHN" not in HUBS[r.hub]:
            d = min(DELTA, w_chn)
            dw2 = pd.Series(0.0, index=wn.index)
            dw2[hub_set] = d * wn[hub_set] / w_hub
            dw2["CHN"] = -d
            m_chn = price(dw2, pg)
        rows.append({"iso3": r.iso3, "peak_year": r.peak_year, "hub": r.hub,
                     "m_hub": m_hub, "m_chn": m_chn})
    cf = pd.DataFrame(rows)
    print(f"\nepisodes priced: {len(cf)}")

    def stats(s):
        s = s.dropna()
        return len(s), s.median(), s.quantile(.25), s.quantile(.75)

    lines = []
    for label, col, sub in [
            ("Toward own hub, all economies", "m_hub", cf),
            ("\\quad US-hub economies", "m_hub", cf[cf.hub == "US"]),
            ("\\quad EU-hub economies", "m_hub", cf[cf.hub == "EU"]),
            ("From China to own hub (China share $>0.5$\\%)", "m_chn", cf),
            ("\\quad US-hub economies", "m_chn", cf[cf.hub == "US"]),
            ("\\quad EU-hub economies", "m_chn", cf[cf.hub == "EU"])]:
        n, med, q1, q3 = stats(sub[col])
        print(f"{label:50s} n={n:3d} median={med:6.2f} IQR=[{q1:5.2f},{q3:5.2f}]")
        lines.append(f"{label} & {n} & ${med:.1f}$ & $[{q1:.1f},\\ {q3:.1f}]$ \\\\")

    tex = [
        r"\begin{table}[H]", r"\centering\small",
        r"\caption{A partner-portfolio counterfactual: months of full negative cycle saved by "
        r"moving five percentage points of the pre-crisis export-share portfolio, priced with "
        r"the full-cycle coefficients of Table~\ref{tab:main} at each episode's realised partner "
        r"growth. Negative values are months saved. An accounting exercise with local, "
        r"partial-equilibrium coefficients, not a general-equilibrium prediction.}",
        r"\label{tab:counterfactual}",
        r"\begin{tabularx}{\textwidth}{@{}lYYY@{}}", r"\toprule",
        r"Rebalancing & Episodes & Median months & Interquartile range \\ \midrule",
        *lines[:3], r"\midrule", *lines[3:],
        r"\bottomrule", r"\end{tabularx}",
        r"\\[2pt]\footnotesize{The move toward the hub is funded proportionally from all "
        r"non-hub partners (upper panel) or from the China share alone, capped at that share "
        r"(lower panel). The 219 observations in the upper panel correspond to the 219 unique "
        r"country-by-peak-year export portfolios across the 263 episodes (69 US-hub, 146 EU-hub, "
        r"and 4 China-hub in Mongolia); the lower panel restricts to portfolios with a "
        r"pre-downturn China export share exceeding 0.5 percent.}",
        r"\end{table}",
    ]
    with open(os.path.join(OUT, "tables_counterfactual.tex"), "w", encoding="utf-8") as f:
        f.write("\n".join(tex) + "\n")
    cf.to_csv(os.path.join(DATA, "counterfactual_rebalance.csv"), index=False)
    print("\nsaved output/tables_counterfactual.tex, data/counterfactual_rebalance.csv")


if __name__ == "__main__":
    main()
