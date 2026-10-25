"""Seasonally adjust the monthly Haver activity panel (X-13ARIMA-SEATS) before recovery dating.

Most series are NSA -> seasonal swings would corrupt trough/recovery detection. Adjust each NSA
series with the modken-snork SeasonalAdjuster (X-13ARIMA-SEATS, log+outlier, with STL and
state-space fallbacks), the same routine used in the DSGE data pipeline. Interior gaps are
interpolated; series need >= 36 monthly obs.

Output: data/haver_activity_sa.csv  (date x country, seasonally adjusted level)
Run: python scripts/seasonal_adjust.py
"""
import os
import sys

import pandas as pd

SNORK = os.environ.get("SNORK_ROOT", r"C:\Users\ysholomytskyi\coding\modken-snork")
sys.path.insert(0, SNORK)
from modken.data.transforms import SeasonalAdjuster  # noqa: E402

DATA = os.path.join(os.path.dirname(__file__), "..", "data")
SA = SeasonalAdjuster(method="x13")   # X-13 required; falls back only if the run fails


def main():
    panel = pd.read_csv(os.path.join(DATA, "haver_recovery_panel2.csv"),
                        index_col=0, parse_dates=True)
    panel.index = pd.DatetimeIndex(panel.index).to_period("M")
    disc = pd.read_csv(os.path.join(DATA, "haver_activity_discovered.csv"))
    disc = disc[disc.freq == "M"]
    info = {f"{r.db}:{r.code}": ("NSA" in str(r.descriptor).upper(), r.iso3)
            for _, r in disc.iterrows()}

    out = {}
    for col in panel.columns:
        if col not in info:
            continue
        is_nsa, iso = info[col]
        s = panel[col].dropna()
        if len(s) < 36:
            continue
        # contiguous full monthly range, interpolate interior gaps
        full = pd.period_range(s.index.min(), s.index.max(), freq="M")
        s = s.reindex(full).interpolate(limit_area="inside").dropna()
        if len(s) < 36:
            continue
        sa = SA.adjust(s, period=12) if is_nsa else s
        out[iso] = sa

    sa_panel = pd.DataFrame(out).sort_index()
    sa_panel.to_csv(os.path.join(DATA, "haver_activity_sa.csv"))
    print(f"SA panel (X-13): {sa_panel.shape[1]} countries, "
          f"{sa_panel.index.min()}..{sa_panel.index.max()}")
    print("countries:", sorted(sa_panel.columns))


if __name__ == "__main__":
    main()
