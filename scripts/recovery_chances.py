"""Who recovers and who is stuck. Refined, idiosyncratic-only anchor measure: the growth of a
country's hub DURING the country's own (local) downturns, excluding the global-crisis years
2008-09 and 2020 when every hub crashes together and no anchor helps. Also quantifies that
global-crisis failure directly.
Output: output/recovery_chances.png
Run: python scripts/recovery_chances.py
"""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

DATA = os.path.join(os.path.dirname(__file__), "..", "data")
OUT = os.path.join(os.path.dirname(__file__), "..", "output")
GLOBAL = {2008, 2009, 2020}
EU = ["DEU", "FRA", "ITA", "ESP", "NLD", "POL"]
COL = {"US": "tab:blue", "EU": "tab:orange", "CN": "tab:red"}


def main():
    hub = pd.read_csv(os.path.join(DATA, "hub_panel.csv"))
    weo = pd.read_csv(os.path.join(DATA, "weo_realgdp_annual.csv"))
    g = weo.set_index(["COUNTRY", "year"])["ngdp_rpch"]
    hubg = {"US": g.xs("USA", level=0), "EU": g.loc[EU].groupby("year").mean(),
            "CN": g.xs("CHN", level=0)}

    cty_hub = hub.groupby("iso3").hub.agg(lambda s: s.mode().iat[0])
    ep = hub[~hub.peak_year.isin(GLOBAL)].copy()   # idiosyncratic downturns only

    # per country: mean hub growth over the recovery window of its LOCAL downturns
    rows = []
    for iso, sub in ep.groupby("iso3"):
        h = cty_hub[iso]
        vals = []
        for yr in sub.peak_year:
            vals += [hubg[h].get(y) for y in range(yr, yr + 3)]
        vals = [v for v in vals if pd.notna(v)]
        if vals:
            rows.append((iso, h, np.mean(vals), len(sub)))
    df = pd.DataFrame(rows, columns=["iso3", "hub", "hubgrow", "n"]).sort_values("hubgrow")

    # global-crisis failure: hub growth in the global-crisis years
    glob = {h: hubg[h].reindex([2009, 2020]).mean() for h in hubg}

    fig, ax = plt.subplots(1, 2, figsize=(13, 5.2),
                           gridspec_kw={"width_ratios": [3, 1]})
    # panel A: who recovers / who is stuck
    ax[0].barh(df.iso3, df.hubgrow, color=[COL[h] for h in df.hub])
    ax[0].axvline(0, c="k", lw=.8)
    ax[0].set_title("Who recovers and who is stuck:\nhub growth during a country's own (local) downturns")
    ax[0].set_xlabel("mean hub real GDP growth over the recovery window, %")
    ax[0].tick_params(axis="y", labelsize=7)
    for h, c in COL.items():
        ax[0].plot([], [], "s", color=c, label={"US": "US hub", "EU": "EU hub", "CN": "China hub"}[h])
    ax[0].legend(fontsize=8, loc="lower right")

    # panel B: in a global crisis the demand hubs (US, EU) crash; China stimulated but buys little
    ax[1].bar(list(glob.keys()), list(glob.values()),
              color=[COL[h] for h in glob])
    ax[1].axhline(0, c="k", lw=.8)
    ax[1].set_title("Global crisis (2009 & 2020):\nthe demand hubs crash\n(China stimulated, but buys little)")
    ax[1].set_ylabel("hub growth, %")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "recovery_chances.png"), dpi=130)
    print("saved output/recovery_chances.png")
    print("\nBest-placed (hub grows most during local downturns):")
    print(df.tail(5)[["iso3", "hub", "hubgrow"]].to_string(index=False))
    print("Worst-placed (hub barely grows / shrinks when they are down):")
    print(df.head(5)[["iso3", "hub", "hubgrow"]].to_string(index=False))
    print("\nGlobal-crisis hub growth (2009 & 2020 avg):",
          {h: round(v, 1) for h, v in glob.items()}, "-> anchor fails for all")
    print(f"idiosyncratic median hub growth: {df.hubgrow.median():.1f}% (positive: the anchor is there)")


if __name__ == "__main__":
    main()
