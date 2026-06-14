---
title: CLR Test
aliases: [CLR test, conditional likelihood ratio test, Moreira CLR]
tags: [econometrics, iv, weak-instruments, inference]
updated: 2026-03-05
---

# CLR Test

> [!summary]
> Conditional Likelihood Ratio test (Moreira 2003): weak-instrument robust test that conditions on a sufficient statistic for nuisance parameters. Provides correct size regardless of instrument strength; more powerful than [[Anderson–Rubin]].

## When to use

CLR is the preferred test when instruments are weak or of unknown strength. Unlike [[Anderson–Rubin]], which tests joint hypotheses, CLR isolates the structural parameter. It achieves near-optimal power under weak instruments by conditioning on the concentration parameter, making inference robust to first-stage $F < 10$. Particularly valuable in just-identified models where [[Two-Stage Least Squares (2SLS)|2SLS]] SEs are unreliable.

## Stata

```stata
ivreg2 y x (endog = z1 z2), clr  // requires weakiv package
weakivtest  // reports CLR statistic and confidence set
```

> [!note]
> CLR inverts the test to construct confidence intervals. In overidentified models, use [[Anderson–Rubin]] or subset selection to isolate strong instruments first.

## Related notes

- [[Anderson–Rubin]]
- [[weak instruments]]
- [[Two-Stage Least Squares (2SLS)|2SLS]]
- [[Robust Methods (MOC)]]
