# Scripts — reproducible pipeline

All data pulls and analysis live here. Run from the project root (`ydist_paper/`).

| Script | What it does | Outputs (in `../data/`) |
|---|---|---|
| `imf_sdmx.py` | Shared helper for the IMF SDMX 3.0 API (api.imf.org). | — |
| `fetch_imts.py` | Monthly bilateral trade to China & World, all reporters, 2015+. Computes China trade shares. | `imts_raw_monthly_2015.parquet`, `imts_china_share_monthly.csv` |
| `fetch_weo.py` | Annual real GDP (level + growth) and nominal USD GDP, all countries. | `weo_realgdp_annual.csv` |
| `build_panel.py` | Step-1 panel: crisis episodes × recovery speed × pre-crisis trade openness. Also pulls annual trade-to-World 2000+ for openness. | `imts_world_annual.csv`, `step1_panel.csv` |
| `analyze_step1.py` | First-cut test: does pre-crisis openness predict faster recovery? Pooled vs idiosyncratic. | (stdout) |

Crisis dates: `../laeven_valencia_crisis_dates.csv` (≤2017 authoritative; 2018-25 reconstructed).

## Status of findings
- IMTS China-shift result: see `../connectedness_paper_status.md`.
- Step-1 first cut: naive pooled openness→recovery is null/wrong-signed (global 2008 cluster
  transmits the shock, per Rodrik); idiosyncratic-only flips to predicted sign (more-open
  recover ~1.2y faster) but weak (n=24). NOT yet confirmed — needs external-demand-from-
  healthy-partners measure + IMF (MONA) horse race + global-cycle netting.

## Data sources / API notes
- IMF SDMX 3.0 base: https://api.imf.org/external/sdmx/3.0 (legacy portal retired Nov 2025).
- Reporter wildcard in a data key must be `*`; multi-codes are `+`-joined.
- IMTS dims: COUNTRY.INDICATOR.COUNTERPART_COUNTRY.FREQUENCY; codes XG_FOB_USD, MG_CIF_USD,
  CHN, G001 (World), A/M. WEO dims: COUNTRY.INDICATOR.FREQUENCY; NGDP_R, NGDP_RPCH, NGDPD.
- Both IMTS trade and WEO NGDPD are in raw USD.
