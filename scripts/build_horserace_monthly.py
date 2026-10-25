"""Horse race on ENDOGENOUS downturn episodes from SA monthly activity.

Laeven-Valencia dates are too sparse for our 35 SA countries, so define episodes directly:
each maximal 'underwater' stretch (activity below its running peak) with depth >= MIN_DEPTH
is a downturn. depth = max % below peak; recov_m = months from peak to new high (censored).
Anchor year = peak year (attach annual treatments to it).

Treatments: program (MONA, active in [yr-1,yr+1]); trade_open (IMTS trade/World / WEO GDP);
fin_open (Lane-MF (assets+liab)/GDP), both pre-crisis (peak year).
Run: python scripts/build_horserace_monthly.py
"""
import os

import numpy as np
import pandas as pd

DATA = os.path.join(os.path.dirname(__file__), "..", "data")
MIN_DEPTH, CENSOR = 3.0, 60


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
        s = "***" if abs(t) > 2.6 else "**" if abs(t) > 1.96 else "*" if abs(t) > 1.64 else ""
        print(f"  {name:20s} {b:9.3f} (t={t:5.2f}) {s}")
    print(f"  R2={r2:.3f}  n={n}")


def downturns(s):
    s = s.dropna()
    if len(s) < 24:
        return []
    rm = s.cummax()
    uw = (s / rm - 1) < -1e-9
    eps, in_ep, start = [], False, 0
    for t in range(len(s)):
        if uw.iloc[t] and not in_ep:
            in_ep, start = True, t  # peak at start-1
        if in_ep and (not uw.iloc[t] or t == len(s) - 1):
            peak_i = max(start - 1, 0)
            seg = (s.iloc[peak_i:t + 1] / s.iloc[peak_i] - 1)
            depth = -seg.min() * 100
            recovered = not uw.iloc[t]
            recov_m = (s.index[t] - s.index[peak_i]).n if recovered else CENSOR
            if depth >= MIN_DEPTH:
                eps.append({"peak_year": s.index[peak_i].year,
                            "depth_m": depth, "recov_m": recov_m})
            in_ep = False
    return eps


def main():
    sa = pd.read_csv(os.path.join(DATA, "haver_activity_sa.csv"), index_col=0)
    sa.index = pd.PeriodIndex(sa.index, freq="M")
    cw = pd.read_csv(os.path.join(DATA, "ifs_iso3_crosswalk.csv"))
    mona = pd.read_csv(os.path.join(DATA, "mona_arrangements.csv"))
    name2ifs = dict(zip(mona.country_name, mona.country_code.astype("Int64").astype(str)))
    ifs2iso = dict(zip(cw.ifs.astype(str), cw.iso3))
    sa = sa.rename(columns={n: ifs2iso.get(name2ifs.get(n)) for n in sa.columns})
    sa = sa.loc[:, [c for c in sa.columns if isinstance(c, str)]]

    rows = []
    for iso in sa.columns:
        for e in downturns(sa[iso]):
            e["iso3"] = iso
            rows.append(e)
    ep = pd.DataFrame(rows)
    ep = ep[(ep.peak_year >= 2004) & (ep.peak_year <= 2024)]

    # treatments
    mona["iso3"] = mona.country_code.astype("Int64").astype(str).map(ifs2iso)
    ep["program"] = [int(len(mona[(mona.iso3 == r.iso3)
                       & mona.approval_year.between(r.peak_year - 1, r.peak_year + 1)]) > 0)
                     for _, r in ep.iterrows()]
    # trade openness (peak year): IMTS trade-to-World / WEO nominal GDP
    tw = pd.read_csv(os.path.join(DATA, "imts_world_annual.csv"))
    weo = pd.read_csv(os.path.join(DATA, "weo_realgdp_annual.csv"))
    topen = tw.merge(weo[["COUNTRY", "year", "ngdpd_usd"]],
                     left_on=["COUNTRY", "year"], right_on=["COUNTRY", "year"], how="left")
    topen["trade_open"] = topen.trade_world_usd / topen.ngdpd_usd
    ep = ep.merge(topen[["COUNTRY", "year", "trade_open"]],
                  left_on=["iso3", "peak_year"], right_on=["COUNTRY", "year"], how="left")
    lmf = pd.read_excel(os.path.join(DATA, "lmf_ewn_2024.xlsx"), sheet_name="Dataset")
    lmf["iso3"] = lmf.IFS_Code.astype("Int64").astype(str).map(ifs2iso)
    lmf["fin_open"] = (lmf["Total assets"] + lmf["Total liabilities"]) / lmf["GDP (US$)"]
    ep = ep.merge(lmf[["iso3", "Year", "fin_open"]],
                  left_on=["iso3", "peak_year"], right_on=["iso3", "Year"], how="left")
    ep["prog_x_open"] = ep.program * ep.trade_open
    ep["recovered"] = (ep.recov_m < CENSOR).astype(int)
    ep.to_csv(os.path.join(DATA, "horserace_endog.csv"), index=False)

    print(f"Endogenous downturn episodes (depth>={MIN_DEPTH}%): {len(ep)} "
          f"across {ep.iso3.nunique()} countries; programs={ep.program.sum()}")
    print(f"median depth={ep.depth_m.median():.1f}%  median recov={ep.recov_m.median():.0f}m  "
          f"recovered={ep.recovered.mean():.0%}")
    show(ols(ep, "depth_m", ["fin_open", "trade_open"]),
         "LEG 1  shock DEPTH ~ financial openness + trade openness")
    show(ols(ep, "recov_m", ["trade_open", "program", "prog_x_open", "depth_m"]),
         "LEG 2  recovery MONTHS ~ trade_open + program + program x openness + depth")


if __name__ == "__main__":
    main()
