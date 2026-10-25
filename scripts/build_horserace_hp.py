"""HP-output-gap cycle + horse race: 3 timing measures, country-clustered SEs, and the
China-vs-rest decomposition of the healthy-partner demand pull.

Cycle: HP filter on log SA activity (monthly lamb=129600) -> output gap (%). Negative-gap
episodes (depth>=MIN_DEPTH). Timings: t_full (peak->peak), t_contraction (peak->trough),
t_climb (trough->peak); depth_gap = -min gap.

ext_demand = sum_p w_p g_p  (w_p pre-crisis export share, g_p partner real GDP growth over
peak..peak+2). Decomposed:  china_pull = w_CHN*g_CHN ;  rest_pull = ext_demand - china_pull.
china_w = export share to China (to show the rising link).

SEs clustered by country. ONE_SIDED=True -> real-time HP (endpoint robustness).
Run: python scripts/build_horserace_hp.py
"""
import os

import numpy as np
import pandas as pd
from statsmodels.tsa.filters.hp_filter import hpfilter

DATA = os.path.join(os.path.dirname(__file__), "..", "data")
LAMB, MIN_DEPTH, CENSOR = 129600, 2.0, 60
ONE_SIDED = False
# Persistence horizons (months the gap must stay >=0) for the crossing-independent recovery
# measure that answers the referee's "short zero-crossings mechanically mark recovery" concern.
PERSIST_KS = (3, 6)

# IMF advanced economies (ISO3) - the "good actors" whose stable demand may pull others out.
ADVANCED = {
    "USA", "CAN", "GBR", "DEU", "FRA", "ITA", "ESP", "NLD", "BEL", "AUT", "FIN", "GRC",
    "PRT", "IRL", "LUX", "JPN", "KOR", "AUS", "NZL", "CHE", "NOR", "SWE", "DNK", "ISL",
    "SGP", "HKG", "TWN", "ISR", "CYP", "MLT", "SVN", "SVK", "EST", "LVA", "LTU", "CZE",
}
# Commodity exporters (fuel/metals/agri) among the episode countries - to test whether the
# "China pull -> deeper downturn" result is just commodity-exporter composition.
COMMODITY = {
    "ARG", "CHL", "COL", "ECU", "PER", "PRY", "SUR", "MOZ", "MNG", "KGZ", "RWA",
    "AGO", "NGA", "ZMB", "AZE", "RUS", "BOL", "GHA", "KAZ",
}


def ols(d, y, xs, cluster="iso3"):
    """OLS with cluster-robust (by `cluster`) SEs."""
    d = d.dropna(subset=[y] + xs + [cluster])
    if len(d) < len(xs) + 5:
        return None
    X = np.column_stack([np.ones(len(d))] + [d[x].values.astype(float) for x in xs])
    yv = d[y].values.astype(float)
    XtX_inv = np.linalg.inv(X.T @ X)
    b = XtX_inv @ X.T @ yv
    u = yv - X @ b
    meat = np.zeros((X.shape[1], X.shape[1]))
    groups = d[cluster].values
    for g in np.unique(groups):
        Xg, ug = X[groups == g], u[groups == g]
        s = Xg.T @ ug
        meat += np.outer(s, s)
    G, n, k = len(np.unique(groups)), len(d), X.shape[1]
    corr = (G / (G - 1)) * ((n - 1) / (n - k))
    V = corr * XtX_inv @ meat @ XtX_inv
    se = np.sqrt(np.diag(V))
    r2 = 1 - (u @ u) / ((yv - yv.mean()) ** 2).sum()
    return list(zip(["const"] + xs, b, se)), r2, n, G


def show(res, title):
    print(f"\n{title}")
    if not res:
        print("  (insufficient obs)"); return
    coefs, r2, n, G = res
    for name, b, se in coefs:
        t = b / se if se else 0
        s = "***" if abs(t) > 2.6 else "**" if abs(t) > 1.96 else "*" if abs(t) > 1.64 else ""
        print(f"  {name:14s} {b:9.3f} (t={t:5.2f}) {s}")
    print(f"  R2={r2:.3f}  n={n}  clusters={G}")


def gap_series(s, one_sided=ONE_SIDED, filter_type="hp", hamilton_h=24, hamilton_p=4):
    s = s.dropna()
    ls = np.log(s.clip(lower=1e-9))
    if filter_type == "hamilton":
        # Hamilton (2018) linear projection filter: y_t on const and y_{t-h}, ..., y_{t-h-p+1}
        n = len(ls)
        start = hamilton_h + hamilton_p - 1
        if n <= start + 12:
            return pd.Series(dtype=float)
        yv = ls.values[start:]
        X_cols = [np.ones(len(yv))]
        for lag in range(hamilton_h, hamilton_h + hamilton_p):
            X_cols.append(ls.values[start - lag:n - lag])
        X = np.column_stack(X_cols)
        beta = np.linalg.lstsq(X, yv, rcond=None)[0]
        resid = (yv - X @ beta) * 100.0
        return pd.Series(resid, index=ls.index[start:])
    if one_sided:
        trend = pd.Series(index=ls.index, dtype=float)
        for i in range(36, len(ls) + 1):
            trend.iloc[i - 1] = hpfilter(ls.iloc[:i], lamb=LAMB)[1].iloc[-1]
        return ((ls - trend) * 100).dropna()
    return (hpfilter(ls, lamb=LAMB)[0] * 100).dropna()


def _persist_recovery(gap, trough_i, k):
    """First month index at/after the trough where the gap is >=0 and stays >=0 for k
    consecutive months. Returns None if no such sustained return exists within the series
    (the k-month confirmation window must fit before the series ends)."""
    vals = gap.values
    n = len(vals)
    for r in range(trough_i, n - k + 1):
        if (vals[r:r + k] >= 0).all():
            return r
    return None


def episodes_from_gap(gap, min_depth=MIN_DEPTH, min_dur=1, merge_gap=0):
    below = (gap < 0).copy()
    if merge_gap > 0 and len(below) > 2:
        # Bridge isolated non-negative blips of length <= merge_gap between negative spells
        bvals = below.values.copy()
        i = 0
        n = len(bvals)
        while i < n:
            if not bvals[i]:
                j = i
                while j < n and not bvals[j]:
                    j += 1
                if i > 0 and j < n and (j - i) <= merge_gap:
                    bvals[i:j] = True
                i = j
            else:
                i += 1
        below = pd.Series(bvals, index=gap.index)
    eps, in_ep, start = [], False, 0
    for t in range(len(gap)):
        if below.iloc[t] and not in_ep:
            in_ep, start = True, t
        if in_ep and (not below.iloc[t] or t == len(gap) - 1):
            seg = gap.iloc[start:t + 1]
            depth = -seg.min()
            peak_i, trough_i = start, start + seg.values.argmin()
            rec_i = t if not below.iloc[t] else None
            dur_spell = (gap.index[rec_i] - gap.index[peak_i]).n if rec_i else CENSOR
            if depth >= min_depth and dur_spell >= min_dur:
                row = {"peak_year": gap.index[peak_i].year, "depth_gap": depth,
                       "t_contraction": (gap.index[trough_i] - gap.index[peak_i]).n,
                       "t_full": dur_spell,
                       "t_climb": (gap.index[rec_i] - gap.index[trough_i]).n if rec_i else CENSOR}
                # --- crossing-independent recovery outcomes (referee: HP zero-crossing) ---
                # Cumulative activity loss: area of the negative gap over the spell (a magnitude,
                # not a crossing date), so it does not depend on when the gap first touches zero.
                row["cum_loss"] = float(-seg[seg < 0].sum())
                # Persistent-return durations: recovery dated only once the gap stays >=0 for k
                # months, searching the full series so a brief crossing does not end the spell.
                for k in PERSIST_KS:
                    rp = _persist_recovery(gap, trough_i, k)
                    row[f"t_full_p{k}"] = (gap.index[rp] - gap.index[peak_i]).n if rp is not None else CENSOR
                    row[f"t_climb_p{k}"] = (gap.index[rp] - gap.index[trough_i]).n if rp is not None else CENSOR
                eps.append(row)
            in_ep = False
    return eps


def build_episodes(one_sided=False, min_depth=MIN_DEPTH, crisis_only=False,
                   min_dur=1, merge_gap=0, filter_type="hp"):
    """Build the episode panel with treatments + partner-demand decomposition.
    one_sided : real-time (expanding-window) HP trend.
    min_depth : minimum gap depth (%) for an episode.
    crisis_only : keep only episodes near a Laeven-Valencia crisis (peak_year within +/-1).
    min_dur : minimum negative-spell duration (months).
    merge_gap : bridge non-negative blips of length <= merge_gap months between negative spells.
    filter_type : 'hp' (default) or 'hamilton' (Hamilton 2018 linear projection filter).
    """
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
        try:
            g = gap_series(sa[iso], one_sided=one_sided, filter_type=filter_type)
        except Exception:
            continue
        if g.empty:
            continue
        for e in episodes_from_gap(g, min_depth=min_depth, min_dur=min_dur, merge_gap=merge_gap):
            e["iso3"] = iso
            rows.append(e)
    ep = pd.DataFrame(rows)
    ep = ep[(ep.peak_year >= 2004) & (ep.peak_year <= 2024)]

    mona["iso3"] = mona.country_code.astype("Int64").astype(str).map(ifs2iso)

    def prog_focus(iso, yr):
        m = mona[(mona.iso3 == iso) & mona.approval_year.between(yr - 1, yr + 1)]
        if m.empty:
            return 0, 0, 0
        return 1, int(m.focus_exchange_rate.max()), int(m.focus_trade.max())

    pf = [prog_focus(r.iso3, r.peak_year) for _, r in ep.iterrows()]
    ep[["program", "f_fx", "f_trade"]] = pd.DataFrame(pf, index=ep.index)
    # program decomposed by instrument content
    ep["prog_fx"] = ep.program * ep.f_fx            # program WITH exchange-rate focus (devaluation)
    ep["prog_nofx"] = ep.program * (1 - ep.f_fx)    # program WITHOUT exchange-rate focus
    ep["prog_trade"] = ep.program * ep.f_trade      # program WITH trade-liberalization focus
    tw = pd.read_csv(os.path.join(DATA, "imts_world_annual.csv"))
    weo = pd.read_csv(os.path.join(DATA, "weo_realgdp_annual.csv"))
    topen = tw.merge(weo[["COUNTRY", "year", "ngdpd_usd"]], on=["COUNTRY", "year"], how="left")
    topen["trade_open"] = topen.trade_world_usd / topen.ngdpd_usd
    ep = ep.merge(topen[["COUNTRY", "year", "trade_open"]],
                  left_on=["iso3", "peak_year"], right_on=["COUNTRY", "year"], how="left")

    # ext_demand decomposed into China vs rest.
    # IMPORTANT: restrict partners to REAL countries (crosswalk ISO3). WEO's country list
    # also contains aggregate group codes (G001=World, G200, ...) which would otherwise
    # enter the weighted partner average and dilute/contaminate it.
    real_countries = set(cw.iso3)
    bx = pd.read_csv(os.path.join(DATA, "imts_bilateral_sa.csv"))
    bx = bx[bx.partner.isin(real_countries)]
    growth = weo[weo.COUNTRY.isin(real_countries)].set_index(["COUNTRY", "year"])["ngdp_rpch"]

    def extdem(iso, yr):
        w = bx[(bx.iso3 == iso) & (bx.year.between(yr - 3, yr - 1))].groupby("partner").exp.mean()
        w = w[(w.index != iso) & (w > 0)]
        if w.empty:
            return (np.nan,) * 8
        yrs = list(range(yr, yr + 3))
        pg = pd.Series({p: growth.reindex([(p, y) for y in yrs]).mean() for p in w.index})
        pv = pd.Series({p: growth.reindex([(p, y) for y in yrs]).std() for p in w.index})
        v = pg.notna()
        if not v.any():
            return (np.nan,) * 8
        wn = w[v] / w[v].sum()
        contrib = wn * pg[v]                       # each partner's contribution to the pull
        total = float(contrib.sum())
        is_chn = contrib.index == "CHN"
        is_adv = contrib.index.isin(ADVANCED)
        china_pull = float(contrib[is_chn].sum())
        adv_pull = float(contrib[is_adv].sum())
        emer_pull = float(contrib[~is_adv & ~is_chn].sum())   # EMs excl China
        us_pull = float(contrib[contrib.index == "USA"].sum())
        otheradv_pull = adv_pull - us_pull                    # advanced economies excl US
        us_w = float(wn[wn.index == "USA"].sum())
        vv = pv.reindex(wn.index).notna()                     # exposure-weighted partner volatility
        partner_vol = float((wn[vv] * pv.reindex(wn.index)[vv]).sum() / wn[vv].sum()) if vv.any() else np.nan
        return (total, china_pull, adv_pull, emer_pull, us_pull, otheradv_pull, us_w, partner_vol)

    vals = [extdem(r.iso3, int(r.peak_year)) for _, r in ep.iterrows()]
    ep[["ext_demand", "china_pull", "adv_pull", "emer_pull",
        "us_pull", "otheradv_pull", "us_w", "partner_vol"]] = pd.DataFrame(vals, index=ep.index)
    ep["commodity"] = ep.iso3.isin(COMMODITY).astype(int)
    ep["china_pull_comm"] = ep.china_pull * ep.commodity
    ep["china_pull_noncomm"] = ep.china_pull * (1 - ep.commodity)
    ep["prog_fx_x_adv"] = ep.prog_fx * ep.adv_pull

    if crisis_only:
        crises = pd.read_csv(os.path.join(DATA, "..", "laeven_valencia_crisis_dates.csv"))
        crises = crises.dropna(subset=["iso3", "start_year"])
        crises["start_year"] = crises.start_year.astype(int)
        key = set(zip(crises.iso3, crises.start_year))
        near = ep.apply(lambda r: any((r.iso3, r.peak_year + d) in key
                                      for d in (-1, 0, 1)), axis=1)
        ep = ep[near]
    return ep


def main():
    ep = build_episodes(one_sided=ONE_SIDED, min_depth=MIN_DEPTH)
    ep.to_csv(os.path.join(DATA, "horserace_hp.csv"), index=False)
    print(f"HP negative-cycle episodes (depth>={MIN_DEPTH}%, {'1-sided' if ONE_SIDED else '2-sided'} HP): "
          f"{len(ep)} / {ep.iso3.nunique()} countries; programs={ep.program.sum()}")
    print(f"median US export share={ep.us_w.median():.0%}")

    print("\n=== Total partner pull, country-clustered SEs ===")
    show(ols(ep, "t_climb", ["ext_demand", "trade_open", "program", "depth_gap"]), "CLIMB (trough->peak)")
    show(ols(ep, "t_full", ["ext_demand", "trade_open", "program", "depth_gap"]), "FULL cycle")

    print("\n=== US vs OTHER-ADVANCED vs EMERGING demand pull, clustered ===")
    show(ols(ep, "t_climb", ["us_pull", "otheradv_pull", "emer_pull", "china_pull",
                             "trade_open", "depth_gap"]), "CLIMB (trough->peak)")
    show(ols(ep, "t_full", ["us_pull", "otheradv_pull", "emer_pull", "china_pull",
                            "trade_open", "depth_gap"]), "FULL cycle")

    print("\n=== ADVANCED vs EMERGING vs CHINA demand pull ('good actors' test), clustered ===")
    show(ols(ep, "t_climb", ["adv_pull", "emer_pull", "china_pull", "trade_open", "program", "depth_gap"]),
         "CLIMB (trough->peak)")
    show(ols(ep, "t_full", ["adv_pull", "emer_pull", "china_pull", "trade_open", "program", "depth_gap"]),
         "FULL cycle")
    show(ols(ep, "depth_gap", ["adv_pull", "emer_pull", "china_pull", "trade_open", "program"]),
         "DEPTH")

    # Is "China -> deeper" just commodity-exporter composition? Split china_pull by it.
    ep["commodity"] = ep.iso3.isin(COMMODITY).astype(int)
    ep["china_pull_comm"] = ep.china_pull * ep.commodity
    ep["china_pull_noncomm"] = ep.china_pull * (1 - ep.commodity)
    print(f"\ncommodity-exporter episodes: {ep.commodity.sum()}/{len(ep)}")
    show(ols(ep, "depth_gap", ["china_pull_comm", "china_pull_noncomm", "commodity",
                               "emer_pull", "adv_pull", "trade_open", "program"]),
         "DEPTH: China pull split by COMMODITY vs non-commodity exporter")

    print(f"\n=== PROGRAM BY INSTRUMENT (fx-focus={ep.prog_fx.sum()}, no-fx={ep.prog_nofx.sum()}, "
          f"trade-focus={ep.prog_trade.sum()}), clustered ===")
    show(ols(ep, "t_climb", ["prog_fx", "prog_nofx", "adv_pull", "emer_pull",
                             "trade_open", "depth_gap"]),
         "CLIMB ~ program(FX) + program(no-FX) + partner pulls")
    show(ols(ep, "t_full", ["prog_fx", "prog_nofx", "adv_pull", "emer_pull",
                            "trade_open", "depth_gap"]),
         "FULL cycle ~ program(FX) + program(no-FX) + partner pulls")
    show(ols(ep, "depth_gap", ["prog_fx", "prog_nofx", "prog_trade", "adv_pull",
                               "emer_pull", "trade_open"]),
         "DEPTH ~ program(FX) + program(no-FX) + program(trade)")

    # The full mechanism: devaluation works only when advanced partners are growing.
    ep["prog_fx_x_adv"] = ep.prog_fx * ep.adv_pull
    print("\n=== TRIPLE: devaluation program x advanced-partner demand, clustered ===")
    show(ols(ep, "t_climb", ["prog_fx", "adv_pull", "prog_fx_x_adv", "prog_nofx",
                             "emer_pull", "trade_open", "depth_gap"]),
         "CLIMB ~ prog_fx + adv_pull + prog_fx*adv_pull + ...")
    show(ols(ep, "t_full", ["prog_fx", "adv_pull", "prog_fx_x_adv", "prog_nofx",
                            "emer_pull", "trade_open", "depth_gap"]),
         "FULL ~ prog_fx + adv_pull + prog_fx*adv_pull + ...")


if __name__ == "__main__":
    main()
