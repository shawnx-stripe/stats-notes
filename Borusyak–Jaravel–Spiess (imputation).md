---
title: Borusyak–Jaravel–Spiess (imputation)
aliases:
- BJS imputation
- imputation estimator
- Borusyak-Jaravel-Spiess
- Borusyak-Jaravel-Spiess (imputation)
tags:
- causal-inference
- did
- panel-data
updated: 2026-03-03
---

# Borusyak–Jaravel–Spiess (imputation)

> [!summary] Quick definition
> An imputation-based estimator for staggered [[Difference-in-Differences (DiD)]]. It estimates the counterfactual untreated outcome $Y_{it}(0)$ for treated observations using only untreated (pre-treatment and never-treated) data, then computes unit-time treatment effects as residuals. Avoids the negative-weighting problem of [[two-way fixed effects]] under [[treatment effect heterogeneity]].

---

## How it works

1. **Estimate the untreated model** using only observations that are not yet treated (never-treated + pre-treatment periods):
$$
Y_{it} = \alpha_i + \gamma_t + X_{it}'\delta + \varepsilon_{it} \quad \text{for } (i,t) \text{ with } D_{it}=0
$$

2. **Impute** the counterfactual for each treated observation:
$$
\hat Y_{it}(0) = \hat\alpha_i + \hat\gamma_t + X_{it}'\hat\delta
$$

3. **Compute treatment effects** as residuals:
$$
\hat\tau_{it} = Y_{it} - \hat Y_{it}(0) \quad \text{for } D_{it}=1
$$

4. **Aggregate** into a summary ATT (e.g., simple average, event-time average, cohort average) with appropriate standard errors.

> [!tip] Key advantage
> The imputation step uses only clean (untreated) variation, so it never compares a treated unit to an already-treated "control." This eliminates the contamination problem identified by [[Goodman–Bacon decomposition]].

---

## Assumptions

- [[parallel trends assumption]] (conditional on covariates and FEs)
- No [[Anticipatory effects]]
- Correct specification of the untreated model (unit + time FE, optionally covariates)

---

## Minimal code snippets

> [!example] R

```r
# install.packages("didimputation")
library(didimputation)

# df: panel with id, time, outcome Y, treatment indicator D,
# and first_treat (cohort adoption time, Inf for never-treated)
res <- did_imputation(
  data = df, yname = "Y", gname = "first_treat",
  tname = "time", idname = "id"
)
summary(res)
```

> [!example] Python: pyfixest

```python
import pyfixest as pf

# df: panel with columns id, time, Y, D (treatment indicator), first_treat
# Imputation estimator via pyfixest
fit = pf.did.event_study(
    data=df,
    yname='Y',
    idname='id',
    tname='time',
    gname='first_treat',
    estimator='did2s'  # Gardner/imputation approach
)
pf.did.event_study_plot(fit)
```

> [!example] Stata

```stata
* ssc install did_imputation
did_imputation Y id time first_treat, allhorizons pretrends(5)
event_plot, default_look
```

---

## Related notes

- [[Difference-in-Differences (DiD)]] · [[two-way fixed effects]] · [[staggered adoption]]
- [[Gardner DID2S]] · [[Callaway–Sant’Anna estimator]] (Callaway-Sant'Anna) · [[Sun–Abraham estimator]]
- [[Goodman–Bacon decomposition]] · [[event study]]
- [[Causal Inference (MOC)]]
