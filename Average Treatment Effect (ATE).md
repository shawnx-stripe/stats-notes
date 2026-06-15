---
title: Average Treatment Effect (ATE)
aliases: [ATE, average causal effect, population average treatment effect]
tags: [causal-inference, ate, matching, weighting, dr, tmle, did, iv]
updated: 2025-09-17
---

# Average Treatment Effect (ATE)

> [!summary] Quick definition
> The ATE is the average causal effect in the target population:
> $$
> ATE = \mathbb{E}[Y(1) - Y(0)].
> $$
> It differs from [[Average Treatment Effect on the Treated (ATT)]] and [[Local Average Treatment Effect (LATE)|LATE]] in target population and identification requirements.

- Population choice matters (sample vs. super-population vs. transport/target population).
- Requires assumptions depending on design: [[Unconfoundedness]], [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]], [[Overlap]]; or design-based identification (e.g., randomized experiments).

## Relationships to other estimands

- Decomposition:
$$
ATE = P(D=1)\cdot ATT + P(D=0)\cdot ATU,
$$
where $ATU = \mathbb{E}[Y(1)-Y(0)\mid D=0]$.
- With perfect randomization: [[Average Treatment Effect (ATE)|ATE]] = [[Intent-to-Treat (ITT)|ITT effect]] = [[Average Treatment Effect on the Treated (ATT)|ATT]].
- [[Instrumental Variables (IV)|IV]] settings: [[Two-Stage Least Squares (2SLS)|2SLS]]/Wald identifies [[Local Average Treatment Effect (LATE)|LATE]] for compliers, not ATE, unless effects are homogeneous or additional structure is imposed.

## Identification by design

### Randomized experiments
- Under random assignment and [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]]:
$$
ATE = \mathbb{E}[Y \mid D=1] - \mathbb{E}[Y \mid D=0].
$$

### Selection on observables (unconfoundedness)
- If {Y(1), Y(0)} ⟂ D | X and [[Overlap]]:
  - Match/weight/adjust on X (or on [[propensity score]] e(X)) to identify ATE.

### Difference-in-Differences (DiD)
- Classic DiD generally targets ATT for treated units. To target ATE, aggregate cohort-time effects (including never-treated) with population-representative weights, or design a symmetric rollout. See [[Callaway–Sant’Anna estimator]], [[group-time average treatment effect]].

### Instrumental Variables (IV)
- With binary Z and D, [[Instrumental Variables (IV)|IV]] identifies [[Local Average Treatment Effect (LATE)|LATE]]; this equals ATE only under strong assumptions (e.g., homogeneous effects). Otherwise report LATE and discuss external validity gaps.

## Estimators (cross-sectional)

### 1) [[Inverse Probability Weighting (IPW)|IPW]] (inverse probability weighting)
- ATE-IPW (copy-ready):
$$
\widehat{ATE}_{IPW}=\frac{1}{N}\sum_i\left[\frac{D_iY_i}{\hat e(X_i)}-\frac{(1-D_i)Y_i}{1-\hat e(X_i)}\right].
$$
- Stabilized IPW improves variance:
$$
SW_i=\begin{cases}
\frac{\hat p}{\hat e(X_i)}, & D_i=1\\
\frac{1-\hat p}{1-\hat e(X_i)}, & D_i=0
\end{cases},\quad \hat p=\frac{1}{N}\sum_i D_i.
$$

### 2) [[Outcome regression (OR)]]
- Model $m_d(X)=\mathbb{E}[Y\mid D=d,X]$ and compute:
$$
\widehat{ATE}_{OR}=\frac{1}{N}\sum_i \left(\hat m_1(X_i)-\hat m_0(X_i)\right).
$$

### 3) Doubly robust (AIPW/DR)
- Consistent if either PS or OR model is correct:
$$
\widehat{ATE}_{AIPW}=\frac{1}{N}\sum_i\Bigg[
\hat m_1(X_i)-\hat m_0(X_i)
+\frac{D_i\big(Y_i-\hat m_1(X_i)\big)}{\hat e(X_i)}
-\frac{(1-D_i)\big(Y_i-\hat m_0(X_i)\big)}{1-\hat e(X_i)}
\Bigg].
$$
- See [[Augmented Inverse Probability Weighting (AIPW)|AIPW]] and [[Doubly Robust estimators]]. [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]] provides a targeted, DR alternative with good finite-sample behavior. [[double machine learning]] extends to ML nuisance models with orthogonalization.

### 4) Matching and subclassification
- [[matching]] on X or PS; [[stratification|subclassification]] on PS quantiles; then average within strata.

> [!tip] Overlap and stability
> - Inspect PS overlap and extreme weights; trim or switch to overlap/entropy weights (e.g., weights ∝ e(X)(1−e(X))) when necessary. See [[entropy balancing]].

## Panel/DiD variants for ATE

- Estimate cohort-time $ATT(g,t)$ and aggregate with population weights to approximate ATE over units/time:
$$
ATE \approx \sum_{g,t} w_{g,t}\, ATT(g,t),\quad \sum_{g,t} w_{g,t}=1,
$$
choosing $w_{g,t}$ to reflect the target population/time window. See [[Callaway–Sant’Anna estimator]] and [[group-time average treatment effect]].

## Diagnostics and good practice

> [!check] Checklist
> - [ ] Define target population (sample vs. target) and time horizon.
> - [ ] Check [[Overlap]]: PS densities, weight summaries (min/median/max, ESS).
> - [ ] Balance diagnostics pre/post weighting/matching (SMDs, variance ratios).
> - [ ] Sensitivity to trimming thresholds and model choices.
> - [ ] Use robust/clustered SEs; small-G corrections if clustered (see [[clustered standard errors]], [[few-cluster corrections]]).
> - [ ] For ML-based DR/DML, use cross-fitting and pre-specify learners.

> [!warning] Common pitfalls
> - Severe lack of overlap leading to unstable IPW estimates.
> - Using post-treatment variables (see [[bad controls]]).
> - Interpreting IV-derived [[Local Average Treatment Effect (LATE)|LATE]] as ATE without justification.
> - Naively averaging ATT estimates and calling it ATE without population-representative weights.

## Minimal code snippets

> [!example] R: ATE-IPW and AIPW

```r
# IPW
ps_mod <- glm(D ~ X1 + X2 + poly(X3,2) + X1:X2, family = binomial(), data = df)
ps <- ps_mod$fitted.values
ate_ipw <- mean(df$D*df$Y/ps - (1-df$D)*df$Y/(1-ps))

# AIPW
# Outcome models
m1 <- lm(Y ~ X1 + X2 + poly(X3,2) + X1:X2, data = subset(df, D==1))
m0 <- lm(Y ~ X1 + X2 + poly(X3,2) + X1:X2, data = subset(df, D==0))
m1hat <- predict(m1, newdata = df)
m0hat <- predict(m0, newdata = df)
aipw <- mean(m1hat - m0hat + df$D*(df$Y - m1hat)/ps - (1-df$D)*(df$Y - m0hat)/(1-ps))
```

> [!example] Stata: ATE with teffects

```stata
* IPW ATE
teffects ipw (Y) (D X1 X2 c.X3##c.X3), ate vce(robust)

* AIPW ATE
teffects aipw (Y X1 X2 c.X3##c.X3) (D X1 X2 c.X3##c.X3), ate vce(robust)
```

> [!example] Python: EconML DRLearner (ATE, sketch)

```python
# pip install econml
from econml.dr import DRLearner
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LogisticRegression

Y = df['Y'].values
T = df['D'].values
X = df[['X1','X2','X3']].values

dr = DRLearner(model_propensity=LogisticRegression(max_iter=2000),
               model_regression=RandomForestRegressor(),
               model_final=RandomForestRegressor(),
               random_state=123)
dr.fit(Y, T, X=X)
ate = dr.ate(X)
print(ate.mean())  # sample ATE estimate
```

## Copy-ready formulas

- Definition:
$$
ATE = \mathbb{E}[Y(1) - Y(0)]
$$
- ATE-IPW:
$$
\widehat{ATE}_{IPW}=\frac{1}{N}\sum_i\left[\frac{D_iY_i}{\hat e(X_i)}-\frac{(1-D_i)Y_i}{1-\hat e(X_i)}\right]
$$
- AIPW:
$$
\widehat{ATE}_{AIPW}=\frac{1}{N}\sum_i\left[\hat m_1(X_i)-\hat m_0(X_i)+\frac{D_i(Y_i-\hat m_1(X_i))}{\hat e(X_i)}-\frac{(1-D_i)(Y_i-\hat m_0(X_i))}{1-\hat e(X_i)}\right]
$$

## Reporting essentials

- Target population and window; sample vs. external target (transportability).
- Identification strategy and assumptions (randomization, unconfoundedness, DiD, IV).
- Diagnostics: overlap, weight stability, balance, model fit (for DR).
- Inference details: SE type, clustering level, small-sample corrections if needed.
- Sensitivity: alternative PS models, trimming, weights (stabilized, overlap), and DR vs. IPW.

---

## Related notes
- [[Average Treatment Effect on the Treated (ATT)]]
- [[Local Average Treatment Effect (LATE)|Local Average Treatment Effect (LATE)]]
- [[Intent-to-Treat (ITT)]]
- [[matching]]
- [[propensity score]]
- [[Inverse Probability Weighting (IPW)|IPW]]
- [[Augmented Inverse Probability Weighting (AIPW)|AIPW]]
- [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]]
- [[Doubly Robust estimators]]
- [[double machine learning]]
- [[Unconfoundedness]]
- [[Overlap]]
- [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]]
- [[bad controls]]
- [[Difference-in-Differences (DiD)]]
- [[Callaway–Sant’Anna estimator]]
- [[group-time average treatment effect]]
- [[clustered standard errors]]
- [[few-cluster corrections]]