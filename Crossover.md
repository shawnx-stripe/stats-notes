---
title: Crossover
aliases: [crossover trial, cross-over, 2x2 crossover, AB/BA design, N-of-1 trial, Williams design]
tags: [experimentation, design, rct, crossover, within-subject, carryover, washout, mixed-models, power]
updated: 2025-09-17
---

# Crossover

> [!summary] Quick definition
> A crossover trial assigns each subject (or cluster) to multiple treatments in different time periods (e.g., AB/BA), allowing each subject to serve as their own control. This can substantially improve precision by removing between-subject variability. Correct design requires adequate washout to mitigate carryover effects and analysis that accounts for period/sequence effects and within-subject correlation.

- Common designs: 2×2 AB/BA, 3×3 Latin/Williams sequences (ABC/BCA/CAB), N-of-1.
- Use when: outcomes respond quickly and wash out, treatment effects are reversible, and within-subject comparison is meaningful.

---

## When to use (and when not)

> [!tip] Use when
> - Treatment effect is reversible and short-lived relative to period length.
> - Adequate washout is feasible between periods.
> - Between-subject heterogeneity is high; within-subject control boosts power.
> - Outcomes can be repeatedly measured reliably per subject/cluster.

> [!warning] Avoid/consider alternatives when
> - Irreversible or long-acting effects; strong carryover cannot be mitigated.
> - Progressive disease or secular trends dominate (unstable baselines).
> - Severe period effects or learning/novelty effects that differ by treatment.
> - Substantial attrition over periods.

Related: [[switchback experiment]] (time-sliced at system level), cluster crossover/stepped-wedge (cluster-level rollouts).

---

## Basic 2×2 crossover (AB/BA)

- Sequences: S1: A→B; S2: B→A.
- Periods: typically two, separated by washout.
- Randomization: allocate subjects to sequences S1/S2 (often 1:1).
- Measurements: outcome at end of each period (or repeatedly within period).

Modeling framework (continuous outcome):
- Fixed effects: treatment, period, sequence; random subject intercept.
- Optionally test for carryover (treatment from previous period).

---

## Extended designs

- 3+ treatments: Latin square or Williams designs balance first-order carryover and period effects.
- N-of-1: single subject receives A/B repeatedly (ABAB…); analyze within-subject with time-series methods.
- Cluster crossover: units are clusters (e.g., hospitals, geos), not individuals; analyze with cluster mixed models and cluster-level variance.

---

## Assumptions

- No (or negligible) carryover after washout (or adequately modeled).
- Stable condition across periods aside from treatment (control period/sequence effects).
- No differential time trends across sequences beyond modeled period/sequence terms.
- SUTVA within subject/cluster periods; no interference across subjects/clusters.

---

## Analysis methods

### 1) 2×2 crossover mixed model (continuous Y)
A standard analysis includes:
- Fixed: treatment (A vs B), period (1 vs 2), sequence (AB vs BA).
- Random: subject intercept (and optionally subject-by-period slopes).
- Optionally include carryover (previous treatment) as a sensitivity check.

Treatment effect is the adjusted difference in means accounting for period/sequence; precision benefits from within-subject pairing.

### 2) ANOVA approach (balanced)
Classical AB/BA ANOVA with terms for sequence, subject(sequence), period, treatment; less flexible than mixed models.

### 3) GLMMs for non-Gaussian outcomes
Use logistic/Poisson/negative binomial mixed models with the same fixed/random structure.

### 4) Cluster crossover
Mixed models with random intercepts at subject and cluster if applicable, or random cluster-period effects; cluster-robust inference.

> [!warning] Carryover
> Routine inclusion and testing of carryover terms is debated (Senn). Prefer strong design/washout; treat carryover modeling as sensitivity rather than definitive test.

---

## Minimal code snippets

> [!example] R: 2×2 crossover mixed model (lme4/lmerTest)

```r
# df: subject, sequence (AB/BA), period (1/2), trt (A/B), Y
library(lme4); library(lmerTest)
df$trt <- relevel(factor(df$trt), "A")
df$period <- factor(df$period)
df$sequence <- factor(df$sequence)

# Mixed model: fixed = trt + period + sequence, random = subject intercept
fit <- lmer(Y ~ trt + period + sequence + (1 | subject), data = df)
summary(fit)  # trtB coefficient is treatment effect (B vs A)

# Optional carryover term (previous treatment)
df <- df[order(df$subject, df$period), ]
df$carry <- ave(as.character(df$trt), df$subject, FUN = function(z) c(NA, head(z, -1)))
fit_carry <- lmer(Y ~ trt + period + sequence + carry + (1 | subject), data = df)
summary(fit_carry)
```

> [!example] Stata: 2×2 crossover mixed model

```stata
* subject id, sequence (AB/BA), period (1/2), trt (A/B), outcome Y
encode trt, gen(trt_f)
encode sequence, gen(seq_f)
mixed Y i.trt_f i.period i.seq_f || subject:, variance
* Treatment effect: coefficient on trt_f (B vs A)
```

> [!example] Python: mixedlm (statsmodels)

```python
import statsmodels.formula.api as smf
df['trt'] = df['trt'].astype('category')
df['period'] = df['period'].astype('category')
df['sequence'] = df['sequence'].astype('category')

fit = smf.mixedlm("Y ~ C(trt) + C(period) + C(sequence)", data=df, groups=df["subject"]).fit()
print(fit.summary())
```

> [!example] R: Binary outcome (logistic GLMM)

```r
library(lme4)
fit_glmm <- glmer(Y ~ trt + period + sequence + (1 | subject), data = df, family = binomial)
summary(fit_glmm)
```

---

## Washout and carryover

- Washout period: interval long enough for treatment effect to dissipate (based on pharmacokinetics/system dynamics).
- Diagnostics:
  - Compare baseline levels at start of each period.
  - Include carryover indicators as sensitivity (previous treatment).
  - Look for treatment-by-period interactions indicating asymmetric effects.

> [!warning] If carryover is significant and cannot be mitigated, prefer parallel-group RCT or analyze only first period (loses crossover benefit).

---

## Period and sequence effects

- Period: calendar/time effects or learning/adaptation between periods; always include period fixed effects.
- Sequence: structural differences between AB and BA sequences; include to guard against confounding.

---

## Power and sample size

- Gains: crossover reduces required N for a given MDE due to within-subject control; effect depends on within-subject correlation ρ.
- Heuristic (continuous outcome):
  - Variance of within-subject difference ∝ σ²(1−ρ); higher ρ ⇒ larger gains.
- Calculators: dedicated crossover power formulas (e.g., 2×2 AB/BA), or simulate mixed models based on expected ρ, σ², and period length.

See [[power analysis]] and [[Minimum Detectable Effect (MDE)|MDE]] for planning considerations; incorporate period/sequence and carryover assumptions.

---

## Cluster crossover and stepped-wedge

- Cluster crossover: similar modeling, but randomization and inference at cluster level; use cluster-period random effects.
- Stepped-wedge: all clusters start control then sequentially cross over to treatment; analyze with DiD/mixed models; see [[staggered adoption]] and [[Difference-in-Differences (DiD)]].

---

## Practical considerations

- Pre-registration: specify sequences, washout length, primary endpoint, mixed model structure, handling of carryover, period effects, multiplicity (if multiple endpoints), and any interim looks ([[pre-registration]] · [[sequential testing]]).
- CONSORT: use appropriate CONSORT extension for crossover; report sequence allocation, period outcomes, attrition per period ([[Consolidated Standards of Reporting Trials (CONSORT)|CONSORT]]).
- Logging: for digital trials, log assignment at period start, exposure windows, and adherence; align time zones and [[seasonality]].

---

## Diagnostics and reporting

> [!check]
> - [ ] Balance: baseline comparability across sequences at period start  
> - [ ] Period effects modeled (FE), sequence effects included  
> - [ ] Carryover sensitivity (washout adequacy)  
> - [ ] Within-subject correlation handled via random effects  
> - [ ] Robustness: alternative washout, removing first post-switch window, modeling treatment×period interaction  
> - [ ] Attrition across periods; ITT as primary, per-protocol secondary

---

## Common pitfalls

> [!warning]
> - Inadequate washout leading to biased within-subject contrast  
> - Ignoring period or sequence effects in analysis  
> - Treating correlated observations as independent (underestimated SEs)  
> - Substantial attrition causing imbalance between sequences/periods  
> - Differential time trends between sequences (e.g., seasonality misalignment)

---

## Related notes

- [[Experimental Design (MOC)]] · [[AB Testing (MOC)]]  
- [[switchback experiment]] · [[geo experiment]] · [[staggered adoption]]  
- [[Analysis of Covariance (ANCOVA)|ANCOVA]] · [[Controlled Experiments Using Pre-Experiment Data (CUPED)|CUPED]] (baseline adjustment within subjects)  
- [[clustered standard errors]] · [[few-cluster corrections]]  
- [[pre-registration]] · [[Consolidated Standards of Reporting Trials (CONSORT)|CONSORT]]

---