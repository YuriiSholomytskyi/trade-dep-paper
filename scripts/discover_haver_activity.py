"""Auto-discover the best monthly activity series per crisis country in Haver.

Concept mnemonics vary by database AND country (gvi/tws/trsc/rsx/i/d/dm2n/vpmi...), so we
do NOT reconstruct tickers. Instead: enumerate each database's catalog ONCE (cached to
data/haver_codes/<db>.txt), filter to our crisis countries' numeric codes, read descriptors,
and keep the best activity proxy per country.

Priority of recovery proxy: Economic Activity index > GDP(monthly) > Industrial Production >
Retail trade > Manufacturing sales.

Output: data/haver_activity_discovered.csv (chosen series per country) +
        data/haver_recovery_panel2.csv (the actual monthly data)
Run: python scripts/discover_haver_activity.py
"""
import os
import re

import Haver
import pandas as pd

OUT = os.path.join(os.path.dirname(__file__), "..", "data")
CODES_DIR = os.path.join(OUT, "haver_codes")
os.makedirs(CODES_DIR, exist_ok=True)
DBS = ["EMERGELA", "EMERGEMA", "EMERGEPR", "EMERGECW", "EMERGEFM"]

# IFS numeric -> country name, taken from the MONA program population (97 countries).
# MONA country_code IS the IFS numeric code, which is also what Haver embeds in series codes.
_mona = pd.read_csv(os.path.join(OUT, "mona_arrangements.csv"))
CRISIS_IFS = {str(int(r.country_code)): r.country_name
              for _, r in _mona.dropna(subset=["country_code"]).iterrows()}
# descriptor keyword -> priority rank (lower = preferred). Headline activity proxies only.
PRIORITY = [
    (r"economic activity (indicator|index)|indicator of economic activity", 0),
    (r"industrial production", 1),
    (r"real retail|retail (trade|sales).*(index|value)", 2),
    (r"manufacturing.*(sales|production)", 3),
]
# descriptors that look like activity but are NOT a real activity level -> drop
BLOCK = re.compile(
    r"fsi|loan|credit|government|expenditure|impact of demand|news index|stock price|"
    r"swap|reserve|%\s*bal|\bbalance\b|climate|confidence|survey|expectation|sentiment|"
    r"wholesale and retail trade|wholesale & retail", re.I)
# sectoral sub-indices (a sub-sector, not the headline total) -> usable but down-ranked
SECTORAL = re.compile(
    r":\s*(electricity|dairy|chemical|livestock|food|textile|beverage|tobacco|"
    r"special regimes|information|communication|mining|construction|agriculture|services|"
    r"wood|paper|metal|machinery|repair)|primary (activity|sector)", re.I)


def cached_dbcodes(db):
    f = os.path.join(CODES_DIR, f"{db}.txt")
    if os.path.exists(f):
        return open(f, encoding="utf-8").read().split()
    codes = [str(c) for c in Haver.dbcodes(db)]
    open(f, "w", encoding="utf-8").write("\n".join(codes))
    print(f"[{db}] cached {len(codes)} codes", flush=True)
    return codes


def rank(desc):
    d = str(desc).lower()
    if BLOCK.search(d):
        return 99
    penalty = 10 if SECTORAL.search(d) else 0  # headline beats sub-sector
    for pat, r in PRIORITY:
        if re.search(pat, d):
            return r + penalty
    return 99


def main():
    chosen, frames = [], []
    for db in DBS:
        codes = cached_dbcodes(db)
        # codes whose 3-digit numeric run is one of our IFS codes; short codes only
        # (activity series are short like n614d / c213ae; junk codes are long)
        cand = [c for c in codes
                if len(c) <= 9
                and (m := re.search(r"\d{3,4}", c)) and m.group(0)[:3] in CRISIS_IFS]
        if not cand:
            continue
        print(f"[{db}] {len(cand)} short candidate codes", flush=True)
        # metadata in chunks to stay responsive; skip chunks that error
        chunks = []
        for i in range(0, len(cand), 500):
            try:
                mm = Haver.metadata(cand[i:i+500], database=db)
                if isinstance(mm, pd.DataFrame) and len(mm):
                    chunks.append(mm)
            except Exception:
                continue
        if not chunks:
            continue
        meta = pd.concat(chunks, ignore_index=True)
        meta = meta[meta.frequency.isin(["M", "Q"])].copy()
        if not len(meta):
            continue
        meta["ifs"] = meta.code.astype(str).str.extract(r"(\d{3})")[0]
        meta["iso3"] = meta.ifs.map(CRISIS_IFS)
        meta["rank"] = meta.descriptor.map(rank)
        meta = meta[meta["rank"] < 99]
        # best series per country in this db
        best = meta.sort_values(["iso3", "rank", "frequency"]).groupby("iso3").first()
        for iso3, r in best.iterrows():
            chosen.append({"iso3": iso3, "db": db, "code": r.code, "rank": r["rank"],
                           "freq": r.frequency, "descriptor": r.descriptor})
        print(f"[{db}] activity series for: {sorted(best.index)}", flush=True)

    ch = pd.DataFrame(chosen)
    # one chosen series per country across all dbs (lowest rank wins)
    ch = ch.sort_values(["iso3", "rank"]).drop_duplicates("iso3")
    ch.to_csv(os.path.join(OUT, "haver_activity_discovered.csv"), index=False)
    # pull the chosen series
    for db, g in ch.groupby("db"):
        d = Haver.data(list(g.code), database=db)
        if isinstance(d.index, pd.PeriodIndex):
            d.index = d.index.to_timestamp(how="end").normalize()
        d.columns = [f"{db}:{c}" for c in d.columns]
        frames.append(d)
    panel = pd.concat(frames, axis=1).sort_index()
    panel.to_csv(os.path.join(OUT, "haver_recovery_panel2.csv"))
    print(f"\nChosen activity series for {ch.iso3.nunique()} crisis countries: "
          f"{sorted(ch.iso3)}", flush=True)
    print("MISSING:", sorted(set(CRISIS_IFS.values()) - set(ch.iso3)), flush=True)


if __name__ == "__main__":
    main()
