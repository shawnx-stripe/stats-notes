---
title: Intent-to-Treat (ITT)
aliases: [ITT, intention-to-treat, ITT effect, offer effect, assignment effect]
tags: [causal-inference, rct, iv, noncompliance, policy-evaluation, did]
updated: 2025-09-17
---

# Intent-to-Treat (ITT)

> [!summary] Quick definition
> The Intent-to-Treat (ITT) effect is the causal effect of being assigned or offered treatment (policy intent), regardless of whether units comply. With randomized assignment $Z$, the ITT is the difference in average outcomes between $Z=1$ and $Z=0$ groups. It is policy-relevant and unbiased under random assignment even with [[noncompliance]].

- Typical use: RCTs with imperfect take-up, encouragement designs, or policies where assignment/eligibility differs from actual receipt.
- Contrast with: [[Treatment-on-the-Treated (TOT)]] and [[Local Average Treatment Effect (LATE)|LATE]] which target effects of receiving treatment among compliers.

## Setup and notation

- $Z_i \in \{0,1\}$: assignment/offer/eligibility (instrument).
- $D_i \in \{0,1\}$ or continuous: actual treatment received (take-up).
- $Y_i$: outcome; potential outcomes $Y_i(z)$ for assignment, and $Y_i(d)$ for treatment receipt.
- [[treated group]] and [[control group]] refer to receipt ($D$) unless stated; ITT focuses on $Z$.

## ITT estimand (difference in means)

- Copy-ready:
$$
ITT = \mathbb{E}[Y \mid Z=1] - \mathbb{E}[Y \mid Z=0]
$$

- With random assignment, SUTVA, and no differential attrition, the difference-in-means is an unbiased estimate of ITT.

> [!tip] Policy interpretation
> ITT answers: “What is the average effect of offering/assigning the program?” This is often the relevant object for policy makers.

## Relationship to TOT and LATE

- First stage (effect of assignment on receipt):
$$
\Delta_D = \mathbb{E}[D \mid Z=1] - \mathbb{E}[D \mid Z=0]
$$

- Under standard IV assumptions — [[exclusion restriction]] (assignment affects $Y$ only via $D$), [[monotonicity]] (no defiers), and independence of $Z$ — the Wald ratio identifies the [[Local Average Treatment Effect (LATE)|LATE]]:
$$
LATE = \frac{ITT}{\Delta_D}
$$

- If treatment is binary and these assumptions hold, LATE equals the [[Treatment-on-the-Treated (TOT)]] for compliers. ITT is typically an attenuated (diluted) effect relative to TOT when take-up is below 100%.

> [!warning] Caution
> Without exclusion or with interference, $ITT/\Delta_D$ need not equal a causal effect. Report ITT regardless; compute LATE only if assumptions are plausible.

## ITT in panels and DiD

- When assignment varies over time or by unit (e.g., eligibility rolled out), estimate an ITT via [[Difference-in-Differences (DiD)]] using assignment $Z$ in place of receipt $D$:
$$
Y_{it} = \alpha_i + \gamma_t + \tau \,(Z_{it} \cdot Post_t) + X_{it}'\theta + \varepsilon_{it}
$$
- Here, $\tau$ is an ITT-type DiD effect of assignment. With noncompliance, $\tau$ is diluted relative to the “effect of receipt.” To recover a LATE-style effect, divide by the DiD first stage for $D$.

## Assumptions for unbiased ITT

- Random or as-if random assignment $Z$ (or valid design justifying independence).
- [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]] and [[No spillovers]] (or model [[interference]]).
- No selective attrition by assignment status (or handle with weighting/bounds).
- For panel/DiD ITT: [[parallel trends assumption]] holds for untreated potential outcomes with respect to assignment groups.

## Diagnostics and reporting

> [!check] Good practice
> - [ ] Report compliance rates: $\mathbb{E}[D \mid Z=1]$, $\mathbb{E}[D \mid Z=0]$, and $\Delta_D$.
> - [ ] Present ITT with CIs; if computing LATE, report instrument strength (first-stage F-stat).
> - [ ] Discuss plausibility of exclusion and monotonicity if reporting LATE/TOT.
> - [ ] Address [[interference]]/spillovers and [[composition]]/attrition.
> - [ ] Cluster SEs at assignment level; use [[few-cluster corrections]] if clusters are few. See [[clustered standard errors]].

## Common pitfalls

> [!warning] Avoid these
> - Dropping noncompliers from the analysis (breaks randomization).
> - Calling a Wald ratio “TOT” without discussing IV assumptions.
> - Ignoring spillovers from the offer (e.g., control units benefit indirectly).
> - Conditioning on post-assignment variables (creates [[bad controls]]).

## Minimal code snippets

> [!example] ITT (difference in means)

```r
# R
with(df, mean(Y[Z==1]) - mean(Y[Z==0]))
t.test(Y ~ Z, data = df)  # CI for ITT
```

```stata
* Stata
ttest Y, by(Z)   // ITT and CI (randomized assignment)
```

```python
# Python
import numpy as np
itt = df.loc[df.Z==1, 'Y'].mean() - df.loc[df.Z==0, 'Y'].mean()
print(itt)
```

> [!example] LATE via Wald ratio (if IV assumptions hold)

```r
# R
itt_y <- with(df, mean(Y[Z==1]) - mean(Y[Z==0]))
itt_d <- with(df, mean(D[Z==1]) - mean(D[Z==0]))
late  <- itt_y / itt_d

# Or 2SLS (AER)
library(AER)
summary(ivreg(Y ~ D | Z, data = df))
```

```stata
* Stata
ivregress 2sls Y (D = Z)
```

```python
# Python (linearmodels)
from linearmodels.iv import IV2SLS
res = IV2SLS.from_formula('Y ~ 1 + [D ~ Z]', data=df).fit(cov_type='robust')
print(res.summary)
```

> [!example] ITT in DiD (assignment as treatment)

```r
# R (fixest)
library(fixest)
est <- feols(Y ~ Z:Post | id + time, cluster = ~id, data = df)
etable(est)  # tau is ITT-DiD
```

## Copy-ready formulas

- ITT:
$$
ITT = \mathbb{E}[Y \mid Z=1] - \mathbb{E}[Y \mid Z=0]
$$

- First stage:
$$
\Delta_D = \mathbb{E}[D \mid Z=1] - \mathbb{E}[D \mid Z=0]
$$

- LATE (Wald ratio, under IV assumptions):
$$
LATE = \frac{\mathbb{E}[Y \mid Z=1] - \mathbb{E}[Y \mid Z=0]}{\mathbb{E}[D \mid Z=1] - \mathbb{E}[D \mid Z=0]}
$$

## When to favor ITT

- Policy makers care about the impact of offering/assigning a program (not just on compliers).
- Noncompliance is substantial or mechanisms of take-up are complex.
- Exclusion or monotonicity are doubtful; report ITT regardless, and LATE as a secondary estimand if justified.

---

## Related notes
- [[treated group]]
- [[control group]]
- [[noncompliance]]
- [[Treatment-on-the-Treated (TOT)]]
- [[Instrumental Variables (IV)]]
- [[Local Average Treatment Effect (LATE)|LATE]]
- [[exclusion restriction]]
- [[monotonicity]]
- [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]]
- [[No spillovers]]
- [[interference]]
- [[Difference-in-Differences (DiD)]]
- [[parallel trends assumption]]
- [[composition]]
- [[bad controls]]
- [[clustered standard errors]]
- [[few-cluster corrections]]
- [[clustering]]