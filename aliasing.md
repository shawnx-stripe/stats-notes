---
title: Aliasing
aliases: [aliasing, effect aliasing, confounding in factorial designs]
tags: [experimental-design, design-of-experiments, identification]
updated: 2026-04-02
---

# Aliasing

> [!summary] Quick definition
> In factorial and fractional-factorial designs, aliasing means two or more effects are mathematically confounded, so the data cannot separately identify them.

## Where it appears

- Fractional factorial designs that trade runs for information.
- Screening experiments where higher-order interactions are assumed negligible.
- Designs with generators that intentionally confound some effects.

## Why it matters

- An estimated main effect may partly reflect an interaction.
- Design resolution summarizes how severe the confounding is.
- Interpretation depends on which higher-order effects are assumed to be small.

## Simple example

In a $2^{3-1}$ design with generator $I = ABC$, the alias structure implies:

$$
A = BC, \quad B = AC, \quad C = AB.
$$

You cannot separately identify $A$ from $BC$ in that design.

## Related notes

- [[factorial design]]
- [[Experimental Design (MOC)]]
- [[response surface methodology]]

