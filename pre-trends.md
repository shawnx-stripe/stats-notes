---
title: Pre-Trends
aliases: [pretrends, pre-trend checks, pre-treatment trends]
tags: [econometrics, causal-inference, did, diagnostics, event-study]
updated: 2025-09-17
---

# Pre-Trends

> [!summary] Quick definition
> Pre-trends are the behavior of outcomes for the [[treated group]] and [[control group]] before treatment starts. In [[Difference-in-Differences (DiD)]], inspecting pre-trends helps assess the plausibility of the [[parallel trends assumption]].

- Goal: verify that treated and control groups exhibit similar outcome dynamics prior to treatment.
- Tools: visual plots, [[event study]] leads, slope-difference tests, placebo dates.

## Why pre-trends matter

- If treated and control groups have different pre-treatment dynamics, the [[DiD estimator]] may attribute existing differences to the treatment.
- Pre-trend diagnostics are not proofs, but they provide evidence for or against parallel trends.

## How to check pre-trends

### 1) Visual inspection
- Plot average outcomes by group over time, focusing on pre-period.
- Consider differences-in-levels and differences-in-changes (plot the treated minus control difference).

### 2) Event-study leads
- Estimate a relative-time model with pre-treatment leads; under no anticipation and parallel trends, pre-lead coefficients should be near zero.
- Copy-ready:
$$
Y_{it} = \alpha_i + \gamma_t + \sum_{k \ne -1} \beta_k\,\mathbf{1}\{t - G_i = k\} + \varepsilon_{it}
$$
- Inspect coefficients for k < 0.

### 3) Slope-difference tests in pre-period
- In pre-period only, regress outcome on time interacted with treated:
$$
Y_{it} = \alpha_i + \gamma_t + \delta \,(D_i \cdot t) + \varepsilon_{it} \quad \text{(pre-period only)}
$$
- Test H0: δ = 0 (equal linear pre-trend slopes). Consider adding polynomial or flexible time interactions if warranted.

### 4) Placebo treatment dates
- Assign a fake treatment date within pre-period and run DiD; significant “effects” suggest non-parallel trends or chance overfitting.

> [!warning] Power and multiple testing
> - Pre-periods are often short; tests have low power. Do not treat “not significant” as proof of parallel trends.
> - Many-leads event studies risk false positives; use joint tests and thoughtful binning.

## Good practice

> [!check] Pre-trend checklist
> - [ ] Plot group means and treated-minus-control differences in pre-period.
> - [ ] Estimate an event study with clearly labeled leads; report joint F-test that all leads are zero.
> - [ ] Consider conditional pre-trend checks (with [[covariates]] or weights).
> - [ ] Run placebo dates and alternative control groups/windows.
> - [ ] Pre-register which pre-period window and tests you’ll use.

> [!tip] Binning leads and lags
> - Bin distant relative times (e.g., k ≤ −5) to avoid noisy estimates and improve readability.

## What if pre-trends differ?

### 1) Narrow windows and refine controls
- Use a tighter pre-period where trends look stable.
- Choose more comparable controls (same region/industry), or use [[matching]]/[[entropy balancing]].

### 2) Conditional parallel trends
- Allow trends to be equal after conditioning on X:
$$
\mathbb{E}[Y_{it}(0) - Y_{i,t-1}(0) \mid D_i, X_i] \text{ equal across groups}
$$
- Implement with rich time×covariate interactions or reweighting.

### 3) Unit-specific trends (use cautiously)
- Add unit-specific linear trends to absorb differential linear drift:
$$
Y_{it} = \alpha_i + \gamma_t + \lambda_i t + \beta D_{it} + \varepsilon_{it}
$$
- Caveat: can absorb part of the treatment effect if effects evolve slowly; interpret the estimand carefully.

### 4) Alternative designs
- [[Synthetic Control]] to match the treated unit’s pre-path closely.
- [[Triple Differences (DDD)|DDD]] to difference out a third dimension.
- For [[staggered adoption]], use cohort-time ATT estimators like [[Callaway–Sant’Anna estimator]] or [[Sun–Abraham estimator]].

## Minimal code for pre-trend checks

> [!example] R: event study leads and plot (Sun–Abraham via fixest)

```r
library(fixest)
# G = first treatment time
es <- feols(Y ~ sunab(G, time) | id + time, data = df, cluster = ~id)
iplot(es)  # plot leads/lags; check pre-treatment leads (k < 0) ~ 0

# Joint F-test of all leads = 0 (names vary by version; example using wald)
coefs <- grep("^sunab::(-", names(coef(es)))  # indices of lead terms (negative k)
wald(es, keep = names(coef(es))[coefs])  # joint test that leads are zero
```

> [!example] Stata: event-study leads

```stata
* Requires eventstudyinteract (ssc install eventstudyinteract)
eventstudyinteract Y G time, cohort(G) absorb(id time) vce(cluster id)
* Inspect pre-treatment leads; test jointly equal to zero:
testparm _b[lead*]
```

> [!example] Python: linearmodels manual event-time leads

```python
from linearmodels.panel import PanelOLS
import numpy as np

df = df.set_index(['id','time'])
rel = df.index.get_level_values('time') - df['G']
for k in range(-6, 7):
    df[f'rt_{k}'] = (rel == k).astype(int)

formula = 'Y ~ 1 + ' + ' + '.join([f'rt_{k}' for k in range(-6,7) if k != -1]) + ' + EntityEffects + TimeEffects'
mod = PanelOLS.from_formula(formula, data=df)
res = mod.fit(cov_type='clustered', cluster_entity=True)
print(res)

# Joint test of pre-treatment leads (pseudo, depends on your testing util)
pre_leads = [f'rt_{k}' for k in range(-6,0) if k != -1]
# Use statsmodels' wald_test or custom routine to test coefficients jointly
```

> [!example] Pre-period slope-difference test (R)

```r
pre <- subset(df, time < first_treatment_time)  # adjust as needed
est_pre <- feols(Y ~ D:time | id + time, data = pre, cluster = ~id)
# Test H0: coefficient on D:time = 0 (equal linear pre-trend slopes)
```

## Reporting essentials

- Show pre-period plots with confidence bands.
- Report joint tests of lead coefficients and discuss power.
- Document how you chose the pre-window and controls; show robustness to alternatives.
- If using adjustments (weights, trends), explain the estimand and provide sensitivity analyses.

## Copy-ready snippets

- Event-study with leads/lags:
$$
Y_{it} = \alpha_i + \gamma_t + \sum_{k \ne -1} \beta_k\,\mathbf{1}\{t - G_i = k\} + \varepsilon_{it}
$$

- Slope-difference test (pre-period only):
$$
Y_{it} = \alpha_i + \gamma_t + \delta \,(D_i \cdot t) + \varepsilon_{it}, \quad H_0:\ \delta=0
$$

- Conditional parallel trends:
$$
\mathbb{E}[Y_{it}(0) - Y_{i,t-1}(0) \mid D_i=1, X_i] = \mathbb{E}[Y_{it}(0) - Y_{i,t-1}(0) \mid D_i=0, X_i]
$$

## Common pitfalls

> [!warning] Avoid these
> - Declaring success from “no significant difference” with tiny pre-samples.
> - Overfitting with too many leads/lags and treating individual p-values at face value.
> - Using different pre-windows across specifications after seeing the data (“peeking”).
> - Ignoring [[Anticipatory effects]] that generate real pre-period deviations.

---

## Related notes
- [[Difference-in-Differences (DiD)]]
- [[DiD estimator]]
- [[parallel trends assumption]]
- [[event study]]
- [[treated group]]
- [[control group]]
- [[staggered adoption]]
- [[Sun–Abraham estimator]]
- [[Callaway–Sant’Anna estimator]]
- [[covariates]]
- [[placebo test]]
- [[matching]]
- [[entropy balancing]]
- [[balanced panel]]
- [[Triple Differences (DDD)|DDD]]
- [[Synthetic Control]]
- [[seasonality]]
- [[Anticipatory effects]]
- [[few-cluster corrections]]