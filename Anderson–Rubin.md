---
title: Anderson–Rubin
aliases:
- Anderson–Rubin test
- AR test
- weak-IV robust inference
- Anderson-Rubin
- Anderson-Rubin test
tags:
- econometrics
- iv
- inference
updated: 2026-03-03
---

# Anderson–Rubin

> [!summary] Quick definition
> The Anderson–Rubin (AR) test provides valid inference on structural parameters in [[Instrumental Variables (IV)]] models regardless of instrument strength. Unlike standard Wald/t-tests based on [[Two-Stage Least Squares (2SLS)|two-stage least squares (2SLS)]], the AR test does not require the [[relevance]] condition for valid size, making it the primary tool for [[weak instruments]]-robust inference.

---

## Core idea

Test $H_0: \beta = \beta_0$ by substituting the hypothesized value into the structural equation and testing whether the reduced-form residuals are uncorrelated with instruments:

$$
Y - X_2 \beta_0 = X_1 \gamma + Z \pi + \varepsilon
$$

Under $H_0$ (and the [[exclusion restriction]]), $\pi = 0$. The AR statistic tests this:

$$
AR(\beta_0) = \frac{(Y - X_2\beta_0)' P_{M_1 Z} (Y - X_2\beta_0) \,/\, q}{(Y - X_2\beta_0)' M_{[X_1, Z]} (Y - X_2\beta_0) \,/\, (n - k_1 - q)}
$$

where $q$ = number of excluded instruments, $P_{M_1 Z}$ projects onto instruments after partialing out $X_1$.

Under $H_0$: $AR \sim F(q, n - k_1 - q)$ regardless of instrument strength.

---

## Confidence intervals

Invert the AR test: the AR confidence set is all $\beta_0$ values not rejected at level $\alpha$:

$$
\text{CI}_{\text{AR}} = \{\beta_0 : AR(\beta_0) \le F_{q, n-k_1-q}^{1-\alpha}\}
$$

> [!note] Properties
> - Valid even with arbitrarily weak instruments
> - With just-identified models ($q = 1$), the AR CI has correct size and is the standard approach
> - With over-identified models ($q > k_2$), the AR test has lower power because it jointly tests exclusion + the null — consider the CLR test (Moreira, 2003) for better power in this case

---

## When to use

> [!check] Use AR when
> - First-stage F is below conventional thresholds (~10 for Stock–Yogo)
> - You want inference that is robust to instrument strength
> - As a robustness check alongside standard 2SLS Wald CIs

---

## Minimal code snippets

> [!example] R

```r
library(AER)
fit <- ivreg(y ~ x1 + x2 | x1 + z, data = df)
summary(fit, diagnostics = TRUE)  # includes weak-IV diagnostics

# For explicit AR test/CI:
# install.packages("ivmodel")
library(ivmodel)
iv <- ivmodel(Y = df$y, D = df$x2, Z = df$z, X = df$x1)
AR.test(iv)    # AR test
AR.power(iv)   # power analysis
```

> [!example] Stata

```stata
* weakiv provides AR, CLR, and K tests
* ssc install weakiv
ivreg2 y (x2 = z) x1, robust
weakiv
```

---

## Related notes

- [[Instrumental Variables (IV)]] · [[Two-Stage Least Squares (2SLS)|two-stage least squares (2SLS)]] · [[Limited Information Maximum Likelihood (LIML)|LIML]]
- [[weak instruments]] · [[exclusion restriction]] · [[relevance]]
- [[Causal Inference (MOC)]] · [[Econometrics (MOC)]]
