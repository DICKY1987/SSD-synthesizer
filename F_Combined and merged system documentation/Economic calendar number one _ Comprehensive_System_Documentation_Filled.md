# 📘 Comprehensive System Documentation Template (Extended for Trading/AI Systems, v2)

## 1.0 System Overview & Architecture
### 1.1 Purpose and Scope  
Automated trading system that converts economic calendar events into actionable MT4 signals; imports CSV, enhances with anticipation events and equity market opens, monitors in real time, and generates signals for MT4/Excel integration.

### 1.2 Architectural Diagrams (C4, component, network)  
 

### 1.3 Data Flow Diagrams (DFDs)  
Downloads/Import → Raw Calendar Sheet → Processed Events → Enhanced Events (anticipation + equity) → Chronological Sort → Final Display → Strategy Execution → Signal Entry → MT4 Transfer → Trade Execution.

### 1.4 Stakeholders & Responsibilities  
 

### 1.5 Trading Philosophy & Strategic Approach  
Event-driven signals from economic events, anticipation events (default 2 h pre-event, configurable 1/2/4 h), plus equity market open events (Tokyo 21:00 CST; London 02:00 CST; New York 08:30 CST). Performance-based parameter selection and integrated risk management.

---

## 2.0 Data Models & Persistence
### 2.1 Logical Data Model (entities, attributes, relationships)  
Calendar events (title, country, impact, dates, status, quality scores), trading signals (export tracking), system status (health).

### 2.2 Physical Database Schema (tables, types, constraints)  
SQLite with UPSERT using natural keys (title, country, event_date, event_time); indexing for status and trigger_time queries; transaction/context management.

### 2.3 State Management & Persistence Rules (sessions, caches, lifecycles)  
Status/health tracking via system status table; event lifecycle status; signal export tracking with metadata.

### 2.4 Data Retention & Archival Policies (compliance, cleanup, backups)  
Automated backups (timestamped naming), retention policies, validation and recovery procedures.

### 2.5 Terminal-Specific Persistence Mechanisms  
 

---

## 3.0 Interfaces & APIs
### 3.1 API Specifications (REST, gRPC, design principles)  
FastAPI web app with REST endpoints and WebSocket updates.

### 3.2 Detailed Endpoint Contracts (inputs, outputs, permissions)  
 

### 3.3 Function-Level Contracts (internal libraries/modules)  
 

### 3.4 Integration Points (external APIs/services consumed)  
Multi-source calendar imports (ForexFactory, Investing, DailyFX).

### 3.5 Communication Contracts (Runtime Bridges)  
Real-time WebSocket broadcasting with client state management and reconnection; error handling and message queuing; health check systems.

### 3.6 Signal Queueing & Ordering Guarantees  
Processed events sorted chronologically before export.

### 3.7 Legacy Integration Modules  
Excel/VBA calendar management; MT4 integration via standardized EA-compatible CSV export.

---

## 4.0 Core Logic & Behavior
### 4.1 Business Logic & Algorithms (descriptions/pseudocode)  
Pipeline: Import → Impact filter (High/Medium) → Time zone standardization (CST) → Country mapping → Categorize → De-dup → Add anticipation/equity events → 15-sec monitoring → Trigger (−3 min configurable) → Strategy ID (RCI) → Parameter set selection (tiers) → Risk-adjusted adjustments.

### 4.2 Error Handling & Exception Strategy (error catalog, logging, recovery)  
Multi-level logging; retry with exponential backoff; circuit breaker patterns; component health/status monitoring and error escalation.

### 4.3 Edge Case Specifications (invalid inputs, boundaries)  
Past/future window validation (past tolerance 1 day; future range 14 days); weekend blocking; timezone-aware scheduling.

### 4.4 Embedded Annotations (Code Comment Layer for devs)  
 

### 4.5 Safety Controls  
Emergency stop/resume; emergency pause triggers; trading embargo windows (e.g., 60 min before / 30 min after high-impact events).

### 4.6 Adaptive Reentry Logic  
Risk score (0–100; base 50) drives parameter adjustments; risk tiers (Emergency/Recovery/Conservative/etc.); weighted smoothing (e.g., 60/40) and signal-strength scaling with risk.

---

## 5.0 Deployment & Operations
### 5.1 Infrastructure & Environment Requirements (runtime, hardware, cloud)  
Python implementations (multiple), FastAPI service, SQLite storage; Excel/VBA and MT4 integration.

### 5.2 Dependency Specifications (libraries, frameworks, versions)  
AsyncIOScheduler/APScheduler (UTC scheduling), FastAPI, SQLite.

### 5.3 Configuration & Secrets Management  
Pydantic-based configuration; environment variable overrides (e.g., DATABASE_PATH, SIGNALS_*); YAML configs with validation, backups, runtime updates.

### 5.3.1 Multi-Format Configuration & Profile Management  
YAML (hierarchical), CSV/EA export profiles; hot-reload/runtime updates and versioned backups.

### 5.4 Build & Deployment Process (CI/CD steps, rollback strategy)  
 

### 5.4.1 Release Gates (Trading)  
 

### 5.5 Operational Runbooks & Process Orchestration (jobs, retries, recovery)  
 

### 5.6 Broker/Terminal Failover SOP  
 

### 5.7 Observability & SLOs  
Performance/health monitoring: response-time tracking, resource/utilization metrics, error-rate monitoring, uptime tracking; component health scoring with alerts.

### 5.7.1 Trading Analytics & Performance Dashboards  
Outcome analysis: trade classification, quality scoring, streaks, profit factor, execution quality; dashboards with timers, emergency stop, performance metrics.

---

## 6.0 Non-Functional Requirements (NFRs)
### 6.1 Performance (response times, throughput, latency budgets)  
 

### 6.2 Scalability (growth in users, data, transaction volume)  
 

### 6.3 Availability & Reliability (uptime targets, DR strategy)  
 

### 6.4 Auditing & Logging (security, compliance, debugging)  
Comprehensive logging (INFO/WARN/ERROR/CRITICAL), timing metrics, rotation/archival, error context with stack traces.

### 6.5 Deterministic Replay & Time Sync  
 

### 6.6 Immutable Audit Logging  
 

### 6.7 Temporal/Regional Handling  
Time zone conversion to CST in processing; UTC-aware scheduling; weekend/holiday filtering with timezone considerations; regional equity market open times used as events.

---

## 7.0 Security Specifications
### 7.1 Authentication & Authorization (OAuth2, RBAC, MFA)  
 

### 7.2 Data Encryption (in transit, at rest)  
 

### 7.3 Vulnerability Mitigation (OWASP Top 10, secure coding standards)  
 

### 7.4 Compliance (GDPR, HIPAA, PCI-DSS, domain-specific)  
 

### 7.5 Secrets & Key Management (vaults, rotation, access inventories)  
 

---

## 8.0 Model Governance (for AI/Trading Systems)
 

---

## 9.0 Requirements Traceability (RTM Layer)
| Requirement ID | Description | Linked Code | Test Case | Compliance Ref | Linked Config |
|----------------|-------------|-------------|-----------|----------------|---------------|
 

---

## 10.0 Cross-View Linking
 

---

## 11.0 Export Strategy
EA-compatible CSV export: semicolon-delimited, 22+ columns including id/symbol/event fields, trading parameters, execution windows; timestamped filenames and MT4 file-path targeting with backups.

---

## Appendix: Strategy ID System (from docs)
5-digit RCI: Region (e.g., N. America = 1, Europe = 2, Asia-Pacific = 3), country code within region, impact (Medium = 2, High = 3), checksum (sum mod 10). Example: USA + Medium → “10124”. Excludes CHF and Low impact.

---

**Notes:**  
• Sections intentionally left blank where no explicit source text was found.  
• All filled content is quoted or summarized directly from the three provided documents.
