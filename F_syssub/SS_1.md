HUEY_P Trading System — Architecture and Subsystem Specification (SRS Supplemental)
1. Introduction
1.1 Purpose

This document supplements the HUEY_P Trading System – Process and Sub-Process Identification by expanding subsystem coverage using additional reference materials. It establishes a complete, layered architectural map with traceability between system components, subsystems, modules, and parameters.

1.2 Scope

The trading system automates economic-event-driven strategies across MetaTrader 4 (MT4). It integrates Python analytics, VBA/Excel pre-processing, MQL4 Expert Advisors, socket/CSV bridges, and SQL/CSV persistence, supporting real-time execution, reentry logic, and system health monitoring.

1.3 Definitions, Acronyms, Abbreviations

EA: Expert Advisor (MetaTrader 4 trading module)

CSV Bridge: File-based communication layer for redundancy

DLL Socket: Dynamic Link Library enabling MT4↔Python sockets

Reentry Matrix: Multi-dimensional outcome-based reentry configuration

Anticipation Events: Synthetic triggers before high-impact news releases

1.4 References

Process & Sub-Process Identification

Parameter Categorization

Atomic Process Flow Reentry System v3

Communication Reference

1.5 Overview

This SRS decomposes the architecture into systems, subsystems, components, and modules, mapped by functional role, dependencies, and traceable source references.

2. Overall Description
2.1 Product Perspective

The HUEY_P system is a multi-layer distributed architecture:

Data Sources: Economic calendar CSV/XLSX, market session events

Processing: Python pipelines, Excel/VBA preprocessing

Communication: Primary DLL/socket bridge; fallback CSV

Execution: MQL4 EAs with reentry state machines

Persistence: SQL trade logs, CSV/YAML configs

Monitoring: System health, latency, backup/archival

2.2 Product Functions

Import, normalize, and filter economic events

Generate trading signals from fundamental + technical inputs

Map signals to parameter sets via reentry matrix

Validate and transmit parameters to EAs (socket or CSV)

Execute trades, apply straddle logic, manage reentry

Persist trades, logs, and configs

Monitor health, failover communication bridges

2.3 User Characteristics

Intended for professional algorithmic traders with MT4 familiarity

Operators require skills in risk management, system monitoring, and EA deployment

2.4 Constraints

MT4 environment limitations (no native sockets without DLLs)

Risk cap enforcement ≤ 3.5% per trade

Governance rules enforce stop loss and risk bounds

2.5 Assumptions and Dependencies

Economic calendar files consistently available weekly

Broker permits straddle/pending orders within slippage tolerances

System health requires socket or CSV bridge availability

3. Specific Requirements
3.1 Functional Requirements
3.1.1 Economic Calendar Processing

Import CSV/XLSX → normalize columns → filter HIGH/MED events

Inject anticipation events (1h, 8h)

Append market session opens (Tokyo, London, NY)

3.1.2 Signal Generation and Validation

Merge calendar triggers, technical indicators, external JSON signals

Debounce duplicates; classify proximity buckets

Score signal quality, enforce blackout filters

3.1.3 Parameter Resolution and Governance

Map signals to parameter_set_id using matrix_map.csv

Enforce EA-side schema validation (parameters.schema.json)

Govern parameters (risk%, SL/TP, max trades)

3.1.4 Communication Bridge Management

Primary: DLL/socket (1–5 ms latency)

Backup: CSV polling (2–5 s)

Failover orchestration within 30 s; recovery with validation

3.1.5 Trade Execution (EA)

Manage state machine (IDLE→ORDERS→TRIGGERED→CLOSED)

Support order types: MARKET, PENDING, STRADDLE

Apply reentry multipliers, straddle cancelation, trailing stops

3.1.6 Reentry Matrix Processing

Classify outcomes: FULL_SL, BE, PARTIAL_TP, FULL_TP

Build combination_id with context + duration

Lookup matrix → determine action, size multiplier, delays

3.1.7 Data Persistence and Backup

SQL + CSV trade logging

YAML/CSV configuration loading with overrides

7-year trade retention compliance

3.1.8 System Monitoring

Health checks: EA heartbeats (30 s), service freshness (2 min)

Latency targets: < 100 ms signal, < 200 ms execution

Alert escalation + preventive maintenance detection

3.1.9 Configuration & Profile Management

Hierarchical YAML + CSV loading

Hot reload detection and propagation

Profiles: conservative/moderate/aggressive; ECO vs non-ECO

3.1.10 Reporting & Analytics

Performance dashboards (win rates, Sharpe ratios, matrix analysis)

Operational efficiency metrics (failover, latency, utilization)

3.2 Performance Requirements

Socket latency ≤ 10 ms

CSV polling ≤ 5 s

Execution latency ≤ 200 ms p99

Risk enforcement ≤ 3.5% trade exposure

3.3 Design Constraints

File operations must be atomic (write→fsync→rename)

Schema validation is mandatory pre-execution

Parameters restricted by governance_checklist.csv

EA must support fallback to CSV when socket unavailable

Traceability & Coverage

Expanded from manual: Reentry atomic flow (matrix resolution, file rotation, heartbeat)

Additional subsystems: Parameter governance (risk/SL enforcement)

Not in baseline doc: Explicit socket/CSV channel design

Manual-only content: High-level monitoring and performance reports

✅ Completeness Check:
All systems and subsystems from baseline + supplemental docs are represented. New subsystems include parameter governance, reentry atomic steps, socket/CSV communication architecture, and schema enforcement.