---
title: Marginal treatment effect (MTE)
aliases:
  - MTE
  - Marginal treatment effects
  - Treatment effect at the margin
  - Heckman-Vytlacil MTE
tags:
  - causal-inference
  - econometrics
  - treatment-effects
  - heterogeneity
  - selection-models
updated: 2025-09-26
---

# Marginal treatment effect (MTE)

> [!summary] Quick definition
> The causal effect of treatment for individuals who are indifferent between treatment and control at a given level of unobserved resistance to treatment. MTE characterizes how treatment effects vary along the margin of selection and serves as a building block for all standard treatment effect parameters ([[Average Treatment Effect (ATE)|ATE]], [[Average Treatment Effect on the Treated (ATT)|ATT]], [[Local Average Treatment Effect (LATE)|LATE]], etc.).

## Core concept and notation

- Binary treatment D ∈ {0,1}, covariates X, [[potential outcomes]] Y₁ and Y₀
- Selection into treatment based on unobserved resistance U:
$$
D = \mathbf{1}\{P(X,Z) \geq U\}, \quad U \sim \text{Uniform}(0,1)
$$
where P(X,Z) = Pr(D=1|X,Z) is the [[propensity score]] and Z is an [[Instrumental Variables (IV)|IV]]

- MTE definition (Heckman & Vytlacil, 2005):
$$
\text{MTE}(x,u) \equiv \mathbb{E}[Y_1 - Y_0 \mid X=x, U=u]
$$
Interpretation: average treatment effect for individuals with characteristics x who are at the u-th quantile of resistance to treatment

### Intuition with examples

| U value | Interpretation | Example (college attendance) |
|---------|---------------|------------------------------|
| U ≈ 0 | Always-takers | Students who attend regardless of costs |
| U ≈ 0.5 | Marginal | Students swayed by moderate tuition changes |
| U ≈ 1 | Never-takers | Students who won't attend even with subsidies |

- If MTE(x,u) decreases in u: those most eager to be treated (low U) benefit most
- If MTE(x,u) increases in u: those most resistant (high U) would benefit most if treated

## Identification

### From [[Local IV]]

Under standard IV assumptions ([[exclusion restriction]], [[exogeneity]], [[monotonicity]]):

$$
\text{MTE}(x,p) = \frac{\partial}{\partial p}\,\mathbb{E}[Y \mid X=x, P(X,Z)=p]
$$

Equivalently, using the instrument Z directly:
$$
\text{MTE}\big(x,P(x,z)\big) = \frac{\partial_z\,\mathbb{E}[Y \mid X=x, Z=z]}{\partial_z\,\mathbb{E}[D \mid X=x, Z=z]}
$$

### Integral representation

The observed outcome conditional on X and P can be written as:
$$
\mathbb{E}[Y \mid X=x, P=p] = \mathbb{E}[Y_0 \mid X=x] + \int_0^p \text{MTE}(x,u)\,du
$$

This shows how MTE builds up the observed outcome function through integration.

## Relationship to standard parameters

All standard treatment effect parameters are weighted averages of MTE:

### Average Treatment Effect ([[Average Treatment Effect (ATE)|ATE]])
$$
\text{ATE}(x) = \int_0^1 \text{MTE}(x,u)\,du
$$
Equal weights across all margins of selection.

### Average Treatment on Treated ([[Average Treatment Effect on the Treated (ATT)|ATT]])
$$
\text{ATT}(x) = \frac{1}{\bar{p}(x)} \int_0^{\bar{p}(x)} \text{MTE}(x,u)\,du = \int_0^1 \text{MTE}(x,u)\,\omega^{\text{ATT}}(u,x)\,du
$$
where $\omega^{\text{ATT}}(u,x) = \frac{\min\{u, \bar{p}(x)\}}{\bar{p}(x)}$ and $\bar{p}(x) = \mathbb{E}[D \mid X=x]$

### Average Treatment on Untreated ([[Average Treatment Effect on the Untreated (ATU)|ATU]])
$$
\text{ATU}(x) = \frac{1}{1-\bar{p}(x)} \int_{\bar{p}(x)}^1 \text{MTE}(x,u)\,du
$$

### Local Average Treatment Effect ([[Local Average Treatment Effect (LATE)|LATE]])
For instrument moving propensity from p₀ to p₁:
$$
\text{LATE}(x; p_0 \to p_1) = \frac{1}{p_1-p_0} \int_{p_0}^{p_1} \text{MTE}(x,u)\,du
$$

### Policy-Relevant Treatment Effect ([[Policy-Relevant Treatment Effect (PRTE)|PRTE]])
For policy shifting propensity distribution from F_old to F_new:
$$
\text{PRTE} = \int_0^1 \text{MTE}(x,u)\,\omega^{\text{PRTE}}(u)\,du
$$
where weights depend on the policy-induced change in treatment probability.

## Key assumptions

> [!check] Required conditions
> - [ ] **Selection on unobservables**: D = 1{P(X,Z) ≥ U} with scalar U
> - [ ] **Separability**: U enters selection equation additively/monotonically
> - [ ] **Uniformity**: U ~ Uniform(0,1) (normalization)
> - [ ] **Independence**: (Y₁, Y₀, U) ⊥ Z | X
> - [ ] **Exclusion**: Z affects Y only through D
> - [ ] **Support**: P(X,Z) has sufficient variation for u of interest

## Estimation approaches

### 1. Parametric MTE
Specify functional form:
$$
\text{MTE}(x,u) = x'\beta + K(u)
$$
where K(u) is polynomial or spline in u. Estimate via [[Generalized Method of Moments (GMM)|GMM]] or maximum likelihood.

### 2. Semiparametric estimation
- **Propensity-based**: Estimate P(X,Z) flexibly, then use [[local polynomial regression]] or [[splines]] to estimate derivative of E\[Y|X,P] with respect to P
- **Direct Local IV**: Estimate derivatives of E\[Y|X,Z] and E\[D|X,Z] with respect to Z using [[kernel regression]]

### 3. Nonparametric estimation
Use fully flexible methods (e.g., [[kernel regression]], [[random forests]]) with [[cross-fitting]] for first-stage propensity score.

> [!tip] Implementation strategy
> 1. Start with visual inspection: plot E[Y|P] to assess curvature
> 2. Test for heterogeneity: is MTE(u) constant? (implies ATE = ATT = ATU)
> 3. Use [[bootstrap]] for inference, accounting for first-stage estimation
> 4. Report MTE at key quantiles (u = 0.1, 0.5, 0.9) with confidence bands

## Interpretation and policy implications

### Selection patterns

| MTE pattern     | Interpretation              | Policy implication                                                      |
| --------------- | --------------------------- | ----------------------------------------------------------------------- |
| Decreasing in u | Positive selection on gains | Current participants benefit most; expansion reduces average effect     |
| Increasing in u | Negative selection on gains | Non-participants would benefit most; expansion increases average effect |
| Flat            | No selection on gains       | ATE = ATT = ATU; selection is on levels not gains                       |
| U-shaped        | Essential heterogeneity     | Both always-takers and never-takers benefit more than marginal          |

### Policy evaluation

MTE enables evaluation of policies that change treatment take-up:
- **Marginal policy changes**: Effect depends on MTE at current margin
- **Non-marginal changes**: Integrate MTE over affected range
- **Optimal policy**: Target treatment to individuals with highest MTE(x,u)

## Common pitfalls

> [!warning] Avoid these mistakes
> - **Weak instruments**: Poor variation in P(X,Z) makes derivatives unstable
> - **Extrapolation**: Estimating MTE outside support of P leads to speculation
> - **Ignoring X**: MTE typically varies with observables; don't assume homogeneity
> - **Binary IV**: With binary Z, only [[Local Average Treatment Effect (LATE)|LATE]] is identified, not full MTE curve
> - **Misspecification**: Wrong functional form for selection can bias all parameters

## Practical example

College attendance with distance as instrument:
- Treatment D: attending college
- Instrument Z: distance to nearest college
- Outcome Y: earnings

Expected patterns:
- MTE high for u ≈ 0: high-ability students who would attend anyway
- MTE lower for u ≈ 0.5: marginal students need encouragement
- MTE possibly higher for u ≈ 1: high-ability but credit-constrained students

Policy implications:
- If MTE decreasing: focus on retention rather than expansion
- If MTE increasing: expand access through subsidies
- If MTE flat: quantity matters more than composition

## Copy-ready formulas

- MTE definition:
$$
\text{MTE}(x,u) = \mathbb{E}[Y_1 - Y_0 \mid X=x, U=u]
$$

- Identification via derivative:
$$
\text{MTE}(x,p) = \frac{\partial}{\partial p}\,\mathbb{E}[Y \mid X=x, P(X,Z)=p]
$$

- Weights for standard parameters:
$$
\theta = \int_0^1 \text{MTE}(x,u)\,\omega_\theta(u,x)\,du
$$

## Minimal code snippets (optional)

```r
# R: Estimate and plot MTE using local polynomial
library(np)
library(ggplot2)

# Assume df has Y, D, Z, X, and estimated p_hat
# Local polynomial regression of Y on p
bw <- npregbw(Y ~ p_hat, data = df, regtype = "ll")
model <- npreg(bw)

# Compute MTE as numerical derivative
p_grid <- seq(0.1, 0.9, by = 0.01)
y_smooth <- predict(model, newdata = data.frame(p_hat = p_grid))
mte <- diff(y_smooth) / diff(p_grid)
p_mid <- p_grid[-1] - diff(p_grid)/2

# Plot MTE
ggplot(data.frame(u = p_mid, mte = mte), aes(x = u, y = mte)) +
  geom_line() +
  geom_ribbon(aes(ymin = mte - 1.96*se, ymax = mte + 1.96*se), alpha = 0.3) +
  labs(x = "Resistance to treatment (u)", y = "MTE", 
       title = "Marginal Treatment Effect")
```

```python
# Python: Estimate MTE via splines
import numpy as np
from scipy.interpolate import UnivariateSpline
import matplotlib.pyplot as plt

# Fit spline to E[Y|p]
spl = UnivariateSpline(df['p_hat'], df['Y'], s=0.1)

# Compute MTE as derivative
p_grid = np.linspace(0.1, 0.9, 100)
mte = spl.derivative()(p_grid)

# Compute standard parameters
ate = np.trapz(mte, p_grid) / (p_grid[-1] - p_grid[0])
p_bar = df['D'].mean()
att_weights = np.minimum(p_grid, p_bar) / p_bar
att = np.trapz(mte * att_weights, p_grid) / np.trapz(att_weights, p_grid)

print(f"ATE: {ate:.3f}, ATT: {att:.3f}")

# Plot
plt.plot(p_grid, mte)
plt.xlabel('Resistance to treatment (u)')
plt.ylabel('MTE')
plt.title('Marginal Treatment Effect')
plt.axhline(y=ate, color='r', linestyle='--', label='ATE')
plt.axhline(y=att, color='g', linestyle='--', label='ATT')
plt.legend()
plt.show()
```

---

## Related notes
- [[Average Treatment Effect (ATE)|ATE]]
- [[Average Treatment Effect on the Treated (ATT)|ATT]]
- [[Average Treatment Effect on the Untreated (ATU)|ATU]]
- [[Local Average Treatment Effect (LATE)|LATE]]
- [[Policy-Relevant Treatment Effect (PRTE)|PRTE]]
- [[potential outcomes]]
- [[propensity score]]
- [[Instrumental Variables (IV)|IV]]
- [[Local IV]]
- [[exclusion restriction]]
- [[exogeneity]]
- [[monotonicity]]
- [[Generalized Method of Moments (GMM)|GMM]]
- [[local polynomial regression]]
- [[splines]]
- [[kernel regression]]
- [[random forests]]
- [[cross-fitting]]
- [[bootstrap]]
- [[selection on gains]]
- [[essential heterogeneity]]