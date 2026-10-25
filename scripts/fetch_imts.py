"""Pull monthly bilateral trade (to China and World) for all reporters from IMTS,
and compute each country's China trade share. Outputs:
  data/imts_raw_monthly_2015.parquet  - tidy raw obs
  data/imts_china_share_monthly.csv    - wide, with exp_share_chn / imp_share_chn

Run: python scripts/fetch_imts.py
"""
import os
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(__file__))
from imf_sdmx import fetch_data, to_period_dt  # noqa: E402

OUT = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(OUT, exist_ok=True)

# all reporters (*), exports FOB + imports CIF, partner China + World, monthly
KEY = "*.XG_FOB_USD+MG_CIF_USD.CHN+G001.M"
START = "2015-01"


def main():
    df = fetch_data("IMF.STA", "IMTS", KEY, start=START)
    df = df[["COUNTRY", "INDICATOR", "COUNTERPART_COUNTRY", "TIME_PERIOD", "OBS_VALUE"]]
    df.to_parquet(os.path.join(OUT, "imts_raw_monthly_2015.parquet"))

    w = df.pivot_table(index=["COUNTRY", "TIME_PERIOD"],
                       columns=["INDICATOR", "COUNTERPART_COUNTRY"],
                       values="OBS_VALUE", aggfunc="first")
    w.columns = ["_".join(c) for c in w.columns]
    w = w.reset_index()
    w["exp_share_chn"] = w["XG_FOB_USD_CHN"] / w["XG_FOB_USD_G001"]
    w["imp_share_chn"] = w["MG_CIF_USD_CHN"] / w["MG_CIF_USD_G001"]
    w["date"] = to_period_dt(w["TIME_PERIOD"], "M")
    w = w.sort_values(["COUNTRY", "date"])
    w.to_csv(os.path.join(OUT, "imts_china_share_monthly.csv"), index=False)
    print(f"reporters={w.COUNTRY.nunique()} span={w.TIME_PERIOD.min()}..{w.TIME_PERIOD.max()}")


if __name__ == "__main__":
    main()
