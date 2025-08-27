# Multi-EA Signal Execution System with Reentry and Optimization

## 1. Project Overview

This project defines a modular, multi-currency trading system built on a 30-EA MT4 architecture, enhanced with Python-based signal analytics, SQLite state tracking, robust reentry logic, and hierarchical bridge communication. It supports real-time signal execution, event-driven orchestration, and adaptive reentry optimization.

---

## 2. Architecture and Directory Layout

```
TradingSystem/
├── MT4/
│   ├── Experts/               # 30 per-pair compiled EAs
│   ├── Include/               # Shared MQL4 libraries (Core, Bridge, Reentry)
│   └── Files/                 # Signal input, response output, pair configs
├── Python/
│   ├── services/              # Core analytics, signal generation, orchestration
│   ├── data/                  # Market data, logs, signals
│   ├── config/                # Per-pair YAML + global master config
├── Database/                 # SQLite database for tracking + analytics
└── PowerShell/               # Deployment and monitoring scripts
```

---

## 3. MT4 EA Template Overview

Each EA is compiled with:
- `TRADING_PAIR`, `CONFIG_FILE`, `SIGNAL_FILE`, `RESPONSE_FILE`
- Core engine `CTradingEACore`
- Communication `CBridgeInterface`
- Optional: `CReentryLogic`

**Reentry Parameters:**
```mql4
input bool ENABLE_REENTRY_SYSTEM = true;
input int REENTRY_DELAY_SECONDS = 30;
input string REENTRY_CONFIG_FILE = "EURUSD_reentry.csv";
```

---

## 4. Signal Generation and Analytics

Python ML service handles signal generation with:
- Random Forest, SVM, Neural Net ensemble
- CNN chart recognition
- RCI system + economic calendar integration
- SHAP explainability, Monte Carlo simulation
- Event triggers: 0.1 pip moves, high-confidence patterns

**Output:** UUID-based `SignalModel` objects with strategy ID, confidence, explanation, state.

---

## 5. Reentry Logic

### 5.1 Decision Logic
```mql4
// Mapped as:
// 1 = SL, 2 = Partial Loss, 3 = Breakeven, 4 = Partial TP, 5 = TP, 6 = Beyond TP
```

### 5.2 Config Files
CSV: `EURUSD_reentry.csv`, `EURUSD_reentry_conservative.csv`, etc.
```
Action,Type,SizeMultiplier,DelaySeconds,ConfidenceAdjustment,Parameters
1,NO_REENTRY,0.0,0,1.0,"Stop loss - no reentry"
...
```

---

## 6. SQLite Data Layer

Schema includes:
- `ticks`, `orders`, `bridge_logs`, `margin_snapshots`
- `reentry_chains_<pair>` and `reentry_performance_<pair>`

Supports analytics for reentry performance, chain stats, optimization.

---

## 7. Reentry Python Integration

`ReentryAnalytics`:
- Analyze action performance: P&L, Sharpe, win rate
- Track and score reentry chains
- Optimize parameters (e.g., lot size, delay)

---

## 8. Resilience & Fault Tolerance

- Circuit breaker on bridges (3-tier fallback: DLL, NamedPipe, File)
- Graceful degradation strategies (e.g., use cached data)
- Retry policies and state fallback handling

---

## 9. Performance Optimization

- Adaptive batching based on system metrics
- Resource thresholds (CPU, memory)
- Smart EA load throttling during overloads

---

## 10. Testing & Simulation

- Full isolation simulation framework
- Simulation DB, mocked MT4 bridge
- Data replay, validation, risk-free test runs

---

## 11. Security & Audit

- JWT-authenticated APIs with role-based access
- Security audit logs (IP, agent, user ID)
- Session expiration, token refresh, and forensic replay

---

## 12. Deployment Notes

- `Deploy_All_EAs.ps1`: compiles + copies 30 EAs
- Python services run via supervisor or systemd
- Reentry and signal analytics log separately per pair

---

## 13. Excel Dashboard

- Sheet: `ReentryOverview` and `ActionMatrix`
- Fetches reentry metrics from Python via API
- Color-coded P&L, status tags (e.g., OPTIMAL, NEEDS_OPTIMIZATION)

---

## 14. Bridge Architecture

1. **DLL Socket** – primary, <10ms, persistent TCP
2. **Named Pipe** – fallback, <50ms, memory-speed
3. **File-Based** – fallback, <500ms, batch-based

---

## 15. Lifecycle Coordination

- Signal state tracked via UUID through lifecycle (generated, executed, closed)
- Lifecycle reconciler handles orphans, sync issues hourly

---

## 16. Plugin System

- Formal `PluginInterface` for external validators
- Timeouts: 1s (indicators), 5s (signals)
- Memory sandboxing (512MB)

---

## 17. Final Notes

This document serves as the full specification for implementing and maintaining a scalable, explainable, reentry-enabled trading system. All development and execution decisions should conform to the contracts, architecture, and design standards herein.
