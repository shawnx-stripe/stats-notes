---
title: Treated Group
aliases: [treatment group, exposed group, intervention group]
tags: [causal-inference, design, sampling, did, rct]
updated: 2025-09-17
---

# Treated Group

> [!summary] Quick definition
> The set of units that receive the intervention/exposure under study. Denote treatment status by $D_i=1$ for treated units (vs. $D_i=0$ for controls).

- Context: part of a [[quasi-experimental design]] or [[randomized controlled trial (RCT)]].
- Purpose: provides observed outcomes under treatment; needs a comparable [[control group]] to approximate the counterfactual.

## Defining the treated group

- Binary treatment: $D_i = 1$ if unit received the policy/program; otherwise 0.
- Timing:
  - Ever-treated (common in [[Difference-in-Differences (DiD)]]): $D_i=1$ if treated at or after adoption; define adoption cohort $G_i$ (first treatment time).
  - Staggered adoption: separate groups by cohort $G_i$; use event time $t-G_i$.
- Intensity/dose:
  - If treatment varies in intensity, consider a continuous exposure $D_i \in \mathbb{R}_+$ and model dose–response, or bin into categories.
- Compliance:
  - [[Intent-to-Treat (ITT)]]: assign treated by offer/eligibility.
  - As-treated or Treatment-on-the-Treated requires addressing [[noncompliance]] (e.g., with [[Instrumental Variables (IV)]] for [[Local Average Treatment Effect (LATE)|LATE]]).

## Selection and comparability

- RCTs: randomization balances observed and unobserved factors in expectation.
- Quasi-experiments: justify why treated units are comparable to controls under the design’s assumptions (e.g., [[parallel trends assumption]] in DiD, local randomization in [[Regression Discontinuity Design (RDD)]]).
- Use design or statistical adjustment:
  - [[matching]] / [[propensity score]] weighting
  - [[stratification]] / blocking
  - [[Synthetic Control]] for a treated aggregate unit

## Diagnostics for the treated group

> [!check] Pre-analysis checklist
> - [ ] Precise, reproducible treatment definition (timing, intensity, eligibility)
> - [ ] No contamination: avoid units partially treated unless explicitly modeled
> - [ ] Balance checks vs. control on pre-treatment covariates
> - [ ] Stable composition: guard against selective entry/exit after assignment
> - [ ] For DiD: assess treated vs. control [[pre-trends]] with an [[event study]]
> - [ ] Document handling of [[spillovers]] / [[interference]] and [[Anticipatory effects]]

## Common pitfalls

> [!warning] Threats to validity
> - Spillovers to controls (violates [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]]): consider spatial buffers or exposure mappings.
> - Anticipation/behavioral responses pre-treatment: include leads or redefine treatment start.
> - Misclassification of treatment status or date.
> - Differential attrition or measurement post-treatment.
> - “Always-treated” or “never-observed pre” units limit identification in DiD.

## Reporting essentials

- Explicit treatment rule and timing window (e.g., “treated if policy effective in county by 2018-01-01”).
- Unit of treatment assignment (individual, school, county, firm).
- Share of treated units, clusters affected, and treatment intensity (if any).
- For staggered timing: distribution of adoption cohorts $G$.

## Minimal examples

> [!example] DiD flags (pseudo-code)
```r
# R
df$Post   <- as.integer(df$time >= policy_date[df$unit])
df$TreatedEver <- as.integer(!is.na(policy_date[df$unit]))
df$DPost <- df$TreatedEver * df$Post
```

```python
# Python
df["Post"] = (df["time"] >= df["policy_date"]).astype(int)
df["TreatedEver"] = df["policy_date"].notna().astype(int)
df["DPost"] = df["Post"] * df["TreatedEver"]
```

---

Related notes to create:
- [[control group]]
- [[quasi-experimental design]]
- [[Difference-in-Differences (DiD)]]
- [[Regression Discontinuity Design (RDD)]]
- [[Instrumental Variables (IV)]]
- [[parallel trends assumption]]
- [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]]
- [[spillovers]]
- [[interference]]
- [[Anticipatory effects]]
- [[matching]]
- [[propensity score]]
- [[stratification]]
- [[Synthetic Control]]
- [[Intent-to-Treat (ITT)]]
- [[noncompliance]]
- [[Local Average Treatment Effect (LATE)|LATE]]
- [[pre-trends]]


---
