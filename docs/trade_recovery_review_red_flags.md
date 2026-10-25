# Review of *The Consumer of Last Resort: External Demand and Crisis Recovery*

## Overall assessment

The paper has a strong central idea and unusually clear narrative, but in its current form I would expect a demanding referee to recommend **major revision**, primarily because several causal and quantitative claims are materially stronger than the design supports.

## Highest-priority red flags

### 1. Critical algebraic sign error in the core theoretical result

The paper defines

\[
s_i(q)=w_i(1-q),
\]

so

\[
\frac{\partial s_i}{\partial q}=-w_i.
\]

Therefore,

\[
\frac{\partial \operatorname{Var}(y_i)}{\partial q}
=
-w_i\frac{\partial \operatorname{Var}(y_i)}{\partial s_i},
\]

not

\[
w_i\frac{\partial \operatorname{Var}(y_i)}{\partial s_i}
\]

as written in Corollary 1. Below \(s^*\), \(\partial\operatorname{Var}(y_i)/\partial s_i<0\), so the **correct expression is positive precisely because of the missing minus sign**. The verbal conclusion may survive, but the displayed derivation is wrong at the central point of the model. This must be corrected before circulation.

### 2. “Shift-share instrument” is not actually being used as an instrument

The paper repeatedly calls the demand measure a “shift-share (Bartik) instrument,” but the empirical specification appears to put the shift-share variable directly into the outcome regression. There is no endogenous regressor being instrumented, no first stage, and no exclusion restriction.

Call it a **shift-share exposure measure** or **Bartik-style regressor**, unless an actual IV design is introduced. Otherwise, informed readers will immediately question the terminology and identification claim.

### 3. The baseline recovery regression is mechanically contaminated by future outcomes

The baseline treatment averages partner growth from the peak year through peak \(+2\), while the dependent variable is the time from the peak until recovery. Thus, partner growth is measured partly **during the recovery it is supposed to explain**.

The paper recognizes this, but then continues to state headline results causally, using terms such as external demand “drives,” “shortens,” “rescues,” and “pulls” economies out. The baseline identifies a conditional association, not a causal duration effect.

More seriously, the purported timing solutions are not as clean as claimed:

- The contraction begins at the peak and therefore overlaps the peak-year growth observation.
- “Crisis-year only” partner growth is contemporaneous with a monthly contraction occurring within that year.
- Annual partner GDP growth cannot generally be described as predetermined relative to a within-year monthly recovery outcome.

Neither result should be called “free of the overlap concern.” Use lagged or forecast partner demand known at the episode peak, or instrument realized partner import demand with genuinely external shocks.

### 4. The US variable is not an identified US-demand shock

The local-projection impulse is twelve-month US industrial-production growth multiplied by each country’s US export share. US industrial production is not a structural US import-demand shock. It can reflect:

- global demand;
- global manufacturing and commodity cycles;
- supply shocks;
- common financial conditions;
- demand originating outside the US;
- inventory and trade-cycle effects.

Multiplying an endogenous global variable by predetermined exposure does not make the shift exogenous. The local projections establish heterogeneous comovement with US industrial production, not necessarily transmission of exogenous US consumer demand.

A stronger design would use a measure closer to the mechanism, such as US real import absorption by product, ideally purged of exporter supply and global demand components.

### 5. Standard errors do not appear to address common time shocks

The paper clusters by country. But the “shifts” are common hub-growth observations, often shared by many countries and episodes. Errors can therefore be correlated across countries experiencing downturns in the same year or global episode.

Country clustering alone is unlikely to be sufficient. At minimum, show:

- two-way clustering by country and episode peak year;
- year or global-cycle fixed effects;
- shock-level inference;
- a leave-one-period-out construction;
- inference that recognizes the limited number of independent US growth shocks.

The permutation exercise reallocates exposure across countries but does not solve common-time-shock inference. Indeed, the placebo distribution being centered around approximately \(-1.7\), rather than zero, is direct evidence that US growth carries a common-cycle component.

### 6. US exposure may proxy persistent regional differences

The US-exposed group is geographically concentrated in Latin America and the Caribbean, while the EU-exposed group contains emerging Europe and a diverse set of other economies. Export shares can correlate with:

- geography;
- institutions;
- dollarization;
- remittances;
- tourism;
- commodity structure;
- exchange-rate regimes;
- synchronization with US financial conditions;
- data quality;
- crisis type.

The permutation test shows that the actual exposure allocation matters. It does **not** show that trade demand, rather than correlated characteristics of the US-linked countries, is the mechanism.

Country fixed effects, partner-specific trends, region-by-year effects, or a more granular product-level shift-share structure would help.

### 7. IMF arrangement control does not justify “over and above official support”

A binary indicator for an active arrangement cannot “absorb the financing and policy anchor” supplied by IMF-supported programs. Program participation is endogenous to crisis severity, financing needs, policy actions, and expected recovery. Programs also vary enormously in size, timing, conditionality, reviews, disbursements, and implementation.

The paper can say the relationship is estimated **conditional on an active-arrangement indicator**. It cannot safely say that the demand effect is measured “over and above official support.”

### 8. Duration outcomes need a duration model

The principal outcomes are months to trough and months to recovery, with durations censored at 60 months. They are nonnegative, discrete, skewed, and censored. Yet the tables appear to report linear regressions.

That creates obvious concerns:

- predicted negative durations;
- incorrect treatment of censoring;
- nonconstant variance;
- duration dependence;
- repeated episodes per country;
- competing definitions of recovery.

A survival specification should be central, not optional:

- Cox or accelerated-failure-time model;
- discrete-time hazard model;
- shared country frailty;
- explicit right-censoring;
- recurrent-event treatment.

The linear model can remain as an interpretable robustness check.

### 9. The two-sided HP filter mechanically uses future information

Episodes, peaks, troughs, gaps, and recovery dates are constructed from a two-sided HP filter. That means future observations help determine whether an earlier month was below trend and when the recovery occurred. This is especially problematic because the paper makes timing and policy-assessment claims.

The one-sided robustness is useful, but it produces only 199 rather than 245 episodes. The paper needs to explain:

- why 46 episodes disappear;
- whether the country composition changes;
- whether episode timing changes materially;
- whether the same events are being compared;
- sensitivity to alternative recession-dating methods.

### 10. Selection into the sample is potentially consequential

The sample frame consists of countries that received an IMF arrangement at some point during 2005-2025, followed by availability of monthly activity data and occurrence of a qualifying HP-gap episode. This conditions on:

1. eventual program participation;
2. data availability;
3. crisis realization;
4. survival of the dating algorithm.

The result is 245 algorithmic episodes but only 34 countries, with very uneven episode counts. The estimand may therefore be dominated by frequently cycling or particularly well-measured economies.

The paper needs episode-weight diagnostics, country-equal-weight estimates, and a table showing how each sample restriction changes composition.

## Major interpretation problems

### 11. The China conclusion exceeds what the sample can establish

Only Mongolia is classified as China-hub, and the paper explicitly says an export-side China hub cannot be estimated. That is a power and support limitation, not evidence that China cannot provide recovery demand.

The defensible conclusion is:

> In this IMF-program-selected sample and historical episode structure, exposure to Chinese demand is too limited to estimate a China-hub recovery effect precisely.

The stronger statements that China “buys too little,” “provides no insurance,” or cannot substitute as a consumer are not established by this sample. The insignificant China recovery coefficient is especially uninformative when median export exposure is below 0.5 percent.

### 12. Table 1 does not establish that deglobalization losses failed to materialize

Table 1 indexes the nominal value of imports plus exports. The 2020-2025 period includes major commodity-price movements, inflation, exchange-rate changes, freight-cost shocks, and pandemic base effects. A higher nominal trade index does not demonstrate greater real integration or refute welfare losses from fragmentation.

The claim that projected losses for poorer economies “have not materialised” is particularly problematic. Scenario losses are counterfactual differences relative to a no-fragmentation path, not predictions that nominal trade must fall below its 2017-2019 level.

Separate:

- nominal trade value;
- real trade volume;
- trade intensity relative to GDP;
- bilateral reallocation;
- welfare or output relative to a counterfactual.

### 13. The “insurance quality” statistic is ad hoc

Table 2 defines quality as mean import-demand growth divided by its standard deviation. But the theoretical discussion says insurance depends on both volatility and covariance with the client’s domestic shock. The table omits the covariance that the model says is essential.

It also compares aggregate hubs using only 2010-2024 observations, excluding 2020, without uncertainty intervals. The ranking could be highly period-sensitive. The statistic should either be presented as a descriptive growth-volatility ratio or replaced with a measure of import-demand performance specifically during partners’ downturns.

### 14. “Calibrated DSGE” materially overstates the model

The dynamic model is a small linear gap system with several imposed reduced-form relationships. In particular:

- the shock process is called a “belief about payoff” without an optimization problem;
- consumption is crowded out directly by import-light activity;
- import demand falls mechanically with the activity term;
- the periphery equation contains an imposed \((1+\kappa q)\) buffering-loss multiplier;
- no household budget constraint, resource constraint, trade-pricing block, market clearing, or welfare criterion is shown;
- determinacy and solution conditions are not reported.

Calling this a **stylized dynamic core-periphery model** would be credible. Calling it a calibrated DSGE invites scrutiny that the current model will not withstand. Figure 4 demonstrates properties built into the equations rather than independently generated economic mechanisms.

### 15. Several calibration claims are not documented

The text says the periphery export exposure equals the sample median, but the appendix summary statistics report trade openness, not the median export share corresponding to \(\lambda=0.30\). The import-light output share of 0.45, import content of consumption of 0.50, and buffering parameter of 1.20 appear stylized rather than empirically calibrated.

That is acceptable for an illustration, but:

- label them illustrative;
- document the source or target for every parameter;
- show sensitivity over plausible ranges;
- avoid numerical welfare-like statements such as “variance rises 16 percent” unless robust.

## Internal inconsistencies and presentation red flags

### 16. Claims about openness contradict each other

The paper says:

- generic openness prolongs the contraction;
- generic openness does little for the rebound;
- openness is associated with deeper and more protracted downturns;
- openness is “neither stabilising nor destabilising.”

These are not equivalent. If openness significantly lengthens contraction, the paper should say that openness increases exposure to the initial shock but has no robust association with the subsequent climb.

### 17. Headline coefficient needs much more careful interpretation

The abstract’s “one-percentage-point rise in US-weighted partner demand shortens the downturn by roughly six months” sounds like a one-point increase in US growth. It is actually a one-point increase in the **US contribution**, roughly US export share multiplied by US growth.

For a country with a 10 percent US share, a one-point increase in the contribution would require approximately 10 percentage points more US growth. That is not a marginal or empirically common change. Report effects for:

- a one-standard-deviation change;
- an interquartile change;
- a 1 percentage point US growth shock at representative export shares.

Table 4 otherwise risks presenting a numerically dramatic but economically hard-to-interpret coefficient.

### 18. Table 4 and Table 13 appear to disagree on the baseline t-statistic

The main table reports the full-cycle US coefficient of \(-6.10\) with \(t=-3.1\), while the appendix baseline robustness table reports approximately \(-6.1\) with \(t=-3.4\). If these are genuinely the same specification, the discrepancy needs correction or explanation.

### 19. “Goods trade is a lower bound” is not demonstrated

The services section shows that adding rough services/remittance proxies does not eliminate the goods coefficient. That does not establish that the goods estimate is a lower bound. Omitted services channels could amplify or attenuate the goods coefficient depending on correlation and measurement error.

### 20. The portfolio counterfactual should not be framed as partner choice

Export destinations are equilibrium outcomes shaped by geography, specialization, trade agreements, supply chains, prices, and importer demand. Applying local regression coefficients to a five-point portfolio reallocation is an accounting exercise, as the table eventually acknowledges, but language such as “partner choice pays” sounds policy-causal.

Call this an **exposure reweighting calculation**, not a counterfactual policy experiment.

## Bottom line

The paper’s **publishable core** is narrower and stronger than its current framing:

> Among externally vulnerable emerging and developing economies, predetermined export exposure interacted with partner growth is strongly associated with shorter downturns, with the association concentrated in US-exposed economies. The result is robust to several alternative episode definitions, but causal interpretation remains limited by common global shocks, timing overlap, and endogenous trade exposure.

The immediate fixes are:

1. Correct the theoretical sign error.
2. Stop calling the regressor an instrument.
3. Recast the headline result as an association unless identification is strengthened.
4. Add common-time-shock inference and survival models.
5. Substantially narrow the China and fragmentation claims.
6. Rename the DSGE as a stylized dynamic model.
7. Reinterpret the coefficient using realistic exposure and shock changes.
8. Remove “over and above official support.”
9. Reconcile the table discrepancies.
10. Move the US import-light scenario into a clearly labeled speculative section.

The central idea is good. The main risk is not that the paper lacks a result, but that it currently **claims three results at once**: a causal recovery effect, a structural consumer-versus-producer theory, and a forward US-China scenario. The empirical design most convincingly supports only the first as a robust conditional association.
