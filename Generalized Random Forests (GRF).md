---
title: Generalized Random Forests (GRF)
aliases: [GRF, generalized random forests, generalized RF, grf package, local moment forests]
tags: [causal-inference, machine-learning, forests, grf, cate, iv, quantiles, regression, orthogonal, honesty]
updated: 2025-09-17
---

# Generalized Random Forests (GRF)

> [!summary] Quick definition
> Generalized Random Forests (GRF; Athey, Tibshirani & Wager) are “honest” random-forest methods that estimate parameters defined by local moment conditions, not just conditional means. GRF provides a unified framework for:
> - regression (mean/derivatives),
> - quantiles,
> - heterogeneous treatment effects (CATE; [[causal forests]]),
> - instrumental variables/local treatment effects (instrumental forests),
> - and other semiparametric targets,
> with valid uncertainty estimates and calibration tests.

- R implementation: the grf package (regression_forest, quantile_forest, causal_forest, instrumental_forest, etc.).
- Links to: [[double machine learning]] (orthogonalization idea), [[policy learning]], [[uplift]], [[off-policy evaluation]] for downstream use of CATE.

---

## What GRF solves

- Local estimation of parameters θ(x) defined by generalized moments:
$$
\mathbb{E}\big[\psi(W;\theta(x))\mid X\approx x\big]=0
$$
where ψ is a (possibly orthogonal) score. Forest weights construct adaptive neighborhoods around x to solve these local moments.

- Supported tasks (major):
  - Regression: m(x)=E[Y|X=x] (regression_forest)
  - Quantiles: Q_τ(x) (quantile_forest)
  - CATE: τ(x)=E[Y(1)−Y(0)|X=x] under [[Unconfoundedness]] (causal_forest)
  - IV/LATE heterogeneity: local treatment effects with instruments (instrumental_forest)
  - Derivatives and partial effects: average/partial effects (average_partial_effect)

See also: [[causal forests]] for the CATE specialization.

---

## Key ideas

- Honesty: split the sample into subsamples to choose splits vs estimate leaf effects; reduces bias and enables asymptotic theory.
- Adaptive neighborhoods: tree splits create weights W_i(x) that define a local sample around each x.
- Orthogonalization (where applicable): residualize outcomes/treatments to build Neyman‑orthogonal scores (robust to nuisance errors; links to [[double machine learning]]).
- Valid inference: asymptotic normality at points, forest-based variance estimators, calibration tests.

---

## When to use GRF

- You need nonparametric, data‑adaptive estimation with uncertainty for:
  - heterogeneous treatment effects (for [[policy learning]] and [[uplift]]),
  - local IV/LATE variation (instrumental forests; complements [[Instrumental Variables (IV)]]),
  - quantiles and robust summaries,
  - flexible regression and partial effects.
- You have moderate‑to‑large n, moderate p; covariates are strictly pre‑treatment (avoid [[leakage]]).

---

## Assumptions (by task)

- Regression/quantiles: standard smoothness/regularity; iid or appropriate sampling.
- CATE (causal_forest): [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]], [[Unconfoundedness]], [[Overlap]] (propensities bounded away from 0/1).
- Instrumental forests: valid instrument ([[exclusion restriction]], [[relevance]]); monotonicity if LATE interpretation; overlap in (Z|X).
- Inference assumes honesty and regular tuning; see package docs for details.

---

## Software (R grf)

- Main learners
  - regression_forest(X, Y)
  - quantile_forest(X, Y, quantiles=…)
  - causal_forest(X, Y, W[, X.test])
  - instrumental_forest(X, Y, W, Z)
- Inference/summaries
  - predict(forest, estimate.variance=TRUE)
  - average_treatment_effect(forest, target.sample="all"/"treated")
  - test_calibration(forest) (BLP/calibration)
  - variable_importance(forest)
  - average_partial_effect(regression_forest, target)
- Tuning helper: tune_parameters

---

## Code examples (R)

> [!example] CATE with causal_forest

```r
library(grf)

X <- as.matrix(df[, c("X1","X2","X3")])
Y <- df$Y
W <- df$D  # 0/1 treatment

# Fit CATE forest
cf <- causal_forest(X, Y, W, num.trees = 2000, honesty = TRUE)

# Pointwise CATE predictions with variance
pred <- predict(cf, estimate.variance = TRUE)
tau_hat <- pred$predictions
se_hat  <- sqrt(pred$variance.estimates)

# ATE and SE (forest-based)
ate <- average_treatment_effect(cf, target.sample = "all")
c(ATE = ate$estimate, SE = ate$std.err)

# Calibration / BLP test of heterogeneity usefulness
test <- test_calibration(cf)
test  # reports slope/intercept and p-values

# Variable importance
variable_importance(cf)
```

> [!example] Instrumental forests (local IV)

```r
# Z: instrument; W: endogenous treatment
Z <- df$Z
ivf <- instrumental_forest(X, Y, W, Z, num.trees = 2000, honesty = TRUE)
tau_iv <- predict(ivf)$predictions

# Optional: average partial effect (if appropriate)
# average_partial_effect(ivf, X)  # task-specific; see docs
```

> [!example] Quantile regression forest

```r
qf <- quantile_forest(X, Y, quantiles = c(0.1, 0.5, 0.9), num.trees = 2000)
q_pred <- predict(qf, X_new)  # matrix: rows=points, cols=quantiles
```

> [!example] Regression forest & partial effects

```r
rf <- regression_forest(X, Y, num.trees = 2000)
y_hat <- predict(rf)$predictions

# Average partial effect of a feature (global derivative)
ape <- average_partial_effect(rf, X, target = 1) # 1 = first feature
ape$estimate; ape$std.err
```

---

## Diagnostics and good practice

> [!check]
> - [ ] Identification: CATE requires [[Unconfoundedness]] and [[Overlap]]; IV requires [[exclusion restriction]] and [[relevance]]  
> - [ ] Overlap diagnostics: propensities from a separate model; trim tails if needed  
> - [ ] Stability: vary num.trees, min.node.size, honesty, sample.fraction; check τ̂ distribution and rank stability  
> - [ ] Calibration: use test_calibration (BLP) to verify that τ̂ carries signal  
> - [ ] Uncertainty: use predict(…, estimate.variance=TRUE); ATE SE via average_treatment_effect  
> - [ ] Variable importance: interpret with care; confirm with partial dependence or subgroup summaries  
> - [ ] Policy validation: if using τ̂ for targeting, evaluate policies with [[off-policy evaluation]] (DR/IPS) and confirm in [[AB Testing (MOC)]]

---

## Tuning tips

- num.trees: 2000–4000 for stable predictions/SEs.
- min.node.size: larger nodes reduce variance; too small → noisy leaves.
- honesty=TRUE (default) for valid inference.
- sample.fraction ~ 0.5 (defaults are good); tune with tune_parameters if needed.
- For IV forests: ensure strong first stage locally; weak instruments lead to noise (see [[weak instruments]]).

---

## Inference and calibration

- Pointwise CIs: τ̂(x) ± 1.96·SE(x) from predict variance.
- Global ATE/ATT: average_treatment_effect (forest-based influence function SE).
- Calibration (BLP): test_calibration(cf) regresses true effect proxy on τ̂(x); slope ~ 1 indicates good calibration (see [[causal forests]] for interpretation).

---

## Using GRF outputs

- Targeting and [[policy learning]]:
  - Define policy π(x)=1{τ̂(x) > c} or treat top‑b% by τ̂; evaluate with [[off-policy evaluation]] (DR preferred), then validate via [[AB Testing (MOC)]] with [[guardrail metric]]s and [[sequential testing]] if peeking.
- Uplift curves ([[uplift]]):
  - Sort by τ̂; compute Qini/AUUC; ensure overlap and holdout evaluation to avoid optimistic bias.
- Subgroup reporting:
  - Average τ̂ within interpretable bins (deciles; categorical groups); report means with SEs and avoid over-slicing ([[multiple testing control]] caution).

---

## Comparisons

- vs standard random forests: GRF solves moment conditions (not just E[Y|X]), supports CATE/IV/quantiles, and offers inference.
- vs [[double machine learning]] meta‑learners: Similar orthogonalization goal; DML is a framework with arbitrary learners; GRF provides a one‑stop forest with inference and calibration tools.
- vs [[causal forests]]: causal_forest is a GRF specialization; the “GRF” page is broader.

---

## Pitfalls

> [!warning]
> - Poor overlap (propensity near 0/1) → unstable τ̂; trim/redefine target ([[Overlap]])  
> - Using post‑treatment features ([[leakage]])  
> - Interpreting pointwise τ̂(x) without uncertainty or calibration; prefer aggregate summaries and CIs  
> - Using τ̂ for policy without OPE and online validation ([[off-policy evaluation]], [[AB Testing (MOC)]])  
> - Weak or invalid instruments in instrumental forests → noisy/biased local effects ([[weak instruments]], [[exclusion restriction]])

---

## Reporting essentials

- Task (regression/quantile/CATE/IV), identification assumptions (Unconfoundedness/IV) and diagnostics
- GRF settings: num.trees, honesty, min.node.size, sample.fraction; tuning method
- ATE/ATT with SEs (if CATE); calibration test results; variable importance
- Overlap diagnostics; trimming rules; sensitivity to tuning/seeds
- If used for policy: OPE value with CIs, online validation plan, guardrails, and sequential control
- Software versions (grf), seeds, and code for reproducibility

---

## Related notes

- Causal heterogeneity: [[causal forests]] · [[double machine learning]] · [[uplift]] · [[policy learning]]
- Identification: [[Unconfoundedness]] · [[Overlap]] · [[Instrumental Variables (IV)]] · [[exclusion restriction]] · [[weak instruments]]
- Evaluation: [[off-policy evaluation]] · [[AB Testing (MOC)]] · [[sequential testing]] · [[guardrail metric]] · [[multiple testing control]]
- Modeling hygiene: [[leakage]] · [[cross-fitting]]
- Time series / panels: see [[Time Series (MOC)]] if applying forests to time‑indexed data (use time‑aware splits)

---

## References

- Athey, Tibshirani, & Wager (2019), “Generalized Random Forests.”
- Wager & Athey (2018), “Estimation and Inference of Heterogeneous Treatment Effects using Random Forests.” (causal forests)
- grf R package documentation and vignettes

---