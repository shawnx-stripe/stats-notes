---
title: Back-Door Criterion
aliases: [back-door criterion, back door criterion, backdoor adjustment]
tags: [causal-inference, identification, graphical-models]
updated: 2026-03-05
---

# Back-Door Criterion

> [!summary]
> Graphical criterion (Pearl) for identifying sufficient adjustment sets. A set $Z$ satisfies the back-door criterion relative to $(X,Y)$ if it blocks all back-door paths from $X$ to $Y$ and contains no descendants of $X$.

## Formal definition

A set $Z$ satisfies the back-door criterion relative to the ordered pair $(X, Y)$ if:
1. No node in $Z$ is a descendant of $X$
2. $Z$ blocks every path between $X$ and $Y$ that contains an arrow into $X$ (a "back-door path")

When the criterion holds, conditioning on $Z$ identifies the causal effect:

$$
P(Y \mid \operatorname{do}(X=x)) = \sum_z P(Y \mid X=x, Z=z) P(Z=z)
$$

## When to use

- You have a causal DAG representing the data-generating process
- You want to identify a minimal sufficient adjustment set
- You want to verify that a proposed adjustment set is sufficient

> [!tip]
> Multiple adjustment sets may satisfy the back-door criterion. Use tools like `dagitty` (R) or `DoWhy` (Python) to enumerate all minimal sufficient sets.

## Python snippet

```python
import dowhy
from dowhy import CausalModel

model = CausalModel(
    data=df,
    treatment='X',
    outcome='Y',
    graph="digraph {X -> Y; Z -> X; Z -> Y; U -> X; U -> Y;}"
)
# Identify backdoor adjustment sets
identified_estimand = model.identify_effect()
print(identified_estimand.backdoor_variables)
```

## Related notes

- [[causal DAGs]]
- [[front-door criterion]]
- [[Unconfoundedness]]
- [[Identification Strategies (MOC)]]
