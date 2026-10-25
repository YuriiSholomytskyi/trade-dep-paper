# Trade dependence and crisis recovery

What explains faster recovery from downturns: external demand from growing trading partners.

| Path | What it is |
|---|---|
| `paper/trade_recovery_revised.tex` / `.pdf` | Current paper |
| `output/` | Tables (`.tex`) and figures (`.png`) that the paper `\input`s / includes |
| `scripts/` | Data pulls and analysis; see `scripts/README.md` |
| `data/` | Panels and raw inputs used by the scripts |
| `docs/` | Status log (data recipes, findings) and review notes |
| `laeven_valencia_crisis_dates.csv` | Crisis dates read by the scripts |
| `MODELS_MODKEN_SNORK.md` | Instructions for accessing and running underlying models from `modken-snork` |
| `imf_seal_white.png` | Cover-page seal |

## Build

```
cd paper
pdflatex trade_recovery_revised.tex   # run twice
```

## Reproducing the tables and figures

Run scripts from the repo root. Haver access (`import Haver`) and the IMF SDMX API (`scripts/imf_sdmx.py`) are needed for the data pulls.
`scripts/seasonal_adjust.py` needs an X-13ARIMA-SEATS binary (not included).

Large regenerable files are git-ignored (`data/ctot_raw_monthly.csv`, `data/imts_bilateral_exports_annual.csv`,
`data/imts_china_share_monthly.csv`, `data/imts_raw_monthly_*.parquet`, `data/haver_codes/`). Re-create them with the
`fetch_*` / `build_*` / `discover_haver_activity.py` scripts, or remove those lines from `.gitignore` to track them.
