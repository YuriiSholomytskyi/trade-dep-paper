"""Appendix tables: episode summary statistics and the sample country list.

Reads the episode panel (hub_panel.csv) and writes two LaTeX tables:
  output/appendix_summary.tex   -- summary statistics of the estimation sample
  output/appendix_countries.tex -- the sample economies, by hub, with episode counts
Run: python scripts/appendix_tables.py
"""
import os

import numpy as np
import pandas as pd

DATA = os.path.join(os.path.dirname(__file__), "..", "data")
OUT = os.path.join(os.path.dirname(__file__), "..", "output")


def main():
    hub = pd.read_csv(os.path.join(DATA, "hub_panel.csv"))

    # ---- summary statistics ----
    rows = [
        ("Depth of output gap (\\%)", "depth_gap"),
        ("Contraction, peak to trough (months)", "t_contraction"),
        ("Climb, trough to gap's return to zero (months)", "t_climb"),
        ("Full negative cycle (months)", "t_full"),
        ("External demand (shift-share, \\%)", "ext_demand"),
        ("US-demand pull (\\%)", "us_pull"),
        ("Trade openness (trade/GDP)", "trade_open"),
    ]
    lines = [
        r"\begin{table}[H]", r"\centering\small",
        rf"\caption{{Summary statistics for the estimation sample: {len(hub)} output-gap episodes "
        rf"across {hub.iso3.nunique()} economies, 2004--2024.}}", r"\label{tab:appsummary}",
        r"\begin{tabularx}{\textwidth}{@{}lYYYYY@{}}", r"\toprule",
        r"Variable & Mean & Median & Std.\ dev. & Min & Max \\ \midrule",
    ]
    for label, col in rows:
        s = pd.to_numeric(hub[col], errors="coerce").dropna()
        lines.append(f"{label} & {s.mean():.1f} & {s.median():.1f} & {s.std():.1f} & "
                     f"{s.min():.1f} & {s.max():.1f} \\\\")
    prog = pd.to_numeric(hub["program"], errors="coerce").dropna()
    lines += [
        r"\midrule",
        f"Episodes with an active IMF-supported arrangement & \\multicolumn{{5}}{{c}}{{"
        f"{int(prog.sum())} of {len(prog)} ({100*prog.mean():.0f}\\%)}} \\\\",
        r"\bottomrule", r"\end{tabularx}",
        r"\\[2pt]\footnotesize{Episodes are negative-output-gap spells reaching a depth of at least "
        r"two percent, dated from monthly activity with a Hodrick--Prescott filter. Durations are "
        r"censored at 60 months. External demand and the US-demand pull are the shift-share "
        r"measures of the text.}",
        r"\end{table}",
    ]
    with open(os.path.join(OUT, "appendix_summary.tex"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    # ---- country list by hub ----
    cty_hub = hub.groupby("iso3").hub.agg(lambda s: s.mode().iat[0])
    ep_n = hub.groupby("iso3").size()
    lab = {"US": "United States hub", "EU": "European Union hub", "CN": "China hub"}
    clines = [
        r"\begin{table}[H]", r"\centering\small",
        r"\caption{Sample economies by hub (the destination taking the largest share of exports), "
        r"with the number of downturn episodes.}", r"\label{tab:appcountries}",
        r"\begin{tabularx}{\textwidth}{@{}lX@{}}", r"\toprule",
        r"Hub & Economies (episodes) \\ \midrule",
    ]
    for h in ["US", "EU", "CN"]:
        isos = sorted(cty_hub[cty_hub == h].index)
        cells = ", ".join(f"{i} ({int(ep_n[i])})" for i in isos)
        clines.append(f"{lab[h]} & {cells} \\\\ \\addlinespace")
    clines += [
        r"\bottomrule", r"\end{tabularx}",
        r"\\[2pt]\footnotesize{Hub assignment is the trading partner, among the United States, the "
        r"European Union, and China, to which the economy directs the largest share of its exports. "
        r"Only one economy (Mongolia) is assigned to the China hub, so the China hub cannot be "
        r"estimated on the export side.}",
        r"\end{table}",
    ]
    with open(os.path.join(OUT, "appendix_countries.tex"), "w", encoding="utf-8") as f:
        f.write("\n".join(clines) + "\n")

    print("saved output/appendix_summary.tex and output/appendix_countries.tex")
    print(f"episodes={len(hub)}, countries={hub.iso3.nunique()}")


if __name__ == "__main__":
    main()
