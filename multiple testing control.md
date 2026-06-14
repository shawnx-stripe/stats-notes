---
title: multiple testing control
aliases: [multiple comparisons, multiplicity, familywise error rate, FWER, q-values, stepdown, online FDR]
tags: [experimentation, statistics, inference, multiple-testing, fdr, fwer, sequential, ab-testing, econometrics]
updated: 2025-09-17
---

# multiple testing control

> [!summary] Quick definition
> Multiple testing control manages Type I error inflation when testing many hypotheses. Common goals:
> - Control the familywise error rate (FWER): P(≥1 false positive) ≤ α (e.g., Bonferroni/Holm)
> - Control the false discovery rate (FDR): E[V/(R∨1)] ≤ q (e.g., BH/BY, q-values)
> Variants handle dependence, hierarchical structures, weights, and streaming (online) testing.

- Use cases: many metrics/guardrails in [[AB Testing (MOC)]], subgroup scans, multiple variants/factors, event-study leads/lags, model selection.

---

## Key quantities and goals

- m: number of hypotheses/tests, with ordered p-values p_(1) ≤ … ≤ p_(m).
- R: total rejections; V: false rejections; S: true rejections; m0: number of true nulls.
- FWER = P(V ≥ 1).
- FDR = E[V/(R∨1)].

> [!tip] Which to use?
> - Confirmatory, critical safety: FWER (Bonferroni/Holm).
> - Exploratory screens and metric gardens: FDR (BH/BY/q-values/weighted).
> - Structured families (primary vs secondary): mix approaches; preregister families and procedures.

See: [[False Discovery Rate (FDR)|FDR]] for details on BH/BY and q-values.

---

## Core procedures (copy-ready)

### Familywise error rate (FWER)
- Bonferroni (simple, conservative):
  - Reject H_i if p_i ≤ α/m.
- Holm step-down (uniformly more powerful than Bonferroni):
  1) Order p_(1)…p_(m).
  2) Find smallest k with p_(k) > α/(m−k+1); reject all i < k.
  3) Else reject all (strong control, any dependence).
- Hochberg step-up (requires independence/PRDS):
  1) Order p_(1)…p_(m).
  2) Find largest k with p_(k) ≤ α/(m−k+1); reject all i ≤ k.

### False discovery rate (FDR)
- Benjamini–Hochberg (BH; independence/PRDS):
  - Find largest k with p_(k) ≤ (k/m)·α; reject all i ≤ k.
- Benjamini–Yekutieli (BY; arbitrary dependence):
  - Replace α by α/c(m) where c(m)=∑_{i=1}^m 1/i; apply BH with α' = α/c(m) (more conservative).
- q-values (Storey):
  - q_(i) = min_{j≥i} (m·p_(j)/j), optionally scaled by π̂0; report q instead of p.

### Stepdown/Westfall–Young (resampling)
- Permutation/bootstrap-based stepdown maxT procedures controlling FWER under dependence by resampling the joint null distribution (useful with correlated metrics; computational).

### Weighted and hierarchical control
- Weighted BH/Holm: assign weights w_i > 0 (∑w_i = m); apply procedure to p_i / w_i (prioritize important metrics).
- Independent Hypothesis Weighting (IHW): data-driven covariate-based weights to increase power (independence across folds).
- Hierarchical FDR (tree of families): control at parent before testing children (gatekeeping) or use hierarchical BH/IHW variants.

### Online/streaming control (sequential)
- Alpha-investing / LORD / SAFFRON:
  - Control (online) FDR as tests arrive; allocate/earn back α-wealth over time.
- Group-sequential (different goal): controls Type I across interim looks for a fixed set; see [[sequential testing]].

---

## Structuring the problem (families)

- Define families of hypotheses a priori (e.g., guardrails family, OEC family, heterogeneity family, event-study family).
- Control multiplicity within each family; avoid mixing unrelated families unless justified.
- Primary vs secondary:
  - Primary outcomes: prespecified; strict control (FWER or unadjusted if single).
  - Secondary: control FDR or FWER as appropriate; label exploratory.

> [!warning] Do not define families after seeing results; preregister (see [[pre-registration]]).

---

## Dependence and correlation

- Positively dependent (PRDS) p-values: BH valid.
- Arbitrary/strong dependence: BY, resampling (Westfall–Young), or hierarchical/weighted strategies.
- Spatial/temporal or clustered dependence: consider resampling schemes that respect structure (block bootstrap, permutation within blocks), or test joint patterns (e.g., event-study joint tests) with FWER/FDR for families.

---

## Event studies and panels

- Many coefficients (leads/lags). Good practice:
  - Use joint tests of all pre-treatment leads = 0 (Omnibus).
  - If making individual claims, control FDR (BH on lead set) or FWER (Holm), and report effect sizes with CIs.
  - For staggered designs, use valid estimators ([[Sun–Abraham estimator]] / [[Callaway–Sant’Anna estimator]]) and then apply multiplicity within the families reported.

---

## AB testing and guardrails

- OEC (primary) usually single, prespecified test (no multiplicity or gatekeeping).
- Guardrail metrics: define as a family; use FDR (e.g., 5%) or FWER if high stakes; use non-inferiority/equivalence tests with margins; adjust p or margins accordingly; track sequential looks via online FDR or alpha-spending.

---

## Code snippets

> [!example] R: FDR/FWER adjustments

```r
p <- c(0.001, 0.02, 0.20, 0.04, 0.005)

# FDR: BH and BY
p_bh <- p.adjust(p, method = "BH")
p_by <- p.adjust(p, method = "BY")

# FWER: Bonferroni and Holm
p_bonf <- p.adjust(p, method = "bonferroni")
p_holm <- p.adjust(p, method = "holm")

# q-values (Storey)
# install.packages("qvalue")
library(qvalue)
q <- qvalue(p)$qvalues

data.frame(p, p_bh, p_by, p_bonf, p_holm, q)
```

> [!example] Python: FDR/FWER (statsmodels)

```python
import numpy as np
from statsmodels.stats.multitest import multipletests, fdrcorrection

p = np.array([0.001, 0.02, 0.20, 0.04, 0.005])

# BH FDR
rej_bh, p_bh, _, _ = multipletests(p, alpha=0.05, method='fdr_bh')
# BY FDR
rej_by, p_by, _, _ = multipletests(p, alpha=0.05, method='fdr_by')
# Holm FWER
rej_holm, p_holm, _, _ = multipletests(p, alpha=0.05, method='holm')
# Bonferroni FWER
rej_bonf, p_bonf, _, _ = multipletests(p, alpha=0.05, method='bonferroni')
```

> [!example] Stata: Holm/Hochberg (built-in) and Romano–Wolf (user-written)

```stata
* Holm step-down after regressions
reg y x1
reg y x2
reg y x3
pv, from(1) using(my_pvals)  // Or collect p-values manually

* Built-in commands
* multproc: built-in multiple testing procedures (Stata 17+)
multproc bonferroni p1 p2 p3, alpha(0.05)
multproc holm p1 p2 p3, alpha(0.05)

* Romano–Wolf stepdown (rwolf; user-written)
* ssc install rwolf
rwolf (y x1) (y x2) (y x3), reps(5000) cluster(clusterid)
```

> [!example] R: IHW (covariate-weighted FDR)

```r
# install.packages("IHW")
library(IHW)
# p: p-values; covariate: e.g., baseline variance or count (independent of test under null)
ihw_res <- ihw(p ~ covariate, alpha = 0.05)
rejected <- rejections(ihw_res)
adj_p <- adj_pvalues(ihw_res)
```

> [!example] Online FDR (concept; Python packages vary)
- Use `onlineFDR` (R) or implement LORD/SAFFRON according to literature when p-values arrive sequentially.

---

## Workflow and governance

> [!check] Recommended steps
> - [ ] Define families and primary vs secondary outcomes in [[pre-registration]]  
> - [ ] Choose control target (FWER vs FDR), justify dependence assumptions  
> - [ ] Set α/q per family; pick procedure (Holm/BH/BY/weighted/hierarchical/online)  
> - [ ] If streaming looks: use online FDR or group-sequential alpha spending ([[sequential testing]])  
> - [ ] Apply within-family adjustments; report adjusted p or q-values and decisions  
> - [ ] Provide effect sizes and CIs; avoid “significance-only” reporting  
> - [ ] Archive raw p-values and adjusted results; document deviations

---

## Diagnostics and good practice

> [!check]
> - [ ] Check correlation/dependence structure (heatmaps of test statistics)  
> - [ ] Sensitivity: BH vs BY; Holm vs Bonferroni; weighted vs unweighted  
> - [ ] Hierarchical control when natural groupings exist (e.g., domains → sub-metrics)  
> - [ ] For event studies, joint tests + FDR on selected families  
> - [ ] Avoid fishing: prespecify; if exploratory, label clearly and replicate

---

## Common pitfalls

> [!warning]
> - Post-hoc family definition and cherry-picking  
> - Ignoring dependence (using BH where BY/resampling is required)  
> - Mixing confirmatory and exploratory metrics under one adjustment without rationale  
> - Applying BH repeatedly over time (dashboard peeking) → use online FDR  
> - Reporting only adjusted p-values without effect sizes and CIs  
> - Forgetting multiplicity across interim looks (needs sequential control)

---

## Reporting essentials

- Families and counts (m), α/q per family, procedure(s) used (Holm/BH/BY/weighted/hierarchical/online)
- Dependence assumptions and any diagnostics
- Adjusted p-values or q-values; number of rejections R; if FDR, expected FDP
- Effect sizes and CIs for all key findings (not just significance)
- Any sensitivity analyses (alternative procedures; family definitions)
- Software and versions (reproducibility)

---

## Related notes

- [[False Discovery Rate (FDR)|FDR]] · [[sequential testing]] · [[pre-registration]]  
- [[guardrail metric]] · [[AA test]] · [[Sample Ratio Mismatch (SRM)|SRM]]  
- [[Experimental Design (MOC)]] · [[AB Testing (MOC)]]  
- [[event study]] · [[Difference-in-Differences (DiD)]]

---
