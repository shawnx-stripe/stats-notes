---
title: Policy-Relevant Treatment Effect (PRTE)
aliases:
  - Policy-Relevant Treatment Effect
  - policy-relevant treatment effect
  - PRTE
tags:
  - causal-inference
  - iv
  - policy
  - treatment-effects
updated: 2026-03-04
---

# Policy-Relevant Treatment Effect (PRTE)

> [!summary] Quick definition
> The Policy-Relevant Treatment Effect (PRTE) is the average causal effect of switching from a status-quo policy to a counterfactual policy that changes the distribution of treatment take-up. Unlike [[Local Average Treatment Effect (LATE)|LATE]], which focuses on compliers with a specific instrument, PRTE weights marginal treatment effects ([[marginal treatment effect (MTE)|MTE]]) by the density of individuals induced into (or out of) treatment by the policy change.

## Key formula

$$
\text{PRTE} = \int_0^1 \operatorname{MTE}(u) \, \omega(u) \, du
$$

where $\omega(u)$ reflects the share of individuals at unobserved resistance margin $u$ whose treatment status changes under the new policy.

## Related notes

- [[marginal treatment effect (MTE)|MTE]]
- [[Local Average Treatment Effect (LATE)|LATE]]
- [[Instrumental Variables (IV)]]
- [[always-takers]]
