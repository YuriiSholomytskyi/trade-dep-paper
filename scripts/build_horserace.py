"""Two-leg horse race: financial openness -> shock DEPTH; trade link + IMF program ->
recovery SPEED, with a program x trade-openness interaction.

Joins (all to ISO3 via data/ifs_iso3_crosswalk.csv):
  step1_panel_extdemand.csv  - crisis episodes: recovery_time, output_loss_pct,
                               pre_openness (trade/GDP), ext_demand (partner-growth pull)
  lmf_ewn_2024.xlsx          - financial openness = (Total assets+liab)/GDP, pre-crisis
  mona_arrangements.csv      - IMF program active around the crisis (IFS-keyed)

Leg 1: output_loss   ~ fin_openness + trade_openness            (does fin openness amplify?)
Leg 2: recovery_time ~ ext_demand + program + program*trade_openness + output_loss
       (does the link speed recovery? does the program help only where open?)
Run: python scripts/build_horserace.py
"""
import os

import numpy as np
import pandas as pd

DATA = os.path.join(os.path.dirname(__file__), "..", "data")
GLOBAL = {2008, 2009, 2020}


def ols(d, y, xs):
    d = d.dropna(subset=[y] + xs)
    if len(d) < len(xs) + 3:
        return None
    X = np.column_stack([np.ones(len(d))] + [d[x].values for x in xs])
    b, *_ = np.linalg.lstsq(X, d[y].values, rcond=None)
    yhat = X @ b
    resid = d[y].values - yhat
    n, k = len(d), X.shape[1]
    sigma2 = (resid @ resid) / (n - k)
    se = np.sqrt(np.diag(sigma2 * np.linalg.inv(X.T @ X)))
    r2 = 1 - (resid @ resid) / ((d[y].values - d[y].mean()) ** 2).sum()
    return list(zip(["const"] + xs, b, se)), r2, n


def show(res, title):
    print(f"\n{title}")
    if not res:
        print("  (insufficient obs)"); return
    coefs, r2, n = res
    for name, b, se in coefs:
        t = b / se if se else 0
        star = "***" if abs(t) > 2.6 else "**" if abs(t) > 1.96 else "*" if abs(t) > 1.64 else ""
        print(f"  {name:22s} {b:10.3f}  (t={t:5.2f}) {star}")
    print(f"  R2={r2:.3f}  n={n}")


def main():
    cw = pd.read_csv(os.path.join(DATA, "ifs_iso3_crosswalk.csv"))
    ifs2iso = dict(zip(cw.ifs.astype(str), cw.iso3))

    ep = pd.read_csv(os.path.join(DATA, "step1_panel_extdemand.csv"))
    ep = ep.sort_values("output_loss_pct", ascending=False).drop_duplicates(["iso3", "start_year"])

    # financial openness (pre-crisis): (Total assets + Total liabilities) / GDP
    lmf = pd.read_excel(os.path.join(DATA, "lmf_ewn_2024.xlsx"), sheet_name="Dataset")
    lmf["iso3"] = lmf["IFS_Code"].astype("Int64").astype(str).map(ifs2iso)
    lmf["fin_open"] = (lmf["Total assets"] + lmf["Total liabilities"]) / lmf["GDP (US$)"]
    fo = lmf[["iso3", "Year", "fin_open"]].rename(columns={"Year": "year"})

    # IMF program active around the crisis: any arrangement approved in [yr-1, yr+1]
    mona = pd.read_csv(os.path.join(DATA, "mona_arrangements.csv"))
    mona["iso3"] = mona.country_code.astype("Int64").astype(str).map(ifs2iso)

    def has_program(iso, yr):
        m = mona[(mona.iso3 == iso) & (mona.approval_year.between(yr - 1, yr + 1))]
        return int(len(m) > 0)

    ep["program"] = [has_program(r.iso3, r.start_year) for _, r in ep.iterrows()]
    ep = ep.merge(fo.assign(year=fo.year + 1).rename(columns={"fin_open": "fin_open_pre"}),
                  left_on=["iso3", "start_year"], right_on=["iso3", "year"], how="left")
    ep["trade_open"] = ep["pre_openness"]
    ep["prog_x_open"] = ep["program"] * ep["trade_open"]

    s = ep[(ep.start_year >= 2005) & (ep.output_loss_pct >= 1)
           & ~ep.start_year.isin(GLOBAL)].copy()
    s.to_csv(os.path.join(DATA, "horserace_panel.csv"), index=False)
    print(f"Idiosyncratic crisis episodes: {len(s)}  "
          f"(program={s.program.sum()}, with fin_open={s.fin_open_pre.notna().sum()})")

    show(ols(s, "output_loss_pct", ["fin_open_pre", "trade_open"]),
         "LEG 1  shock DEPTH ~ financial openness + trade openness")
    show(ols(s, "recovery_time", ["ext_demand", "program", "prog_x_open", "output_loss_pct"]),
         "LEG 2  recovery SPEED ~ ext_demand + program + program x openness + depth")
    show(ols(s, "recovery_time", ["trade_open", "program", "prog_x_open", "output_loss_pct"]),
         "LEG 2b recovery SPEED ~ trade_openness + program + program x openness + depth")


if __name__ == "__main__":
    main()
