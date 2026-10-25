"""Robustness: external demand beyond goods, services and remittances.

The baseline demand measure is a shift-share of pre-crisis GOODS export shares and partner
growth. Services exports (tourism above all) and worker remittances are the same channel, a
foreign buyer whose demand keeps flowing, and dominate the recovery in economies such as Sri
Lanka. Bilateral, partner-level data are available for goods (IMTS) but thin for services, so we
cannot build a fully bilateral services shift-share. Instead we bring in country-level intensities
from the World Bank WDI and run three tests:

  1. Controls: is the goods partner-demand result robust to services/remittance/tourism intensity?
  2. Heterogeneity: does partner demand still shorten the cycle for services- and remittance-
     dependent economies (the channel is not goods-specific)?
  3. Broad external demand: a combined measure that augments the goods shift-share with the
     services and remittance intensities interacted with advanced-partner growth (their dominant
     sources), and its effect on the negative cycle.

Outputs: prints coefficients; writes output/tables_services.tex.
Run: python scripts/services_robustness.py
"""
import os
import sys
import json
import ssl
import time
import urllib.request

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(__file__))
from build_horserace_hp import ols  # noqa: E402

DATA = os.path.join(os.path.dirname(__file__), "..", "data")
OUT = os.path.join(os.path.dirname(__file__), "..", "output")
CACHE = os.path.join(DATA, "wdi_services_intensity.csv")

# WDI indicators (country-year): remittances %GDP, services exports %GDP-equivalent, tourism.
WDI = {
    "remit_gdp": "BX.TRF.PWKR.DT.GD.ZS",     # personal remittances received, % of GDP
    "serv_exp_usd": "BX.GSR.NFSV.CD",         # services exports (BoP, current US$)
    "gdp_usd": "NY.GDP.MKTP.CD",              # GDP (current US$)
    "tour_xp": "ST.INT.RCPT.XP.ZS",           # int'l tourism receipts, % of total exports
}
_CTX = ssl.create_default_context()
_CTX.check_hostname = False
_CTX.verify_mode = ssl.CERT_NONE


def _wdi_all(code, retries=4):
    """Pull one indicator for ALL countries in a single request (fast, robust)."""
    url = (f"https://api.worldbank.org/v2/country/all/indicator/{code}"
           f"?format=json&per_page=25000&date=2000:2025")
    for k in range(retries):
        try:
            r = json.load(urllib.request.urlopen(url, timeout=90, context=_CTX))
            if not r or len(r) < 2 or r[1] is None:
                return []
            return [(x["countryiso3code"], int(x["date"]), x["value"]) for x in r[1]]
        except Exception as e:
            print(f"  retry {code} ({k}): {e!r}")
            time.sleep(3 * (k + 1))
    return []


def fetch_intensity(countries):
    if os.path.exists(CACHE):
        return pd.read_csv(CACHE)
    cset = set(countries)
    rows = {}
    for name, code in WDI.items():
        got = _wdi_all(code)
        for iso, yr, v in got:
            if iso in cset and v is not None:
                rows[(iso, yr, name)] = v
        print(f"  pulled {name} ({code}): {len(got)} rows")
    long = pd.DataFrame(
        [(iso, yr, name, v) for (iso, yr, name), v in rows.items()],
        columns=["iso3", "year", "var", "val"])
    wide = long.pivot_table(index=["iso3", "year"], columns="var", values="val").reset_index()
    wide["serv_exp_gdp"] = 100.0 * wide["serv_exp_usd"] / wide["gdp_usd"]
    wide = wide[["iso3", "year", "remit_gdp", "serv_exp_gdp", "tour_xp"]]
    wide.to_csv(CACHE, index=False)
    return wide


def main():
    hub = pd.read_csv(os.path.join(DATA, "hub_panel.csv"))
    countries = sorted(hub.iso3.unique())
    wdi = fetch_intensity(countries)

    # merge pre-downturn (year before peak) intensities onto each episode
    wdi = wdi.sort_values(["iso3", "year"])
    hub = hub.sort_values("peak_year")
    hub["mkey"] = hub.peak_year - 1
    m = pd.merge_asof(hub, wdi.rename(columns={"year": "mkey"}).sort_values("mkey"),
                      on="mkey", by="iso3", direction="backward")
    for c in ["remit_gdp", "serv_exp_gdp", "tour_xp"]:
        m[c] = m[c].fillna(m[c].median())

    # advanced-partner growth already in panel as otheradv_pull + us_pull (the growing-AE demand);
    # services/remittances flow mostly from advanced + Gulf economies, proxied by AE demand.
    m["ae_pull"] = m["us_pull"].fillna(0) + m["otheradv_pull"].fillna(0)
    # broad external demand: goods shift-share + non-negative GDP-share-weighted AE growth
    # for services exports and remittances (avoiding negative z-score weights).
    m["serv_dem"] = (m["serv_exp_gdp"] / 100.0) * m["ae_pull"]
    m["remit_dem"] = (m["remit_gdp"] / 100.0) * m["ae_pull"]
    m["broad_demand"] = m["ext_demand"] + m["serv_dem"] + m["remit_dem"]

    # high-dependence indicators (top tercile)
    for c, name in [("serv_exp_gdp", "hi_serv"), ("remit_gdp", "hi_remit"), ("tour_xp", "hi_tour")]:
        m[name] = (m[c] >= m[c].quantile(2 / 3)).astype(int)
    m["us_x_serv"] = m["us_pull"] * m["hi_serv"]
    m["us_x_remit"] = m["us_pull"] * m["hi_remit"]

    def line(res, keep):
        d = dict((k, (b, s)) for k, b, s in res[0])
        out = []
        for k in keep:
            if k in d:
                b, s = d[k]
                t = b / s
                out.append((k, b, t))
        return out, res[2], res[3]

    base_parts = ["us_pull", "otheradv_pull", "emer_pull", "china_pull"]
    base_ctrl = ["trade_open", "depth_gap", "program"]

    print("\n=== (1) Goods partner-demand robust to services/remittance/tourism intensity ===")
    r1 = ols(m, "t_full", base_parts + ["remit_gdp", "serv_exp_gdp", "tour_xp"] + base_ctrl)
    for k, b, t in line(r1, base_parts + ["remit_gdp", "serv_exp_gdp", "tour_xp", "trade_open", "depth_gap"])[0]:
        print(f"  {k:14s} {b:7.3f} (t={t:5.2f})")
    print(f"  n={r1[2]} clusters={r1[3]}")

    print("\n=== (2) Heterogeneity: US demand x services/remittance dependence ===")
    r2 = ols(m, "t_full", ["us_pull", "us_x_serv", "us_x_remit", "hi_serv", "hi_remit",
                           "otheradv_pull", "emer_pull", "china_pull"] + base_ctrl)
    for k, b, t in line(r2, ["us_pull", "us_x_serv", "us_x_remit", "hi_serv", "hi_remit",
                             "otheradv_pull", "emer_pull", "china_pull", "trade_open", "depth_gap"])[0]:
        print(f"  {k:14s} {b:7.3f} (t={t:5.2f})")
    print(f"  n={r2[2]} clusters={r2[3]}")

    print("\n=== (3) Broad external demand (goods + services + remittances) ===")
    r3a = ols(m, "t_full", ["ext_demand"] + base_ctrl)
    r3b = ols(m, "t_full", ["broad_demand"] + base_ctrl)
    for tag, r in [("goods only  ", r3a), ("broad demand", r3b)]:
        d = dict((k, (b, s)) for k, b, s in r[0])
        key = "ext_demand" if "ext_demand" in d else "broad_demand"
        b, s = d[key]
        print(f"  {tag}: {key:12s} {b:7.3f} (t={b/s:5.2f})  n={r[2]}")

    # ---- LaTeX table: rows are variables, columns are the three specifications ----
    def cell(res, key):
        if res is None:
            return "--"
        d = dict((k, (b, s)) for k, b, s in res[0])
        if key not in d:
            return ""
        b, s = d[key]
        t = b / s
        star = "***" if abs(t) > 2.58 else "**" if abs(t) > 1.96 else "*" if abs(t) > 1.64 else ""
        val = f"${b:.2f}^{{{star}}}$" if star else f"${b:.2f}$"
        return f"{val} {{\\scriptsize$({t:.1f})$}}"

    # (row label, (spec1 res,key), (spec2 res,key), (spec3 res,key))
    spec = [
        ("US demand", (r1, "us_pull"), (r2, "us_pull"), (None, None)),
        ("Broad external demand", (None, None), (None, None), (r3b, "broad_demand")),
        ("US demand $\\times$ high services", (None, None), (r2, "us_x_serv"), (None, None)),
        ("US demand $\\times$ high remittances", (None, None), (r2, "us_x_remit"), (None, None)),
        ("High services indicator", (None, None), (r2, "hi_serv"), (None, None)),
        ("High remittances indicator", (None, None), (r2, "hi_remit"), (None, None)),
        ("Other advanced demand", (r1, "otheradv_pull"), (r2, "otheradv_pull"), (None, None)),
        ("Emerging demand (excl.\\ China)", (r1, "emer_pull"), (r2, "emer_pull"), (None, None)),
        ("China demand", (r1, "china_pull"), (r2, "china_pull"), (None, None)),
        ("Trade openness", (r1, "trade_open"), (r2, "trade_open"), (r3b, "trade_open")),
        ("Depth of downturn", (r1, "depth_gap"), (r2, "depth_gap"), (r3b, "depth_gap")),
        ("Remittances, \\% GDP", (r1, "remit_gdp"), (None, None), (None, None)),
        ("Services exports, \\% GDP", (r1, "serv_exp_gdp"), (None, None), (None, None)),
        ("Tourism, \\% of exports", (r1, "tour_xp"), (None, None), (None, None)),
    ]

    def rowtex(label, c1, c2, c3):
        return (f"{label} & {cell(*c1) if c1[0] is not None else ''} & "
                f"{cell(*c2) if c2[0] is not None else ''} & "
                f"{cell(*c3) if c3[0] is not None else ''} \\\\")

    tex = [
        r"\begin{table}[H]", r"\centering\small",
        r"\caption{External demand beyond goods: services and remittances. The dependent variable "
        r"is the full negative cycle in months; country-clustered $t$-statistics in parentheses. "
        r"Column 1 adds World Bank pre-downturn intensity controls to the full four-partner "
        r"specification of Table~\ref{tab:main}; column 2 interacts US demand with top-tercile "
        r"services and remittance dependence (including uninteracted main effects); column 3 "
        r"replaces the goods shift-share with a broad external demand measure that augments "
        r"aggregate goods partner demand with GDP-share-weighted services and remittance "
        r"exposures to advanced-partner growth.}",
        r"\label{tab:services}",
        r"\begin{tabularx}{\textwidth}{@{}lYYY@{}}", r"\toprule",
        r" & (1) controls & (2) heterogeneity & (3) broad demand \\ \midrule",
    ]
    tex += [rowtex(lbl, c1, c2, c3) for (lbl, c1, c2, c3) in spec]
    tex += [
        r"\midrule",
        f"Episodes & {r1[2]} & {r2[2]} & {r3b[2]} \\\\",
        f"Countries & {r1[3]} & {r2[3]} & {r3b[3]} \\\\",
        r"\bottomrule", r"\end{tabularx}",
        r"\\[2pt]\footnotesize{Intensities are pre-downturn values from the World Bank WDI "
        r"(personal remittances received as \% of GDP, commercial services exports as \% of GDP, "
        r"and international tourism receipts as \% of total exports). Missing pre-downturn WDI "
        r"observations are imputed at the sample median. All columns include the active IMF "
        r"arrangement indicator (MONA) and downturn depth. $^{*},^{**},^{***}$: significant at "
        r"10, 5, 1 percent.}",
        r"\end{table}",
    ]
    with open(os.path.join(OUT, "tables_services.tex"), "w", encoding="utf-8") as f:
        f.write("\n".join(tex) + "\n")
    print("\nsaved output/tables_services.tex")


if __name__ == "__main__":
    main()
