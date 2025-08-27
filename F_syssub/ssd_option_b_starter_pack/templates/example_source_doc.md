# HUEY_P Ops Runbook (Excerpt)
- Reentry logic supports conservative, moderate, and aggressive profiles.
- Daily loss cap is 3% with a circuit breaker at 4%.
- Time sync: NTP with drift budget of 50ms.
- Immutable logging via hash-chained append-only file; retention 365 days.
