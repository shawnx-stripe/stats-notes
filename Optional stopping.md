---
title: Optional Stopping
aliases: [Optional stopping, optional stopping problem, peeking]
tags: [experimentation, sequential, ab-testing]
updated: 2026-03-05
---

# Optional Stopping

> [!summary]
> Practice of monitoring experiment results and stopping when significance is reached, inflating the false positive rate above the nominal $\alpha$. Addressed by [[sequential testing]] methods that control type I error under continuous monitoring.

## Why it's a problem

If you repeatedly test $H_0: \mu = 0$ as data accumulate and stop when $p < 0.05$, the probability of eventual rejection under the null can exceed 0.80 (instead of 0.05). The test statistic exhibits random walks; you will eventually see a spurious "significant" result.

## Solutions

| Method | Approach |
|--------|----------|
| [[sequential testing]] | Use time-adjusted critical values (e.g., O'Brien–Fleming, Pocock) |
| [[mSPRT]] | Mixture sequential probability ratio test with controlled type I error |
| [[Always Valid Inference (AVI)]] | Confidence sequences valid at all stopping times |
| Pre-commit to fixed $N$ | No peeking; single test at end |

> [!warning]
> "Peeking" at results is only safe if you use sequential testing methods. Standard $p$-values are invalid under optional stopping.

## Example calculation

```python
import numpy as np
# Simulate null (mu=0) with optional stopping
n_sims = 10000
rejections = 0
for _ in range(n_sims):
    data = []
    for i in range(1, 1001):
        data.append(np.random.normal(0, 1))
        if i >= 30:
            from scipy.stats import ttest_1samp
            _, p = ttest_1samp(data, 0)
            if p < 0.05:
                rejections += 1
                break
print(f"False positive rate: {rejections / n_sims:.2f}")  # >> 0.05
```

## Related notes

- [[sequential testing]]
- [[Sequential and Adaptive Experiments (MOC)]]
