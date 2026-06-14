---
title: Random Effects
aliases: [random effects, Random effects, RE estimator, random effects model, GLS estimator]
tags: [econometrics, panel-data]
updated: 2026-03-05
---

# Random Effects

> [!summary]
> Panel data estimator assuming individual effects are uncorrelated with regressors ($\mathbb{E}[\alpha_i \mid X_{it}]=0$). More efficient than FE when valid; tested via [[Hausman test]]. Equivalent to GLS with a specific error structure.

---

## Model and assumptions

Panel data model with individual-specific effects:
$$
Y_{it} = X_{it}'\beta + \alpha_i + u_{it},\quad i=1,\ldots,N,\ t=1,\ldots,T,
$$
where:
- $\alpha_i$ = individual-specific random effect (unobserved heterogeneity)
- $u_{it}$ = idiosyncratic error
- $X_{it}$ = $k \times 1$ vector of regressors

**Random effects (RE) assumption**:
$$
\mathbb{E}[\alpha_i \mid X_{i1}, \ldots, X_{iT}] = 0,
$$
i.e., individual effects are **uncorrelated** with regressors. Also assume:
$$
\mathbb{E}[u_{it} \mid X_i, \alpha_i] = 0 \quad \text{(strict exogeneity)}.
$$

**Composite error**:
$$
v_{it} = \alpha_i + u_{it}.
$$

Variance components:
$$
\mathrm{Var}(\alpha_i) = \sigma^2_\alpha,\quad \mathrm{Var}(u_{it}) = \sigma^2_u.
$$

Correlation within individual:
$$
\mathrm{Corr}(v_{it}, v_{is}) = \frac{\sigma^2_\alpha}{\sigma^2_\alpha + \sigma^2_u} = \rho \quad \text{for } t \neq s.
$$
This is the [[ICC]] (intraclass correlation).

---

## Estimation: Feasible GLS

**GLS transformation**:

Partial demeaning (quasi-demeaning) to remove correlation:
$$
Y_{it} - \theta \bar Y_i = (X_{it} - \theta \bar X_i)'\beta + (v_{it} - \theta \bar v_i),
$$
where:
$$
\theta = 1 - \sqrt{\frac{\sigma^2_u}{\sigma^2_u + T\sigma^2_\alpha}} \in [0,1].
$$

**Special cases**:
- $\theta = 0$ (no demeaning): pooled OLS (if $\sigma^2_\alpha = 0$)
- $\theta = 1$ (full demeaning): fixed effects (within estimator)

**Estimation steps**:
1. Estimate $\sigma^2_u$ and $\sigma^2_\alpha$ from pooled OLS and/or within estimators
2. Compute $\hat\theta$
3. Run OLS on quasi-demeaned data:
$$
\hat\beta_{RE} = \left( \sum_{i,t} (X_{it} - \hat\theta \bar X_i)(X_{it} - \hat\theta \bar X_i)' \right)^{-1} \sum_{i,t} (X_{it} - \hat\theta \bar X_i)(Y_{it} - \hat\theta \bar Y_i).
$$

**Variance estimator**:
$$
\widehat{\mathrm{Var}}(\hat\beta_{RE}) = \hat\sigma^2_u \left( \sum_{i,t} (X_{it} - \hat\theta \bar X_i)(X_{it} - \hat\theta \bar X_i)' \right)^{-1}.
$$

Can use [[clustered standard errors]] (cluster by $i$) for robustness to heteroskedasticity.

---

## Random effects vs fixed effects

| | **Random Effects (RE)** | **Fixed Effects (FE)** |
|---|-------------------------|------------------------|
| Assumption | $\mathbb{E}[\alpha_i \mid X] = 0$ | $\alpha_i$ arbitrary (correlated with $X$) |
| Estimator | GLS (partial demeaning) | Within (full demeaning) |
| Time-invariant $X$ | Identified | Not identified (differenced out) |
| Efficiency | More efficient if assumption holds | Less efficient but robust |
| Consistency | Inconsistent if $\alpha_i \perp\!\!\!\perp X$ fails | Consistent under strict exogeneity |
| Test | [[Hausman test]] for RE vs FE | N/A |

**When to use RE**:
- Individual effects $\alpha_i$ are random draws from population (not of direct interest)
- Regressors are plausibly exogenous (e.g., experimental assignment, time-invariant characteristics like gender)
- You need to estimate effects of time-invariant variables

**When to use FE**:
- Concerned about omitted time-invariant confounders correlated with $X$
- Causal identification via within-individual variation (e.g., [[Difference-in-Differences (DiD)]])
- Prefer conservative approach (FE is robust to $\alpha_i$–$X$ correlation)

> [!tip]
> Run both RE and FE; use [[Hausman test]] to choose. If Hausman rejects (p < 0.05), FE is preferred.

---

## Hausman test

Tests $H_0$: $\mathbb{E}[\alpha_i \mid X] = 0$ (RE is consistent) vs $H_1$: RE is inconsistent.

**Test statistic**:
$$
H = (\hat\beta_{FE} - \hat\beta_{RE})' \left[ \widehat{\mathrm{Var}}(\hat\beta_{FE}) - \widehat{\mathrm{Var}}(\hat\beta_{RE}) \right]^{-1} (\hat\beta_{FE} - \hat\beta_{RE}) \sim \chi^2_k.
$$

- Reject $H_0$: use FE (RE is biased)
- Fail to reject: RE is preferred (more efficient)

See [[Hausman test]] for details.

---

## Mundlak device

**Problem**: RE assumes $\alpha_i \perp X$, but often $\alpha_i$ correlates with individual-specific means $\bar X_i$.

**Mundlak adjustment**:

Specify:
$$
\alpha_i = \bar X_i' \psi + a_i,\quad a_i \perp X,
$$
and estimate:
$$
Y_{it} = X_{it}'\beta + \bar X_i' \psi + a_i + u_{it}.
$$

If $\psi = 0$, RE assumption holds. If $\psi \neq 0$, adding $\bar X_i$ controls for correlation between $\alpha_i$ and $X$.

**Result**: Mundlak RE with $\bar X_i$ gives same $\beta$ as FE but allows estimation of time-invariant effects.

See [[Mundlak adjustment]] for details.

---

## Code snippets

> [!example] R: plm package

```r
library(plm)

# Convert to panel data
pdata <- pdata.frame(df, index = c("id", "time"))

# Random effects
re <- plm(Y ~ X1 + X2, data = pdata, model = "random")
summary(re)

# Fixed effects (for comparison)
fe <- plm(Y ~ X1 + X2, data = pdata, model = "within")
summary(fe)

# Hausman test
phtest(fe, re)  # H0: RE is consistent

# Robust SEs (cluster by id)
coeftest(re, vcov = vcovHC(re, cluster = "group"))
```

> [!example] Stata: xtreg re

```stata
* Declare panel structure
xtset id time

* Random effects
xtreg Y X1 X2, re

* Fixed effects
xtreg Y X1 X2, fe

* Hausman test
hausman fe re, sigmamore

* RE with robust SEs (cluster by id)
xtreg Y X1 X2, re vce(cluster id)
```

> [!example] Stata: Mundlak adjustment

```stata
* Compute individual means
bysort id: egen X1_mean = mean(X1)
bysort id: egen X2_mean = mean(X2)

* RE with Mundlak correction
xtreg Y X1 X2 X1_mean X2_mean, re

* Test H0: psi=0 (Mundlak terms jointly zero)
test X1_mean X2_mean
```

> [!example] Python: linearmodels

```python
from linearmodels.panel import RandomEffects

# Set multi-index (id, time)
df = df.set_index(['id', 'time'])

# Random effects
re_model = RandomEffects.from_formula('Y ~ X1 + X2 + EntityEffects', data=df)
re_result = re_model.fit(cov_type='clustered', cluster_entity=True)
print(re_result)

# Fixed effects (for comparison)
from linearmodels.panel import PanelOLS
fe_model = PanelOLS.from_formula('Y ~ X1 + X2 + EntityEffects', data=df)
fe_result = fe_model.fit(cov_type='clustered', cluster_entity=True)

# Hausman test (manual)
from scipy.stats import chi2
diff = fe_result.params - re_result.params
var_diff = fe_result.cov - re_result.cov
H = diff @ np.linalg.inv(var_diff) @ diff
p_value = 1 - chi2.cdf(H, df=len(diff))
print(f"Hausman test: H={H:.2f}, p={p_value:.4f}")
```

---

## Relation to other methods

- **Pooled OLS**: ignores $\alpha_i$; inconsistent if $\alpha_i$ correlates with $X$ or if serial correlation in $v_{it}$
- **Fixed effects (within)**: differences out $\alpha_i$; see [[two-way fixed effects]]
- **First differences**: another way to eliminate $\alpha_i$; equivalent to FE if $T=2$
- **Correlated random effects (Mundlak)**: relaxes RE assumption; see [[Mundlak adjustment]]
- **Random coefficients models**: allow $\beta_i$ to vary by individual (more flexible than RE)

---

## Practical guidance

> [!tip] When to prefer RE
> - Sample is random draw from population (survey data, not administrative)
> - Need to estimate effects of time-invariant variables (gender, race, education)
> - Efficiency gain matters (large $T$, weak within-variation)
> - Regressors are experimentally assigned or clearly exogenous

> [!warning] When RE is risky
> - Omitted time-invariant confounders likely (e.g., ability in wage regressions)
> - Causal inference goal with observational data
> - Small $T$: FE and RE give similar results; prefer FE for robustness

> [!check] Best practices
> - Always run [[Hausman test]]; report result
> - If Hausman rejects, use FE (or Mundlak RE)
> - Use [[clustered standard errors]] by individual for robustness
> - Report both FE and RE if substantive; discuss economic meaning of differences
> - For time-invariant effects, consider Mundlak approach

---

## Related notes

- [[two-way fixed effects]]
- [[Hausman test]]
- [[Panel Data Methods (MOC)]]
- [[Mundlak adjustment]]
- [[ICC]]
- [[clustered standard errors]]
- [[Ordinary Least Squares (OLS)|OLS]]
- [[Difference-in-Differences (DiD)]]

---

## References

- Wooldridge, *Econometric Analysis of Cross Section and Panel Data* (Ch. 10: RE vs FE)
- Baltagi, *Econometric Analysis of Panel Data*
- Greene, *Econometric Analysis* (Ch. 9: Random effects models)
- Mundlak (1978), "On the Pooling of Time Series and Cross Section Data," *Econometrica*
