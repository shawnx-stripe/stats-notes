---
title: Region of Practical Equivalence (ROPE)
aliases: [Region of Practical Equivalence, rope, equivalence region, ROPE, region of practical equivalence]
tags: [bayesian, testing, decision-theory, equivalence, hdi, thresholds, ab-testing]
updated: 2025-09-25
---

# Region of Practical Equivalence (ROPE)

> [!summary] Quick definition
> ROPE (Region of Practical Equivalence) defines an interval around a null value (often 0) representing effects too small to matter in practice. In Bayesian testing, decisions are made by the posterior mass inside or outside the ROPE rather than by p-values. Common rule: accept practical equivalence if most posterior mass lies within the ROPE; declare a meaningful effect if most mass lies outside. See [[Bayesian Testing]].

- Examples:
  - Mean difference: θ = μ_B − μ_A with ROPE [−ε, +ε] for a minimal important difference ε.
  - Odds ratio: ROPE on log-scale [−ε_log, +ε_log] centered at 0 (OR=1).
  - Noninferiority: one-sided ROPE (e.g., θ > −ε).

---

## Decision rules

Let θ be the effect of interest and R = [L, U] the ROPE (usually symmetric: L=−ε, U=+ε).

- Posterior mass in ROPE:
$$
p_{\text{in}} \;=\; \Pr(\theta \in R \mid y).
$$
- Practical equivalence (accept H0):
$$
\text{Decide equivalence if } \; p_{\text{in}} \ge \tau_{\text{in}} \quad (\text{e.g., } 0.95).
$$
- Meaningful effect (reject equivalence):
$$
\text{Decide meaningful effect if } \; \Pr(\theta \notin R \mid y) \ge \tau_{\text{out}}.
$$
- Inconclusive otherwise.

> [!tip] HDI+ROPE rule of thumb
> - If the 95% HDI lies entirely inside the ROPE → accept practical equivalence.  
> - If the 95% HDI lies entirely outside the ROPE → declare a meaningful effect.  
> - If the 95% HDI overlaps the ROPE → inconclusive.  
> HDI is the highest-density credible interval.

---

## Choosing the ROPE

- Domain-anchored thresholds
  - Minimal clinically/ practically important difference (MCID/MID) from domain literature or stakeholder utility.
  - For AB tests, tie to business value: smallest lift that justifies deployment given costs and risks.
- Scale considerations
  - Differences: ε in outcome units (e.g., days, dollars).  
  - Standardized effects: ε in Cohen’s d (e.g., ±0.1).  
  - Ratios: specify on log scale (log-OR, log-RR) symmetrically around 0.
- One-sided goals
  - Noninferiority: ROPE is (−ε, ∞) or equivalently require Pr(θ > −ε | y) ≥ τ.  
  - Superiority with tolerance: require Pr(θ > ε | y) ≥ τ.

> [!warning]
> - Avoid post-hoc ROPE tuning based on the data. Pre-register ε and thresholds (τ_in/τ_out).  
> - Ensure ROPE is on the decision scale (e.g., absolute risk difference vs odds ratio).

---

## Worked examples

> [!example] Normal mean difference (conjugate)
> Suppose θ | y ∼ 𝓝(μ_n, σ_n²) and ROPE = [−ε, +ε]. Then:
> $$
> p_{\text{in}}
> \;=\; \Pr(-\varepsilon \le \theta \le \varepsilon \mid y)
> \;=\; \Phi\!\left(\frac{\varepsilon - \mu_n}{\sigma_n}\right)
> \;-\; \Phi\!\left(\frac{-\varepsilon - \mu_n}{\sigma_n}\right).
> $$
> Decide practical equivalence if p_in ≥ τ_in (e.g., 0.95).

> [!example] Difference in proportions (simulation)
> Let p_A ∼ Beta(α_A, β_A), p_B ∼ Beta(α_B, β_B), θ = p_B − p_A, ROPE = [−ε, +ε].
> 1) Draw S samples p_A^(s), p_B^(s).  
> 2) θ^(s) = p_B^(s) − p_A^(s).  
> 3) Estimate p_in = mean(−ε ≤ θ^(s) ≤ ε).  
> 4) Report HDI of θ and ROPE decision.

> [!example] Regression coefficient via MCMC
> Given posterior draws β_j^(s), set ROPE R_j around 0 in the predictor’s natural effect units (or standardized). Compute p_in = mean(β_j^(s) ∈ R_j), and apply the HDI+ROPE rule.

---

## Relationship to frequentist equivalence

- Equivalence testing (TOST): specify [−ε, +ε] and reject non-equivalence if both one-sided tests pass.  
- Bayesian ROPE and TOST both formalize practical equivalence; they answer similar decisions with different evidential summaries (posterior mass vs confidence bounds). Reporting both can help communicate across audiences.

---

## Sequential use and AB testing

- Bayesian monitoring permits continuous looks without alpha spending; still, pre-register ROPE and τ thresholds and simulate operating characteristics.  
- In product [[AB Testing (MOC)]], ROPE encodes “minimum launch-worthy lift.” Combine with guardrails and stop when either:
  - Pr(θ ∈ ROPE | y) ≥ τ_in (declare no meaningful impact), or
  - Pr(θ > ε | y) ≥ τ_sup (declare win), or
  - Pr(θ < −ε | y) ≥ τ_harm (declare harm).

---

## Reporting essentials

- Estimand and scale (difference, log-OR, relative change); ROPE bounds and justification
- Priors and computational method (closed form, [[Markov Chain Monte Carlo (MCMC)|MCMC]], [[Sequential Monte Carlo (SMC)|SMC]], approximation)
- Posterior summaries: mean, HDI/credible intervals, p_in, Pr(θ > ε), Pr(θ < −ε)
- Decision thresholds (τ_in/τ_out) and the resulting decision
- Sensitivity to ε and priors; pre-registration info where applicable

---

## Diagnostics and good practice

> [!check]
> - [ ] ROPE chosen from domain utility/MCID, not data-driven  
> - [ ] Scale and direction consistent with decision (two- vs one-sided)  
> - [ ] Posterior computation converged; HDI stable across chains/seeds  
> - [ ] Sensitivity to ε and priors documented  
> - [ ] For multiple endpoints, control discovery rates (Bayesian FDR) or clearly separate families (see [[multiple testing control]], [[False Discovery Rate (FDR)|FDR]])

---

## Pitfalls

> [!warning]
> - ROPE too wide → false “equivalence”; too narrow → indecision  
> - Using symmetric ROPE when only noninferiority matters  
> - Ignoring heterogeneity: small average effect can mask harmful subgroups; examine segments if relevant  
> - Mixing scales (e.g., declaring equivalence on OR when the decision uses risk difference)

---

## Related notes

- Foundations and decisions: [[Bayesian Testing]] · [[Hypothesis testing]]  
- Design and online decisions: [[AB Testing (MOC)]] · [[sequential testing]]  
- Multiplicity: [[False Discovery Rate (FDR)|FDR]] · [[multiple testing control]]

---

## References

- Kruschke, J. K. (2013, 2015). Doing Bayesian Data Analysis; ROPE and HDI decision framework.  
- Kruschke, J. K., & Liddell, T. M. (2018). The Bayesian new statistics.  
- Lakens, D. (2017). Equivalence tests: a practical primer (TOST, frequentist).  
- Schuirmann, D. J. (1987). A comparison of the two one-sided tests procedure and the power approach for equivalence testing.  
- Gelman, A. et al. (2013/2020). Bayesian Data Analysis (decision-theoretic framing and practical thresholds).