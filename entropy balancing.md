---
title: Entropy Balancing
aliases: [Entropy balancing, entropy balance, ebal, calibration weighting, entropy weights]
tags: [causal-inference, weighting, balance, att, ate, did, calibration]
updated: 2025-09-17
---

# Entropy Balancing

> [!summary] Quick definition
> Entropy balancing is a calibration-weighting method that chooses observation weights to exactly match pre-specified covariate moments of a target group while staying as close as possible to baseline weights. It solves a convex optimization problem that minimizes the (relative) entropy (Kullback–Leibler divergence) subject to balance constraints.

- Typical use:
  - ATT: reweight [[control group]] to match the [[treated group]] on pre-treatment covariate moments.
  - DiD: reweight controls to match treated pre-period means (and slopes) to support conditional [[parallel trends assumption]].
  - Survey/design integration: calibrate to known margins.

## Why use entropy balancing?

- Guarantees exact covariate balance on chosen moments (e.g., means, variances).
- Avoids modeling the [[propensity score]]; works purely through balance constraints.
- Produces strictly positive weights, improving stability relative to ad hoc solutions.

## Setup and notation

- Let i index the units you will reweight (often controls, D=0). Let $w_i$ be the weight for unit i.
- Let $x_i$ be a vector of balance functions (e.g., covariates, powers, interactions).
- Let $m$ be the vector of target moments (e.g., treated-group covariate means).
- Optional baseline weights $w_i^{(0)}$ (default uniform).

## Core optimization (copy-ready)

Minimize the Kullback–Leibler divergence of weights to baseline:
$$
\min_{w} \quad \sum_i w_i \log\!\left(\frac{w_i}{w_i^{(0)}}\right)
$$
subject to:
$$
\sum_i w_i x_i = m, \quad \sum_i w_i = 1, \quad w_i > 0 \ \forall i.
$$

- Dual solution has exponential tilting form:
$$
w_i^\star \propto w_i^{(0)} \exp\big(\lambda^\top x_i\big),
$$
with λ chosen to satisfy the moment constraints.

> [!tip] What to balance
> - Start with means of key pre-treatment covariates.
> - Add higher moments (squares) and interactions if needed.
> - In DiD, include pre-period outcomes and possibly pre-trend indicators (e.g., mean and slope).

## ATT vs. ATE usage

- ATT (common): construct weights only for controls so that weighted controls match treated moments; set treated weights to 1 (or to their survey/base weights).
- ATE: balance both groups to a common target (e.g., overall population moments) or use symmetric calibration.

## Entropy balancing in DiD

- Goal: make controls look like treated in the pre-period(s), supporting conditional [[parallel trends assumption]].
- Balance set can include:
  - Pre-period outcome levels (e.g., $Y_{t_0}$, $Y_{t_0-1}$)
  - Pre-trend proxies (e.g., time dummies interacted with baseline covariates, or the pre-period slope)
  - Static covariates (industry, region, demographics)

Then estimate DiD on the reweighted sample with appropriate [[clustered standard errors]].

## Diagnostics

> [!check] After weighting
> - Exact balance on constrained moments (should be identical up to numerical tolerance)
> - Check additional moments not constrained (placebo balance)
> - Weight distribution: min/median/max, effective sample size (ESS)
> - Sensitivity to choice of moments (parsimonious vs. expanded sets)

> [!warning] Feasibility
> If the constraint set is infeasible (no positive weights solve it), relax moment sets, reduce dimensionality, or allow slack with penalties.

## Good practice

- Choose moments guided by design logic (pre-treatment covariates and outcomes).
- Prefer a parsimonious, theory-driven balance set; over-constraining can inflate variance.
- In panels, construct balance constraints within relevant cohorts/time slices when needed.
- Combine with design/base weights by setting $w_i^{(0)}$ accordingly.

## Common pitfalls

> [!warning] Avoid these
> - Balancing on post-treatment variables (see [[bad controls]]).
> - Ignoring outcome-weight interplay: extreme weights can harm precision; monitor ESS and tails.
> - Overfitting balance sets without theory, leading to unstable weights and limited external validity.
> - Treating balance as identification; balance supports assumptions but does not prove them.

## Minimal code snippets

> [!example] R: ebal (ATT style)

```r
# install.packages("ebal")
library(ebal)

# Controls to be reweighted, treated moments as targets
controls <- subset(df, D == 0)
treated  <- subset(df, D == 1)

Xc <- as.matrix(controls[, c("X1","X2","X3","preY","preSlope")])
mt <- colMeans(treated[, c("X1","X2","X3","preY","preSlope")])

fit <- ebalance(Treatment = rep(0, nrow(Xc)), X = Xc, target.margins = mt)
w_ctrl <- fit$w     # positive weights for controls
w <- numeric(nrow(df))
w[df$D==1] <- 1     # ATT: treated weight = 1
w[df$D==0] <- w_ctrl

# Use w in outcome/DiD regression with robust/clustered SEs
```

> [!example] R: cobalt/WeightIt (entropy method)

```r
# install.packages(c("WeightIt","cobalt"))
library(WeightIt); library(cobalt)
wout <- weightit(D ~ X1 + X2 + X3 + preY + preSlope, data = df, method = "ebal", estimand = "ATT")
w <- wout$weights
bal.tab(wout)    # balance diagnostics
```

> [!example] Stata: ebalance

```stata
* ssc install ebalance, replace
* Reweight controls to treated means on selected covariates
preserve
keep if D==0
matrix X = (X1, X2, X3, preY, preSlope)
matrix m = (r(mean_X1_treated), r(mean_X2_treated), r(mean_X3_treated), r(mean_preY_treated), r(mean_preSlope_treated))
* In practice, compute treated means beforehand and plug into m
ebalance X, targets(m)
gen w = _webal   // weights for controls
restore
replace w = 1 if D==1
```

> [!example] Python: cvxpy (sketch)

```python
# pip install cvxpy
import cvxpy as cp
import numpy as np

C = df[df.D==0].copy()   # controls
T = df[df.D==1].copy()   # treated
Xc = C[['X1','X2','X3','preY','preSlope']].to_numpy()
m  = T[['X1','X2','X3','preY','preSlope']].mean().to_numpy()

n = Xc.shape[0]
w = cp.Variable(n)
w0 = np.ones(n)/n

obj = cp.Minimize(cp.sum(cp.kl_div(w, w0)))   # sum w*log(w/w0) - w + w0; kl_div gives convex variant
constraints = [w >= 1e-12,
               cp.sum(w) == 1,
               Xc.T @ w == m]
prob = cp.Problem(obj, constraints)
prob.solve(solver=cp.SCS, verbose=False)

w_ctrl = np.array(w.value).flatten()
df['w'] = 1.0
df.loc[df.D==0, 'w'] = w_ctrl
```

## Copy-ready formulas

- Entropy objective with linear balance:
$$
\min_w \sum_i w_i \log\!\left(\frac{w_i}{w_i^{(0)}}\right)
\quad \text{s.t.} \quad \sum_i w_i x_i = m,\ \sum_i w_i = 1,\ w_i>0.
$$

- Exponential tilting solution:
$$
w_i^\star = \frac{w_i^{(0)} \exp(\lambda^\top x_i)}{\sum_j w_j^{(0)} \exp(\lambda^\top x_j)}.
$$

- Effective sample size (diagnostic):
$$
ESS = \frac{\left(\sum_i w_i\right)^2}{\sum_i w_i^2}.
$$

## Reporting essentials

- Estimand (ATT/ATE) and which group was reweighted.
- Balance set (which moments/variables), and resulting exact balance.
- Weight diagnostics (min/median/max, ESS); any base weights used.
- Outcome model and inference (SEs, clustering level; [[few-cluster corrections]] if needed).
- Sensitivity to balance-set choices; alternative specifications.

---

## Related notes
- [[propensity score]]
- [[matching]]
- [[Inverse Probability Weighting (IPW)|IPW]]
- [[Augmented Inverse Probability Weighting (AIPW)|AIPW]]
- [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]]
- [[Doubly Robust estimators]]
- [[Unconfoundedness]]
- [[Overlap]]
- [[bad controls]]
- [[Difference-in-Differences (DiD)]]
- [[parallel trends assumption]]
- [[treated group]]
- [[control group]]
- [[clustered standard errors]]
- [[few-cluster corrections]]
- [[composition]]
- [[pre-trends]]