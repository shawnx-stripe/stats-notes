---
title: Ignorability
aliases: [ignorability, strong ignorability, ignorable treatment assignment]
tags: [causal-inference, identification, assumptions]
updated: 2026-03-05
---

# Ignorability

> [!summary]
> Assumption that treatment assignment is independent of potential outcomes conditional on observed covariates: $(Y(0),Y(1)) \perp\!\!\perp D \mid X$. Equivalent to [[Unconfoundedness]] plus [[Overlap]]. Foundation for matching and weighting estimators.

## Formal definition

**Strong ignorability** (Rosenbaum & Rubin, 1983):
1. **Unconfoundedness**: $(Y(0), Y(1)) \perp\!\!\perp D \mid X$
2. **Overlap**: $0 < P(D=1 \mid X) < 1$ for all $x$ in the support of $X$

These jointly imply identification of the ATE:
$$
\tau = \mathbb{E}[Y(1) - Y(0)] = \mathbb{E}_X[\mathbb{E}[Y \mid D=1, X] - \mathbb{E}[Y \mid D=0, X]]
$$

> [!warning]
> Ignorability is untestable because it involves unobserved potential outcomes. Violation (unmeasured confounding) leads to bias. Use:
> - **Sensitivity analysis**: [[Rosenbaum sensitivity]], E-value
> - **Falsification tests**: [[placebo test]], [[balance check]] on pre-treatment outcomes
> - **Design-based approaches**: [[Instrumental Variables (IV)]], [[Difference-in-Differences (DiD)]] when ignorability is implausible

## When to use

Ignorability justifies [[propensity score]] methods, [[matching]], [[Inverse Probability Weighting (IPW)|IPW]], and [[Outcome regression (OR)|outcome regression]]. It is plausible in:
- High-quality observational studies with rich pre-treatment covariates
- Post-stratification in experiments with noncompliance
- Conditional randomization designs (e.g., stratified or blocked RCTs)

## Related notes

- [[Unconfoundedness]]
- [[Overlap]]
- [[propensity score]]
- [[Identification Strategies (MOC)]]
