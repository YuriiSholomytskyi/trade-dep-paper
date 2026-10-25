"""Build an IFS-numeric <-> ISO3-alpha country crosswalk.

Lane-Milesi-Ferretti and MONA are keyed by IFS numeric; IMTS and the crisis panel use ISO3.
Source the (IFS, name) pairs from the Lane-MF EWN file (full ~200-country coverage) and map
the name to ISO3 with pycountry, with manual overrides for non-standard IMF names.

Output: data/ifs_iso3_crosswalk.csv (ifs, iso3, name)
Run: python scripts/build_crosswalk.py
"""
import os

import pandas as pd
import pycountry

OUT = os.path.join(os.path.dirname(__file__), "..", "data")

# IMF/Lane-MF names pycountry can't resolve -> ISO3 (extend as needed)
OVERRIDE = {
    "512": "AFG", "Afghanistan, I.R. of": "AFG", "Korea, Rep. of": "KOR",
    "Korea, Republic of": "KOR", "Lao P.D.R.": "LAO", "Lao People's Dem.Rep": "LAO",
    "Congo, Dem. Rep. of": "COD", "Congo, Republic of": "COG", "Congo, Rep. of": "COG",
    "China,P.R.: Mainland": "CHN", "China, P.R.: Mainland": "CHN", "Taiwan Prov.of China": "TWN",
    "Hong Kong SAR": "HKG", "Macao SAR": "MAC", "Russian Federation": "RUS",
    "Venezuela, Rep. Bol.": "VEN", "Venezuela, RB": "VEN", "Bolivia": "BOL", "Iran, I.R. of": "IRN",
    "Syrian Arab Republic": "SYR", "Yemen, Rep. of": "YEM", "Yemen, Republic of": "YEM",
    "Kosovo, Rep. of": "XKX", "Cabo Verde": "CPV", "Cape Verde": "CPV",
    "North Macedonia ": "MKD", "Macedonia, FYR": "MKD", "Micronesia, Fed.Sts.": "FSM",
    "São Tomé and Príncipe": "STP", "Sao Tome & Principe": "STP", "Eswatini": "SWZ",
    "Turkiye": "TUR", "Türkiye, Rep of": "TUR", "Turkey": "TUR", "Slovak Republic": "SVK",
    "Kyrgyz Republic": "KGZ", "Brunei Darussalam": "BRN", "Timor-Leste": "TLS",
    "Curacao and Sint Maarten": "CUW", "West Bank and Gaza": "PSE", "South Sudan, Rep. of": "SSD",
}


def to_iso3(name):
    n = str(name).strip()
    if n in OVERRIDE:
        return OVERRIDE[n]
    base = n.split(",")[0].strip()
    for cand in (n, base):
        try:
            return pycountry.countries.lookup(cand).alpha_3
        except LookupError:
            pass
    try:
        return pycountry.countries.search_fuzzy(base)[0].alpha_3
    except Exception:
        return None


def main():
    lmf = pd.read_excel(os.path.join(OUT, "lmf_ewn_2024.xlsx"), sheet_name="Dataset",
                        usecols=["Country", "IFS_Code"]).drop_duplicates()
    lmf["ifs"] = lmf["IFS_Code"].astype("Int64").astype(str)
    rows, miss = [], []
    for _, r in lmf.iterrows():
        iso3 = OVERRIDE.get(r.ifs) or to_iso3(r.Country)
        rows.append({"ifs": r.ifs, "iso3": iso3, "name": r.Country})
        if not iso3:
            miss.append((r.ifs, r.Country))
    cw = pd.DataFrame(rows).dropna(subset=["iso3"]).drop_duplicates("ifs")
    cw.to_csv(os.path.join(OUT, "ifs_iso3_crosswalk.csv"), index=False)
    print(f"crosswalk: {len(cw)} countries mapped; {len(miss)} unmatched")
    if miss:
        print("UNMATCHED (add to OVERRIDE):", miss[:40])


if __name__ == "__main__":
    main()
