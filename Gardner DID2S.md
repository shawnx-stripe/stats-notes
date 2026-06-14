---
title: Gardner DID2S
aliases:
  - DID2S
  - two-stage DiD
tags:
  - causal-inference
  - did
  - panel-data
updated: 2026-03-03
---

# Gardner DID2S

> [!summary] Quick definition
> A two-stage estimator for [[Difference-in-Differences (DiD)]] with [[staggered adoption]] (Gardner, 2022). Stage 1 estimates unit and time fixed effects using only untreated observations; stage 2 regresses the residualized outcome on treatment indicators. This avoids the contamination bias of [[two-way fixed effects]] when treatment effects are heterogeneous.

---

## Procedure

**Stage 1** — Estimate the untreated model on observations with $D_{it}=0$:

$$
Y_{it} = \alpha_i + \gamma_t + \varepsilon_{it} \quad \text{for } D_{it}=0
$$

Obtain $\hat\alpha_i$ and $\hat\gamma_t$.

**Stage 2** — For **all** observations, compute residuals and regress on treatment:

$$
\tilde Y_{it} = Y_{it} - \hat\alpha_i - \hat\gamma_t
$$

$$
\tilde Y_{it} = \tau D_{it} + u_{it}
$$

The coefficient $\hat\tau$ is the DID2S treatment effect estimate. For event-study specifications, replace $D_{it}$ with event-time dummies.

> [!note] Relationship to BJS
> Gardner DID2S and [[Borusyak–Jaravel–Spiess (imputation)]] are numerically very similar (often identical for simple specs). Both estimate FEs from untreated data only. DID2S frames it as a two-stage regression; BJS as imputation + residual averaging.

---

## Standard errors

- Stage 2 SEs must account for the estimation error from stage 1.
- The `did2s` package provides valid SEs via a GMM-style correction.
- Cluster at the treatment-assignment level as usual.

---

## Minimal code snippets

> [!example] R

```r
# install.packages("did2s")
library(did2s)

# df: panel with id, time, Y, treatment indicator D,
# first_treat (adoption time; Inf or 0 for never-treated)
res <- did2s(
  data = df, yname = "Y", first_stage = ~ 0 | id + time,
  second_stage = ~ i(D), treatment = "D",
  cluster_var = "id"
)
summary(res)
```

> [!example] Stata

```stata
* ssc install did2s
did2s Y, first_stage(id time) second_stage(D) treatment(D) cluster(id)
```

---

## Related notes

- [[Difference-in-Differences (DiD)]] · [[two-way fixed effects]] · [[staggered adoption]]
- [[Borusyak–Jaravel–Spiess (imputation)]] · [[Callaway–Sant'Anna estimator]] · [[Sun–Abraham estimator]]
- [[Goodman–Bacon decomposition]] · [[event study]]
- [[Causal Inference (MOC)]]
