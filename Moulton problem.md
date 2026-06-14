---
title: Moulton problem
aliases:
  - Moulton bias
  - Clustered data bias
  - Moulton factor
  - Moulton correction
  - Design effect clustering
tags:
  - econometrics
  - statistics
  - clustering
  - standard-errors
  - inference
updated: 2025-09-23
---

# Moulton problem

> [!summary] Quick definition
> Standard errors are severely underestimated when analyzing clustered data with common group-level regressors while ignoring the clustering structure. Named after Brent Moulton's 1990 paper demonstrating this bias in labor economics applications.

## Core problem and intuition

- When a regressor varies only at the group level (e.g., state policy) but outcomes are measured at individual level, treating observations as independent dramatically understates uncertainty.
- Block-math (copy/paste as-is):
$$
\text{Moulton factor} = \sqrt{1 + \rho(n_c - 1)}
$$
where $\rho$ is the [[ICC|intraclass correlation]] and $n_c$ is the average cluster size.

- True SE ≈ Naive SE × Moulton factor
- With $\rho = 0.05$ and $n_c = 100$: factor ≈ 2.2, so SEs are 2.2× larger than OLS assumes!

### Simple numeric example

| Setting | Value |
|---------|-------|
| Clusters (states) | 50 |
| Obs per cluster | 100 |
| Total N | 5,000 |
| ICC ($\rho$) | 0.05 |
| Moulton factor | $\sqrt{1 + 0.05(99)} = 2.23$ |

- Naive t-stat = 4.0 → Corrected t-stat ≈ 1.8
- "Significant" result becomes insignificant!

## The general problem setup

- Regression with individual-level outcomes and group-level regressors:
$$
Y_{ig} = \beta_0 + \beta_1 X_g + \varepsilon_{ig}
$$
where $i$ indexes individuals, $g$ indexes groups, and $X_g$ varies only across groups.

- Error structure with clustering:
$$
\varepsilon_{ig} = \nu_g + e_{ig}
$$
where $\nu_g$ is group-specific error and $e_{ig}$ is idiosyncratic error.

- OLS assumes all observations independent, but within-group correlation inflates effective sample size.

## Manifestations and severity

> [!warning] When is it worst?
> - High [[ICC|intraclass correlation]] ($\rho$)
> - Large cluster sizes ($n_c$)
> - Regressors with little/no within-cluster variation
> - Common in: state policies, school interventions, firm-level treatments

Rule of thumb impacts:
- $\rho = 0.01$, $n_c = 50$: SEs understated by 40%
- $\rho = 0.05$, $n_c = 100$: SEs understated by 120%
- $\rho = 0.10$, $n_c = 200$: SEs understated by 340%

## Solutions

### 1. [[clustered standard errors|Clustered standard errors]]
- Cluster at the level of regressor variation
- Block-math (copy/paste as-is):
$$
\hat{V}_{\text{cluster}} = (X'X)^{-1} \left(\sum_{g=1}^G X_g' \hat{u}_g \hat{u}_g' X_g \right) (X'X)^{-1}
$$

### 2. Aggregate to cluster level
- Run analysis on group means/totals
- Degrees of freedom = number of clusters minus parameters

### 3. [[multilevel models|Multilevel models]] / [[random effects|Random effects]]
- Model the error structure explicitly
- Partial pooling can improve efficiency

### 4. [[randomization inference|Design-based inference]]
- [[randomization inference|Randomization inference]] at cluster level
- [[wild cluster bootstrap|Wild cluster bootstrap]] for few clusters

> [!check] Implementation checklist
> - [ ] Identify clustering level(s) in your data
> - [ ] Check which regressors vary only between clusters
> - [ ] Calculate or estimate ICC
> - [ ] Compare naive vs clustered SEs
> - [ ] Report number of clusters

## Good practice

- Always cluster SEs when regressors have limited within-cluster variation
- Cluster at the highest level of aggregation where treatment varies
- With nested clustering, use multi-way clustering or the coarsest level
- Report both number of observations AND number of clusters
- Be cautious with few clusters (< 30-50)

> [!tip] Quick diagnostic
> If clustered SEs are >2× larger than robust SEs, you have a serious Moulton problem. Consider aggregating or using design-based methods.

## Common mistakes

> [!danger] What NOT to do
> - Ignore clustering because "it's just a robustness check"
> - Cluster at wrong level (e.g., individual when treatment is at state)
> - Use clustered SEs with very few clusters without adjustments
> - Add group fixed effects thinking it solves the problem (it doesn't for group-level regressors)

## Extensions and related issues

- [[serial correlation|Serial correlation]] in panels creates similar problems over time
- [[spatial correlation|Spatial correlation]] creates analogous issues in space
- [[few clusters problem|Few clusters problem]] when G < 30-50
- [[multi-way clustering|Multi-way clustering]] for multiple dimensions
- [[Cameron–Gelbach–Miller|Cameron-Gelbach-Miller]] procedures for complex clustering

## When this matters most

- Policy evaluation using individual data with state/regional policies
- Education research with school/classroom interventions  
- Labor economics with firm-level variables
- Health studies with hospital/clinic-level treatments
- Any [[Difference-in-Differences (DiD)|difference-in-differences]] with group-level treatment

## Copy-ready formulas

- Moulton factor:
$$
MF = \sqrt{1 + \rho(n_c - 1)}
$$

- Relationship to [[design effect]]:
$$
\text{DEFF} = 1 + \rho(n_c - 1)
$$

- Effective sample size:
$$
n_{\text{eff}} = \frac{n}{1 + \rho(n_c - 1)}
$$

- ICC definition:
$$
\rho = \frac{\sigma^2_{\nu}}{\sigma^2_{\nu} + \sigma^2_e}
$$

## Minimal code snippets (optional)

```r
# R: Diagnose Moulton problem
library(lfe)
library(lmtest)

# Naive OLS
ols <- lm(y ~ state_policy + controls, data = df)

# Clustered SEs
cluster_se <- felm(y ~ state_policy + controls | 0 | 0 | state, data = df)

# Compare
coeftest(ols)  # Naive
summary(cluster_se)  # Clustered

# Calculate Moulton factor
rho <- ICC::ICCbare(state, y, data = df)
n_c <- mean(table(df$state))
moulton_factor <- sqrt(1 + rho * (n_c - 1))
```

```stata
* Stata: Demonstrate Moulton problem
* Naive regression
reg y state_policy controls

* Store results
estimates store naive

* Clustered standard errors  
reg y state_policy controls, cluster(state)

* Compare
estimates table naive ., se

* Calculate ICC
loneway y state
```

```python
# Python: Moulton factor calculation
import numpy as np
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor

def moulton_factor(rho, cluster_sizes):
    """Calculate Moulton inflation factor"""
    avg_cluster_size = np.mean(cluster_sizes)
    return np.sqrt(1 + rho * (avg_cluster_size - 1))

# Example
rho = 0.05  # ICC
cluster_sizes = [100] * 50  # 50 clusters of size 100
mf = moulton_factor(rho, cluster_sizes)
print(f"Moulton factor: {mf:.2f}")
print(f"SEs understated by: {(mf-1)*100:.0f}%")
```

---

Related notes to create:
- Brent Moulton
- [[ICC|intraclass correlation]]
- [[clustered standard errors]]
- [[design effect]]
- [[multilevel models]]
- [[random effects]]
- [[randomization inference|design-based inference]]
- [[randomization inference]]
- [[wild cluster bootstrap]]
- [[serial correlation]]
- [[spatial correlation]]
- [[few clusters problem]]
- [[multi-way clustering]]
- [[Cameron–Gelbach–Miller|Cameron-Gelbach-Miller]]
- [[Difference-in-Differences (DiD)]]