"""Map monthly demand/activity indicator availability across the EMERGE databases.

Concepts (Haver mnemonic suffixes), best-available per country for the recovery measure:
  gvi  - monthly Economic Activity Indicator (central-bank monthly GDP proxy)
  tws  - wholesale/retail sales (turnover)
  tsc  - manufacturing real sales
  trsc - real retail trade (consumption proxy)
Prefix letter = transformation/variant (n=NSA, s=SA, h=real-SA, ...). 3-digit run = IFS code.

Output: data/haver_concept_availability.csv  (country IFS x concept -> code, freq, span)
Run: python -u scripts/scan_haver_concepts.py
"""
import os
import re

import Haver
import pandas as pd

OUT = os.path.join(os.path.dirname(__file__), "..", "data")
DBS = ["EMERGELA", "EMERGEMA", "EMERGEPR", "EMERGECW", "EMERGEFM"]
CONCEPTS = ["gvi", "tws", "tsc", "trsc"]


def main():
    rows = []
    for db in DBS:
        codes = [str(c).lower() for c in Haver.dbcodes(db)]
        hit = [c for c in codes if any(c.endswith(k) for k in CONCEPTS)]
        print(f"[{db}] {len(hit)} candidate concept series", flush=True)
        if not hit:
            continue
        try:
            m = Haver.metadata(hit, database=db)
        except Exception as e:
            print(f"[{db}] metadata failed: {e}", flush=True)
            continue
        m = m[m.frequency.isin(["M", "Q"])].copy()
        for _, r in m.iterrows():
            code = str(r.code).lower()
            concept = next((k for k in CONCEPTS if code.endswith(k)), None)
            ifs = re.search(r"(\d{3,4})", code)
            rows.append({
                "db": db, "ifs": ifs.group(1) if ifs else None, "concept": concept,
                "code": r.code, "freq": r.frequency,
                "country": str(r.descriptor).split(":")[0],
                "start": r.startdate, "end": r.enddate,
                "descriptor": r.descriptor,
            })
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(OUT, "haver_concept_availability.csv"), index=False)
    # summary: countries x concept counts
    piv = df.pivot_table(index="country", columns="concept", values="code",
                         aggfunc="count", fill_value=0)
    print(f"\n{df.country.nunique()} countries, {len(df)} monthly/quarterly series", flush=True)
    print("countries per concept:", df.groupby("concept").country.nunique().to_dict(), flush=True)
    print("\n", piv.to_string())


if __name__ == "__main__":
    main()
