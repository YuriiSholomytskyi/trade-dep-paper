"""Recovery as a censored time-to-event outcome (referee Section IV, must-fix #9).

The linear duration regressions treat the full negative cycle as a continuous outcome and set
non-recovering spells to the 60-month cap. This script re-does the analysis with methods built for
censored durations, so the estimate does not depend on that top-coding:

  1. Kaplan-Meier recovery curves (probability the output gap has returned to zero by month t),
     split at the median US-demand pull, with a log-rank test of equality.
  2. A discrete-time proportional-hazards model: the monthly recovery hazard is fit with a
     complementary-log-log link on the episode/month panel, a smooth baseline hazard (cubic in
     the month), and country-clustered standard errors. The coefficient on the US pull is a log
     hazard ratio; a positive value means US-exposed downturns exit faster, the hazard-model
     counterpart of the negative coefficient in the linear duration regression.

Recovery is the event (output gap returns to zero); spells that never return within the 60-month
window are right-censored. Output: prints the numbers, writes output/tables_survival.tex
(label tab:survival) and output/km_recovery.png (Figure~\\ref{fig:km}).
Run: python scripts/survival_recovery.py
"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import statsmodels.api as sm  # noqa: E402

sys.path.insert(0, os.path.dirname(__file__))
from build_horserace_hp import CENSOR, build_episodes  # noqa: E402

OUT = os.path.join(os.path.dirname(__file__), "..", "output")
XS = ["us_pull", "otheradv_pull", "emer_pull", "china_pull", "trade_open", "depth_gap", "program"]


def km_curve(dur, ev):
    """Kaplan-Meier estimate of S(t)=Pr(still in downturn at t); returns (times, S)."""
    dur = np.asarray(dur, float)
    ev = np.asarray(ev, float)
    times = np.array(sorted(set(dur[ev == 1])))
    S, s = [], 1.0
    for t in times:
        at_risk = (dur >= t).sum()
        d = ((dur == t) & (ev == 1)).sum()
        s *= (1 - d / at_risk) if at_risk else 1.0
        S.append(s)
    return times, np.array(S)


def km_median(times, S):
    """First month at which recovery probability 1-S reaches one half."""
    below = np.where(S <= 0.5)[0]
    return float(times[below[0]]) if len(below) else np.nan


def logrank(dur, ev, grp):
    """Two-group log-rank chi-square (1 df) and p-value."""
    dur = np.asarray(dur, float)
    ev = np.asarray(ev, float)
    grp = np.asarray(grp)
    event_times = np.array(sorted(set(dur[ev == 1])))
    O1 = E1 = V = 0.0
    for t in event_times:
        at_risk = dur >= t
        n = at_risk.sum()
        d = ((dur == t) & (ev == 1)).sum()
        n1 = (at_risk & (grp == 1)).sum()
        d1 = ((dur == t) & (ev == 1) & (grp == 1)).sum()
        O1 += d1
        E1 += d * n1 / n
        if n > 1:
            V += d * (n1 / n) * (1 - n1 / n) * (n - d) / (n - 1)
    chi2 = (O1 - E1) ** 2 / V if V else np.nan
    from scipy import stats
    return chi2, float(stats.chi2.sf(chi2, 1)), O1, E1


def person_period(ep, dur_col="t_full"):
    """Expand each episode to one row per at-risk month; y=1 in the recovery month."""
    rows = []
    for _, r in ep.iterrows():
        T = max(1, int(round(r[dur_col])))
        recovered = r[dur_col] < CENSOR
        for m in range(1, T + 1):
            y = 1 if (recovered and m == T) else 0
            rows.append({"iso3": r.iso3, "month": m, "y": y,
                         **{x: r[x] for x in XS}})
    return pd.DataFrame(rows)


def fit_cloglog(pp, covs):
    pp = pp.copy()
    pp["m1"] = pp.month
    pp["m2"] = pp.month ** 2
    pp["m3"] = pp.month ** 3
    cols = covs + ["m1", "m2", "m3"]
    X = sm.add_constant(pp[cols].astype(float))
    model = sm.GLM(pp.y.astype(float), X,
                   family=sm.families.Binomial(link=sm.families.links.CLogLog()))
    return model.fit(cov_type="cluster", cov_kwds={"groups": pp.iso3.values})


def main():
    hp_path = os.path.join(os.path.dirname(__file__), "..", "data", "horserace_hp.csv")
    ep = (pd.read_csv(hp_path) if os.path.exists(hp_path) else build_episodes())
    ep = ep.dropna(subset=["t_full", "t_climb"] + XS + ["iso3"]).copy()
    n = len(ep)
    ep["event"] = (ep.t_full < CENSOR).astype(int)
    cens = int((ep.event == 0).sum())
    print(f"episodes={n}  right-censored (never returned to trend within {CENSOR} mo): "
          f"{cens} ({100*cens/n:.1f}%)")

    # ---- 1. Kaplan-Meier by US-exposure group (split at the median US pull) ----
    med = ep.us_pull.median()
    ep["hi_us"] = (ep.us_pull > med).astype(int)
    thi, Shi = km_curve(ep.loc[ep.hi_us == 1, "t_full"], ep.loc[ep.hi_us == 1, "event"])
    tlo, Slo = km_curve(ep.loc[ep.hi_us == 0, "t_full"], ep.loc[ep.hi_us == 0, "event"])
    mhi, mlo = km_median(thi, Shi), km_median(tlo, Slo)
    chi2, p_lr, O1, E1 = logrank(ep.t_full, ep.event, ep.hi_us)
    print(f"KM median recovery: high-US {mhi:.0f} mo vs low-US {mlo:.0f} mo")
    print(f"log-rank chi2(1)={chi2:.2f}  p={p_lr:.3f}")

    plt.figure(figsize=(6.2, 4.0))
    for t, S, lab, style in [(thi, Shi, f"High US exposure (median recovery {mhi:.0f} mo)", "-"),
                             (tlo, Slo, f"Low US exposure (median recovery {mlo:.0f} mo)", "--")]:
        t = np.concatenate([[0], t])
        rec = 1 - np.concatenate([[1.0], S])       # cumulative recovery probability
        plt.step(t, rec, where="post", linestyle=style, linewidth=1.8, label=lab)
    plt.xlabel("Months since peak")
    plt.ylabel("Probability output gap has returned to zero")
    plt.ylim(0, 1)
    plt.xlim(0, CENSOR)
    plt.legend(frameon=False, fontsize=9, loc="lower right")
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, "km_recovery.png"), dpi=200)
    plt.close()
    print("saved output/km_recovery.png")

    # ---- 2. Discrete-time proportional-hazards models (cloglog), clustered by country ----
    pp_full = person_period(ep, "t_full")
    pp_climb = person_period(ep, "t_climb")
    xs_nodepth = [c for c in XS if c != "depth_gap"]

    res = fit_cloglog(pp_full, XS)
    res_nodepth = fit_cloglog(pp_full, xs_nodepth)
    res_climb = fit_cloglog(pp_climb, XS)

    print("\nDiscrete-time hazard (cloglog), country-clustered; coef = log hazard ratio")
    for tag, r, covs in [("Full cycle (with depth)", res, XS),
                         ("Full cycle (no depth)", res_nodepth, xs_nodepth),
                         ("Climb phase (from trough)", res_climb, XS)]:
        print(f"--- {tag} ---")
        for c in covs:
            b, z, pv = r.params[c], r.tvalues[c], r.pvalues[c]
            print(f"  {c:14s} coef={b:7.3f}  HR={np.exp(b):5.2f}  z={z:5.2f}  p={pv:.3f}")

    # ---- LaTeX table ----
    lab = {"us_pull": "US demand", "otheradv_pull": "Other advanced demand",
           "emer_pull": "Emerging demand (excl.\\ China)", "china_pull": "China demand",
           "trade_open": "Trade openness", "depth_gap": "Depth of downturn",
           "program": "Active IMF arrangement"}

    def hcell(r, c):
        if c not in r.params:
            return ""
        b, z = r.params[c], r.tvalues[c]
        star = f"^{{{'***' if abs(z) > 2.58 else '**' if abs(z) > 1.96 else '*' if abs(z) > 1.64 else ''}}}"
        if star == "^{}":
            star = ""
        return f"${np.exp(b):.2f}$ / ${b:.2f}{star}$ {{\\scriptsize$({z:.1f})$}}"

    trows = []
    for c in XS:
        trows.append(f"{lab[c]} & {hcell(res, c)} & {hcell(res_nodepth, c)} & {hcell(res_climb, c)} \\\\")
    tex = [
        r"\begin{table}[H]", r"\centering\small",
        r"\caption{Recovery as a censored time-to-event outcome. The event is the return of the "
        r"output gap to zero; spells that do not return within " + str(CENSOR) + r" months are "
        r"right-censored (" + f"{cens}" + r" of " + f"{n}" + r" episodes, "
        f"{100*cens/n:.0f}" + r"\%). Estimates are from discrete-time proportional-hazards models "
        r"with a complementary-log-log link, a cubic baseline hazard in the month, and "
        r"country-clustered standard errors. Each cell reports $\text{HR} \;/\; \log(\text{HR})$ with "
        r"the clustered $z$-statistic in parentheses. Column 1 models the full negative cycle from the "
        r"peak with baseline controls; column 2 omits the post-onset downturn depth control; column 3 "
        r"starts the risk clock at the episode trough (modeling the post-trough climb phase).}",
        r"\label{tab:survival}",
        r"\begin{tabularx}{\textwidth}{@{}lYYY@{}}", r"\toprule",
        r"Covariate & (1) Full cycle & (2) Full cycle (no depth) & (3) Climb from trough \\ \midrule",
        *trows,
        r"\midrule",
        f"Episodes & {n} ({ep.iso3.nunique()} countries) & {n} ({ep.iso3.nunique()} countries) & {n} ({ep.iso3.nunique()} countries) \\\\",
        f"Episode-months at risk & {len(pp_full)} & {len(pp_full)} & {len(pp_climb)} \\\\",
        r"\bottomrule", r"\end{tabularx}",
        r"\\[2pt]\footnotesize{Hazard ratios are $\exp(\text{coef})$; a value above one raises the "
        r"probability of returning to trend in a given month. The baseline-hazard terms (cubic in "
        r"the month) are included in all columns. $z$-statistics use country-clustered standard "
        r"errors. $^{*}$, $^{**}$, $^{***}$: significance at 10, 5, 1 percent.}",
        r"\end{table}",
    ]
    with open(os.path.join(OUT, "tables_survival.tex"), "w", encoding="utf-8") as f:
        f.write("\n".join(tex) + "\n")
    print("saved output/tables_survival.tex")

    # numbers the paper text cites
    print(f"\nfor text: censored {cens}/{n} ({100*cens/n:.0f}%); "
          f"US HR={np.exp(res.params['us_pull']):.2f} (z={res.tvalues['us_pull']:.1f}); "
          f"log-rank p={p_lr:.3f}; KM median hi/lo = {mhi:.0f}/{mlo:.0f} mo")


if __name__ == "__main__":
    main()
