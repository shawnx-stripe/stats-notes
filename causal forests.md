---
title: causal forests
aliases: [Causal forests, causal forest, heterogeneous treatment effects forest, CF, CATE forest]
tags: [causal-inference, machine-learning, treatment-effect-heterogeneity, CATE, policy-learning, orthogonal, dml]
updated: 2025-09-17
---

# causal forests

> [!summary] Quick definition
> Causal forests (Wager & Athey; Athey, Tibshirani & Wager) are random-forest methods that estimate heterogeneous treatment effects (CATE τ(x)) under unconfoundedness. They use “honest” splitting and orthogonalized/gradient-based criteria so that splits target treatment-effect variation rather than outcome prediction. The generalized random forest (GRF) framework extends to many causal tasks (CATE, IV/”instrumental forests”, quantile/robust effects).

- Outputs: pointwise CATE estimates τ̂(x), uncertainty (pointwise SE / confidence intervals), average treatment effect (ATE/ATT), subgroup effects, variable importance.
- Good for: discovering and quantifying heterogeneity, guiding [[policy learning]], and reporting interpretable effect patterns (partial dependence, subgroup summaries).

---

## Identification and assumptions

- Standard CATE setting (binary treatment):
  - [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]], [[Unconfoundedness]]: {Y(1),Y(0)} ⟂ D | X
  - [[Overlap]]: 0 < P(D=1 | X=x) < 1
- With instrumental forests (IV): instrument relevance and [[exclusion restriction]] (local effects).
- With observational data: model quality and overlap diagnostics are critical; causal forests do not replace identification.

> [!warning] Only use strictly pre-treatment covariates; avoid [[leakage]] and [[bad controls]].

---

## How causal forests work (high level)

- Honesty: separate subsamples for split selection and leaf estimation to reduce bias.
- Splitting criterion: targets heterogeneity in treatment effect (e.g., variance of estimates across child nodes), not just outcome variance.
- Orthogonalization (optional/GRF): residualize Y and D on X (à la [[double machine learning]]) so splits focus on effect signal and are robust to nuisance error.

Let τ(x) = E\[Y(1)−Y(0) | X=x]. GRF solves a local moment condition using forest weights W_i(x):
$$
\hat\tau(x)\ \text{solves}\ \sum_i W_i(x)\,\psi(W_i;\tau)=0,
$$
with ψ the orthogonal score (e.g., AIPW/partialling-out score).

---

## What you can estimate

- CATE τ(x) with SEs and confidence intervals
- ATE/ATT and subgroup averages (forest-weighted aggregation)
- Best linear predictor (BLP) of τ̂(x) to summarize heterogeneity strength
- Instrumental forests: local IV/LATE-style heterogeneity (binary/continuous IVs)
- Quantile/robust effects (distributional GRF variants)

---

## Software

### R (grf)

- CATE (causal_forest), ATE, variable importance, BLP tests, CIs
```r
# install.packages("grf")
library(grf)

X <- as.matrix(df[, c("X1","X2","X3")])
Y <- df$Y
W <- df$D  # 0/1 treatment

cf <- causal_forest(X, Y, W, num.trees = 2000, honesty = TRUE)
# Point estimates
tau_hat <- predict(cf)$predictions

# ATE and SE (forest-based)
ate <- average_treatment_effect(cf, target.sample = "all")
ate$estimate; ate$std.err

# Calibrated variance / CIs for CATE at points
pred <- predict(cf, estimate.variance = TRUE)
ci_lo <- pred$predictions - 1.96*sqrt(pred$variance.estimates)
ci_hi <- pred$predictions + 1.96*sqrt(pred$variance.estimates)

# Variable importance (split frequencies)
vi <- variable_importance(cf); vi
```

- Instrumental forests
```r
# Z is instrument; estimate local IV (treatment effect) heterogeneity
Z <- df$Z
ivf <- instrumental_forest(X, Y, W, Z)
tau_iv <- predict(ivf)$predictions
```

- Diagnostics: best linear predictor (BLP) test of heterogeneity
```r
test <- test_calibration(cf) # tests if tau_hat is calibrated; reports BLP slope
test
```

### Python (econml)

- CausalForestDML / ForestDRLearner provide orthogonalized forests
```python
# pip install econml
from econml.dml import CausalForestDML
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LogisticRegression

Y = df['Y'].values
T = df['D'].values
X = df[['X1','X2','X3']].values

cf = CausalForestDML(model_t=LogisticRegression(max_iter=2000),
                     model_y=RandomForestRegressor(n_estimators=300, random_state=0),
                     n_estimators=2000, min_samples_leaf=5, random_state=0)
cf.fit(Y, T, X=X)
tau_hat = cf.effect(X)
ate = cf.ate(X)
intervals = cf.effect_interval(X)  # pointwise CIs

# Variable importance (feature importances from underlying forest)
vi = cf.feature_importances_
```

---

## Practical workflow

> [!check]
> - [ ] Ensure identification (design/RCT or strong observables with [[Overlap]]), define estimand  
> - [ ] Clean strictly pre-treatment features; standardize/transform as needed  
> - [ ] Fit causal forest (sufficient trees; honesty on; cross-fitting via orthogonal learners where applicable)  
> - [ ] Summarize heterogeneity: distribution of τ̂(x); subgroup averages; BLP and variable importance  
> - [ ] Validate with ATE from forest vs baseline estimator (AIPW/[[double machine learning]])  
> - [ ] Diagnostics: overlap (propensity tails), calibration (test_calibration), uncertainty bands  
> - [ ] Use τ̂(x) for [[policy learning]]; evaluate via DR [[off-policy evaluation]]; confirm online via A/B

---

## Interpretation aids

- Subgroup effects: average τ̂(x) over interpretable bins (e.g., deciles of a score, categorical segments) with SEs.
- Partial dependence of τ̂(x): visualize how CATE varies along top features (keeping others fixed).
- BLP (best linear predictor) test: regresses true effects (unknown) on τ̂(x) using forest weights; slope close to 1 suggests well-calibrated heterogeneity.
- Variable importance: which features drive splits; pairwise interaction depth.

---

## Inference and uncertainty

- Pointwise SEs/CIs from forest asymptotics (GRF) or via bootstrap (expensive).
- ATE/ATT SEs from forest-based influence functions.
- Clustered data: average pointwise influence scores at cluster level; then use [[clustered standard errors]] / [[few-cluster corrections]] (not always off-the-shelf; consider aggregation + robust SEs).

---

## Strengths and limitations

> [!tip] Strengths
> - Data-adaptive detection of heterogeneity without prespecifying interactions  
> - Honesty reduces bias; orthogonalization improves robustness to nuisance error  
> - Provides uncertainty estimates and tests (BLP/calibration)

> [!warning] Limitations
> - Requires identification and good [[Overlap]]; fails under severe propensity tails  
> - Can be unstable with small N or very high p; needs many trees and careful tuning  
> - CATE pointwise CIs can be wide; multiple testing and selection issues remain  
> - Interpretability is better than black-box nets but still “model-based”; prefer subgroup summaries and policy value

---

## Tuning tips

- Trees: 2000–4000 often stabilize τ̂; honesty=TRUE; sample.fraction ~ 0.5 (R grf defaults are strong).
- Leaf size: set min.node.size/min_samples_leaf to avoid tiny leaves (variance explosions).
- Orthogonalization: prefer residualization (Y on X; D on X) when strong confounding is present (econml’s DML learners).
- Cross-fitting: built-in in many DML implementations; keep out-of-fold predictions.

---

## Diagnostics

> [!check]
> - [ ] Overlap: histogram of propensity ê(X); consider trimming extreme tails  
> - [ ] ATE validation: forest ATE vs AIPW/DR estimate  
> - [ ] Calibration/BLP test (grf::test_calibration)  
> - [ ] Stability: τ̂ across random seeds/folds; variable importance robustness  
> - [ ] Placebos: τ̂ on pre-period or negative-control outcomes should be ~0 patternless  
> - [ ] Policy value: does a simple policy (treat top-b%) improve DR value vs treat-all?

---

## Common pitfalls

> [!warning]
> - Using post-treatment features (leakage)  
> - Equating τ̂(x) ranking with perfect targeting—always validate with OPE and A/B  
> - Ignoring uncertainty when slicing many subgroups (multiplicity)  
> - Over-interpreting noisy local effects; prefer aggregation/subgroup means with CIs  
> - Disregarding cluster/time dependence in SEs for panels/clustered data

---

## Reporting essentials

- Design and identification (RCT vs observational; assumptions checked), sample size
- Feature set (pre-treatment only), preprocessing, overlap diagnostics
- Model settings: number of trees, honesty, min leaf size, orthogonalization details
- ATE/ATT (with SEs) and key subgroup averages; BLP calibration test
- Variable importance and partial dependence/ICE-style views of τ̂(x)
- Policy evaluation (off-policy DR value) and, if applicable, online validation
- Sensitivity to hyperparameters and seeds

---

## Related notes

- [[treatment effect heterogeneity]] · [[double machine learning]] · [[Augmented Inverse Probability Weighting (AIPW)|AIPW]] · [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]]
- [[policy learning]] · [[policy tree]] · [[uplift]]
- [[Unconfoundedness]] · [[Overlap]] · [[bad controls]] · [[leakage]]
- [[clustered standard errors]] · [[few-cluster corrections]] · [[off-policy evaluation]]
- [[AB Testing (MOC)]] · [[Causal Inference (MOC)]] 

---

## References (brief)

- Wager, S., & Athey, S. (2018). “Estimation and Inference of Heterogeneous Treatment Effects using Random Forests.”
- Athey, Tibshirani, & Wager (2019). “Generalized Random Forests.”
- grf documentation (R); econml documentation (Python).

---
