"""Step-1 panel: crisis episodes x recovery speed x pre-crisis trade openness.

Joins:
  laeven_valencia_crisis_dates.csv  (crisis episodes)
  data/weo_realgdp_annual.csv        (real GDP level -> recovery time; USD GDP -> openness)
  data/imts_raw_monthly_2015.parquet (trade to World -> openness; only 2015+ so 2008 crises
                                       lack pre-crisis trade here -> flagged)

Recovery time = first year real GDP regains its pre-crisis peak, minus crisis start year.
Pre-crisis openness = (exports+imports to World, USD) / nominal USD GDP, mean of the
3 years before the crisis.

Output: data/step1_panel.csv
Run: python scripts/build_panel.py
"""
import os
import sys

import numpy as np
import pandas as pd

ROOT = os.path.join(os.path.dirname(__file__), "..")
DATA = os.path.join(ROOT, "data")
sys.path.insert(0, os.path.dirname(__file__))
from imf_sdmx import fetch_data  # noqa: E402

MAX_HORIZON = 12  # years to look for recovery before censoring


def annual_trade_to_world():
    """Annual total trade (exports FOB + imports CIF) to World, USD, from IMTS.
    Pulled at annual frequency back to 2000 so 2008-era crises have pre-crisis openness.
    Cached to data/imts_world_annual.csv.
    """
    cache = os.path.join(DATA, "imts_world_annual.csv")
    if os.path.exists(cache):
        return pd.read_csv(cache)
    df = fetch_data("IMF.STA", "IMTS", "*.XG_FOB_USD+MG_CIF_USD.G001.A", start="2000")
    df = df[["COUNTRY", "INDICATOR", "TIME_PERIOD", "OBS_VALUE"]]
    g = df.pivot_table(index=["COUNTRY", "TIME_PERIOD"], columns="INDICATOR",
                       values="OBS_VALUE", aggfunc="first")
    g["trade_world_usd"] = g.get("XG_FOB_USD", np.nan) + g.get("MG_CIF_USD", np.nan)
    g = g[["trade_world_usd"]].reset_index().rename(columns={"TIME_PERIOD": "year"})
    g["year"] = g["year"].astype(int)
    g.to_csv(cache, index=False)
    return g


def recovery_metrics(gdp_country, crisis_year):
    """Return (recovery_time, output_loss_pct).
    recovery_time = years until real GDP regains its pre-crisis (year-1) level
                    (NaN if censored within horizon).
    output_loss_pct = max % drop of real GDP below the pre-crisis peak within horizon
                      (0 if GDP never fell -> no recession to recover from).
    """
    s = gdp_country.set_index("year")["ngdp_r"].dropna()
    if crisis_year - 1 not in s.index:
        return np.nan, np.nan
    peak = s.loc[crisis_year - 1]
    fut = s[(s.index >= crisis_year) & (s.index <= crisis_year + MAX_HORIZON)]
    if fut.empty:
        return np.nan, np.nan
    output_loss = max(0.0, 100 * (peak - fut.min()) / peak)
    regained = fut[fut >= peak]
    rt = int(regained.index.min() - crisis_year) if len(regained) else np.nan
    return rt, output_loss


def main():
    crises = pd.read_csv(os.path.join(ROOT, "laeven_valencia_crisis_dates.csv"))
    weo = pd.read_csv(os.path.join(DATA, "weo_realgdp_annual.csv"))
    trade = annual_trade_to_world()

    # USD GDP merged with annual trade -> openness
    op = trade.merge(weo[["COUNTRY", "year", "ngdpd_usd"]],
                     left_on=["COUNTRY", "year"], right_on=["COUNTRY", "year"], how="left")
    # Both IMTS trade and WEO NGDPD are in raw USD -> openness is a clean ratio.
    op["openness"] = op["trade_world_usd"] / op["ngdpd_usd"]

    rows = []
    for _, c in crises.iterrows():
        iso, yr, ctype = c["iso3"], c["start_year"], c["crisis_type"]
        if pd.isna(iso) or pd.isna(yr):
            continue
        yr = int(yr)
        gc = weo[weo.COUNTRY == iso]
        if gc.empty:
            continue
        rt, loss = recovery_metrics(gc, yr)
        pre = op[(op.COUNTRY == iso) & (op.year.between(yr - 3, yr - 1))]["openness"]
        rows.append({
            "iso3": iso, "country": c["country"], "crisis_type": ctype,
            "start_year": yr, "recovery_time": rt, "output_loss_pct": loss,
            "pre_openness": pre.mean() if len(pre) else np.nan,
            "n_pre_obs": int(pre.notna().sum()),
        })
    panel = pd.DataFrame(rows)
    panel.to_csv(os.path.join(DATA, "step1_panel.csv"), index=False)
    print(f"episodes={len(panel)}  with recovery_time={panel.recovery_time.notna().sum()}"
          f"  with pre_openness={panel.pre_openness.notna().sum()}")
    print(panel[panel.start_year >= 2015].dropna(subset=['recovery_time']).head(20).to_string())


if __name__ == "__main__":
    main()
