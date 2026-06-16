---
title: RMSPE
aliases: [root mean squared prediction error, root mean square prediction error]
tags: [prediction, diagnostics, synthetic-control]
updated: 2026-06-16
---

# RMSPE

> [!summary] Quick definition
> RMSPE is the square root of the average squared prediction error.

## When it matters

RMSPE is a scale-dependent fit metric:
$$
\operatorname{RMSPE} = \sqrt{\frac{1}{T}\sum_{t=1}^T (Y_t - \hat Y_t)^2}.
$$

In synthetic control, pre-treatment RMSPE summarizes how closely the weighted donor pool tracks the treated unit before treatment. It is often used to filter poor placebo units or scale post/pre fit ratios in permutation-style diagnostics.

Low RMSPE supports pre-treatment fit, but it is not identification by itself. A good-looking pre-period can still fail if the donor pool is affected by spillovers, the treated unit has unique unmodeled shocks, or the intervention timing is endogenous.

## Diagnostics

- Plot pre-treatment residuals, not just the scalar RMSPE.
- Compare treated-unit RMSPE with donor placebo RMSPEs.
- Check sensitivity to donor pool, predictors, and pre-period length.

## Related notes

- [[placebo test]]
- [[Synthetic Control]]
- [[Prophet]]
- [[MASE]]
