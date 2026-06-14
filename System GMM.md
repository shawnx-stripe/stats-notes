---
title: System GMM
aliases: [System GMM, Blundell-Bond, Blundell–Bond estimator]
tags: [econometrics, panel-data, dynamic-panels, gmm]
updated: 2026-03-05
---

# System GMM

> [!summary]
> Augments the [[Arellano–Bond]] difference-GMM estimator by adding level equations with lagged differences as instruments. Exploits additional moment conditions; improves efficiency when the autoregressive parameter is close to unity.

## Moment conditions

**Difference equations** (Arellano–Bond):

$$
E[\Delta\epsilon_{it} \cdot y_{i,t-s}] = 0, \quad s \geq 2
$$

**Level equations** (Blundell–Bond addition):

$$
E[\epsilon_{it} \cdot \Delta y_{i,t-1}] = 0
$$

The level moments require an additional stationarity assumption: $E[\alpha_i \Delta y_{i,t-1}] = 0$. Combined, these provide more instruments and reduce finite-sample bias.

## When to use

- Dynamic panel ($y_{it} = \rho y_{it-1} + \ldots$) with $T$ small
- [[Arellano–Bond]] difference-GMM has weak instruments (when $\rho \approx 1$)
- Series are close to random walk; first-differencing reduces signal

> [!warning]
> System GMM requires the stationarity condition to hold. Test with the Arellano–Bond serial correlation test and the Sargan/Hansen test. If both AB and System GMM reject, difference-GMM may be more robust.

## Stata snippet

```stata
xtabond2 y L.y x1 x2, gmm(L.y, lag(2 .)) iv(x1 x2) robust small
* gmm() specifies GMM-type instruments; iv() for standard instruments
* Add "twostep" for two-step efficient GMM
```

## Related notes

- [[Arellano–Bond]]
- [[Generalized Method of Moments (GMM)|GMM]]
- [[Panel Data Methods (MOC)]]
- [[Nickell bias]]
