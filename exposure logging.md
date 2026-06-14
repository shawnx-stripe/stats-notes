---
title: exposure logging
aliases: [exposure event, impression logging, eligibility/exposure, logging for experiments]
tags: [experimentation, ab-testing, logging, instrumentation, data-engineering, diagnostics, srm, qa]
updated: 2025-09-17
---

# exposure logging

> [!summary] Quick definition
> Exposure logging records when a unit (user/session/device/geo) is actually exposed to a variant during an experiment. Reliable exposure events enable triggered analyses, variance reduction (pre-exposure baselines), and guardrails. Poor exposure logging causes bias, [[Sample Ratio Mismatch (SRM)|SRM]], and invalid inference.

- Use with: [[bucketing]] for assignment, [[AA test]]/[[Sample Ratio Mismatch (SRM)|SRM]] for sanity, [[AB Testing (MOC)]], [[guardrail metric]]s, [[sequential testing]].

---

## Why exposure logging matters

- Defines the analysis population:
  - ITT: all assigned units (regardless of exposure)
  - Triggered: units truly exposed (e.g., saw page/feature)
- Reduces bias from dilution/non-exposure; enables proper baselines ([[Controlled Experiments Using Pre-Experiment Data (CUPED)|CUPED]]/[[Analysis of Covariance (ANCOVA)|ANCOVA]]) and safety monitors.
- Supports dosage/intensity analyses (exposure count, dwell time).

> [!warning] Without reliable exposure, triggered analyses are biased or underpowered; SRM may mask routing/logging bugs.

---

## Core concepts

- Assignment vs. Eligibility vs. Exposure vs. Outcome
  - Assignment: deterministic variant from [[bucketing]]
  - Eligibility: in the at-risk population (met pre-specified conditions)
  - Exposure: actually saw/used feature (first-render, impression, viewable threshold, click)
  - Outcome: metric measurement window (post-exposure)
- Unit of analysis
  - Must align with randomization unit (user/device/session/geo/time-block) and clustering in SEs.

---

## What to log (event schema)

- Required fields (per event)
  - experiment_id, namespace, variant (arm)
  - unit identifiers: user_id, device_id, session_id, geo_id (as applicable)
  - assignment_hash_version, salt_id (for reproducibility)
  - timestamp (UTC), timezone offset if client-side
  - event_type: assignment | eligibility | exposure | outcome
  - exposure_context: surface/page, trigger_name, exposure_reason
  - request_id/impression_id (idempotency), app_version/build
  - consent/privacy flags; bot_filter flag; environment (prod/stage)
- Optional
  - dosage: exposure_count, dwell_time_ms, viewable (boolean), viewability_pct
  - network/perf: latency_ms, status_code
  - cohort labels: stratum/block, pre-period baseline window id

> [!tip] Idempotency and dedupe
> Include a unique impression_id per exposure; enforce de-dup on write or downstream (exactly-once is hard; aim for at-least-once with idempotent consumers).

---

## Design guidelines

- Define “exposure” precisely per surface:
  - Page: first meaningful paint or viewable (≥ 1s, ≥ 50% pixels)
  - API feature: successful response (2xx) with feature enabled
  - Ads/content: viewability thresholds; click for interactive exposure
- Triggered experiments:
  - Log eligibility separate from exposure; analyze on exposed (triggered) set but report ITT too.
  - Guard against “triggered bias” by predefining eligibility symmetrically across arms.
- Time and windows:
  - Use UTC timestamps; document analysis windows; handle clock skew; align to [[seasonality]] cycles.
- Privacy/compliance:
  - Respect consent; pseudonymize IDs; do not log sensitive PII; TTL/retention policies; data minimization.  

---

## QA and diagnostics

> [!check] Monitoring
> - [ ] Assignment→eligibility→exposure funnel by arm; parity across variants  
> - [ ] [[Sample Ratio Mismatch (SRM)|SRM]] at assignment, eligibility, exposure, and analysis layers  
> - [ ] Lag distributions (assignment→exposure); spikes/outages by time-of-day/week  
> - [ ] Duplicate/late event rate; idempotent de-dup success  
> - [ ] Join rates between exposure and outcomes; symmetric across arms  
> - [ ] Platform changes: app versions, deployments, schema changes

> [!warning] Red flags
> - Large differences in exposure rate across arms with equal eligibility  
> - Inner-join drop-off only in one arm (analysis bias)  
> - Time-window misalignment (variant starts later)  
> - Identity drift (user↔device), bot asymmetries

---

## Common pitfalls and remedies

- Inner joins bias
  - Pitfall: joining outcomes to exposures with inner join drops unexposed units asymmetrically.
  - Remedy: analyze ITT on assigned (left join outcomes to assignment); for triggered, confirm symmetric eligibility and exposure logging across arms.
- Missing/late exposures
  - Remedy: event buffering with retries; watermark-based windows; late-arrival handling.
- Multiple exposures per unit
  - Remedy: define first exposure for triggered analysis; use counts/dwell for dosage modeling.
- Client vs server logging mismatch
  - Remedy: reconcile client/server event sources; use server confirmation or dual logging with reconciliation rules.

---

## Minimal schemas and code

> [!example] JSON event (exposure)

```json
{
  "event_type": "exposure",
  "namespace": "feed",
  "experiment_id": "exp_42",
  "variant": "B",
  "user_id": "u_123",
  "session_id": "s_abc",
  "assignment_hash_version": "v2",
  "salt_id": "salt_2025_01",
  "timestamp": "2025-09-17T14:23:35Z",
  "surface": "home_feed",
  "trigger_name": "feed_render",
  "impression_id": "imp_7f9e2",
  "app_version": "iOS_7.3.1",
  "consent": true,
  "bot_filtered": false
}
```

> [!example] SQL table (PostgreSQL)

```sql
CREATE TABLE exp_exposure (
  event_ts          timestamptz NOT NULL,
  namespace         text NOT NULL,
  experiment_id     text NOT NULL,
  variant           text NOT NULL,
  user_id           text,
  session_id        text,
  geo_id            text,
  assignment_hash_version text,
  salt_id           text,
  surface           text,
  trigger_name      text,
  impression_id     text,
  app_version       text,
  consent           boolean,
  bot_filtered      boolean,
  PRIMARY KEY (experiment_id, impression_id)  -- idempotency
);
CREATE INDEX ON exp_exposure (experiment_id, variant, event_ts);
CREATE INDEX ON exp_exposure (user_id, event_ts);
```

> [!example] Kafka topic (avro-like fields)

```
topic: experiments.exposure.v1
key: experiment_id + impression_id
value: {event_ts, namespace, variant, unit_ids..., context..., hash_version, salt_id}
```

> [!example] Client-side debounced logging (pseudo)

```javascript
let sent = false;
function onRender() {
  if (sent) return;
  const now = new Date();
  // Optional: ensure viewability threshold
  setTimeout(() => {
    if (isViewable(1000, 0.5)) {
      logExposure({exp_id, variant, user_id, session_id, impression_id, ts: now.toISOString()});
      sent = true;
    }
  }, 1000);
}
```

> [!example] SQL: ITT vs triggered cohorts

```sql
-- ITT: all assigned users
SELECT d.experiment_id, d.variant, COUNT(*) AS n_assigned
FROM assignment d
GROUP BY 1,2;

-- Triggered: exposed users
SELECT e.experiment_id, e.variant, COUNT(DISTINCT e.user_id) AS n_exposed
FROM exp_exposure e
GROUP BY 1,2;

-- Join outcomes carefully: for ITT, left-join outcomes onto assignment
SELECT d.variant,
       AVG(o.metric) FILTER (WHERE d.variant='B') - AVG(o.metric) FILTER (WHERE d.variant='A') AS diff
FROM assignment d
LEFT JOIN outcomes o
  ON o.user_id = d.user_id AND o.window_id = d.window_id
WHERE d.experiment_id = 'exp_42'
GROUP BY d.variant;
```

---

## Analysis tips

- ITT vs triggered:
  - Report ITT as default (policy effect of assignment).
  - Triggered analyses require symmetric eligibility/exposure across arms; document definitions.
- CUPED/ANCOVA:
  - Use pre-exposure baselines; do not use post-exposure features ([[leakage]]).
- Clustering:
  - If randomization at session/geo/time-block: cluster SEs appropriately; apply [[few-cluster corrections]] when clusters are few.

---

## Governance and reproducibility

- Registry: store experiment metadata (namespace, salts, splits, exclusion groups).
- Versioning: schema version, hash algorithm version, client SDK version.
- Audits: reproducible replays of assignment and exposure; signed configs.

---

## Reporting essentials

- Exposure definition and trigger conditions; unit and namespace
- Assignment→eligibility→exposure funnel and parity by arm
- SRM and [[AA test]] results at multiple layers
- Join rates and handling of duplicates/late events
- Any outages, deploys, schema/app-version changes during run
- Alignment with analysis windows and [[seasonality]]

---

## Common pitfalls

> [!warning]
> - Logging exposure only after success (e.g., click) → selection bias  
> - Using inner joins that drop unexposed units asymmetrically  
> - Clock skew/timezone mishandling; partial-day windows across variants  
> - Identity drift and bot asymmetry; per-session analysis with per-user bucketing  
> - Multiple exposures counted inconsistently; missing idempotency keys  
> - Changing hash/salt mid-run (reassignment artifacts)

---

## Related notes

- [[AB Testing (MOC)]] · [[Experimental Design (MOC)]]
- [[bucketing]] · [[Sample Ratio Mismatch (SRM)|SRM]] · [[AA test]] · [[guardrail metric]]
- [[Controlled Experiments Using Pre-Experiment Data (CUPED)|CUPED]] · [[Analysis of Covariance (ANCOVA)|ANCOVA]] · [[power analysis]] · [[Minimum Detectable Effect (MDE)|MDE]]
- [[sequential testing]] · [[clustered standard errors]] · [[few-cluster corrections]]
- [[seasonality]] · [[switchback experiment]] · [[geo experiment]]