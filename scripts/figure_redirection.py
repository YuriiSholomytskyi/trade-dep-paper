"""Figure: trade grew but was redirected. Levels, trailing-12m, from IMTS.
Left  : US goods imports rerouted from China to connector economies (Vietnam+Mexico),
        while total US imports kept rising.
Right : China's goods exports redirected from the US to the rest of the world,
        while total China exports kept rising.
Output: output/figure_redirection.png
Run: python scripts/figure_redirection.py
"""
import os
import sys

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(__file__))
from imf_sdmx import fetch_data, to_period_dt  # noqa: E402

OUT = os.path.join(os.path.dirname(__file__), "..", "output")


def series(df, reporter, indicator, partner):
    s = df[(df.COUNTRY == reporter) & (df.INDICATOR == indicator)
           & (df.COUNTERPART_COUNTRY == partner)].copy()
    s["date"] = to_period_dt(s["TIME_PERIOD"], "M")
    s = s.set_index("date")["OBS_VALUE"].sort_index()
    return (s.rolling(12, min_periods=12).sum()) / 1e9   # trailing-12m, $bn


def main():
    us = fetch_data("IMF.STA", "IMTS", "USA.MG_CIF_USD.CHN+VNM+MEX+G001.M", start="2010")
    cn = fetch_data("IMF.STA", "IMTS", "CHN.XG_FOB_USD.USA+G001.M", start="2010")

    us_chn = series(us, "USA", "MG_CIF_USD", "CHN")
    us_conn = (series(us, "USA", "MG_CIF_USD", "VNM").add(
               series(us, "USA", "MG_CIF_USD", "MEX"), fill_value=0))
    us_tot = series(us, "USA", "MG_CIF_USD", "G001")
    cn_us = series(cn, "CHN", "XG_FOB_USD", "USA")
    cn_tot = series(cn, "CHN", "XG_FOB_USD", "G001")
    cn_row = cn_tot - cn_us

    fig, ax = plt.subplots(1, 2, figsize=(13, 4.6))
    lo = pd.Timestamp("2011-01-01")

    ax[0].plot(us_tot.loc[lo:].index, us_tot.loc[lo:], color="k", lw=2, label="total US imports")
    ax[0].plot(us_chn.loc[lo:].index, us_chn.loc[lo:], color="tab:red", lw=2, label="from China")
    ax[0].plot(us_conn.loc[lo:].index, us_conn.loc[lo:], color="tab:green", lw=2,
               label="from Vietnam + Mexico")
    ax[0].set_title("US imports rerouted, not reduced")
    ax[0].set_ylabel("goods imports, US\\$bn (12m)"); ax[0].legend(fontsize=8, loc="upper left")

    ax[1].plot(cn_tot.loc[lo:].index, cn_tot.loc[lo:], color="k", lw=2, label="total China exports")
    ax[1].plot(cn_row.loc[lo:].index, cn_row.loc[lo:], color="tab:blue", lw=2,
               label="to rest of world")
    ax[1].plot(cn_us.loc[lo:].index, cn_us.loc[lo:], color="tab:red", lw=2, label="to the US")
    ax[1].set_title("China exports redirected from the US to the rest of the world")
    ax[1].set_ylabel("goods exports, US\\$bn (12m)"); ax[1].legend(fontsize=8, loc="upper left")

    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "figure_redirection.png"), dpi=130)
    print("saved output/figure_redirection.png")

    def last(s):
        return s.dropna().iloc[-1], s.dropna().index[-1].year
    print(f"US total imports: {last(us_tot)[0]:.0f}bn ({last(us_tot)[1]}); "
          f"from China {us_chn.dropna().iloc[-1]:.0f}bn (peak {us_chn.max():.0f}); "
          f"from VNM+MEX {us_conn.dropna().iloc[-1]:.0f}bn")
    print(f"China total exports: {last(cn_tot)[0]:.0f}bn; to US {cn_us.dropna().iloc[-1]:.0f}bn; "
          f"to RoW {cn_row.dropna().iloc[-1]:.0f}bn")


if __name__ == "__main__":
    main()
