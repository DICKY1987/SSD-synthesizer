
# Reentry Governance Checklist (Mapped to EA Inputs & CSV Columns)

> Use this checklist to verify governance controls are configured and enforced. Each item maps to EA inputs and/or CSV columns.

| Control | Purpose | EA Input Name | CSV Column | Default | Range / Rule | Enforcement Point | Telemetry / DB Column | Failure Action | Notes |
|---|---|---|---|---|---|---|---|---|---|
| Allow Reentry | Global enable/disable for reentry logic | AllowReentry |  | 1 | 0 or 1 | Analyzer/Governance Gate | trades_<SYMBOL>.is_reentry | Skip reentry | Gate before queue/execute |
| Min Delay Seconds | Minimum allowed delay before any reentry executes | MinDelaySeconds | DelaySeconds | 0 | >= 0 | Governance Gate + Executor | reentry_executions_<SYMBOL>.ts | Enforce max(actual, min) | Per-action delay must not be less than this |
| Max Generations | Maximum number of reentry generations allowed | MaxGenerations |  | 0 | >= 0 integer | Analyzer/Governance Gate | trades_<SYMBOL>.reentry_generation | Stop chain | Check generation before enqueue |
| Daily Loss Limit | Stop new reentries when daily realized PnL <= -limit | DailyLossLimit |  |  | currency amount | Governance Gate | aggregated day PnL | Stop chain & disable | Reset by broker day rollover |
| Min Confidence | Minimum confidence required to execute | MinConfidence | ConfidenceAdjustment |  | 0.0–1.0 (or model-based) | Governance Gate | reentry_executions_<SYMBOL>.confidence | Skip reentry | Requires EA to compute confidence metric |
| Blackout After N Losses | Pause reentries after N consecutive losses | BlackoutAfterLosses, BlackoutMinutes |  |  | N>=1; minutes>=0 | Governance Gate | counters in EA state | Disable for window | Track consecutive losses and timestamps |
| Max Position Size | Hard cap on lots for any reentry | MaxPositionSize | SizeMultiplier |  | >0; broker cap | Executor (pre-OrderSend) | reentry_executions_<SYMBOL>.size_lots | Clamp/Skip | Clamp to min(broker max, governance cap) |
| Spread Guard | Block entries if spread too wide | MaxSpreadPoints |  |  | points/pips | Executor (pre-OrderSend) | execution error logs | Skip | Compare current spread to limit |
| Freeze Level Guard | Avoid entry near broker freeze level | FreezeLevelGuard |  | 1 | 0 or 1 | Executor (pre-OrderSend) | execution error logs | Skip | Check distance to SL/TP vs freeze level |
| Retries (Bounded) | Bounded retries on transient send errors | MaxOrderSendRetries |  | 2 | >=0 integer | Executor | reentry_executions_<SYMBOL>.status,error | Abort chain on hard errors | Backoff between retries |
| Magic Base Offset | Distinct magic space for reentries/generations | ReentryMagicBase |  |  | integer | Executor | trades_<SYMBOL>.* | N/A | e.g., base+1000+generation for lineage |
| Queue Mode | Use OnTimer queue vs Sleep in trade thread | UseOnTimerQueue |  | 1 | 0 or 1 | Scheduler | execution timing | N/A | Re-check guards right before OrderSend |
| Profile Path | CSV path pattern for per-symbol profiles | ReentryProfilePath |  |  | path | Init/Loader | config files | N/A | e.g., MQL4/Files/config/<SYMBOL>_reentry.csv |
| Live Profile Reload | Enable periodic reload of profile without restart | EnableLiveProfileReload, ReloadSeconds |  | 0 | 0 or 1; seconds>=5 | OnTimer Loader | profile version tag | Skip reload | Optional enhancement |
| Execution Logging | Audit every attempted execution | EnableExecutionLog |  | 1 | 0 or 1 | Executor/Post-Trade | reentry_executions_<SYMBOL> | N/A | Append-only logging |
| Performance Snapshot | Maintain per-action KPIs |  |  | auto | derived | Analytics Job | reentry_performance_<SYMBOL> | N/A | Updated nightly or on schedule |
