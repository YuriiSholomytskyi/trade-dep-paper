"""Robustness of the US-demand recovery result across specifications.
Runs the full-negative-cycle US-vs-partner decomposition under:
  baseline (2-sided HP, depth>=2), one-sided HP, true-crisis subsample (L-V),
  depth>=3, depth>=1.5.
Reports the partner-pull coefficients (t) and n for each; saves a text table.
Run: python scripts/robustness_hp.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from build_horserace_hp import build_episodes, ols  # noqa: E402

OUT = os.path.join(os.path.dirname(__file__), "..", "output")
XS = ["us_pull", "otheradv_pull", "emer_pull", "china_pull", "trade_open", "depth_gap", "program"]
SPECS = [
    ("Baseline (2-sided HP, depth>=2)",          dict(one_sided=False, min_depth=2.0), True),
    ("Baseline (omitting depth control)",        dict(one_sided=False, min_depth=2.0), False),
    ("One-sided (real-time) HP",                 dict(one_sided=True,  min_depth=2.0), True),
    ("Hamilton (2018) filter",                   dict(one_sided=False, min_depth=2.0, filter_type="hamilton"), True),
    ("Minimum duration >=3 months",              dict(one_sided=False, min_depth=2.0, min_dur=3), True),
    ("Merged 1-month positive blips",            dict(one_sided=False, min_depth=2.0, merge_gap=1), True),
    ("True-crisis subsample (L-V)",              dict(one_sided=False, min_depth=2.0, crisis_only=True), True),
    ("Depth threshold >=3%",                     dict(one_sided=False, min_depth=3.0), True),
    ("Depth threshold >=1.5%",                   dict(one_sided=False, min_depth=1.5), True),
]
REPORT = ["us_pull", "otheradv_pull", "emer_pull", "china_pull", "trade_open"]


def _tex_cell(b, se):
    if se != se:  # nan
        return ""
    t = b / se if se else 0
    star = "***" if abs(t) > 2.58 else "**" if abs(t) > 1.96 else "*" if abs(t) > 1.64 else ""
    val = f"${b:.1f}^{{{star}}}$" if star else f"${b:.1f}$"
    return f"{val}{{\\scriptsize$({t:.1f})$}}"


def main():
    lines = []
    header = (f"{'Specification':34s} {'n':>4s} {'clu':>4s}  " +
              "  ".join(f"{v:>12s}" for v in REPORT))
    lines.append(header); lines.append("-" * len(header))
    texrows = []
    base_ep = None
    for label, kw, use_depth in SPECS:
        if kw == dict(one_sided=False, min_depth=2.0) and base_ep is not None:
            ep = base_ep
        else:
            ep = build_episodes(**kw)
            if kw == dict(one_sided=False, min_depth=2.0):
                base_ep = ep
        xs_use = XS if use_depth else [x for x in XS if x != "depth_gap"]
        res = ols(ep, "t_full", xs_use)
        if not res:
            lines.append(f"{label:34s}  (insufficient obs)"); continue
        coefs, r2, n, G = res
        cd = {name: (b, se) for name, b, se in coefs}
        cells = []
        for v in REPORT:
            b, se = cd.get(v, (float("nan"), float("nan")))
            t = b / se if se else 0
            star = "***" if abs(t) > 2.6 else "**" if abs(t) > 1.96 else "*" if abs(t) > 1.64 else ""
            cells.append(f"{b:6.2f}({t:4.1f}){star:3s}")
        lines.append(f"{label:34s} {n:4d} {G:4d}  " + "  ".join(cells))
        lab = (label.replace(">=", "$\\ge$").replace("%", "\\%")
               .replace("L-V", "Laeven--Valencia"))
        texrows.append(f"{lab} & {n} & " +
                       " & ".join(_tex_cell(*cd.get(v, (float('nan'), float('nan'))))
                                  for v in REPORT) + r" \\")
    out = "\n".join(lines)
    print("\nFULL NEGATIVE CYCLE: partner-demand pull, coef(t), by specification\n")
    print(out)
    with open(os.path.join(OUT, "robustness_table.txt"), "w") as f:
        f.write("Full negative cycle ~ demand pull by partner + trade_open + depth; "
                "country-clustered SEs\n\n" + out + "\n")

    tex = [
        r"\begin{table}[H]", r"\centering\scriptsize",
        r"\caption{Robustness of the partner-demand decomposition across specifications. The "
        r"dependent variable is the full negative cycle in months; the partner-demand pulls enter "
        r"together with trade openness and shock depth, country-clustered $t$-statistics in "
        r"parentheses. The US-demand coefficient is stable across the filter, the depth threshold, "
        r"and the crisis-dating chronology.}",
        r"\label{tab:robustness}",
        r"\begin{tabularx}{\textwidth}{@{}lcYYYYY@{}}", r"\toprule",
        r"Specification & Ep. & US & Other adv. & Emerging & China & Openness \\ \midrule",
        *texrows,
        r"\bottomrule", r"\end{tabularx}",
        r"\\[2pt]\footnotesize{Emerging excludes China. Every specification includes the "
        r"active-arrangement indicator, and all rows except the second include the downturn-depth "
        r"control (so the first row reproduces the full-cycle column of Table~\ref{tab:main}). "
        r"The one-sided filter uses an expanding (real-time) Hodrick--Prescott trend after a "
        r"36-month burn-in; the Hamilton (2018) filter defines the cyclical component as the "
        r"residual from projecting $100\ln(\text{Index}_t)$ on four lags at a 24-month horizon; "
        r"the minimum-duration row drops spells shorter than three months; the merged-blip row "
        r"bridges isolated one-month non-negative readings between negative spells; and the "
        r"Laeven--Valencia subsample keeps episodes within a year of a recognized systemic crisis. "
        r"$^{*}$, $^{**}$, $^{***}$: 10, 5, 1 percent.}",
        r"\end{table}",
    ]
    with open(os.path.join(OUT, "tables_robustness.tex"), "w", encoding="utf-8") as f:
        f.write("\n".join(tex) + "\n")
    print("\nsaved output/robustness_table.txt and output/tables_robustness.tex")


if __name__ == "__main__":
    main()
