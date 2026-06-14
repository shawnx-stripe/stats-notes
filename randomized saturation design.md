---
title: randomized saturation design
aliases: [saturation design, two-stage randomization, cluster saturation, partial interference design, Hudgens–Halloran design]
tags: [experimentation, interference, spillovers, cluster-randomized, design, policy, causal-inference]
updated: 2025-09-17
---

# randomized saturation design

> [!summary] Quick definition
> A randomized saturation design assigns clusters (schools, geos, villages, markets) to different treatment shares (saturation levels), and then randomizes treatment to individuals within clusters at the assigned share. By varying saturation across clusters, it identifies direct (own-treatment) and spillover (exposure) effects under partial interference.

- Use when interference/spillovers within clusters are likely and of interest.
- Outputs: direct effect at a given saturation, spillover/indirect effects across saturation levels among the untreated, and overall/policy effects of changing saturation.

See also: [[interference]] · [[spillovers]] · [[No spillovers]] · [[geo experiment]].

---

## Why use saturation designs

- Standard RCTs assume no interference (SUTVA). When peers or market conditions within clusters affect outcomes, effects depend on how many others are treated.
- Randomizing the within-cluster treatment probability (saturation) provides variation to disentangle:
  - Direct effect of own treatment (holding cluster exposure fixed),
  - Indirect (spillover) effect of others’ treatment (for the untreated),
  - Overall/policy effect of raising saturation.

---

## Setup and notation

- Clusters c = 1,…,C; individuals i in cluster c.
- Saturation levels S ∈ {s₁, s₂, …} (e.g., 0, 1/3, 2/3, 1). Stage 1: assign each cluster to s_c ∈ S.
- Stage 2: within cluster c, assign individual treatment D_ic ∼ Bernoulli(s_c) (or exactly s_c·n_c treated).
- Potential outcomes with interference (exposure mapping):
  - Y_ic(d, e) where d ∈ {0,1} is own assignment and e summarizes others’ treatment in c (often e ≈ s_c).

Key estimands (Hudgens–Halloran style):
- Direct effect at saturation e:
  $$
  DE(e) = \mathbb{E}\big[Y(1,e) - Y(0,e)\big].
  $$
- Spillover (indirect) effect on untreated when moving saturation e₀→e₁:
  $$
  IE_0(e_1,e_0) = \mathbb{E}\big[Y(0,e_1) - Y(0,e_0)\big].
  $$
- Overall/policy effect of changing saturation e₀→e₁:
  $$
  OE(e_1,e_0) = \mathbb{E}\big[Y(1,e_1)\big] - \mathbb{E}\big[Y(0,e_0)\big],
  $$
  often operationalized as the difference in average outcomes between clusters assigned e₁ vs e₀.

> [!note] Partial interference
> Design assumes interference only within clusters, not across clusters (exposure is governed by s_c).

---

## Design choices

- Saturation set S: include multiple levels (e.g., {0, 1/3, 2/3, 1}) to separate direct and spillover effects. Include pure control (0) and, when feasible, 100% saturation for policy bounds.
- Within-cluster assignment: Bernoulli(s_c) or fixed counts (exact s_c); stratify by cluster size if variable.
- Blocking/stratification: assign saturation within blocks of similar clusters (size, baseline outcome) to improve efficiency.
- Buffers/geography: use geographic buffers to limit cross-cluster spillovers; or diagnose with [[Conley standard errors]].

---

## Estimation (design-based)

Within saturation strata and across saturation levels:

- Direct effect at e:
  - Compare treated vs untreated within clusters assigned saturation e; aggregate across clusters:
  $$
  \widehat{DE}(e) = \Big[\bar Y_{D=1 \mid s=e} - \bar Y_{D=0 \mid s=e}\Big] \quad \text{(HT/Hájek weighted if needed).}
  $$

- Spillover on untreated (e₀→e₁):
  - Compare untreated across saturation levels:
  $$
  \widehat{IE}_0(e_1,e_0) = \bar Y_{D=0 \mid s=e_1} - \bar Y_{D=0 \mid s=e_0}.
  $$

- Overall/policy effect (e₀→e₁):
  - Compare cluster-level means across e₁ vs e₀ (mixing treated and untreated):
  $$
  \widehat{OE}(e_1,e_0) = \bar Y_{\mid s=e_1} - \bar Y_{\mid s=e_0}.
  $$

Regression-based (two-stage randomization aware):
- Individual level (simple):
  $$
  Y_{ic} = \alpha + \beta D_{ic} + \sum_{e\in S\setminus e_0} \gamma_e \mathbf{1}\{s_c=e\} + \sum_{e} \delta_e \big(D_{ic}\cdot \mathbf{1}\{s_c=e\}\big) + X_{ic}'\theta + \varepsilon_{ic}.
  $$
  - β (or δ_e) identifies direct effect at baseline (or at e); γ_e trace spillover among untreated; δ_e allow direct effects to vary with e.
  - Use cluster-robust SEs at the cluster level; include block FE if blocked.

- Cluster-level (means):
  - Regress cluster mean outcomes on saturation dummies; within e, regress within-cluster treated-minus-untreated difference on a constant to estimate DE(e).

Inference:
- Cluster-robust SEs; with few clusters, apply [[few-cluster corrections]] or randomization inference respecting the two-stage assignment.

---

## Randomization inference (recommended)

- Permute saturation labels across clusters within blocks, and within each cluster permute individual assignments consistent with s_c.
- Recompute estimands to obtain exact (or approximate) p-values under the design.

---

## Power and sample size

- Drivers: number of clusters per saturation level, cluster sizes, ICC (intra-cluster correlation), number of saturation levels, and effect magnitudes (DE and IE).
- Planning tips:
  - Ensure adequate clusters per level (balanced across S).
  - Larger ICC reduces effective information; prioritize more clusters over larger clusters.
  - Include pure control and at least one intermediate saturation to estimate spillovers.
  - Use simulations with plausible ICC and variance to assess MDE for DE(e) and IE_0(e₁,e₀). See [[power analysis]].

---

## Minimal code snippets

> [!example] R: assignment and simple estimators

```r
set.seed(123)
# C clusters, sizes n_c
C <- 60
sizes <- rpois(C, lambda = 80) + 20
Sats <- c(0, 1/3, 2/3, 1)
s_c <- sample(Sats, C, replace = TRUE)

# Assign individuals
cluster_id <- rep(1:C, times = sizes)
s_assigned <- s_c[cluster_id]
D <- rbinom(length(cluster_id), 1, prob = s_assigned)

# Suppose we simulate outcomes with spillovers:
# Y = tau*D + eta*s_assigned + noise + cluster RE
tau <- 0.2; eta <- 0.1
u_c <- rnorm(C, 0, 0.3)[cluster_id]
Y <- tau*D + eta*s_assigned + u_c + rnorm(length(D), 0, 1)

df <- data.frame(c=cluster_id, s=s_assigned, D=D, Y=Y)

# Direct effect at s = 1/3
e <- 1/3
with(subset(df, s==e), mean(Y[D==1]) - mean(Y[D==0]))

# Spillover on untreated between e1=2/3 and e0=0
with(subset(df, s==2/3 & D==0), mean(Y)) - with(subset(df, s==0 & D==0), mean(Y))
```

> [!example] R: regression with cluster-robust SEs

```r
library(lmtest); library(sandwich)
df$s_fac <- factor(df$s)
fit <- lm(Y ~ D * s_fac, data = df)
# Cluster-robust by cluster c
vc <- vcovCL(fit, cluster = ~ c, type = "HC1")
coeftest(fit, vcov = vc)
```

> [!example] Stata: cluster-robust regression

```stata
* s is categorical saturation; D is individual assignment
xi: reg Y i.s##c.D, vce(cluster c)
* Direct effect at baseline saturation is _b[c.D]; interactions give differences at other s levels
```

> [!example] Randomization inference (sketch in R)

```r
B <- 1000
stat_obs <- with(subset(df, s==1/3), mean(Y[D==1]) - mean(Y[D==0]))
stat_sim <- replicate(B, {
  # permute individual treatment within clusters consistent with s_c
  D_sim <- unlist(lapply(1:C, function(cc){
    n <- sum(df$c==cc); p <- unique(df$s[df$c==cc])[1]
    rbinom(n, 1, p)
  }))
  with(subset(transform(df, D=D_sim), s==1/3), mean(Y[D==1]) - mean(Y[D==0]))
})
p_val <- mean(abs(stat_sim) >= abs(stat_obs))
```

---

## Practical checklist

> [!check]
> - [ ] Define clusters and justify partial interference (within-cluster only)  
> - [ ] Choose saturation set S; include multiple levels and pure control  
> - [ ] Block clusters by size/baseline; randomize saturations within blocks  
> - [ ] Define within-cluster assignment (Bernoulli or fixed counts)  
> - [ ] Pre-register estimands: DE(e), IE_0(e₁,e₀), OE(e₁,e₀), and analysis plan ([[pre-registration]])  
> - [ ] Plan power with ICC and cluster counts; prioritize more clusters  
> - [ ] Instrumentation: log cluster ID, saturation, individual assignment, exposure windows ([[exposure logging]])  
> - [ ] Inference: cluster-robust SEs; few-cluster corrections; consider randomization inference  
> - [ ] Diagnose spillovers across clusters (proximity analyses); consider [[Conley standard errors]] if spatial

---

## Common pitfalls

> [!warning]
> - Too few clusters per saturation level (low power; unstable estimates)  
> - Only extreme saturations (0 vs 1): cannot separate direct vs spillover without modeling assumptions  
> - Cross-cluster interference (media bleed, mobility) invalidating partial interference  
> - Treating cluster-level policy effect as individual effect; be precise about estimand  
> - Ignoring cluster size heterogeneity in assignment or analysis  
> - Using iid SEs; not accounting for few clusters

---

## Reporting essentials

- Saturation levels, number of clusters and sizes per level; blocking/stratification rules
- Within-cluster assignment procedure and adherence
- Estimands (DE, IE, OE) with definitions; identification under partial interference
- Estimation method (design-based differences vs regression), clustering level, small-sample corrections
- Diagnostics: cross-cluster spillovers, balance, baseline comparability; placebo tests
- Results: DE(e) for each e; IE_0 across e pairs; policy contrasts OE(e₁,e₀); uncertainty (CIs/p-values)
- Limitations: residual interference, generalizability, saturation-dependent mechanisms

---

## Related notes

- [[interference]] · [[spillovers]] · [[No spillovers]]  
- [[geo experiment]] · [[switchback experiment]]  
- [[clustered standard errors]] · [[few-cluster corrections]] · [[Conley standard errors]]  
- [[power analysis]] · [[Minimum Detectable Effect (MDE)|MDE]]  
- [[pre-registration]] · [[Experimental Design (MOC)]]

---