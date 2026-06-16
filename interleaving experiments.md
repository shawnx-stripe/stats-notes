---
title: interleaving experiments
aliases: [interleaving, interleaved experiments, team draft interleaving, balanced interleaving]
tags: [experimentation, ab-testing, ranking, search, variance-reduction, sensitivity]
updated: 2026-06-17
---

# interleaving experiments

> [!summary] Quick definition
> Interleaving experiments merge ranked results from two competing algorithms into a single list shown to the same user, enabling within-user comparison rather than between-user comparison. This dramatically increases sensitivity (up to 50–100× faster than standard A/B tests) for ranking and recommendation evaluation. Used as a screening mechanism before full A/B tests.

- Use in: search ranking, recommendations, ads ranking, content feeds — any system producing ranked lists.
- Core idea: measure which ranker's items a user prefers by observing clicks/engagement on a blended list.
- Not a replacement for A/B tests: validates direction quickly, but A/B confirms causal impact on business metrics.

---

## When to use

- Comparing two ranking models (control vs. candidate) on the same traffic.
- Needing faster signal than standard A/B (which may require weeks for booking/conversion metrics).
- Screening many candidates before committing A/B traffic to the most promising ones.

> [!warning] Limitations
> - Only measures relative preference between two rankers, not absolute metric impact.
> - Rankers that optimize set-level composition (diversity, pacing) may be invalidated when their outputs are interleaved.
> - Downstream business metrics (revenue, retention) still require A/B confirmation.

---

## Team draft algorithm

The standard approach for blending two ranked lists:

1. Flip a fair coin to decide which team picks first.
2. Alternate picks: each ranker selects its highest-ranked remaining item for the interleaved list.
3. When both rankers agree on the same item at a position, it's left unassigned (contributes no signal).
4. When they disagree, a **competitive pair** is created — these pairs carry the signal.

$$
\text{Preference score} = \frac{\text{clicks on Team A items} - \text{clicks on Team B items}}{\text{total clicks on competitive pairs}}
$$

---

## Competitive pairs and variance reduction

The key insight: only score impressions where rankers disagree. Shared items add noise without signal.

- If two rankers produce identical orderings, a query contributes zero variance.
- This deduplication of shared rankings is the mechanism behind the sensitivity gain.
- Position bias is mitigated by the coin flip (each team's item appears above the other's 50% of the time within pairs).

---

## Attribution for low-frequency conversions

For platforms where conversions are rare (e.g., bookings rather than clicks), attribution logic matters:

- **First-click**: credit the team whose item the user first engaged with.
- **Last-click**: credit the team whose item led to final conversion.
- **Every-click**: credit proportionally across all engagements.

> [!tip] Validate attribution against A/B ground truth
> Run parallel A/B and interleaving experiments; choose the attribution method that best aligns interleaving conclusions with A/B outcomes.

---

## Statistical analysis

- Test statistic: 1-sample t-test on per-query preference margin.
- Null hypothesis: no preference (margin = 0).
- Each query with competitive pairs contributes one observation.
- Confidence intervals on win rate or preference score.

```python
import numpy as np
from scipy import stats

# scores: per-query preference margin (positive = Team A preferred)
scores = np.array([...])  # one entry per query with competitive pairs

# 1-sample t-test: is mean score different from 0?
t_stat, p_value = stats.ttest_1samp(scores, 0)

# confidence interval
n = len(scores)
se = scores.std(ddof=1) / np.sqrt(n)
ci_95 = (scores.mean() - 1.96 * se, scores.mean() + 1.96 * se)
```

---

## Three-phase experimentation pipeline

1. **Offline evaluation**: NDCG, MAP, or other IR metrics on held-out judgments.
2. **Interleaving**: fast online signal with minimal traffic (often ~6% of A/B traffic, 1/3 the duration).
3. **A/B test**: full causal validation of business metrics for candidates that pass interleaving.

> [!check] Pipeline logic
> - Offline filters out clearly bad models (cheap).
> - Interleaving identifies promising candidates (fast, sensitive).
> - A/B confirms causal metric impact (definitive but expensive).

---

## Practical considerations

- **Traffic efficiency**: multiple interleaving "lanes" can run in parallel, each hosting one experiment.
- **Agreement rate**: Airbnb reports ~82% agreement between interleaving and A/B conclusions.
- **False positive rate**: typically very low — interleaving is conservative for detecting real differences.
- **Carryover**: minimal in ranking contexts since each query is independent.

---

## Relation to counterfactual evaluation

Interleaving requires online traffic; **counterfactual evaluation** (off-policy evaluation) uses logged data to estimate alternative ranking performance without deployment. The two are complementary:

- Interleaving: online, within-user, high sensitivity, requires live traffic.
- Counterfactual/OPE: offline, uses logged propensities, no live traffic needed, but requires overlap.

See [[off-policy evaluation]] for the OPE framework.

---

## Common pitfalls

> [!warning]
> - Applying to rankers that optimize page-level composition (diversity constraints) — interleaving disrupts the intended set.
> - Ignoring position bias without proper coin-flip randomization.
> - Using click-based credit for conversion-based metrics without validation.
> - Treating interleaving as a replacement for A/B (it measures preference, not causal business impact).
> - Running too few queries to achieve significance (power depends on competitive pair rate).

---

## Related notes

- [[AB Testing (MOC)]] · [[Experimental Design (MOC)]]
- [[off-policy evaluation]] · [[exposure logging]]
- [[sequential testing]] · [[power analysis]]
- [[ML-assisted variance reduction]] · [[Controlled Experiments Using Pre-Experiment Data (CUPED)|CUPED]]

---

## References

- Zhang, Deng, Du, Gao, He, & Katariya (2025). "Harnessing the Power of Interleaving and Counterfactual Evaluation for Airbnb Search Ranking." KDD 2025.
- Chapelle, Joachims, Radlinski, & Yue (2012). "Large-scale Validation and Analysis of Interleaved Search Evaluation." TOIS.
- Radlinski & Craswell (2010). "Comparing the sensitivity of information retrieval metrics." SIGIR.
