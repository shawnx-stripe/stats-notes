---
title: Hypothesis testing
aliases: [statistical hypothesis testing, testing, significance testing, null-hypothesis significance testing, NHST]
tags: [statistics, econometrics, inference, hypothesis-testing, power, multiple-testing, sequential]
updated: 2025-09-17
---

# Hypothesis testing

> [!summary] Quick definition
> Hypothesis testing assesses whether data provide sufficient evidence against a null hypothesis (H0) in favor of an alternative (H1). A test computes a statistic and a p-value (or compares to a critical value) given a pre-specified significance level α. Decisions trade off Type I error (false positive) and power (1−β). Modern practice emphasizes effect sizes, confidence intervals, assumptions, and multiplicity/peeking control.

- Core elements: H0/H1, test statistic, sampling distribution under H0, significance α, p-value/critical region, power (1−β), assumptions.
- Complements: effect size estimation, confidence intervals, [[power analysis]], [[multiple testing control]], [[sequential testing]].

---

## Key concepts

- Null hypothesis H0 and alternative H1 (one- or two-sided)
- Type I error (α): reject H0 when H0 true
- Type II error (β): fail to reject when H1 true; power = 1 − β
- P-value: probability, under H0, of a result at least as extreme as observed
- Confidence interval (CI): family of acceptance regions inverted across parameter values
- Assumptions: distributional (e.g., normality), independence, correct variance structure; violations require robust methods

> [!warning] Interpretation
> - A small p-value does not measure effect size or practical importance.
> - Failing to reject H0 is not proof H0 is true (may be underpowered).

---

## Families of tests

- Parametric (assume specific forms)
  - z-test (known variance / large n), t-test (unknown variance), χ² tests (variance; contingency tables), F-test (variance ratios, ANOVA)
- Nonparametric / rank-based
  - Wilcoxon/Mann–Whitney, Wilcoxon signed-rank, Kruskal–Wallis, Kolmogorov–Smirnov
- Regression/M-estimation-based
  - [[Wald, LM, and LR tests]] for linear and generalized linear models; joint tests; specification checks
- Resampling/design-based
  - [[randomization inference]] (permutation tests), bootstrap-based tests (studentized/percentile)

---

## Common testing scenarios

- One mean (one-sample t), two means (two-sample t: equal/unequal variances), paired mean (paired t)
- One proportion (binomial test), two proportions (z-test for proportions)
- Multiple means: ANOVA / regression F-tests; post-hoc with multiplicity control
- Contingency tables: χ² test of independence, Fisher’s exact (small counts)
- Regression coefficients: t/Wald tests; joint restrictions via χ²/F; robust [[clustered standard errors]] for dependence

---

## Test design choices

- One- vs two-sided alternatives
  - Two-sided: H1: θ ≠ θ0 (default when direction uncertain)
  - One-sided: H1: θ > θ0 or θ < θ0 (pre-specify; more power if correct)
- Significance level α (e.g., 0.05) and target power 1−β (e.g., 0.8) → plan via [[power analysis]] and target [[Minimum Detectable Effect (MDE)|MDE]]
- Assumptions and robustness
  - If heteroskedasticity/cluster dependence: use robust/clustered/HAC variances
  - If skew/heavy tails/small n: consider nonparametric tests or transformations
- Many tests or peeking
  - Control [[multiple testing control]] (FWER/FDR)
  - Use [[sequential testing]] for interim looks

---

## Canonical formulas (copy-ready)

- Two-sample t-test (unequal variances, Welch)
$$
t = \frac{\bar X_1 - \bar X_0}{\sqrt{\frac{s_1^2}{n_1}+\frac{s_0^2}{n_0}}},\quad
\text{df} \ \text{via Welch–Satterthwaite}.
$$

- Proportions difference (large-sample z)
$$
z = \frac{\hat p_1 - \hat p_0}{\sqrt{\frac{\hat p_1(1-\hat p_1)}{n_1}+\frac{\hat p_0(1-\hat p_0)}{n_0}}}.
$$

- χ² test (contingency K×L)
$$
\chi^2 = \sum_{k,\ell}\frac{(O_{k\ell}-E_{k\ell})^2}{E_{k\ell}},\ \ E_{k\ell}=\frac{(\text{row}_k)(\text{col}_\ell)}{N}.
$$

- Regression Wald (linear restrictions Rθ=r)
$$
W = (R\hat\theta - r)^\top [R\,\widehat{\mathrm{Var}}(\hat\theta)\,R^\top]^{-1}(R\hat\theta - r)\sim\chi^2_q.
$$

- Likelihood Ratio
$$
LR = 2\big(\ell(\hat\theta) - \ell(\tilde\theta)\big)\sim\chi^2_q
$$

- LM/Score (at restricted θ̃)
$$
LM = S(\tilde\theta)^\top \widehat I(\tilde\theta)^{-1} S(\tilde\theta)\sim\chi^2_q.
$$

---

## Workflow (practical)

> [!check]
> - [ ] Define estimand and hypotheses (one/two-sided); set α and target power  
> - [ ] Choose test/statistic consistent with design and assumptions  
> - [ ] Pre-specify families and [[multiple testing control]]; sequential plan if peeking  
> - [ ] Compute test using appropriate variance (robust/cluster/HAC as needed)  
> - [ ] Report effect size, CI, p-value, and diagnostic checks  
> - [ ] Interpret in context (practical significance); document limitations

---

## Robust inference choices

- Heteroskedasticity: HC (White) sandwich SEs
- Cluster dependence: [[clustered standard errors]]; with few clusters, use [[few-cluster corrections]] or [[wild cluster bootstrap]]
- Serial correlation: [[Newey–West]] HAC
- Spatial dependence: [[Conley standard errors]]

---

## Equivalence and non-inferiority

- Non-inferiority: H0: θ ≤ −m vs H1: θ > −m (margin m); pass if lower CI bound > −m
- Equivalence (TOST): test H0a: θ ≤ −m and H0b: θ ≥ m; reject both (two one-sided tests) to claim |θ| < m
- Common in guardrail/[[Overall Evaluation Criterion (OEC)|OEC]] contexts; pre-specify margins

---

## Resampling and design-based alternatives

- [[randomization inference]] for exact p-values under known assignment (few clusters, blocked/matched designs, switchbacks, saturation)
- Bootstrap CI/tests for complex stats (ratios/quantiles); use cluster/block bootstrap if dependence

---

## Interpretation and reporting

> [!check] Report
> - Test type (t/z/χ²/F/Wald/LM/LR/permutation) and sidedness
> - Assumptions and variance method (iid/robust/cluster/HAC), clustering level; small-G corrections if any
> - Effect size and units; 95% CI; p-value
> - If many tests: family definition and adjustment method ([[False Discovery Rate (FDR)|FDR]]/Holm/Bonferroni)
> - If interim looks: sequential method used
> - Diagnostics: normality/variance checks (if relevant), balance/overlap for causal designs

---

## Pitfalls

> [!warning]
> - P-hacking: outcome switching, subgroup mining without [[multiple testing control]]  
> - Optional stopping without [[sequential testing]]  
> - Using parametric tests under severe assumption violations without robustness  
> - Interpreting “non-significant” as “no effect” (often underpowered)  
> - Confusing statistical with practical significance  
> - Ignoring dependence (using iid SEs when clustering/time/spatial dependence exists)

---

## Code snippets

> [!example] R

```r
# Two-sample t-test (Welch)
t.test(Y ~ D, data = df, var.equal = FALSE)

# Two proportions
prop.test(x = c(x1, x0), n = c(n1, n0), correct = FALSE)

# χ² test of independence
tbl <- table(df$g, df$h); chisq.test(tbl)

# Regression Wald joint test (robust SEs)
library(sandwich); library(lmtest)
fit <- lm(Y ~ X1 + X2 + X3, data = df)
co <- vcovHC(fit, type = "HC1")
waldtest(fit, vcov = co, R = rbind(c(0,0,1,0), c(0,0,0,1)))
```

> [!example] Python

```python
import numpy as np, pandas as pd
from scipy import stats
import statsmodels.formula.api as smf

# Welch t-test
stats.ttest_ind(df.loc[df.D==1,'Y'], df.loc[df.D==0,'Y'], equal_var=False)

# Two proportions (normal approx)
p1, p0 = x1/n1, x0/n0
se = np.sqrt(p1*(1-p1)/n1 + p0*(1-p0)/n0)
z = (p1 - p0)/se
p = 2*(1-stats.norm.cdf(abs(z)))

# Regression and robust Wald
res = smf.ols('Y ~ X1 + X2 + X3', data=df).fit(cov_type='HC1')
print(res.summary())
```

> [!example] Stata

```stata
* Welch t-test
ttest Y, by(D) unequal

* Two proportions
prtest p1 = p0

* χ² test
tab g h, chi2

* Regression with clustered SEs and joint test
reg Y X1 X2 X3, vce(cluster cluster_id)
test X2 X3
```

---

## Links to design-specific testing

- Causal panels/DiD: joint pre-trend tests, event-study Wald tests; use [[Callaway–Sant’Anna estimator]] / [[Sun–Abraham estimator]] and cluster-aware inference
- Experiments: non-inferiority for guardrails; AA checks, [[Sample Ratio Mismatch (SRM)|SRM]]; use [[sequential testing]] if peeking
- IV: use weak-IV-robust tests (e.g., [[Anderson–Rubin|Anderson–Rubin test]]) when relevance is weak

---

## Related notes

- [[power analysis]] · [[Minimum Detectable Effect (MDE)|MDE]]
- [[multiple testing control]] · [[False Discovery Rate (FDR)|FDR]] · [[sequential testing]]
- [[Wald, LM, and LR tests]]
- [[randomization inference]]
- [[clustered standard errors]] · [[few-cluster corrections]] · [[Newey–West]] · [[Conley standard errors]]
- [[Experimental Design (MOC)]] · [[AB Testing (MOC)]]
- [[Difference-in-Differences (DiD)]] · [[event study]]

---