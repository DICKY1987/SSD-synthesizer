# Software Requirements Specification (SRS) — Performance, Scalability, and Test/Validation Subsystems of the Trading Platform

> **Scope of this SRS:** This document consolidates and structures the **Performance Optimization & Scalability** subsystem and the **Testing & Validation Framework** subsystem drawn from the provided artifacts (Sections “U_8 Remediated Performance Optimization and Scalability” and “U_9 Remediated Testing and Validation Framework”). Where other platform layers are referenced (e.g., MT4 bridges, simulation data, market data providers), they are captured to the extent they appear in the provided materials; gaps are explicitly called out.

---

## 1. Introduction

### 1.1 Purpose
This SRS defines the **architectural decomposition** and **specific requirements** for:
- The **Performance Optimization & Scalability** subsystem (resource management, batching, memory, database pooling).
- The **Testing & Validation Framework** subsystem (simulation isolation, mock interfaces, bridge testing and failover).  
It formalizes responsibilities, dependencies, constraints, and traceability to the provided source documents.

### 1.2 Scope
The scope covers platform-internal services that:
- Monitor and dynamically tune compute and memory utilization, batching behavior, and DB connectivity.
- Provide a **fully isolated** simulation mode with mock interfaces and automated bridge validation/failover testing.

### 1.3 Definitions, Acronyms, Abbreviations
- **MT4**: MetaTrader 4 execution environment.
- **Bridge**: Communication mechanism between analysis layer and MT4 (e.g., `dll_socket`, `named_pipes`, `file_based`).
- **Simulation Mode**: Execution context where live systems are isolated and mocked.
- **Adaptive Batching**: Dynamic batch-size adjustment based on performance feedback.

### 1.4 References
- **U_8 Remediated Performance Optimization and Scalability** (Section 8): SmartResourceManager, AdaptiveBatchManager, MemoryManager, DatabaseConnectionPool.
- **U_9 Remediated Testing and Validation Framework** (Section 9): SimulationFramework, Mock interfaces, BridgeTestSuite, ComprehensiveBridgeTestSuite (connectivity, latency, failover, recovery).

### 1.5 Overview
Section 2 provides overall description and layered architecture; Section 3 specifies functional, performance, and design constraints with traceability. Relationship mapping and completeness checks are embedded throughout.

---

## 2. Overall Description

### 2.1 Product Perspective
These subsystems plug into a broader trading platform that includes data ingestion, analytics, MT4 execution, and persistence. They provide **cross-cutting** capabilities:
- Runtime resource governance and throughput optimization.
- Safe, isolated testing + automated communication-bridge validation.

### 2.2 Product Functions (High Level)
- **Resource Management**: Monitor CPU/memory; tune batch sizes; throttle background work.
- **Memory Governance**: Warning/critical thresholds; cache cleanup; GC triggers; alerting.
- **DB Connectivity**: Pooled connections; health checks; idle cleanup; min/max pool size.
- **Simulation Isolation**: Separate DB/files; mock MT4, market data, calendar; live-access validation.
- **Bridge Testing**: Connectivity, latency, failover from primary to tertiary; recovery & promotion.

### 2.3 User Characteristics
- **Developers/QA**: Configure thresholds, run simulation suites, analyze reports.  
- **SRE/Ops**: Monitor alerts, tune resource limits, oversee DB pool sizing.  

### 2.4 Constraints
- Resource thresholds (e.g., CPU ≥80% and Memory ≥90% trigger actions).
- Simulation must **not** access live DBs/paths/endpoints; violations fail validation.
- Bridge latency expectations: dll_socket <10 ms avg; named_pipes <50 ms; file_based <500 ms.

### 2.5 Assumptions and Dependencies
- **Assumes** availability of bridge manager and health monitor used by test suites.
- **Depends** on alerting/logging services for memory/validation events.
- **Depends** on mock providers and isolated filesystem/DB for simulation.

---

## 3. Specific Requirements

### 3.1 Functional Requirements

#### 3.1.1 Architectural Decomposition (Systems → Subsystems → Components → Modules)

##### A. System: Performance Optimization & Scalability
- **Subsystem A1: Smart Resource Management**
  - **Component A1.1: SmartResourceManager**
    - *Role*: Monitors system metrics; adjusts batching; reduces background load at thresholds.
    - *Dependencies*: System metrics provider; AdaptiveBatchManager; background workers.
  - **Component A1.2: AdaptiveBatchManager**
    - *Role*: Maintains current batch size; adjusts based on avg processing time; records metrics.
    - *Modules*: `adjust_batch_size_based_on_performance`, `process_adaptive_batch`, `split_into_batches`, `process_single_batch`.
    - *Dependencies*: PerformanceHistory logger; time measurement.
- **Subsystem A2: Memory Governance**
  - **Component A2.1: MemoryManager**
    - *Role*: Monitors memory usage; warning/critical handling; cache cleanup; GC; batch-size reduction; alerts.
    - *Modules*: `monitor_memory_usage`, `handle_warning_memory_usage`, `handle_critical_memory_usage`.
    - *Dependencies*: Cache managers; adaptive batching; alert service; GC.
- **Subsystem A3: Database Connection Optimization**
  - **Component A3.1: DatabaseConnectionPool**
    - *Role*: Min/max pool; health-check; acquire/return; idle cleanup; replacement on failure.
    - *Modules*: `get_connection`, `return_connection`, `validate_connection_health`, `cleanup_idle_connections`, `initialize_pool`.
    - *Dependencies*: DB driver; timeouts; metrics collector.

##### B. System: Testing & Validation Framework
- **Subsystem B1: Simulation Mode & Isolation**
  - **Component B1.1: SimulationFramework**
    - *Role*: Enforces simulation-only execution; sets up isolated DB, file paths; initializes mocks; validates no live access.
    - *Modules*: `initialize_simulation_environment`, `create_simulation_database`, `setup_simulation_file_paths`, `initialize_mock_interfaces`, `validate_no_live_system_access`.
    - *Dependencies*: Config (`is_simulation_mode`), sqlite, filesystem, network sockets.
  - **Component B1.2: Mock Interfaces**
    - *Modules*: `MockMT4Interface`, `MockMarketDataProvider`, `MockEconomicCalendar` (load test data and historical series).
    - *Dependencies*: Historical market data, test events.
  - **Component B1.3: Simulation Persistence**
    - *Role*: `simulation_trading.db` with `sim_signals`, `sim_trades`, `sim_market_data` tables; backup/rotate on re-init.
- **Subsystem B2: Bridge Validation & Reliability**
  - **Component B2.1: BridgeTestSuite**
    - *Role*: Validates failover from primary (`dll_socket`) → secondary (`named_pipes`) → tertiary (`file_based`) and back to primary on recovery.
  - **Component B2.2: ComprehensiveBridgeTestSuite**
    - *Role*: Runs end-to-end suite: connectivity, latency, failover, recovery, load, errors, concurrency. Uses `bridge_manager`, `bridge_health_monitor`.
    - *Modules*: `test_individual_bridge_connectivity`, `test_bridge_latency_performance`, `test_bridge_failover_sequence`, `test_bridge_recovery_procedures`, `test_bridge_load_handling`, `test_bridge_error_handling`, `test_bridge_concurrent_access`, `run_complete_bridge_test_suite`.

#### 3.1.2 Layered Decomposition (Cross-Referenced)
- **Data Sources**
  - Historical market data for simulation; test economic calendar events.
- **Data Processing (Excel/VBA, Python)**
  - *In scope here*: Python-based adaptive batching and performance logging. (No Excel/VBA in provided materials.)
- **Communication/Bridges (C++, sockets, pipes)**
  - Bridges under test: `dll_socket` (primary), `named_pipes` (secondary), `file_based` (tertiary).
- **Execution & Reentry (MQL4 EAs, logic systems)**
  - Execution represented via `MockMT4Interface` in simulation. (Actual EA/re-entry logic not detailed in provided materials.)
- **Persistence (SQL, CSV/YAML configs)**
  - `simulation_trading.db` schema (`sim_signals`, `sim_trades`, `sim_market_data`); DB pool for live/other contexts (class shown generally).
- **Configuration Management**
  - `is_simulation_mode` gate; directory scaffolding under `/simulation/data/…`.
- **Monitoring, Logging, Deployment**
  - Memory warnings/critical alerts; performance history; connection/health metrics; test-suite results.

#### 3.1.3 Relationship Mapping & Explicit Flows
- **Performance Control Loop**  
  *System metrics → SmartResourceManager → AdaptiveBatchManager → process batches → PerformanceHistory → adjust batch size (next iteration).*
- **Memory Protection Flow**  
  *MemoryManager monitors usage → (warning) cleanup/size reduction → (critical) aggressive cache clear + GC + batch reduction + alert.*
- **Simulation Isolation Flow**  
  *Config flag → init SimulationFramework → create isolated DB + dirs → init mocks (MT4, market data, calendar) → verify no live DB/files/net endpoints accessible → pass/fail gate.*
- **Bridge Failover & Recovery Flow**  
  *All bridges healthy → simulate primary failure → expect `named_pipes` → simulate secondary failure → expect `file_based` → restore primary → health successes → promotion back to `dll_socket`.*

#### 3.1.4 Detailed Functional Requirements (selected)

**A. Resource & Batching**
1) The system SHALL reduce background processing and/or increase batch size when CPU utilization exceeds 80%.  
2) The system SHALL shrink batch sizes when avg processing time per batch exceeds the defined slow threshold (e.g., >1000 ms).  
3) The system SHALL increase batch sizes when avg processing time per batch is <100 ms, up to a max.  

**B. Memory Management**
4) The system SHALL perform moderate cleanup at ≥80% memory and aggressive cleanup + GC at ≥90%, emitting alerts at critical.  

**C. Database Pooling**
5) The system SHALL maintain a connection pool with min/max bounds, validate health on checkout/return, and replace unhealthy connections; it SHALL clean up over-idle connections and replenish to minimum.  

**D. Simulation Isolation**
6) The system SHALL initialize an isolated SQLite database (`simulation_trading.db`) with `sim_signals`, `sim_trades`, `sim_market_data` schema; it SHALL back up any existing file on re-init.  
7) The system SHALL create `/simulation/data` directory trees (signals, market_data, logs, configs) and ensure no writes to known live paths.  
8) The system SHALL validate that live endpoints, live DBs, and live file paths are inaccessible in simulation; any access SHALL fail validation.  

**E. Mock Interfaces**
9) The system SHALL initialize mock MT4, market data (with historical loads), and calendar test events for simulation runs.  

**F. Bridge Testing**
10) The test suite SHALL verify per-bridge connectivity and response validity.  
11) The test suite SHALL measure average latency for each bridge and compare to thresholds (dll_socket <10 ms; named_pipes <50 ms; file_based <500 ms).  
12) The test suite SHALL simulate failures and verify automatic failover primary→secondary→tertiary and subsequent recovery/promote to primary after health successes.  

### 3.2 Performance Requirements
- **CPU/Memory Thresholds**: Action triggers at CPU ≥80% and Memory ≥80/90% (warn/critical).  
- **Batch Throughput Targets**: Batch size auto-tunes to keep avg batch processing near sub-second unless constrained by errors/backpressure.  
- **Bridge Latency Targets**: dll_socket avg <10 ms; named_pipes avg <50 ms; file_based avg <500 ms (accept/flag if exceeded).  
- **DB Pool Responsiveness**: Acquire with timeout; unhealthy connections not returned to pool; idle connections trimmed after max idle time.  

### 3.3 Design Constraints
- **Isolation Hardening**: Simulation MUST NOT access live DBs (`live_trading.db`), live directories (e.g., `C:\TradingLive\`, `/live/data/`), or live endpoints; detection → error.  
- **Health Validation**: DB connections validated via simple query (e.g., `SELECT 1`).  
- **Promotion Logic**: Bridge recovery requires successive health checks before promotion back to primary (suite sends multiple test signals post-restore).  

---

## 4. Traceability

- **From U_8 → Performance & Scalability**  
  Requirements 1–5, CPU/memory thresholds, adaptive batching logic, GC, alerting, and DB pool specifics trace to U_8.  
- **From U_9 → Testing & Validation**  
  Requirements 6–12, simulation DB/schema, directory isolation, mock interfaces, live access validation, and bridge suites/latency/failover/recovery trace to U_9.  

> **Additional constraints present in spec but not in a “manual”:**  
> - Explicit latency ceilings per bridge modality.  
> - Exact CPU/Memory thresholds driving actions and the specific corrective steps (GC, cache clear, batch reduction, alert).  

---

## 5. Relationship Mapping

**Hierarchical:**  
- Systems → Subsystems → Components/Modules as defined in §3.1.1.

**Sequential:**  
- *Perf-loop*: Metrics → ResourceManager → AdaptiveBatch → Work Execution → Metrics.  
- *Isolation*: Config → SimFramework → Isolated DB/FS → Mocks → Live-access validation.  
- *Failover*: Primary healthy → failure → auto-switch to secondary → failure → tertiary → restore + promotion back to primary after health streak.  

**Cross-cutting:**  
- Alerting/logging spans memory, performance, and simulation validation.  

**Example explicit flow present in artifacts:**  
- *Simulation calendar/market data (mocked) → Simulation DB tables → Communication Service → Bridge Manager → (dll_socket | named_pipes | file_based) → Mock MT4.*  

---

## 6. Layer-by-Layer Summary (Mapped to Provided Materials)

1) **Data Sources**: Historical ticks and test events for simulation.  
2) **Data Processing (Python)**: Adaptive batching; performance logging.  
3) **Communication/Bridges**: dll_socket (primary), named_pipes (secondary), file_based (tertiary).  
4) **Execution & Reentry**: MockMT4Interface for simulation (real EA/reentry not specified here).  
5) **Persistence**: `simulation_trading.db` schema; connection pooling concepts.  
6) **Configuration Management**: Simulation flag; isolated directories.  
7) **Monitoring/Logging/Deployment**: Alerts on memory; test results aggregation; connection/latency metrics.  

---

## 7. Completeness Check

- **Represented systems/subsystems from provided files:**  
  - Performance Optimization & Scalability → SmartResourceManager, AdaptiveBatchManager, MemoryManager, DatabaseConnectionPool. ✔️  
  - Testing & Validation → SimulationFramework (DB/files isolation + mocks), BridgeTestSuite, ComprehensiveBridgeTestSuite (connectivity/latency/failover/recovery). ✔️
- **Consolidation of duplicates:** None detected across the two inputs.
- **Gaps (not covered in provided materials):**  
  - Actual **live** data sources and ETL beyond simulation mocks.  
  - **MQL4 EA** internal execution & **re-entry logic** specifics.  
  - **Configuration** artifacts outside `is_simulation_mode`.  
  - **Operational deployment** pipelines (CI/CD), production monitoring dashboards.  
  These can be appended when corresponding documents are provided.

---

### Appendix A — Quick Index (Subsystem → Key Modules)

- **SmartResourceManager** → `optimize_processing_load`  
- **AdaptiveBatchManager** → `adjust_batch_size_based_on_performance`, `process_adaptive_batch`  
- **MemoryManager** → `monitor_memory_usage`, `handle_warning_memory_usage`, `handle_critical_memory_usage`  
- **DatabaseConnectionPool** → `get_connection`, `return_connection`, `validate_connection_health`, `cleanup_idle_connections`  
- **SimulationFramework** → `initialize_simulation_environment`, `create_simulation_database`, `setup_simulation_file_paths`, `initialize_mock_interfaces`, `validate_no_live_system_access`  
- **Bridge Suites** → `test_individual_bridge_connectivity`, `test_bridge_latency_performance`, `test_bridge_failover_sequence`, `run_complete_bridge_test_suite`  
