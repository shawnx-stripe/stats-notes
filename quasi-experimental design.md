---
title: Quasi-Experimental Design
aliases: [quasi-experiments, quasi-experimental methods]
tags: [causal-inference, econometrics, methods, design]
updated: 2025-09-17
---

# Quasi-Experimental Design

> [!summary] Quick definition
> Designs that aim to estimate causal effects without explicit randomization, leveraging as-if random variation, discontinuities, timing, or structural assumptions to identify effects.

- Goal: estimate effects like [[Average Treatment Effect (ATE)]] or [[Average Treatment Effect on the Treated (ATT)]].
- Frameworks: [[potential outcomes]], [[causal DAGs]].
- Key trade-off: stronger assumptions than RCTs, but often greater feasibility and external validity in real-world policy settings.

## Why quasi-experimental?

- Randomized experiments may be infeasible, unethical, or too costly.
- Policies and shocks create natural variation that can mimic random assignment under credible assumptions.
- Emphasis on research design first, estimation second.

## Core identification assumptions (generic)

- [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]]: well-defined treatment, no hidden variation; no interference/spillovers unless modeled.
- [[Unconfoundedness]] or design-specific identifying assumptions (e.g., [[parallel trends assumption]] in DiD, local randomization in RDD).
- [[Overlap]]/positivity: units have non-zero probability of each treatment status within covariate support.
- Correct temporal ordering: treatment precedes outcomes.
- No severe measurement or selection biases that invalidate identification.

> [!equation] Potential outcomes view
> - ATE = E[Y(1) − Y(0)]
> - Ignorability example: {Y(1), Y(0)} ⫫ T | X
> - Overlap: 0 < P(T = 1 | X) < 1

## Major families of quasi-experimental designs

### Designs exploiting time and groups
- [[Difference-in-Differences (DiD)]]: compare changes over time in treated vs. control groups. Assumption: [[parallel trends assumption]].
- [[Interrupted Time Series (ITS)]]: structural break at intervention time within a treated unit; often improved with a comparison series.
- [[Synthetic Control]]: constructs a weighted combination of controls to approximate the treated unit’s pre-treatment path.

### Designs exploiting thresholds or rules
- [[Regression Discontinuity Design (RDD)]]: treatment assigned by a cutoff on a running variable; effect identified locally at the cutoff. Requires no precise manipulation and smooth potential outcomes at the threshold.

### Designs exploiting exogenous variation
- [[Instrumental Variables (IV)]]: instrument Z affects treatment T but has no direct effect on Y except through T and is independent of potential outcomes. Requires [[relevance]] and [[exclusion restriction]], often [[monotonicity]] for LATE.

### Selection on observables
- [[Propensity Score Matching (PSM)]], [[Inverse Probability Weighting (IPW)|Inverse Probability Weighting (IPW)]], [[Doubly Robust estimators]] like [[Augmented Inverse Probability Weighting (AIPW)|AIPW]] or [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]]. Assumption: [[Unconfoundedness|unconfoundedness]] given X.

## Design vs. estimation

> [!tip] Prioritize design
> - Diagnose threats with design-specific checks before choosing estimators.
> - Estimators improve precision; they don’t fix identification failures.

- Estimation choices: parametric vs. nonparametric, fixed effects, machine learning for nuisance components (e.g., [[double machine learning]]).
- Always align standard errors with the assignment mechanism (e.g., cluster at the treatment or assignment level).

## Common threats to validity

- [[selection bias|Selection bias]] and omitted variables
- Differential [[pre-trends]] (DiD/ITS)
- Precise manipulation of the [[running variable]] (RDD)
- Violations of [[exclusion restriction]] (IV)
- [[spillovers|Spillovers]] / [[interference]] between units
- [[Anticipatory effects]] and policy endogeneity
- [[Attrition]] or changing [[composition]]
- [[Measurement error]] in treatment or outcome
- [[seasonality|Seasonality]] and time-varying confounders

## Diagnostics and falsification

- DiD/ITS: pre-trend plots, leads in [[event study]], placebo intervention dates.
- RDD: density test at cutoff (e.g., McCrary), balance tests, bandwidth robustness, local polynomial order checks.
- IV: first-stage strength (F-stat), overidentification tests (with caution), alternative instruments.
- Selection on observables: covariate balance before/after weighting/matching, sensitivity analyses (e.g., Rosenbaum bounds).

> [!check] Minimal design checklist
> - [ ] State estimand (ATE/ATT/LATE) and causal DAG.
> - [ ] Justify identification assumption(s).
> - [ ] Describe assignment/selection mechanism.
> - [ ] Pre-register outcome(s), model(s), bandwidths/windows.
> - [ ] Plan robustness, placebos, and diagnostics.
> - [ ] Specify clustering and small-sample corrections.

## Reporting essentials

- Clearly define treatment, timing, sample, unit of analysis.
- Show design diagrams (cutoff, timelines, DAGs).
- Present main effect with appropriate uncertainty: confidence intervals and clustered SEs.
- Include robustness table: alternative windows/bandwidths/specifications, different control groups, and placebos.
- Discuss external validity and limitations.

## When to use which design? (very short guide)

- Policy starts at a known time for a subset of units: [[Difference-in-Differences (DiD)]], [[Synthetic Control]], [[Interrupted Time Series (ITS)|ITS]].
- Treatment by cutoff or score: [[Regression Discontinuity Design (RDD)]].
- Policy-induced or natural instrument: [[Instrumental Variables (IV)]].
- Rich covariates, no obvious design shock: [[Propensity Score Matching (PSM)]] / [[Inverse Probability Weighting (IPW)|IPW]] / [[Doubly Robust estimators]].

## Minimal math snippets (copy-ready)

Inline examples:
- $ATE = \mathbb{E}[Y(1) - Y(0)]$
- Ignorability: $\{Y(1), Y(0)\} \perp T \mid X$
- Overlap: $0 < P(T=1 \mid X) < 1$

Block examples:
$$
ATE = \int \Big(\mathbb{E}[Y \mid T=1, X=x] - \mathbb{E}[Y \mid T=0, X=x]\Big)\, dF_X(x)
$$

## Example code snippets (optional)

```r
# R: packages you’ll commonly use
# DiD / TWFE
library(fixest); feols(Y ~ i(Post, D, ref = 0) | id + time, cluster = ~id, data = df)

# Staggered DiD
library(did); att_gt(yname = "Y", gname = "G", idname = "id", tname = "time", data = df)

# RDD
library(rdrobust); rdrobust(y = Y, x = score, c = cutoff)

# IV
library(AER); ivreg(Y ~ T + X1 + X2 | Z + X1 + X2, data = df)

# Synthetic Control
library(Synth); # dataprep() then synth()
```

```stata
* Stata: common commands
* DiD / TWFE
reghdfe Y c.Post##i.D, absorb(id time) vce(cluster id)

* Staggered DiD
csdid Y, ivar(id) time(time) gvar(G) method(dripw) vce(cluster id)

* RDD
rdrobust Y score, c(cutoff)

* IV
ivregress 2sls Y (T = Z) X1 X2, vce(cluster id)

* Synthetic Control
synth Y X1 X2, trunit(1) trperiod(2010)
```

```python
# Python: sketch only
# IV
from linearmodels.iv import IV2SLS
res = IV2SLS.from_formula('Y ~ 1 + X1 + X2 + [T ~ Z]', data=df).fit(cov_type='robust')

# TWFE
from linearmodels.panel import PanelOLS
df = df.set_index(['id','time'])
mod = PanelOLS.from_formula('Y ~ 1 + D + Post + D:Post + EntityEffects + TimeEffects', data=df)
mod.fit(cov_type='clustered', cluster_entity=True)
```

## References and further reading

- [[Angrist and Pischke]] (Mostly Harmless Econometrics; Mastering ‘Metrics)
- [[Imbens and Rubin]] (Causal Inference)
- [[Hernán and Robins]] (Causal Inference: What If)
- [[Cunningham (Mixtape)]]

> [!note] Triangulation
> When feasible, apply multiple designs (e.g., DiD + IV + RDD) and check whether conclusions align.

---

Related notes to create:
- [[Difference-in-Differences (DiD)]]
- [[Interrupted Time Series (ITS)]]
- [[Synthetic Control]]
- [[Regression Discontinuity Design (RDD)]]
- [[Instrumental Variables (IV)]]
- [[propensity score]]
- [[Propensity Score Matching (PSM)]]
- [[Inverse Probability Weighting (IPW)|Inverse Probability Weighting (IPW)]]
- [[Doubly Robust estimators]]
- [[Augmented Inverse Probability Weighting (AIPW)|AIPW]]
- [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]]
- [[potential outcomes]]
- [[causal DAGs]]
- [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]]
- [[Unconfoundedness]]
- [[Overlap]]
- [[parallel trends assumption]]
- [[event study]]
- [[relevance]]
- [[exclusion restriction]]
- [[monotonicity]]
- [[running variable]]
- [[pre-trends]]
- [[spillovers|Spillovers]]
- [[Anticipatory effects]]
- [[selection bias|Selection bias]]
- [[Attrition]]
- [[Measurement error]]
- [[seasonality|Seasonality]]
- [[double machine learning]]
- [[Average Treatment Effect (ATE)]]
- [[Average Treatment Effect on the Treated (ATT)]]