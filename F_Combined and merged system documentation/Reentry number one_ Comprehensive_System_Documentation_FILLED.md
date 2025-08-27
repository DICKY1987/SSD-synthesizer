# 📘 Comprehensive System Documentation (Filled from Reentry Trading System Docs)

## 1.0 System Overview & Architecture
**1.1 Purpose and Scope**  
Provide a **single, machine- and human-readable spec** for a reentry-based trading system that Python, MT4 Expert Advisor (EA), and UI must obey. Normative scope: executable parameter schema, CSV message contracts, matrix ID grammar, EA validation checklist, invariants, and test cues【10†source】【11†source】.  

**1.2 Architectural Diagrams (C4, component, network)**  
Not provided.  

**1.3 Data Flow Diagrams (DFDs)**  
Not provided.  

**1.4 Stakeholders & Responsibilities**  
Actors:  
- **PY (Python):** Ingests calendar, generates signals, parameter sets, writes to CSV.  
- **EA (Expert Advisor):** Validates, executes orders, applies SL/TP/reentry logic, emits responses.  
- **BR (CSV Bridge):** Filesystem-based transport.  
- **FS (Filesystem):** Atomic write/rename, log management【11†source】.  

**1.5 Trading Philosophy & Strategic Approach**  
- **Fusion strategy:** Combines **anticipation signals** (1hr/8hr before economic events) with **reentry logic** (O → R1 → R2).  
- **Outcome-driven:** Each leg classified (WIN, LOSS, BE, etc.) and drives next-generation mapping.  
- **Constraint-first:** Interfaces and validation rules are strict; strategy logic itself is not prescribed【10†source】【11†source】.  

---

## 2.0 Data Models & Persistence
**2.1 Logical Data Model**  
Entities:  
- `parameter_set_id` (PS-...)  
- `combination_id` (generation:signal:duration:proximity:outcome)  
- CSV payload rows (`trading_signals.csv`, `trade_responses.csv`, `parameter_log.csv`)【10†source】.  

**2.2 Physical Database Schema**  
Not provided (CSV-only transport).  

**2.3 State Management & Persistence Rules**  
- Python maintains in-memory calendar index, offsets, and chain state.  
- EA persists last-known-good parameter set on schema validation failures【11†source】.  

**2.4 Data Retention & Archival Policies**  
- CSV logs rotated daily or >100MB.  
- Archives purged after ~30 days【11†source】.  

**2.5 Terminal-Specific Persistence Mechanisms**  
- EA logs to `parameter_log.csv`.  
- No MT4 global vars used; persistence is file-based【10†source】【11†source】.  

---

## 3.0 Interfaces & APIs
**3.1 API Specifications**  
CSV-only transport between Python and EA.  

**3.2 Detailed Endpoint Contracts**  
- `trading_signals.csv`: UPDATE_PARAMS, TRADE_SIGNAL, CANCEL_PENDING, HEARTBEAT.  
- `trade_responses.csv`: ACK_UPDATE, ACK_TRADE, REJECT_SET, REJECT_TRADE, CANCELLED, HEARTBEAT【10†source】.  

**3.3 Function-Level Contracts**  
- Python validates parameters against `parameters.schema.json`.  
- EA mirrors schema validation locally【10†source】【11†source】.  

**3.4 Integration Points**  
Economic calendar ingestion (`economic_calendar*.csv`/`.xlsx` from Downloads)【11†source】.  

**3.5 Communication Contracts (Runtime Bridges)**  
- CSV append-only, atomic write (tmp→rename).  
- SHA-256 checksum for payload integrity.  
- Heartbeats every 30s, timeout escalation after 90s.  
- Retry/backoff for file locks【10†source】【11†source】.  

**3.6 Signal Queueing & Ordering Guarantees**  
- Duplicate suppression (debounce).  
- Strict chronological ordering of anticipation/events.  
- Reentry capped at R2【10†source】【11†source】.  

**3.7 Legacy Integration Modules**  
Not applicable (no sockets, no DLLs).  

---

## 4.0 Core Logic & Behavior
**4.1 Business Logic & Algorithms**  
- Signals derived from economic calendar + injected anticipation rows.  
- Combination ID grammar ensures deterministic routing.  
- EA enforces SL/TP, ATR, and risk rules【10†source】【11†source】.  

**4.2 Error Handling & Exception Strategy**  
- Schema failures → REJECT_SET.  
- Trade send failures → retries, then REJECT_TRADE.  
- Partial CSV lines skipped, no crash.  
- Fallback: switch to failsafe parameter set or escalate【11†source】.  

**4.3 Edge Case Specifications**  
- Risk >3.50% rejected (E1001).  
- TP ≤ SL rejected (E1012).  
- ATR periods outside [5,200] rejected (E1020).  
- Pending timeout <1 clamped (W2003).  
- R3 generation disallowed (E1030)【10†source】【11†source】.  

**4.4 Embedded Annotations**  
Not provided.  

**4.5 Safety Controls**  
- Effective risk enforced (`min(global_risk_percent × risk_multiplier, 3.50)`).  
- Eco cutoff windows enforced (`eco_cutoff_minutes_before/after`).  
- Last-known-good params preserved if validation fails【10†source】【11†source】.  

**4.6 Adaptive Reentry Logic**  
- Chain: O → R1 → R2 → terminal.  
- Duration categories: FLASH, QUICK, LONG, EXTENDED.  
- Outcomes feed next-generation mapping.  
- Logging of reentry decisions in CSVs【10†source】【11†source】.  

---

## 5.0 Deployment & Operations
**5.1 Infrastructure & Environment Requirements**  
- Windows, MT4 terminal, Python runtime.  
- Filesystem paths: `Common\Files\reentry\...`【10†source】.  

**5.2 Dependency Specifications**  
Not specified.  

**5.3 Configuration & Secrets Management**  
- Config files: `parameters.schema.json`, `matrix_map.csv`.  
- Parameters in YAML/JSON schema【10†source】【11†source】.  

**5.4 Build & Deployment Process**  
- Schema auto-generated from YAML to JSON.  
- Python builds `json_payload` per trade request.  
- EA validates version compatibility (must be "3.0")【10†source】.  

**5.5 Operational Runbooks & Process Orchestration**  
- Heartbeat monitoring.  
- Log rotation.  
- Error escalation to notification channel【11†source】.  

**5.6 Broker/Terminal Failover SOP**  
Not specified.  

**5.7 Observability & SLOs**  
- SLA matrix: step-level timing requirements (e.g., schema load ≤500ms, EA poll ≤5s).  
- Latency budgets for critical paths【11†source】.  

---

## 6.0 Non-Functional Requirements (NFRs)
**6.1 Performance**  
- CSV append latency ≤50ms.  
- EA poll detection ≤5s.  
- Broker order latency targets: MARKET ≤500ms, STRADDLE ≤800ms【11†source】.  

**6.2 Scalability**  
Not specified.  

**6.3 Availability & Reliability**  
- Heartbeat echo required every 90s.  
- Recovery from degraded schema state supported【11†source】.  

**6.4 Auditing & Logging**  
- `parameter_log.csv` echoes parameters.  
- `trade_responses.csv` logs all rejections/errors.  
- Daily rotation with compression【10†source】【11†source】.  

**6.5 Deterministic Replay & Time Sync**  
- UTC ISO-8601 timestamps.  
- Replay supported via archived CSVs【10†source】.  

**6.6 Immutable Audit Logging**  
- Append-only CSV; never modified in place.  
- SHA-256 integrity checks【10†source】.  

**6.7 Temporal/Regional Handling**  
- Local time conversion for economic calendar ingestion.  
- Normalized to UTC internally【11†source】.  

---

## 7.0 Security Specifications
Not specified.  

---

## 8.0 Model Governance (for AI/Trading Systems)
Not specified.  

---

## 9.0 Requirements Traceability (RTM Layer)
Partially derivable from validation rules and error codes, but explicit RTM table not provided.  

---

## 10.0 Cross-View Linking
Combination IDs and parameter sets link logic, configs, and CSV records【10†source】【11†source】.  

---

## 11.0 Export Strategy
- CSV schemas and SLA matrix provide developer and ops views.  
- Glossary defines key terms like *Effective risk* and *Combination ID*【10†source】.  
