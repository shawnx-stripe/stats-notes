---
title: Post-Treatment Conditioning
aliases: [post-treatment conditioning, conditioning on post-treatment variables]
tags: [causal-inference, identification, bias]
updated: 2026-03-05
---

# Post-Treatment Conditioning

> [!summary]
> Controlling for variables affected by treatment introduces selection bias even in randomized experiments. A form of [[collider bias]] that can open backdoor paths. See [[bad controls]].

## Why it introduces bias

Post-treatment variables $M$ are mediators or outcomes. Conditioning on $M$ creates spurious associations between treatment $D$ and outcome $Y$ through shared causes of $M$ and $Y$. Even under random assignment:

$$
\mathbb{E}[Y(d) \mid M = m] \neq \mathbb{E}[Y(d)]
$$

because the conditioning set is itself affected by treatment.

> [!warning] Common mistakes
> - Controlling for intermediate outcomes (e.g., compliance, intermediate health measures)
> - Adjusting for variables measured post-randomization
> - Including "bad controls" that are descendants of treatment in a DAG
>
> **Rule of thumb**: Only adjust for pre-treatment covariates unless doing formal mediation analysis with sequential ignorability assumptions.

## Example

In an RCT of a job training program, controlling for "applied for jobs" (post-treatment) biases the effect estimate because application is affected by both training and unobserved motivation, which also affects employment outcomes.

## Related notes

- [[bad controls]]
- [[collider bias]]
- [[covariates]]
- [[selection bias]]
- [[causal DAGs]]
