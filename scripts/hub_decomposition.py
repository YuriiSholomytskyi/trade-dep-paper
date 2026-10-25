"""Hub test: each economy recovers through the demand of its OWN regional hub.
Assign every country to the hub it exports most to (US / Europe / China), then split the
partner-demand pull into own-hub vs non-hub, and show own-hub demand drives recovery across
blocs. This turns the 'US result is concentrated in the US bloc' diagnostic into the central
mechanism: it is a hub effect, and it holds for every hub.
Run: python scripts/hub_decomposition.py
"""
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(__file__))
from build_horserace_hp import build_episodes, ols, show  # noqa: E402

DATA = os.path.join(os.path.dirname(__file__), "..", "data")

US_HUB = {"USA"}
EU_HUB = {"AUT", "BEL", "BGR", "HRV", "CYP", "CZE", "DNK", "EST", "FIN", "FRA", "DEU",
          "GRC", "HUN", "IRL", "ITA", "LVA", "LTU", "LUX", "MLT", "NLD", "POL", "PRT",
          "ROU", "SVK", "SVN", "ESP", "SWE", "GBR", "CHE", "NOR"}
CN_HUB = {"CHN"}
HUBS = {"US": US_HUB, "EU": EU_HUB, "CN": CN_HUB}


def main():
    hp_path = os.path.join(DATA, "horserace_hp.csv")
    ep = pd.read_csv(hp_path) if os.path.exists(hp_path) else build_episodes()
    cw = pd.read_csv(os.path.join(DATA, "ifs_iso3_crosswalk.csv"))
    weo = pd.read_csv(os.path.join(DATA, "weo_realgdp_annual.csv"))
    real = set(cw.iso3)
    growth = weo[weo.COUNTRY.isin(real)].set_index(["COUNTRY", "year"])["ngdp_rpch"]
    bx = pd.read_csv(os.path.join(DATA, "imts_bilateral_sa.csv"))
    bx = bx[bx.partner.isin(real)]

    def pulls(iso, yr):
        w = bx[(bx.iso3 == iso) & (bx.year.between(yr - 3, yr - 1))].groupby("partner").exp.mean()
        w = w[(w.index != iso) & (w > 0)]
        if w.empty:
            return None
        pg = pd.Series({p: growth.reindex([(p, y) for y in range(yr, yr + 3)]).mean()
                        for p in w.index})
        v = pg.notna()
        if not v.any():
            return None
        wn = w[v] / w[v].sum()
        contrib = wn * pg[v]
        # export SHARE to each hub (assign hub by max share)
        shares = {h: float(wn[wn.index.isin(s)].sum()) for h, s in HUBS.items()}
        hub = max(shares, key=shares.get)
        hub_pull = float(contrib[contrib.index.isin(HUBS[hub])].sum())
        nonhub_pull = float(contrib.sum()) - hub_pull
        return hub, shares[hub], hub_pull, nonhub_pull

    res = [pulls(r.iso3, int(r.peak_year)) for _, r in ep.iterrows()]
    ep[["hub", "hub_share", "hub_pull", "nonhub_pull"]] = pd.DataFrame(
        [r if r else (None, np.nan, np.nan, np.nan) for r in res], index=ep.index)
    ep = ep.dropna(subset=["hub_pull"])

    # Assign each country to its modal hub across episodes (partitioning the 34 countries into 9 US, 24 EU, 1 CN)
    bycty = ep.groupby("iso3").hub.agg(lambda s: s.mode().iat[0])
    ep["cty_hub"] = ep.iso3.map(bycty)
    print("Hub assignment (countries):")
    for h in ["US", "EU", "CN"]:
        print(f"  {h}: {sorted(bycty[bycty == h].index)}")
    print(f"\nMedian own-hub export share: {ep.hub_share.median():.0%}")

    # Recompute own-hub and non-hub pull relative to each country's primary (modal) hub so bloc subsamples partition the 34 countries cleanly
    def cty_pulls(iso, yr, chub):
        w = bx[(bx.iso3 == iso) & (bx.year.between(yr - 3, yr - 1))].groupby("partner").exp.mean()
        w = w[(w.index != iso) & (w > 0)]
        pg = pd.Series({p: growth.reindex([(p, y) for y in range(yr, yr + 3)]).mean()
                        for p in w.index})
        v = pg.notna()
        wn = w[v] / w[v].sum()
        contrib = wn * pg[v]
        hp_val = float(contrib[contrib.index.isin(HUBS[chub])].sum())
        nhp_val = float(contrib.sum()) - hp_val
        return hp_val, nhp_val

    cp = [cty_pulls(r.iso3, int(r.peak_year), r.cty_hub) for _, r in ep.iterrows()]
    ep[["hub_pull", "nonhub_pull"]] = pd.DataFrame(cp, index=ep.index)

    ep["is_us_hub"] = (ep.cty_hub == "US").astype(int)
    ep["is_eu_hub"] = (ep.cty_hub == "EU").astype(int)
    ep["is_cn_hub"] = (ep.cty_hub == "CN").astype(int)
    ep["hub_pull_us"] = ep.hub_pull * ep.is_us_hub
    ep["hub_pull_eu"] = ep.hub_pull * ep.is_eu_hub
    ep["hub_pull_cn"] = ep.hub_pull * ep.is_cn_hub

    print("\n=== Own-hub vs non-hub demand pull (with hub-bloc FE), country-clustered ===")
    r_pool_climb = ols(ep, "t_climb", ["hub_pull", "nonhub_pull", "trade_open", "depth_gap",
                                       "program", "is_us_hub", "is_cn_hub"])
    r_pool_full = ols(ep, "t_full", ["hub_pull", "nonhub_pull", "trade_open", "depth_gap",
                                     "program", "is_us_hub", "is_cn_hub"])
    show(r_pool_climb, "CLIMB (trough->peak)")
    show(r_pool_full, "FULL cycle")

    r_inter = ols(ep, "t_full", ["hub_pull_us", "hub_pull_eu", "hub_pull_cn",
                                 "nonhub_pull", "is_us_hub", "is_cn_hub",
                                 "trade_open", "depth_gap", "program"])
    show(r_inter, "POOLED INTERACTION (FULL cycle)")

    # Wild cluster bootstrap (Rademacher weights, restricted under H0: beta_hub_pull = 0)
    def wild_boot_pval(df, y, target, controls, cluster="iso3", B=4999, seed=42):
        d = df.dropna(subset=[y, target] + controls + [cluster]).copy()
        res_u = ols(d, y, [target] + controls, cluster=cluster)
        cd = {k: (b, se) for k, b, se in res_u[0]}
        t_obs = cd[target][0] / cd[target][1]
        Xc = np.column_stack([np.ones(len(d))] + [d[c].values.astype(float) for c in controls])
        yv = d[y].values.astype(float)
        b_r = np.linalg.lstsq(Xc, yv, rcond=None)[0]
        yhat_r = Xc @ b_r
        u_r = yv - yhat_r
        groups = d[cluster].values
        uniq_g = np.unique(groups)
        G = len(uniq_g)
        X = np.column_stack([np.ones(len(d)), d[target].values.astype(float)] +
                            [d[c].values.astype(float) for c in controls])
        XtX_inv = np.linalg.inv(X.T @ X)
        n, k = len(d), X.shape[1]
        corr = (G / (G - 1)) * ((n - 1) / (n - k))
        g_idx = [np.where(groups == g)[0] for g in uniq_g]
        rng = np.random.default_rng(seed)
        weights = rng.choice([-1.0, 1.0], size=(B, G))
        count = 0
        for b_i in range(B):
            u_star = u_r.copy()
            for gi, idx in enumerate(g_idx):
                u_star[idx] *= weights[b_i, gi]
            y_star = yhat_r + u_star
            b_star = XtX_inv @ (X.T @ y_star)
            e_star = y_star - X @ b_star
            meat = np.zeros((k, k))
            for idx in g_idx:
                s = X[idx].T @ e_star[idx]
                meat += np.outer(s, s)
            se_star = np.sqrt(corr * (XtX_inv[1] @ meat @ XtX_inv[1]))
            t_star = b_star[1] / se_star if se_star > 0 else 0.0
            if abs(t_star) >= abs(t_obs):
                count += 1
        return (count + 1) / (B + 1)

    # per-bloc: own-hub demand within each bloc
    print("\n=== Own-hub demand, within each bloc (full cycle) ===")
    bloc_res = {}
    bloc_wb = {}
    for h in ["US", "EU", "CN"]:
        sub = ep[ep.cty_hub == h]
        if sub.iso3.nunique() < 4:
            print(f"  {h}: too few countries ({sub.iso3.nunique()})"); continue
        r = ols(sub, "t_full", ["hub_pull", "nonhub_pull", "trade_open", "depth_gap", "program"])
        r_par = ols(sub, "t_full", ["hub_pull", "trade_open", "depth_gap"])
        bloc_res[h] = (r, r_par)
        wb_p = wild_boot_pval(sub, "t_full", "hub_pull", ["nonhub_pull", "trade_open", "depth_gap", "program"])
        wb_p_par = wild_boot_pval(sub, "t_full", "hub_pull", ["trade_open", "depth_gap"])
        bloc_wb[h] = (wb_p, wb_p_par)
        if r:
            coefs, r2, n, G = r
            b, se = dict((x[0], (x[1], x[2])) for x in coefs)["hub_pull"]
            b0, se0 = dict((x[0], (x[1], x[2])) for x in r_par[0])["hub_pull"]
            print(f"  {h}-hub bloc (n={n}, {G} countries): full ctrl = {b:.2f} (t={b/se:.2f}, wb p={wb_p:.3f}); "
                  f"parsimonious = {b0:.2f} (t={b0/se0:.2f}, wb p={wb_p_par:.3f})")

    # Save LaTeX table output/tables_hubs.tex
    OUT = os.path.join(os.path.dirname(__file__), "..", "output")
    def cell(res, key):
        if not res:
            return ""
        d = {k: (b, se) for k, b, se in res[0]}
        if key not in d:
            return ""
        b, se = d[key]
        t = b / se if se else 0
        star = "***" if abs(t) > 2.58 else "**" if abs(t) > 1.96 else "*" if abs(t) > 1.64 else ""
        val = f"${b:.2f}^{{{star}}}$" if star else f"${b:.2f}$"
        return f"{val} {{\\scriptsize$({t:.1f})$}}"

    r_us, _ = bloc_res["US"]
    r_eu, _ = bloc_res["EU"]
    wb_us = bloc_wb["US"][0]
    wb_eu = bloc_wb["EU"][0]
    wb_pool_climb = wild_boot_pval(ep, "t_climb", "hub_pull",
                                   ["nonhub_pull", "trade_open", "depth_gap", "program", "is_us_hub", "is_cn_hub"])
    wb_pool_full = wild_boot_pval(ep, "t_full", "hub_pull",
                                  ["nonhub_pull", "trade_open", "depth_gap", "program", "is_us_hub", "is_cn_hub"])

    tex = [
        r"\begin{table}[t]", r"\centering\small",
        r"\caption{Regional hub demand and recovery duration. Each economy is assigned to its "
        r"primary regional export hub (United States, European Union, or China; Table~\ref{tab:appcountries}). "
        r"Columns 1--2 pool all episodes with hub-bloc fixed effects for the climb phase and the full "
        r"negative cycle; columns 3--4 estimate the full-cycle specification separately within the "
        r"US-hub and EU-hub subsamples; column 5 estimates a pooled full-cycle regression interacting "
        r"own-hub demand with hub-bloc indicators. Country-clustered $t$-statistics in parentheses.}",
        r"\label{tab:hubs}",
        r"\begin{tabularx}{\textwidth}{@{}lYYYYY@{}}", r"\toprule",
        r" & (1) Pooled & (2) Pooled & (3) US-hub & (4) EU-hub & (5) Pooled \\",
        r" & Climb & Full cycle & Full cycle & Full cycle & Interaction \\ \midrule",
        f"Own-hub demand & {cell(r_pool_climb, 'hub_pull')} & {cell(r_pool_full, 'hub_pull')} & "
        f"{cell(r_us, 'hub_pull')} & {cell(r_eu, 'hub_pull')} & \\\\",
        f"Own-hub $\\times$ US-hub bloc & & & & & {cell(r_inter, 'hub_pull_us')} \\\\",
        f"Own-hub $\\times$ EU-hub bloc & & & & & {cell(r_inter, 'hub_pull_eu')} \\\\",
        f"Non-hub demand & {cell(r_pool_climb, 'nonhub_pull')} & {cell(r_pool_full, 'nonhub_pull')} & "
        f"{cell(r_us, 'nonhub_pull')} & {cell(r_eu, 'nonhub_pull')} & {cell(r_inter, 'nonhub_pull')} \\\\",
        f"Trade openness & {cell(r_pool_climb, 'trade_open')} & {cell(r_pool_full, 'trade_open')} & "
        f"{cell(r_us, 'trade_open')} & {cell(r_eu, 'trade_open')} & {cell(r_inter, 'trade_open')} \\\\",
        f"Depth of downturn & {cell(r_pool_climb, 'depth_gap')} & {cell(r_pool_full, 'depth_gap')} & "
        f"{cell(r_us, 'depth_gap')} & {cell(r_eu, 'depth_gap')} & {cell(r_inter, 'depth_gap')} \\\\",
        r"\midrule",
        f"Wild bootstrap $p$ (own-hub) & ${wb_pool_climb:.3f}$ & ${wb_pool_full:.3f}$ & ${wb_us:.3f}$ & ${wb_eu:.3f}$ & \\\\",
        f"Episodes & {r_pool_climb[2]} & {r_pool_full[2]} & {r_us[2]} & {r_eu[2]} & {r_inter[2]} \\\\",
        f"Countries & {r_pool_climb[3]} & {r_pool_full[3]} & {r_us[3]} & {r_eu[3]} & {r_inter[3]} \\\\",
        r"\bottomrule", r"\end{tabularx}",
        r"\\[2pt]\footnotesize{All columns control for an active IMF-supported arrangement (MONA); "
        r"columns 1, 2, and 5 include hub-bloc fixed effects, and column 5 also includes the China-hub "
        r"interaction (4 episodes in Mongolia). Wild cluster bootstrap $p$-values use 4,999 Rademacher "
        r"draws imposed under the null hypothesis (Cameron, Gelbach, and Miller, 2008). "
        r"$^{*},^{**},^{***}$: significant at 10, 5, 1 percent.}",
        r"\end{table}",
    ]
    with open(os.path.join(OUT, "tables_hubs.tex"), "w", encoding="utf-8") as f:
        f.write("\n".join(tex) + "\n")
    print("saved output/tables_hubs.tex")

    ep.drop(columns=["cty_hub", "is_us_hub", "is_eu_hub", "is_cn_hub",
                     "hub_pull_us", "hub_pull_eu", "hub_pull_cn"]).to_csv(
        os.path.join(DATA, "hub_panel.csv"), index=False)


if __name__ == "__main__":
    main()
