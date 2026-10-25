"""Figure 1: the world re-coupled to China; the US decoupled. Import side.
Trailing-12m China import share by country from IMTS.
Output: output/figure1_china_shift.png
Run: python scripts/figure1_china_shift.py
"""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

DATA = os.path.join(os.path.dirname(__file__), "..", "data")
OUT = os.path.join(os.path.dirname(__file__), "..", "output")


def main():
    df = pd.read_csv(os.path.join(DATA, "imts_china_share_monthly.csv"),
                     parse_dates=["date"])
    df = df.sort_values(["COUNTRY", "date"])
    # trailing-12m China import share per country
    g = df.groupby("COUNTRY")
    df["chn12"] = g["MG_CIF_USD_CHN"].transform(lambda s: s.rolling(12, min_periods=12).sum())
    df["wld12"] = g["MG_CIF_USD_G001"].transform(lambda s: s.rolling(12, min_periods=12).sum())
    df["share"] = 100 * df["chn12"] / df["wld12"]
    df = df[(df.date >= "2015-01-01") & df.share.notna() & (df.share.between(0, 80))]

    wide = df.pivot_table(index="date", columns="COUNTRY", values="share")
    us = wide["USA"].dropna()
    row = wide.drop(columns=[c for c in ["USA"] if c in wide]).median(axis=1)

    fig, ax = plt.subplots(1, 2, figsize=(12, 4.4))

    # (A) US vs rest-of-world median China import share over time
    ax[0].plot(us.index, us.values, color="tab:red", lw=2, label="United States")
    ax[0].plot(row.index, row.values, color="tab:blue", lw=2,
               label="rest of world (median)")
    ax[0].set_title("China import share: the US decoupled, the world re-coupled")
    ax[0].set_ylabel("imports from China, % of total (12m)")
    ax[0].legend(fontsize=9)

    # (B) change in China import share 2021 -> latest, across countries
    def near(d):
        sub = wide.loc[:d].tail(1)
        return sub.iloc[0]
    latest = wide.dropna(how="all").index.max()
    base = pd.Timestamp("2021-12-31")
    delta = (near(latest) - near(base)).dropna()
    plot_delta = delta[delta.between(-25, 25)]  # trim tails for display only
    ax[1].hist(plot_delta.values, bins=24, color="tab:blue", alpha=0.75,
               label=f"{(delta>0).mean()*100:.0f}% rose")
    ax[1].axvline(0, c="grey", lw=.8)
    if "USA" in delta:
        ax[1].axvline(delta["USA"], c="tab:red", lw=2,
                      label=f"US {delta['USA']:+.1f} pp")
    ax[1].axvline(delta.median(), c="k", ls="--", lw=1.2,
                  label=f"median {delta.median():+.1f} pp")
    ax[1].set_title("Change in China import share, 2021 to 2026")
    ax[1].set_xlabel("percentage points"); ax[1].set_ylabel("countries")
    ax[1].legend(fontsize=8)

    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "figure1_china_shift.png"), dpi=130)
    print("saved output/figure1_china_shift.png")
    print(f"US import share from China: {us.iloc[0]:.1f}% ({us.index[0].year}) "
          f"-> {us.iloc[-1]:.1f}% ({us.index[-1].year})")
    print(f"RoW median: {row.dropna().iloc[0]:.1f}% -> {row.dropna().iloc[-1]:.1f}%")
    print(f"{(delta>0).mean()*100:.0f}% of countries raised their China import share; "
          f"median {delta.median():+.1f}pp; US {delta.get('USA', float('nan')):+.1f}pp")


if __name__ == "__main__":
    main()
