"""Pull annual GDP series from WEO for all countries.
  NGDP_R    - real GDP, constant prices, domestic currency (level -> time-to-recover)
  NGDP_RPCH - real GDP growth, percent change
  NGDPD     - nominal GDP, current prices, US dollar (denominator for trade openness)

Output: data/weo_realgdp_annual.csv  (COUNTRY, year, ngdp_r, ngdp_rpch, ngdpd_usd)
Run: python scripts/fetch_weo.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from imf_sdmx import fetch_data  # noqa: E402

OUT = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(OUT, exist_ok=True)

KEY = "*.NGDP_R+NGDP_RPCH+NGDPD.A"


def main():
    df = fetch_data("IMF.RES", "WEO", KEY)
    df = df[["COUNTRY", "INDICATOR", "TIME_PERIOD", "OBS_VALUE"]]
    w = df.pivot_table(index=["COUNTRY", "TIME_PERIOD"], columns="INDICATOR",
                       values="OBS_VALUE", aggfunc="first").reset_index()
    w = w.rename(columns={"TIME_PERIOD": "year", "NGDP_R": "ngdp_r",
                          "NGDP_RPCH": "ngdp_rpch", "NGDPD": "ngdpd_usd"})
    w["year"] = w["year"].astype(int)
    w = w.sort_values(["COUNTRY", "year"])
    w.to_csv(os.path.join(OUT, "weo_realgdp_annual.csv"), index=False)
    print(f"reporters={w.COUNTRY.nunique()} years={w.year.min()}..{w.year.max()} rows={len(w)}")


if __name__ == "__main__":
    main()
