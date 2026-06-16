---
title: Highest Density Interval (HDI)
aliases: [Highest Density Interval, Highest Posterior Density, HPD, HPDI, highest posterior density interval, HDI, highest density interval]
tags: [bayesian, intervals, uncertainty, credible-intervals, hdi, testing]
updated: 2025-09-25
---

# Highest Density Interval (HDI)

> [!summary] Quick definition
> The Highest Density Interval (HDI), also called Highest Posterior Density (HPD) interval, is the Bayesian credible set of a given probability mass (e.g., 95%) containing only points whose posterior density is at least as high as any point outside the set. For unimodal symmetric posteriors, the HDI equals the equal‑tailed interval; for skewed or multimodal posteriors, the HDI is generally shorter and may be disjoint. See [[Bayesian Testing]] and [[Region of Practical Equivalence (ROPE)|ROPE]].

- Purpose: summarize posterior uncertainty with minimal‑width (highest‑density) sets.
- Scope: 1D intervals, circular variables (wrap‑around), and multidimensional HD regions via isodensity contours.
- Related: [[Bayesian Testing]] · [[Region of Practical Equivalence (ROPE)|ROPE]] · [[Markov Chain Monte Carlo (MCMC)|MCMC]] · [[Sequential Monte Carlo (SMC)|SMC]] · [[priors]]

---

## Definition

Let p(θ|y) be the posterior density. The 100(1−α)% HD region is
$$
\mathcal{H}_{1-\alpha}
= \{\theta:\; p(\theta\mid y) \ge k_\alpha\},
\quad\text{with}\quad
\int_{\mathcal{H}_{1-\alpha}} p(\theta\mid y)\, d\theta = 1-\alpha,
$$
where k_α is the largest threshold that achieves the target mass. In 1D and unimodal cases, the HDI is a single interval [L, U] with p(L|y) = p(U|y) and posterior mass 1−α between them.

- Symmetric unimodal posteriors (e.g., Normal): HDI equals equal‑tailed interval.
- Skewed posteriors (e.g., Beta, Gamma): HDI differs from equal‑tailed and is typically shorter.
- Multimodal posteriors: HD region can consist of multiple disjoint intervals.

---

## How to compute

### Closed forms (special cases)

- Normal posterior: if θ|y ~ 𝓝(μ, σ²),
$$
\text{HDI}_{1-\alpha} = \big[\mu - z_{1-\alpha/2}\,\sigma,\;\mu + z_{1-\alpha/2}\,\sigma\big].
$$
- Exponential family with conjugacy often yields analytic or easily computed HDIs via solving p(L)=p(U) and mass constraints (e.g., Beta, Gamma).

### From posterior samples (MCMC/SMC)

1D shortest‑interval method:
1) Sort posterior draws θ^{(1)} ≤ … ≤ θ^{(S)}.  
2) Let m = ⌊(1−α)·S⌋.  
3) For i=1..S−m, form candidate interval [θ^{(i)}, θ^{(i+m)}]; choose the one with minimal width.  
4) Return that as the 1D HDI.

> [!example] Python-like
> ```python
> import numpy as np
> def hdi_1d(samples, cred_mass=0.95):
>     x = np.sort(np.asarray(samples))
>     s = len(x); m = int(np.floor(cred_mass*s))
>     widths = x[m:] - x[:s-m]
>     j = np.argmin(widths)
>     return float(x[j]), float(x[j+m])
> ```

Isodensity threshold (general, possibly multimodal):
- Compute posterior log density for samples (via model or KDE).  
- Find threshold k_α such that the top‑mass set {draws with log p ≥ k_α} contains proportion 1−α of posterior mass; report union of intervals (1D) or level‑set region (multi‑D).

Multidimensional HD region:
- Define region {θ: p(θ|y) ≥ k_α}; approximate by KDE or model log posterior; choose k_α to include 1−α mass. Visualize via contour lines.

Circular variables:
- Work in angle space \[−π, π) and allow wrap‑around shortest arc covering 1−α mass.

Weighted samples:
- Replace counts with weights in both methods; for shortest interval, accumulate weights until reaching 1−α and minimize width.

---

## HDI vs equal‑tailed CI

- Equal‑tailed credible interval (ETI): bounds at α/2 and 1−α/2 quantiles; invariant to reparameterization monotone transforms in the quantile sense.
- HDI: minimizes width in density space; differs from ETI when skewed or multimodal; not simply the quantiles unless symmetric.
- Communication: report both when skewness is strong; HDI often aligns better with high‑probability regions.

---

## Properties and cautions

- Invariance:
  - Credible sets must be computed in the parameterization of interest; transforming an HDI by a nonlinear map is not, in general, the HDI of the transformed parameter (Jacobian changes density). Recompute HDI on the target scale.
- Nonuniqueness:
  - If p(θ|y) has flat tops or plateaus, multiple HDIs achieve the same density threshold; any such set is valid.
- Discreteness:
  - For discrete parameters, the HD set is the smallest set of categories with cumulative posterior ≥ 1−α (take those with largest posterior mass).
- Constrained supports:
  - For parameters on \[0,1] or (0,∞), HDIs may abut boundaries; shortest‑interval and isodensity methods handle this naturally.

---

## Using HDI with ROPE

- HDI+ROPE decision rule (common in practice; see [[Region of Practical Equivalence (ROPE)|ROPE]]):
  - If the 95% HDI lies entirely inside ROPE → practical equivalence.
  - If the 95% HDI lies entirely outside ROPE → meaningful effect.
  - If it overlaps → inconclusive (consider more data or decision‑theoretic thresholds).

---

## Diagnostics and good practice

> [!check]
> - [ ] Convergence/mixing of posterior sampler ([[Markov Chain Monte Carlo (MCMC)|MCMC]]): multiple chains, R̂≈1, effective sample size  
> - [ ] Robustness: HDI stable across seeds, thinning, KDE bandwidths (if used)  
> - [ ] Scale: compute HDI on decision‑relevant parameterization (e.g., risk difference vs log‑odds)  
> - [ ] Multimodality: consider disjoint HDIs or report full posterior plots  
> - [ ] Sensitivity to α: show 50%, 80%, 95% HDIs to convey concentration

---

## Common pitfalls

> [!warning]
> - Reporting only point estimates without uncertainty  
> - Confusing frequentist coverage with Bayesian credibility; HDIs are posterior, not long‑run frequency guarantees  
> - Transforming HDIs between scales without recomputation  
> - Ignoring multimodality; a single interval can be misleading when the posterior has multiple modes

---

## Reporting essentials

- Credible mass (e.g., 95%), HDI bounds, posterior mean/median, and visualization (density with HDI marked)
- Parameterization and scale; prior specification; computation method (closed form vs MCMC/KDE)
- If used for decisions: ROPE bounds and result; posterior probabilities Pr(θ>0), etc.
- Sensitivity: alternative α, alternative parameterizations

---

## Examples

> [!example] Beta posterior HDI
> For θ|y ~ Beta(a,b), the 95% HDI endpoints L,U satisfy p(L)=p(U) and Pr(L≤θ≤U)=0.95. Numerically solve for L,U; many libraries provide hdi for Beta.

> [!example] Multimodal mixture
> For θ|y a two‑component Gaussian mixture, the 95% HD region can be two intervals around each mode. Use isodensity thresholding on posterior draws and report the union.

---

## Related notes

- [[Bayesian Testing]]
- [[Region of Practical Equivalence (ROPE)]]
- [[Markov Chain Monte Carlo (MCMC)]]

---

## References

- Box & Tiao (1973). Bayesian Inference in Statistical Analysis.  
- Bernardo & Smith (1994). Bayesian Theory.  
- Gelman, Carlin, Stern, Dunson, Vehtari, & Rubin (2013/2020). Bayesian Data Analysis.  
- Chen, Shao, & Ibrahim (2000). Monte Carlo Methods in Bayesian Computation.  
- Kruschke (2015). Doing Bayesian Data Analysis (HDI+ROPE usage).  

---
