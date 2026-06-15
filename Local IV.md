---
title: Local IV
aliases:
  - LIV
  - Local instrumental variables
  - Local Wald estimator
  - Marginal treatment effect identification
tags:
  - causal-inference
  - econometrics
  - instrumental-variables
  - policy-evaluation
  - selection-models
updated: 2025-09-26
---

# Local IV

> [!summary] Quick definition
> A continuous-analogue of the [[Wald estimator]]/[[Instrumental Variables (IV)|instrumental variables]] approach that identifies the [[marginal treatment effect (MTE)|MTE]] (Marginal Treatment Effect) by differentiating outcome and treatment propensities with respect to a (smooth) instrument. Under a single-index, monotone selection model and valid instruments, this “local Wald” ratio recovers the effect for individuals at the margin of indifference to treatment.

## Core setup and notation

- Binary treatment D ∈ {0,1}, covariates X, instrument Z (continuous or with many support points).
- [[potential outcomes]]: Y1, Y0; observed outcome Y = D Y1 + (1−D) Y0.
- Selection model (single-index, monotone in a scalar unobservable U):
$$
D = \mathbf{1}\{ P(X,Z) \ge U \}, \quad U \sim \text{Uniform}(0,1), \quad P(X,Z) = \Pr(D=1\mid X,Z)
$$
- [[marginal treatment effect (MTE)|MTE]] (Heckman–Vytlacil):
$$
\text{MTE}(x,u) \equiv \mathbb{E}[Y_1 - Y_0 \mid X=x,\, U=u], \quad u \in (0,1)
$$
Interpretation: effect for units with covariates x and resistance-to-treatment U exactly at u (marginal individuals).

## Identification via Local IV

Two equivalent representations under standard conditions ([[exclusion restriction]], [[exogeneity]] of Z given X, single-index [[monotonicity]], smoothness):

1) Derivative with respect to the propensity p = [[propensity score]] P(X,Z):
$$
\text{MTE}(x,p) \;=\; \frac{\partial}{\partial p}\, \mathbb{E}[\,Y \mid X=x,\; P(X,Z)=p\,]
$$
and the integral relationship:
$$
\mathbb{E}[\,Y \mid X=x,\; P=p\,] \;=\; \mathbb{E}[Y_0 \mid X=x] \;+\; \int_{0}^{p} \text{MTE}(x,u)\,du
$$

2) Local IV (local Wald) ratio using the instrument Z directly:
$$
\text{MTE}\big(x,\, P(x,z)\big) \;=\;
\frac{\dfrac{\partial}{\partial z}\,\mathbb{E}[\,Y \mid X=x, Z=z\,]}
     {\dfrac{\partial}{\partial z}\,\mathbb{E}[\,D \mid X=x, Z=z\,]}
$$

- With a binary Z, derivatives are not defined; the finite-difference Wald yields [[Local Average Treatment Effect (LATE)|LATE]], the average of MTE over the interval of propensities moved by Z.

## Relationships to familiar estimands

- [[Local Average Treatment Effect (LATE)|LATE]] (for Z shifting p from p0 to p1 at X=x):
$$
\text{LATE}(x; z_0 \!\to\! z_1) \;=\; \frac{\mathbb{E}[Y\mid X=x,z_1]-\mathbb{E}[Y\mid X=x,z_0]}{\mathbb{E}[D\mid X=x,z_1]-\mathbb{E}[D\mid X=x,z_0]}
\;=\; \frac{1}{p_1-p_0}\int_{p_0}^{p_1} \text{MTE}(x,u)\,du
$$

- [[Average Treatment Effect (ATE)|ATE]] and other policy parameters are weighted averages of MTE:
  - ATE(x) = ∫_0^1 MTE(x,u) du; ATE = E_X[ATE(X)].
  - [[Average Treatment Effect on the Treated (ATT)|ATT]], [[Average Treatment Effect on the Untreated (ATU)|ATU]], [[Policy-Relevant Treatment Effect (PRTE)|PRTE]], etc., are averages of MTE with estimand-specific weights over u and X.

## Key assumptions

- [[exclusion restriction]]: Z affects outcomes only via D (Y1, Y0 ⟂ Z | X).
- Instrument [[exogeneity]]: (Y1, Y0, U) ⟂ Z | X.
- Monotone single-index selection: D = 1{P(X,Z) ≥ U} with scalar U and strictly increasing CDF (no defiers; see [[monotonicity]]).
- Smoothness and support:
  - E[Y | X=x, Z=z] and E[D | X=x, Z=z] are differentiable in z (or in p = P(X,Z)).
  - Support of P(X,Z) covers the range of u of interest ([[common support]]).

> [!check] Pre-analysis checklist
> - [ ] Specify the target: pointwise MTE(x,u) or averages ([[Average Treatment Effect (ATE)|ATE]], [[Average Treatment Effect on the Treated (ATT)|ATT]], [[Policy-Relevant Treatment Effect (PRTE)|PRTE]]).
> - [ ] Argue instrument validity ([[exclusion restriction]], independence given X).
> - [ ] Verify monotone single-index selection is plausible.
> - [ ] Check instrument strength and that P(X,Z) varies smoothly with Z.
> - [ ] Assess support of p across X; avoid extrapolating u where p is rarely observed.

## Estimation strategies

1) Propensity-index approach (two-step):
- Step 1: Estimate p̂(x,z) = Pr(D=1 | X,Z) flexibly (e.g., probit/logit/GAM/ML with [[cross-fitting]]).
- Step 2: Estimate m(x,p) = E[Y | X=x, p̂=p]. Common implementations:
  - Partial out X (Robinson): regress Y on X, take residuals; regress residuals on a flexible function of p; take derivative wrt p.
  - Additive model: Y ~ g(p) + h(X); then MTE(x,p) = g′(p).
- Step 3: Compute MTE(x,p) = ∂ m(x,p) / ∂ p. Estimate derivatives via:
  - [[kernel regression]] / local polynomial (local linear gives closed-form derivative).
  - [[splines]]/series in p (e.g., B-splines) and differentiate basis.
- Inference: [[bootstrap]] with sample splitting to account for first-stage p̂.

2) Local IV ratio using Z:
- Estimate ∂ E[Y | X=x,Z=z] / ∂ z and ∂ E[D | X=x,Z=z] / ∂ z via local linear or spline smoothers in z (conditioning on X additively or by residualizing).
- Take their ratio at z, yielding MTE(x, p(x,z)).
- Requires smooth Z with adequate local variation.

3) Parametric/semi-parametric MTE parameterization:
- Specify MTE(x,u) = x′β + s(u; θ) + x′Γ r(u), with r(u) a low-order polynomial or spline in u.
- Use the integral relationship E[Y | X=x, p] = E[Y0 | X=x] + ∫_0^p MTE(x,u) du to fit parameters by least squares or [[Generalized Method of Moments (GMM)|GMM]].
- Integrate estimated MTE against weights to obtain [[Average Treatment Effect (ATE)|ATE]]/[[Average Treatment Effect on the Treated (ATT)|ATT]]/[[Policy-Relevant Treatment Effect (PRTE)|PRTE]].

4) Control function equivalence:
- Under single-index selection, define V = F_{U|X,Z}(U | X,Z) = U. Then E[Y | X,Z] = E[Y0 | X] + ∫_0^{P(X,Z)} MTE(X,u) du.
- Estimation parallels the propensity-index approach.

## From MTE to policy-relevant parameters

- ATE at X=x:
$$
\text{ATE}(x) = \int_0^1 \text{MTE}(x,u)\,du, \quad \text{ATE}=\mathbb{E}_X[\text{ATE}(X)]
$$
- ATT at X=x with p̄(x) = E[D|X=x] (under U ~ Uniform(0,1)):
$$
\text{ATT}(x) = \frac{1}{\bar{p}(x)} \int_0^1 \text{MTE}(x,u)\,(1-u)\,du
$$
- ATU at X=x:
$$
\text{ATU}(x) = \frac{1}{1-\bar{p}(x)} \int_0^1 \text{MTE}(x,u)\,u\,du
$$
- LATE between p0 and p1:
$$
\text{LATE}(x; p_0\!\to\!p_1) = \frac{1}{p_1-p_0} \int_{p_0}^{p_1} \text{MTE}(x,u)\,du
$$
- [[Policy-Relevant Treatment Effect (PRTE)|PRTE]] (policy-relevant treatment effect):
  - For a change in policy that shifts the distribution of P from G_old to G_new:
$$
\text{PRTE} = \mathbb{E}_X\!\left[\int_0^1 \text{MTE}(X,u)\,\big(g_{\text{new}}(u\mid X)-g_{\text{old}}(u\mid X)\big)\,du\right]
$$
  - For small shifts, weights are proportional to the change in P induced by the policy.

## Practical implementation

- Use flexible first-stage for P(X,Z). Cross-validate and use [[cross-fitting]] to reduce bias.
- Ensure overlap in p across values of X; trim regions with sparse support ([[common support]]).
- For local IV in Z, choose bandwidths by cross-validation; check sensitivity to bandwidth.
- Center and scale Z and continuous X to stabilize local derivative estimation.
- Report both pointwise MTE(x,u) and averages ([[Average Treatment Effect (ATE)|ATE]]/[[Average Treatment Effect on the Treated (ATT)|ATT]]/[[Local Average Treatment Effect (LATE)|LATE]]/[[Policy-Relevant Treatment Effect (PRTE)|PRTE]]) with uncertainty.

> [!tip] Reporting
> - Plot MTE(u) at representative X values with bands.
> - Show the first-stage p̂(X,Z) distribution and the range of u actually supported.
> - Provide sensitivity to first-stage specification and smoothing choices.

## Common pitfalls

> [!warning] Beware
> - Discrete or weak Z: with few support points, only [[Local Average Treatment Effect (LATE)|LATE]]-type averages are identified; pointwise MTE is not.
> - Violations of single-index [[monotonicity]]: multiple unobservables or non-monotone selection break identification.
> - Extrapolation in u: estimating MTE where p has little support leads to unstable derivatives.
> - Ignoring first-stage error: derivatives of E[Y|p̂] must account for estimation of p̂; use [[bootstrap]]/split-sample.
> - Over-controlling: do not include post-treatment or affected-by-Z covariates that violate the [[exclusion restriction]].

## When to use

- Settings with smooth, policy-induced variation in treatment propensity (prices, distances, thresholds with noise, continuous encouragements).
- When heterogeneity in treatment effects by selection margin is substantively important and you want policy counterfactuals ([[Policy-Relevant Treatment Effect (PRTE)|PRTE]]).

## Copy-ready formulas

- Propensity-index identification:
$$
\text{MTE}(x,p) \;=\; \frac{\partial}{\partial p}\,\mathbb{E}[Y \mid X=x,\, P(X,Z)=p]
$$

- Local IV ratio:
$$
\text{MTE}\big(x, P(x,z)\big) \;=\; \frac{\partial_z\,\mathbb{E}[Y \mid X=x, Z=z]}{\partial_z\,\mathbb{E}[D \mid X=x, Z=z]}
$$

- Integral relationship:
$$
\mathbb{E}[Y \mid X=x, P=p] \;=\; \mathbb{E}[Y_0 \mid X=x] \;+\; \int_{0}^{p} \text{MTE}(x,u)\,du
$$

- LATE as an average of MTE over a propensity segment [p0, p1]:
$$
\text{LATE}(x; p_0\!\to\!p_1) \;=\; \frac{1}{p_1-p_0}\int_{p_0}^{p_1} \text{MTE}(x,u)\,du
$$

- Weights for average effects:
  - [[Average Treatment Effect on the Treated (ATT)|ATT]](x):
$$
\text{ATT}(x) \;=\; \frac{1}{\bar{p}(x)} \int_0^1 \text{MTE}(x,u)\,(1-u)\,du
$$
  - [[Average Treatment Effect on the Untreated (ATU)|ATU]](x):
$$
\text{ATU}(x) \;=\; \frac{1}{1-\bar{p}(x)} \int_0^1 \text{MTE}(x,u)\,u\,du
$$
  - [[Average Treatment Effect (ATE)|ATE]](x):
$$
\text{ATE}(x) \;=\; \int_0^1 \text{MTE}(x,u)\,du
$$

## Minimal code snippets (optional)

```r
# R: Propensity-index + spline in p with derivative (GAM + gratia)
library(mgcv)
library(gratia)

# Step 1: First-stage propensity (flexible)
m_p <- gam(D ~ s(Z) + s(X1) + X2, family = binomial(), data = df)
df$p_hat <- predict(m_p, type = "response")

# Step 2: Outcome model with additive structure
m_y <- gam(Y ~ s(p_hat, k = 10) + s(X1) + X2, data = df)

# Step 3: Derivative wrt p (MTE) at a grid of p (additive model => MTE = g'(p))
p_grid <- data.frame(p_hat = seq(0.05, 0.95, by = 0.01))
der <- derivatives(m_y, term = "s(p_hat)", newdata = p_grid)
mte <- der$derivative
# ATE by integrating MTE over u
ATE_hat <- trapz::trapz(p_grid$p_hat, mte)
ATE_hat
```

```python
# Python: Series in p with spline basis and analytic derivative via finite diff
import numpy as np
import pandas as pd
from sklearn.preprocessing import SplineTransformer
from sklearn.linear_model import LinearRegression, LogisticRegression

# First-stage propensity
X_first = df[['Z','X1','X2']].to_numpy()
D = df['D'].to_numpy()
clf = LogisticRegression(max_iter=2000).fit(X_first, D)
p_hat = clf.predict_proba(X_first)[:, 1]
df['p_hat'] = p_hat

# Spline basis in p and linear controls
spl = SplineTransformer(degree=3, n_knots=8, include_bias=False)
B = spl.fit_transform(p_hat.reshape(-1, 1))
X_ctrl = df[['X1','X2']].to_numpy()
X_design = np.hstack([B, X_ctrl])

# Outcome regression
y = df['Y'].to_numpy()
ols = LinearRegression().fit(X_design, y)
coef_B = ols.coef_[:B.shape[1]]

# Derivative of spline basis wrt p at grid points (numeric)
def spline_derivative(transformer, p_vec):
    eps = 1e-5
    Bp = transformer.transform((p_vec + eps).reshape(-1, 1))
    Bm = transformer.transform((p_vec - eps).reshape(-1, 1))
    return (Bp - Bm) / (2 * eps)

p_grid = np.linspace(0.05, 0.95, 91)
dB = spline_derivative(spl, p_grid)
mte = dB @ coef_B  # MTE(p) in additive model
ATE = np.trapz(mte, p_grid)
print("ATE:", ATE)
```

```stata
* Stata: Local IV ratio via local linear derivatives in Z (illustrative)
* Residualize Y and D on X (partialling out)
reg Y X1 X2
predict Y_tilde, resid
reg D X1 X2
predict D_tilde, resid

* Choose evaluation point z0 and a symmetric window h
local z0 = 0
local h  = 0.5

* Local linear derivative estimates at z0
lpoly Y_tilde Z if inrange(Z, `z0'-`h', `z0'+`h'), degree(1) at(`z0') deriv(1)
matrix list r(table)
scalar dEy = r(table)[1,1]

lpoly D_tilde Z if inrange(Z, `z0'-`h', `z0'+`h'), degree(1) at(`z0') deriv(1)
matrix list r(table)
scalar dEd = r(table)[1,1]

display "MTE at z0 = " `z0' " is " dEy/dEd
```

Notes:
- Use [[bootstrap]] (or the block/bootstrap if needed) for uncertainty, accounting for the first-stage p̂ and smoothing.
- For multiple X, consider additive structures or residualization ([[partialling out]]) to stabilize derivative estimation.
- Prefer cluster-robust or design-based uncertainty when Z varies at a cluster level ([[clustered standard errors]]).

---

## Related notes
- [[Wald estimator]]
- [[Instrumental Variables (IV)|instrumental variables]]
- [[marginal treatment effect (MTE)|MTE]]
- [[potential outcomes]]
- [[exclusion restriction]]
- [[exogeneity]]
- [[monotonicity]]
- [[propensity score]]
- [[Local Average Treatment Effect (LATE)|LATE]]
- [[Average Treatment Effect (ATE)|ATE]]
- [[Average Treatment Effect on the Treated (ATT)|ATT]]
- [[Average Treatment Effect on the Untreated (ATU)|ATU]]
- [[Policy-Relevant Treatment Effect (PRTE)|PRTE]]
- [[cross-fitting]]
- [[kernel regression]]
- [[splines]]
- [[bootstrap]]
- [[Generalized Method of Moments (GMM)|GMM]]
- [[common support]]
- [[partialling out]]
- [[clustered standard errors]]