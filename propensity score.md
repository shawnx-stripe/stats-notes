---
title: Propensity Score
aliases:
- PS
- e(X)
- propensity-score
- treatment propensity
- Propensity Score
- Propensity score
tags:
- causal-inference
- unconfoundedness
- weighting
- matching
- ATT
- ATE
updated: 2025-09-17
---

# Propensity Score

> [!summary] Quick definition
> The propensity score is the probability of receiving treatment given observed covariates:
> $$
> e(X) = \Pr(D=1 \mid X).
> $$
> Under [[Unconfoundedness]] and [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]], adjusting for the scalar $e(X)$ is sufficient to remove bias from observed confounders. It is used for [[matching]], [[Inverse Probability Weighting (IPW)|IPW]] weighting, and [[stratification|subclassification]]/stratification.

- Typical goals: estimate [[Treatment-on-the-Treated (TOT)]]/ATT or [[Average Treatment Effect (ATE)|ATE]].
- Works best with good [[Overlap]] and pre-treatment [[covariates]].

## Identification and core idea

- If {Y(1), Y(0)} ⟂ D | X and 0 < e(X) < 1 (positivity), then
  - Within strata of e(X), treated and controls are comparable in expectation.
  - You can match, weight, or stratify on e(X) to estimate effects.

## Ways to use propensity scores

### 1) Matching on e(X)
- Nearest neighbor or caliper matching on PS (or on Mahalanobis distance within PS calipers).
- Good practice: use calipers on the logit of e(X), e.g., 0.2 SD of logit(PS), and check balance.

### 2) Inverse Probability Weighting (IPW)
- ATE weights:
  - Treated: w_i = 1 / e(X_i)
  - Controls: w_i = 1 / (1 − e(X_i))
- ATT weights:
  - Treated: w_i = 1
  - Controls: w_i = e(X_i) / (1 − e(X_i))

ATE-IPW estimator (copy-ready):
$$
\widehat{ATE} = \frac{1}{N}\sum_i \left[ \frac{D_i Y_i}{\hat e(X_i)} - \frac{(1-D_i)Y_i}{1-\hat e(X_i)} \right].
$$

ATT-IPW (difference in weighted means):
$$
\widehat{ATT} =
\frac{\sum_{i:D_i=1} Y_i}{N_1}
\;-\;
\frac{\sum_{i:D_i=0} \frac{\hat e(X_i)}{1-\hat e(X_i)} Y_i}{\sum_{i:D_i=0} \frac{\hat e(X_i)}{1-\hat e(X_i)}}.
$$

- Stabilized weights to reduce variance:
  - ATE: SW_i = P(D=1)/e(X_i) for treated; SW_i = P(D=0)/(1−e(X_i)) for controls.

### 3) Subclassification (stratification)
- Partition e(X) into K strata (e.g., quintiles), estimate within-stratum differences, then average across strata (weighted by stratum size).
- Check balance within each stratum; increase K if needed.

### 4) Doubly robust (AIPW/DR)
- Combine outcome regression with IPW. Consistent if either PS model or outcome model is correct. See [[Augmented Inverse Probability Weighting (AIPW)|AIPW]] and [[Doubly Robust estimators]].

## Estimating the propensity score

- Models: logistic/probit regression with interactions and nonlinear terms (splines, polynomials).
- Machine learning: gradient boosting, random forests, neural nets, generalized additive models.
- Covariate balancing approaches: [[CBPS]] (covariate balancing propensity score).
- Use cross-validation/cross-fitting to avoid overfitting; prioritize balance, not PS predictive accuracy.

> [!tip] Specification
> - Include only pre-treatment covariates.
> - Allow flexible forms (interactions, nonlinearities).
> - After estimation, assess balance; re-specify until balance is acceptable.

## Diagnostics: balance and overlap

> [!check] After matching/weighting, report
> - Standardized mean differences (SMD) for each covariate before/after; target |SMD| < 0.1.
> - Variance ratios close to 1; eCDF/QQ overlays.
> - Overlap of PS by treatment status (density/histogram).
> - Common support actions: trimming/truncation (e.g., drop e(X) < 0.01 or > 0.99, or extreme weights).
> - Weight diagnostics: min/median/max, percent above thresholds, effective sample size (ESS).

> [!warning] Pitfalls
> - Including post-treatment variables (creates [[bad controls]]).
> - Declaring success based on predictive AUC rather than balance.
> - Severe lack of overlap (extreme weights); consider trimming, narrower target (ATT/TUT), or alternative designs (e.g., [[entropy balancing]]).
> - Using naive bootstrap for nearest-neighbor matching SEs (can be invalid).

## Propensity scores in DiD

- Use PS to reweight controls to match treated pre-treatment composition; supports conditional [[parallel trends assumption]].
- Match on pre-period outcomes and slopes plus PS for stronger design.
- Then estimate DiD with weights and clustered SEs; see [[Difference-in-Differences (DiD)]] and [[clustered standard errors]].

## Variance and robustness

- Weight instability inflates variance; use stabilized weights and trim extremes.
- Consider entropy balancing or overlap weighting (weights ∝ e(X)(1−e(X))) for improved stability.
- DR estimators (AIPW/TMLE) mitigate model misspecification risk.

## Minimal code snippets

> [!example] R: PS estimation, ATT-IPW, balance

```r
# PS via logistic regression
ps_mod <- glm(D ~ X1 + X2 + poly(X3,2) + X1:X2, data = df, family = binomial())
ps <- ps_mod$fitted.values

# ATT-IPW weights
w <- ifelse(df$D==1, 1, ps/(1-ps))

# ATT estimate (weighted difference in means)
att <- with(df, weighted.mean(Y[D==1], w[D==1]) - weighted.mean(Y[D==0], w[D==0]))

# Balance with cobalt
library(cobalt)
bal.tab(df$D, df[,c("X1","X2","X3")], weights = w, estimand = "ATT", method = "weighting")
love.plot(df$D, df[,c("X1","X2","X3")], weights = w, abs = TRUE)
```

> [!example] R: Subclassification

```r
K <- 5
q <- quantile(ps, probs = seq(0,1,length.out=K+1))
df$stratum <- cut(ps, breaks = q, include.lowest = TRUE)
att_s <- with(df, tapply(Y, list(D, stratum), mean, na.rm=TRUE))
# Aggregate across strata weighted by treated share per stratum
```

> [!example] Stata: IPW and AIPW

```stata
* Propensity score
logit D X1 X2 c.X3##c.X3 c.X1#c.X2
predict ps, pr

* ATT weights for controls
gen w = cond(D==1, 1, ps/(1-ps))

* Weighted ATT (difference in means)
mean Y [iw=w] if D==1
scalar mu1 = r(mean)
mean Y [iw=w] if D==0
scalar mu0 = r(mean)
display mu1 - mu0

* Built-in estimators
teffects ipw (Y) (D X1 X2 c.X3##c.X3), atet vce(robust)
teffects aipw (Y X1 X2 c.X3##c.X3) (D X1 X2 c.X3##c.X3), atet vce(robust)
```

> [!example] Python: ATT-IPW (sketch)

```python
import numpy as np
from sklearn.linear_model import LogisticRegression

X = df[['X1','X2','X3']].values
ps = LogisticRegression(max_iter=2000).fit(X, df['D']).predict_proba(X)[:,1]
df['w'] = np.where(df['D']==1, 1.0, ps/(1-ps))

mu1 = (df.loc[df.D==1, 'Y'] * df.loc[df.D==1, 'w']).sum() / df.loc[df.D==1, 'w'].sum()
mu0 = (df.loc[df.D==0, 'Y'] * df.loc[df.D==0, 'w']).sum() / df.loc[df.D==0, 'w'].sum()
att = mu1 - mu0
print(att)
```

## Copy-ready formulas

- Definition:
$$
e(X) = \Pr(D=1 \mid X)
$$

- ATE-IPW:
$$
\widehat{ATE} = \frac{1}{N}\sum_i \left[ \frac{D_i Y_i}{\hat e(X_i)} - \frac{(1-D_i)Y_i}{1-\hat e(X_i)} \right]
$$

- ATT-IPW control weights:
$$
w_i =
\begin{cases}
1, & D_i=1 \\
\frac{\hat e(X_i)}{1-\hat e(X_i)}, & D_i=0
\end{cases}
$$

- Stabilized weights (ATE):
$$
SW_i =
\begin{cases}
\frac{P(D=1)}{\hat e(X_i)}, & D_i=1 \\
\frac{P(D=0)}{1-\hat e(X_i)}, & D_i=0
\end{cases}
$$

## Good practice

> [!check] Workflow
> - [ ] Specify pre-treatment covariates; fit flexible PS model.
> - [ ] Diagnose overlap; trim extremes or restrict the target (ATT vs ATE).
> - [ ] Match/weight/stratify; check balance (SMDs, variance ratios, eCDFs).
> - [ ] Consider stabilized weights; report weight diagnostics (min/max/ESS).
> - [ ] Use DR estimators for robustness; cluster SEs when data are clustered.
> - [ ] Pre-register covariates, model classes, calipers/trimming rules.

> [!warning] Common pitfalls
> - Post-treatment adjustment; mixing mediators/colliders into X.
> - Relying on PS alone without checking balance.
> - Severe lack of overlap ignored (huge weights, unstable estimates).
> - Treating high AUC as success (the goal is balance, not prediction).

## Reporting essentials

- Estimand (ATE/ATT), PS model specification (variables, functional forms).
- Balance diagnostics before/after; overlap plots.
- Trimming/caliper rules; stabilized weights; weight summaries and ESS.
- Estimator (matching/IPW/stratification/DR) and variance method.
- Sensitivity analyses (alternative specs, trimming thresholds).

---

## Related notes
- [[Unconfoundedness]]
- [[Overlap]]
- [[matching]]
- [[Inverse Probability Weighting (IPW)|IPW]]
- [[Augmented Inverse Probability Weighting (AIPW)|AIPW]]
- [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]]
- [[Doubly Robust estimators]]
- [[CBPS]]
- [[entropy balancing]]
- [[covariates]]
- [[bad controls]]
- [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]]
- [[Difference-in-Differences (DiD)]]
- [[parallel trends assumption]]
- [[composition]]
- [[clustered standard errors]]
- [[few-cluster corrections]]
- [[stratification|subclassification]]
- [[Love plot]]