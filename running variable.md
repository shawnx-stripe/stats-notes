---
title: Running Variable
aliases: [running variable, assignment variable, forcing variable, score variable]
tags: [econometrics, rdd, identification]
updated: 2026-03-05
---

# Running Variable

> [!summary]
> The continuous variable that determines treatment assignment at a cutoff in a [[Regression Discontinuity Design (RDD)]]. Observations just above and below the cutoff are compared as a local experiment.

## Key requirements

- **Continuous**: No mass points near the cutoff (test with [[rddensity]])
- **Not manipulable**: Units cannot precisely control the value (test with [[McCrary test]])
- **Pre-determined**: Measured before treatment assignment
- **Relevant**: Substantively related to treatment but not a direct cause of the outcome (except through treatment)

## Common examples

| Context | Running variable | Cutoff | Treatment |
|---------|-----------------|--------|-----------|
| Education | Test score | Passing threshold | Scholarship |
| Elections | Vote share | 50% | Incumbent wins |
| Policy | Age | 65 | Medicare eligibility |
| Regulation | Firm size | 50 employees | Labor law applies |

> [!warning] Manipulation
> If units can precisely manipulate the running variable (e.g., self-reported income for subsidy eligibility), the local randomization assumption fails. Always test for discontinuities in the density.

## Related notes

- [[Regression Discontinuity Design (RDD)]]
- [[fuzzy RDD]]
- [[McCrary test]]
- [[density test]]
- [[bandwidth selection]]
