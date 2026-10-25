"""Build the monthly recovery panel from Haver by direct ticker construction.

For each (database, IFS country) we already know carries data, try every combo
  prefix in {n, s, h}  x  concept in {gvi, tws, tsc, trsc}
and keep the series that return data. No catalog scanning (dbcodes is the slow part);
Haver.data on a known ticker list is fast.

  gvi  = monthly economic activity index   tsc  = manufacturing real sales
  tws  = wholesale/retail turnover          trsc = real retail trade

Output: data/haver_recovery_panel.csv (date x series) + data/haver_recovery_coverage.csv
Run: python scripts/build_recovery_panel.py
"""
import os

import Haver
import pandas as pd

OUT = os.path.join(os.path.dirname(__file__), "..", "data")
PREFIXES = ["n", "s", "h", "c"]
# concept mnemonics vary by database/country:
#   gvi=activity, tws=wholesale/retail turnover, tsc=mfg sales,
#   trsc/rsx=retail trade, i/d=industrial production
CONCEPTS = ["gvi", "tws", "tsc", "trsc", "rsx", "i", "d"]
DBS = ["EMERGELA", "EMERGEMA", "EMERGEPR", "EMERGECW", "EMERGEFM"]

# Idiosyncratic EM crisis countries -> IMF (IFS) 3-digit numeric code (advanced 2008 cases
# excluded - they are global crises and not in Haver EMERGE dbs).
CRISIS_IFS = {
    "ARG": "213", "BRA": "223", "ECU": "248", "JAM": "343", "SUR": "366", "BLZ": "339",
    "AGO": "614", "CIV": "662", "LSO": "666", "NAM": "728", "NGA": "694", "SDN": "732",
    "SSD": "733", "SYC": "718", "ZAF": "199", "ZMB": "754", "LBN": "446",
    "AZE": "912", "BLR": "913", "RUS": "922", "UKR": "926", "LKA": "524",
}


def _norm(d):
    """Normalize a Haver frame to a month-end DatetimeIndex (handles M and Q)."""
    if isinstance(d.index, pd.PeriodIndex):
        d = d.copy()
        d.index = d.index.to_timestamp(how="end").normalize()
    return d


def pull(codes, db):
    """Batch Haver.data (fast; invalid codes are dropped), normalize index.
    Falls back to per-code only if the batch call raises."""
    try:
        d = Haver.data(codes, database=db)
        if isinstance(d, pd.DataFrame) and d.shape[1]:
            return _norm(d)
    except Exception:
        pass
    cols = {}
    for c in codes:
        try:
            d = Haver.data([c], database=db)
            if isinstance(d, pd.DataFrame) and d.shape[1] and d[c].notna().any():
                cols[c] = _norm(d)[c]
        except Exception:
            continue
    return pd.DataFrame(cols)


def main():
    iso_by_ifs = {v: k for k, v in CRISIS_IFS.items()}
    cand = [f"{p}{ifs}{c}" for ifs in CRISIS_IFS.values()
            for p in PREFIXES for c in CONCEPTS]
    frames, cover = [], []
    for db in DBS:
        d = pull(cand, db)
        if d.empty:
            print(f"[{db}] 0 hits", flush=True)
            continue
        # label + verify via metadata (cheap)
        m = Haver.metadata(list(d.columns), database=db)
        desc = dict(zip(m.code.astype(str), m.descriptor)) if len(m) else {}
        d.columns = [f"{db}:{c}" for c in d.columns]
        frames.append(d)
        for c in d.columns:
            code = c.split(":")[1]
            ifs = "".join(ch for ch in code if ch.isdigit())[:3]
            cover.append({"db": db, "code": code, "iso3": iso_by_ifs.get(ifs, "?"),
                          "concept": next((k for k in CONCEPTS if code.endswith(k)), "?"),
                          "descriptor": desc.get(code, "")})
        print(f"[{db}] {d.shape[1]} hits, countries: "
              f"{sorted({iso_by_ifs.get(''.join(ch for ch in c.split(':')[1] if ch.isdigit())[:3],'?') for c in d.columns})}",
              flush=True)

    if not frames:
        print("nothing pulled"); return
    panel = pd.concat(frames, axis=1).sort_index()
    panel.to_csv(os.path.join(OUT, "haver_recovery_panel.csv"))
    cov = pd.DataFrame(cover)
    cov.to_csv(os.path.join(OUT, "haver_recovery_coverage.csv"), index=False)
    print(f"\nTOTAL {panel.shape[1]} monthly series across "
          f"{cov.iso3.nunique()} crisis countries, span {panel.index.min()}..{panel.index.max()}")
    print("countries with ANY monthly activity:", sorted(cov.iso3.unique()))
    print("MISSING:", sorted(set(CRISIS_IFS) - set(cov.iso3)))


if __name__ == "__main__":
    main()
