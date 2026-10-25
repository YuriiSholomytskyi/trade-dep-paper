"""Generate LaTeX result tables from the horse-race regressions, so the paper's numbers are
exact and reproducible. Writes output/tables.tex (\\input into the paper).
Run: python scripts/make_tables.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from build_horserace_hp import build_episodes, ols  # noqa: E402

OUT = os.path.join(os.path.dirname(__file__), "..", "output")
LBL = {"us_pull": "US demand", "otheradv_pull": "Other advanced demand",
       "emer_pull": "Emerging demand (excl.\\ China)", "china_pull": "China demand",
       "china_pull_comm": "China demand $\\times$ commodity exporter",
       "china_pull_noncomm": "China demand $\\times$ non-commodity",
       "trade_open": "Trade openness", "fin_open": "Financial openness",
       "partner_vol": "Partner volatility",
       "program": "IMF programme", "prog_fx": "Programme, exchange-rate focus",
       "prog_nofx": "Programme, no exchange-rate focus", "depth_gap": "Depth of downturn",
       "commodity": "Commodity exporter", "const": "Constant"}


def cell(b, se):
    t = b / se if se else 0
    star = "^{***}" if abs(t) > 2.6 else "^{**}" if abs(t) > 1.96 else "^{*}" if abs(t) > 1.64 else ""
    return f"${b:.2f}{star}$ {{\\scriptsize$({t:.1f})$}}"


def col(ep, y, xs):
    res = ols(ep, y, xs)
    coefs, r2, n, G = res
    d = {name: (b, se) for name, b, se in coefs}
    return d, r2, n, G


def table(ep, outcomes, rows, caption, label, note=""):
    cols = [col(ep, y, xs) for _, y, xs in outcomes]
    s = ["\\begin{table}[t]", "\\centering", "\\small",
         f"\\caption{{{caption}}}", f"\\label{{{label}}}",
         "\\begin{tabular}{l" + "c" * len(outcomes) + "}", "\\toprule",
         " & " + " & ".join(f"{h}" for h, _, _ in outcomes) + " \\\\", "\\midrule"]
    for r in rows:
        cells = []
        for d, _, _, _ in cols:
            if r in d:
                b, se = d[r]; cells.append(cell(b, se))
            else:
                cells.append("")
        s.append(f"{LBL.get(r, r)} & " + " & ".join(cells) + " \\\\")
    s.append("\\midrule")
    s.append("Episodes & " + " & ".join(str(c[2]) for c in cols) + " \\\\")
    s.append("Countries & " + " & ".join(str(c[3]) for c in cols) + " \\\\")
    s.append("\\bottomrule\\end{tabular}")
    if note:
        s.append(f"\\\\[2pt]\\footnotesize{{{note}}}")
    s.append("\\end{table}")
    return "\n".join(s)


def main():
    ep = build_episodes()
    parts = ["us_pull", "otheradv_pull", "emer_pull", "china_pull"]

    t1 = table(
        ep,
        [("Depth", "depth_gap", parts + ["trade_open", "partner_vol", "program"]),
         ("Contraction", "t_contraction", parts + ["trade_open", "depth_gap", "program"]),
         ("Climb", "t_climb", parts + ["trade_open", "depth_gap", "program"]),
         ("Full cycle", "t_full", parts + ["trade_open", "depth_gap", "program"])],
        parts + ["trade_open", "partner_vol", "depth_gap"],
        "External demand and the output cycle, by partner type. Output-gap episodes, "
        "country-clustered standard errors ($t$ in parentheses).",
        "tab:main",
        "Depth in percent; durations in months. Contraction is peak (start of the negative-gap "
        "spell) to trough (minimum gap), climb is trough to the output gap's return to zero, full "
        "cycle is peak to the output gap's return to zero. All columns also track "
        "official support with an indicator for an active IMF-supported arrangement (MONA), so "
        "the demand effects are estimated conditional on whether an arrangement is in place. "
        "$^{*},^{**},^{***}$: significant at 10, 5, 1 percent.")

    ep["comm_note"] = ep.commodity
    t2 = table(
        ep,
        [("Depth of downturn", "depth_gap",
          ["china_pull_comm", "china_pull_noncomm", "commodity", "emer_pull",
           "otheradv_pull", "us_pull", "trade_open", "program"])],
        ["china_pull_comm", "china_pull_noncomm", "commodity", "emer_pull",
         "otheradv_pull", "us_pull", "trade_open"],
        "The China-depth association is commodity-exporter composition.",
        "tab:china",
        "China demand interacted with a commodity-exporter indicator. The effect is present "
        "only among commodity exporters. The regression also tracks an indicator for an active "
        "IMF-supported arrangement.")

    with open(os.path.join(OUT, "tables.tex"), "w") as f:
        f.write("\n\n".join([t1, t2]) + "\n")
    print("wrote output/tables.tex")
    print(f"episodes={len(ep)} countries={ep.iso3.nunique()}")


if __name__ == "__main__":
    main()
