# Software Requirements Specification (SRS)

## 1. Introduction

### 1.1 Purpose
This SRS documents the architecture and requirements of the HUEY_P Trading System, providing a precise, traceable decomposition from systems → subsystems → components → modules. It consolidates and normalizes content from the remediated technical units provided by the author into an IEEE‑830–style artifact suitable for engineering, audit, and implementation.

### 1.2 Scope
The scope covers runtime orchestration, state management, security and access control, fault tolerance and resilience, performance and scalability, monitoring/alerting, configuration management, testing/validation, and simulation. Execution targets include Python services, Excel/VBA dashboards, MQL4 execution bridges, and persistence layers (databases and files).

### 1.3 Definitions, Acronyms, Abbreviations
- **Bridge**: Communication mechanism between Python services and MT4/EA (dll_socket, named_pipes, file_based).
- **Lifecycle**: State model for signals/trades (GENERATED → TRANSMITTED → ACKNOWLEDGED → EXECUTED → COMPLETED → ANALYZED).
- **Circuit Breaker**: Guard component that opens after repeated failures to prevent cascading faults.
- **RBAC**: Role‑Based Access Control.
- **SLO**: Service Level Objective.
- **TTL**: Time‑to‑Live (cache invalidation/retention parameter).
- **UUID**: Universally Unique Identifier for signals and entities.

### 1.4 References
- Unit 4: State Management & Persistence (Remediated)
- Unit 5: Master Orchestration Cycle (Remediated)
- Unit 6: Fault Tolerance & Resilience (Remediated)
- Unit 7: Security & Access Control (Remediated)
- Unit 8: Performance Optimization & Scalability (Remediated)
- Unit 9: Testing & Validation Framework (Remediated)

> Within sections below, each requirement lists its source Unit(s) to preserve traceability.

### 1.5 Overview
Section 2 provides the overall system description and layered decomposition. Section 3 enumerates functional, performance, and design constraints as testable requirements. Appendices provide the decomposition catalog and a traceability matrix.

---

## 2. Overall Description

### 2.1 Product Perspective
The system is a multi‑service trading platform with:
- Event‑driven processing for market data, signals, alerts, lifecycle operations (Unit 5).
- Multiple communication bridges to MT4/EA with hierarchical failover (Unit 6, Unit 5).
- Strong state persistence & recovery with atomic transactions and checkpoints (Unit 4).
- RBAC security with JWT‑based authentication and comprehensive audit trails (Unit 7).
- Performance governance via adaptive batching, resource management, and DB pooling (Unit 8).
- Excel/VBA dashboards as operational interfaces (Unit 5).
- Full simulation isolation and comprehensive automated test suites (Unit 9).

### 2.2 Product Functions
Key functions include:
1) **Market Data Intake & Validation**: Batch and validate WebSocket events; trigger currency‑strength calculations on significant price moves. (U5)
2) **Signal Generation & Transmission**: Feature engineering, ML inference with timeout; fallback to rule‑based; transmit via healthiest bridge; track lifecycle via UUID. (U5, U6)
3) **Bridge Health & Failover**: Monitor bridges, evaluate state transitions with hysteresis; enforce circuit breakers and automatic failover. (U5, U6)
4) **Alerting & Escalation**: Policy‑based routing, deduplication, escalation chains; time‑based routing for trading vs off‑hours. (U5)
5) **State Management**: Atomic updates, checkpoints, integrity validation, distributed synchronization, recovery. (U4)
6) **Security & Access Control**: JWT auth, session mgmt, RBAC with permission caching, audit logging, suspicious‑activity detection. (U7)
7) **Performance Governance**: Adaptive batching, resource and memory management, latency targets, DB pooling. (U8)
8) **Configuration Management**: Hierarchical merge, hot‑reload, conflict resolution, versioning and rollback. (U5)
9) **Testing & Simulation**: Isolated environment, mock interfaces (MT4, market data, calendar), bridge test suites incl. latency, failover, recovery. (U9)
10) **Excel/VBA Operational Dashboards**: Real‑time bridge health, lifecycle views, alerts interface, simulation indicators. (U5)

### 2.3 User Characteristics
- **System Admins**: Manage configuration, security roles, and deployments.
- **Traders/Risk Managers**: Monitor signals, executions, alerts; review dashboards and reports.
- **Engineers/QA**: Implement services, maintain bridges, write tests, run simulation suites.
- **Auditors**: Review audit trails, configuration versions, reconciliation and test evidence.

### 2.4 Constraints
- Strict isolation between simulation and live modes with no cross‑access. (U9)
- Communication must prefer primary bridge (dll_socket) and degrade gracefully. (U6, U5)
- State changes must be atomic with rollback and checkpointing. (U4)
- Authentication and authorization must be enforced for all APIs with audit trails. (U7)
- Performance guardrails must auto‑tune batch sizes and resource consumption. (U8)

### 2.5 Assumptions and Dependencies
- MT4/EA environment reachable via one of the supported bridges.
- Datastores available for state, audit logs, and simulation.
- Time synchronization across services.
- Network conditions may degrade; failover and recovery are essential.

### 2.6 Architecture Decomposition (Systems → Subsystems → Components → Modules)

#### 2.6.1 Systems & Subsystems
1) **Event Orchestration System (U5, U6, U8)**
   - Subsystems: MarketDataEventProcessor; SignalEventProcessor; AlertEventCoordinator; BridgeHealthCoordinator; LifecycleEventCoordinator; PowerShell Ops Cycle.
2) **Communication Bridge System (U5, U6)**
   - Subsystems: Bridge Manager; Health Monitor; Circuit Breakers; Failover Controller.
3) **State & Persistence System (U4, U5)**
   - Subsystems: StateCheckpointer; AtomicStateTransaction; StateRecovery; DistributedStateManager.
4) **Security & Access System (U7)**
   - Subsystems: Authentication; Session Mgmt; RBAC Permission Manager; Security Audit Logger; Suspicious‑Activity Monitor.
5) **Performance & Scalability System (U8)**
   - Subsystems: SmartResourceManager; AdaptiveBatchManager; MemoryManager; DB Connection Pool.
6) **Testing & Simulation System (U9)**
   - Subsystems: SimulationFramework; Mock Interfaces; Bridge Test Suites; Validation Orchestrator.
7) **Operational Dashboard System (U5)**
   - Subsystems: Excel Dashboard Controller; Bridge Health View; Signal Lifecycle View; Alert Management Interface; Simulation Indicators.
8) **Configuration Management System (U5)**
   - Subsystems: Hierarchical Config Merge & Conflict Resolution; Hot‑Reload; Versioning & Rollback.

#### 2.6.2 Components → Modules (Representative)
- **MarketDataEventProcessor** → modules: batch window (100ms), validation, currency‑strength trigger.
- **SignalEventProcessor** → modules: feature extraction, ML inference (5s timeout), rule‑based fallback, bridge transmit, plugin validation.
- **BridgeHealthCoordinator** → modules: metrics collection, hysteresis thresholds (e.g., 10 consecutive successes / 3 failures), circuit breaker mgmt, auto‑failover.
- **LifecycleEventCoordinator** → modules: atomic state updates, cross‑system sync, hourly reconciliation & orphan cleanup.
- **StateCheckpointer** → modules: atomic checkpoint write, versioning, integrity checksum.
- **DistributedStateManager** → modules: conflict detection and resolution, propagation.
- **JWTAuthProvider** → modules: token generation/validation, refresh/expiry.
- **PermissionManager** → modules: permission calc with cache; audit of permission checks; role inheritance.
- **SecurityAuditLogger** → modules: access attempts; permission checks; suspicious activity detection.
- **SmartResourceManager / AdaptiveBatchManager** → modules: adjust batch size; performance history; failure handling; memory governance.
- **DatabaseConnectionPool** → modules: min/max connections, health validation, exhaustion handling.
- **SimulationFramework** → modules: isolated DB schema; file paths; mock MT4/MarketData/Calendar; live‑access guards.
- **Bridge Test Suites** → modules: connectivity, latency, failover, recovery, load, error handling, concurrency.
- **Excel/VBA Interfaces** → modules: BridgeHealth, SignalTracking, AlertManagement, emergency overrides.
- **Config Management (PS)** → modules: merge by priority, conflict reporting, hot‑deploy, rollback, audit versioning.

### 2.7 Layered Decomposition
- **Data Sources**: Market data (WebSocket), calendar (live or mock in simulation). (U5, U9)
- **Data Processing (Excel/VBA, Python)**: Event processors, feature extraction, ML inference, rule‑based fallback, Excel dashboards. (U5)
- **Communication/Bridges (C++, sockets, pipes)**: dll_socket → named_pipes → file_based with health & circuit breakers. (U5, U6)
- **Execution & Reentry (MQL4 EAs, logic systems)**: Orders via active bridge; lifecycle reconciliation; reentry governed by system state. (U5, U6)
- **Persistence (SQL, CSV/YAML configs)**: Atomic state DB, checkpoints, simulation DB schema, logs/audit. (U4, U9)
- **Configuration Management**: Hierarchical sources, conflict detection, hot‑reload, rollback and versioning. (U5)
- **Monitoring, Logging, Deployment**: Alert router, escalation, quantitative bridge metrics, audit logs, PS ops tasks. (U5, U7)

### 2.8 Relationship Mapping & Flows
- **Primary Flow (Live)**: MarketData(WebSocket) → MarketDataEventProcessor(100ms batch, validate) → SignalEventProcessor(ML or rule‑based fallback) → Bridge Manager (health‑aware transmit) → MT4/EA → LifecycleEventCoordinator (state sync) → Persistence (atomic DB + checkpoints) → Alerts/Excel Dashboards.
- **Degradation Flow**: On ML outage → rule‑based signals; on stale data → cache‑only with warnings; on DB outage → queued ops with replay; on bridge failure → fallback bridge; recovery procedures validated with state checks.
- **Simulation Flow**: Mock data/calendar → Simulation DB → Mock MT4 → Validation suites; live endpoints blocked; results compared to SLOs.

---

## 3. Specific Requirements

### 3.1 Functional Requirements (FR)

#### 3.1.1 Event Orchestration
- **FR‑E1** Market data events SHALL be collected in a 100ms batch window and validated; anomalies MUST raise alerts. (Source: U5)
- **FR‑E2** Currency‑strength calculations SHALL trigger on significant price moves (≥0.1 pip). (U5)
- **FR‑E3** Signal generation SHALL run feature extraction, attempt ML inference (timeout 5s), and fallback to rule‑based if timed out or degraded. (U5, U6)
- **FR‑E4** Signals SHALL be created with UUIDs and lifecycle initialized; lifecycle transitions MUST be validated and synchronized. (U5)
- **FR‑E5** Alerts SHALL be deduplicated within a 5‑minute window and routed per policy, with escalation on unacknowledged thresholds. (U5)

#### 3.1.2 Communication Bridges
- **FR‑B1** System SHALL attempt transmission via primary bridge (dll_socket); upon failure, sequentially fail over to named_pipes, then file_based. (U6, U5)
- **FR‑B2** Bridge health SHALL be sampled at 5‑second intervals; state transitions MUST honor hysteresis (promotion after ≥10 successes, degrade after ≥3 failures). (U5)
- **FR‑B3** Circuit breakers per bridge SHALL open after defined thresholds and reset after timeouts; global error triggers SHALL escalate. (U6)

#### 3.1.3 State & Persistence
- **FR‑S1** State updates SHALL be atomic with rollback on validation failure; checkpoints SHALL be created with version and checksum. (U4)
- **FR‑S2** On recovery, services SHALL restore from last known good checkpoint validated via checksum and timestamp. (U4)
- **FR‑S3** Distributed state inconsistencies SHALL be detected and resolved with conflict resolution; resolved states SHALL be propagated atomically. (U4)

#### 3.1.4 Security & Access Control
- **FR‑SEC1** API requests SHALL be authenticated via JWT; sessions SHALL expire per policy (e.g., 1h access, 24h refresh). (U7)
- **FR‑SEC2** Authorization decisions SHALL use RBAC with permission caching and inherited roles; each decision SHALL be audit‑logged. (U7)
- **FR‑SEC3** All access attempts (success/failure) SHALL be audit‑logged with user/IP/UA/endpoint; suspicious patterns SHALL trigger alerts and active countermeasures. (U7)

#### 3.1.5 Performance & Scalability
- **FR‑P1** System SHALL adapt batch sizes based on processing time history and system load (CPU/memory thresholds). (U8)
- **FR‑P2** Memory manager SHALL apply graduated responses (warning vs critical) including cache cleanup, GC, batch reduction, and alerting. (U8)
- **FR‑P3** Database access SHALL use a validated connection pool with min/max bounds and health checks; pool exhaustion MUST raise errors within timeout. (U8)

#### 3.1.6 Testing, Validation & Simulation
- **FR‑T1** Simulation mode SHALL initialize an isolated DB schema and file paths; live endpoints/paths MUST be inaccessible. (U9)
- **FR‑T2** Mock interfaces (MT4, market data, calendar) SHALL be provided for deterministic tests. (U9)
- **FR‑T3** Bridge test suites SHALL cover connectivity, latency, failover, recovery, load, error handling, and concurrency with pass/fail criteria. (U9)

#### 3.1.7 Configuration Management & Operations
- **FR‑C1** Config manager SHALL merge hierarchical sources by precedence, detect conflicts, and support hot‑reload with rollback and audit versioning. (U5)
- **FR‑C2** Operational tasks (health coordination, recovery, escalation) SHALL run on scheduled intervals and respond to events. (U5)
- **FR‑C3** Dashboards SHALL visualize bridge health, lifecycle states, alerts, and simulation indicators with refresh cadence (e.g., 10s). (U5)

### 3.2 Performance Requirements (PR)
- **PR‑1** Bridge latency targets: dll_socket <10ms avg; named_pipes <50ms avg; file_based <500ms avg. (U9 test expectations)
- **PR‑2** Bridge success rate SLO ≥90% under nominal conditions; circuit breaker triggers at configured thresholds. (U5/U6)
- **PR‑3** ML inference timeout ≤5s; batch processing typical window ≤100ms for intake. (U5)
- **PR‑4** Memory usage responses at ≥80% (warning) and ≥90% (critical) MUST execute prescribed actions within 1s. (U8)
- **PR‑5** Connection pool acquisition MUST succeed or fail within configured timeout (default 30s). (U8)

### 3.3 Design Constraints (DC)
- **DC‑1** All state changes MUST be transactionally safe with rollback and checkpointing; checkpoints MUST include checksums and monotonic versioning. (U4)
- **DC‑2** Simulation mode MUST be fully isolated (DB, filesystem, network) with validation tests failing if any live path/endpoint is reachable. (U9)
- **DC‑3** Security MUST implement JWT with verified expiry and token type, and RBAC with inheritance and wildcard permissions; audit logs retained per policy (e.g., 90 days). (U7)
- **DC‑4** Graceful degradation policies MUST be explicit: ML → rule‑based, stale data → cache‑only + warnings, DB outage → queue/replay, bridge failure → fallback bridge. (U6)
- **DC‑5** Configuration changes MUST be auditable with versioning and rollback, and hot‑reload MUST be atomic. (U5)

---

## Appendix A — Layer → System Mapping
- Data Sources → MarketData, Calendar (mock/live) — U5, U9
- Data Processing → Event processors, feature/ML, Excel dashboards — U5
- Communication/Bridges → dll_socket, named_pipes, file_based with health/circuit breakers — U5, U6
- Execution & Reentry → MT4/EA via active bridge; lifecycle reconciliation — U5, U6
- Persistence → Atomic DB, checkpoints, simulation DB — U4, U9
- Config Mgmt → Hierarchical merge, hot‑reload, rollback — U5
- Monitoring/Logging/Deployment → Alerts, escalation, audits, PS ops — U5, U7

## Appendix B — Decomposition Catalog (Modules)
- MarketDataEventProcessor; SignalEventProcessor; AlertEventCoordinator; BridgeHealthCoordinator; LifecycleEventCoordinator (U5)
- HierarchicalCircuitBreaker; GracefulDegradation; AutomatedRecoverySystem (U6)
- StateCheckpointer; StateRecovery; DistributedStateManager (U4)
- JWTAuthProvider; PermissionManager; SecurityAuditLogger; RoleDefinition (U7)
- SmartResourceManager; AdaptiveBatchManager; MemoryManager; DatabaseConnectionPool (U8)
- SimulationFramework; MockMT4Interface; ComprehensiveBridgeTestSuite (U9)

## Appendix C — Traceability Matrix (excerpt)
| Requirement | Unit Source(s) | Notes |
|---|---|---|
| FR‑E1, FR‑E2, FR‑E3, FR‑E4, FR‑E5 | U5 | Event orchestration, lifecycle, alerting |
| FR‑B1, FR‑B2, FR‑B3 | U5, U6 | Bridges, health, circuit breakers |
| FR‑S1, FR‑S2, FR‑S3 | U4 | State mgmt & recovery |
| FR‑SEC1‑3 | U7 | Auth, RBAC, audit |
| FR‑P1‑P3 | U8 | Perf governance, DB pool |
| FR‑T1‑T3 | U9 | Simulation & test suites |
| FR‑C1‑C3 | U5 | Config mgmt & dashboards |

> Full expansion of the matrix can be generated as a separate artifact as needed.

