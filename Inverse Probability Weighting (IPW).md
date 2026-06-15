---
title: Inverse Probability Weighting (IPW)
aliases:
- IPW
- inverse propensity weighting
- Horvitz–Thompson weighting
- IPTW
- inverse probability weighting
- Inverse Probability Weighting (IPW)
tags:
- causal-inference
- weighting
- propensity-score
- ate
- att
- diagnostics
- dr
updated: 2025-09-17
---

# Inverse Probability Weighting (IPW)

> [!summary] Quick definition
> IPW estimates causal effects by reweighting observations with the inverse of their treatment probabilities (the [[propensity score]]), creating a pseudo-population where treatment is independent of covariates. Under [[Unconfoundedness]], [[Overlap]], and [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]], IPW identifies [[Average Treatment Effect (ATE)]] or [[Average Treatment Effect on the Treated (ATT)]].

- ATE weights emphasize underrepresented treatment arms.
- ATT weights emphasize making controls resemble the treated group.

## Assumptions

- [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]] (no interference; well-defined treatment)
- [[Unconfoundedness]]: {Y(1), Y(0)} ⟂ D | X
- [[Overlap]] (positivity): 0 < e(X) < 1 almost surely, where e(X) = P(D=1|X)

## Core notation

- D ∈ {0,1}: treatment
- X: pre-treatment [[covariates]]
- Y: outcome
- e(X) = P(D=1|X): [[propensity score]]

## IPW estimators (copy-ready)

### ATE (Horvitz–Thompson and Hájek)

- Horvitz–Thompson (unnormalized):
$$
\widehat{ATE}_{HT} = \frac{1}{N}\sum_{i=1}^N\left[\frac{D_i Y_i}{\hat e(X_i)} - \frac{(1-D_i)Y_i}{1-\hat e(X_i)}\right]
$$

- Hájek (normalized; usually more stable):
$$
\widehat{ATE}_{H\acute{a}jek} =
\frac{\sum_i \frac{D_i Y_i}{\hat e(X_i)}}{\sum_i \frac{D_i}{\hat e(X_i)}}
-
\frac{\sum_i \frac{(1-D_i) Y_i}{1-\hat e(X_i)}}{\sum_i \frac{(1-D_i)}{1-\hat e(X_i)}}
$$

- Stabilized weights (variance reduction; ATE):
$$
SW_i=
\begin{cases}
\displaystyle \frac{\hat p}{\hat e(X_i)}, & D_i=1\\[6pt]
\displaystyle \frac{1-\hat p}{1-\hat e(X_i)}, & D_i=0
\end{cases}
\quad \text{with } \hat p=\frac{1}{N}\sum_i D_i
$$

### ATT

- Weights:
$$
w_i =
\begin{cases}
1, & D_i=1\\[4pt]
\displaystyle \frac{\hat e(X_i)}{1-\hat e(X_i)}, & D_i=0
\end{cases}
$$

- ATT estimator (difference in weighted means):
$$
\widehat{ATT} =
\frac{\sum_{i:D_i=1} Y_i}{\sum_{i:D_i=1} 1}
-
\frac{\sum_{i:D_i=0} \frac{\hat e(X_i)}{1-\hat e(X_i)} Y_i}{\sum_{i:D_i=0} \frac{\hat e(X_i)}{1-\hat e(X_i)}}
$$

## Estimation steps

> [!check] Workflow
> - [ ] Choose estimand (ATE vs. ATT) and target population.
> - [ ] Specify pre-treatment X (avoid [[bad controls]]) and estimate e(X) with flexible models (logit/probit or ML).
> - [ ] Compute IPW (stabilized if ATE); assess [[Overlap]] and weight stability.
> - [ ] Estimate effect (HT or Hájek) and use appropriate SEs (robust; [[clustered standard errors]] if needed).
> - [ ] Check post-weighting balance (SMDs, variance ratios, eCDFs).

## Diagnostics and overlap

> [!check] Inspect
> - Propensity overlap: histograms/densities of $\hat e(X)$ by D.
> - Weight distribution: min/median/max, tail shares (e.g., > 10, > 20).
> - Effective sample size (ESS):
$$
ESS = \frac{\left(\sum_i w_i\right)^2}{\sum_i w_i^2}
$$
> - Covariate balance after weighting (target |SMD| < 0.1).

> [!tip] Remedies for poor overlap
> - Trimming/truncation: keep $\alpha \le \hat e(X) \le 1-\alpha$ (e.g., α ∈ [0.01, 0.05]).
> - Stabilized or overlap weights (for ATE on the overlap population: treated weights ∝ 1−e, controls ∝ e).
> - Consider [[entropy balancing]] for deterministic moment balance.
> - Switch estimand (e.g., ATT) or design if overlap is fundamentally absent.

## IPW vs. AIPW/TMLE

- [[Augmented Inverse Probability Weighting (AIPW)|AIPW]] and [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]] are [[Doubly Robust estimators]] that combine IPW with outcome regression, yielding consistency if either model is correct and often better efficiency.
- Plain IPW relies solely on $\hat e(X)$; more sensitive to model misspecification and extreme weights.

## Variants and extensions

- Survey/data with base weights: estimate e(X) with design weights and multiply final analysis weight by base weight × IPW; normalize (Hájek) within groups. Report how you combined weights.
- Multi-valued/continuous treatment: use generalized propensity scores; IPW generalizes but requires adapted estimation and diagnostics.
- Panels/DiD: IPW can reweight controls to treated-like pre-period composition; for identification in DiD, prefer DR-DiD methods (see [[Augmented Inverse Probability Weighting (AIPW)|AIPW]] and [[Callaway–Sant’Anna estimator]]).

## Inference

- Use robust (sandwich) SEs; cluster by assignment or panel unit where appropriate; apply [[few-cluster corrections]] if clusters are few.
- Bootstrap with resampling at the appropriate cluster level when design dictates.
- For Hájek estimators, delta-method or bootstrap is common; many software functions handle this automatically.

## Minimal code snippets

> [!example] R: ATE-IPW and ATT-IPW with diagnostics

```r
# PS model
ps_mod <- glm(D ~ X1 + X2 + poly(X3,2) + X1:X2, family = binomial(), data = df)
ps <- pmax(pmin(ps_mod$fitted.values, 0.995), 0.005)

# ATE weights (stabilized)
p <- mean(df$D)
w_ate <- ifelse(df$D==1, p/ps, (1-p)/(1-ps))

# Hájek ATE
mu1 <- sum((df$D * df$Y)/ps) / sum(df$D/ps)
mu0 <- sum(((1-df$D) * df$Y)/(1-ps)) / sum((1-df$D)/(1-ps))
ate_hajek <- mu1 - mu0

# ATT weights
w_att <- ifelse(df$D==1, 1, ps/(1-ps))
att <- (with(df, sum(Y[D==1]) / sum(D==1))) -
       (with(df, sum(Y[D==0] * w_att[D==0]) / sum(w_att[D==0])))

# Balance diagnostics (cobalt)
library(cobalt)
bal.tab(df$D, df[,c("X1","X2","X3")], weights = w_att, estimand = "ATT", method = "weighting")
```

> [!example] Stata: ATE/ATT via teffects ipw

```stata
* Propensity and IPW (built-in)
teffects ipw (Y) (D X1 X2 c.X3##c.X3), ate vce(robust)
teffects ipw (Y) (D X1 X2 c.X3##c.X3), atet vce(robust)

* Extract and inspect weights (pscore + manual)
logit D X1 X2 c.X3##c.X3
predict ps, pr
gen w_att = cond(D==1, 1, ps/(1-ps))
sum w_att
```

> [!example] Python: ATE-Hájek and ATT-IPW (sketch)

```python
import numpy as np
from sklearn.linear_model import LogisticRegression

X = df[['X1','X2','X3']].values
D = df['D'].values
Y = df['Y'].values

ps = LogisticRegression(max_iter=2000).fit(X, D).predict_proba(X)[:,1]
ps = np.clip(ps, 0.005, 0.995)

# ATE Hájek
mu1 = ((D*Y)/ps).sum() / (D/ps).sum()
mu0 = (((1-D)*Y)/(1-ps)).sum() / (((1-D)/(1-ps))).sum()
ate = mu1 - mu0

# ATT
w_att = np.where(D==1, 1.0, ps/(1-ps))
mu1_t = Y[D==1].mean()
mu0_cw = (Y[D==0]*w_att[D==0]).sum() / w_att[D==0].sum()
att = mu1_t - mu0_cw
print(ate, att)
```

## Good practice and pitfalls

> [!check] Best practices
> - [ ] Rich, pre-treatment X; allow nonlinearities/interactions (or ML).
> - [ ] Clip/truncate extreme PS (e.g., to [0.01, 0.99]); consider stabilized/overlap weights.
> - [ ] Report balance after weighting and weight diagnostics (min/max, ESS).
> - [ ] Use [[Augmented Inverse Probability Weighting (AIPW)|AIPW]]/[[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]] if robustness/efficiency is a concern.

> [!warning] Avoid these
> - Using post-treatment variables in the PS (see [[bad controls]]).
> - Proceeding with severe lack of overlap (huge/unbounded weights) without trimming or redefining the estimand.
> - Relying on predictive AUC of the PS instead of checking covariate balance.
> - Ignoring clustering/serial correlation in SEs.

## Copy-ready snippets

- ATE (HT):
$$
\widehat{ATE}_{HT} = \frac{1}{N}\sum_i\left[\frac{D_i Y_i}{\hat e(X_i)} - \frac{(1-D_i)Y_i}{1-\hat e(X_i)}\right]
$$

- ATE (Hájek):
$$
\widehat{ATE}_{H\acute{a}jek} =
\frac{\sum_i \frac{D_i Y_i}{\hat e(X_i)}}{\sum_i \frac{D_i}{\hat e(X_i)}} -
\frac{\sum_i \frac{(1-D_i)Y_i}{1-\hat e(X_i)}}{\sum_i \frac{(1-D_i)}{1-\hat e(X_i)}}
$$

- ATT weights:
$$
w_i = \mathbf{1}\{D_i=1\} + \mathbf{1}\{D_i=0\}\cdot \frac{\hat e(X_i)}{1-\hat e(X_i)}
$$

- Effective sample size:
$$
ESS = \frac{\left(\sum_i w_i\right)^2}{\sum_i w_i^2}
$$

## Reporting essentials

- Estimand (ATE/ATT), PS model specification (variables, forms, learners), and whether stabilization/trimming was used.
- Overlap and weight diagnostics (plots, min/max, ESS) and post-weighting balance.
- SEs and inference details (robust/clustered; [[few-cluster corrections]] if applicable).
- Sensitivity to trimming thresholds, alternative PS models, and alternative weighting schemes (stabilized, overlap).
- If survey weights exist, how they were combined with IPW.

---

## Related notes
- [[Average Treatment Effect (ATE)]]
- [[Average Treatment Effect on the Treated (ATT)]]
- [[propensity score]]
- [[Unconfoundedness]]
- [[Overlap]]
- [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]]
- [[Augmented Inverse Probability Weighting (AIPW)|AIPW]]
- [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]]
- [[Doubly Robust estimators]]
- [[entropy balancing]]
- [[matching]]
- [[bad controls]]
- [[clustered standard errors]]
- [[few-cluster corrections]]
- [[Difference-in-Differences (DiD)]]
- [[Callaway–Sant’Anna estimator]]