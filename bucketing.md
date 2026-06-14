---
title: bucketing
aliases:
- random assignment
- hashing
- bucketization
- traffic split
- assignment
- namespace
- Bucketing
tags:
- experimentation
- ab-testing
- assignment
- hashing
- srm
- identity
- exposure
- rollout
updated: 2025-09-17
---

# bucketing

> [!summary] Quick definition
> Bucketing is the deterministic assignment of units (e.g., users, sessions, devices, geos) to experiment variants via a seeded hash and a mapping to planned traffic shares. Good bucketing ensures stable assignment, reproducibility, and correct split proportions for valid inference (no [[Sample Ratio Mismatch (SRM)|SRM]]), while allowing ramping, mutual exclusion, and namespace isolation.

- Core uses: [[AB Testing (MOC)]], canaries/rollouts, geo-/switchback experiments, holdouts.
- Goals: stability (sticky assignment), reproducibility (seed/salt), planned allocation (e.g., 50/50), isolation across experiments.

---

## Key concepts

- Unit of randomization: user, device, session/request, account, geo/cluster, time block (switchbacks).
- Namespace: a scope that prevents collisions across experiments sharing a unit (e.g., “search-results-page” namespace).
- Seed/salt: experiment-specific secret added to the key (unit_id + namespace + salt) to generate independent assignments.
- Deterministic hashing: same (unit_id, namespace, salt) maps to same bucket; allows backfills and replays.
- Allocation map: cumulative thresholds that map uniform[0,1) to variants (supports multi-arm splits).

> [!warning] Unit mismatch
> Bucketing at user-level but analyzing at session-level without accounting for clustering inflates Type I error (use [[clustered standard errors]]).

---

## Best practices

- Use strong hash (e.g., murmur3/xxhash/sha256) → 64-bit integer → map to [0,1).
- Always include namespace + experiment_id + secret salt in the hash key to avoid collisions/correlation across tests.
- Persist assignments (sticky bucketing) at the unit level so users do not flip variants mid-experiment.
- Implement mutual exclusion (exclusion groups) when experiments may interfere; or allocate within disjoint namespaces.
- Support ramping by changing allocation thresholds, not the hash. Do not change salts mid-run.
- Validate identity stability (user_id login changes, cross-device) and bot filtering symmetry.
- Log assignment and exposure events separately; analyze on exposed population only when using triggered designs, but keep [[AA test]] and [[Sample Ratio Mismatch (SRM)|SRM]] on upstream layers too.
- Document planned split, namespace, salt management, exclusion rules, and ramp plan.

---

## Typical flows

1) Determine unit and namespace (e.g., user_id in “feed-ranking” namespace).
2) Build key = concat(namespace, experiment_id, user_id, salt).
3) Hash key → 64-bit → u = hash / 2^64 ∈ [0,1).
4) Map u to variant via split thresholds (e.g., [0, 0.5) → A, [0.5, 1) → B).
5) Persist assignment; emit assignment and exposure logs.
6) For ramps, adjust thresholds; do not change hash inputs.

---

## Ramping and allocation

- Multi-arm: define cumulative thresholds (e.g., A:0.2, B:0.3, C:0.5).
- Ramping: 1% → 5% → 20% → 50% by shifting thresholds; keep seeds constant.
- Holdouts: reserve global or namespace-level buckets (e.g., 1–5%) for long-term evaluation or baselines.
- Traffic shaping/throttling: avoid asymmetric throttling across arms (causes [[Sample Ratio Mismatch (SRM)|SRM]]).

---

## Mutual exclusion and collisions

- Exclusion groups: ensure a unit participates in at most one test of a given family/namespace at a time.
- Layered/nested bucketing: parent bucket for eligibility → child buckets per test (consistent hashing across layers).
- Geo/cluster constraints: first assign clusters, then inherit to units; prioritize number of clusters over cluster size for power.

---

## Special designs

- Switchbacks (time-sliced): unit = time block; hash on (namespace, experiment_id, time_block); ensure block lengths exceed autocorrelation span; align with [[seasonality]].
- Geo experiments: unit = geo/market; bucket at geo level; sizes vary → plan with cluster power; analyze with SCM/DiD and cluster-robust SEs.
- Bandits: bucketing replaced by adaptive allocation; inference differs (SRM is expected; see bandits).

---

## Diagnostics and monitoring

> [!check] Monitor continuously
> - [ ] [[Sample Ratio Mismatch (SRM)|SRM]] at assignment, eligibility, exposure, and analysis layers  
> - [ ] [[AA test]] periodically, especially after identity/logging changes  
> - [ ] Balance on key covariates and pre-period metrics  
> - [ ] Hash stability across deploys; namespace collisions; salt rotation policies  
> - [ ] Exposure logging completeness; time-zone alignment; cycle coverage (see [[seasonality]])

---

## Pitfalls and remedies

> [!warning]
> - Non-uniform hash/modulus bug → SRM; fix hashing and replay assignments  
> - Changing salts mid-run → reassignment; avoid, or restart test  
> - Sticky bucketing disabled → units flip variants; re-enable persistence; exclude flip windows in sensitivity  
> - Assignment in analysis join omitted for one arm → asymmetric drops; fix joins/logs  
> - Mutual exclusion missing → interference across tests; introduce exclusion groups or staged rollouts  
> - Unit identity drift (user↔device) → unstable cohorts; improve identity resolution and filtering

---

## Minimal code snippets

> [!example] Python: deterministic hash to variant (two-arm)

```python
import hashlib
def assign_variant(user_id, namespace, exp_id, salt, splits=[0.5, 1.0], variants=('A','B')):
    key = f"{namespace}:{exp_id}:{user_id}:{salt}".encode('utf-8')
    h = hashlib.sha256(key).digest()
    # take first 8 bytes as unsigned 64-bit
    val = int.from_bytes(h[:8], 'big', signed=False)
    u = val / float(2**64)  # in [0,1)
    for thr, name in zip(splits, variants):
        if u < thr:
            return name
    return variants[-1]
```

> [!example] SQL: bucket users with consistent hashing (PostgreSQL)

```sql
-- Requires pgcrypto for digest(); map first 8 bytes to bigint then to [0,1)
WITH params AS (
  SELECT 'feed'::text AS namespace, 'exp42'::text AS exp_id, 's3cr3t'::text AS salt
),
assign AS (
  SELECT u.user_id,
         ('x' || substr(encode(digest(namespace||':'||exp_id||':'||u.user_id||':'||salt, 'sha256'), 'hex'),1,16))::bit(64)::bigint AS h64
  FROM users u, params
)
SELECT user_id,
       CASE WHEN (h64::numeric / 18446744073709551616) < 0.5 THEN 'A' ELSE 'B' END AS variant
FROM assign;
```

> [!example] JavaScript: multi-arm thresholds

```javascript
function assignVariant(id, namespace, expId, salt, thresholds=[0.2,0.5,1.0], variants=['A','B','C']){
  const key = `${namespace}:${expId}:${id}:${salt}`;
  const h = sha256.arrayBuffer(key); // use a crypto lib; returns ArrayBuffer
  const view = new DataView(h);
  const high = view.getUint32(0);
  const low  = view.getUint32(4);
  const val = high * 2**32 + low;
  const u = val / 2**64;
  for (let i=0;i<thresholds.length;i++){
    if (u < thresholds[i]) return variants[i];
  }
  return variants[variants.length-1];
}
```

> [!example] Switchback: time-based bucketing key

```python
time_block = f"{year}-{week:02d}"  # or 15-min block
key = f"{namespace}:{exp_id}:{time_block}:{salt}"
# hash and map as usual
```

---

## Reproducibility and governance

- Log and store: namespace, experiment_id, salt/seed id (not necessarily the secret), planned splits, ramp schedule.
- Keep a registry of active experiments and exclusion groups; block conflicting launches.
- Provide replay tools to recompute assignments for audits and backfills.

---

## Reporting essentials

- Unit of randomization; namespace and exclusion policy
- Hashing method; key components; salt policy
- Planned splits and ramp schedule; assignment vs. exposure rules (triggered vs. ITT)
- SRM and AA outcomes; identity stability checks; logging completeness
- Any re-bucketing events and their handling (e.g., restart, sensitivity cut)

---

## Related notes

- [[AB Testing (MOC)]] · [[Experimental Design (MOC)]]
- [[Sample Ratio Mismatch (SRM)|SRM]] · [[AA test]] · [[guardrail metric]]
- [[exposure logging]] · [[sequential testing]]
- [[Controlled Experiments Using Pre-Experiment Data (CUPED)|CUPED]] · [[Analysis of Covariance (ANCOVA)|ANCOVA]]
- [[clustered standard errors]] · [[few-cluster corrections]]
- [[seasonality]] · [[switchback experiment]] · [[geo experiment]]