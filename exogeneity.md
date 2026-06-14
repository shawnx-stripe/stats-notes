---
title: Exogeneity
aliases: [exogeneity, Exogeneity, strict exogeneity, exogenous]
tags: [econometrics, identification, assumptions]
updated: 2026-03-05
---

# Exogeneity

> [!summary]
> Condition that regressors are uncorrelated with the error term: $\mathbb{E}[u_i \mid X_i]=0$. Strict exogeneity additionally conditions on all periods. Failure leads to endogeneity bias; remedies include [[Instrumental Variables (IV)]] and [[Difference-in-Differences (DiD)]].

## Definitions

**Contemporary exogeneity**: $\mathbb{E}[u_i \mid X_i] = 0$ for cross-sectional data.

**Strict exogeneity** (panel data): $\mathbb{E}[u_{it} \mid X_{i1}, \ldots, X_{iT}] = 0$ for all $t$. Rules out feedback from $u_{it}$ to future $X_{is}$.

**Predetermined regressors**: Weaker than strict exogeneity; $\mathbb{E}[u_{it} \mid X_{i1}, \ldots, X_{it}] = 0$ allows feedback after period $t$.

> [!warning]
> Exogeneity fails when:
> - Omitted variable bias: $X$ and $u$ share a common cause
> - Reverse causality: $Y$ affects $X$
> - Measurement error in $X$ (classical case)
> - Sample selection based on $u$

## When to use

Exogeneity is the core identifying assumption for [[Ordinary Least Squares (OLS)|OLS]]. When violated, OLS is biased. Remedies:
- **Omitted confounders**: Add controls, use fixed effects, or [[Difference-in-Differences (DiD)]]
- **Reverse causality**: [[Instrumental Variables (IV)]] or dynamic panel methods
- **Measurement error**: IV with a valid instrument for the mismeasured variable

## Related notes

- [[Instrumental Variables (IV)]]
- [[Ordinary Least Squares (OLS)|OLS]]
- [[Identification Strategies (MOC)]]
- [[selection bias]]
- [[Unconfoundedness]]
