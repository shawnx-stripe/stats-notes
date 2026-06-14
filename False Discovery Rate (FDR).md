---
title: False Discovery Rate (FDR)
aliases: [FDR, false discovery rate, Benjamini–Hochberg, BH, Benjamini–Yekutieli, BY, q-value]
tags: [multiple-testing, inference, experimentation, ab-testing, sequential, diagnostics, econometrics, statistics]
updated: 2025-09-17
---

# False Discovery Rate (FDR)

> [!summary] Quick definition
> The False Discovery Rate (FDR) is the expected proportion of rejected nulls that are false discoveries:
> $$
> \mathrm{FDR} = \mathbb{E}\!\left[\frac{V}{R \vee 1}\right],
> $$
> where V = number of false rejections and R = total rejections. FDR-controlling procedures (e.g., Benjamini–Hochberg) provide more power than FWER controls (e.g., Bonferroni) while limiting the expected fraction of false positives among findings.

- Common use: many metrics in [[AB Testing (MOC)]], guardrail families, subgroup/heterogeneity screens, feature screens.
- Contrast: FWER (probability of ≥1 false positive) is stricter; FDR tolerates some false positives but controls their proportion.

---

## Core procedures

### Benjamini–Hochberg (BH) step-up (independence / PRDS)
- Input: p-values $p_1,\dots,p_m$, target FDR level α.
- Steps:
  1) Order p-values $p_{(1)} \le \cdots \le p_{(m)}$ with ranks i = 1..m.
  2) Find the largest
     $$
     k = \max\Big\{i: p_{(i)} \le \tfrac{i}{m}\alpha \Big\}.
     $$
  3) Reject all hypotheses with $p_{(i)} \le p_{(k)}$ (i ≤ k).
- Valid when p-values are independent or positively dependent (PRDS).

### Benjamini–Yekutieli (BY) (arbitrary dependence)
- Replace α by $\alpha / c(m)$ where $c(m)=\sum_{i=1}^m \frac{1}{i}\approx \log(m)+\gamma$.
- Steps otherwise same as BH; more conservative under dependence.

### q-values (Storey)
- q-value for $p_{(i)}$ estimates the minimal FDR at which $H_{(i)}$ would be called significant:
  $$
  q_{(i)} = \min_{j \ge i} \frac{m\,p_{(j)}}{j}, \quad \text{optionally using } \hat\pi_0 \text{ for adaptivity}.
  $$
- Report $q$ instead of p to convey FDR-adjusted evidence.

### Weighted / structured FDR (optional)
- Weighted BH: assign weights $w_i>0$ (sum to m), apply BH to $p_i/w_i$ (more power for prioritized hypotheses).
- Independent Hypothesis Weighting (IHW): data-driven weights from covariates (improves power under independence across folds).
- Hierarchical FDR: control FDR along a tree of hypotheses (families→children).

### Online FDR (sequential streams)
- Alpha-investing / LORD / SAFFRON control FDR as hypotheses arrive over time (useful for dashboards/continuous monitoring). See [[sequential testing]] for design-level control.

---

## Choosing an approach

- Independent/PRDS p-values: BH.
- Arbitrary or strong dependence (e.g., many correlated metrics): BY, or hierarchical/weighted methods if structure known.
- Many related metrics with covariates (e.g., baseline variance/volume): IHW/weighted BH.
- Streaming/continuous looks: online FDR (LORD/SAFFRON) or pre-planned group-sequential plus multiplicity.

---

## Applications

- Experiment guardrails: treat guardrails as a family; control FDR at α_g (e.g., 5%) while OEC uses its own threshold.
- Metric gardens: dozens of exploratory metrics post-launch; BH to flag candidates; validate key ones in follow-up tests.
- Event-study leads/lags: if many lead coefficients tested, consider FDR alongside joint tests (or predefine families).
- Subgroup/heterogeneity scans: FDR control across subgroup effects; follow-up confirmatory tests recommended.

---

## Code snippets

> [!example] R: BH/BY and q-values

```r
p <- c(0.001, 0.04, 0.02, 0.20, 0.005)
# Adjusted p-values
p_bh <- p.adjust(p, method = "BH")
p_by <- p.adjust(p, method = "BY")

# q-values (Storey)
# install.packages("qvalue")
library(qvalue)
q <- qvalue(p)$qvalues

data.frame(p, p_bh, p_by, q)
```

> [!example] Python: BH/BY via statsmodels

```python
import numpy as np
from statsmodels.stats.multitest import multipletests, fdrcorrection

p = np.array([0.001, 0.04, 0.02, 0.20, 0.005])

# BH / BY adjusted p-values
rej_bh, p_bh, _, _ = multipletests(p, alpha=0.05, method='fdr_bh')
rej_by, p_by, _, _ = multipletests(p, alpha=0.05, method='fdr_by')

# BH decision directly (or use fdrcorrection)
rej, p_bh2 = fdrcorrection(p, alpha=0.05)

print(p_bh, p_by, rej_bh)
```

> [!example] Stata: BH decisions (manual)

```stata
* p-values in variable p; alpha = 0.05
preserve
keep p
drop if missing(p)
gsort p
gen i = _n
sum i
scalar m = r(max)
gen crit = (i/m)*0.05
gen pass = p <= crit
egen k = max(cond(pass, i, .))
scalar k = k[1]
gen reject = i <= k  // 1 = reject under BH
restore
```

---

## Reporting essentials

- Family definition (which hypotheses/metrics included), target α, and procedure (BH/BY/weighted/hierarchical).
- Adjusted p-values or q-values; number of rejections R and estimated FDR (e.g., max q among rejections).
- Dependence structure assumption (independence/PRDS vs arbitrary) and justification.
- Any weighting/hierarchy and how weights/nodes were chosen.
- If sequential: method (e.g., LORD/SAFFRON), cadence, and linkage to [[sequential testing]].
- Sensitivity: results under BH vs BY; robustness to alternative families.

---

## Diagnostics and good practice

> [!check]
> - [ ] Define families a priori (e.g., guardrails vs exploratory metrics)  
> - [ ] Use BH for independent/PRDS p-values; BY or hierarchical FDR for strong dependence  
> - [ ] Prefer q-values for reporting; keep raw p-values available  
> - [ ] For streaming dashboards, adopt online FDR; avoid ad-hoc peeking  
> - [ ] Combine with effect sizes and CIs; don’t rely on significance alone  
> - [ ] Pre-register primary outcomes; use FDR mainly for secondary/exploratory sets

---

## Pitfalls

> [!warning]
> - Post-hoc reshaping families to obtain significance (p-hacking)  
> - Treating FDR control as effect-size evidence (it isn’t)  
> - Ignoring dependence; BH under severe dependence may under-control → use BY/hierarchical  
> - Mixing confirmatory (OEC) and exploratory (guardrails) under one FDR without rationale  
> - Continuous monitoring with BH applied repeatedly (inflates error) → use online FDR or sequential plans

---

## Copy-ready formulas

- BH critical line:
$$
\text{Reject } H_{(1)},\dots,H_{(k)},\quad k=\max\{i: p_{(i)}\le \tfrac{i}{m}\alpha\}.
$$

- BY adjustment:
$$
\alpha'=\frac{\alpha}{\sum_{i=1}^m 1/i},\quad \text{use BH with }\alpha'.
$$

- q-values (basic):
$$
q_{(i)} = \min_{j\ge i} \frac{m\,p_{(j)}}{j}\ \ (\text{optionally } \times\,\hat\pi_0).
$$

---

## Related notes

- [[sequential testing]] · [[guardrail metric]] · [[AA test]] · [[Sample Ratio Mismatch (SRM)|SRM]]
- [[AB Testing (MOC)]] · [[Experimental Design (MOC)]]
- [[policy learning]] · [[uplift]]
- [[Difference-in-Differences (DiD)]] (many leads/lags → multiplicity)  
- [[multiple testing control|multiple comparisons]] · [[Hierarchical False Discovery Rate (FDR)|hierarchical FDR]] · [[Independent Hypothesis Weighting (IHW)|IHW]]

---
