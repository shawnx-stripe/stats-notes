---
title: Collider Bias
aliases: [collider bias, Berkson's bias, selection on collider, endogenous selection bias]
tags: [causal-inference, identification, bias, graphical-models]
updated: 2026-03-05
---

# Collider Bias

> [!summary]
> Bias introduced by conditioning on a common effect (collider) of treatment and outcome (or their ancestors). Opens a spurious association path even in the absence of confounding. Classic example: conditioning on post-treatment variable.

## Causal structure

In a DAG where $X \to C \leftarrow Y$ (C is a collider):
- $X$ and $Y$ are marginally independent
- Conditioning on $C$ induces a spurious correlation between $X$ and $Y$

This is called "explaining away" or "Berkson's paradox."

## Classic example

**Hospital admissions**: Suppose disease A and disease B both cause hospitalization. Among hospitalized patients, having disease A makes disease B *less likely* (conditioning on hospitalization opens a spurious negative association). This does not imply A prevents B in the general population.

## How to avoid

- Do not condition on post-treatment variables
- Do not condition on intermediate outcomes or mediators unless performing mediation analysis
- Use [[causal DAGs]] to identify which variables are colliders

> [!warning]
> Adjusting for a collider can introduce bias even when the treatment is randomized. Always check the DAG before adding control variables.

## Python simulation

```python
import numpy as np
np.random.seed(42)
X = np.random.normal(0, 1, 1000)
Y = np.random.normal(0, 1, 1000)
C = X + Y + np.random.normal(0, 0.5, 1000)  # C is a collider

# Marginal correlation: X and Y independent
np.corrcoef(X, Y)[0, 1]  # ≈ 0

# Conditional on C: X and Y become correlated
from scipy.stats import linregress
C_resid_X = linregress(C, X).slope
C_resid_Y = linregress(C, Y).slope
# Now X and Y are negatively correlated after partialling out C
```

## Related notes

- [[causal DAGs]]
- [[bad controls]]
- [[selection bias]]
- [[post-treatment conditioning]]
- [[Identification Strategies (MOC)]]
