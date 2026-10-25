"""Recovery outcomes that do NOT depend on the HP zero-crossing (referee concern: short
crossings of zero mechanically mark 'recovery'; the same generated gap sets selection, depth,
and duration).

On the baseline episode sample we re-estimate the four-partner full-cycle decomposition on:
  - t_full        : baseline full negative cycle (peak -> gap returns to zero), for comparison;
  - t_full_p3/p6  : persistent return (gap must stay >=0 for 3 / 6 months), so a brief crossing
                    does not date a recovery;
  - cum_loss      : cumulative activity loss, the area of the negative gap over the spell, a
                    magnitude that has no crossing date at all.
Durations keep the shock-depth control (as in the headline); cumulative loss drops it because
depth is mechanically part of the area.
Run: python scripts/alt_recovery.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from build_horserace_hp import build_episodes, ols  # noqa: E402

OUT = os.path.join(os.path.dirname(__file__), "..", "output")
PARTNERS = ["us_pull", "otheradv_pull", "emer_pull", "china_pull", "trade_open"]
# (outcome column label, y, extra controls beyond the partner pulls)
OUTCOMES = [
    ("Full cycle",          "t_full",    ["depth_gap", "program"]),
    ("Persist. $k=3$",      "t_full_p3", ["depth_gap", "program"]),
    ("Persist. $k=6$",      "t_full_p6", ["depth_gap", "program"]),
    ("Cumulative loss",     "cum_loss",  ["program"]),
]
ROWLABEL = {"us_pull": "US demand", "otheradv_pull": "Other advanced",
            "emer_pull": "Emerging", "china_pull": "China", "trade_open": "Trade openness"}


def _cell(b, se):
    if se != se:
        return ""
    t = b / se if se else 0
    star = "***" if abs(t) > 2.58 else "**" if abs(t) > 1.96 else "*" if abs(t) > 1.64 else ""
    val = f"${b:.1f}^{{{star}}}$" if star else f"${b:.1f}$"
    return f"{val}{{\\scriptsize$({t:.1f})$}}"


def main():
    ep = build_episodes(one_sided=False, min_depth=2.0)
    results, agg, ns = {}, {}, {}
    for label, y, extra in OUTCOMES:
        # Panel A: total external demand (all partners together).
        ra = ols(ep, y, ["ext_demand"] + extra)
        agg[label] = ({name: (b, se) for name, b, se in ra[0]} if ra else {})
        # Panel B: the four-partner decomposition + trade openness.
        res = ols(ep, y, PARTNERS + extra)
        if not res:
            results[label] = {}; ns[label] = 0; continue
        coefs, r2, n, G = res
        results[label] = {name: (b, se) for name, b, se in coefs}
        ns[label] = n
        ea = agg[label].get("ext_demand", (float("nan"), float("nan")))
        et = ea[0] / ea[1] if ea[1] else 0
        print(f"\n{label} ({y}, n={n}, clusters={G}, R2={r2:.3f})  "
              f"ext_demand={ea[0]:.2f} (t={et:.2f})")
        for name in PARTNERS:
            b, se = results[label][name]
            t = b / se if se else 0
            star = "***" if abs(t) > 2.6 else "**" if abs(t) > 1.96 else "*" if abs(t) > 1.64 else ""
            print(f"  {name:14s} {b:8.2f} (t={t:5.2f}) {star}")

    # LaTeX: outcomes as columns, partner pulls as rows.
    cols = [lab for lab, _, _ in OUTCOMES]
    tex = [
        r"\begin{table}[H]", r"\centering\small",
        r"\caption{Recovery outcomes that do not depend on the HP zero-crossing. The full-cycle "
        r"column reproduces the main specification; the persistent-return columns date recovery "
        r"only once the output gap stays non-negative for three or six months, so a brief crossing "
        r"of zero cannot mark a recovery; the cumulative-loss column is the area of the negative gap "
        r"over the episode, a magnitude with no crossing date. Country-clustered $t$-statistics in "
        r"parentheses.}",
        r"\label{tab:altrecovery}",
        r"\begin{tabularx}{\textwidth}{@{}l" + "Y" * len(cols) + r"@{}}", r"\toprule",
        "Demand pull & " + " & ".join(cols) + r" \\ \midrule",
        r"\multicolumn{" + str(len(cols) + 1) + r"}{@{}l}{\emph{Panel A. All partners}} \\",
        "External demand & " + " & ".join(
            _cell(*agg[lab].get("ext_demand", (float("nan"), float("nan")))) for lab in cols)
        + r" \\ \midrule",
        r"\multicolumn{" + str(len(cols) + 1) + r"}{@{}l}{\emph{Panel B. By partner type}} \\",
    ]
    for name in PARTNERS:
        row = " & ".join(_cell(*results[lab].get(name, (float("nan"), float("nan"))))
                         for lab in cols)
        tex.append(f"{ROWLABEL[name]} & {row} " + r"\\")
    tex.append(r"\midrule")
    tex.append("Episodes & " + " & ".join(str(ns[lab]) for lab in cols) + r" \\")
    tex += [
        r"\bottomrule", r"\end{tabularx}",
        r"\\[2pt]\footnotesize{Emerging excludes China. Duration columns are in months and include "
        r"the shock-depth control and the active-arrangement indicator, as in "
        r"Table~\ref{tab:main}; the cumulative-loss column omits the depth control, which is "
        r"mechanically part of the area, and is in gap-percent-months. A negative coefficient means "
        r"a stronger demand pull is associated with a shorter cycle or a smaller cumulative loss. "
        r"$^{*}$, $^{**}$, $^{***}$: 10, 5, 1 percent.}",
        r"\end{table}",
    ]
    with open(os.path.join(OUT, "tables_altrecovery.tex"), "w", encoding="utf-8") as f:
        f.write("\n".join(tex) + "\n")
    print("\nsaved output/tables_altrecovery.tex")


if __name__ == "__main__":
    main()
