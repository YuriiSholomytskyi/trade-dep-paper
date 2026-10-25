"""Clean-timing robustness for the demand result.

The baseline demand measure weights partner growth over a fixed window anchored at the peak,
[peak, peak+2], by pre-crisis export shares. A referee may still worry that partner growth over
that window overlaps the recovery it is meant to explain. This script rebuilds the US-demand pull
with shifts that are predetermined relative to the recovery and re-estimates the duration
regressions:

  baseline  : partner growth over [peak, peak+2]      (the paper's measure)
  onset     : partner growth in the peak year only     (set at the shock, before the rebound)
  prewindow : partner growth over [peak-5, peak-1]      (fully pre-sample; no overlap at all)

Weights are always the pre-crisis export shares (mean of [peak-3, peak-1]). If the US coefficient
survives under the onset and prewindow shifts, the result is not an artefact of window overlap.

Output: prints the US-demand coefficient on the full cycle and the climb under each timing.
Run: python scripts/prewindow_demand.py
"""
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(__file__))
from build_horserace_hp import ols, DATA  # noqa: E402

OUT = os.path.join(os.path.dirname(__file__), "..", "output")


def main():
    hub = pd.read_csv(os.path.join(DATA, "hub_panel.csv"))
    bx = pd.read_csv(os.path.join(DATA, "imts_bilateral_exports_annual.csv"))
    weo = pd.read_csv(os.path.join(DATA, "weo_realgdp_annual.csv"))
    cw = pd.read_csv(os.path.join(DATA, "ifs_iso3_crosswalk.csv"))
    real = set(cw.iso3)
    bx = bx[bx.partner.isin(real)]
    growth = weo[weo.COUNTRY.isin(real)].set_index(["COUNTRY", "year"])["ngdp_rpch"]

    def pull(iso, yr, years, partner="USA"):
        """Export-share-weighted partner growth over `years`; also the single-partner (US) pull."""
        w = bx[(bx.COUNTRY == iso) & (bx.year.between(yr - 3, yr - 1))].groupby("partner").exp_usd.mean()
        w = w[(w.index != iso) & (w > 0)]
        if w.empty:
            return np.nan, np.nan
        g = pd.Series({p: growth.reindex([(p, y) for y in years]).mean() for p in w.index})
        v = g.notna()
        if not v.any():
            return np.nan, np.nan
        wn = w[v] / w[v].sum()
        total = float((wn * g[v]).sum())
        us = float(wn[wn.index == partner].sum() * g.get(partner, np.nan)) \
            if partner in wn.index and pd.notna(g.get(partner)) else 0.0
        return total, us

    windows = {
        "baseline":  lambda yr: range(yr, yr + 3),
        "onset":     lambda yr: [yr],
        "prewindow": lambda yr: range(yr - 5, yr),
    }
    for name, wf in windows.items():
        tot, us = [], []
        for _, r in hub.iterrows():
            t, u = pull(r.iso3, int(r.peak_year), list(wf(int(r.peak_year))))
            tot.append(t)
            us.append(u)
        hub[f"ext_{name}"] = tot
        hub[f"us_{name}"] = us

    def usbeta(res):
        d = dict((k, (b, s)) for k, b, s in res[0])
        b, s = d["us"]
        return b, b / s, res[2], res[3]

    print("US-demand pull on recovery duration, by timing of the partner-growth shift")
    print("(country-clustered t; controls: trade_open, program, depth_gap)\n")
    print(f"{'timing':10s} {'outcome':10s} {'US beta':>9s} {'t':>7s} {'n':>5s} {'clust':>6s}")
    cells = {}
    for name in windows:
        dd = hub.rename(columns={f"us_{name}": "us"})
        for outcome in ["t_full", "t_climb"]:
            res = ols(dd, outcome, ["us", "trade_open", "program", "depth_gap"])
            if res:
                b, t, n, g = usbeta(res)
                cells[(name, outcome)] = (b, t, n, g)
                print(f"{name:10s} {outcome:10s} {b:9.2f} {t:7.2f} {n:5d} {g:6d}")
        print()

    # ---- LaTeX table for the appendix ----
    lab = {"baseline": "Baseline: peak to peak$+2$",
           "onset": "Onset: crisis (peak) year only",
           "prewindow": "Pre-sample: peak$-5$ to peak$-1$"}

    def cell(name, outcome):
        if (name, outcome) not in cells:
            return ""
        b, t, n, g = cells[(name, outcome)]
        star = "***" if abs(t) > 2.58 else "**" if abs(t) > 1.96 else "*" if abs(t) > 1.64 else ""
        val = f"${b:.1f}^{{{star}}}$" if star else f"${b:.1f}$"
        return f"{val} {{\\scriptsize$({t:.1f})$}}"

    tex = [
        r"\begin{table}[H]", r"\centering\small",
        r"\caption{The US-demand effect by the timing of the partner-growth shift. The dependent "
        r"variable is recovery duration in months; each cell is the US-demand coefficient with its "
        r"country-clustered $t$-statistic. The onset measure uses only the crisis-year value of "
        r"partner growth, which substantially shortens the overlap with the recovery relative to the "
        r"baseline three-year window, though it is not strictly predetermined when a downturn begins "
        r"before the end of the calendar year; the pre-sample measure uses partner growth over the "
        r"five years before the downturn.}",
        r"\label{tab:prewindow}",
        r"\begin{tabularx}{\textwidth}{@{}lYY@{}}", r"\toprule",
        r"Timing of partner growth & Full cycle & Climb \\ \midrule",
    ]
    for name in ["baseline", "onset", "prewindow"]:
        tex.append(f"{lab[name]} & {cell(name,'t_full')} & {cell(name,'t_climb')} \\\\")
    tex += [
        r"\midrule",
        f"Episodes & {cells[('baseline','t_full')][2]} & {cells[('baseline','t_climb')][2]} \\\\",
        f"Clusters & {cells[('baseline','t_full')][3]} & {cells[('baseline','t_climb')][3]} \\\\",
        r"\bottomrule", r"\end{tabularx}",
        r"\\[2pt]\footnotesize{Weights are pre-crisis export shares throughout; only the years over "
        r"which partner growth is averaged differ. Controls: trade openness, an indicator for an "
        r"active IMF-supported arrangement, and shock depth. The US pull enters on its own here, "
        r"rather than alongside the other three partner pulls as in the horse race of "
        r"Table~\ref{tab:main}, so the baseline coefficient ($-5.3$) is close to but not identical to "
        r"the full-cycle coefficient there ($-5.6$). "
        r"$^{*}$, $^{**}$, $^{***}$: significance at 10, 5, 1 percent.}",
        r"\end{table}",
    ]
    with open(os.path.join(OUT, "tables_prewindow.tex"), "w", encoding="utf-8") as f:
        f.write("\n".join(tex) + "\n")
    print("saved output/tables_prewindow.tex")


if __name__ == "__main__":
    main()
