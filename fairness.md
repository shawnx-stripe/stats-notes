---
title: Fairness
aliases: [fairness, algorithmic fairness, fairness constraints, group fairness]
tags: [ml, experimentation, policy-learning, diagnostics]
updated: 2026-04-02
---

# Fairness

> [!summary] Quick definition
> Fairness asks whether model decisions, treatment assignment, or measured outcomes differ across relevant groups in ways that are unacceptable for the product, policy, or experiment.

## What to check

- Exposure or treatment-rate differences by protected or operational groups.
- Outcome-quality differences conditional on assignment.
- Constraint compliance under deployment rules, not just offline model scores.

## Minimal code snippets

```python
group_rates = df.groupby("group")["treat"].mean()
group_outcomes = df.groupby("group")["outcome"].mean()
print(group_rates)
print(group_outcomes)
```

## Related notes

- [[policy learning]] · [[bandits]] · [[uplift]] · [[guardrail metric]]
