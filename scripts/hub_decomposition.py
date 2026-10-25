"""Hub test: each economy recovers through the demand of its OWN regional hub.
Assign every country to the hub it exports most to (US / Europe / China), then split the
partner-demand pull into own-hub vs non-hub, and show own-hub demand drives recovery across
blocs. This turns the 'US result is concentrated in the US bloc' diagnostic into the central
mechanism: it is a hub effect, and it holds for every hub.
Run: python scripts/hub_decomposition.py
"""
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(__file__))
from build_horserace_hp import build_episodes, ols, show  # noqa: E402

DATA = os.path.join(os.path.dirname(__file__), "..", "data")

US_HUB = {"USA"}
EU_HUB = {"AUT", "BEL", "BGR", "HRV", "CYP", "CZE", "DNK", "EST", "FIN", "FRA", "DEU",
          "GRC", "HUN", "IRL", "ITA", "LVA", "LTU", "LUX", "MLT", "NLD", "POL", "PRT",
          "ROU", "SVK", "SVN", "ESP", "SWE", "GBR", "CHE", "NOR"}
CN_HUB = {"CHN"}
HUBS = {"US": US_HUB, "EU": EU_HUB, "CN": CN_HUB}


def main():
    ep = build_episodes()
    cw = pd.read_csv(os.path.join(DATA, "ifs_iso3_crosswalk.csv"))
    weo = pd.read_csv(os.path.join(DATA, "weo_realgdp_annual.csv"))
    real = set(cw.iso3)
    growth = weo[weo.COUNTRY.isin(real)].set_index(["COUNTRY", "year"])["ngdp_rpch"]
    bx = pd.read_csv(os.path.join(DATA, "imts_bilateral_sa.csv"))
    bx = bx[bx.partner.isin(real)]

    def pulls(iso, yr):
        w = bx[(bx.iso3 == iso) & (bx.year.between(yr - 3, yr - 1))].groupby("partner").exp.mean()
        w = w[(w.index != iso) & (w > 0)]
        if w.empty:
            return None
        pg = pd.Series({p: growth.reindex([(p, y) for y in range(yr, yr + 3)]).mean()
                        for p in w.index})
        v = pg.notna()
        if not v.any():
            return None
        wn = w[v] / w[v].sum()
        contrib = wn * pg[v]
        # export SHARE to each hub (assign hub by max share)
        shares = {h: float(wn[wn.index.isin(s)].sum()) for h, s in HUBS.items()}
        hub = max(shares, key=shares.get)
        hub_pull = float(contrib[contrib.index.isin(HUBS[hub])].sum())
        nonhub_pull = float(contrib.sum()) - hub_pull
        return hub, shares[hub], hub_pull, nonhub_pull

    res = [pulls(r.iso3, int(r.peak_year)) for _, r in ep.iterrows()]
    ep[["hub", "hub_share", "hub_pull", "nonhub_pull"]] = pd.DataFrame(
        [r if r else (None, np.nan, np.nan, np.nan) for r in res], index=ep.index)
    ep = ep.dropna(subset=["hub_pull"])

    # hub assignment counts (by episode and by country)
    bycty = ep.groupby("iso3").hub.agg(lambda s: s.mode().iat[0])
    print("Hub assignment (countries):")
    for h in ["US", "EU", "CN"]:
        print(f"  {h}: {sorted(bycty[bycty == h].index)}")
    print(f"\nMedian own-hub export share: {ep.hub_share.median():.0%}")

    print("\n=== Own-hub vs non-hub demand pull, country-clustered ===")
    show(ols(ep, "t_climb", ["hub_pull", "nonhub_pull", "trade_open", "depth_gap"]),
         "CLIMB (trough->peak)")
    show(ols(ep, "t_full", ["hub_pull", "nonhub_pull", "trade_open", "depth_gap"]),
         "FULL cycle")

    # per-bloc: own-hub demand within each bloc
    print("\n=== Own-hub demand, within each bloc (full cycle) ===")
    for h in ["US", "EU", "CN"]:
        sub = ep[ep.hub == h]
        if sub.iso3.nunique() < 4:
            print(f"  {h}: too few countries ({sub.iso3.nunique()})"); continue
        r = ols(sub, "t_full", ["hub_pull", "trade_open", "depth_gap"])
        if r:
            coefs, r2, n, G = r
            b, se = dict((x[0], (x[1], x[2])) for x in coefs)["hub_pull"]
            print(f"  {h}-hub bloc (n={n}, {G} countries): own-hub pull = {b:.2f} (t={b/se:.2f})")

    ep.to_csv(os.path.join(DATA, "hub_panel.csv"), index=False)


if __name__ == "__main__":
    main()
