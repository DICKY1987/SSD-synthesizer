# Comprehensive System Documentation — Filled from Provided Sources (v2)

> Only fields supported by explicit statements in the source docs are populated. All other fields are intentionally left blank.

---

## 1.0 System Overview & Architecture
### 1.1 Purpose and Scope
- **Purpose**: Implement an MT4 **Multi-Source Signal Execution System** that processes trading signals with sub‑10ms internal latency, supports reentry logic for failed/partial trades, and maintains high reliability across three communication tiers. fileciteturn0file1
- **Scope (In)**: Multi-source signal ingestion, strategy ID→parameter set mapping, risk‑adaptive parameter management (10 profiles), MT4 EA integration (30 pairs), reentry logic, SQLite state tracking/analytics. fileciteturn0file1
- **Scope (Out)**: Broker selection & account management; portfolio optimization across accounts; web/mobile UIs; external portfolio system integrations. fileciteturn0file1

### 1.2 Architectural Diagrams (C4, component, network)
- **Views referenced**: Context, Container, Component, Dataflow, Deployment (Draw.io XML provided in spec). fileciteturn0file1

### 1.3 Data Flow Diagrams (DFDs)
- **High-level flow**: Signal Sources → Communication Bridge (Socket→Pipes→Files) → Signal Processor → Strategy Mapper (StrategyID→ParameterSetID) → Parameter Resolver → MT4 EA → Reentry Engine → SQLite (state/audit). fileciteturn0file1

### 1.4 Stakeholders & Responsibilities
- Principal Systems Architect — overall design decisions.  
- Risk Management Team — parameter set definitions/validation.  
- Development Team — implementation/testing/deployment.  
- Operations Team — monitoring/maintenance. fileciteturn0file1

### 1.5 Trading Philosophy & Strategic Approach
- **Fusion strategy**: Multi‑source (AI/ML, technical, manual, calendar) with **risk‑adaptive** parameters and **reentry** for trade recovery; EA operates under **conservative fail‑safe defaults** on error. fileciteturn0file1

---

## 2.0 Data Models & Persistence
### 2.1 Logical Data Model (entities, attributes, relationships)
- **Entities noted**: Signals (UUID, strategyId), ParameterSets (10 profiles), ReentryConfigs (per‑pair profiles), Executions/Trades, Performance KPIs; tracked in SQLite with audit trail. fileciteturn0file1

### 2.2 Physical Database Schema (tables, types, constraints)
- **DB**: SQLite for state persistence; views and migration templates referenced (e.g., `sqlite_reentry_*`). fileciteturn0file0

### 2.3 State Management & Persistence Rules
- Trade/Signal lifecycle persisted with correlation IDs; idempotent processing; atomic file writes (temp→rename). fileciteturn0file1

### 2.4 Data Retention & Archival Policies
- (Not specified in sources.)

### 2.5 Terminal-Specific Persistence Mechanisms
- MT4 **Files** directory used for CSV failover; EA maintains state and logging; DLL communication enabled in EA settings when applicable. fileciteturn0file2

---

## 3.0 Interfaces & APIs
### 3.1 API Specifications (REST, gRPC, design principles)
- (Not applicable; system uses sockets/pipes/files.)

### 3.2 Detailed Endpoint Contracts (inputs, outputs, permissions)
- (Not specified as REST/gRPC; see 3.5 for runtime bridge contracts.)

### 3.3 Function-Level Contracts (internal libraries/modules)
- Core components include: `SignalTriggerHandler`, `StrategyResolver`, `ParameterSetLoader`, `SignalBuilder`, MT4 `CTradingEACore`, `CBridgeInterface`, `CReentryLogic`, `CSVDataManager`, `SQLiteManager` (with key methods listed). fileciteturn0file1

### 3.4 Integration Points (external APIs/services consumed)
- MT4 Terminal (MQL4 EA), Python Analytics Engine, Economic Calendar CSV feed. fileciteturn0file1

### 3.5 Communication Contracts (Runtime Bridges)
- **Primary**: DLL‑backed socket (ports 5555/9999) with message types: HEARTBEAT, STATUS_REQUEST, TRADE_UPDATE, ERROR.  
- **Fallbacks**: Named Pipes → CSV Files; atomic write patterns; heartbeat/liveness checks; retry/backoff and reconnection logic; structured error codes including DLL‑specific ranges (5000+). fileciteturn0file2 fileciteturn0file1

### 3.6 Signal Queueing & Ordering Guarantees
- Signals validated and processed idempotently; conservative default parameters on error; three‑tier failover maintains ordering via bridge interfaces (as specified). fileciteturn0file1

### 3.7 Legacy Integration Modules
- CSV‑based communication mode; Excel/VBA pipelines mentioned at repository level; DLL bridge (C++ socket). fileciteturn0file2

---

## 4.0 Core Logic & Behavior
### 4.1 Business Logic & Algorithms (descriptions/pseudocode)
- StrategyID resolves to ParameterSetID; risk parameters applied to create trade instruction; EA executes and reports results; Reentry Logic evaluates failed/partial outcomes and may schedule reentry per profile. fileciteturn0file1

### 4.2 Error Handling & Exception Strategy
- **Circuit breaker** after consecutive errors; enhanced error catalog (50+ codes incl. DLL‑specific); recovery with bounded retries; class‑based `LogManager`. fileciteturn0file2

### 4.3 Edge Case Specifications
- Fail‑safe defaults; idempotent processing; conservative behavior on data/bridge errors. fileciteturn0file1

### 4.4 Embedded Annotations (Code Comment Layer for devs)
- (Not explicitly specified.)

### 4.5 Safety Controls
- Global enable/disable for reentry; min delay; max generations; daily loss cap; min confidence; spread/freeze‑level guards; retries bounded; distinct magic offsets; execution logging and KPI snapshots. fileciteturn0file0

### 4.6 Adaptive Reentry Logic
- Per‑pair **Reentry Profiles** (CSV): actions (NO_REENTRY/SAME_TRADE/INCREASE_SIZE/etc.), size multipliers, delay seconds, optional confidence adjustments; decision logging and analytics. fileciteturn0file0

---

## 5.0 Deployment & Operations
### 5.1 Infrastructure & Environment Requirements
- Windows 10/11; MT4 Terminal; Python environment (requirements file provided). fileciteturn0file1 fileciteturn0file2

### 5.2 Dependency Specifications
- Python: pandas, numpy, matplotlib, plotly, PyYAML, dateutil, websockets, psutil, colorlog, etc. (see `huey_requirements.txt`). fileciteturn0file2

### 5.3 Configuration & Secrets Management
- EA inputs (e.g., `AutonomousMode`, `EnableDLLSignals`, risk settings); Python `huey_config.txt` for app/db/bridge/logging/alerts. fileciteturn0file2

### 5.3.1 Multi-Format Configuration & Profile Management
- YAML system config; CSV profiles/parameters; hot‑reload/live profile reload noted; PowerShell automation scripts for install/verify. fileciteturn0file0 fileciteturn0file1

### 5.4 Build & Deployment Process (CI/CD steps, rollback strategy)
- (Not specified as CI/CD steps; manual deployment outlined.)

### 5.4.1 Release Gates (Trading)
- (Not specified.)

### 5.5 Operational Runbooks & Process Orchestration
- Bridge diagnostics and emergency recovery scripts; port connectivity tests; database init/repair scripts. fileciteturn0file2

### 5.6 Broker/Terminal Failover SOP
- (Not specified beyond three‑tier communication failover.)

### 5.7 Observability & SLOs
- SLOs: 99.9% signal delivery; 99.5% execution success; latency budgets: <10ms processing, <100ms failover. KPIs and performance snapshots referenced. fileciteturn0file1 fileciteturn0file0

### 5.7.1 Trading Analytics & Performance Dashboards
- (Analytics/monitoring module referenced; dashboard in Python interface.) fileciteturn0file1 fileciteturn0file2

---

## 6.0 Non-Functional Requirements (NFRs)
### 6.1 Performance
- Sub‑10ms signal processing (internal); three‑tier failover <100ms. fileciteturn0file1
### 6.2 Scalability
- 30 concurrent currency pair EAs. fileciteturn0file1
### 6.3 Availability & Reliability
- 99.9% signal delivery; three‑tier failover; conservative defaults on error. fileciteturn0file1
### 6.4 Auditing & Logging
- Complete signal→execution traceability in SQLite; class‑based logging. fileciteturn0file1 fileciteturn0file2
### 6.5 Deterministic Replay & Time Sync
- (Not specified.)
### 6.6 Immutable Audit Logging
- (Not specified.)
### 6.7 Temporal/Regional Handling
- (Not specified.)

---

## 7.0 Security Specifications
- (Not specified.)

---

## 8.0 Model Governance (for AI/Trading Systems)
- (Not specified.)

---

## 9.0 Requirements Traceability (RTM Layer)
| Requirement ID | Description | Linked Code | Test Case | Compliance Ref | Linked Config |
|---|---|---|---|---|---|
| REQ-001 | Process multi‑source signals with sub‑10ms internal latency | EA bridge + Python Signal Processor | test_signal_processing.py | — | YAML/CSV configs fileciteturn0file1 |
| REQ-002 | Maintain 99.9% signal delivery with three‑tier failover | Bridge (Socket→Pipes→Files) | test_ea_python_communication.py | — | EA inputs + Python config fileciteturn0file1 fileciteturn0file2 |
| REQ-003 | Enable reentry for failed/partial trades with audit trail | CReentryLogic + SQLite | test_system_integration.py | — | Reentry CSV profiles fileciteturn0file1 fileciteturn0file0 |

---

## 10.0 Cross-View Linking
- IDs/terms consistent across architecture, components, and ops procedures in sources. fileciteturn0file1 fileciteturn0file2

---

## Sources
- Signal _ analyze your reentry system files to provide.md (governance controls, reentry artifacts & automation references). fileciteturn0file0  
- signal_system_technical_spec.md (system goals, architecture, diagrams, dataflow, SLOs). fileciteturn0file1  
- CLAUDE.md (repository structure, EA/Python bridge, configs, diagnostics, error handling). fileciteturn0file2  
- Comprehensive_System_Documentation_Template_v2.md (template sections used for structure only). fileciteturn0file3

*Generated: 2025-08-27 14:13:32*