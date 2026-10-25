"""Mechanism test: does the monthly EXPORT rebound LEAD the monthly ACTIVITY rebound?

For each crisis country with monthly Haver activity, align:
  exports to World (IMTS, monthly)  vs  activity proxy (Haver, monthly)
Take 12-month (YoY) growth of each (removes seasonality / unit differences), then
cross-correlate activity_growth_t with export_growth_{t-k} for k = -12..+12.
A peak at POSITIVE k means exports lead activity by k months -> "recovery runs through
the trade link." Reported per country and pooled.
Run: python scripts/analyze_leadlag.py
"""
import os
import sys

import numpy as np
import pandas as pd

ROOT = os.path.join(os.path.dirname(__file__), "..")
DATA = os.path.join(ROOT, "data")
sys.path.insert(0, os.path.dirname(__file__))
from imf_sdmx import to_period_dt  # noqa: E402

MAXLAG = 12


def monthly_exports():
    df = pd.read_parquet(os.path.join(DATA, "imts_raw_monthly_2015.parquet"))
    df = df[(df.COUNTERPART_COUNTRY == "G001") & (df.INDICATOR == "XG_FOB_USD")].copy()
    df["date"] = to_period_dt(df["TIME_PERIOD"], "M")
    return df.pivot_table(index="date", columns="COUNTRY", values="OBS_VALUE")


def yoy(s):
    return s.astype(float).pct_change(12)


def main():
    act = pd.read_csv(os.path.join(DATA, "haver_recovery_panel2.csv"),
                      index_col=0, parse_dates=True)
    act.index = pd.DatetimeIndex(act.index).to_period("M")  # align by month, not day
    disc = pd.read_csv(os.path.join(DATA, "haver_activity_discovered.csv"))
    disc = disc[disc.freq == "M"]
    col_by_iso = {r.iso3: f"{r.db}:{r.code}" for _, r in disc.iterrows()}
    exp = monthly_exports()
    exp.index = pd.DatetimeIndex(exp.index).to_period("M")

    rows = []
    for iso, col in col_by_iso.items():
        if col not in act.columns or iso not in exp.columns:
            continue
        a = yoy(act[col]).rename("act")
        e = yoy(exp[iso]).rename("exp")
        d = pd.concat([a, e], axis=1).dropna()
        if len(d) < 36:
            continue
        # cross-correlation: corr(act_t, exp_{t-k})
        cc = {k: d["act"].corr(d["exp"].shift(k)) for k in range(-MAXLAG, MAXLAG + 1)}
        cc = pd.Series(cc).dropna()
        best_k = int(cc.idxmax())
        rows.append({"iso3": iso, "n": len(d), "best_lag": best_k,
                     "peak_corr": round(cc.max(), 2),
                     "corr_at_0": round(cc.get(0, np.nan), 2),
                     "exports_lead": best_k > 0})
    res = pd.DataFrame(rows).sort_values("best_lag", ascending=False)
    res.to_csv(os.path.join(DATA, "leadlag_results.csv"), index=False)
    print(res.to_string(index=False))
    lead = res[res.best_lag > 0]
    print(f"\nExports LEAD activity (best_lag>0) in {len(lead)}/{len(res)} countries; "
          f"median best_lag = {res.best_lag.median():.0f} months, "
          f"median peak corr = {res.peak_corr.median():.2f}")


if __name__ == "__main__":
    main()
