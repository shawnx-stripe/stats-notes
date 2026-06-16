---
title: Placebo Test
aliases:
- placebo
- in-space placebo
- in-time placebo
- negative control test
- placebo outcomes
tags:
- causal-inference
- diagnostics
- robustness
- did
- rdd
- iv
- synthetic-control
- permutation
updated: 2025-09-17
---

# Placebo Test

> [!summary] Quick definition
> A placebo test is a falsification exercise that repeats the analysis in a situation where no effect is expected (e.g., on a placebo outcome, at a placebo date, or for placebo “treated” units). Finding no effect increases credibility; finding an effect warns of misspecification or violated assumptions.

- Use alongside design diagnostics (e.g., [[pre-trends]] for DiD).
- Placebos are suggestive, not proofs; interpret with care and consider multiple-testing issues.

## Why use placebos?

- Probe key identification assumptions (e.g., [[parallel trends assumption]], no direct [[exclusion restriction]] channels, continuity at RD cutoff).
- Detect spurious associations from trends, seasonality, model misspecification, or [[composition]] changes.
- Assess specificity: effects should appear when and where they should, and not elsewhere.

## Common types of placebo tests

### 1) Placebo timing (in-time)
- Assign a fake treatment date in the pre-period and re-estimate.
- Expect no post-minus-pre effect around the placebo date if trends are well controlled and no [[Anticipatory effects]].

### 2) Placebo units (in-space)
- Assign “treatment” to units that were never treated (or to donor units), holding everything else fixed.
- Used heavily in [[Synthetic Control]]: permutation tests compare the treated unit’s gap to gaps when each donor is treated in turn.

### 3) Placebo outcomes (negative control outcomes)
- Analyze outcomes that should not be affected by treatment (e.g., mortality for a policy plausibly affecting only prices).
- Evidence of an effect on placebo outcomes suggests residual confounding or spillovers.

### 4) Placebo exposures (negative control exposures)
- Use a variable known not to affect the outcome in place of treatment; should yield null results.

### 5) Placebo cutoffs (RDD)
- Estimate RD at fake thresholds where no policy changes occur.
- Expect no discontinuity in the outcome at non-policy cutoffs; also test continuity of predetermined covariates at the true cutoff.

### 6) Instrument placebos (IV)
- Check that the instrument has no effect on outcomes that it should not affect (placebo outcomes), or in pre-periods before the endogenous regressor could change.

> [!warning] Contamination
> Placebo units/dates may still be indirectly affected (e.g., via [[spillovers]]/[[interference]] or early announcements). Interpret “false positives” in light of such channels.

## Interpreting placebo tests

- Passing a placebo test (null effect) supports the design but does not prove validity.
- Failing a placebo test signals potential violations (e.g., non-parallel trends, seasonality, direct effects of instrument).
- Adjust expectations for power: small samples or noisy outcomes may fail to detect spurious effects.
- Multiple testing: control false discoveries (pre-register placebos, use joint tests, or adjust p-values).

## Placebo tests by design

### Difference-in-Differences (DiD)
- In-time: fake treatment date in the pre-period.
- Leads in [[event study]] are a built-in placebo (pre-treatment coefficients ≈ 0).
- Placebo outcomes not expected to respond to policy.

### Synthetic Control
- In-space permutation: treat each donor as if treated; compare post/pre RMSPE-adjusted gaps.
- In-time placebo date for the treated unit.

### Regression Discontinuity (RDD)
- Placebo cutoffs away from the true cutoff.
- Placebo on predetermined covariates (continuity checks).
- “Donut” RD (exclude near-cutoff data) as a robustness variant.

### Instrumental Variables (IV)
- Placebo outcomes and pre-periods; the instrument should not move those.
- Event-time alignment: no reduced-form effect of Z before treatment can respond.

## Minimal code snippets

> [!example] R: DiD placebo date (fixest)

```r
library(fixest)

# Suppose policy_date is the true adoption time; define a placebo date in pre-period
df$Post_placebo <- as.integer(df$time >= (df$policy_date - 2))  # shift earlier by 2 periods
placebo_est <- feols(Y ~ TreatedEver:Post_placebo | id + time, cluster = ~id, data = df)
etable(placebo_est)
# Expect the coefficient on TreatedEver:Post_placebo ~ 0
```

> [!example] R: Synthetic Control in-space placebos (Synth)

```r
library(Synth)
# Fit SCM for treated unit, then loop over donors as placebo-treated
# Compare post/pre RMSPE ratios to form permutation distribution.
```

> [!example] R: RD placebo cutoffs (rdrobust)

```r
library(rdrobust)
c_true <- c0
# Grid of placebo cutoffs away from c0
for (cc in seq(c0 - 10, c0 + 10, by = 2)) {
  if (cc == c_true) next
  fit <- rdrobust(y = df$Y, x = df$X, c = cc)
  # Store estimates to form a null distribution
}
```

> [!example] Stata: DiD placebo date

```stata
* Placebo post in pre-period
gen Post_placebo = time >= policy_date - 2
reghdfe Y c.Post_placebo##i.TreatedEver, absorb(id time) vce(cluster id)
```

> [!example] Stata: Synthetic Control in-space placebos

```stata
* ssc install synth
* Loop over donor units, treating each as if treated; collect RMSPE ratios
```

> [!example] Python: DiD placebo (linearmodels)

```python
from linearmodels.panel import PanelOLS
df = df.set_index(['id','time'])
df['Post_placebo'] = (df['time'] >= (df['policy_date'] - 2)).astype(int)
df['D_placebo'] = df['TreatedEver'] * df['Post_placebo']

mod = PanelOLS.from_formula('Y ~ 1 + TreatedEver + Post_placebo + D_placebo + EntityEffects + TimeEffects',
                            data=df)
res = mod.fit(cov_type='clustered', cluster_entity=True)
print(res)
```

## Permutation and placebo p-values

- For permutation-based placebos (e.g., Synthetic Control in-space), form a test statistic T (e.g., post/pre RMSPE ratio or average post gap) for the treated unit and for each placebo unit.
- Two-sided permutation p-value (copy-ready):
$$
p = \frac{1 + \sum_{b=1}^{B} \mathbf{1}\big(|T_b^\ast| \ge |T_{\text{obs}}|\big)}{B + 1}.
$$

## Good practice

> [!check] Checklist
> - [ ] Pre-register placebo tests and outcomes to avoid fishing.
> - [ ] Use joint tests (e.g., all pre-treatment leads) rather than many single tests.
> - [ ] Report effect sizes with CIs, not just p-values.
> - [ ] For Synthetic Control, report pre-fit (RMSPE), gap plots, and placebo distributions (possibly RMSPE-scaled).
> - [ ] Ensure placebo units/dates are plausibly unaffected (watch for [[spillovers]]/[[Anticipatory effects]]).

> [!tip] Power and multiplicity
> - Low power is common; interpret nulls cautiously.
> - Control for multiple comparisons (Bonferroni/Holm) or rely on pre-specification to limit tests.

## Common pitfalls

> [!warning] Avoid these
> - Declaring validity based solely on “no significant placebos” with tiny samples.
> - Ignoring that placebo settings may still be indirectly exposed.
> - Mixing specification changes between main and placebo analyses.
> - Overinterpreting single placebo that “fails” among many (multiple-testing).

## Copy-ready definitions

- Placebo (in-time): assign a fake treatment date in pre-period and re-estimate.
- Placebo (in-space): assign “treatment” to untreated units and recompute the estimator.
- Negative control outcome: an outcome Y_nc that should not respond to treatment; test effect ≈ 0.
- Permutation p-value:
$$
p = \frac{1 + \#\{|T_b^\ast| \ge |T_{\text{obs}}|\}}{B + 1}.
$$

---

## Related notes
- [[Difference-in-Differences (DiD)]]
- [[event study]]
- [[pre-trends]]
- [[parallel trends assumption]]
- [[Synthetic Control]]
- [[Regression Discontinuity Design (RDD)]]
- [[Instrumental Variables (IV)]]
- [[exclusion restriction]]
- [[Anticipatory effects]]
- [[spillovers]]
- [[interference]]
- [[composition]]
- [[bad controls]]
- [[robustness checks]]
- [[randomization inference|permutation test]]
- [[randomization inference]]
- [[RMSPE]]
- [[Conley standard errors]]
