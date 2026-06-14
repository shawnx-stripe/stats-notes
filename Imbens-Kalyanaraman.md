---
title: Imbens–Kalyanaraman
aliases: [Imbens-Kalyanaraman, Imbens–Kalyanaraman, IK bandwidth, IK optimal bandwidth, "Imbens–Kalyanaraman (IK) bandwidth"]
tags: [econometrics, rdd]
updated: 2026-03-05
---

# Imbens–Kalyanaraman

> [!summary]
> MSE-optimal bandwidth selector for local linear RDD estimation (Imbens & Kalyanaraman 2012). Predecessor to [[Calonico-Cattaneo-Titiunik]] (CCT) bandwidth. Balances bias and variance of the local polynomial estimator at the cutoff.

## Bandwidth Formula

The IK bandwidth minimizes the MSE of the local linear RDD estimator at the cutoff:

$$
h_{\text{IK}} = C_{\text{IK}} \cdot \left(\frac{\hat{\sigma}^2_+^2 + \hat{\sigma}^2_-^2}{n \cdot (\hat{m}^{(2)}_+ - \hat{m}^{(2)}_-)^2}\right)^{1/5}
$$

where $\hat{m}^{(2)}_\pm$ are estimates of the second derivative of the conditional mean on each side of the cutoff, and $C_{\text{IK}}$ is a constant depending on the kernel.

> [!tip]
> - **CCT improvement**: [[Calonico-Cattaneo-Titiunik]] bandwidth uses more robust derivative estimates and adds bias correction
> - **Rule-of-thumb**: IK bandwidth is now considered a starting point; use CCT in practice via [[rdrobust]]
> - **Sensitivity**: Always report estimates across multiple bandwidths (e.g., $0.5h$, $h$, $1.5h$)

## Code

```r
# R: IK bandwidth (rdrobust package defaults to CCT)
library(rdrobust)
rd <- rdrobust(y, running_var, c = cutoff, bwselect = "mserd")
summary(rd)  # uses CCT MSE-optimal bandwidth
```

## Related notes

- [[Regression Discontinuity Design (RDD)]]
- [[Calonico-Cattaneo-Titiunik]]
- [[bandwidth selection]]
