"""Step-1 FIRST CUT: does pre-crisis trade openness predict faster recovery?

Sample: crisis episodes 2005+ that caused an actual output contraction
(output_loss_pct >= 1) and have non-censored recovery_time + pre-crisis openness.

Reports: openness above/below median -> mean recovery time & output loss;
plus simple OLS of recovery_time and output_loss on openness with controls.
Run: python scripts/analyze_step1.py
"""
import os

import numpy as np
import pandas as pd

DATA = os.path.join(os.path.dirname(__file__), "..", "data")


def main():
    p = pd.read_csv(os.path.join(DATA, "step1_panel.csv"))
    # one episode per country-year (collapse crisis types: take worst output loss)
    p = (p.sort_values("output_loss_pct", ascending=False)
           .drop_duplicates(["iso3", "start_year"]))
    s = p[(p.start_year >= 2005) & (p.output_loss_pct >= 1)
          & p.recovery_time.notna() & p.pre_openness.notna()].copy()
    print(f"Recession episodes (2005+, loss>=1%, recovered, openness known): {len(s)}")
    print(f"  median recovery_time={s.recovery_time.median():.1f}y  "
          f"median output_loss={s.output_loss_pct.median():.1f}%  "
          f"median openness={100*s.pre_openness.median():.0f}%")

    def split(sample, lbl):
        med = sample.pre_openness.median()
        hi, lo = sample[sample.pre_openness >= med], sample[sample.pre_openness < med]
        print(f"  {lbl:30s} n={len(sample):3d}  "
              f"MORE-open rec={hi.recovery_time.mean():.2f}y loss={hi.output_loss_pct.mean():.1f}%"
              f"  | LESS-open rec={lo.recovery_time.mean():.2f}y loss={lo.output_loss_pct.mean():.1f}%")

    # KEY: pooled vs idiosyncratic (global shocks transmit the crisis -> must exclude/condition)
    GLOBAL = {2008, 2009, 2020}
    print("\nOpenness split (above/below median pre-crisis trade/GDP):")
    split(s, "ALL crises")
    idio = s[~s.start_year.isin(GLOBAL)]
    split(idio, "IDIOSYNCRATIC (excl 08/09/20)")
    print(f"  -> idiosyncratic corr(openness, recovery_time)="
          f"{idio.pre_openness.corr(idio.recovery_time):.3f} (negative = more-open recover faster)")

    # simple OLS with numpy (recovery_time ~ openness + output_loss)
    for yname in ["recovery_time", "output_loss_pct"]:
        d = s.dropna(subset=[yname, "pre_openness"])
        X = np.column_stack([np.ones(len(d)), d.pre_openness.values,
                             d.output_loss_pct.values if yname == "recovery_time"
                             else d.start_year.values])
        y = d[yname].values
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
        yhat = X @ beta
        ss_res = ((y - yhat) ** 2).sum(); ss_tot = ((y - y.mean()) ** 2).sum()
        r2 = 1 - ss_res / ss_tot
        ctrl = "output_loss" if yname == "recovery_time" else "start_year"
        print(f"\nOLS {yname} = {beta[0]:.2f} + ({beta[1]:.2f})*openness "
              f"+ ({beta[2]:.4f})*{ctrl}   R2={r2:.3f}  n={len(d)}")
        print("    (openness in 0-1 share; negative coef on recovery_time = faster recovery)")

    # show the recession episodes
    cols = ["iso3", "country", "crisis_type", "start_year", "output_loss_pct",
            "recovery_time", "pre_openness"]
    print("\n", s.sort_values("pre_openness")[cols].to_string(index=False))


if __name__ == "__main__":
    main()
