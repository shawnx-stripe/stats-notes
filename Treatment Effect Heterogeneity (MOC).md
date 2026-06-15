---
title: Treatment Effect Heterogeneity (MOC)
aliases:
  - Conditional treatment effects
  - Effect modification
tags:
  - MOC
  - causal-inference
  - heterogeneity
  - treatment-effects
  - machine-learning
updated: 2025-09-26
---

# Treatment Effect Heterogeneity (MOC)

> [!summary] Overview
> Methods for understanding how treatment effects vary across individuals, groups, or contexts. Covers defining heterogeneous effects, the marginal treatment effect framework, and modern ML approaches for discovering and estimating conditional average treatment effects (CATE).

## Core Concept

Treatment effects often vary systematically:
- **By observable characteristics** (X): Age, income, baseline health
- **By unobservable characteristics** (U): Motivation, ability, preferences
- **By selection into treatment**: Those who select in may benefit more/less
- **By context**: Time, place, implementation

The ATE can hide important variation that matters for policy targeting, mechanisms, external validity, and welfare analysis.

## Hierarchy of Effects

```mermaid
graph TD
    A[Individual Effect: τᵢ] --> B[CATE: τ(x) = E[τᵢ|Xᵢ=x]]
    B --> C[Group Effects]
    C --> D[ATE: E[τᵢ]]
    C --> E[ATT: E[τᵢ|Dᵢ=1]]
    C --> F[ATU: E[τᵢ|Dᵢ=0]]
    B --> G[MTE: E[τᵢ|Xᵢ=x, Uᵢ=u]]
    G --> H[LATE: Marginal compliers]
    H --> I[PRTE: Policy-relevant]
```

## Key Parameters

### Population-Level
- [[Average Treatment Effect (ATE)]]: $\text{ATE} = \mathbb{E}[Y_1 - Y_0]$
- [[Average Treatment Effect on the Treated (ATT)]]: $\text{ATT} = \mathbb{E}[Y_1 - Y_0 | D = 1]$
- ATU: $\text{ATU} = \mathbb{E}[Y_1 - Y_0 | D = 0]$ — relevant for program expansion

### Selection-Based
- [[Local Average Treatment Effect (LATE)|LATE]]: $\mathbb{E}[Y_1 - Y_0 | \text{Complier}]$ — identified by [[Instrumental Variables (IV)]]
- [[marginal treatment effect (MTE)]]: $\text{MTE}(x,u) = \mathbb{E}[Y_1 - Y_0 | X=x, U=u]$ — building block for all other effects; identified via [[Local IV]]
- [[Treatment-on-the-Treated (TOT)]]: adjusts [[Intent-to-Treat (ITT)]] for [[noncompliance]]

### Conditional
- **CATE**: $\tau(x) = \mathbb{E}[Y_1 - Y_0 | X = x]$ — target of most HTE methods
- **QTE**: $\text{QTE}_q = Q_{Y_1}(q) - Q_{Y_0}(q)$ — effects on different parts of outcome distribution

## Identification

| Method | Key Assumption | Identifies |
|--------|---------------|------------|
| RCT with interactions | Random assignment | CATE |
| Observational with [[Unconfoundedness]] | Selection on observables | CATE |
| [[Instrumental Variables (IV)]] | Exclusion, monotonicity | LATE, MTE |
| [[Regression Discontinuity Design (RDD)]] | Continuity | Effect at cutoff |
| [[Difference-in-Differences (DiD)]] | Parallel trends | ATT variations |

## Estimation Methods

### Traditional
- **Subgroup analysis**: Simple but suffers from multiple testing, arbitrary groups, low power
- **Regression with interactions**: $Y_i = \alpha + \beta D_i + \gamma X_i + \delta (D_i \times X_i) + \varepsilon_i$; δ captures heterogeneity but assumes linearity

### Machine Learning

- **[[causal forests]] / [[Generalized Random Forests (GRF)|GRF]]**: Adaptive heterogeneity discovery, honest splitting for valid inference, provides τ̂(x) and CIs
- **[[double machine learning]]**: Residualize nuisances with ML, estimate τ(X) on residuals with [[cross-fitting]]

### Meta-Learners

- **S-Learner**: Single model μ̂(X,D); τ̂(x) = μ̂(x,1) - μ̂(x,0)
- **T-Learner**: Separate models μ̂₁(X), μ̂₀(X); τ̂(x) = μ̂₁(x) - μ̂₀(x)
- **X-Learner**: Cross-impute individual effects, combine with propensity weighting; works well with imbalanced treatment
- **R-Learner**: Minimize $\sum_i [(Y_i - m(X_i)) - \tau(X_i)(D_i - e(X_i))]^2$; efficient under correct specification

### [[policy learning]] and [[policy tree]]
- Learn optimal treatment rules: d*(x) = 𝟙{τ̂(x) > 0}
- Maximize value: V(d) = 𝔼[Y(d(X))]
- Interpretable rules via trees

## Testing for Heterogeneity

### Best Linear Predictor (BLP)
For causal forest estimates τ̂(Xᵢ):
$$
\tau_i = \alpha + \beta \cdot \hat\tau(X_i) + \epsilon_i
$$
- β = 1: Well-calibrated; β = 0: No detectable heterogeneity

### Sorted Group Average Treatment Effects (GATES)
Sort by τ̂(Xᵢ) into quantiles, estimate ATE within each, test for differences across groups.

## Practical Workflow

1. **Define question**: exploratory (what drives HTE?), confirmatory (test pre-specified HTE), or policy (who to treat?)
2. **Choose estimand**: ATE vs ATT vs LATE; observable vs unobservable heterogeneity
3. **Select method**: causal forest/DML for large samples and high-dimensional X; regression interactions for small/pre-specified
4. **Estimate with honest inference**: sample splitting, cross-fitting, multiple testing correction
5. **Validate**: BLP calibration, GATES, held-out data, placebo tests

## Key Packages

- **R**: `grf` (causal forests), `policytree`, `DoubleML`
- **Python**: `econml` (CausalForestDML, meta-learners), `causalml` (uplift trees)
- **Stata**: `teffects`, `rcall` to R's `grf`

## Common Pitfalls

> [!warning] Avoid These
> 1. **Fishing for heterogeneity** — multiple testing without correction
> 2. **Overfitting** — not using honest/split-sample methods
> 3. **Extrapolation** — effects outside common support
> 4. **Ignoring uncertainty** — point estimates without CIs
> 5. **Misinterpreting LATE as ATE** — different populations
> 6. **Power issues** — underpowered for subgroup detection

## Interpretation and Policy

### Welfare
$$
W(G) = \int_{x \in G} \tau(x) f(x) dx - C(G)
$$
Optimal targeting: treat those with τ(x) > marginal cost.

### External Validity (transport)
$$
\text{ATE}_{\text{target}} = \int \tau(x) f_{\text{target}}(x) dx
$$

## Checklist

> [!check] HTE Analysis
> - [ ] Pre-specify hypotheses about heterogeneity
> - [ ] Use sample splitting / [[cross-fitting]] for honest inference
> - [ ] Test global null of no heterogeneity
> - [ ] Report BLP calibration and GATES
> - [ ] Validate on held-out data (internal) or different context (external)
> - [ ] Check overlap by subgroup; assess common support
> - [ ] Multiple testing corrections if exploring
> - [ ] Translate to policy recommendations with uncertainty

## Key Papers

- Heckman & Vytlacil (2005) — MTE framework
- Imbens & Angrist (1994) — LATE
- Athey & Imbens (2016) — Recursive partitioning
- Wager & Athey (2018) — Causal forests
- Chernozhukov et al. (2018) — Double/debiased ML
- Künzel et al. (2019) — Metalearners
- Athey & Wager (2021) — Policy learning

---

## Related notes
- [[treatment effect heterogeneity|CATE]]
- [[quantile treatment effects]]
- [[best linear predictor]]
- [[GATES]]
- [[meta-learners]]
- [[honest inference]]
- [[policy value]]
- [[fairness in treatment assignment]]
- [[selection on gains]]
- [[essential heterogeneity]]
