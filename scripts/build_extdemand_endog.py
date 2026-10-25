"""Add the external-demand (healthy-partner pull) measure to the endogenous downturn
episodes, then re-run Leg 2 of the horse race. This is the decisive test: generic trade
openness amplifies/slows (Rodrik), but the thesis is that demand pull from GROWING partners
speeds recovery.

ext_demand(episode) = sum_p w_p * (partner p real GDP growth over peak_year..peak_year+2),
  w_p = share of the country's exports to partner p, pre-downturn (peak_year-3..peak_year-1).
Run: python scripts/build_extdemand_endog.py
"""
import os
import sys

import numpy as np
import pandas as pd

DATA = os.path.join(os.path.dirname(__file__), "..", "data")
sys.path.insert(0, os.path.dirname(__file__))
from imf_sdmx import fetch_data  # noqa: E402
from build_horserace_monthly import ols, show  # noqa: E402


def bilateral(reporters):
    cache = os.path.join(DATA, "imts_bilateral_sa.csv")
    if os.path.exists(cache):
        return pd.read_csv(cache)
    key = "+".join(sorted(reporters)) + ".XG_FOB_USD.*.A"
    df = fetch_data("IMF.STA", "IMTS", key, start="2000")[
        ["COUNTRY", "COUNTERPART_COUNTRY", "TIME_PERIOD", "OBS_VALUE"]]
    df.columns = ["iso3", "partner", "year", "exp"]
    df["year"] = df.year.astype(int)
    df.to_csv(cache, index=False)
    return df


def main():
    ep = pd.read_csv(os.path.join(DATA, "horserace_endog.csv"))
    weo = pd.read_csv(os.path.join(DATA, "weo_realgdp_annual.csv"))
    countries = set(weo.COUNTRY.unique())
    growth = weo.set_index(["COUNTRY", "year"])["ngdp_rpch"]

    bx = bilateral(ep.iso3.unique())
    bx = bx[bx.partner.isin(countries)]

    def extdem(iso, yr):
        w = bx[(bx.iso3 == iso) & (bx.year.between(yr - 3, yr - 1))].groupby("partner").exp.mean()
        w = w[(w.index != iso) & (w > 0)]
        if w.empty:
            return np.nan
        wn = w / w.sum()
        pg = pd.Series({p: growth.reindex([(p, y) for y in range(yr, yr + 3)]).mean()
                        for p in wn.index})
        v = pg.notna()
        return float((wn[v] * pg[v]).sum() / wn[v].sum()) if v.any() else np.nan

    ep["ext_demand"] = [extdem(r.iso3, int(r.peak_year)) for _, r in ep.iterrows()]
    ep.to_csv(os.path.join(DATA, "horserace_endog_extdemand.csv"), index=False)
    print(f"episodes with ext_demand: {ep.ext_demand.notna().sum()}/{len(ep)}; "
          f"median partner-growth pull={ep.ext_demand.median():.2f}%")

    # Leg 2 with the HEALTHY-PARTNER channel
    show(ols(ep, "recov_m", ["ext_demand", "program", "depth_m"]),
         "LEG 2  recovery MONTHS ~ ext_demand(partner growth) + program + depth")
    show(ols(ep, "recov_m", ["ext_demand", "trade_open", "program", "prog_x_open", "depth_m"]),
         "LEG 2+ recovery MONTHS ~ ext_demand + trade_open + program + prog x open + depth")
    # and does the partner pull reduce the DEPTH too?
    show(ols(ep, "depth_m", ["ext_demand", "fin_open", "trade_open"]),
         "LEG 1+ shock DEPTH ~ ext_demand + fin_openness + trade_openness")


if __name__ == "__main__":
    main()
