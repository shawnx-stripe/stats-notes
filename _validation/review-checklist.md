---
title: Review Checklist
updated: 2026-04-02
---

# Vault Review Checklist

Tracking issues found during the 2026-03-03 and 2026-04-02 vault reviews.

---

## A. Math/Code Errors

- [x] **CUPED.md:81** — Multivariate CUPED formula used no-intercept OLS `(X'X)^{-1}X'Y`; fixed to sample covariance form `Σ_XX^{-1}Σ_XY`
- [x] **CUPED.md:192** — R code used `lm(Y ~ 0 + X1 + X2 + X3)`; fixed to `lm(Y ~ X1 + X2 + X3)` with `[-1]` to extract slopes only
- [x] **CUPAC.md:116** — Same no-intercept issue; fixed R code to use intercept model with `[-1]`
- [x] **CUPAC.md:163** — Stata code used `noconstant`; fixed to include constant

## B. Formatting Issues

- [x] **bootstrap.md:61-62** — Table used `$\[...\]$` (escaped display-math delimiters inside inline math); fixed to `$[...]$`

## C. Structural / Link Issues

- [x] **Causal Inference (MOC).md:214** — Self-referential link `[[Causal Inference (MOC)]]` in Related hubs; removed
- [x] **Causal Inference (MOC).md** — `[[wild cluster bootstrap]] (placeholder)` labels removed (file exists)
- [x] **Causal Inference (MOC).md** — `two-stage least squares (2SLS) (placeholder)` label removed (file exists)
- [x] **Causal Inference (MOC).md** — `[[weak instruments]] (placeholder)` label removed (file exists)
- [x] **Causal Inference (MOC).md** — `[[Conley standard errors]] (placeholder)` label removed (file exists)
- [x] **Causal Inference (MOC).md** — `[[Moulton problem]] (placeholder)` label removed
- [x] **Causal Inference (MOC).md:154** — `Anderson–Rubin (placeholder)` changed to proper wikilink `[[Anderson–Rubin]]`
- [x] **Two-Stage Least Squares (2SLS).md** — Added alias `two-stage least squares (2SLS)` so that wikilink spelling resolves

## D. Stub Notes Created

- [x] `Goodman–Bacon decomposition.md` — stub created (tags: causal-inference, did, diagnostics)
- [x] `Borusyak–Jaravel–Spiess (imputation).md` — stub created (tags: causal-inference, did, panel-data)
- [x] `Gardner DID2S.md` — stub created (tags: causal-inference, did, panel-data)
- [x] `boundary discontinuity.md` — stub created (tags: causal-inference, rdd, spatial)
- [x] `LIML.md` — stub created (tags: econometrics, iv, estimation)
- [x] `Anderson–Rubin.md` — stub created (tags: econometrics, iv, inference)

## E. Infrastructure Created

- [x] `.gitignore` — excludes .DS_Store, .obsidian workspace files, .trash
- [x] `CLAUDE.md` — repo-level instructions for note conventions
- [x] `_validation/review-checklist.md` — this file
- [x] `_validation/broken-links.md` — broken link audit
- [x] `.claude/commands/new-note.md` — slash command for note creation
- [x] `.claude/commands/check-links.md` — slash command for link checking

---

## F. 2026-04-02 Link Cleanup

- [x] Added missing note stubs: `Central Limit Theorem.md`, `Law of Large Numbers.md`, `Moran’s I.md`, `Hierarchical False Discovery Rate (FDR).md`, `Independent Hypothesis Weighting (IHW).md`, `fairness.md`, `profile likelihood.md`, `cutoff.md`, `variance estimation.md`, `Missing Not At Random (MNAR).md`, `aliasing.md`, `Coarsened Exact Matching (CEM).md`, `measurement error.md`, `Oster’s delta.md`, `de Chaisemartin–D’Haultfœuille.md`
- [x] Removed stale `(placeholder)` suffixes from live links in `Maximum Likelihood Estimation (MLE).md`, `Bayesian Testing.md`, `Econometrics (MOC).md`, `Experimental Design (MOC).md`, `False Discovery Rate (FDR).md`, `Hidden Markov Model (HMM).md`, `ML for Econometrics (MOC).md`, `Sequential Monte Carlo (SMC).md`, `Structural models.md`, `factorial design.md`, and `power analysis.md`
- [x] Final narrowed wikilink audit: `0` live unresolved links, `0` live ambiguous links, `0` stale placeholder labels

## Known Remaining Items (not bugs, intentional stubs)

These wikilinks appear in notes' `Related notes to create` sections and are intentional future stubs. They do not need immediate action and are excluded from the live-link audit:

- Reading list entries: `[[Angrist and Pischke]]`, `[[Imbens and Rubin]]`, `[[Hernán and Robins]]`, `[[Cunningham (Mixtape)]]`
- Bootstrap-related: `jackknife`, `permutation test`, `cross-validation`, `resampling methods`, `BCa bootstrap`, `block bootstrap`, etc.
- 2SLS-related: `k-class estimator`, `JIVE`, `Cragg-Donald statistic`, `Sargan test`, `Hansen J test`, etc.
- TWFE-related: `within transformation`, `demeaning`
- See `_validation/broken-links.md` for the full list.
