# 📘 Comprehensive System Documentation (Filled from 3 source docs)

> Source docs used: `4D Matrix.md`, `most_acurate_matirx_doc.md`, `multidimensionalreentrydecisionsysteminPython.md`  
> NOTE: Only information explicitly present in the three docs was used. Any field with no explicit source remains blank.

## 1.0 System Overview & Architecture

### 1.1 Purpose and Scope
A production-ready, scalable *reentry decision* subsystem for trading that implements a **reduced 4D matrix** with conditional duration logic. The v3.0 design fixes the combination space at **652 combinations per symbol** and enforces a **hard stop after R2** reentry generation. The system replaces broad “market context” with **Future Event Proximity** buckets and adds regional/temporal specificity for signals.

### 1.2 Architectural Diagrams (C4, component, network)
<!-- blank -->

### 1.3 Data Flow Diagrams (DFDs)
<!-- blank -->

### 1.4 Stakeholders & Responsibilities
<!-- blank -->

### 1.5 Trading Philosophy & Strategic Approach
- **Deterministic, static, rule-based** approach that can be modified based on performance analysis.  
- **Safety-first near scheduled events**: conservative behavior in *IMMEDIATE* proximity and **no reentry during news window after a loss**.  
- **Bounded reentry**: strict **R2** (two-generation) limit to prevent runaway chains.  
- **Fusion strategy**: combines event-driven (ECO_HIGH/ECO_MED), anticipation timing (1HR/8HR), regional equity opens (Asia/Europe/USA), and technical signals under one matrix.

---

## 2.0 Data Models & Persistence

### 2.1 Logical Data Model (entities, attributes, relationships)
- **ReentryMatrix**  
  - Dimensions (reduced 4D): *Signal Type* × *Reentry Duration (conditional)* × *Outcome* × *Future Event Proximity*.
  - Signals (canonical): `ECO_HIGH`, `ECO_MED`, `ANTICIPATION_1HR`, `ANTICIPATION_8HR`, `EQUITY_OPEN_ASIA`, `EQUITY_OPEN_EUROPE`, `EQUITY_OPEN_USA`, `ALL_INDICATORS`.
  - Reentry durations: `FLASH`, `QUICK`, `LONG`, `EXTENDED` (applies **only** to ECO_HIGH/ECO_MED); others use `NO_DURATION`.
  - Outcomes: `1..6` = `FULL_SL`, `PARTIAL_LOSS`, `BREAKEVEN`, `PARTIAL_PROFIT`, `FULL_TP`, `BEYOND_TP`.
  - Future Event Proximity: `IMMEDIATE`, `SHORT`, `LONG`, `EXTENDED`.

- **MatrixCell** (default/assigned values per coordinate)  
  Fields (as defined across rule implementations & tracking):  
  `parameter_set_id`, `action_type`, `size_multiplier`, `confidence_adjustment`, `delay_minutes`, `max_attempts`, `conditions`, performance fields (`total_executions`, `successful_executions`, `total_pnl`, `last_execution`), user fields (`user_override`, `notes`, `created_date`, `modified_date`).

- **MatrixDataManager**  
  Responsibilities: save/load **versioned** matrix JSON per symbol; maintain `current_matrix.json` symlink; enumerate versions with metadata (`version`, `created_date`, `total_cells`, `user_overrides`).

- **MatrixPerformanceTracker**  
  Tracks executions per matrix coordinate; maintains in‑memory DB with periodic persistence; exposes summary stats (e.g., `total_executions`, `successful_executions`, `total_pnl`, `best_pnl`, `worst_pnl`, `avg_duration_minutes`, `last_execution`).

### 2.2 Physical Database Schema (tables, types, constraints)
- **Filesystem layout (per symbol)** under `reentry_matrices/`  
  `current_matrix.json`, `matrix_v*.json`, `performance_history.csv`.

- **SQL (Entry Order Tracking / Straddle support)**  
  A `straddle_executions` table with columns including `straddle_id`, `symbol`, `combination_id`, `buy_ticket`, `sell_ticket`, prices/lots, which leg filled, timestamps, and `auto_cancel_success`.

### 2.3 State Management & Persistence Rules (sessions, caches, lifecycles)
- Saving a matrix writes a **versioned** JSON with metadata and updates `current_matrix.json` to point at the chosen version.  
- Loading may target an explicit version (`matrix_v{version}.json`) or `current_matrix.json`; missing files raise `FileNotFoundError`.  
- Version listing aggregates metadata from all `matrix_v*.json` files.  
- Performance tracker uses an **in‑memory** store with a cache and supports periodic persistence/summary recompute.

### 2.4 Data Retention & Archival Policies (compliance, cleanup, backups)
<!-- blank -->

### 2.5 Terminal-Specific Persistence Mechanisms
<!-- blank -->

---

## 3.0 Interfaces & APIs

### 3.1 API Specifications (REST, gRPC, design principles)
<!-- blank -->

### 3.2 Detailed Endpoint Contracts (inputs, outputs, permissions)
<!-- blank -->

### 3.3 Function-Level Contracts (internal libraries/modules)
- **DefaultRuleEngine.get_default_cell(signal_type, duration/time_cat, outcome, proximity/context, generation)** → returns `MatrixCell` using priority rules and conservative fallback.  
  High‑priority rules include *future proximity/news window*, *flash move (duration-gated)*, *regional equity*, *anticipation timing*, and *generation limit*.

- **MatrixDataManager.save_matrix(symbol, matrix, version=None)** → writes versioned JSON + `current_matrix.json` symlink; returns effective version.  
  **load_matrix(symbol, version=None)** → loads from explicit or `current_matrix.json`.  
  **list_versions(symbol)** → returns metadata list.

- **MatrixPerformanceTracker.record_reentry_result(matrix_coordinates, trade_result)** → appends execution and updates summary stats.  
  **get_cell_performance(matrix_coordinates)** → returns comprehensive performance record (with cache).

### 3.4 Integration Points (external APIs/services consumed)
<!-- blank -->

### 3.5 Communication Contracts (Runtime Bridges)
<!-- blank -->

### 3.6 Signal Queueing & Ordering Guarantees
<!-- blank -->

### 3.7 Legacy Integration Modules
<!-- blank -->

---

## 4.0 Core Logic & Behavior

### 4.1 Business Logic & Algorithms (descriptions/pseudocode)
- **Rule priorities (reduced v3.0):**  
  1) Future event proximity / news‑window safety  
  2) Flash‑move duration rules (only for ECO signals)  
  3) Regional equity open rules (USA/Europe/Asia)  
  4) Anticipation timing (1HR vs 8HR)  
  5) Generation limit (stop at R2)  
  6) Conservative fallback (`parameter_set_id=1`, `NO_REENTRY`, reduced size, delay)

### 4.2 Error Handling & Exception Strategy (error catalog, logging, recovery)
<!-- blank -->

### 4.3 Edge Case Specifications (invalid inputs, boundaries)
<!-- blank -->

### 4.4 Embedded Annotations (Code Comment Layer for devs)
<!-- blank -->

### 4.5 Safety Controls
- **Max generations:** stop after **R2**.  
- **Event proximity safety:** conservative behavior when proximity is `IMMEDIATE`.  
- **News‑window safety:** **no reentry after loss** during news window.

### 4.6 Adaptive Reentry Logic
- Outcome classification: integers **1..6** mapping to `FULL_SL` … `BEYOND_TP`.  
- Duration gating: `FLASH/QUICK/LONG/EXTENDED` apply **only** to ECO_HIGH/ECO_MED; other signals use `NO_DURATION`.  
- Parameter‑set selection via rules (e.g., IDs 1/2/6/7/8/9 in examples) and performance‑based recommendations.

---

## 5.0 Deployment & Operations

### 5.1 Infrastructure & Environment Requirements (runtime, hardware, cloud)
<!-- blank -->

### 5.2 Dependency Specifications (libraries, frameworks, versions)
- Python standard library modules explicitly shown: `dataclasses`, `typing`, `datetime`, `json`, `pathlib`, `time`.

### 5.3 Configuration & Secrets Management
<!-- blank -->

### 5.3.1 Multi-Format Configuration & Profile Management
<!-- blank -->

### 5.4 Build & Deployment Process (CI/CD steps, rollback strategy)
<!-- blank -->

### 5.4.1 Release Gates (Trading)
<!-- blank -->

### 5.5 Operational Runbooks & Process Orchestration (jobs, retries, recovery)
<!-- blank -->

### 5.6 Broker/Terminal Failover SOP
<!-- blank -->

### 5.7 Observability & SLOs
- **Metrics catalog (from performance tracker):** `total_executions`, `successful_executions`, `total_pnl`, `best_pnl`, `worst_pnl`, `avg_duration_minutes`, `last_execution`.
- **Alerting heuristics (examples in optimizer):** flag on **win rate < 40%**, **profit factor < 1.0**, **max consecutive losses > 5**; suggest reducing size, increasing delay, or switching to `NO_REENTRY` as appropriate.

### 5.7.1 Trading Analytics & Performance Dashboards
- Reentry performance reporting supported by per‑cell histories and summary stats.

---

## 6.0 Non-Functional Requirements (NFRs)

### 6.1 Performance (response times, throughput, latency budgets)
<!-- blank -->

### 6.2 Scalability (growth in users, data, transaction volume)
<!-- blank -->

### 6.3 Availability & Reliability (uptime targets, DR strategy)
<!-- blank -->

### 6.4 Auditing & Logging (security, compliance, debugging)
<!-- blank -->

### 6.5 Deterministic Replay & Time Sync
<!-- blank -->

### 6.6 Immutable Audit Logging
<!-- blank -->

### 6.7 Temporal/Regional Handling
- Regional variants (`EQUITY_OPEN_ASIA`, `EQUITY_OPEN_EUROPE`, `EQUITY_OPEN_USA`) and anticipation timing (`ANTICIPATION_1HR`, `ANTICIPATION_8HR`) are explicitly modeled in the signal space.

---

## 7.0 Security Specifications
<!-- blank -->

---

## 8.0 Model Governance (for AI/Trading Systems)
- **No ML models** are specified here; logic is **static rule-based**.

---

## 9.0 Requirements Traceability (RTM Layer)
<!-- blank -->

---

## 10.0 Cross-View Linking
<!-- blank -->

---

## 11.0 Export Strategy
<!-- blank -->
