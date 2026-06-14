---
title: Overall Evaluation Criterion (OEC)
aliases: [OEC, Overall Evaluation Criterion, overall evaluation criterion, overall evaluation metric, north-star metric]
tags: [experimentation, ab-testing, metrics, evaluation, decision-making, composite-metric, business-value]
updated: 2025-09-17
---

# Overall Evaluation Criterion (OEC)

> [!summary] Quick definition
> The Overall Evaluation Criterion (OEC) is the pre-specified primary metric used to judge an experiment’s success. It should reflect long-run user and business value while being measurable over the experiment horizon. The OEC can be a single outcome or a composite of multiple components with clear weights and units.

- In experiments, the OEC drives the go/no-go decision; [[guardrail metric]]s gate safety and reliability but do not replace the OEC.
- A good OEC is aligned (correlates with long-term value), sensitive (detects meaningful change), robust (not easily gamed), and feasible (measurable with adequate power).

---

## Role vs. guardrails and secondary metrics

- OEC: primary objective to optimize (e.g., long-run engagement, revenue/user net of costs, retention).
- Guardrails: safety constraints (latency, errors, churn, fairness) with pass/fail rules (often non-inferiority); see [[guardrail metric]].
- Secondary/exploratory metrics: diagnostics and insights; control multiplicity with [[False Discovery Rate (FDR)|FDR]] if inferential claims are made.

---

## Designing an OEC

> [!check] Properties
> - Alignment: correlates with long-run outcomes (e.g., retention, LTV).
> - Sensitivity and power: sufficient variance and signal over planned duration (see [[power analysis]], [[Minimum Detectable Effect (MDE)|MDE]]).
> - Robustness: hard to game; stable across seasons/cohorts; monotone with value.
> - Feasibility: reliably logged ([[exposure logging]]), consistent unit of analysis, adequate sample size.

### Forms

- Single outcome (e.g., revenue/user 7-day, retained at day-30).
- Composite/utility:
$$
\text{OEC} = \sum_{k=1}^K w_k\, f_k,
$$
with components f_k in commensurate units (or normalized), weights w_k reflecting business value.
- Utility net of cost:
$$
\text{OEC} = \text{Benefit} - \lambda \cdot \text{Cost},
$$
e.g., revenue − λ·(compute, inventory, ad spend).

### Normalization and scaling

- Standardize components for stability and comparability:
  - Z-score: $f_k^\star = (f_k - \mu_k)/\sigma_k$ (use pre-period/control baselines).
  - Percent change: relative to baseline $\mu_k$.
  - Winsorization/trimmed means for heavy tails (with pre-registration).

### Windows and attribution

- Define time window (e.g., 7d/14d/28d), timezone, and inclusion rules.
- Attribution for multi-touch outcomes: first-touch/last-touch or fractional; pre-register the rule.

### Unit of analysis

- Align with randomization (user, session, device, geo, time-block); if misaligned, use [[clustered standard errors]] and cluster-aware aggregation.

---

## Composite OEC examples

- Engagement composite:
$$
\text{OEC} = 0.6\cdot \text{Sess/User} + 0.4\cdot \text{Time/User}
$$
- Profit proxy:
$$
\text{OEC} = \text{Rev/User} - \lambda_1 \cdot \text{Refunds/User} - \lambda_2 \cdot \text{InfraCost/User}.
$$
- Marketplace balance (two-sided):
$$
\text{OEC} = w_D \cdot \text{DemandFill} + w_S \cdot \text{SupplyUtilization} - w_W \cdot \text{WaitTime}.
$$

> [!warning] Weight setting
> Calibrate weights via backtests to long-run value (e.g., retention/LTV), managerial preference curves, or KKT-style tradeoffs; document rationale and sensitivity.

---

## Goodhart-proofing and governance

- Audit for manipulability (e.g., clicks vs satisfaction); use countervailing terms (e.g., dwell-adjusted clicks).
- Periodically revalidate correlation with long-run outcomes (holdout geos/cohorts).
- Freeze OEC definition per release cycle; changes via [[pre-registration]] with versioning.

---

## Estimation and inference

- Difference-in-means or [[Analysis of Covariance (ANCOVA)|ANCOVA]]/[[Controlled Experiments Using Pre-Experiment Data (CUPED)|CUPED]] on OEC (strictly pre-exposure baselines).
- Use robust/[[clustered standard errors]] (cluster by randomization unit; apply [[few-cluster corrections]] if needed).
- Ratio OECs (e.g., revenue/user): consider log transform or delta-method variance; pre-register handling of zeros/heavy tails.
- Sequential looks: follow [[sequential testing]] (alpha spending or always-valid p-values).

---

## Diagnostics

> [!check]
> - [ ] [[AA test]] pass; no [[Sample Ratio Mismatch (SRM)|SRM]] at assignment/eligibility/exposure/analysis  
> - [ ] Seasonality coverage and stability across cohorts ([[seasonality]])  
> - [ ] Sensitivity to windows (±1 week), outliers (winsor/trim), and attribution rules  
> - [ ] Correlation with long-term KPIs (backtest)  
> - [ ] Fairness: group-wise OEC changes; ensure no harmful subgroup effects if constrained

---

## Minimal code snippets

> [!example] R: Composite OEC and robust inference

```r
library(sandwich); library(lmtest)

# Define components and weights
w <- c(sess=0.6, time=0.4)
df$OEC <- with(df, w["sess"]*sessions_per_user + w["time"]*time_per_user)

# ANCOVA with CUPED baseline (preOEC)
fit <- lm(OEC ~ D + preOEC, data = df)
coeftest(fit, vcov = vcovHC(fit, type="HC1"))
```

> [!example] Python: Delta method for ratio OEC

```python
import numpy as np
import statsmodels.api as sm

# OEC = Revenue/User
rev_t = df.loc[df.D==1, 'revenue'].mean()
usr_t = df.loc[df.D==1, 'users'].mean()
rev_c = df.loc[df.D==0, 'revenue'].mean()
usr_c = df.loc[df.D==0, 'users'].mean()

R_t = rev_t / usr_t
R_c = rev_c / usr_c
diff = R_t - R_c

# Delta-method SE via linearization (sketch; better: bootstrap)
# Var(rev/usr) ≈ (1/usr^2)Var(rev) - 2*rev/usr^3 Cov(rev,usr) + (rev^2/usr^4)Var(usr)
```

> [!example] SQL: OEC aggregation per user

```sql
SELECT user_id,
       SUM(revenue) AS rev_user,
       SUM(session_time) AS time_user,
       COUNT(DISTINCT session_id) AS sess_user
FROM events
WHERE ts BETWEEN :start AND :end
GROUP BY 1;
```

---

## Common pitfalls

> [!warning]
> - OEC not aligned with long-run value (optimize clicks; harm retention)  
> - Post-treatment leakage in baselines ([[leakage]])  
> - Unstable ratio/quantile OECs without robust handling  
> - Ignoring clustering/serial correlation (switchback/geo)  
> - Changing OEC definition mid-run or post hoc  
> - Overweighting easy-to-move but low-value components

---

## Reporting essentials

- Exact OEC formula, weights, units, windows, and attribution
- Unit of analysis and clustering level; variance method
- CUPED/CUPAC details (baseline windows, θ training sample, R²)
- Main effect with CI; sequential/multiplicity controls applied
- Diagnostics and robustness (windows, outliers, subgroups)
- Guardrails outcomes and decision rationale

---

## Related notes

- [[AB Testing (MOC)]] · [[Experimental Design (MOC)]]
- [[guardrail metric]] · [[AA test]] · [[Sample Ratio Mismatch (SRM)|SRM]] · [[pre-registration]]
- [[Controlled Experiments Using Pre-Experiment Data (CUPED)|CUPED]] · [[Controlled Experiments Using Pre-Experiment Covariates (CUPAC)|CUPAC]] · [[Analysis of Covariance (ANCOVA)|ANCOVA]] · [[power analysis]] · [[Minimum Detectable Effect (MDE)|MDE]]
- [[sequential testing]] · [[seasonality]] · [[clustered standard errors]] · [[few-cluster corrections]]
- [[policy learning]] · [[uplift]] · [[leakage]]

---