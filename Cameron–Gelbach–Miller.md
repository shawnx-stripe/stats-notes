---
title: Cameron–Gelbach–Miller
aliases:
- CGM
- two-way clustered standard errors
- Cameron Gelbach Miller
- Cameron-Gelbach-Miller
tags:
- inference
- standard-errors
- clustering
- variance
- econometrics
- panels
- DiD
- OLS
updated: 2025-09-24
---

# Cameron–Gelbach–Miller

> [!summary] Quick definition
> Cameron–Gelbach–Miller (CGM) provide a multiway cluster-robust variance estimator for linear models when errors may be correlated within multiple clustering dimensions (e.g., unit and time). For two-way clustering, the variance is the sum of one-way clustered variances minus the variance clustered on intersection groups. See [[clustered standard errors]] for one-way clustering and [[few-cluster corrections]]/[[wild cluster bootstrap]] when cluster counts are small.

- Purpose: valid standard errors and tests when errors are correlated within each of several non-nested clustering dimensions.
- Typical use: panels (cluster by unit and by time), multi-market data (e.g., firm and industry), network dyads (sender, receiver).
- Related: [[Conley standard errors]] (spatial correlation), [[Difference-in-Differences (DiD)]], [[two-way fixed effects]], [[Ordinary Least Squares (OLS)|OLS]].

---

## Setup

Consider OLS with y = Xβ + u on n observations. Each observation belongs to one cluster in each of R clustering dimensions r=1,…,R (e.g., firm, time).

- Let G_r be the set of clusters along dimension r; for any nonempty subset S ⊆ {1,…,R}, define intersection clusters as unique tuples across S.
- For any clustering scheme C (a partition of {1,…,n}), define the cluster-robust “meat”:
$$
\widehat{B}_C
\;=\;
\sum_{g \in C} X_g' \hat u_g \hat u_g' X_g,
$$
where X_g stacks rows of X and ŭ_g stacks residuals for observations in cluster g. The usual (one-way) CRV1 variance is:
$$
\widehat{V}_C
\;=\;
(X'X)^{-1}\, \widehat{B}_C \, (X'X)^{-1}.
$$

---

## CGM multiway variance

- Two-way clustering (A and B):
$$
\widehat{\mathrm{Var}}_{\text{CGM}}(\hat\beta)
\;=\;
\widehat{V}_{A}
\;+\;
\widehat{V}_{B}
\;-\;
\widehat{V}_{A \cap B}.
$$

- R-way clustering (inclusion–exclusion over all nonempty subsets S):
$$
\widehat{\mathrm{Var}}_{\text{CGM}}(\hat\beta)
\;=\;
\sum_{\emptyset \neq S \subseteq \{1,\dots,R\}}
(-1)^{|S|+1}\;\widehat{V}_{\cap S},
$$
where “∩ S” denotes clustering on the intersection groups formed by all dimensions in S.

> [!tip] Degrees-of-freedom scaling
> Many implementations multiply each one-way component by a finite-sample factor (e.g., CRV1):
> $$
> \lambda_C
> \;=\;
> \frac{G_C}{G_C-1} \cdot \frac{n-1}{n-k},
> \qquad
> \widehat{V}^{\,\text{CRV1}}_{C} = \lambda_C \,(X'X)^{-1}\widehat{B}_C(X'X)^{-1},
> $$
> where G_C is the number of (intersection) clusters in scheme C and k is the number of coefficients. Check your software’s defaults.

---

## Assumptions and scope

- Within-cluster dependence is unrestricted for each clustering dimension; across-cluster independence (or weak dependence that vanishes asymptotically).
- Asymptotics: the number of clusters must grow in each clustering dimension; large, heterogeneous cluster sizes are allowed.
- Clustering dimensions need not be nested; intersections handle overlap automatically.
- Works with absorbed fixed effects; use residuals from the estimated model.

> [!warning]
> - If any clustering dimension has few clusters (e.g., G ≤ 30, especially ≤ 10), CGM asymptotics can be unreliable. Prefer [[few-cluster corrections]] (e.g., CR2/CR3) or [[wild cluster bootstrap]] for inference.

---

## When to use CGM

- Panel regressions with potential correlation within units and within time.
- Multi-index data (e.g., student-by-class with school effects; firm-by-market with calendar shocks).
- Two-way FE [[Difference-in-Differences (DiD)]] with serial correlation across units and common shocks over time.

---

## Implementation notes

- Ensure cluster identifiers exist for each dimension and for their intersections (software typically constructs intersections internally).
- Absorbing fixed effects does not replace clustering; FE remove mean shifts but not serial/common-shock correlation in errors.
- Non-PSD issues are rare but can arise numerically; symmetrize the covariance (V ← (V+V')/2) if needed.

---

## Software

- Stata
  - reghdfe: absorb high-D FE; vce(cluster id time) implements CGM two-way (and multiway) clustering.
  - ivreg2: vce(cluster id time) supports multiway clustering.
  - boottest: wild cluster bootstrap with multiway clusters for robust p-values/CIs.

- R
  - fixest::feols(..., cluster = ~ id + time) or vcov = ~ id + time.
  - sandwich::vcovCL(fit, cluster = ~ id + time) with lmtest::coeftest.
  - multiwayvcov::cluster.vcov for base lm/glm; clubSandwich for small-sample corrections.

- Python
  - linearmodels (PanelOLS/IV2SLS): cov_type="clustered", clusters=DataFrame with multiple cluster cols.
  - statsmodels: multiway clustering available via cov_type="cluster" with groups, groups2 (version-dependent).

---

## Examples

> [!example] Stata (two-way clustering)
> reg y x1 x2 i.year, vce(cluster firm year)  
> reghdfe y x1 x2, a(firm year) vce(cluster firm year)

> [!example] R (fixest)
> fit <- fixest::feols(y ~ x1 + x2 | firm + year, data = df, cluster = ~ firm + year)  
> se <- fixest::se(fit)

> [!example] Python (linearmodels)
> from linearmodels.panel import PanelOLS  
> `mod = PanelOLS(df.y, df.loc[:, ['x1', 'x2']], entity_effects=True, time_effects=True)`  
> `res = mod.fit(cov_type='clustered', clusters=df.loc[:, ['firm', 'year']])`

---

## Connections and alternatives

- Spatial and distance-based correlation: use [[Conley standard errors]] when correlation decays with distance rather than within discrete clusters.
- Few clusters: see [[few-cluster corrections]] (e.g., CR2/CR3 via clubSandwich) and [[wild cluster bootstrap]] for p-values/CIs.
- Randomization-based inference: [[randomization inference]] can complement when treatment is assigned at cluster level.

---

## Reporting essentials

- Clustering dimensions used (e.g., firm and year) and counts of clusters in each and their intersections.
- Any finite-sample corrections (CRV1/CR2/CR3) and software versions.
- Sensitivity: results under alternative clustering schemes (e.g., triple clustering if relevant) and robustness with wild cluster bootstrap.

---

## Additional references

- Cameron, A. C., & Miller, D. L. (2015). A practitioner’s guide to cluster-robust inference. Journal of Human Resources, 50(2), 317–372.  
- Thompson, S. B. (2011). Simple formulas for standard errors that cluster by both firm and time. Journal of Financial Economics, 99(1), 1–10.  
- MacKinnon, J. G., Nielsen, M. Ø., & Webb, M. D. (2022). Cluster-robust inference: A guide to empirical practice. Journal of Econometrics (overview, small-sample issues).  

---

## Appendix: Inclusion–exclusion derivation (sketch)

Let u be the true regression disturbance and ŭ the OLS residual. The cluster-robust covariance for a clustering scheme C has “meat”
$$
\widehat{B}_C = \sum_{g \in C} X_g' \hat u_g \hat u_g' X_g.
$$
If errors exhibit within-cluster covariance along multiple dimensions (e.g., A and B), add contributions from each dimension, but subtract the double-counted intersection:
$$
\widehat{B}_{\text{CGM}} = \widehat{B}_{A} + \widehat{B}_{B} - \widehat{B}_{A\cap B}.
$$
Generalizing to R dimensions gives the inclusion–exclusion sum over all nonempty subsets S ⊆ {1,\dots,R} with alternating signs:
$$
\widehat{B}_{\text{CGM}} = \sum_{\emptyset \neq S \subseteq \{1,\dots,R\}} (-1)^{|S|+1} \widehat{B}_{\cap S},
\qquad
\widehat{\mathrm{Var}}_{\text{CGM}}(\hat\beta) = (X'X)^{-1}\, \widehat{B}_{\text{CGM}} \, (X'X)^{-1}.
$$

> [!note] Why intersections?
> A pair of observations that share both an A-cluster and a B-cluster contribute to within-cluster covariance twice in V_A + V_B; subtracting V_{A∩B} corrects this double counting.

---

## Edge cases and FAQs

- Singleton intersections
  - If some intersection groups (e.g., A∩B cells) have only one observation, they contribute zero to the meat for that scheme. That is fine; ensure software handles empty/small cells gracefully.

- Perfect nesting vs non-nesting
  - If B is nested within A (or vice versa), multiway reduces to the coarser clustering: intersections add nothing beyond the coarser scheme. Use the coarsest valid cluster dimension.

- High-dimensional fixed effects (FE)
  - Absorbing FE does not replace clustering. FE remove mean shifts but not serial/common-shock correlation in errors. Cluster on the relevant dimensions even with FE absorbed.

- Heteroskedasticity
  - CGM inherits heteroskedastic robustness from CRV estimators; no separate HC correction is needed.

- Nonlinear models
  - CGM is standard for linear M-estimators with asymptotic linearity. For nonlinear ML/GLM, use the same inclusion–exclusion logic on the sandwich “meat” built from scores, and robustify accordingly; check software support.

---

## Diagnostics and sanity checks

> [!check]
> - [ ] Report cluster counts for each dimension and their intersections (min/median/max cell sizes)  
> - [ ] Compare one-way vs CGM SEs; CGM SEs should be ≥ the largest one-way in many common settings  
> - [ ] Sensitivity to alternative clustering choices (e.g., add a third dimension if plausible)  
> - [ ] Few clusters? cross-check with [[wild cluster bootstrap]] p-values and [[few-cluster corrections]] (CR2/CR3)  
> - [ ] Influence of very large clusters: re-estimate excluding the largest cluster(s)  

> [!tip] Simulation-based validation
> - Block-bootstrap or wild cluster bootstrap that respects both clustering dimensions can validate inference when theory is borderline (unequal cluster sizes, modest G).

---

## Three-way clustering example (concept)

Suppose clusters along A, B, C. Then:
$$
\widehat{V}_{\text{CGM}} = \widehat{V}_A + \widehat{V}_B + \widehat{V}_C
- \widehat{V}_{A\cap B} - \widehat{V}_{A\cap C} - \widehat{V}_{B\cap C}
+ \widehat{V}_{A\cap B\cap C}.
$$

Pseudocode outline:
1) Fit the model; get residuals ŭ and X.  
2) Build grouping indices for A, B, C and for all intersections (A∩B, A∩C, B∩C, A∩B∩C).  
3) For each scheme C in {A, B, C, A∩B, A∩C, B∩C, A∩B∩C}: compute B_C = ∑_g X_g' ŭ_g ŭ_g' X_g, then V_C = (X'X)^{-1} B_C (X'X)^{-1}, optionally with finite-sample factor λ_C.  
4) Combine with signs (+, +, +, −, −, −, +).  

---

## Practical tips

- Intersections in software
  - Most packages construct intersections internally when you pass multiple cluster IDs. If not, create a composite factor (e.g., paste(idA, idB)).

- Degrees of freedom in tests
  - With large clusters, asymptotic normal/t approximations are fine. With few clusters, base t-tests on an effective df (e.g., min(G_A, G_B)−1) is ad hoc; prefer bootstrap-based p-values.

- Collinearity and dropped groups
  - If FE or data cleaning drop some clusters, re-check cluster counts and intersections; missing or empty groups can change df and scaling factors.

---

## Worked numeric micro-example (two-way)

Suppose four observations with clusters:
- A: \[a1, a1, a2, a2], B: \[b1, b2, b1, b2].
Intersections: \[a1∩b1, a1∩b2, a2∩b1, a2∩b2] — all singletons.

- Then V_{A∩B}=0 (singleton cells), so two-way CGM reduces to V_A + V_B.  
- This toy shows why intersections matter only when there is within-cell covariance (multiple obs per intersection).

---

## Related notes

- [[clustered standard errors]] for one-way clustering foundations  
- [[few-cluster corrections]] for small G  
- [[wild cluster bootstrap]] for inference with few or unbalanced clusters  
- [[Conley standard errors]] when correlation decays with distance rather than discrete clusters  
- [[Difference-in-Differences (DiD)]] and [[two-way fixed effects]] where CGM is commonly applied

---

## References

- Cameron, A. C., Gelbach, J. B., & Miller, D. L. (2011). Robust inference with multiway clustering. Journal of Business & Economic Statistics, 29(2), 238–249.  
- Cameron, A. C., Gelbach, J. B., & Miller, D. L. (2006). Robust inference with multi-way clustering. (Working paper).  
- Petersen, M. A. (2009). Estimating standard errors in finance panel data. Review of Financial Studies, 22(1), 435–480.  
- MacKinnon, J. G., & Webb, M. D. (2017, 2020). Wild bootstrap inference for few (multiway) clusters.  
- Roodman, MacKinnon, Nielsen, & Webb (2019). Fast and wild: Bootstrap inference in Stata using boottest.
