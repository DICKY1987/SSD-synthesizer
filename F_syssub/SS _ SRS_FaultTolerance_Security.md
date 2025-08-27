# Software Requirements Specification (SRS)

## 1. Introduction

### 1.1 Purpose
This Software Requirements Specification (SRS) defines the architecture, interfaces, and requirements for the **Fault Tolerance & Resilience** and **Security & Access Control** subsystems within the Trading System. It expands subsystem definitions into a complete decomposition (Systems → Subsystems → Components → Modules), maps components to layers, and provides traceable, machine-readable requirements with source references.

### 1.2 Scope
This SRS covers:  
- Fault handling (hierarchical circuit breakers, graceful degradation, automated recovery).  
- Security (authentication with JWT, audit logging, RBAC permissioning).  
Interfaces to other platform layers (e.g., execution engines, data services) are identified as dependencies when referenced by the source material.

### 1.3 Definitions, Acronyms, Abbreviations
- **HCB**: Hierarchical Circuit Breaker  
- **RBAC**: Role-Based Access Control  
- **JWT**: JSON Web Token  
- **Bridge**: Inter-process communication mechanism (dll_socket, named_pipes, file_based)  

### 1.4 References
- U_6_Remediated_Fault_Tolerance_and_Resilience.md  
- U_7_Remediated_Security_and_Access_Control.md  

### 1.5 Overview
Section 2 presents the architecture and layered decomposition. Section 3 enumerates specific, testable requirements with traceability to the source documents.

---

## 2. Overall Description

### 2.1 Product Perspective (Architecture Mapping: Systems → Subsystems → Components → Modules)
**System: Trading Platform Reliability & Security Envelope**  

- **Subsystem: Fault Tolerance & Resilience (U_6)**  
  - *Components*  
    - **HierarchicalCircuitBreaker (HCB)** → manages per-bridge circuit breakers, attempts operation through dll_socket → named_pipes → file_based fallbacks.  
    - **GracefulDegradation** → policy engine for ml_service_unavailable, market_data_stale, database_outage, bridge_failure.  
    - **AutomatedRecoverySystem** → recovery policies for service_crash, bridge_failure, database_corruption, configuration_conflict.  

- **Subsystem: Security & Access Control (U_7)**  
  - *Components*  
    - **SecurityManager** → request authentication, session handling, audit of access attempts.  
    - **JWTAuthProvider** → token issuing/validation.  
    - **SecurityAuditLogger** → writes audit records, monitors suspicious activity.  
    - **PermissionManager (RBAC)** → role definitions, permission checks, audit of permission decisions.  

### 2.2 Product Functions
- Route operations through hierarchical circuit-breakers and fail over across bridges.  
- Degrade functionality gracefully (switch to rules, cache-only, queue & replay, fallback bridge).  
- Recover failed services with state validation and escalation.  
- Authenticate via JWT, maintain auditable access trails, detect brute force patterns.  
- Enforce RBAC with cached permission decisions and auditing.

### 2.3 User Characteristics
- Operators (SRE/SysOps) monitor resilience and triggers.  
- Security admins manage roles/policies and review audit logs.  
- Application services act as clients of both subsystems (service accounts).  

### 2.4 Constraints
- Bridge-specific thresholds/timeouts must be enforced.  
- JWT HS256 with secret management.  
- Audit log retention.

### 2.5 Assumptions and Dependencies
- Availability of multiple bridges (dll_socket, named_pipes, file_based).  
- Presence of configuration, alerting, queueing, and state-recovery services.  
- Security dependencies: audit database, policy engine, and token secrets storage.  

### 2.6 Layered Decomposition
- **Data Sources**: Market data cache; audit database; configuration storage.  
- **Data Processing**: Rule-based vs ML signal generators.  
- **Communication/Bridges**: dll_socket → named_pipes → file_based hierarchy via HCB.  
- **Execution & Reentry**: Execution engine consuming operations via active bridge.  
- **Persistence**: Queue persistence; audit log persistence.  
- **Configuration Management**: Runtime config updates; security policy updates.  
- **Monitoring, Logging, Deployment**: Degradation/recovery events; audit & alerts.

### 2.7 Relationship Mapping (Flows)
- **Operation Flow**: Operation → HCB → dll_socket → fallback → AutomatedRecovery/Degradation.  
- **Degradation Flow**: ML unavailable → rule-based signals; Market data stale → cache-only; DB outage → queue; Bridge failure → fallback.  
- **Security Flow**: Request → SecurityManager → JWTAuthProvider → SecurityAuditLogger → PermissionManager → Allow/Deny.

---

## 3. Specific Requirements

### 3.1 Functional Requirements

#### 3.1.1 Fault Tolerance & Resilience (FT)
- **FT-HCB-001**: System SHALL attempt bridges in order dll_socket → named_pipes → file_based.  
- **FT-HCB-002**: Each bridge SHALL have independent circuit breaker with thresholds/timeouts.  
- **FT-HCB-003**: Successful HALF_OPEN call SHALL reset to CLOSED.  
- **FT-GD-010**: On ml_service_unavailable, enable rules, disable ML, update config.  
- **FT-GD-011**: On market_data_stale, cache-only mode with warnings.  
- **FT-GD-012**: On database_outage, queue ops with replay.  
- **FT-GD-013**: On bridge_failure, activate fallback bridge.  
- **FT-RCV-020**: On service_crash, recover state, restart, validate health, escalate if fail.  
- **FT-RCV-021**: Provide recovery for bridge_failure, db_corruption, config_conflict.

#### 3.1.2 Security & Access Control (SEC)
- **SEC-AUTH-001**: Authenticate requests using JWT. Audit success/failure.  
- **SEC-AUTH-002**: Support access/refresh tokens, reject expired/invalid.  
- **SEC-AUD-010**: Persist audit records with timestamp, user, IP, UA, endpoint.  
- **SEC-AUD-011**: ≥5 failed attempts in 15m → high-severity alert, possible block.  
- **SEC-RBAC-020**: Evaluate permissions via explicit grants, roles, inheritance.  
- **SEC-RBAC-021**: Cache permission decisions (TTL). Audit checks.  
- **SEC-RBAC-022**: Provide predefined roles (system_admin, trader, risk_manager, developer, viewer).

### 3.2 Performance Requirements
- **PR-HCB-001**: dll_socket threshold=3, timeout=30s; named_pipes=5/60s; file_based=10/120s.  
- **PR-GD-002**: Market data warn=60s; max staleness=5m.  
- **PR-GD-003**: Queue max=10k; replay batch=100; replay interval=10s.  
- **PR-AUTH-004**: Access token=3600s; Refresh=86400s; Permission cache TTL=300s.  
- **PR-AUD-005**: Detection window=15m; fail threshold=5; log retention=90 days.

### 3.3 Design Constraints
- **DC-SEC-001**: JWT algorithm HS256; token payload includes id, roles, permissions, iat/exp. Secrets secured/rotated.  
- **DC-FT-002**: Circuit breaker must implement CLOSED/HALF_OPEN/OPEN.  
- **DC-OPS-003**: Recovery must validate health; escalate on failure.

---

## 4. Traceability
- FT-HCB-001..003 → U_6 §6.1  
- FT-GD-010..013 → U_6 §6.2  
- FT-RCV-020..021 → U_6 §6.3  
- SEC-AUTH-001..002 → U_7 §7.1  
- SEC-AUD-010..011 → U_7 §7.1.3  
- SEC-RBAC-020..022 → U_7 §7.2  

---

## 5. Dependencies
- **Upstream**: Market data feeds/cache; configuration service; security policy store.  
- **Downstream**: Execution engine via bridges; audit DB persistence.

---

## 6. Interfaces
- **Bridge Interface**: Operation dispatch through active bridge, breaker state handling.  
- **Security API**: authenticate_request, log audit, check permission.  
- **Recovery API**: handle_system_failure → policy → health validation → escalation.

---

## 7. Completeness Check
- All subsystems/components covered: HCB, GracefulDegradation, AutomatedRecovery, SecurityManager, JWTAuthProvider, SecurityAuditLogger, PermissionManager.  
- Performance and design constraints preserved.  

