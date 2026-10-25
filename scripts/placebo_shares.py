"""Identification check: randomization inference on the exposure shares.

The US-demand pull is us_w * g_US, where us_w is the pre-crisis US export share and g_US is US
growth over the episode window. The concern is that the effect is identified off a handful of
US-exposed economies. This test asks whether the ACTUAL assignment of US exposure to economies is
special: we hold US growth fixed to each episode's window and randomly permute the us_w vector
across episodes, rebuild the pull, and re-estimate the full-cycle regression. If the true
coefficient lies in the tail of the permutation distribution, the effect comes from the real
exposure structure, not from which six countries happen to recover.

Output: prints the true coefficient, the permutation distribution, and a randomization p-value.
Run: python scripts/placebo_shares.py
"""
import os
import sys

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(__file__))
from build_horserace_hp import ols, DATA  # noqa: E402

OUT = os.path.join(os.path.dirname(__file__), "..", "output")

N_PERM = 2000
SEED_BASE = 12345  # fixed offsets; no RNG state that would break reproducibility


def main():
    hub = pd.read_csv(os.path.join(DATA, "hub_panel.csv")).reset_index(drop=True)
    weo = pd.read_csv(os.path.join(DATA, "weo_realgdp_annual.csv"))
    us = weo[weo.COUNTRY == "USA"].set_index("year")["ngdp_rpch"]

    # US growth over each episode's window [peak, peak+2], independent of the exposure weight
    def g_us(yr):
        return us.reindex(range(int(yr), int(yr) + 3)).mean()
    hub["g_us"] = hub.peak_year.map(g_us)
    hub = hub.dropna(subset=["g_us", "us_w", "t_full", "trade_open", "program", "depth_gap"]).copy()
    hub = hub.reset_index(drop=True)

    # rebuilt pull (should track the panel's us_pull closely)
    hub["us_pull_rebuilt"] = hub["us_w"] * hub["g_us"]
    ctrl = ["trade_open", "program", "depth_gap"]

    def beta(dd, col):
        res = ols(dd, "t_full", [col] + ctrl)
        d = dict((k, b) for k, b, s in res[0])
        return d[col]

    true_b = beta(hub.rename(columns={"us_pull_rebuilt": "x"}), "x")

    # permutation: shuffle the us_w vector across episodes, hold g_us (timing) fixed
    w = hub["us_w"].values
    g = hub["g_us"].values
    base = hub[["t_full", "iso3"] + ctrl].copy()
    perm_bs = []
    for k in range(N_PERM):
        # deterministic permutation from a fixed seed offset (reproducible, no global RNG)
        rng = np.random.default_rng(SEED_BASE + k)
        wp = rng.permutation(w)
        dd = base.copy()
        dd["x"] = wp * g
        try:
            perm_bs.append(beta(dd, "x"))
        except Exception:
            pass
    perm_bs = np.array(perm_bs)

    # one-sided p: fraction of placebos at least as negative as the true coefficient
    p_left = float((perm_bs <= true_b).mean())
    print(f"true US-demand coefficient (rebuilt pull): {true_b:.2f}")
    print(f"permutation mean {perm_bs.mean():.2f}, sd {perm_bs.std():.2f}, "
          f"5th/95th pct [{np.percentile(perm_bs,5):.2f}, {np.percentile(perm_bs,95):.2f}]")
    print(f"placebos at least as negative as true: {p_left:.4f}  (N={len(perm_bs)})")
    print(f"true coefficient is at the {100*p_left:.1f}th percentile of the placebo distribution")

    # ---- figure ----
    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    ax.hist(perm_bs, bins=40, color="0.7", edgecolor="white")
    ax.axvline(true_b, color="tab:red", lw=2,
               label=f"actual US exposure ({true_b:.1f})")
    ax.axvline(0, color="k", lw=0.8)
    ax.set_xlabel("US-demand coefficient on the full negative cycle (months)")
    ax.set_ylabel(f"placebo reassignments (of {len(perm_bs)})")
    ax.set_title("Randomization test: the true effect versus randomly reassigned US exposure")
    ax.legend(fontsize=9, loc="upper left")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "figure_placebo.png"), dpi=130)
    print("saved output/figure_placebo.png")


if __name__ == "__main__":
    main()
