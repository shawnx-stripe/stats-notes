---
title: Unconfoundedness
aliases: [unconfoundedness, conditional independence assumption, CIA, selection on observables, conditional exchangeability]
tags: [causal-inference, identification, observables, propensity-score, doubly-robust, dag]
updated: 2025-09-17
---

# Unconfoundedness

> [!summary] Quick definition
> Unconfoundedness (ignorability) assumes that, conditional on observed pre-treatment covariates $X$, treatment assignment $D$ is as good as random:
> $$
> \{Y(1), Y(0)\} \perp D \mid X.
> $$
> Together with [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]] and [[Overlap]] (positivity), it identifies causal effects (e.g., [[Average Treatment Effect (ATE)]], [[Average Treatment Effect on the Treated (ATT)]]) using observed data.

- Also called “selection on observables,” “conditional independence assumption (CIA),” or “conditional exchangeability.”
- Requires that all joint causes of $D$ and $Y$ are included in $X$ and are measured without problematic error.

## Formal statements and implications

### Core assumption
- Conditional independence:
$$
\{Y(1), Y(0)\} \perp D \mid X.
$$

### Positivity/Overlap
- For every $x$ in the support of $X$:
$$
0 < \Pr(D=1 \mid X=x) < 1.
$$

### Identification (g-formula)
- ATE (g-computation):
$$
ATE = \mathbb{E}\big[m_1(X) - m_0(X)\big],\quad m_d(X)=\mathbb{E}[Y \mid D=d,X].
$$

### Propensity score sufficiency
- With the [[propensity score]] $e(X)=\Pr(D=1\mid X)$ (a balancing score):
  - $D \perp X \mid e(X)$ and $\{Y(1),Y(0)\}\perp D \mid e(X)$.
  - Match, weight, or stratify on $e(X)$ instead of the full $X$. See [[propensity score]] and [[matching]].

> [!tip] ATT vs. ATE under ignorability
> - ATE: ignorability must hold for the whole population.
> - ATT: a weaker form suffices, requiring $Y(0) \perp D \mid X$ (plus positivity where controls exist).

## What to condition on

- Include pre-treatment covariates that are common causes of $D$ and $Y$ (confounders).
- Do not include:
  - Post-treatment variables or mediators (see [[bad controls]]).
  - Pure colliders or descendants of colliders (see [[collider bias]] and [[causal DAGs]]).
- Practical tools: use a DAG to decide adjustment sets; consider domain knowledge for confounders.

## Estimation under unconfoundedness

- Outcome regression (g-computation): model $m_d(X)$ and average $\hat m_1(X)-\hat m_0(X)$.
- IPW (inverse probability weighting): weight by $1/\hat e(X)$ or $\hat e(X)/(1-\hat e(X))$; see [[Inverse Probability Weighting (IPW)|IPW]].
- [[Doubly Robust estimators]]:
  - [[Augmented Inverse Probability Weighting (AIPW)|AIPW]]: combines OR and IPW; consistent if either nuisance model is right.
  - [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]]: targeted update of outcome model using the propensity; efficient and bounded.
  - [[double machine learning]] (DML): orthogonal moments with cross-fitting to use ML for nuisances.

> [!warning] Overlap matters
> Severe lack of overlap (extreme propensities/weights) can make estimates unstable. Consider trimming, stabilized/overlap weights, or redefining the target sample.

## Diagnostics and sensitivity

> [!check] After fitting, examine:
> - Balance in $X$ between treated and controls (standardized mean differences, variance ratios, eCDFs) after matching/weighting.
> - Propensity overlap (histograms/densities), weight summaries (min/median/max, ESS).
> - Robustness to alternative PS/OR specifications, trimming thresholds, and learner libraries (for ML).

> [!tip] Sensitivity to unobserved confounding
> Unconfoundedness is untestable. Use sensitivity analyses:
> - [[Rosenbaum sensitivity]] bounds for matched designs.
> - Oster’s $\delta$ (coefficient stability), Altonji–Elder–Taber style checks.
> - Negative controls if available.

## Relation to other designs

- Randomized experiments: ignorability holds by design without conditioning (given successful randomization and no attrition bias).
- [[Difference-in-Differences (DiD)]]: relies on [[parallel trends assumption]], not ignorability. Conditional DiD assumes parallel trends given $X$.
- [[Instrumental Variables (IV)]]: does not require unconfoundedness; instead needs [[exclusion restriction]] and [[monotonicity]] to identify [[Local Average Treatment Effect (LATE)|LATE]].
- [[Regression Discontinuity Design (RDD)]]: relies on continuity at a cutoff rather than ignorability given $X$.

## Time-varying treatments

- “Sequential unconfoundedness” (longitudinal): at each time, treatment is as good as random given past observed history (treatments and covariates). Identification via g-methods:
  - Marginal Structural Models with IPTW, [[LTMLE]] (longitudinal TMLE), or g-formula with proper time ordering.

## Common pitfalls

> [!warning] Avoid these
> - Using post-treatment variables in $X$ (bad controls).
> - Ignoring measurement error in key confounders (can reintroduce bias).
> - Overly rigid parametric models for $m_d$ or $e$ without checks.
> - Poor overlap and extreme weights without trimming or stabilization.
> - Treating balance on a limited set of moments as proof of ignorability.

## Minimal code snippets

> [!example] R: AIPW (ATE) with checks

```r
# Propensity model
ps_mod <- glm(D ~ X1 + X2 + poly(X3,2) + X1:X2, data = df, family = binomial())
ps <- pmax(pmin(ps_mod$fitted.values, 0.995), 0.005)

# Outcome models
m1 <- lm(Y ~ X1 + X2 + poly(X3,2) + X1:X2, data = subset(df, D==1))
m0 <- lm(Y ~ X1 + X2 + poly(X3,2) + X1:X2, data = subset(df, D==0))
m1hat <- predict(m1, newdata = df); m0hat <- predict(m0, newdata = df)

# AIPW ATE
aipw <- mean((m1hat - m0hat) + df$D*(df$Y - m1hat)/ps - (1-df$D)*(df$Y - m0hat)/(1-ps))

# Balance diagnostics (cobalt)
library(cobalt)
w <- ifelse(df$D==1, 1, ps/(1-ps))
bal.tab(df$D, df[,c("X1","X2","X3")], weights = w, estimand = "ATT", method = "weighting")
```

> [!example] Stata: IPW and AIPW

```stata
logit D X1 X2 c.X3##c.X3 c.X1#c.X2
predict ps, pr
teffects ipw (Y) (D X1 X2 c.X3##c.X3), ate vce(robust)
teffects aipw (Y X1 X2 c.X3##c.X3) (D X1 X2 c.X3##c.X3), ate vce(robust)
```

> [!example] Python: DR learner (ATE)

```python
from econml.dr import DRLearner
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestRegressor

Y = df['Y'].values
T = df['D'].values
X = df[['X1','X2','X3']].values

dr = DRLearner(model_propensity=LogisticRegression(max_iter=2000),
               model_regression=RandomForestRegressor(random_state=123),
               random_state=123)
dr.fit(Y, T, X=X)
ate = dr.ate(X).mean()
print(ate)
```

## Copy-ready formulas

- Ignorability:
$$
\{Y(1), Y(0)\} \perp D \mid X
$$
- Overlap:
$$
0 < \Pr(D=1 \mid X=x) < 1 \ \text{for all } x
$$
- g-formula (ATE):
$$
ATE = \mathbb{E}\big[\mathbb{E}[Y \mid D=1,X] - \mathbb{E}[Y \mid D=0,X]\big]
$$
- ATE-IPW:
$$
\widehat{ATE} = \frac{1}{N}\sum_{i}\left(\frac{D_iY_i}{\hat e(X_i)} - \frac{(1-D_i)Y_i}{1-\hat e(X_i)}\right)
$$

## Reporting essentials

- Define target estimand (ATE/ATT) and population.
- List covariates used for adjustment and justify their pre-treatment status and causal role (use a DAG).
- Show balance/overlap diagnostics and any trimming/clipping rules.
- Specify estimator (OR, IPW, [[Doubly Robust estimators]] like [[Augmented Inverse Probability Weighting (AIPW)|AIPW]]/[[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]]/[[double machine learning]]) and inference (SEs; clustering if applicable).
- Provide sensitivity analysis to unobserved confounding.

---

## Related notes
- [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]]
- [[Overlap]]
- [[propensity score]]
- [[matching]]
- [[Inverse Probability Weighting (IPW)|IPW]]
- [[Augmented Inverse Probability Weighting (AIPW)|AIPW]]
- [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]]
- [[Doubly Robust estimators]]
- [[double machine learning]]
- [[Average Treatment Effect (ATE)]]
- [[Average Treatment Effect on the Treated (ATT)]]
- [[bad controls]]
- [[collider bias]]
- [[causal DAGs]]
- [[Rosenbaum sensitivity]]
- [[Oster’s delta]]
- [[Difference-in-Differences (DiD)]]
- [[parallel trends assumption]]
- [[Instrumental Variables (IV)]]
- [[exclusion restriction]]
- [[Local Average Treatment Effect (LATE)|LATE]]
- [[sequential ignorability|sequential unconfoundedness]]
- [[Marginal Structural Models (MSM)]]
- [[Inverse Probability Weighting (IPW)|IPTW]]
- [[LTMLE]]
