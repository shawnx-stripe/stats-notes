---
title: Potential outcomes
aliases:
  - Neyman–Rubin causal model
  - Rubin causal model
  - PO framework
  - Counterfactual outcomes
tags:
  - causal-inference
  - econometrics
  - statistics
  - identification
  - estimation
updated: 2025-09-26
---

# Potential outcomes

> [!summary] Quick definition
> A framework for causal inference that defines causal effects as contrasts between potential outcomes an individual would have under different treatments. Only one potential outcome is observed; the others are counterfactual.

## Core idea and notation

- For unit i, let W_i ∈ {0,1} be treatment, and potential outcomes Y_i(1), Y_i(0).
- Observed outcome and consistency:
$$
Y_i = Y_i(W_i) = W_i\,Y_i(1) + (1-W_i)\,Y_i(0)
$$
- Average treatment effects:
$$
\text{ATE} = \mathbb{E}[Y(1) - Y(0)], \quad
\text{ATT} = \mathbb{E}[Y(1) - Y(0)\mid W=1], \quad
\text{ATC} = \mathbb{E}[Y(1) - Y(0)\mid W=0]
$$
- Heterogeneous effect (conditional ATE):
$$
\tau(x) = \mathbb{E}[Y(1)-Y(0)\mid X=x]
$$

## Key assumptions

- SUTVA (Stable Unit Treatment Value Assumption):
  - Consistency: $Y = Y(W)$ given the version of treatment received.
  - No interference: one unit’s outcome does not depend on other units’ treatments. See [[interference]] and [[No spillovers]].
- Well-defined treatment and outcome (no ambiguous versions).
- For observational identification via covariates:
  - Ignorability/unconfoundedness:
$$
(Y(1), Y(0)) \perp W \mid X
$$
  - Overlap/positivity:
$$
0 < e(X) \equiv P(W=1 \mid X) < 1 \quad \text{almost surely}
$$

> [!check] Pre-analysis checklist
> - [ ] Define the estimand (ATE, ATT, ATC, CATE) and target population.
> - [ ] Justify SUTVA and treatment definition.
> - [ ] Argue ignorability (or specify an instrument, design, or sensitivity analysis).
> - [ ] Check overlap/common support; plan trimming if needed.
> - [ ] Specify primary estimation method and robustness checks.

## Identification

- Randomized experiments:
  - By design, $(Y(1),Y(0)) \perp W$, so
$$
\text{ATE} = \mathbb{E}[Y \mid W=1] - \mathbb{E}[Y \mid W=0]
$$
- Observational studies with ignorability:
  - G-formula (standardization):
$$
\mathbb{E}[Y(w)] = \mathbb{E}\big[ \mathbb{E}[Y \mid W=w, X] \big], \quad w \in \{0,1\}
$$
  - Propensity score e(X) is a balancing score: $W \perp X \mid e(X)$.
- Connections to other designs:
  - [[Instrumental Variables (IV)|instrumental variables]] identify LATE under independence, exclusion, and monotonicity:
$$
\text{LATE} = \frac{\mathbb{E}[Y \mid Z=1] - \mathbb{E}[Y \mid Z=0]}{\mathbb{E}[W \mid Z=1] - \mathbb{E}[W \mid Z=0]}
$$
  - [[Difference-in-Differences (DiD)|difference-in-differences]] identifies ATT under [[parallel trends assumption]] framed as potential outcomes over time.
  - [[Regression Discontinuity Design (RDD)|regression discontinuity]] identifies a local ATE at the cutoff.

## Estimation methods (binary treatment)

- Outcome regression (g-computation): model $m_w(x)=\mathbb{E}[Y\mid W=w,X=x]$ and average $m_1(X)-m_0(X)$.
- Inverse probability weighting (IPW):
$$
\hat{\tau}_{\text{IPW}} = \frac{1}{n}\sum_{i=1}^n \left( \frac{W_i Y_i}{\hat{e}(X_i)} - \frac{(1-W_i) Y_i}{1-\hat{e}(X_i)} \right)
$$
- Augmented IPW / Doubly robust (AIPW):
$$
\hat{\tau}_{\text{AIPW}} = \frac{1}{n}\sum_{i=1}^n \left[ \big(\hat{m}_1(X_i)-\hat{m}_0(X_i)\big) + \frac{W_i\,(Y_i-\hat{m}_1(X_i))}{\hat{e}(X_i)} - \frac{(1-W_i)\,(Y_i-\hat{m}_0(X_i))}{1-\hat{e}(X_i)} \right]
$$
- Matching and weighting:
  - Nearest-neighbor, caliper, and optimal matching on X or the [[propensity score]].
  - [[balancing weights]] (e.g., entropy balancing, stable balancing weights).
- Machine learning for CATE:
  - T-/S-/X-learners, causal forests, R-learner, DR-learner; cross-fitting for efficiency and bias control.

## Extensions

- Multi-valued or continuous treatments:
  - Dose–response function: $\mu(w) = \mathbb{E}[Y(w)]$; use generalized propensity scores.
- Time-varying treatments and confounding:
  - Potential outcomes $Y(a_0,\dots,a_T)$; identification via [[sequential ignorability]] and the g-formula; estimators include [[Inverse Probability Weighting (IPW)|IPW]] of marginal structural models and [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]].
- Interference:
  - Define $Y_i(w_i, w_{-i})$; use exposure mappings, partial/interference neighborhoods, or design-based approaches.
- Principal stratification:
  - Effects within latent strata (e.g., compliers); connects to IV and [[Local Average Treatment Effect (LATE)|LATE]].

## Good practice

- Pre-specify estimands and analysis plan; justify assumptions with domain knowledge and, where applicable, [[causal DAGs|DAG]]s.
- Diagnose overlap; visualize e(X) distributions; trim or reweight if needed.
- Assess covariate balance before and after adjustment.
- Use robust uncertainty: nonparametric bootstrap for matching; sandwich SEs for weighting; influence-function-based SEs for AIPW/TMLE.
- Conduct sensitivity analyses for unmeasured confounding (e.g., Rosenbaum bounds, Γ; marginal sensitivity models; E-values).

## Common mistakes

- Treating adjusted associations as causal without a clear estimand or assumptions.
- Ignoring lack of overlap or extreme propensity scores.
- Using post-treatment variables as controls (violates consistency/ignorability).
- Assuming SUTVA without considering spillovers, multiple versions, or interference.
- Reporting only p-values; omit effect sizes and uncertainty for causal estimands.

## Simple numeric example

- RCT with equal allocation: mean(Y|W=1)=12, mean(Y|W=0)=10 → ATE = 2.
- Observational with estimated $\hat{e}(X)$:
  - Compute IPW ATE using the formula above; compare to outcome regression; check balance.

## Copy-ready formulas

- Observed outcome:
$$
Y = W Y(1) + (1-W) Y(0)
$$
- ATE, ATT, ATC:
$$
\text{ATE} = \mathbb{E}[Y(1)-Y(0)], \quad \text{ATT} = \mathbb{E}[Y(1)-Y(0)\mid W=1], \quad \text{ATC} = \mathbb{E}[Y(1)-Y(0)\mid W=0]
$$
- G-formula:
$$
\mathbb{E}[Y(w)] = \mathbb{E}\big[\mathbb{E}[Y \mid W=w, X]\big]
$$
- Propensity score:
$$
e(X) = P(W=1 \mid X)
$$
- IPW and AIPW (doubly robust) estimators as above.

## Obsidian rendering tips

- Use block math with `$$ ... $$` and inline math with `$ ... $`.
- Avoid LaTeX spacing commands that may render oddly.
- Enable math rendering in settings; switch MathJax versions if symbols look off.

## Minimal code snippets (optional)

```r
# R: AIPW for ATE with cross-fitting (grf + glm)
library(grf)
library(glmnet)

# Fit nuisance models
X <- model.matrix(~ . - Y - W, data = df)[, -1]
Y <- df$Y; W <- df$W

# Propensity via logistic regression
ps_mod <- cv.glmnet(X, W, family = "binomial")
e_hat <- as.numeric(predict(ps_mod, X, s = "lambda.min", type = "response"))

# Outcome models via regression forest
m1 <- regression_forest(X[W==1,], Y[W==1])
m0 <- regression_forest(X[W==0,], Y[W==0])
m1_hat <- predict(m1, X)$predictions
m0_hat <- predict(m0, X)$predictions

# AIPW estimate
tau_hat <- mean((m1_hat - m0_hat) + W*(Y - m1_hat)/e_hat - (1-W)*(Y - m0_hat)/(1 - e_hat))
tau_hat
```

```python
# Python: DR-learner with econml
import numpy as np
from sklearn.linear_model import LassoCV, LogisticRegressionCV
from econml.drlearner import DRLearner

X = df.drop(columns=['Y','W']).to_numpy()
Y = df['Y'].to_numpy()
W = df['W'].to_numpy()

mdl_y = LassoCV(cv=5)
mdl_t = LogisticRegressionCV(cv=5, max_iter=1000, solver='lbfgs')
dr = DRLearner(model_regression=mdl_y, model_propensity=mdl_t)
dr.fit(Y, W, X=X)
ate = np.mean(dr.effect(X))
ate
```

---

Related notes to create:
- [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]]
- [[consistency]]
- [[interference]]
- [[No spillovers]]
- [[ignorability]]
- [[Unconfoundedness|unconfoundedness]]
- [[Overlap|overlap]]
- [[Overlap|positivity]]
- [[propensity score]]
- [[Inverse Probability Weighting (IPW)|inverse probability weighting]]
- [[Augmented Inverse Probability Weighting (AIPW)|AIPW]]
- [[Doubly Robust estimators|doubly robust]]
- [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]]
- [[g-formula]]
- [[sequential ignorability]]
- [[Instrumental Variables (IV)|instrumental variables]]
- [[Local Average Treatment Effect (LATE)|LATE]]
- [[principal stratification]]
- [[balancing weights]]
- [[common support]]
- [[treatment effect heterogeneity|CATE]]
- [[Average Treatment Effect (ATE)|ATE]]
- [[Average Treatment Effect on the Treated (ATT)|ATT]]
- [[Average Treatment Effect on the Untreated (ATU)]] (ATC)
- [[Difference-in-Differences (DiD)|difference-in-differences]]
- [[Regression Discontinuity Design (RDD)|regression discontinuity]]
- [[causal DAGs|DAG]]
