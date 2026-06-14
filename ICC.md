---
title: ICC
aliases: [ICC, intraclass correlation, intraclass correlation coefficient, Intraclass Correlation (ICC)]
tags: [experimentation, design, clustering]
updated: 2026-03-05
---

# ICC

> [!summary]
> Intraclass Correlation Coefficient: fraction of total variance attributable to between-cluster variation. Determines the [[design effect]] and required sample size in cluster-randomized experiments. $\text{ICC} = \sigma^2_b / (\sigma^2_b + \sigma^2_w)$.

---

## Definition and formula

Consider observations $Y_{ij}$ nested within clusters $i = 1,\ldots,G$, $j=1,\ldots,n_i$.

**One-way random effects model**:
$$
Y_{ij} = \mu + \alpha_i + \varepsilon_{ij},
$$
where:
- $\alpha_i \sim (0, \sigma^2_b)$ (between-cluster random effect)
- $\varepsilon_{ij} \sim (0, \sigma^2_w)$ (within-cluster error)
- $\alpha_i \perp \varepsilon_{ij}$

**ICC (intraclass correlation)**:
$$
\rho = \frac{\sigma^2_b}{\sigma^2_b + \sigma^2_w}.
$$

**Interpretation**:
- $\rho$ = correlation between any two observations in the same cluster
- $\rho = 0$: no clustering (all variation within clusters)
- $\rho = 1$: perfect clustering (all variation between clusters)
- Typical values: 0.01–0.2 in many applications (0.05 is common rule of thumb)

**Variance decomposition**:
- Total variance: $\mathrm{Var}(Y_{ij}) = \sigma^2_b + \sigma^2_w$
- Between-cluster variance: $\sigma^2_b$
- Within-cluster variance: $\sigma^2_w$

---

## Estimation

**Method 1: One-way ANOVA**

Decompose sum of squares:
$$
\text{SS}_{\text{total}} = \text{SS}_{\text{between}} + \text{SS}_{\text{within}}.
$$

Mean squares:
$$
\text{MS}_b = \frac{\text{SS}_{\text{between}}}{G-1}, \quad \text{MS}_w = \frac{\text{SS}_{\text{within}}}{N-G}.
$$

Estimate:
$$
\hat\sigma^2_w = \text{MS}_w, \quad \hat\sigma^2_b = \frac{\text{MS}_b - \text{MS}_w}{\bar n},
$$
where $\bar n = \frac{1}{G}\sum_i n_i$ (average cluster size; use harmonic mean if unbalanced).

ICC estimate:
$$
\hat\rho = \frac{\hat\sigma^2_b}{\hat\sigma^2_b + \hat\sigma^2_w}.
$$

**Method 2: Mixed-effects (REML/ML)**

Fit random intercept model:
$$
Y_{ij} = \mu + \alpha_i + \varepsilon_{ij}
$$
via `lmer()` (R), `mixed` (Stata), or `statsmodels.MixedLM` (Python).

Extract variance components $\hat\sigma^2_b, \hat\sigma^2_w$ and compute $\hat\rho$.

> [!tip]
> ANOVA and REML give similar ICC estimates for balanced designs. REML is preferred for unbalanced clusters or with covariates.

---

## Relationship to design effect and sample size

**Design effect (DEFF)**:
$$
\text{DEFF} = 1 + (m-1)\rho,
$$
where $m$ = average cluster size.

**Interpretation**: variance inflation due to clustering. If $\rho=0.05$ and $m=20$:
$$
\text{DEFF} = 1 + 19 \times 0.05 = 1.95.
$$
Effective sample size is $N / 1.95 \approx 0.51 N$ (need ~2× as many units as in simple random sampling).

**Minimum Detectable Effect (MDE)**:

For cluster-randomized trial with $G$ clusters per arm, cluster size $m$, and ICC $\rho$:
$$
\text{MDE} \propto \sqrt{\frac{1 + (m-1)\rho}{Gm}} = \sqrt{\frac{\text{DEFF}}{Gm}}.
$$

Key insights:
- Higher ICC ⇒ larger MDE (need more clusters or larger clusters)
- Increasing cluster size $m$ helps, but with diminishing returns if $\rho > 0$ (better to add more clusters)
- See [[power analysis]] and [[Minimum Detectable Effect (MDE)|MDE]] for details

---

## Estimation in practice

> [!check] Steps
> 1. Fit random intercept model or run one-way ANOVA
> 2. Extract $\hat\sigma^2_b$ and $\hat\sigma^2_w$
> 3. Compute $\hat\rho = \hat\sigma^2_b / (\hat\sigma^2_b + \hat\sigma^2_w)$
> 4. Report ICC with confidence interval (bootstrap or delta method)

> [!warning] Negative variance estimates
> If ANOVA yields $\hat\sigma^2_b < 0$, set $\hat\rho = 0$ (indicates negligible clustering). REML/ML constrain $\sigma^2_b \geq 0$.

**Confidence intervals**:
- Bootstrap: resample clusters and recompute ICC
- Delta method: approximate CI using asymptotic variance of $\hat\sigma^2_b, \hat\sigma^2_w$
- Bayesian: posterior distribution of $\rho$ from mixed model

---

## Code snippets

> [!example] R: ICC from one-way ANOVA

```r
library(ICC)

# Compute ICC using ANOVA method
icc_result <- ICCest(cluster_id, outcome, data = df)
print(icc_result)  # ICC estimate + CI
```

> [!example] R: ICC from lme4

```r
library(lme4)

# Random intercept model
fit <- lmer(outcome ~ 1 + (1 | cluster_id), data = df)
vc <- as.data.frame(VarCorr(fit))

sigma2_b <- vc$vcov[vc$grp == "cluster_id"]
sigma2_w <- vc$vcov[vc$grp == "Residual"]
icc <- sigma2_b / (sigma2_b + sigma2_w)
cat("ICC =", icc, "\n")
```

> [!example] R: ICC with covariates

```r
library(lme4)

# Conditional ICC (after adjusting for X1, X2)
fit <- lmer(outcome ~ X1 + X2 + (1 | cluster_id), data = df)
vc <- as.data.frame(VarCorr(fit))
sigma2_b <- vc$vcov[vc$grp == "cluster_id"]
sigma2_w <- vc$vcov[vc$grp == "Residual"]
icc_conditional <- sigma2_b / (sigma2_b + sigma2_w)
cat("Conditional ICC =", icc_conditional, "\n")
```

> [!example] Python: ICC with pingouin

```python
import pingouin as pg

# Compute ICC(1,1) — single rater/measurement
icc = pg.intraclass_corr(data=df, targets='subject', raters='cluster_id',
                         ratings='outcome')
print(icc)
# ICC types: ICC1, ICC2, ICC3 (different models; ICC1 is random effects)
```

> [!example] Python: ICC from statsmodels

```python
import statsmodels.formula.api as smf

# Random intercept model
md = smf.mixedlm("outcome ~ 1", df, groups=df["cluster_id"])
mdf = md.fit()

sigma2_b = float(mdf.cov_re.iloc[0, 0])
sigma2_w = mdf.scale  # residual variance
icc = sigma2_b / (sigma2_b + sigma2_w)
print(f"ICC = {icc:.4f}")
```

> [!example] Stata: loneway and xtmixed

```stata
* One-way ANOVA ICC
loneway outcome cluster_id

* Mixed model
xtmixed outcome || cluster_id:, variance
estat icc  // report ICC
```

---

## Interpretation guidelines

| ICC | Interpretation | Implication |
|-----|----------------|-------------|
| < 0.01 | Negligible clustering | Can ignore clustering (but still cluster SEs for safety) |
| 0.01–0.05 | Low clustering | Moderate design effect; cluster SEs essential |
| 0.05–0.15 | Moderate clustering | Substantial design effect; power/sample size adjustments needed |
| > 0.15 | High clustering | Large design effect; prioritize recruiting more clusters over larger clusters |

**For [[geo experiment]]**: ICCs often 0.05–0.20 (cities/regions are heterogeneous); see [[geo experiment]] for geospatial design considerations.

---

## ICC vs clustered standard errors

- **ICC**: measures clustering strength; used for design and power analysis
- [[clustered standard errors]]: adjust SEs and inference post-estimation to account for within-cluster correlation
- Even if ICC is small, always use clustered SEs when randomization is at cluster level
- See [[Moulton problem]] for consequences of ignoring clustering in regression

---

## Practical guidance

> [!tip] When to estimate ICC
> - **Pre-experiment**: Use pilot data or external estimates to inform power analysis
> - **Post-experiment**: Estimate ICC to verify design assumptions and guide future studies
> - **Cluster-randomized trials**: Always report ICC (essential for replication and meta-analysis)

> [!check] Reporting
> - Report ICC estimate with 95% CI
> - State estimation method (ANOVA, REML, conditional on covariates)
> - Report cluster count $G$ and average cluster size $m$
> - Compute and report design effect $1 + (m-1)\rho$
> - If ICC differs from design assumption, recalculate realized power

> [!warning] Pitfalls
> - ICC is outcome-specific; cannot assume same ICC across outcomes
> - ICC can vary by subgroup (e.g., treatment vs control)
> - Very small number of clusters ($G < 10$): ICC estimates unstable
> - Do not confuse ICC with $R^2$ (ICC is about clustering, not model fit)

---

## Related notes

- [[power analysis]]
- [[Minimum Detectable Effect (MDE)|MDE]]
- [[geo experiment]]
- [[Moulton problem]]
- [[clustered standard errors]]
- [[design effect]]
- [[random effects]]

---

## References

- Donner & Klar, *Design and Analysis of Cluster Randomization Trials in Health Research*
- Raudenbush & Bryk, *Hierarchical Linear Models*
- Eldridge & Kerry, *A Practical Guide to Cluster Randomised Trials in Health Services Research*
- Wooldridge, *Econometric Analysis of Cross Section and Panel Data* (Ch. 21: clustered data)
