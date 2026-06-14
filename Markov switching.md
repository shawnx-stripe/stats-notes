---
title: Markov Switching
aliases: [Markov switching, regime switching, Hamilton regime switching]
tags: [econometrics, time-series, structural-breaks]
updated: 2026-03-05
---

# Markov Switching

> [!summary]
> Time-series model where parameters switch between discrete regimes (states) governed by a hidden Markov chain. Allows for recurrent structural changes (e.g., expansions/recessions). Estimated via the EM algorithm or Bayesian methods.

## Model specification

$$
y_t = \mu_{S_t} + \phi_{S_t}(y_{t-1} - \mu_{S_{t-1}}) + \sigma_{S_t}\epsilon_t
$$

where $S_t \in \{1, 2, \ldots, K\}$ is the unobserved regime at time $t$, governed by:

$$
P(S_t = j \mid S_{t-1} = i) = p_{ij}
$$

Transition probabilities $p_{ij}$ form the Markov chain; parameters $(\mu_k, \phi_k, \sigma_k)$ vary by regime.

## When to use

- Business cycles: expansions vs. recessions with different dynamics
- Volatility regimes: low vs. high variance periods in financial returns
- Policy shifts: structural breaks that recur or alternate
- Better than one-time break tests ([[Bai–Perron]]) when regime changes are recurrent

> [!tip]
> Use likelihood-ratio tests or information criteria (AIC/BIC) to select the number of regimes $K$. Start with $K=2$ and check if additional regimes are justified.

## Related notes

- [[Bai–Perron]]
- [[Hidden Markov Model (HMM)|HMM]]
- [[Time Series (MOC)]]
- [[EM algorithm]]
