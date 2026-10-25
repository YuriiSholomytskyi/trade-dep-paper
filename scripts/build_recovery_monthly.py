"""Monthly recovery metrics (from SA activity) + re-run the two-leg horse race.

For each idiosyncratic crisis episode in a country with SA monthly activity:
  peak  = max SA level in [start_year-1 .. start_year]      (pre-crisis peak month)
  trough= min SA level in [peak .. peak+36m]
  depth_m = 100*(peak-trough)/peak                          (precise monthly output loss)
  recov_m = months from peak until SA regains peak (<=60m, else censored)
Keeps episodes with a real contraction (depth_m >= 2).

Then horse race (program x openness etc.) on the monthly-derived sample.
Run: python scripts/build_recovery_monthly.py
"""
import os

import numpy as np
import pandas as pd

DATA = os.path.join(os.path.dirname(__file__), "..", "data")
GLOBAL = {2008, 2009, 2020}
HORIZON, CENSOR = 36, 60


def ols(d, y, xs):
    d = d.dropna(subset=[y] + xs)
    if len(d) < len(xs) + 3:
        return None
    X = np.column_stack([np.ones(len(d))] + [d[x].values for x in xs])
    b, *_ = np.linalg.lstsq(X, d[y].values, rcond=None)
    resid = d[y].values - X @ b
    n, k = len(d), X.shape[1]
    se = np.sqrt(np.diag((resid @ resid) / (n - k) * np.linalg.inv(X.T @ X)))
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
        print(f"  {name:20s} {b:9.3f} (t={t:5.2f}) {star}")
    print(f"  R2={r2:.3f}  n={n}")


def recovery(sa, yr):
    """peak/trough/depth/recovery-months for a crisis starting in year yr."""
    pre = sa[(sa.index >= pd.Period(yr - 1, "M")) & (sa.index <= pd.Period(f"{yr}-12", "M"))]
    if pre.empty:
        return None
    peak_m = pre.idxmax(); peak = pre.max()
    post = sa[(sa.index >= peak_m) & (sa.index <= peak_m + HORIZON)]
    if post.empty:
        return None
    trough = post.min()
    depth = 100 * (peak - trough) / peak if peak else np.nan
    fut = sa[(sa.index > peak_m) & (sa.index <= peak_m + CENSOR)]
    regained = fut[fut >= peak]
    recov_m = (regained.index.min() - peak_m).n if len(regained) else np.nan
    return depth, recov_m


def main():
    sa = pd.read_csv(os.path.join(DATA, "haver_activity_sa.csv"), index_col=0)
    sa.index = pd.PeriodIndex(sa.index, freq="M")
    # re-key SA columns (MONA names) -> ISO3
    cw = pd.read_csv(os.path.join(DATA, "ifs_iso3_crosswalk.csv"))
    mona = pd.read_csv(os.path.join(DATA, "mona_arrangements.csv"))
    name2ifs = dict(zip(mona.country_name, mona.country_code.astype("Int64").astype(str)))
    ifs2iso = dict(zip(cw.ifs.astype(str), cw.iso3))
    name2iso = {n: ifs2iso.get(name2ifs.get(n)) for n in sa.columns}
    sa = sa.rename(columns=name2iso)
    sa = sa.loc[:, [c for c in sa.columns if isinstance(c, str)]]

    crises = pd.read_csv(os.path.join(DATA, "..", "laeven_valencia_crisis_dates.csv"))
    crises = crises.dropna(subset=["iso3", "start_year"])
    crises["start_year"] = crises.start_year.astype(int)
    crises = crises[(crises.start_year >= 2005) & (~crises.start_year.isin(GLOBAL))]
    crises = crises[crises.iso3.isin(sa.columns)].drop_duplicates(["iso3", "start_year"])

    rows = []
    for _, c in crises.iterrows():
        r = recovery(sa[c.iso3].dropna(), c.start_year)
        if r is None:
            continue
        depth, recov_m = r
        rows.append({"iso3": c.iso3, "start_year": c.start_year,
                     "depth_m": depth, "recov_m": recov_m})
    ep = pd.DataFrame(rows)
    ep = ep[ep.depth_m >= 2]  # real contraction
    ep["recov_m"] = ep.recov_m.fillna(CENSOR)  # censor non-recoveries

    # attach treatments: program, fin_open, trade_open, ext_demand
    mona["iso3"] = mona.country_code.astype("Int64").astype(str).map(ifs2iso)
    ep["program"] = [int(len(mona[(mona.iso3 == r.iso3)
                       & mona.approval_year.between(r.start_year - 1, r.start_year + 1)]) > 0)
                     for _, r in ep.iterrows()]
    ext = pd.read_csv(os.path.join(DATA, "step1_panel_extdemand.csv"))
    ext = ext.drop_duplicates(["iso3", "start_year"])[["iso3", "start_year", "pre_openness", "ext_demand"]]
    ep = ep.merge(ext, on=["iso3", "start_year"], how="left").rename(columns={"pre_openness": "trade_open"})
    lmf = pd.read_excel(os.path.join(DATA, "lmf_ewn_2024.xlsx"), sheet_name="Dataset")
    lmf["iso3"] = lmf.IFS_Code.astype("Int64").astype(str).map(ifs2iso)
    lmf["fin_open"] = (lmf["Total assets"] + lmf["Total liabilities"]) / lmf["GDP (US$)"]
    fo = lmf[["iso3", "Year", "fin_open"]].rename(columns={"Year": "year"})
    fo["year"] = fo.year + 1
    ep = ep.merge(fo, left_on=["iso3", "start_year"], right_on=["iso3", "year"], how="left")
    ep["prog_x_open"] = ep.program * ep.trade_open
    ep.to_csv(os.path.join(DATA, "horserace_panel_monthly.csv"), index=False)

    print(f"Monthly-derived idiosyncratic episodes (depth>=2%): {len(ep)} "
          f"across {ep.iso3.nunique()} countries; programs={ep.program.sum()}")
    print(f"median depth={ep.depth_m.median():.1f}%  median recov={ep.recov_m.median():.0f} months")
    show(ols(ep, "depth_m", ["fin_open", "trade_open"]),
         "LEG 1  shock DEPTH ~ financial openness + trade openness")
    show(ols(ep, "recov_m", ["ext_demand", "program", "prog_x_open", "depth_m"]),
         "LEG 2  recovery MONTHS ~ ext_demand + program + program x openness + depth")
    show(ols(ep, "recov_m", ["trade_open", "program", "prog_x_open", "depth_m"]),
         "LEG 2b recovery MONTHS ~ trade_open + program + program x openness + depth")


if __name__ == "__main__":
    main()
