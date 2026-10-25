"""Shift-share external-demand pull for crisis countries (Leg-2 rescue channel).

For each crisis episode:
  weight_p   = share of the country's exports going to partner p, mean of yr-3..yr-1
  ext_demand = sum_p weight_p * (partner p real GDP growth, mean of yr..yr+2)
i.e. the demand impulse transmitted to the crisis country through its trade links from
partners that were growing during its recovery window. High ext_demand = healthy anchor
pulling it out (idiosyncratic crisis with a live lifeline).

Output: data/step1_panel_extdemand.csv  (step1 panel + ext_demand, own_growth_partners)
Run: python scripts/build_external_demand.py
"""
import os
import sys

import numpy as np
import pandas as pd

ROOT = os.path.join(os.path.dirname(__file__), "..")
DATA = os.path.join(ROOT, "data")
sys.path.insert(0, os.path.dirname(__file__))
from imf_sdmx import fetch_data  # noqa: E402


def bilateral_exports(reporters):
    """Annual exports (FOB USD) for the given reporters to every partner, 2000+."""
    cache = os.path.join(DATA, "imts_bilateral_exports_annual.csv")
    if os.path.exists(cache):
        return pd.read_csv(cache)
    key = "+".join(sorted(reporters)) + ".XG_FOB_USD.*.A"
    df = fetch_data("IMF.STA", "IMTS", key, start="2000")
    df = df[["COUNTRY", "COUNTERPART_COUNTRY", "TIME_PERIOD", "OBS_VALUE"]]
    df = df.rename(columns={"COUNTERPART_COUNTRY": "partner", "TIME_PERIOD": "year",
                            "OBS_VALUE": "exp_usd"})
    df["year"] = df["year"].astype(int)
    df.to_csv(cache, index=False)
    return df


def main():
    panel = pd.read_csv(os.path.join(DATA, "step1_panel.csv"))
    weo = pd.read_csv(os.path.join(DATA, "weo_realgdp_annual.csv"))
    countries = set(weo.COUNTRY.unique())  # real economies (exclude IMTS aggregates G***)

    epis = panel.dropna(subset=["iso3", "start_year"]).copy()
    epis["start_year"] = epis["start_year"].astype(int)
    bx = bilateral_exports(epis.iso3.unique())
    bx = bx[bx.partner.isin(countries)]  # drop aggregate partners
    growth = weo.set_index(["COUNTRY", "year"])["ngdp_rpch"]

    out = []
    for _, e in epis.iterrows():
        iso, yr = e["iso3"], e["start_year"]
        # pre-crisis export weights to each partner (yr-3..yr-1)
        w = bx[(bx.COUNTRY == iso) & (bx.year.between(yr - 3, yr - 1))]
        w = w.groupby("partner")["exp_usd"].mean()
        w = w[w.index != iso]  # drop self
        if w.sum() <= 0 or w.empty:
            ext = np.nan
        else:
            wn = w / w.sum()
            # partner growth averaged over recovery window yr..yr+2
            pg = {p: growth.reindex([(p, y) for y in range(yr, yr + 3)]).mean()
                  for p in wn.index}
            pg = pd.Series(pg)
            valid = pg.notna()
            ext = float((wn[valid] * pg[valid]).sum() / wn[valid].sum()) if valid.any() else np.nan
        row = e.to_dict()
        row["ext_demand"] = ext
        out.append(row)

    res = pd.DataFrame(out)
    res.to_csv(os.path.join(DATA, "step1_panel_extdemand.csv"), index=False)
    print(f"episodes={len(res)}  with ext_demand={res.ext_demand.notna().sum()}")
    print(res.ext_demand.describe().round(2).to_string())


if __name__ == "__main__":
    main()
