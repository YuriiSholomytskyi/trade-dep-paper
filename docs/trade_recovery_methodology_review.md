# Referee Review: *The Consumer of Last Resort: External Demand and Crisis Recovery*

## Overall assessment

The paper contains a potentially publishable empirical finding, but the current version has several internal contradictions and methodological claims that would attract immediate referee criticism. The most serious issues are not stylistic. They concern the consistency of the reported results, identification, inference, censoring, and the interpretation of the theoretical model.

The most defensible result is narrower than the paper currently claims:

> Among the selected sample of program-exposed emerging and developing economies, downturn episodes in countries with greater predetermined export exposure to the United States tend to be shorter when US growth is stronger.

This is an interesting result. At present, however, the paper does not establish that:

- US demand causally shortens recovery;
- external demand is the principal determinant of recovery;
- openness prolongs contractions;
- China is a destabilizing supply-side partner;
- the United States provides “insurance” while China does not;
- official financing and external-demand anchors are complements; or
- an import-light US expansion would necessarily raise the expected cost of future downturns.

Those interpretations go beyond the design.

---

## I. Critical numerical and internal inconsistencies

These issues should be corrected before the paper is circulated.

### 1. The trade-openness claim contradicts Table 4

The text states that generic trade openness enters the contraction regression positively and significantly, implying that more open economies experience longer contractions. Table 4 reports:

- contraction coefficient: **1.10**, with \(t=1.2\);
- depth coefficient: **0.31**, with \(t=0.2\); and
- full-cycle coefficient: **0.60**, with \(t=0.3\).

None of these estimates is statistically significant. The paper therefore cannot conclude that openness prolongs contractions or deepens downturns.

The appropriate conclusion is:

> Trade openness has no statistically detectable association with downturn depth or duration in the baseline specification.

This correction is required in the abstract, Introduction, Results, and Conclusion. It also removes the proposed empirical contrast in which openness amplifies the initial shock while partner demand supports the recovery.

### 2. The China results are described incorrectly

The Results section describes the China-demand term as “correctly signed but insignificant.” Table 4 instead reports:

- depth: \(+2.25\), with \(t=3.6\);
- climb: \(+2.57\), with \(t=3.6\); and
- full cycle: \(+1.86\), with \(t=2.1\).

In the reported baseline specification, China exposure is therefore associated with deeper downturns and longer recoveries, and the estimates are statistically significant. If stronger foreign demand is expected to reduce duration, the duration coefficients are also not “correctly signed.”

A defensible description is:

> The baseline China term is positively associated with downturn depth and recovery duration. The depth association appears concentrated among commodity exporters, although the paper does not establish that the duration associations have the same explanation.

Table 5 decomposes only the depth result. It cannot explain the significant China coefficients for climb and full-cycle duration. Comparable interaction regressions are needed for the duration outcomes.

### 3. The number of episodes is inconsistent

The main text and most regression tables report **263 episodes**, while Table 11 is titled “245 output-gap episodes across 34 economies.” The body of Table 11 then states “109 of 263.” This is a direct inconsistency and probably reflects an obsolete number from an earlier data build.

### 4. The portfolio counterfactual narrative contradicts Table 6

The text states that reallocating the China share toward the hub gives a modest saving for the US-linked bloc and no saving for the Europe-linked bloc. Table 6 reports a median of **\(-0.4\) months** for EU-hub economies. The narrative and table therefore disagree.

### 5. Baseline coefficients differ across tables

Table 4 reports a US full-cycle coefficient of approximately \(-5.59\), while Table 14 labels \(-5.3\) as the baseline. Small differences can arise from changes in samples or controls, but a table presented as a timing comparison should reproduce the same baseline sample and specification. Otherwise the difference must be explained explicitly.

### 6. The definition of depth is incorrect or ambiguous

The appendix defines depth as the “largest negative value” of the output gap. Table 11 reports depth as a positive variable, with a mean of 8.1, minimum of 2.0, and maximum of 55.4. The variable is evidently the absolute magnitude of the minimum gap.

Use:

> Depth is the absolute value of the minimum output gap observed during the episode.

Otherwise the signs of the coefficients cannot be interpreted consistently.

---

## II. Identification

Identification is the paper's main methodological weakness.

### 1. The baseline is not a causal shift-share design

The partner-growth measure covers the peak year and the following two years. The dependent variable is the duration of a recovery occurring during substantially the same period. Although the paper acknowledges this overlap, it repeatedly uses causal language such as “effect,” “drives,” “pulls,” “identifies,” and “shortens.”

Predetermined export shares do not make subsequent partner growth exogenous to domestic recovery. Partner growth may reflect:

- the global business cycle;
- commodity cycles;
- global financial conditions;
- US monetary policy;
- pandemic and crisis dynamics;
- regional shocks; and
- synchronized confidence or capital-flow shocks.

The baseline estimate should therefore be interpreted as a conditional association, not as a causal effect.

Recommended language:

> A one-percentage-point increase in the export-share-weighted US growth contribution is associated with a full negative cycle approximately 5.6 months shorter.

The verb “shortens” should be reserved for a design that provides stronger causal identification.

### 2. Decomposition by partner type does not solve the global-factor problem

The paper argues that a common global factor should raise all advanced-economy terms similarly, whereas only the US term carries the effect. This is insufficient. US growth may be a better proxy for the global cycle than growth in the other-advanced aggregate. The partner components also differ in volatility, measurement error, concentration of exposure, timing, and covariance with commodity and financial cycles.

The significance of the US coefficient and insignificance of another coefficient do not establish that the coefficients differ. The paper should report formal tests such as:

\[
H_0:\beta_{US}=\beta_{OA}.
\]

It should also compare standardized effects and consider controls for:

- world growth excluding the United States;
- global trade volume growth;
- global financial conditions;
- commodity prices;
- regional growth; and
- common episode-onset effects, where feasible.

### 3. Crisis-year growth is not necessarily predetermined

Table 14 describes growth in the peak calendar year as predetermined relative to recovery. This is generally false when the downturn begins during the year. If an episode begins in February, realized annual partner growth includes ten months after the downturn begins and potentially much of the recovery.

A genuinely predetermined measure would use one of the following:

- partner growth realized strictly before the peak month;
- a forecast vintage dated before the peak;
- partner growth over the preceding 12 months;
- high-frequency growth known at the episode onset; or
- forecast revisions or external shocks dated after the peak but measured independently of domestic recovery.

The pre-sample estimate in Table 14 is only marginally significant, with \(t=-1.5\). This is an important qualification rather than a secondary robustness result.

### 4. The contraction regression does not eliminate simultaneity

The paper states that contraction duration precedes the partner-growth window. It does not. The partner-growth window begins in the peak year, and contraction duration also begins at the peak. At least part of the regressor and outcome are contemporaneous.

The contraction specification is less mechanically connected to a full three-year recovery interval, but it is not a clean pre-treatment test.

### 5. The randomization exercise does not establish causality

Permuting US export shares shows that the observed matching of shares to countries is unusual relative to arbitrary reassignments. This is a useful diagnostic of exposure structure. It does not establish that US demand causes recovery because actual US exposure may be correlated with:

- geography;
- supply-chain integration;
- institutions;
- exchange-rate regimes;
- remittance links;
- sector composition;
- tourism dependence;
- access to US financing; and
- migration patterns.

The placebo distribution being centered away from zero is itself evidence that the US shifter contains a common-cycle component.

Replace:

> The actual structure therefore identifies the effect.

with:

> The result indicates that the estimate depends on the observed allocation of US export exposure rather than merely on the common variation in US growth.

---

## III. Inference in the shift-share design

Country-clustered standard errors and a wild-cluster bootstrap address within-country dependence and the small number of country clusters. They do not necessarily address dependence induced by common shifters.

This matters because:

- the same US growth realization enters many episodes;
- multiple episodes use overlapping three-year shifter windows;
- episodes within one country repeatedly use similar export shares;
- partner-group shifters are common across many observations; and
- the number of effectively independent aggregate shocks may be small.

At least one of the following should be implemented:

1. Exposure-robust or shift-share-robust inference based on the partner shifters.
2. Shock-level regression or inference at the partner-year level.
3. Multiway clustering that recognizes country dependence and common onset-year or shifter dependence, with its limitations clearly stated.
4. Randomization inference that randomizes valid shifters under an explicit null, rather than only reallocating country shares.
5. Reporting of exposure concentration and the effective number of independent shifters.

The paper should explicitly state whether identification is claimed from exogenous shifts or from exogenous shares. At present it invokes elements of both approaches without stating the assumptions required for either.

---

## IV. Duration outcomes and censoring

Full-cycle and climb durations are capped at 60 months. These are censored time-to-event outcomes. Treating every observation at 60 months as if recovery occurred exactly in month 60 generally does not estimate the uncensored conditional mean duration.

Minimum corrections:

- report the number and percentage of episodes censored at 60 months;
- report Kaplan-Meier or cumulative recovery curves by exposure group;
- estimate a Cox model, accelerated failure-time model, or discrete-time hazard model;
- treat recovery as the event and unresolved spells as right-censored;
- adjust inference for repeated country episodes;
- compare the sign and significance with the linear duration regressions; and
- show whether late-sample episodes have enough future observations to permit a complete 60-month recovery.

There is also a possible mismatch among the paper's outcome descriptions:

- end of the negative-gap spell;
- recovery of the prior activity peak;
- peak to recovery; and
- peak to peak.

Crossing a zero output gap is not the same as regaining the previous level of activity. The event should be defined mathematically and described consistently throughout.

---

## V. Episode construction and HP-filter concerns

### 1. Mechanical dependence among episode selection, depth, and duration

Episode selection, downturn depth, and duration are all constructed from the same filtered activity series. Consequently:

- deeper gaps mechanically tend to take longer to cross zero;
- the filter determines both the episode boundaries and measured depth;
- controlling for depth conditions on a variable jointly generated with duration; and
- if external demand affects depth, depth may be a mediator rather than a conventional control.

The no-depth specification is therefore important and should appear in a table rather than only in the text.

### 2. Two-sided HP filtering uses future information

The two-sided HP gap at a given month depends on future observations and can revise the timing and depth of historical downturns. The one-sided robustness check is useful, but the paper should document:

- the monthly smoothing parameter;
- minimum series length;
- treatment of missing values;
- endpoint trimming;
- whether trends are estimated separately over differing country samples; and
- whether sample extension changes earlier episode classifications.

Alternative filters should be treated as genuine robustness checks, not only as confirmation of the preferred dating rule.

### 3. Episode proliferation creates unequal empirical weight

The number of episodes differs sharply by country. Costa Rica contributes 29 episodes, whereas Mexico contributes three and Chile one. Countries with many episodes therefore receive more weight in the point estimate even though standard errors are clustered by country.

Recommended checks:

- equal-country-weight regressions;
- country-level aggregation;
- inverse-number-of-episodes weighting;
- exclusion of countries with unusually many episodes;
- a histogram of episodes per country; and
- country fixed effects, if the specification permits them.

A leave-one-country-out exercise does not fully address systematic weighting by countries with many episodes.

---

## VI. Sample selection and official-support interpretation

The sample consists of countries that had an IMF arrangement at some point between 2005 and 2025. This conditions on a policy and financing outcome related to macroeconomic vulnerability, institutions, market access, crisis severity, geopolitics, and willingness to request Fund support. The estimates therefore do not automatically generalize to emerging and developing economies as a whole.

The active-arrangement indicator is also not an adequate control for “official support.” It does not capture:

- program size;
- actual disbursements;
- timing;
- conditionality;
- precautionary versus drawing status;
- other multilateral support; and
- endogeneity of program approval to severity and expected recovery.

It is correct to say that the regressions condition on an active-arrangement indicator. It is too broad to say that they condition on “the official support in place.”

The claim that official financing and external demand are complements is plausible but not estimated. Establishing complementarity would require an interaction between external demand and a credibly identified measure of program support.

A safer statement is:

> The results motivate examining whether official financing is particularly valuable when external demand is weak.

---

## VII. Static theoretical model

### 1. Incorrect statement about relative volatility

The paper states that the core must satisfy \(\sigma_\mu<\sigma_\varepsilon\), otherwise exposure raises variance rather than reducing it. This is incorrect under the paper's zero-covariance assumption.

With

\[
V(s)=(1-s)^2\sigma_\varepsilon^2+s^2\sigma_\mu^2,
\]

we have

\[
V'(s)=2\left[s(\sigma_\varepsilon^2+\sigma_\mu^2)-\sigma_\varepsilon^2\right].
\]

At \(s=0\),

\[
V'(0)=-2\sigma_\varepsilon^2<0,
\]

regardless of whether \(\sigma_\mu\) exceeds \(\sigma_\varepsilon\). Even a more volatile but uncorrelated second income source initially provides diversification. The condition \(\sigma_\mu<\sigma_\varepsilon\) implies only that the variance-minimizing share \(s^\star\) exceeds one-half.

Correct text:

> With zero covariance, a marginal increase in exposure from zero lowers variance for any finite \(\sigma_\mu^2\). A relatively stable core raises the variance-minimizing exposure share and increases the potential diversification gain.

### 2. The covariance condition is overstated

With covariance \(c\),

\[
V(s)=(1-s)^2\sigma_\varepsilon^2+s^2\sigma_\mu^2+2s(1-s)c.
\]

At \(s=0\),

\[
V'(0)=2(c-\sigma_\varepsilon^2).
\]

A marginal increase in exposure still lowers variance whenever \(c<\sigma_\varepsilon^2\). Positive correlation does not automatically eliminate diversification.

### 3. The economic interpretation of \(s\) is problematic

The equation

\[
y_i=(1-s_i)\varepsilon_i+s_i\mu
\]

treats output as a convex portfolio of a domestic shock and foreign demand. If \(s_i\) is the export share of output, increasing exports mechanically reduces the loading on the domestic shock from one to \(1-s_i\). This is not an accounting identity. Domestic value added remains exposed to productivity, financial, fiscal, and supply shocks.

The equation is better presented as a reduced-form income-exposure representation. Alternatively, derive it from a transparent decomposition such as

\[
y_i=d_i+x_i, \qquad x_i=s_i\mu,
\]

with an explicit relationship between domestic-demand variance and export orientation.

### 4. “Insurance” is stronger than the model supports

The model studies unconditional output variance. It does not model recovery duration, downside risk, state-contingent insurance, or partner demand specifically during domestic recessions.

The relevant object for the paper's empirical argument is closer to

\[
E[\mu_t\mid \varepsilon_{it}<0]
\]

or a downturn-state covariance, not only \(\operatorname{Var}(\mu)\). The static model explains unconditional diversification, while the empirical analysis studies duration conditional on entering a downturn. The conceptual link should be made explicit or the insurance language should be narrowed.

### 5. The calibration is illustrative, not evidentiary

The reported maximum variance reduction follows from the chosen values \(\sigma_\varepsilon=5\) and \(\sigma_\mu=2\). Unless these parameters and the distribution of exposure are tied transparently to empirical moments, the resulting magnitudes should be labeled numerical illustrations rather than quantitative implications.

---

## VIII. Dynamic model

The dynamic model largely embeds the desired conclusions by construction:

- import demand contains \(-\theta\hat\iota_t\);
- consumption contains \(-\psi\hat\iota_t\); and
- periphery output contains \((1+\kappa\theta)\), which directly makes domestic shocks larger when \(\theta\) is high.

The result that an import-light boom reduces imports and worsens periphery outcomes therefore follows from imposed signs rather than from a deeper equilibrium mechanism.

Additional concerns:

1. The real-rate equation is not a standard monetary-policy rule because inflation is absent.
2. Consumption is forward-looking, but no household budget constraint or transversality condition is reported.
3. Output is a weighted sum of consumption and import-light activity without a production or goods-market foundation.
4. The belief shock and sector-activity equation do not identify a technology or welfare mechanism.
5. The buffering-loss term duplicates the conclusion to be demonstrated.
6. Comparing US expansions “of the same magnitude” requires a precise normalization of the output paths or shocks.
7. Calibration targets and sensitivity analysis are not provided.

The section should be presented as a stylized numerical illustration rather than a structural dynamic core-periphery model. A simpler accounting model of US absorption, import intensity, and foreign exports may serve the paper better.

---

## IX. Economic assessments that should be narrowed

### 1. “China is a producer, not a consumer”

This claim is too broad. The paper supports the narrower statement that export exposure to China is limited in this sample and only Mongolia is classified as China-hubbed under the paper's assignment rule. It does not establish that China generally fails to provide external demand.

### 2. Weak correlation is interpreted inconsistently

The scenario discussion treats weak correlation between China's import demand and other countries' downturns as a disadvantage. In the static model, weak or zero correlation is what creates diversification benefits.

If the intended claim is that China does not increase imports when partners enter downturns, the relevant concept is lack of countercyclicality, not weak unconditional correlation.

### 3. “Insurance comes only from consumers” is false

Recovery and risk sharing can also operate through:

- imported-input prices;
- capital and credit flows;
- remittances;
- tourism;
- supply-chain continuity;
- technology diffusion;
- official financing; and
- commodity prices.

The paper estimates one export-demand channel. It should not define all other channels out of the concept of insurance.

### 4. Supply links need not amplify downturns

Greater imports from China may transmit shocks, but they may also lower production costs, relax input constraints, increase real household income, support domestic production, and reduce inflation. The paper does not estimate the net effect of import sourcing from China. Claims that supply-side China exposure amplifies downturns should therefore be removed unless directly tested.

### 5. The import-light US scenario is not empirically validated

The regressions use US GDP or industrial-production growth interacted with export shares. They do not estimate how different components of US growth affect partner recovery. The paper does not establish that recent US growth is becoming import-light, that AI, reshoring, or defense spending reduces aggregate US imports, or the likely size of the foreign spillover.

Section VII should be presented explicitly as a hypothetical mechanism motivated by, but not estimated in, the paper.

---

## X. Local projections

The LP regressor is US industrial-production growth multiplied by each country's US export share. This is an exposure measure, not automatically a structural US-demand shock.

Potential confounders include:

- global manufacturing growth;
- commodity demand;
- synchronized industrial cycles;
- US monetary and financial conditions;
- exchange-rate movements; and
- changes in global inventories.

Recommended robustness checks:

- use a residualized US industrial-production innovation;
- control for world industrial production excluding the United States;
- control for global trade growth and commodity prices;
- control for US monetary and financial shocks;
- use alternative US import-demand measures;
- report leads or pre-trend coefficients;
- use exposure-robust inference; and
- formally test equality of the recession and normal-state responses.

The LP results support positive transmission of US activity. They do not by themselves show that US demand accelerates the exit from recession. A recovery-hazard specification would address that question more directly.

---

## XI. Recommended central claim

A credible revised framing is:

> Using 263 downturn episodes across 34 economies with a history of IMF arrangements, the paper documents that stronger growth in a country's pre-downturn export markets is associated with shorter downturn duration. The association is strongest for US-oriented economies and remains under alternative episode definitions and timing measures. Because the partner-growth windows overlap recovery, common aggregate shocks may affect the estimates, and the effective number of shifters is limited, the results are interpreted as robust descriptive evidence of an external-demand channel rather than a causal estimate.

This remains a worthwhile contribution.

---

## XII. Priority revisions

### Must fix

1. Reconcile 245 versus 263 episodes.
2. Correct all claims concerning trade openness.
3. Correct the description of the China coefficients.
4. Reconcile Table 6 with its narrative.
5. Reconcile baseline coefficients across tables.
6. Correct the definition of downturn depth.
7. Fix the theoretical statements about relative volatility and covariance.
8. Replace causal language with association language.
9. Treat 60-month observations as censored.
10. Add shift-share-appropriate inference.
11. Stop calling peak-year growth predetermined unless it is measured before the peak month.
12. Separate the empirically supported result from the hypothetical import-light US scenario.

### Strongly recommended

13. Add onset measures or forecast-vintage shocks that are genuinely predetermined.
14. Add global and regional cycle controls.
15. Report equal-country-weight and episode-weighted estimates.
16. Estimate recovery hazards.
17. Formally test the equality of US and other-advanced coefficients.
18. Report standardized effects and effects of realistic interquartile changes.
19. Recast the dynamic model as an illustrative accounting exercise.
20. Narrow claims concerning China, supply-side exposure, and official financing.

---

## Final assessment

The empirical pattern is interesting and sufficiently strong to justify further work. The current paper, however, presents a descriptive exposure association as a structural demand and insurance mechanism. Correcting the inconsistencies between the text and tables, adopting inference appropriate for common shift-share shifters, handling censored durations correctly, fixing the mathematical claims in the static model, and narrowing the economic interpretation would make the paper substantially more credible.
