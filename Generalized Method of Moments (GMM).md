---
title: Generalized Method of Moments (GMM)
aliases: [GMM, generalized method of moments, Generalized Method of Moments, method of moments, GEL (related)]
tags: [econometrics, estimation, inference, moments, gmm, iv, hac, cluster, panels, dynamic-panel, overidentification]
updated: 2025-09-25
---

# Generalized Method of Moments (GMM)

> [!summary] Quick definition
> Generalized Method of Moments (GMM) estimates parameters by matching sample moments to population moment conditions. Given E[g(W, θ0)] = 0, GMM chooses θ to make sample moments close to zero using an optimal weighting matrix. Under standard conditions, GMM is consistent, asymptotically normal, and efficient among estimators using those moments. Overidentifying restrictions are tested with the Hansen J test.

- Core: moments, weighting matrix, sandwich variance, overidentification tests.
- Typical uses: [[Instrumental Variables (IV)]], dynamic panels (Arellano–Bond / Blundell–Bond), time series with heteroskedasticity/serial correlation.
- Related: [[Maximum Likelihood Estimation (MLE)|MLE]] (full likelihood alternative), [[weak instruments]], [[clustered standard errors]], [[Conley standard errors]], [[Time Series (MOC)]].

---

## Setup and notation

- Data: observations W_i, i=1,…,n (iid or weakly dependent).
- Moment conditions:
$$
\mathbb{E}\!\big[g(W_i;\,\theta_0)\big] = 0,
\qquad g:\mathcal{W}\times\Theta\to\mathbb{R}^m,
$$
with θ0 ∈ ℝ^p and m ≥ p (exactly identified if m=p; overidentified if m>p).
- Sample moments and Jacobian:
$$
\bar g_n(\theta) = \frac{1}{n}\sum_{i=1}^n g(W_i;\theta),
\qquad
G(\theta) = \frac{\partial}{\partial \theta'}\,\mathbb{E}\!\big[g(W_i;\theta)\big]\Big|_{\theta}.
$$

---

## Estimator

Given a positive definite weighting matrix W_n (m×m),
$$
\hat\theta
=\arg\min_{\theta\in\Theta}\; Q_n(\theta),
\qquad
Q_n(\theta) = \bar g_n(\theta)'\, W_n \,\bar g_n(\theta).
$$

- Exactly identified (m=p): θ̂ solves the sample moment equations, Q_n(θ̂)=0.
- Overidentified (m>p): θ̂ trades off moments via W_n.

---

## Asymptotics and inference

Under regularity and identification (rank G(θ0)=p):

- Asymptotic normality
$$
\sqrt{n}\,(\hat\theta - \theta_0)
\;\xrightarrow{d}\;
\mathcal{N}\!\Big(0,\; V\Big),
\quad
V = (G' W G)^{-1}\, G' W S W G \, (G' W G)^{-1},
$$
where G = G(θ0) and S = Var[\,\sqrt{n}\,\bar g_n(\theta_0)\,] (long-run covariance of the moments).

- Optimal weighting
$$
W^\star = S^{-1}
\quad\Rightarrow\quad
V^\star = (G' S^{-1} G)^{-1}.
$$

- Two-step GMM (practical)
  1) Preliminary θ̂₁ with W₁ (e.g., identity).  
  2) Estimate Ŝ at θ̂₁ (heteroskedastic/HAC/cluster-robust), set Ŵ = Ŝ^{-1}, re-estimate θ̂₂.  
  3) Inference: plug Ŝ at θ̂₂ into the sandwich variance above.

> [!note] Hansen J overidentification test (m>p)
> With Ŵ = Ŝ^{-1},
> $$
> J = n\, \bar g_n(\hat\theta)' \, Ŵ \, \bar g_n(\hat\theta)
> \;\xrightarrow{d}\;\chi^2_{\,m-p}
> $$
> under correct specification. Large J rejects joint validity of moments/instruments.

---

## Estimating S (covariance of moments)

- Heteroskedastic iid:
$$
\hat S = \frac{1}{n}\sum_{i=1}^n g_i g_i', \quad g_i = g(W_i;\hat\theta_1).
$$
- HAC (time series; Newey–West):
$$
\hat S = \Gamma_0 + \sum_{h=1}^{L} k\!\left(\frac{h}{L+1}\right)\,(\Gamma_h + \Gamma_h'),
\quad
\Gamma_h = \frac{1}{n}\sum_{t=1+h}^n g_t g_{t-h}'.
$$
- Clustering: sum cluster-level outer products of cluster moment sums; see [[clustered standard errors]].

---

## Identification and diagnostics

- Rank condition: G(θ0) full column rank p.
- Weak identification: flat Q_n(θ) → instability and large SEs; check curvature and sensitivity.
- Over-ID diagnostics: Hansen J; in IV settings, difference-in-Hansen tests for instrument subsets; avoid instrument proliferation.

---

## Linear IV as GMM (2SLS equivalence)

Moments with instruments Z (n×L), regressors X (n×p), outcome y:
$$
g_i(\beta) = z_i \,(y_i - x_i'\beta).
$$
One-step GMM with W = (Z'Z/n)^{-1} yields
$$
\hat\beta_{\text{2SLS}}
= (X' Z W Z' X)^{-1} X' Z W Z' y,
$$
equal to 2SLS. Efficient (heteroskedastic-robust) IV–GMM uses Ŵ=(Z'Ω̂Z/n)^{-1} with Ω̂=diag(û_i^2).

- J test = Sargan–Hansen overidentification test.
- Weak instruments: see [[weak instruments]].

---

## Nonlinear GMM and CUE

- Nonlinear moments: minimize Q_n(θ) with numerical optimization (BFGS, trust-region). Provide analytic gradients/Jacobians for stability.
- Continuously Updated GMM (CUE):
$$
Q^{\text{CUE}}_n(\theta) = \bar g_n(\theta)'\, \hat S(\theta)^{-1}\, \bar g_n(\theta),
$$
often better small-sample properties but heavier computation.

---

## Misspecification (quasi-GMM)

If no θ satisfies E[g(W,θ)]=0, θ̂ targets the pseudo-true θ* minimizing the population criterion. Inference still uses the sandwich with S and G at θ*. J tends to be large.

---

## Dynamic panel GMM (Arellano–Bond; Blundell–Bond)

Model with unit effects μ_i:
$$
y_{it} = \alpha\, y_{i,t-1} + x_{it}'\beta + \mu_i + \varepsilon_{it}.
$$
- Difference GMM (Arellano–Bond, 1991): difference to remove μ_i; instrument Δy_{i,t-1}, Δx with lagged levels assuming no serial correlation in ε_it.
- System GMM (Arellano–Bover/Blundell–Bond, 1995/1998): stack difference + level equations; add instruments for levels using lagged differences under stationarity-type conditions; helps with persistence/weak instruments.

Practical points:
- Instrument proliferation: collapse instruments, cap max lags.
- AR tests: AB AR(1) and AR(2) on differenced residuals.
- Two-step SEs: Windmeijer (2005) correction.
- Cluster by unit; few clusters → consider [[few-cluster corrections]] or [[wild cluster bootstrap]].

---

## Practical guidance

> [!check] Estimation workflow
> - [ ] Specify economically motivated moments; ensure exogeneity/pre-treatment instruments  
> - [ ] Step 1: θ̂₁ with simple W; Step 2: estimate Ŝ and re-estimate with Ŵ=Ŝ^{-1}  
> - [ ] Report robust SEs, J test, and, for IV, first-stage diagnostics  
> - [ ] Sensitivity: bandwidths/clustering, instrument subsets, CUE vs two-step  
> - [ ] Diagnostics: curvature of Q, stability across subsets/lags, AR(2) in panels
> - [ ] Scale variables; regularize ill-conditioned Ŵ; provide analytic Jacobians where possible

> [!warning]
> - Weak/invalid instruments → biased/unstable estimates; J may mislead with many instruments  
> - HAC choices (kernel/bandwidth) affect inference; justify and do sensitivity  
> - Failing to cluster in panels yields invalid SEs

---

## Minimal formulas and code

> [!example] Two-step IV–GMM (matrix form)
> 1) β̂₁ via 2SLS with
> $$
> W_1 \;=\; (Z^\top Z / n)^{-1}.
> $$
> 2) Define residuals and covariance:
> $$
> \hat u \;=\; y - X\hat\beta_1,\qquad
> \hat\Omega \;=\; \operatorname{diag}(\hat u \odot \hat u),\qquad
> \hat S \;=\; \frac{1}{n}\, Z^\top \hat\Omega\, Z.
> $$
> 3) Update weighting and re-estimate:
> $$
> \hat W \;=\; \hat S^{-1},\qquad
> \hat\beta_2 \;=\; (X^\top Z \hat W Z^\top X)^{-1} X^\top Z \hat W Z^\top y.
> $$
> 4) Sandwich variance:
> $$
> \hat V \;=\; (X^\top Z \hat W Z^\top X)^{-1}\, X^\top Z \hat W \hat S \hat W Z^\top X \,(X^\top Z \hat W Z^\top X)^{-1}.
> $$
> 5) Hansen J statistic:
> $$
> J \;=\; \frac{(y - X\hat\beta_2)^\top Z \hat W Z^\top (y - X\hat\beta_2)}{n}.
> $$



> [!example] Nonlinear GMM (pseudocode)
> ```
> choose θ0
> repeat:
>   compute g_i(θ), ḡ(θ), optionally G(θ)
>   if step 1: W = I; else: W = Ŝ(θ_prev)^{-1}
>   θ ← argmin ḡ(θ)' W ḡ(θ)  # BFGS/Trust-Region
> until convergence
> compute robust V̂ using Ŝ at θ̂
> ```

---

## Alternatives and relatives

- GEL (Generalized Empirical Likelihood): empirical likelihood (EL), exponential tilting (ET), ETEL; moment-based with likelihood-ratio style inference, often improved small-sample properties.
- CUE vs two-step GMM: CUE can reduce small-sample bias/variance at higher computational cost.
- SMM/Indirect inference: simulation-based analogs when moments depend on simulated outputs.
- LIML/K-class (IV): alternatives to 2SLS under weak instruments; LIML connects to GMM with special weighting.
- GEE: generalized estimating equations for correlated outcomes; akin to GMM on quasi-scores.
- Optimal instruments (Chamberlain): for conditional moments, using instruments equal to conditional expectations can attain semiparametric efficiency.

---

## Software

- Stata
  - ivreg2, gmm (nonlinear GMM), xtabond/xtabond2 (AB/BB panels), estat overid, estat firststage, Windmeijer small option.
- R
  - AER::ivreg, ivreg::ivreg (2SLS; combine with sandwich/clubSandwich)  
  - gmm (linear/nonlinear), plm::pgmm (dynamic panels), systemfit  
  - sandwich, clubSandwich (CR2/CR3), lmtest
- Python
  - linearmodels: IV2SLS, IVGMM, IVGMMCUE, Panel GMM (Arellano–Bond/Blundell–Bond)  
  - statsmodels: GMM classes; HAC/cluster covariances
- Julia
  - GMM.jl; FixedEffectModels.jl (IV); paneltools

---

## Examples

> [!example] R: IV–GMM with robust SEs
> ```r
> library(AER); library(sandwich); library(lmtest)
> fit <- ivreg(y ~ x1 + x2 | z1 + z2, data = df)
> vc <- vcovCL(fit, cluster = ~ id)  # or vcovHC/clubSandwich
> coeftest(fit, vcov = vc)
> ```

> [!example] Python: IVGMM (linearmodels)
> ```python
> from linearmodels.iv import IVGMM
> y = df['y']; X = df[['x1','x2']]; Z = df[['z1','z2']]
> res = IVGMM(y, X, Z).fit(iter_limit=2)  # two-step
> print(res.summary)
> ```

> [!example] Stata: System GMM
> ```
> xtabond2 y L.y x1 x2, gmm(L.y, collapse lag(2 .)) iv(x1 x2) ///
>          twostep robust small
> estat sargan
> estat abond
> ```

---

## Reporting essentials

- Moment conditions and economic justification; instrument sets and lag strategy
- Weighting scheme: one-step vs two-step vs CUE; how Ŝ was estimated (HC/HAC/cluster) and tuning choices
- Estimates with robust SEs and 95% CIs; Hansen J (df=m−p) and p-value
- For IV: first-stage stats (F, partial R²), weak-IV diagnostics; subset J tests
- For dynamic panels: instrument counts (total/collapsed), AR(1)/AR(2) p-values, Hansen/Sargan tests, Windmeijer correction
- Sensitivity analyses: alternative instruments, bandwidths, clustering, and specifications
- Reproducibility: data filters, software versions, seeds, and code

---

## Common pitfalls

> [!warning]
> - Treating large J p-values as proof of instrument strength/validity; J often has low power with many instruments  
> - Ignoring weak instruments; normal approximations can fail badly  
> - Overly many instruments in panel GMM → overfitting endogenous variables and weak J  
> - HAC bandwidth/kernel choices left unjustified; results can be sensitive  
> - Failing to cluster in panels or using post-treatment instruments (see [[leakage]])

---

## Related notes

- Identification and IV: [[Instrumental Variables (IV)]] · [[weak instruments]] · [[Local Average Treatment Effect (LATE)|LATE]]  
- Inference: [[clustered standard errors]] · [[Conley standard errors]] · [[Hypothesis testing]]  
- Modeling/design: [[Time Series (MOC)]] · [[Maximum Likelihood Estimation (MLE)|MLE]] · [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]] · [[double machine learning]]

---

## References

- Hansen, L. P. (1982). Large sample properties of GMM estimators. Econometrica.  
- Newey, W. K., & McFadden, D. (1994). Large sample estimation and hypothesis testing. In Handbook of Econometrics, Vol. 4.  
- Newey, W. K., & West, K. D. (1987). A simple, positive semi-definite HAC estimator. Econometrica.  
- Hall, A. R. (2005). Generalized Method of Moments. Oxford University Press.  
- Hansen, L. P., & Singleton, K. J. (1982). Generalized instrumental variables estimation of nonlinear rational expectations models. Econometrica.  
- Hansen, L. P., Heaton, J., & Yaron, A. (1996). Finite-sample properties of some alternative GMM estimators. Journal of Business & Economic Statistics.  
- Arellano, M., & Bond, S. (1991). Some tests of specification for panel data: Monte Carlo evidence and an application to employment equations. Review of Economic Studies.  
- Arellano, M., & Bover, O. (1995). Another look at instrumental variable estimation of error-components models. Journal of Econometrics.  
- Blundell, R., & Bond, S. (1998). Initial conditions and moment restrictions in dynamic panel data models. Journal of Econometrics.  
- Windmeijer, F. (2005). A finite sample correction for the variance of linear efficient two-step GMM estimators. Journal of Econometrics.  
- Stock, J. H., & Yogo, M. (2005). Testing for weak instruments in linear IV regression. In Identification and Inference for Econometric Models (Cambridge University Press).  
- Hansen, L. P., Heaton, J., & Ogaki, M. (1996). Efficiency bounds implied by conditional moment restrictions. Journal of the American Statistical Association.  
- Newey, W. K., & Smith, R. J. (2004). Higher order properties of GMM and generalized empirical likelihood estimators. Econometrica.  
- Kitamura, Y., & Stutzer, M. (1997). An information-theoretic alternative to generalized method of moments estimation. Econometrica.  
- Sargan, J. D. (1958). The estimation of economic relationships using instrumental variables. Econometrica.  
- Hayashi, F. (2000). Econometrics. Princeton University Press (GMM chapters).  
- Wooldridge, J. M. (2010). Econometric Analysis of Cross Section and Panel Data (2nd ed.). MIT Press (GMM and panel GMM). 