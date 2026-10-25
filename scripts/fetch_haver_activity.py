"""Pull monthly economic-activity indicators (GVI) from Haver for emerging markets.

GVI = central-bank Monthly Economic Activity Indicator (Chile IMACEC, Colombia ISE, Mexico,
Peru, Argentina, etc.) - the high-frequency recovery proxy where annual WEO GDP is too coarse
and quarterly GDP is unavailable for EM crisis countries.

Series code pattern: <prefix><IFS-country-code>gvi (e.g. n213gvi = Argentina, IFS 213).
Databases scanned: the EMERGE* family (LA / MA / PR / CW / FM).

Output: data/haver_activity_monthly.csv  (date x series) + data/haver_activity_meta.csv
Run: python scripts/fetch_haver_activity.py
Requires: the Haver package + IMF-network DLX path (see memory: haver-access).
"""
import os

import Haver
import pandas as pd

OUT = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(OUT, exist_ok=True)

DBS = ["EMERGELA", "EMERGEMA", "EMERGEPR", "EMERGECW", "EMERGEFM"]


def main():
    meta_frames, data_frames = [], []
    for db in DBS:
        try:
            codes = [c for c in Haver.dbcodes(db) if str(c).lower().endswith("gvi")]
        except Exception as e:
            print(f"[{db}] dbcodes failed: {e}")
            continue
        if not codes:
            print(f"[{db}] no GVI series")
            continue
        m = Haver.metadata(codes, database=db)
        # keep only monthly activity-index series
        m = m[m.frequency == "M"]
        codes = list(m.code)
        d = Haver.data(codes, database=db)
        d.columns = [f"{db}:{c}" for c in d.columns]
        data_frames.append(d)
        m["db"] = db
        meta_frames.append(m)
        print(f"[{db}] {len(codes)} monthly GVI series, "
              f"{m.descriptor.str.split(':').str[0].nunique()} countries")

    if not data_frames:
        print("No Haver data pulled - check network/DLX path with Haver.path().")
        return
    data = pd.concat(data_frames, axis=1).sort_index()
    meta = pd.concat(meta_frames, ignore_index=True)
    data.to_csv(os.path.join(OUT, "haver_activity_monthly.csv"))
    meta.to_csv(os.path.join(OUT, "haver_activity_meta.csv"), index=False)
    print(f"saved {data.shape[1]} series, span {data.index.min()}..{data.index.max()}")


if __name__ == "__main__":
    main()
