---
title: Kalman filter
aliases: [KF, Kalman Filter, linear Gaussian state-space model, LDS, Kalman smoother, RTS smoother]
tags: [time-series, state-space, filtering, smoothing, estimation, inference, em, control]
updated: 2025-09-21
---

# Kalman filter

> [!summary] Quick definition
> The Kalman filter provides optimal recursive estimation of latent states in linear, Gaussian state-space models. It yields filtered and predicted state estimates, their covariances, innovations, and the log-likelihood. The Rauch–Tung–Striebel (RTS) smoother refines estimates using all data. See also [[Hidden Markov Model (HMM)|HMM]] (discrete states) and [[Sequential Monte Carlo (SMC)|SMC]] (nonlinear/non-Gaussian generalization).

- Use cases: tracking, signal extraction, forecasting, sensor fusion, econometric unobserved-components models.
- Related: [[Maximum Likelihood Estimation (MLE)|MLE]] via Kalman likelihood; EM for parameter learning; extensions (EKF/UKF/EnKF) for nonlinear models; SLDS links HMM and LDS.

---

## Linear Gaussian state-space model

With optional control inputs u_t:
$$
\begin{aligned}
x_t &= F_t x_{t-1} + B_t u_t + w_t,\quad &&w_t \sim \mathcal{N}(0, Q_t), \\
y_t &= H_t x_t \;\; + D_t u_t + v_t,\quad &&v_t \sim \mathcal{N}(0, R_t),
\end{aligned}
$$
where x_t ∈ R^n, y_t ∈ R^m. Matrices may be time-varying. Initialization: x_{0|0} and P_{0|0}.

---

## Kalman filter (predict–update)

Predict:
$$
\begin{aligned}
\hat x_{t|t-1} &= F_t \hat x_{t-1|t-1} + B_t u_t, \\
P_{t|t-1} &= F_t P_{t-1|t-1} F_t' + Q_t.
\end{aligned}
$$

Innovation and gain:
$$
\begin{aligned}
\tilde y_t &= y_t - H_t \hat x_{t|t-1} - D_t u_t, \\
S_t &= H_t P_{t|t-1} H_t' + R_t, \\
K_t &= P_{t|t-1} H_t' S_t^{-1}.
\end{aligned}
$$

Update:
$$
\begin{aligned}
\hat x_{t|t} &= \hat x_{t|t-1} + K_t \tilde y_t, \\
P_{t|t} &= (I - K_t H_t) P_{t|t-1} (I - K_t H_t)' + K_t R_t K_t' \quad \text{(Joseph form)}.
\end{aligned}
$$

Log-likelihood (for [[Maximum Likelihood Estimation (MLE)|MLE]]/EM):
$$
\ell(\theta) = -\frac{1}{2} \sum_{t=1}^T \left[ \log |2\pi S_t| + \tilde y_t' S_t^{-1} \tilde y_t \right].
$$

> [!tip] Missing observations
> If some entries of y_t are missing, either:
> - select observed components with H_t^\*, R_t^\* and apply the standard update; or
> - skip update (set $\hat x_{t|t}=\hat x_{t|t-1}$, $P_{t|t}=P_{t|t-1}$) for fully missing y_t.

---

## RTS smoother (fixed-interval)

Backward recursion for t = T−1,…,0 with $J_t = P_{t|t} F_{t+1}' P_{t+1|t}^{-1}$:
$$
\begin{aligned}
\hat x_{t|T} &= \hat x_{t|t} + J_t \left(\hat x_{t+1|T} - \hat x_{t+1|t}\right), \\
P_{t|T} &= P_{t|t} + J_t \left(P_{t+1|T} - P_{t+1|t}\right) J_t'.
\end{aligned}
$$

Cross-covariances (useful for EM):
$$
P_{t,t-1|T} = J_{t-1} P_{t|T}.
$$

---

## Parameter learning (EM for LDS)

Given a sequence {y_t}, alternate:

- E-step: run filter + RTS smoother to obtain expectations:
$$
\mathbb{E}[x_t],\;\mathbb{E}[x_t x_t'],\;\mathbb{E}[x_t x_{t-1}'].
$$

- M-step (no controls; time-invariant):
$$
\begin{aligned}
F &= \Big(\sum_{t=2}^T \mathbb{E}[x_t x_{t-1}']\Big)\Big(\sum_{t=2}^T \mathbb{E}[x_{t-1}x_{t-1}']\Big)^{-1}, \\
Q &= \frac{1}{T-1}\sum_{t=2}^T \Big(\mathbb{E}[x_t x_t'] - F \mathbb{E}[x_t x_{t-1}']' \Big), \\
H &= \Big(\sum_{t=1}^T y_t \mathbb{E}[x_t]'\Big)\Big(\sum_{t=1}^T \mathbb{E}[x_t x_t']\Big)^{-1}, \\
R &= \frac{1}{T}\sum_{t=1}^T \Big(y_t y_t' - H \mathbb{E}[x_t] y_t' \Big).
\end{aligned}
$$
Include inputs (B, D) and time-variation as needed. Initialize via PCA/OLS; iterate until log-likelihood convergence.

---

## Practical guidance

> [!check] Implementation checklist
> - Use Cholesky to solve $S_t^{-1}\tilde y_t$ and compute $\log|S_t|$; avoid explicit matrix inverses  
> - Maintain symmetry: P ← (P + P')/2; use Joseph form for numerical stability  
> - Initialize: diffuse $P_{0|0}=\lambda I$ (large λ) or use a short training run  
> - Handle missing y_t via selection matrices or skip updates  
> - Time-varying matrices are straightforward; ensure positive semidefiniteness of Q_t, R_t

> [!tip] Square-root and information forms
> - Square-root filter/smoother propagate Cholesky factors of covariances for better stability.  
> - Information filter uses precision matrices (good for sparse H, large-scale sensor fusion).

> [!warning]
> - Singular/near-singular S_t, Q_t, or R_t → add jitter εI or re-specify model  
> - Model misspecification (e.g., heavy tails) → consider robust filters or [[Sequential Monte Carlo (SMC)|SMC]]  
> - Switching dynamics violate linear–Gaussian assumptions → consider SLDS (with [[Hidden Markov Model (HMM)|HMM]] and [[Sequential Monte Carlo (SMC)|SMC]])

---

## Steady-state and forecasting

- Time-invariant systems converge to a steady-state gain K satisfying the discrete algebraic Riccati equation (DARE). Use it for long stationary runs.
- Multi-step forecasts: iterate the predict step; forecast variance grows via $P_{t+h|t}$ recursion.

---

## Minimal code sketch (Python-like)

```python
import numpy as np

def kf_filter(y, F, H, Q, R, x0, P0, B=None, D=None, U=None):
    """
    y: T x m, possibly with np.nan for missing
    F,H,Q,R: system matrices (assumed time-invariant here)
    x0,P0: initial mean/cov
    B,D,U: optional control matrices and inputs (T x r)
    Returns: dict with filtered/predicted states, covariances, innovations, S, loglik
    """
    T, m = y.shape
    n = x0.shape[0]
    x_pred = np.zeros((T, n))
    P_pred = np.zeros((T, n, n))
    x_filt = np.zeros((T, n))
    P_filt = np.zeros((T, n, n))
    innov  = np.zeros((T, m))
    S_list = np.zeros((T, m, m))
    loglik = 0.0
    x, P = x0.copy(), P0.copy()

    for t in range(T):
        # predict
        u = U[t] if (U is not None) else None
        if B is not None and u is not None:
            x = F @ x + B @ u
        else:
            x = F @ x
        P = F @ P @ F.T + Q
        x_pred[t], P_pred[t] = x, P

        # observed indices
        obs = ~np.isnan(y[t])
        if obs.any():
            Ht = H[obs, :]
            Rt = R[np.ix_(obs, obs)]
            yt = y[t, obs]
            dt = (D @ u)[obs] if (D is not None and u is not None) else 0.0

            v = yt - (Ht @ x) - dt
            S = Ht @ P @ Ht.T + Rt
            # solve via Cholesky
            L = np.linalg.cholesky(S)
            K = (P @ Ht.T) @ np.linalg.solve(L.T, np.linalg.solve(L, np.eye(L.shape[0])))
            x = x + K @ v
            I_KH = np.eye(n) - K @ Ht
            P = I_KH @ P @ I_KH.T + K @ Rt @ K.T  # Joseph form

            innov[t, obs] = v
            S_list[t][np.ix_(obs, obs)] = S
            logdetS = 2.0 * np.sum(np.log(np.diag(L)))
            quad = v @ np.linalg.solve(L.T, np.linalg.solve(L, v))
            loglik += -0.5 * (logdetS + quad + np.sum(obs) * np.log(2*np.pi))

        x_filt[t], P_filt[t] = x, P

    return dict(x_pred=x_pred, P_pred=P_pred, x_filt=x_filt, P_filt=P_filt,
                innov=innov, S=S_list, loglik=loglik)
```

---

## Variants and extensions

- Nonlinear: Extended KF (EKF), Unscented KF (UKF), Ensemble KF (EnKF)
- Robust/Student-t noise, constraints (e.g., nonnegativity), time-aggregation/irregular sampling
- Switching LDS (SLDS): discrete regime via [[Hidden Markov Model (HMM)|HMM]], continuous states via KF; inference with [[Sequential Monte Carlo (SMC)|SMC]]

---

## Related notes

- [[Hidden Markov Model (HMM)|HMM]] · [[Sequential Monte Carlo (SMC)|SMC]] · [[Time Series (MOC)]]  
- Estimation: [[Maximum Likelihood Estimation (MLE)|MLE]] · [[Bayesian econometrics]]  
- Modeling: unobserved components, local level/trend/seasonal models (special LDS cases)

---

## References

- Kalman (1960). A new approach to linear filtering and prediction problems.
- Rauch, Tung, & Striebel (1965). Maximum likelihood estimates of linear dynamic systems (RTS smoother).
- Anderson & Moore (1979). Optimal Filtering.
- Durbin & Koopman (2012). Time Series Analysis by State Space Methods.
- Särkkä (2013). Bayesian Filtering and Smoothing.

---