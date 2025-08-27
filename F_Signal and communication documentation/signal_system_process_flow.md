# Signal System - Complete Process Flow Document

## System Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Calendar      │    │   Indicator     │    │   Manual        │
│   System        │    │   System        │    │   Entry         │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 │
                    ┌─────────────▼─────────────┐
                    │   SignalTriggerHandler    │
                    └─────────────┬─────────────┘
                                 │
                    ┌─────────────▼─────────────┐
                    │   Signal Processing       │
                    │   Pipeline                │
                    └─────────────┬─────────────┘
                                 │
                    ┌─────────────▼─────────────┐
                    │   MT4 Integration         │
                    └───────────────────────────┘
```

## Complete Process Flow

### Phase 1: Signal Initiation

```
Event Sources → SignalTriggerHandler
├── Calendar Events (Economic announcements, anticipation events)
├── Indicator Signals (Technical analysis triggers)
└── Manual Entries (User-generated signals)

SignalTriggerHandler Actions:
1. Receive trigger event
2. Extract event metadata (currency, impact, time, source)
3. Generate CompositeKey based on event type
4. Pass to StrategyResolver

CompositeKey Format Examples:
├── "USD_HIGH_NFP" (Calendar economic event)
├── "ANTICIPATION_USD_HIGH_2H" (Calendar anticipation)
├── "MACD_CROSS_EURUSD" (Indicator signal)
└── "MANUAL_EURUSD" (Manual entry)
```

### Phase 2: Strategy Resolution & Parameter Selection

```
StrategyResolver Process:
1. Receive CompositeKey from SignalTriggerHandler
2. Lookup StrategyID in StrategyMap
3. If not found → Use DEFAULT_STRATEGY
4. Return StrategyMetadata object

StrategyMetadata Contains:
├── StrategyID: Integer (301=Calendar, 401=Indicator, 501=Manual)
├── Symbol: String (EURUSD, GBPUSD, etc.)
├── ParameterSetID: Integer (Always 1 for simplified system)
├── Priority: Integer (for conflict resolution)
└── Active: Boolean (strategy enabled/disabled)

ParameterSetLoader Process:
1. Receive ParameterSetID (always 1)
2. Load Parameter Set 1 configuration
3. Validate parameter values
4. Return ParameterProfile object

Parameter Set 1 (Default):
├── LotSize: 0.01
├── StopLoss: 20 pips
├── TakeProfit: 40 pips
├── BuyDistance: 10 pips
├── SellDistance: 10 pips
├── ExpireHours: 24
├── TrailingStop: 0 (disabled)
└── MaxSpread: 3 pips
```

### Phase 3: Signal Building

```
SignalBuilder Process:
1. Receive StrategyMetadata + ParameterProfile
2. Create Signal object with all required fields
3. Generate OrderComment with metadata
4. Add timestamps and processing info
5. Pass to SignalValidator

Signal Object Structure:
├── SignalID: Unique identifier
├── Symbol: Trading pair
├── StrategyID: Strategy identifier
├── ParameterSetID: Always 1
├── LotSize: 0.01
├── StopLoss: 20
├── TakeProfit: 40
├── BuyDistance: 10
├── SellDistance: 10
├── ExpireHours: 24
├── MaxSpread: 3
├── TrailingStop: 0
├── OrderComment: "Strategy:301|Event:NFP|Time:14:30"
├── SourceEvent: Original event data
├── CreatedTime: Signal creation timestamp
├── Status: CREATED
└── ProcessingNotes: ""
```

### Phase 4: Multi-Tier Validation

```
SignalValidator - Tier 1 (Structural):
✓ Check all required fields present
✓ Validate data types (numbers, strings, dates)
✓ Ensure no null/empty critical values
✓ Verify field value ranges
❌ FAIL → Status: REJECTED_TIER1, Log error, STOP

SignalValidator - Tier 2 (Business Logic):
✓ Validate symbol format (6-character pairs)
✓ Check lot size within broker limits
✓ Verify SL/TP ratios are reasonable
✓ Confirm expiration time is future
✓ Validate spread threshold
❌ FAIL → Status: REJECTED_TIER2, Log error, STOP

SignalValidator - Tier 3 (Market Context):
✓ Check market hours for symbol
✓ Verify not weekend/holiday
✓ Confirm broker allows trading
✓ Validate current spread < MaxSpread
❌ FAIL → Status: RETRY_ONCE, Log warning, Queue for retry

Status Update: VALIDATED (if all tiers pass)
```

### Phase 5: Conflict Detection & Resolution

```
ConflictManager Process:
1. Check for existing signals on same symbol within ±5 minutes
2. Apply simple resolution rule: DROP second signal
3. Log conflict details
4. Update signal status

Conflict Detection Logic:
├── Time Window: ±5 minutes from signal time
├── Symbol Match: Exact symbol match required
├── Status Check: Only check VALIDATED/EXPORTED signals
└── Resolution: Always drop the second (newer) signal

Conflict Resolution:
IF conflict detected:
├── First Signal: Continue processing (Status: VALIDATED)
├── Second Signal: Drop immediately (Status: DROPPED_CONFLICT)
├── Log: "Signal dropped - conflict with SignalID:123 on EURUSD"
└── Increment conflict counter for monitoring

IF no conflict:
├── Signal: Continue to export (Status: CONFLICT_CHECKED)
├── Record signal in active signals list
└── Proceed to export phase
```

### Phase 6: Signal Export

```
SignalExporter Process:
1. Receive validated, conflict-free signal
2. Execute transactional export
3. Update signal status
4. Handle export failures

Transactional Export Steps:
1. Create temporary file: signals_temp.csv
2. Write signal data to temporary file
3. Validate temporary file structure
4. Atomic rename: signals_temp.csv → signals.csv
5. Update signal status to EXPORTED
6. Log successful export

Export Failure Handling:
├── File Lock Error → Retry after 2 seconds (max 3 attempts)
├── Write Permission Error → Log CRITICAL error, freeze system
├── Validation Error → Reject signal, log error
└── Partial Write → Delete temp file, retry

Export Success Actions:
├── Reset consecutive failure counter
├── Update last export timestamp
├── Add to MT4 feedback monitoring
└── Log export success
```

### Phase 7: MT4 Integration & Feedback

```
MT4 Communication:
1. MT4 EAs monitor signals.csv for new entries
2. EA processes signal and updates status
3. Excel monitors feedback files for responses

MT4 Feedback Files:
├── signals_status.csv (EA writes signal receipt confirmation)
├── trade_results.csv (EA writes execution results)
└── signal_rejections.csv (EA writes rejection reasons)

Feedback Processing Timeline:
├── T+0: Signal exported to signals.csv
├── T+60s: Check for receipt confirmation in signals_status.csv
├── T+300s: Check for execution result in trade_results.csv
├── Timeout: Mark signal as failed if no feedback

SignalTimeoutMonitor:
├── Track all exported signals
├── Monitor feedback within timeout windows
├── Update signal status based on feedback
├── Count timeouts as failures for freeze logic

Signal Lifecycle States:
CREATED → VALIDATED → CONFLICT_CHECKED → EXPORTED → RECEIVED_BY_MT4 → EXECUTED → COMPLETED
```

### Phase 8: Error Handling & System Protection

```
Error Classification:
├── CRITICAL: System/MT4 connection failures
├── HIGH: Validation failures, export failures
├── MEDIUM: Conflicts, timeouts
└── LOW: Data quality warnings

Consecutive Failure Tracking:
├── Track HIGH and CRITICAL errors only
├── Reset counter on successful signal export
├── Increment on each HIGH/CRITICAL error
├── Trigger system freeze at 3 consecutive failures

System Freeze Logic:
IF consecutive_failures >= 3:
├── Set SystemStatus = FROZEN
├── Stop accepting new signals
├── Log freeze reason and timestamp
├── Alert user via dashboard
├── Require manual unfreeze action

Error Recovery Actions:
├── CRITICAL → Stop all processing, alert user
├── HIGH → Stop affected signal, increment failure counter
├── MEDIUM → Retry with delay, log warning
└── LOW → Log info, continue processing
```

## System State Management

### Named Ranges (System State)
```
SignalProcessingStatus:
├── SystemInitialized: Boolean
├── SignalSystemActive: Boolean
├── LastSignalProcessed: DateTime
├── ConsecutiveFailures: Integer (0-3)
├── SystemFrozen: Boolean
├── FreezeReason: String
├── FreezeTimestamp: DateTime
├── TotalSignalsProcessed: Integer
├── TotalSignalsSuccessful: Integer
├── TotalSignalsRejected: Integer
├── TotalConflictsDetected: Integer
└── LastSuccessfulExport: DateTime

MT4IntegrationStatus:
├── MT4ConnectionVerified: Boolean
├── LastMT4Feedback: DateTime
├── PendingSignalsCount: Integer
├── TimeoutSignalsCount: Integer
├── RejectedSignalsCount: Integer
└── MT4HealthScore: Integer (0-100)
```

### Dashboard Integration Points
```
Real-time Dashboard Updates:
├── Signal processing statistics
├── System health indicators
├── Consecutive failure counter
├── MT4 connection status
├── Recent signal history
├── Conflict resolution log
└── Error summary

Dashboard Refresh Triggers:
├── New signal processed
├── System status change
├── Error occurrence
├── MT4 feedback received
├── System freeze/unfreeze
└── Timer-based refresh (15 seconds)
```

## Key System Benefits

### Simplified Design
- **Single Parameter Set**: No complex parameter selection logic
- **Simple Conflicts**: Drop second signal, no queueing
- **Clear Freeze Logic**: 3 failures = freeze, manual recovery
- **Binary Decisions**: Accept/reject, success/failure

### Robust Error Handling
- **Multi-tier validation** with clear failure points
- **Transactional exports** prevent partial writes
- **Timeout monitoring** with reasonable thresholds
- **Automatic freeze protection** prevents runaway failures

### Complete Traceability
- **Full signal lifecycle** tracking from creation to completion
- **Comprehensive logging** at each process step
- **Audit trail** for all decisions and actions
- **Performance metrics** for system optimization

## Current Implementation Status

### Completed Design Elements
✅ Signal processing pipeline architecture
✅ Multi-tier validation framework
✅ Conflict detection and resolution logic
✅ Error handling and system protection
✅ MT4 integration feedback loops
✅ System state management

### Ready for Implementation
🔄 Module-by-module VBA coding
🔄 Dashboard integration
🔄 Testing framework setup
🔄 MT4 EA communication protocols
🔄 Error logging infrastructure

### Future Enhancements
⏳ Performance-based parameter adjustment
⏳ Advanced conflict resolution strategies
⏳ Real-time system health monitoring
⏳ Automated system recovery procedures