---
title: Exclusion Restriction
aliases: [exclusion, exclusion assumption, no direct effect]
tags: [econometrics, causal-inference, iv, identification, diagnostics]
updated: 2025-09-17
---

# Exclusion Restriction

> [!summary] Quick definition
> In [[Instrumental Variables (IV)]], the exclusion restriction requires that the instrument $Z$ affects the outcome $Y$ only through the endogenous treatment $D$ (and not through any other channel). Formally, potential outcomes depend on $Z$ only via $D$.

## Formal statements

- Potential-outcomes form:
$$
Y(z,d) = Y(d) \quad \text{for all } z,d
$$

- Structural-equation view (with covariates $X$):
$$
Y = \alpha + \beta D + X'\gamma + u, \quad \mathbb{E}[u \mid Z,X] = 0
$$
Exclusion means $Z$ is excluded from the outcome equation except via $D$.

- DAG intuition: valid IV requires a graph with $Z \rightarrow D \rightarrow Y$ and no direct edge $Z \rightarrow Y$ (and $Z$ independent of omitted causes of $Y$ given $X$). See [[Instrumental Variables (IV)]].

## Why it matters

- With [[relevance]] but violated exclusion, IV/[[Two-Stage Least Squares (2SLS)|two-stage least squares (2SLS)]] is biased and can be more misleading than OLS.
- Under independence, [[exclusion restriction]], and (for binary Z,D) [[monotonicity]], the Wald ratio/2SLS identifies [[Local Average Treatment Effect (LATE)|LATE]].

## Common violation channels

- Direct policy or mechanical channel from $Z$ to $Y$ not mediated by $D$.
- General equilibrium or market-wide effects (prices, wages) of $Z$ that move $Y$ directly.
- Information/anticipation from $Z$ changing behavior before $D$ adjusts.
- Sample selection/[[composition]] changes induced by $Z$ (attrition, migration).
- Mis-specified $D$ (e.g., $Z$ shifts multiple treatments, co-interventions).
- Measurement/definition: $Z$ proxies for unobservables that affect $Y$ directly.

Examples:
- “Distance to college” as $Z$ for education: distance may correlate with urban opportunity, affecting $Y$ directly.
- “Policy eligibility” as $Z$ for take-up: eligibility may change expectations or access to other programs.

## Assessing plausibility (no definitive test)

> [!check] Diagnostics and design checks
> - Design argument: why should $Z$ affect $Y$ only through $D$? Specify mechanisms and blocked channels.
> - Placebos:
>   - Outcomes that should not respond to $Z$
>   - Pre-period effects (in panels/[[Difference-in-Differences (DiD)]]): $Z$ shouldn’t move $Y$ before $D$ changes
> - Mediator checks: reduced-form of $Z$ on likely mediators/channels other than $D$
> - Alternative controls/windows: robustness to sample restrictions that mute direct channels
> - Overidentification tests (if overidentified): [[Sargan test]]/[[Hansen J test]]; interpret cautiously
> - For [[fuzzy RDD]]: continuity of potential outcomes at the cutoff (donut RD, density/balance tests)

> [!warning]
> - Passing overid tests does not prove exclusion; failing may reflect other issues.
> - If all instruments share the same direct-effect violation, overid tests can miss it.

## Sensitivity and partial-exclusion approaches

- “Plausibly exogenous” bounds (e.g., Conley et al. 2012): allow a bounded direct effect of $Z$ on $Y$ and derive intervals for $\beta$.
- Control-function or augmented second-stage with $Z$ included to probe direct effects (interpret carefully; not definitive).
- Split-sample or heterogeneity checks where the direct channel is weak/absent.

## Exclusion in common designs

- Noncompliance/encouragement (RCT-IV): $Z$ = assignment; argue that assignment affects $Y$ only via take-up $D$. Report [[Intent-to-Treat (ITT)]], first stage, and discuss spillovers (violate exclusion/[[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]], [[No spillovers]]).
- [[fuzzy DiD]]: exclusion must hold for $Z \cdot Post$—assignment timing should not affect $Y$ directly except via $D \cdot Post$; assess pre-trends by assignment.
- [[fuzzy RDD]]: instrument is above-cutoff; exclusion maps to continuity of potential outcomes at the threshold, aside from treatment probability jump.

## Minimal code snippets

> [!example] R: first stage, reduced form, 2SLS, overid

```r
library(AER)
# First stage (relevance)
fs <- lm(D ~ Z + X1 + X2, data = df); summary(fs)

# Reduced form (effect of Z on Y)
rf <- lm(Y ~ Z + X1 + X2, data = df); summary(rf)

# 2SLS
iv <- ivreg(Y ~ D + X1 + X2 | Z + X1 + X2, data = df)
summary(iv)           # includes diagnostics; use robust/cluster vcov as needed

# Overidentification (only if >1 instrument)
# summary(iv, diagnostics = TRUE) prints Hansen J under AER; interpret cautiously
```

> [!example] Stata

```stata
* First stage and reduced form
reg D Z X1 X2, vce(robust)
reg Y Z X1 X2, vce(robust)

* 2SLS with diagnostics
ivregress 2sls Y X1 X2 (D = Z), vce(robust)
estat firststage
estat overid   // only meaningful with multiple instruments
```

> [!example] Python

```python
from linearmodels.iv import IV2SLS
# Reduced form and first stage (manually with statsmodels or sklearn)
iv = IV2SLS.from_formula('Y ~ 1 + X1 + X2 + [D ~ Z]', data=df).fit(cov_type='robust')
print(iv.summary)
```

## Copy-ready definitions

- Exclusion (potential outcomes):
$$
Y(z,d) = Y(d)
$$

- Structural moment:
$$
\mathbb{E}\big[Z \cdot (Y - \alpha - \beta D - X'\gamma)\big] = 0
$$

- Wald (binary $Z$, $D$; requires exclusion, independence, monotonicity):
$$
LATE = \frac{\mathbb{E}[Y \mid Z=1]-\mathbb{E}[Y \mid Z=0]}{\mathbb{E}[D \mid Z=1]-\mathbb{E}[D \mid Z=0]}
$$

## Reporting essentials

- Define $Z$, $D$, $Y$, and the hypothesized causal channel.
- Substantive justification for exclusion; discuss and rule out likely direct paths.
- Present ITT (reduced form), first stage (strength), and IV estimate; report clustering and [[few-cluster corrections]] if needed.
- If overidentified: report Hansen J/Sargan with caveats.
- Provide sensitivity analyses (alternative controls/windows, bounded direct-effect approaches).

## Common pitfalls

> [!warning] Avoid these
> - Treating overid tests as proof of validity.
> - Ignoring spillovers/interference from $Z$ that affect controls.
> - Using instruments that shift multiple treatments/co-interventions (violates exclusion).
> - Weak instruments; with imperfect exclusion, bias can be severe. See [[weak instruments]].

---

Related notes to create:
- [[Instrumental Variables (IV)]]
- [[Local Average Treatment Effect (LATE)|LATE]]
- [[Intent-to-Treat (ITT)]]
- [[noncompliance]]
- [[Two-Stage Least Squares (2SLS)|two-stage least squares (2SLS)]]
- [[relevance]]
- [[monotonicity]]
- [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]]
- [[No spillovers]]
- [[interference]]
- [[fuzzy RDD]]
- [[Regression Discontinuity Design (RDD)]]
- [[fuzzy DiD]]
- [[Difference-in-Differences (DiD)]]
- [[overidentification test]]
- [[Sargan test]]
- [[Hansen J test]]
- [[weak instruments]]
- [[few-cluster corrections]]
- [[clustered standard errors]]
- [[control function]]
- [[Conley et al. plausibly exogenous]]