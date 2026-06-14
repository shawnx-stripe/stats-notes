---
title: Causal DAGs
aliases: [causal DAGs, causal directed acyclic graphs, DAG, directed acyclic graph, DAGs]
tags: [causal-inference, identification, graphical-models]
updated: 2026-03-05
---

# Causal DAGs

> [!summary]
> Graphical framework (Pearl) where nodes represent variables and directed edges represent direct causal effects. Provides rules (d-separation, [[back-door criterion]], [[front-door criterion]]) for identifying causal effects from observational data.

## Structure and Notation

A causal DAG $G = (V, E)$ consists of:
- **Nodes** $V$: Random variables (treatment $D$, outcome $Y$, covariates $X$, unobserved $U$)
- **Directed edges** $E$: Direct causal relationships (no cycles allowed)
- **Paths**: Sequences of edges connecting nodes (can be directed or undirected)
- **Parents** $\text{pa}(X)$: Direct causes of $X$
- **Descendants** $\text{de}(X)$: Variables caused (directly or indirectly) by $X$

> [!note]
> The acyclicity assumption rules out feedback loops and ensures a causal ordering of variables.

## d-separation

Two sets of variables $X$ and $Y$ are **d-separated** by $Z$ (written $X \perp_d Y \mid Z$) if every path between $X$ and $Y$ is blocked by $Z$.

A path is **blocked** by $Z$ if:
1. The path contains a chain $A \to B \to C$ or fork $A \leftarrow B \to C$ where $B \in Z$
2. The path contains a collider $A \to B \leftarrow C$ where $B \notin Z$ and no descendant of $B$ is in $Z$

**Implication**: If $X \perp_d Y \mid Z$, then $X \perp Y \mid Z$ (conditional independence in the data).

> [!check] Testable implication
> d-separation implies conditional independence. You can test whether observed independencies match the DAG structure using tools like `dagitty` or `causaleffect`.

## Back-Door Criterion

A set of variables $Z$ satisfies the **back-door criterion** relative to $(D, Y)$ if:
1. No node in $Z$ is a descendant of $D$
2. $Z$ blocks all back-door paths from $D$ to $Y$ (paths with an arrow into $D$)

**Result**: If $Z$ satisfies the back-door criterion, the causal effect is identified:

$$
P(Y \mid \text{do}(D=d)) = \sum_z P(Y \mid D=d, Z=z) P(Z=z)
$$

This is the adjustment formula. Conditioning on $Z$ removes confounding.

> [!warning]
> Do NOT condition on descendants of $D$ (post-treatment variables) or colliders—these can induce bias.

## Front-Door Criterion

When there is unmeasured confounding ($U \to D$ and $U \to Y$) but a mediator $M$ satisfies:
1. $M$ intercepts all directed paths from $D$ to $Y$ (i.e., $D \to M \to Y$)
2. No unblocked back-door paths from $D$ to $M$
3. $D$ blocks all back-door paths from $M$ to $Y$

Then the causal effect is identified via:

$$
P(Y \mid \text{do}(D=d)) = \sum_m P(M=m \mid D=d) \sum_{d'} P(Y \mid M=m, D=d') P(D=d')
$$

**Intuition**: Use $M$ as a proxy instrument—first estimate $D \to M$, then estimate $M \to Y$ controlling for $D$.

## Instrumental Variable Graphs

An IV $Z$ in a DAG must satisfy:
1. **Relevance**: $Z \to D$ (or path from $Z$ to $D$)
2. **Exclusion restriction**: No direct path $Z \to Y$ except through $D$
3. **No confounding**: No unblocked back-door paths from $Z$ to $Y$

Typical IV DAG:
```
U → D → Y
↑       ↑
└───────┘

Z → D
```

Here $U$ confounds $D \to Y$, but $Z$ satisfies the IV conditions.

> [!tip]
> Use DAGs to visually verify [[exclusion restriction]]—if you can draw a path from $Z$ to $Y$ not through $D$, the exclusion restriction fails.

## Collider Bias

A **collider** is a variable $C$ where two paths meet: $A \to C \leftarrow B$.

Conditioning on $C$ (or its descendants) **opens** the path between $A$ and $B$, inducing spurious correlation.

**Example**: If $D \to C \leftarrow Y$, conditioning on $C$ creates selection bias in the $D \to Y$ effect.

> [!warning]
> [[bad controls]] are often colliders. Adjusting for them can worsen bias instead of removing it.

## Minimal Code Snippets

### R: dagitty and ggdag

```r
library(dagitty)
library(ggdag)

# Define a DAG
dag <- dagitty('dag {
  Z -> D
  D -> Y
  U -> D
  U -> Y
}')

# Check conditional independencies
impliedConditionalIndependencies(dag)

# Find adjustment sets (back-door criterion)
adjustmentSets(dag, exposure = "D", outcome = "Y")

# Visualize
ggdag(dag) + theme_dag()

# Check if Z is a valid IV
paths(dag, from = "Z", to = "Y")  # should only go through D
```

### Python: dowhy

```python
import dowhy
from dowhy import CausalModel
import pandas as pd

# Define DAG using GML string
causal_graph = """
digraph {
  Z -> D;
  D -> Y;
  U -> D;
  U -> Y;
}
"""

# Create causal model
model = CausalModel(
    data=df,
    treatment='D',
    outcome='Y',
    graph=causal_graph
)

# Identify causal effect
identified_estimand = model.identify_effect(proceed_when_unidentifiable=True)
print(identified_estimand)

# Check if adjustment set is valid
print(model.view_model())
```

### Python: networkx for custom DAG operations

```python
import networkx as nx
import matplotlib.pyplot as plt

# Create DAG
G = nx.DiGraph()
G.add_edges_from([('Z', 'D'), ('D', 'Y'), ('U', 'D'), ('U', 'Y')])

# Check for cycles (should be empty for DAG)
cycles = list(nx.simple_cycles(G))

# Find all paths from Z to Y
paths = list(nx.all_simple_paths(G, 'Z', 'Y'))

# Visualize
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_color='lightblue',
        node_size=1500, arrowsize=20)
plt.show()
```

### Stata: No native DAG package

Stata lacks built-in DAG tools. Use R or Python for DAG analysis, then implement the identified adjustment strategy in Stata:

```stata
* After identifying adjustment set Z = {X1, X2} from dagitty
reg Y D X1 X2, robust
```

## Testable Implications

DAGs make predictions about conditional independencies in the data. You can test:

1. **Implied independencies**: Use `dagitty::impliedConditionalIndependencies()`
2. **Overidentification tests**: If multiple adjustment sets exist, estimates should agree
3. **Placebo tests**: Variables that should be independent given controls can serve as [[placebo test]]s

> [!example]
> If your DAG implies $Z \perp Y \mid X$, test this with `cor.test(Z, Y)` after residualizing on $X$. Rejection suggests misspecification.

## Common Pitfalls

1. **Conditioning on colliders**: Opens spurious paths (see [[collider bias]])
2. **Omitting confounders**: Fails back-door criterion, biased estimates
3. **Conditioning on mediators**: Blocks part of the causal effect (see [[bad controls]])
4. **Unmeasured confounding**: DAG may suggest no valid adjustment set—consider [[Instrumental Variables (IV)]] or [[front-door criterion]]

## Extensions

- **Marginal Structural Models (MSMs)**: Time-varying DAGs for longitudinal treatments
- **Selection Diagrams**: Extend DAGs to handle [[selection bias]] via square nodes
- **Single World Intervention Graphs (SWIGs)**: Directly represent [[potential outcomes]] in graph form

## Related notes

- [[Identification Strategies (MOC)]]
- [[Unconfoundedness]]
- [[bad controls]]
- [[collider bias]]
- [[front-door criterion]]
- [[back-door criterion]]
- [[Instrumental Variables (IV)]]
- [[exclusion restriction]]
- [[selection bias]]
- [[placebo test]]
