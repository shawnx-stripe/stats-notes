---
title: Seasonality
aliases: [Seasonality, seasonal patterns, seasonal effects, time-of-year effects, calendar effects, seasonal adjustment]
tags: [time-series, econometrics, causal-inference, did, panels, decomposition, forecasting]
updated: 2025-09-17
---

# Seasonality

> [!summary] Quick definition
> Seasonality is systematic, calendar-related variation in outcomes that repeats at known intervals (e.g., month-of-year, quarter, day-of-week, holidays). If untreated and treated units differ in seasonal patterns and these aren’t modeled, causal estimates can be biased.

- Common sources: weather/temperature, demand cycles (holidays, back-to-school), billing cycles, production plans, tourism, day-of-week trading, moving holidays (Easter, Lunar New Year), and policy calendars.

## Why it matters for causal inference

- In [[Difference-in-Differences (DiD)]], a policy that starts in a “high” season for treated but “low” for controls can mimic treatment effects unless seasonality is controlled.
- With [[staggered adoption]], cohort-season interactions may be needed if cohorts differ in seasonal composition.
- For [[Synthetic Control]], pre/post fit can deteriorate if seasonal alignment differs or holidays shift; include seasonal predictors.
- In [[Regression Discontinuity Design (RDD)]] around a date threshold, nearby seasonal changes can confound discontinuities.
- In [[Instrumental Variables (IV)]], instruments correlated with calendar cycles may violate [[exclusion restriction]] if seasonality directly affects Y.

## Modeling strategies

### 1) Fixed effects (recommended default)
- Include calendar dummies:
  - Month-of-year, quarter, week-of-year, day-of-week, hour-of-day.
  - Interact with geography/industry when seasonal amplitude differs.

Copy-ready examples:
- Add month-of-year FE: i(month)
- Add interactions for heterogeneous seasonality: i(month) × Region

### 2) Flexible seasonal functions
- Fourier terms (useful with high-frequency series or to avoid many dummies):
$$
Y_t = \dots + \sum_{k=1}^{K} \big[ \alpha_k \cos(2\pi k t/S) + \beta_k \sin(2\pi k t/S) \big] + \varepsilon_t
$$
where S is the seasonal period (e.g., 12 for months).

### 3) Seasonal adjustment (pre-processing)
- STL/X-13ARIMA-SEATS/tramo-seats to remove seasonality from Y (and sometimes X).
- Pros: clearer signals, simpler models.
- Cons: can complicate inference (two-step uncertainty), risks misalignment if applied differently across groups. Prefer modeling seasonality in the regression unless adjustment quality and comparability are assured.

### 4) Event-/holiday-specific indicators
- Include fixed-date and moving-holiday dummies (Easter, Ramadan, Lunar New Year) and window effects (lead/lag around the holiday).
- Local idiosyncrasies: school breaks, fiscal quarter closings, harvest season.

## Seasonality in DiD and event studies

> [!check] Good practice
> - [ ] Include season FE (e.g., month-of-year) in all specifications.
> - [ ] If seasonality differs across groups, add season × group or season × cohort interactions.
> - [ ] Align analysis windows to comparable seasons (e.g., compare same months year-over-year).
> - [ ] In [[event study]], include season FE and confirm pre-trend leads are near zero after controlling for seasonality.

> [!warning] Pitfalls
> - Comparing partial-year pre vs. full-year post (seasonal composition changes).
> - Ignoring moving holidays that shift across years.
> - Treating seasonality with a single linear trend.
> - Using different seasonal adjustments for treated vs. control without documenting methods.

## Diagnostics

- Plots: seasonal subseries (monthly means by month), boxplots by month or weekday.
- Decomposition: STL or X-13 to visualize seasonal component.
- Frequency-domain: periodogram or autocorrelation at seasonal lags (12, 7, 52).
- Stability checks: test whether seasonal differences between groups are stable pre-treatment.

## Minimal code snippets

> [!example] R: Add seasonality to DiD with fixest

```r
library(fixest); library(lubridate)
df$month <- month(df$date)
df$dow   <- wday(df$date, label = TRUE)
# Baseline DiD with month FE
est1 <- feols(Y ~ D:Post + i(month) | id + year, cluster = ~id, data = df)
# Heterogeneous seasonality by region
est2 <- feols(Y ~ D:Post + i(month, region) | id + year, cluster = ~region, data = df)
etable(est1, est2)
```

> [!example] R: STL decomposition (diagnostics)

```r
library(forecast)
# Assume ts monthly data
y_ts <- ts(df$Y, frequency = 12, start = c(2015,1))
fit <- stl(y_ts, s.window = "periodic")
plot(fit)  # trend/seasonal/remainder
```

> [!example] Stata: Add month and DOW FE; moving holiday

```stata
gen month = month(date)
gen dow   = dow(date)
reghdfe Y c.Post##i.D i.month i.dow, absorb(id year) vce(cluster id)

* Moving holiday example: Easter ±k days (requires a date list or package)
* Create a dummy for the Easter week
gen easter_week = inrange(date, easter_date-3, easter_date+3)
reghdfe Y c.Post##i.D i.month i.dow easter_week, absorb(id year) vce(cluster id)
```

> [!example] Python: Statsmodels seasonal_decompose; PanelOLS with season FE

```python
import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose
from linearmodels.panel import PanelOLS

# Decomposition (monthly)
y = df.set_index('date')['Y'].asfreq('M')
res = seasonal_decompose(y, model='additive', period=12)
res.plot()

# Panel with season FE
df = df.set_index(['id','date']).copy()
df['month'] = df.index.get_level_values('date').month
res = PanelOLS.from_formula('Y ~ 1 + D + Post + D:Post + C(month) + EntityEffects + TimeEffects',
                            data=df).fit(cov_type='clustered', cluster_entity=True)
print(res.summary)
```

> [!example] Fourier terms in regression (R)

```r
library(fixest)
S <- 12; K <- 2
for(k in 1:K){
  df[[paste0("cos",k)]] <- cos(2*pi*k*seq_len(nrow(df))/S)
  df[[paste0("sin",k)]] <- sin(2*pi*k*seq_len(nrow(df))/S)
}
est <- feols(Y ~ D:Post + cos1 + sin1 + cos2 + sin2 | id + year, data = df)
```

## Practical guidance

> [!check] Checklist
> - [ ] Identify seasonal period(s): month/quarter/week/day/hour.
> - [ ] Add season FE (and interactions if amplitudes differ across groups/regions).
> - [ ] Model key holidays/events (fixed and moving).
> - [ ] Align pre/post windows across comparable seasons.
> - [ ] If seasonally adjusting, document method and apply consistently across groups.
> - [ ] Use proper clustering (often entity or higher-level region); see [[clustered standard errors]].

> [!tip] High frequency data
> - Day-of-week and month-of-year FE often capture most calendar effects.
> - Add “end-of-month/quarter” dummies for financial settings.

## Common pitfalls

> [!warning] Avoid these
> - Pre-adjusting with black-box filters that differ across groups, then treating adjusted series as error-free.
> - Interpreting seasonal coefficients as policy effects (they’re controls).
> - Ignoring seasonality in covariates X when relying on conditional trends.
> - Neglecting partial-year samples that change seasonal composition (see [[composition]]).

## Copy-ready snippets

- Fourier seasonal terms:
$$
\sum_{k=1}^{K} \alpha_k \cos(2\pi k t/S) + \beta_k \sin(2\pi k t/S)
$$

- Month FE with heterogeneous amplitude across regions:
$$
Y_{it} = \dots + \sum_{m=1}^{11} \delta_{m} \, \mathbf{1}\{\text{month}=m\}
+ \sum_{m=1}^{11} \sum_{r} \eta_{mr}\, \mathbf{1}\{\text{month}=m\}\mathbf{1}\{\text{region}=r\} + \varepsilon_{it}
$$

## Reporting essentials

- Which seasonal controls were included (month/quarter/weekday, holidays, Fourier terms).
- Whether seasonal adjustment was applied (method, parameters) and to which variables.
- Any season × group (or × region/cohort) interactions.
- Choice of clustering and justification.

---

## Related notes
- [[Difference-in-Differences (DiD)]]
- [[event study]]
- [[pre-trends]]
- [[parallel trends assumption]]
- [[staggered adoption]]
- [[Synthetic Control]]
- [[Regression Discontinuity Design (RDD)]]
- [[Instrumental Variables (IV)]]
- [[exclusion restriction]]
- [[composition]]
- [[covariates]]
- [[clustered standard errors]]
- [[placebo test]]
- [[Conley standard errors]]