# Paper idea: Integration as the crisis-recovery mechanism — working status

_Snapshot of brainstorming session, 2026-06-30. Resume from "Next step" at the bottom._

## The converged thesis

**Integration is itself the recovery mechanism.** A country embedded in the global
economy keeps its link through a crisis — visible in the data, the link never breaks —
and that surviving link is what drags it out. IMF programs / reforms are second-order.
For a *closed* economy there is no link to do the dragging, so no amount of money or
conditionality helps.

This subsumes (and is stronger than) the narrower IMF-effectiveness question: the IMF
horse race is just one corollary of the bigger claim that **openness, not policy, is the
binding determinant of crisis recovery.**

## How we got here (thesis evolution)

1. Started: "did the global economy become more connected" (descriptive, crowded).
2. → mechanisms: inflation-targeting diffusion; rich-economy demand lifting poor.
3. → core→periphery transmission: stable US/EU/China export stability to the periphery
   (not symmetric — hierarchical). 2021-22 supports this: core lost control → periphery
   got inflation too; EM CBs hiked ahead of the Fed because they import inflation.
4. → causal crux: in a crisis, what stabilizes — IMF program/reforms or ambient global
   gravity?
5. → final: the **link itself** is the lifeline. Openness > policy. Closed economies
   can't be helped because they have no transmission channel.

## Refinement that makes it credible: WHICH link survives

"The link never breaks" must be specific:
- **Capital flows flee** in a crisis (sudden stop — Calvo; Rey's global financial cycle).
- **Trade, FDI, remittances are sticky** and become the actual lifeline.
  - Trade: real depreciation + open trade → export-led "Phoenix miracle"
    (Calvo–Izquierdo–Talvi: recoveries run through tradables, not credit).
  - Remittances: countercyclical, resilient (Yang; Ratha).
  - FDI: stickier than portfolio capital.

Data story: fickle link (portfolio capital) breaks; resilient links (trade/FDI/remittances)
hold; resilient links pull the country out.

## Identification strategy

- **Killer test — program × openness interaction.** Hypothesis: program coefficient ≈ 0
  for low-integration economies, positive only where openness is already high. The program
  greases an existing channel; it cannot create one.
- **Link-persistence measure.** How much of pre-crisis trade/FDI/remittance link survived
  the crisis; does recovery speed rise with surviving-link strength?
- **Method.** Synthetic control (Abadie) per crisis episode; the synthetic control already
  embeds the global tailwind, so the residual is the true program/own-effort effect.

## Two threats to pre-empt

1. **Openness cuts both ways** (Rodrik 1998: open economies face bigger shocks). Must show
   the *recovery-leg* advantage *conditional on* the shock size, else the net-welfare critic
   wins.
2. **Closedness is endogenous to bad institutions** (Venezuela, Argentina ISI, sanctioned
   states are closed *because* of politics). Isolate with *within-open-economy* variation in
   link persistence, not the open/closed dummy.

## Literature map

- **Factor models of synchronization:** Kose–Otrok–Whiteman (AER 2003);
  Kose–Otrok–Prasad (2012); Ciccarelli–Mojon "Global Inflation" (REStat 2010).
- **Connectedness/spillover networks:** Diebold–Yilmaz (2009/2012/2014).
- **Economic complexity (borrow the network method, not the index):** Hidalgo–Hausmann;
  Neffke–Hausmann skill relatedness / labor-flow networks (for any labor angle).
- **Core→periphery transmission:** Rey "Dilemma not Trilemma" (2013, global financial
  cycle); Gopinath "Dominant Currency Paradigm" (dollar invoicing); pass-through lit
  (Carrière-Swallow et al.).
- **EM inflation / closest prior:** Ha–Kose–Ohnsorge (2019) *Inflation in EMDEs* —
  but pre-COVID/pre-2021, can't speak to anchor robustness under stress.
- **IMF program effectiveness:** Przeworski–Vreeland (2000, programs → slower growth,
  selection); Barro–Lee (2005, political timing); Bird–Rowlands (catalytic finance weak).
- **Auto-correction / recovery:** Calvo–Izquierdo–Talvi "Phoenix miracles" (V-shaped
  recoveries without credit); Baldwin "Great Trade Collapse" (2009).

## Sample window: 2005+ (locked)

Forward-focused paper; nothing before 2005. Consistent MONA regime (post-2002
conditionality reforms bedded in → uniform reporting). Crisis waves covered: GFC 2008-09,
Euro periphery 2010-12, taper/EM 2013-15, COVID 2020 (RFI/RCF surge ~80+ arrangements),
2022 tightening/food-energy. ~200+ arrangements, 5 distinct shocks → enough power for the
program × pre-crisis-openness interaction. No historical supplements (drop Dreher/IMF
pre-1993).

## Forward framing: the link never breaks — it SHIFTS EAST (to China/East Asia)

NOTE: fragmentation framing REJECTED. Author's view: there is no fragmentation/deglobalization;
connectedness is robust. What's happening is a SHIFT of the anchor's center of gravity from
US/EU toward China and East Asian economies. Links persist; their destination reorients East.
(Consistent with "the link never breaks, I see it in the data" — and with rerouting via
connector economies, trade/GDP near highs, remittances at records.)

KILLER FACT: China is now not just the demand anchor but the CRISIS LENDER, displacing the IMF.
- Horn, Reinhart & Trebesch, "China's Overseas Lending" (JIE 2021) and "China as an
  International Lender of Last Resort" (2023): ~$240bn+ bilateral bailouts (Argentina,
  Pakistan, Sri Lanka...), rivaling IMF scale. PBoC bilateral swap lines (McDowell) = parallel
  liquidity backstop.

UPGRADED HORSE RACE (competitors for crisis-recovery speed):
- IMF program (Western multilateral + conditionality) — DATA: MONA
- Link to China/East (trade share, commodity demand, China FDI) — DATA: IMF DOTS, BOP
- China rescue lending / swap lines (LOLR) — DATA: Horn-Reinhart-Trebesch + PBoC swaps
- Pre-crisis openness, general (predetermined moderator) — DATA: Lane-Milesi-Ferretti stocks

TESTABLE CLAIM: over 2005-2024, recovery speed loads increasingly on CHINA-linkage, not the
West/IMF; China bilateral rescue substitutes for — possibly outperforms — IMF programs for
China-connected economies; closed-economy losers are plugged into NEITHER pole.

OPEN GROUND: IMF-effectiveness lit ignores China-as-rival-lender; China-lending lit (Horn et
al.) hasn't run a recovery HORSE RACE vs IMF using MONA. The intersection (MONA ×
Horn-Reinhart-Trebesch, China-linkage as rising moderator) is the contribution.
TODO once lit search lands: confirm nobody has done MONA-vs-China-rescue recovery horse race.

## Data

- **MONA (IMF Monitoring of Fund Arrangements) — IN HAND, full database.** This is the
  treatment backbone. Upgrades the design from a program dummy to rich treatment:
  - Intensity/dose: amount approved & *drawn* relative to quota → dose-response.
  - Compliance/interruptions: reviews completed vs delayed/missed, waivers, interruptions
    → separate "program signed" from "program implemented." Horse race may really be:
    *completed* programs help only where openness is high.
  - Conditionality content: quantitative perf criteria vs structural benchmarks vs prior
    actions. Coverage: modern MONA ~2002+ → spans GFC, EU debt crisis, COVID, 2022
    (the recent window Ha-Kose-Ohnsorge couldn't reach).
  - **TRAP:** MONA conditionality often includes trade/capital-account liberalization, so
    a program can *cause* openness → openness becomes a MEDIATOR, not a rival, contaminating
    a naive horse race. FIX: use **pre-crisis openness STOCK (predetermined)** as the
    moderator (Lane–Milesi-Ferretti External Wealth of Nations stocks; pre-crisis
    trade/remittance ratios). Route 2 (extension): embrace mediation — "IMF works when it
    opens you, not when it disciplines you" — but that's a different paper; don't blur.

- Pair MONA with:
  - Outcomes (recovery speed, growth rebound, output gap): WEO / Haver / WDI.
  - Crisis dating: Laeven–Valencia; Reinhart–Rogoff.
  - Integration/link measures: IMF BOP (trade, FDI, remittances, portfolio flows);
    Lane–Milesi-Ferretti for stocks.
  - Link-persistence (Design 2): high-frequency BOP/flow data around crisis date
    (portfolio flows flee vs trade/FDI/remittances stay).
- Also: Haver Analytics for broad cross-domain series.

## Framing / hook

Crisis-first intro (house style): show a country knocked down, the trade/remittance link
holding flat through the trough in the data, then climbing back up that same wire — while
the closed comparator just lies there.

## LIT-GAP VERDICT (deep-research, completed) — CONTRIBUTION IS OPEN

The horse race (integration vs IMF as competing determinants of crisis-RECOVERY SPEED)
does NOT yet exist. Sub-designs:
- D1 program × openness interaction: **OPEN**. Binder-Bluhm (2017, JMacro), Busse-Vogel
  (2024, Kyklos) get close; nobody interacts program recovery effect with trade/fin openness.
- D2 surviving-link strength → recovery speed: **PARTIALLY CLAIMED**. Sticky-trade/FDI vs
  fickle-capital premise established (Eichengreen-Gupta-Masetti 2018; Calvo-Izquierdo-Talvi
  Phoenix Miracles 2006; Bems-Johnson-Yi 2013) but nobody tests surviving-link → recovery.
- D3 synthetic control netting out global financial cycle: **PARTIALLY CLAIMED**, residual
  leg OPEN (Kuruc 2022 JME; Essers-Ide 2019; Newiak-Willems 2017; Bouvet-Bower-Jones 2022).
- D4 recovery leg conditional on being hit: **most CLAIMED** — Eichengreen-Park-Shin (2024),
  Aizenman et al (2025): **trade openness helps resilience, financial openness HURTS** →
  directly vindicates sticky-link-good / fickle-capital-bad split.
CLEANEST CONTRIBUTION = unified horse race D1+D3: program recovery effect varies with trade
openness / surviving-link strength (tilted toward China), global cycle purged.

## CORE EMPIRICAL STORY (crystallized) + contemporary data (verified June 2026)

SHOW: countries' trade is shifting to CHINA; links didn't break (no fragmentation), they
swung East — and that is WHY crisis recoveries kept working. Stability propagates from the
anchor: connected countries inherit the anchor's stable growth + anchored inflation; China
is now the anchor.

Figure-1 facts (sources in agent outputs):
- China = top trade partner for 60 economies vs 33 US (2023, Lowy/IMF DOTS); ~70% of
  economies trade more with China than US.
- 2024 records: China-ASEAN ~$990bn, China-LatAm $518bn, China-Africa $296bn; BRI partners
  >50% of China total trade.
- China share of US imports 22% (2017) → 13.4% (2024) = reorientation not contraction.
- Global trade at RECORD ($35tn 2025, UNCTAD; WTO volume +4.5%); trade/GDP 56.6% vs 62.8%
  peak. NO deglobalization. DHL: connectedness at record high. Gopinath concedes no
  aggregate deglobalization. WTO calls it "reglobalization." => fragmentation story was a
  POLICY WEAPON aimed at US admin, not a finding. Paper = contrarian-with-evidence.
- China as crisis LENDER rivaling IMF on flow basis: 2024-25 PBoC-style swaps $269bn issued/
  renewed vs IMF $36bn new lending (BU GDP Center). Cumulative China rescue ~$240-250bn
  (Horn-Parks-Reinhart-Trebesch). China net flows to developing world turned NEGATIVE
  -$34bn in 2024 (Lowy "Peak Repayment") — boom→repayment phase.
- Country cases (2024-26): IMF rarely did the FINANCIAL heavy lifting (smallest money pool);
  its leverage = conditionality, esp. forcing FX float. Cash came from bilateral patrons
  (Gulf=Egypt $35bn Ras El-Hekma; China/Gulf=Pakistan ~$12bn deposits; US/China=Argentina)
  and from OWN links (remittances: Pakistan $38bn, Bangladesh $33bn; commodities: Zambia
  copper, Ghana gold, Ethiopia coffee). China two-faced: balance-sheet lifeline (swaps/
  deposits) AND slow comparability-obsessed restructuring gatekeeper (Zambia, Ethiopia).

## DATA DECISION

- Trade-shift core (Figure 1, China share by country over time): **IMF DOTS — renamed IMTS,
  new portal `IMF.STA:IMTS`, free SDMX API.** OLD data.imf.org/DOT API DEAD since Nov 2025.
  Haver = paid repackaging of same national data; use only for HF series DOTS lacks.
- Other sources current (June 2026): MONA on new data.imf.org (legacy froze Aug 2025);
  Laeven-Valencia NEW "Systemic Banking Crises 1970-2025" (IMF WP 2026/094); AidData "China's
  Global Loans and Grants v1.0" (Nov 2025, supersedes GCDF 3.0) + "China as Intl Lender of
  Last Resort v1.0.1" (swaps+rescue, frozen at 2021); Lane-Milesi-Ferretti EWN now through
  year-end 2024; KNOMAD remittances wound down (last Brief 40, Jun 2024; bilateral matrix
  stale at 2021); WEO Apr 2026; WDI Apr 2026.

## IMTS DATA PULLED + HEADLINE RESULT (the punchline)

API recipe (WORKS): base https://api.imf.org/external/sdmx/3.0 ; dataflow IMF.STA/IMTS/+ ;
DSD_IMTS_VINTAGE ; dims COUNTRY.INDICATOR.COUNTERPART_COUNTRY.FREQUENCY ; codes
XG_FOB_USD (exports), MG_CIF_USD (imports), CHN, G001=World, A/M. Wildcard reporter = '*'
(empty string returns nothing). Combined key works:
  *.XG_FOB_USD+MG_CIF_USD.CHN+G001.M?startPeriod=2015-01&format=sdmx-csv
Monthly data runs to 2026-M02. Saved: data/imts_raw_monthly_2015.parquet (489k rows, 237
reporters) and data/imts_china_share_monthly.csv (wide + exp_share_chn/imp_share_chn).
Use trailing-12m sums (min_periods=12) to kill seasonality before computing shares.

HEADLINE (trailing-12m, 2021-12 -> 2026-02, 188 countries w/ both endpoints):
- 74% of countries RAISED import share from China (median +2.15pp). Only 39% raised export
  share to China (median -0.25pp). => shift is an IMPORT shift; selling TO China flat
  (China demand stalled).
- US is the LONE DECOUPLER: import share from China 17.8%->8.3%, export 8.6%->4.6%
  (2025 tariff wave). Everyone else RE-COUPLED: Vietnam 34->43, Ethiopia 26->42, Saudi
  20->28, Indonesia 29->33, Zambia 13->22, Brazil 22->25, S.Africa 21->23, etc.
- INTERPRETATION = the paper: fragmentation describes WASHINGTON'S trade, not the world's.
  US talked fragmentation and got it; rest of world integrated HARDER with China. Import-side
  deepening = importing CHINA'S DISINFLATION (China as cheap supplier exporting price
  stability) -> ties the "stability emerges via inflation" thread to data.
Caveats: imports CIF vs exports FOB; recent months have reporting lags for some reporters.

## REPRODUCIBLE PIPELINE (scripts/ — all pulls + analysis saved as files)

See scripts/README.md. imf_sdmx.py (helper) + fetch_imts.py + fetch_weo.py + build_panel.py
+ analyze_step1.py. Data in data/. Crisis dates: laeven_valencia_crisis_dates.csv (557 rows;
<=2017 authoritative from L-V 2020 Springer file, 2018-25 reconstructed from news).

## STEP-1 FIRST CUT (done) — promising but NOT yet confirmed

Panel: crisis episodes (L-V) x recovery_time (years for WEO real GDP NGDP_R to regain
pre-crisis peak) x pre-crisis trade openness (IMTS trade-to-World / WEO NGDPD, both raw USD).
Sample: 2005+, output_loss>=1%, recovered, openness known.
- POOLED (n=49): naive openness->recovery is NULL/WRONG-SIGNED (more-open rec 2.12y vs
  1.58y). Driven by 2008 advanced-economy banking cluster = GLOBAL shock where the trade
  link TRANSMITS the crisis (Rodrik). => a false null if you don't condition on anchor health.
- IDIOSYNCRATIC (excl 2008/09/20, n=24): sign FLIPS to thesis — more-open recover 1.42y vs
  2.58y (~1.2y faster); corr(openness, recovery_time) = -0.12. Weak, small n, confounds
  visible (Greece 2012 open but 11y on euro-austerity; tiny economies dominate).
CONCLUSION: naive generic-openness test insufficient. Real confirmation needs:
  (1) rescue channel = EXTERNAL DEMAND FROM HEALTHY PARTNERS (trade-weighted partner GDP
      growth), not generic trade/GDP openness;
  (2) explicitly net out / condition on the global financial cycle (Design 3) — pooling
      global crises kills the signal;
  (3) IMF program (MONA) horse race + program x openness interaction;
  (4) more episodes / better recovery metric (combine depth + speed).

## HAVER MONTHLY RECOVERY PANEL (built) — see memory [[haver-access]]

Why: annual WEO GDP too coarse for recovery DYNAMICS; quarterly GDP absent for EM crisis
countries; IMF IPI API gated (403). So monthly activity comes from Haver (package installed,
path \\imfdata\econ\DATA\DLX\DATA). External-demand (shift-share) measure also built:
data/step1_panel_extdemand.csv (trade-weighted partner growth) — weak but right-signed
(idiosyncratic corr -0.16), same ceiling as openness => annual metric is the bottleneck,
hence monthly Haver.

Haver mechanics (scripts/build_recovery_panel.py):
- Ticker = <prefix><IFS-numeric><concept>. dbcodes() enumeration is SLOW (~22s/db) -> do NOT
  scan; construct tickers from numeric codes + concept mnemonics and batch Haver.data (fast).
- Prefixes seen: n (NSA), s (SA), h (real-SA), c (IP in EMERGELA). Vary by db/country.
- Concept mnemonics VARY BY DATABASE: gvi=monthly activity index; tws=wholesale/retail
  turnover; tsc=mfg real sales; trsc=real retail (EMERGELA) / rsx=retail value (EMERGECW);
  i=IP (EMERGELA c..i) / d=IP (EMERGECW). Mixed M+Q freq -> normalize PeriodIndex to
  month-end timestamps before concat.
- Databases: EMERGELA (LatAm), EMERGEMA (MidEast/Africa), EMERGECW (CIS/CentralEurope),
  EMERGEPR, EMERGEFM (frontier).

COVERAGE (idiosyncratic EM crisis set, 22 countries): 13 have monthly activity ->
ARG BRA ECU SUR (LA), AGO CIV NGA SYC ZAF (MA), AZE BLR RUS UKR (CW). GVI specifically:
ARG BRA ECU RUS SUR; others via IP/retail/turnover. MISSING (small/fragile or other db):
BLZ JAM LBN LKA LSO NAM SDN SSD ZMB (LKA/ZMB/LBN matter - find their tickers).
Outputs: data/haver_recovery_panel.csv (43 series, monthly to 2026-05),
data/haver_recovery_coverage.csv. CRISIS_IFS map hardcoded in build_recovery_panel.py.

## HAVER ACTIVITY DISCOVERY + LEAD-LAG (done) — checkpoint

Auto-discovery (scripts/discover_haver_activity.py) caches dbcodes per db once
(data/haver_codes/<db>.txt) then filters to crisis IFS + descriptor-ranks to pick best
activity proxy per country (BLOCK list drops FSI/credit/govt/survey/sectoral junk).
Result: 14 crisis countries (11 monthly, 3 quarterly) -> data/haver_activity_discovered.csv,
data/haver_recovery_panel2.csv. Mostly Industrial Production + ARG/BRA activity index.
Annual-only / dead-ends (skip): ZMB, SDN, SSD, LSO, NAM, BLZ, JAM, LBN.

LEAD-LAG (scripts/analyze_leadlag.py, full-period YoY xcorr exports-to-World vs activity):
- Link is REAL & high-frequency: strong co-movement (BRA 0.64, BLR 0.69).
- But full-period direction AMBIGUOUS: median best_lag=0. Exports lead in 4/10 (SUR,BLR,LKA,
  UKR); activity LEADS exports for oil/commodity exporters (RUS,AZE,ECU) because their IP ~=
  oil output ~= exports. So full-sample xcorr conflates the channel.
CONCLUSION: full-period xcorr is the wrong test. Need CRISIS-WINDOW test: at the recovery,
does the export rebound precede the activity trough/rebound? That isolates "recovery starts
through the link" from normal-times co-movement.

INDEX-ALIGNMENT GOTCHA: IMTS monthly index = month-START; Haver activity = month-END.
Convert both to .to_period('M') before joining or you get zero overlap.

## MONA PROGRAM POPULATION + EXPANDED ACTIVITY PANEL (done) — sample solved

MONA database (LOCAL): C:\Users\ysholomytskyi\coding\localhelper\agents\knowledge\mona.db
(SQLite). Tables: arrangements(312), reviews, purchases, qpc, mecon, description. KEY:
arrangements.country_code IS the IFS numeric = what Haver embeds. Extracted to
data/mona_arrangements.csv: 97 countries with IMF programs 2005-2025 (ECF86 SBA53 EFF41
FCL35 PRGF27 ...). This is the TREATMENT and the natural sample population (distress
countries that sought help).

Generalized discover_haver_activity.py to drive off the 97 MONA IFS codes (not a hardcoded
22). Short-code prefilter (len<=9) + chunked metadata + BLOCK (drop FSI/credit/govt/survey/
climate/%bal) + SECTORAL down-rank (headline beats dairy/livestock/primary sub-indices).
RESULT: 57 program countries with activity (40 monthly, 17 quarterly); 12 economic-activity
indices + 43 industrial production. Files: data/haver_activity_discovered.csv,
data/haver_recovery_panel2.csv. Catalogs cached in data/haver_codes/<db>.txt (dbcodes is the
slow part ~22s/db; never re-enumerate). MISSING/annual-only still: Zambia, Sudan, S.Sudan,
Lesotho, Namibia, Belize, Jamaica, Lebanon, Ghana(Q only), etc.

## HORSE RACE v1 (done, annual) — directionally right, UNDERPOWERED

scripts/build_crosswalk.py -> data/ifs_iso3_crosswalk.csv (206 countries, IFS<->ISO3 via
pycountry; Lane-MF & MONA are IFS-keyed, IMTS/crisis panel ISO3). scripts/build_horserace.py
-> data/horserace_panel.csv. Sample: 29 idiosyncratic episodes (2005+, loss>=1, excl
2008/09/20), only 10 with IMF program.
- LEG 1 (depth ~ fin_open + trade_open): fin_open coef NEGATIVE, insignificant (t=-0.4),
  R2=0.01. No amplification signal in this sample.
- LEG 2 (recovery_time ~ ext_demand + program + program*openness + depth):
  program +3.9 (t=1.5, slower = SELECTION); program*openness -3.9 (t=-0.7, NEGATIVE = thesis
  sign: program drag offset where open); depth +0.10. R2=0.28, n=24.
VERDICT: all signs thesis-consistent but NOTHING significant. Binding constraint = sample
size + coarse annual recovery_time (mostly 0/1/2y). NOT a hypothesis problem - a power problem.
FIX = use the monthly Haver panel (57 countries) to (a) measure recovery precisely and (b)
recover many more usable episodes.

## *** HORSE RACE v2 (monthly, SA, endogenous downturns) — THESIS REVISED ***

Pipeline (all scripted): seasonal_adjust.py (STL on NSA, 35 countries SA monthly) ->
build_horserace_monthly.py (endogenous downturns from SA activity: underwater stretches,
depth>=3%, 164 episodes / 34 countries / 70 programs) -> build_extdemand_endog.py (shift-share
partner-growth pull per episode). Files: horserace_endog.csv, horserace_endog_extdemand.csv.

DECISIVE RESULTS (164 episodes):
- LEG 2 recovery SPEED: ext_demand (healthy-partner pull) ~ ZERO (t=0.06); generic trade_open
  +17.5 (t=2.5, SLOWER); program +8.5 (selection); prog x open -7.3 (thesis sign, insig);
  depth +1.14 (t=10, dominant). => NEITHER the link NOR the program robustly speeds recovery;
  recovery speed is mostly mechanical (depth-driven).
- LEG 1 shock DEPTH: ext_demand -2.28 (t=-2.6, SIGNIFICANT) growing partners => SHALLOWER
  downturn; trade_open +6.1 (t=2.0) Rodrik amplification; fin_open +1.1 (insig).

REVISED THESIS (data-driven, defensible): the trade link does NOT accelerate recovery; a link
to HEALTHY/GROWING partners CUSHIONS the downturn (reduces DEPTH). It works via shock
absorption, not recovery acceleration; since recov time scales with depth, cushioning the fall
indirectly shortens recovery. China story survives on the DEPTH margin: links to growing China
cushion downturns. Generic/financial openness amplifies; healthy-partner link absorbs.
CAVEATS: endogenous downturns (not all true crises); ext_demand window overlaps outcome
(simultaneity); depth->recovery partly mechanical; only 35 SA countries.

## *** HORSE RACE v3 (HP output gap, 3 timing measures) — THESIS CONFIRMED ***

scripts/build_horserace_hp.py: HP filter (log SA activity, monthly lamb=129600) -> output
gap; negative-gap episodes (depth>=2%) = 252 / 34 countries / 107 programs. Three timings:
t_full (peak->peak), t_contraction (peak->trough), t_climb (trough->peak). File:
horserace_hp.csv. ONE_SIDED flag for real-time HP (endpoint robustness) - default 2-sided.

RESULTS (ext_demand = trade-weighted partner growth = healthy-partner pull):
- DEPTH:        ext_demand -1.24 (t=-2.2)** shallower ; trade_open +3.8 (t=1.8)* deeper (Rodrik)
- CONTRACTION:  ext_demand -0.72 (t=-2.5)** shorter  ; trade_open +6.4 (t=3.9)*** longer (Rodrik);
                prog_x_open -3.4 (t=-1.7)* shorter where open
- CLIMB:        ext_demand -2.03 (t=-3.2)*** FASTER climb-out ; trade_open ~0; program ~0
- FULL cycle:   ext_demand -2.63 (t=-3.7)*** shorter ; trade_open ~0

INTERPRETATION (the paper's core, CONFIRMED): a link to GROWING partners cushions the fall
(depth), shortens the contraction, AND speeds the climb-out. Generic/financial openness is
pure Rodrik (deepens+prolongs contraction, no recovery help) = exposure not rescue. Programs:
no robust effect; program x openness shortens contraction where open (thesis sign).
WHY v2 gave a null: level-drawdown peak->peak recov was mechanically dominated by depth; HP
detrending + isolating the CLIMB (trough->peak) reveals the large significant partner effect.
Measurement (HP gap + trough->peak climb) was decisive - user's instinct correct.
CAVEAT: 2-sided HP endpoint bias for 2024+ episodes -> re-run ONE_SIDED=True as robustness.

## *** HORSE RACE v4 (BUG FIXED, clustered SEs, China decomp) — China hook DOESN'T hold ***

BUG FOUND+FIXED: WEO COUNTRY list contains AGGREGATE codes (G001=World, G200, G110...). The
ext_demand partner filter isin(weo.COUNTRY) KEPT them, so every ext_demand was contaminated by
"World" as a giant pseudo-partner. Fixed: restrict partners to real ISO3 via crosswalk
(set(cw.iso3)). Re-run all ext_demand. (build_external_demand.py / build_extdemand_endog.py
have the SAME bug if reused - apply same fix.)

CORRECTED RESULTS (HP gap, 246 episodes/34 countries, SEs CLUSTERED by country):
- CLIMB (trough->peak): ext_demand -1.74 (t=-2.8)*** speeds climb. Decomp: rest_pull -1.96
  (t=-2.8)*** SIGNIFICANT; china_pull -0.94 (t=-1.3) right sign but INSIG.
- FULL cycle: rest_pull -2.38 (t=-2.8)***; china_pull -1.17 (t=-1.2) insig.
- DEPTH: ext_demand -0.49 (t=-0.8) now INSIG (was sig before bug fix - depth-cushioning was
  an artifact of the World-contamination). trade_open +4.5 (t=1.7)* Rodrik.
- CONTRACTION: trade_open +3.96 (t=3.4)*** Rodrik; partners insig.
- Programs: no robust effect anywhere.

HONEST CONCLUSION: the recovery-speeding pull is real (climb, full cycle) but comes from
DIVERSIFIED rest-of-world export partners, NOT China. China export shares too small (median
1.5%) -> china_pull insignificant. This is CONSISTENT with the headline: the China shift is
IMPORT-side (cheap supplier / disinflation channel); on EXPORT-demand China is still small, so
it canNOT be the demand-pull recovery anchor. China=supplier; recovery anchor=rest of world.
The "weld China to recovery" payoff move FAILS - and that's itself a finding (two separate
channels: China import/disinflation vs Western/regional export-demand recovery pull).

## *** HORSE RACE v5 (ADVANCED vs EMERGING vs CHINA) — "GOOD ACTORS" THESIS CONFIRMED ***

Decomposed partner-demand pull by partner type (ADVANCED set hardcoded in build_horserace_hp.py
= IMF AEs; emerging = rest excl China; china separate). Clustered SEs by country, 245 episodes.
- CLIMB:  adv_pull -2.73 (t=-2.5)** ; emer_pull -1.54 (t=-2.0)** ; china_pull -0.96 (t=-1.3) ns
- FULL:   adv_pull -3.64 (t=-2.7)*** ; emer_pull -1.67 (t=-1.8)* ; china_pull -1.21 (t=-1.3) ns
- DEPTH:  adv_pull ~0 ; emer_pull -1.61 (t=-2.4)** cushions ; china_pull +1.86 (t=3.7)*** DEEPER ;
          trade_open +3.96 (t=1.9)* Rodrik ; program +2.37 (t=1.8)* selection

HEADLINE THESIS (data-backed): links to ADVANCED economies ("good actors") FACILITATE RECOVERY
- their demand pull is the largest, most significant driver of a faster climb-out. Emerging
partners help less; CHINA pull does nothing for recovery and correlates with DEEPER downturns
(likely commodity-exporter confound: China-export-heavy = commodity producers w/ volatile IP;
flag + control with commodity dummy). Provocative read: the eastward shift substitutes a
stabilizing advanced-demand anchor for volatile commodity-style China exposure -> may make
recovery harder, not easier. "Good actors still do the stabilizing."

## COMMODITY CONTROL (done) — "China -> deeper" is PURE COMPOSITION, confirmed

Split china_pull by commodity-exporter status (COMMODITY set in build_horserace_hp.py; 95/246
episodes commodity). DEPTH:
- china_pull_comm    +2.09 (t=5.8)*** (commodity exporters: China exposure -> deeper)
- china_pull_noncomm -3.38 (t=-0.7) ns (non-commodity: NO deepening)
=> the "China deepens downturns" result lives ENTIRELY in commodity exporters = commodity-cycle
composition, NOT China destabilizing diversified economies. Safe to state explicitly.

## FINAL HEADLINE RESULTS (HP gap, 245-246 episodes, 34 countries, country-clustered SEs):
1. Advanced "good actor" demand pull -> FASTER recovery (climb -2.7**, full -3.6***) = HEADLINE.
2. Emerging-partner demand -> faster recovery (smaller) + cushions depth (-1.5**).
3. China pull -> no recovery effect; "deeper" is pure commodity composition (above).
4. Generic/financial openness -> Rodrik (deepens/prolongs contraction).
5. IMF programs -> no robust recovery effect (selection on depth).
PAPER THESIS: recovery is facilitated by demand from growing ADVANCED "good-actor" partners;
generic exposure and IMF money don't get you out; the China link is a commodity-side story,
not a recovery anchor. (Ties to headline: China shift is import/disinflation side, not export-
demand recovery side.)

## PROGRAM-BY-INSTRUMENT + TRIPLE (done) — power frontier reached

MONA focus flags (0/1) pulled into panel (build_horserace_hp.py prog_focus): f_fx
(focus_exchange_rate, 50%), f_trade (14%); fiscal near-universal (84-95%, non-discriminating).
prog_fx / prog_nofx / prog_trade = program x focus.
- Program drag is concentrated in NON-FX programs: prog_nofx +4.1 (t=1.6) climb, +3.4 (t=1.7)*
  depth; prog_fx ~0 (neutral). => binary null masked offsetting channels (devaluation export
  boost vs fiscal compression). DIRECTIONAL/MARGINAL - footnote, not a headline.
- TRIPLE prog_fx x adv_pull: +2.4 (t=1.0) climb, +0.4 (t=0.1) full = INSIGNIFICANT, wrong sign.
  Cannot identify a 3-way interaction at this n. Leave as conjecture.

ROBUST across ALL specs: adv_pull (advanced-partner demand) -> faster recovery, t=-2.5..-3.5
ALWAYS significant. THIS IS THE PAPER. emer_pull helps too (smaller). Everything else is
secondary/marginal. Stop slicing here (further cuts = mining noise).

## THEORY — Layer-1 stylized model (scripts/model_layer1.py, output/model_layer1.png)

Core-periphery reduces to TRADE-AS-RISK-SHARING (portfolio). Periphery output:
  y_i = (1-s_i) eps_i + s_i mu ;  eps_i=idiosyncratic (Var sig_e^2, volatile),
  mu=US demand (Var sig_m^2, STABLE, sig_m<sig_e, eps _|_ mu). s_i=export share to core.
  => Var(y_i)=(1-s_i)^2 sig_e^2 + s_i^2 sig_m^2 ; falls in s_i up to s*=sig_e^2/(sig_e^2+sig_m^2).
US AI/ENERGY TILT theta = share of US absorption to LOW-IMPORT-CONTENT domestic capital
(AI/data centers/onshore chips/energy). s_i(theta)=omega_i(1-theta). Rise in theta -> lower s_i
-> HIGHER Var(y_i). Key: US keeps GROWING (level) but import spillover falls (composition).
RESULTS (calib sig_e=5,sig_m=2): stabilization up to 86% var reduction; dVar/dtheta>0 ALWAYS
(+11..+19); world avg periphery variance +16% as theta 0.2->0.5. US-bloc (high omega) most
stabilized at low theta but LOSES MOST as theta rises (Mexico/CentAm have most to lose).
This is the THEORY layer matching us_pull empirics. NEXT theory: Layer-2 quantitative DSGE
(core w/ AI/energy capital accumulation + intertemporal choice + representative SOE), linearized,
IRFs to periphery shock under low vs high theta, volatility table, calibrate omega/eta/import
shares to IMTS. No Dynare -> small Python linear-RE solver / simulation.

## ROBUSTNESS (done) — us_pull BULLETPROOF (scripts/robustness_hp.py, output/robustness_table.txt)

Refactored build_horserace_hp.py -> build_episodes(one_sided, min_depth, crisis_only) importable.
Full-cycle us_pull across specs (all *** at 1%):
- Baseline 2-sided HP: -6.13 (t=-3.4), n=245
- ONE-SIDED (real-time) HP: -7.22 (t=-3.0), n=199  [endpoint-bias worry -> STRONGER, not weaker]
- TRUE-CRISIS subsample (L-V, +/-1yr): -23.6 (t=-2.7), n=23  [US demand matters MOST in real
  crises; small n imprecise but strongly signed]
- depth>=3%: -6.54 (t=-3.1), n=180 ; depth>=1.5%: -5.54 (t=-3.1), n=274
china_pull insignificant throughout. HEADLINE (US demand = recovery anchor) survives everything.

## LOCAL PROJECTIONS (done) — dynamic twin (scripts/local_projections.py, output/local_projections.png)

State-dependent Jorda LP: activity response to a Bartik US-demand impulse (US IP 12m growth x
US export share), country FE + country-clustered SE, by HP-gap state. Control for gap LEVEL +
state (absorbs the mechanical "recession-> mean-reversion" baseline; without it the recession
line was spuriously negative). US IP from Haver USECON:ip (data/us_ip_monthly.csv).
RESULT: US-demand impulse raises activity in BOTH states. Normal times: fast hump, peak +1.44%
(t=6.0) at ~8m. Recession: slower, builds to +0.58% (t=3.9), still rising at 18m = a persistent
recovery pull. Dynamic confirmation of the trade-demand channel + us_pull.

## ECONOMETRIC REVIEW (/economist) — scripts/estimation_diagnostics.py

Reviewed the headline us_pull (full cycle -6.13, t=-3.40). Threats tested:
- FEW CLUSTERS (34): restricted WILD CLUSTER BOOTSTRAP (Rademacher) -> p=0.000. Survives. ✓
- BAD CONTROL (depth on RHS of duration reg): drop depth -> us_pull -6.90 (t=-3.82), STRONGER. ✓
- OVERLAPPING WINDOW: on CONTRACTION outcome (pre-window) us_pull -2.49 (t=-3.41). Survives. ✓
- LEAVE-ONE-COUNTRY-OUT: range -5.3 to -7.5, ALL negative. No single-country driver. ✓
- *** CONCENTRATION (the real issue): drop top-6 US-exposed (MEX,COL,CRI,ECU,DOM,SLV) -> us_pull
  +0.15 (t=0.04). COLLAPSES. Effect identified off the US-exposed bloc (Goldsmith-Pinkham shift-
  share). => REFRAMED as a HUB EFFECT not universal anchor. Honest, and matches regionalization.
- ENDOGENOUS HP EPISODES + window: stated as caveats (LP with dated shock = defence).
PAPER UPDATED: WCB p=0.000, no-depth, contraction robustness; cameron2008 + goldsmith2020 cites.

## HUB DECOMPOSITION (the concentration IS the mechanism) — scripts/hub_decomposition.py

Reframed: US-bloc concentration is NOT a weakness, it's the HUB mechanism. Assign each country
to hub it exports most to (US / EU / China), split pull into own-hub vs non-hub.
Assignment: US hub 9 (MEX,COL,CRI,ECU,DOM,SLV,NIC,PAN,JOR); EU hub 24 (emerging Europe + ARG,
CHL,PER,EGY,PAK...); China hub 1 (MNG only). Median own-hub export share 43%.
RESULTS (clustered): FULL cycle own-hub -2.77 (t=-3.0)*** vs non-hub -1.68 (t=-2.0)** -> own
hub drives recovery MORE. Within blocs: US-bloc via US demand -5.17 (t=-3.4)***; EU-bloc via EU
demand -2.37 (t=-1.7)* (weaker bc EU grew slower = "good actor must be GROWING"). China untestable
(1 country) -> CHINA IS NOT A HUB (no one exports mostly to China; it's a supplier not buyer =
export-side confirmation of the import-side headline).
=> This is the CENTRAL result now. Paper: new subsection "Every bloc recovers through its hub",
abstract + caveats reframed around the hub mechanism. Data: data/hub_panel.csv.

## DISTANCE-FROM-GROWTH + PARTNER VOLATILITY (both added)

User: "farther from stable countries = harder case." Tested (share to US+EU stable hubs +
partner-growth volatility):
- Raw proximity (export share to US+EU) does NOT speed recovery (+5.9, t=1.1, WRONG sign) ->
  stability without GROWTH doesn't pull (EU stable but slow). So it's distance from GROWING, not
  stable-advanced, that matters (= hub_pull, already the result).
- PARTNER VOLATILITY (exposure-weighted std of partner growth) -> DEEPER downturns: +1.74
  (t=2.8)*** on depth. NEW result. Added to build_horserace_hp.py extdem (partner_vol col) + the
  depth column of Table 1 (make_tables.py) + a "Volatile partners deepen the fall" paragraph.
- Hub subsection reframed: hardest case = economy with no large GROWING buyer nearby + volatile
  partners (isolated commodity exporter). "Distance from stable demand is really distance from
  growth." Ties to model s_i (gravity keeps s_i low for the remote).

## ANCHOR QUALITY vs CYCLE + "WHO RECOVERS / WHO IS STUCK" (scripts/recovery_chances.py)

Demand-Sharpe (growth/vol 2005-24): CHN 2.68 highest RAW but fails 2 conditions (not a buyer;
its growth = correlated commodity channel). Among BUYERS (advanced), US dominates: growth 2.1
(2x EU), vol 1.87 (LOWEST major econ), Sharpe 1.13 vs EU 0.45, JPN 0.26. US = rare large+growing
+stable+open-to-your-goods anchor.
REFINED idiosyncratic measure (hub growth during country's LOCAL downturns, excl global 08/09/20):
- Local crises: hub almost always GROWING (median +1.8%); US-bloc strongest (~2.5%), EU-bloc weak
  (~1-1.5%). MEX now GOOD on idiosyncratic (US grew during Mexico's local crises) -> unconditional
  corr (0.86) was inflated by global crises. Deep integration fine for LOCAL, fails GLOBAL.
- GLOBAL crisis (2009&2020): US -2.3%, EU -4.7% (demand hubs CRASH -> anchor fails, Rodrik
  transmits); CHN +5.9% (stimulus, countercyclical) BUT buys little -> reached only Mongolia.
  => mechanism BOUNDED to idiosyncratic crises; global crisis is WORSE, no hub saves you.
IMF POLICY READING (explains the null): for LOCAL crises the partner's demand does the recovery
-> IMF programme has little recovery work left (its BoP financing may bridge, but doesn't turn
output around); where programme would matter most (global crisis, anchor gone) it can't
substitute for a vanished buyer.
Figure output/recovery_chances.png added to paper (Fig "who recovers/stuck").

## VULNERABILITY SYNTHESIS (the conclusion) — asymmetric shift
China rose as SELLER (import side: cheap goods/disinflation, NO recovery help). US eroding as
BUYER (demand side: tariffs cut export access + AI-capex shrinks import appetite = the anchor).
Two movements DON'T offset: country gains a non-anchor (China, volatile supplier) + loses its
anchor (US buyer). Trade never fell -> beside the point. "Re-coupled to China as a seller,
decoupled from US as a buyer; only the buyer stabilises -> eastward shift raises cost of next
crisis." In forward section + this is the paper's one-line conclusion.

## THEORY Layer-2 — DSGE in the user's OWN framework (modken-snork) — see [[modken-snork-dsge]]

Built round `core_periphery_ai` in modken-snork (semi-structural QPM gap model, SS=0). US AI/
energy investment is low-import-content: m = mu_c*c_US - theta*inv_US. Forward-looking US Euler
+ real-rate rule (1 jump var -> Klein-determinate). Driver scratch/cp_ai_irf.py ->
output/model_layer2_irf.png. RESULT (IRFs, low theta=.2 vs high theta=.8):
- US AI boom: US output UP (+0.06) but PERIPHERY output DOWN; cumulative periphery resp
  -0.91 (low theta) vs -2.39 (high theta), trough -0.25. AI-driven US boom is CONTRACTIONARY
  abroad, worse with higher tilt.
- COMPOSITION flips sign: same US output rise from CONSUMPTION -> periphery +0.11; from AI
  INVESTMENT -> periphery -2.4. The headline DSGE result.
RUN NOTE: installed modken (localhelper) shadows repo -> sys.path.insert repo first.

REFINED (both channels + "extra growth, all investment" per user):
- AI capex CROWDS OUT consumption (psi_crowd) and is import-light: a US AI surge gives modest
  EXTRA GROWTH (US output +0.10, the capex IS GDP) but consumption -0.6, US IMPORTS -0.97,
  periphery -0.3. Composition: US consumption boom -> periphery +0.13; US AI capex -> -0.29
  (opposite sign). US "grows" while the world gets nothing (import-light AI, not import-pulling
  consumption). Key user point: AI is investment without an output/productivity boom.
- BUFFERING LOSS (kappa_th): y_P = (1+kappa_th*theta)(1-lam)c_P + lam*x_P. High-AI-tilt world
  has DEEPER periphery downturns from its OWN shocks (panel-3 trough 1.37 high-theta vs 0.87
  low-theta) -> the Layer-1 cushioning channel now in the DSGE.
- Cumulative periphery hit from US AI capex: -1.28 (low theta) -> -2.77 (high theta).
- Calib: wi=.45 wc=.55 phi_y=.25 psi_crowd=.05 kappa_th=1.2 lam=.3 mu_c=.5. (lam*(1-theta)
  REJECTED: cancels in the US-boom channel; used buffering-amplifier instead.)
Both DSGE channels now match Layer-1 + empirics.

## US vs OTHER-AE DECOMPOSITION — the US IS the anchor (the forward punchline)
Split adv_pull into us_pull (USA contribution) + otheradv_pull. Clustered, 245 episodes:
- CLIMB: us_pull -3.93 (t=-2.9)*** ; otheradv -2.15 (t=-2.0)* ; emer -1.57** ; china -1.0 ns
- FULL : us_pull -6.13 (t=-3.4)*** ; otheradv -2.06 (t=-1.5) ns ; emer -1.84** ; china -1.3 ns
US dominates; on the full cycle other-AE fades to insignificance. So "good actors facilitate
recovery" = US demand facilitates recovery. Magnitude: 1pp lower US-weighted demand pull ->
~6 months longer full negative cycle. US export share median 5% but 30-80% for Mexico/CentAm/
Caribbean. FORWARD PUNCHLINE (quantified): US retrenchment (slowdown + tariffs) withdraws the
PRIMARY recovery anchor for US-linked economies; China does NOT substitute (insig). Closes the
loop with the opener (US = lone decoupler) -> US demand = irreplaceable recovery anchor ->
retrenchment measurably raises crisis-recovery risk, no Eastern substitute.
CAVEAT: identified off US growth x US-export exposure; tariffs cut ACCESS not growth (adjacent
channel, estimate separately); outcome = cycle duration not crisis incidence.

## NEXT (robustness before write-up): ONE_SIDED=True HP (endpoint); true-crisis subsample (L-V
## flag); vary MIN_DEPTH; IMF analytical commodity group vs hardcoded. Then WRITE UP around
## "advanced good-actor demand facilitates recovery". Figure 1 (US decoupling) still pending.
## Agg-bug fix also needed in build_external_demand.py / build_extdemand_endog.py if reused.

## *** REFRAME (2026-07-31): PROGRAMME ANGLE = SUPPORTIVE ONLY, de-politicized (FINAL) ***

User decision (iterated in-session to this end state): the paper focuses on WHAT EXPLAINS
FASTER RECOVERY. IMF programmes may be mentioned, but ONLY supportively/constructively
(findings HELP programmes); no criticism or effectiveness verdicts in any sense. Lower
political gradus overall. End state of paper/trade_recovery.tex + generators:
- Sri Lanka opener: programme "anchored the adjustment... set the stage"; external demand
  supplied the pull. Positive on both.
- Related lit: horse-race strand (Przeworski/Barro-Lee/Dreher/Bird) GONE; instead a
  supportive paragraph: IEO (2021) says programmes help countries exploit favourable external
  conditions; our demand measure identifies those conditions (complement, not critique).
- "Who recovers" ends with constructive complements paragraph: partner demand pulls in local
  downturns; official financing bridges to it and carries the greatest weight where no growing
  hub is in reach (global crises, isolated economies). NO null-coefficient reading anywhere.
- MONA: sample frame AND active-arrangement indicator tracked in EVERY regression as an
  "additional factor" so demand effects are "over and above official support" (framing:
  tracking extra factors, not testing programmes). Programme coefficient NEVER displayed or
  discussed. make_tables.py: program in xs but not in rows; footnotes say it is tracked.
  tab:program (by-instrument) table stays DELETED. appendix summary row (42% episodes with
  arrangement) restored, neutral. prewindow: program control restored (onset -4.6, t=-4.0).
- Updated headline numbers w/ program control: US full cycle -6.1 (t=-3.1); contraction -2.6
  (t=-3.2); china x commodity +2.1 (t=6.2); partner vol +1.7 (t=2.9); trade_open now sig only
  on CONTRACTION (+3.15, t=2.9), depth positive insig -> text rewritten accordingly.
- Tone: "US tariff policy"->"shifts in trade policy"; "sole large decoupler"->"exception among
  the large economies"; "tariffs reduce export access"->"trade measures have reduced access".
Compiles clean, 31 pp.

## COMMODITY-CYCLE ROBUSTNESS (2026-07-31) — us_pull SURVIVES; + NOVELTY CHECK

Referee worry: commodity prices co-move with US/global growth -> us_pull could proxy the
commodity cycle (Drechsel-Tenreyro JIE 2018 etc. say commodity prices drive EM cycles).
Test: scripts/commodity_control.py pulls IMF CTOT (IMF.RES/CTOT on api.imf.org SDMX;
indicator CEMPI_CTOTXM_GDP = Commodity Net Export Price Index, GDP-scaled; WGT_TYPE=R_FW_IX
fixed weights = predetermined; 182 countries monthly 1980-2026-05; raw saved
data/ctot_raw_monthly.csv). ctot_g = avg annual log growth over [peak, peak+2] (same window
as ext_demand), + interaction with commodity dummy.
RESULT: corr(ctot_g, us_pull)=0.08 (orthogonal). US demand UNCHANGED: full -6.0 (t=-3.1),
contraction -2.7 (t=-3.2), climb -3.6 (t=-2.5). ctot_g itself: NO significant duration
effects; depth interaction +2.3 (t=1.9) marginal. Added: robustness paragraph in Results,
appendix Table tab:commodity (output/tables_commodity.tex), gruss2019 cite, data-source +
vardef rows. 32 pp.

NOVELTY CHECK (web, 2026-07-31): closest prior = Deb (2006, Rutgers WP 200607) "Trade First
and Trade Fast" — duration analysis of currency-crisis recoveries; partner growth/export
variables shorten recovery (also Sahay-Mishra-Gupta 2003 IMF WP; resilience lit Economic
Modelling 2024: trade openness + external-demand substitution aid resilience). So the RAW
channel (partner growth speeds recovery) is anticipated in older currency-crisis lit -> now
CITED (deb2006) with differentiation: we generalise beyond currency crises to all dated
downturns, shift-share decomposition BY PARTNER TYPE, hub structure, monthly output-gap
episodes. NOT found anywhere: partner-type decomposition / own-hub result / China-not-a-hub /
import-light composition (AI) forward mechanism. Contribution stands on those.

## PORTFOLIO COUNTERFACTUAL (2026-07-31) — "partner choice pays only if partner GROWS"

scripts/counterfactual_rebalance.py: rebalance each episode's pre-crisis export-share vector
by DELTA=5pp toward its own hub (proportional within hub, funded proportionally from non-hub;
variant B funds from China share alone), price with Table-1 full-cycle betas (computed on the
full 245 sample: us -6.10 / oa -2.04 / em -1.85 / ch -1.25) at realised partner growth.
204 episodes priced (unique iso3 x peak_year with non-degenerate hub share).
RESULTS (months of full cycle, negative = saved, linear in DELTA):
- toward hub: US-bloc median -0.44 [IQR -0.52,-0.25] (~1 month per 10pp); EU-bloc +0.20
  (rebalancing toward slow-growing EU SAVES NOTHING - funded EM partners grew faster);
- China->hub: US-bloc -0.09; EU-bloc +0.10.
MESSAGE: partner choice pays only when the chosen partner is growing; big cross-country
recovery gaps come from deep structural orientation (Mexico-type), not marginal shifts.
Paper: new subsection "What partner choice is worth" + Table tab:counterfactual
(output/tables_counterfactual.tex, data/counterfactual_rebalance.csv). Explicit caveat:
accounting exercise, partial-equilibrium, not policy advice (de-politicized). 33 pp.

## LP STATE = CYCLICAL PHASES (2026-07-31, user-directed NEW BASELINE)

User: state must mean CYCLE, not month-by-month sign / random series changes. Final rule in
local_projections.py rec_state() (defaults LP_MIN_RUN=12, LP_MAX_RUN=84, LP_BAND=0.2):
- recession: gap < -0.2% inside a continuous below-band spell of 12-84 months (1-7y);
- normal: gap > +0.2%;
- EXCLUDED (dropped, NOT relabelled): |gap|<=0.2 (on trend), and below-band months in spells
  <12m (transitory dips) or >84m (trend mismeasurement).
TWO BUGS hit along the way: (1) relabelling short-spell months as "normal" contaminated the
normal state (blue line dipped to -0.1 => user caught it); fix = exclude, not relabel.
(2) UNIT BUG: gap from hpfilter(log a) is in LOG units; 0.2 band applied unscaled = 20% =>
sample collapsed, absurd 195% responses; fix = gap*100 before classifying.
NEW BASELINE RESULTS (paper figure/table regenerated): normal peak 1.52 (t=5.9) at h=9;
recession positive from impact, builds to 0.77 (t=3.2) at h=18 still rising, crosses above
normal ~15m. No negative dips anywhere. Sign-rule variant kept as robustness (recession 0.58 =
diluted). Paper: LP paragraph rewritten w/ state definition + new numbers; caption updated.

## PARTNER STABILISATION QUALITY (2026-07-31) — user's "responsive-policy partner" idea

User framing: partners with responsive stabilisation policy recover fast themselves ->
trading with them imports their stabilisation. Test: scripts/partner_stabilization.py.
partner_rebound = export-share-weighted avg of partners' growth in the year AFTER their own
negative-growth years, expanding window through peak year only => FULLY PREDETERMINED
(defends timing too). corr with us_pull 0.43, with partner_vol -0.07.
RESULTS: alone, full cycle -1.61 (t=-1.9)*, depth -1.74 (t=-1.9)*; WITH demand pulls it is
absorbed (-1.11, t=-1.2) while us_pull stays -5.3 (t=-2.5). Ordering = the mechanism:
stabilisation capacity matters BECAUSE it delivers demand; trait predicts recovery until the
delivered demand is measured. Paper: sigma_mu-is-policy sentence in theory ("by exporting to
a well-stabilised economy a country imports that stabilisation"), results paragraph, appendix
Table tab:stabilization (output/tables_stabilization.tex), vardef row. 34 pp.
TRIVIALITY DEFENCE (user worried idea is trivial): the one-liner is simple but its corollaries
are not and are what the paper actually shows: (1) trade VOLUME does not help (openness
prolongs contractions); (2) fast partner GROWTH does not transmit unless spent on imports
(China null); (3) partner STABILITY without growth does not pull (EU weak, counterfactual);
(4) anchor can keep growing while withdrawing demand (import-light composition) - the simple
rule silently fails; (5) magnitude 6 months/pp. Simple premise, non-trivial corollaries.

## (old) NEXT STEP -> PIVOT TO MONTHLY for power

Build monthly recovery metrics from data/haver_recovery_panel2.csv (57 countries): per crisis
episode, trough date + months-to-recover-prior-peak from the monthly activity series (much
finer than annual; yields more usable episodes). Then re-run the horse race (program x
openness, trade-link, fin-openness-on-depth) on the larger monthly-derived sample. Also the
crisis-window lead-lag (export trough vs activity trough) as the mechanism visual.
Need: join Haver activity (IFS/name) to crisis episodes + IMTS via ifs_iso3_crosswalk.csv.

## (superseded) RUN THE HORSE RACE:
(1) Crisis-window lead-lag on the 40 monthly countries: export trough vs activity trough,
    +/-24m around each idiosyncratic episode -> "recovery starts through the link".
(2) Two-leg model: financial openness -> shock DEPTH; trade-link/external-demand -> recovery
    SPEED; program x openness interaction (does IMF program help only where plugged in).
Caveats: oil exporters' IP~=exports collinearity; some chosen series are DISC (discontinued)
vintages / sectoral fallbacks. Still open: Figure 1 (US decoupling vs RoW re-coupling).
IFS->ISO3 crosswalk still needed to join Haver (IFS/name) to IMTS (ISO3) at scale.

## *** REFEREE REVISION (2026-08-24): paper/trade_recovery_revised.tex ***

Reviewer verdict = major revision but friendly (core empirical result publishable; wants the paper
DISCIPLINED to one associational claim). Plan agreed with user, executing in order.

Reviewer's recommended NARROW proposition (build the paper on this): "Conditional on downturn
characteristics, economies recover faster when the foreign markets to which they were already
exposed continue to grow" -- association, follows regional export hubs, not captured by openness.
User decisions: keep title "Consumer of Last Resort"; shrink dynamic DSGE to a paragraph (keep
Fig 3, drop eqs 4-11 + calib table); do alt-recovery + sample-comparison (NOT non-MONA re-est);
present alt-recovery honestly/narrow-led.

DONE - A1 alt recovery measure (referee: HP zero-crossing dates spurious recoveries).
scripts/build_horserace_hp.py episodes_from_gap now also emits (baseline untouched):
  cum_loss (area of negative gap), t_full_p3/p6 + t_climb_p3/p6 (persistent-return: gap must stay
  >=0 for k months, searches full series so brief crossings don't date recovery). PERSIST_KS=(3,6).
scripts/alt_recovery.py -> output/tables_altrecovery.tex (2-panel: all-partners / by-partner-type).
KEY FINDING (263 eps, country-clustered): narrow claim SURVIVES, US-alone concentration is
TIMING-SENSITIVE:
  - t_full baseline: us_pull -5.6*** ; adv_pull -3.8*** ; ext_demand -1.4*
  - t_full_p3      : us_pull -2.0 ns ; adv_pull -2.5** ; emer -2.0* ; ext_demand -1.5** (HOLDS)
  - t_full_p6      : all ns, LOW POWER (9.5% censored, R2=0.03) - flagged, not leaned on
  - cum_loss       : us_pull -34*** (dominant on magnitude); china +21***
Interpretation written into Results ("Recovery measures independent of the HP crossing" para) +
appendix intro: total/advanced demand robust; US-specific sharpening + 6-month number are the
baseline-crossing association, not a definition-free constant. This SUPPORTS reviewer's narrow reframe.

DONE - A2 sample-selection comparison (referee: MONA + monthly-data selection, external validity).
scripts/sample_comparison.py -> output/tables_samplecomp.tex. 3 groups over 2005-24: Included(34)
vs MONA-excluded(59) vs Other-EMDE(65). Observables: GDP(log-tested, skew), trade openness, growth,
growth vol, commodity share. RESULT (Incl - OtherEMDE): size +0.4 log10 (t=1.9)*; openness ns;
growth ns; growth VOL -1.5 (t=-2.5)** (sample LESS volatile, NOT most crisis-prone); COMMODITY
+24.7pp (t=2.8)*** (the one real selection diff, controlled for via CTOT + China-x-commodity split).
Framing: sample = the relevant POPULATION of externally-exposed EMDEs w/ monthly data. Wired into
Sec IV Sample para + appendix app:sample + conclusion limitation 3. Compiles clean, 45 pp.

NEXT (per agreed order): B1 shrink dynamic model to a paragraph; B2 narrow China/fragmentation
claims + compress Sec III; B3 compress import-light scenario; then C1 association-not-causation
audit, C2 reframe intro/contribution on narrow proposition, C3 house-style pass. Then recompile.

DONE - B1 shrink dynamic model. Sec III "A dynamic illustration" now = 2 short paras (frames model
as calibrated illustration, honestly flags the one buffering-loss equation, keeps Fig 3 fig:layer2,
points to appendix). FULL model MOVED to new Appendix H "The dynamic core-periphery model"
(app:model): 6 core eqs, 3 periphery eqs, calib table tab:calib, full IRF discussion; eq:periph_y
explicitly labeled "the single equation that, by construction, builds in the buffering-loss
assumption... imposed, not derived" (answers referee's (1+kappa*theta) objection head-on).

DONE - B2 narrow China/fragmentation to "in this sample" + soften fragmentation-literature takedown.
Edits: Sec III China-not-a-consumer -> "for the economies studied here"; fragmentation projections
-> "over the window studied here" + "whether integration unwinds in future is a separate question";
Sec III closing "shows...matters" -> "finds that, in this sample, ... associated with the pace of
recovery"; intro "shows immaterial" -> "finds it largely immaterial ... in this sample"; results
China-hub "grew as the world's producer" -> "these economies' supplier ... over this period";
related-lit "an actual unwinding did not happen" -> "within this period ... reorientation";
scenario China "predominantly a producer" -> "for the economies in this sample ... a supplier".

DONE - B3 compress import-light scenario. Sec VI 8 paras -> 3, retitled "Implications: if the anchor
turns import-light"; added closing "These are conditional implications ... not forecasts." Constraints
kept: AI is ONE hypothetical import-light shift, conditional mood, low political temperature.

DONE - C1 association-not-causation audit. Dedicated \paragraph{Identification} already present and
clean (shift-share logic, predetermined weights, common-global-factor + timing worries, states
"best read as an association rather than a clean causal effect"). Abstract/intro/results/scenario/
conclusion all associational. Fixed redundant causal pair in intro ("determines...governs" -> "how
it grows shapes the demand it sends abroad"); conclusion "US-demand effect" -> "association".

DONE - C2 reframe intro/contribution on narrow proposition. Contribution para now LEADS with referee's
narrow claim ("conditional on the depth and character of a downturn, economies recover faster when the
foreign markets to which they were already exposed keep growing"), labels estimate an association,
moderated novelty ("existing literature does not provide" -> "lets the data say which partner the
association runs through").

DONE - C3 house-style pass. No em-dashes in file; removed lone "moreover" (line 435). New text uses
comma/clause style, conditional mood.

STATUS: compiles clean twice, 46 pp, no undefined refs. All referee themes addressed:
(1) identification=association [C1 + A1 honesty], (2) novelty moderated [C2], (3) sample defended
[A2], (4) HP-crossing-independent recovery measure [A1], (5) theory simplified to illustration +
buffering-loss owned [B1], (6) China/fragmentation narrowed to sample [B2], (7) length cut [B1+B3].

=== TIER-1 LEAVE-ONE-OUT IDENTIFICATION (referee's shift-share request) ===
DONE - built scripts/identification_loo.py. Leave-one-out import-demand shift
Z_i = sum_j s_ij,e-1 * g_j^{-i}, where g_j^{-i} = growth of destination j's imports from ALL
origins except the exposed economy over yr..yr+2, from imts_bilateral_exports_annual.csv (annual,
aggregate goods; world imports of j proxied by sum of reported bilateral exports into j). Same
predetermined pre-downturn export shares as the baseline pull. Residualized on destination + year FE
(region×time / product×time have no counterpart in aggregate annual data -> stated as out of scope).
Exposure-robust (Adao-Kolesar-Morales / BHJ shock-level) SEs implemented (akm_se). Validation:
pre-trend placebo, shock balance, leave-one-destination, shock concentration.

RESULTS (263/264 episodes, 34 countries): corr(LOO, baseline GDP-growth pull)=0.47 (related, not a
relabel). Full cycle: loo_ext -0.27 (t=-2.6, clustered); residualized -0.91 (t=-3.7). US
decomposition -0.88 (t=-3.0), other-adv/emer/China individually insignificant -> US-led pattern
REPRODUCED under leave-one-out. AKM exposure-robust SE does NOT overturn significance (many diffuse
destinations: median 1/HHI~6, median largest weight 0.33). Placebo: contraction leg no significant
loading (t=-1.5). Balance: small/insig on commodity, marginal on openness. Leave-one-destination:
corr 0.97, coeff stable. Table output/tables_loo.tex.

PAPER (trade_recovery_final_revised.tex): new \paragraph{A leave-one-out import-demand shift.} in
App B (app:robust) with \input tables_loo.tex; pointer added to main Identification para; adao2019
bibitem added; data-and-code appendix documents identification_loo.py. Compiles clean twice, 48 pp,
0 undefined refs / citations.

=== CANONICAL FILE (renamed) ===
paper/trade_recovery_revised.tex is now THE canonical paper (author's identification-integrated
rewrite: leave-one-out design elevated to main-text Identification with eq:loo_shift, adds
Borusyak-Hull-Jaravel citation alongside Adao-Kolesar-Morales, more careful causal framing;
re-inserted the "~20 distinct peak-year values / effective ~22 of 34 clusters" clustering rationale).
Compiles clean twice, 49 pp, 0 undefined refs/citations. Superseded drafts (former
trade_recovery_final_revised.*, original trade_recovery.*, rebuilt_dynamic_core_periphery_model.tex,
and the " - Copy.txt" duplicates) moved to paper/archive/ (nothing deleted). Review .md notes kept
in paper/.
