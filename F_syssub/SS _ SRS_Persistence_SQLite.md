# Software Requirements Specification (SRS)
## HUEY_P Trading System — Persistence Layer (SQLite) & Cross‑Component Integration
**Version:** 0.1 (Focused extraction from attached sources)  
**Status:** Draft (persistence layer complete; other layers stubbed for traceable expansion)

---

### 1. Introduction

#### 1.1 Purpose
This SRS defines the architecture and requirements of the **Persistence Layer** for the HUEY_P trading system, with emphasis on the embedded **SQLite** database, its schema, access patterns, and integration points with Execution Advisors (EAs), bridges, analytics, and administrative tooling. Extracted details originate from the attached source and are kept traceable. fileciteturn0file0

#### 1.2 Scope
The scope for Version 0.1 covers:
- Architectural decomposition of the Persistence Layer (Systems → Subsystems → Components → Modules).
- Explicit role, dependencies, and interfaces of SQLite within the broader architecture.
- Machine‑readable, IEEE‑830‑style requirements for persistence‑related functionality, constraints, and maintenance. fileciteturn0file0

> **Note:** Other layers (Data Sources, Processing, Bridges, Execution/Reentry, Configuration, Monitoring/Deployment) are outlined for traceability and relationship mapping but populated only where directly supported by the attached material; items outside the attached source are marked **[TBD]** for subsequent expansion.

#### 1.3 Definitions, Acronyms, Abbreviations
- **EA** — Execution Advisor (MetaTrader 4 Expert Advisor) [System execution component].
- **Bridge** — Middleware that streams ticks/commands between broker/EA and other services.
- **ORM** — Object‑Relational Mapping layer used by Python services to access SQLite.
- **Tick** — Market data snapshot (bid/ask) at a time instant.
- **Snapshot** — Point‑in‑time capture of configuration or margin/account state.
- **S1** — Reference to the attached **“SQLite Schema and Usage Plan”**. fileciteturn0file0

#### 1.4 References
- **[S1]** U_SQLite Schema and Usage Plan.md (attached). Primary source for all persistence requirements, schema, access patterns, retention, and integration notes. fileciteturn0file0
- **[R‑A]** 4_Remediated_State_Management_and_Persistence.md — referenced by S1 (not attached in this turn).
- **[R‑B]** 12_Broker_Abstraction_and_Margin_Model.md — referenced by S1 (not attached).
- **[R‑C]** 13_EA_Design_and_Bridge_Deployment_Guide.md — referenced by S1 (not attached).
- **[R‑D]** 14_Analytics_Config_and_Report_UI.md — referenced by S1 (not attached).

#### 1.5 Overview
Section 2 provides the overall architectural perspective and layered decomposition. Section 3 enumerates specific, machine‑readable requirements with traceability back to [S1].

---

### 2. Overall Description

#### 2.1 Product Perspective
The Persistence Layer is an **embedded, local SQLite** database used to (a) provide low‑latency access to critical trading state, (b) durably log trading events and signals, and (c) serve as a **cross‑component exchange bus** for EAs, analytics, and orchestration scripts. fileciteturn0file0

#### 2.2 Product Functions
Per [S1], core persistence functions include:  
F‑PF‑01. **Tick Logging** for playback and diagnostic replay. fileciteturn0file0  
F‑PF‑02. **Order Journal** to capture signals and execution results. fileciteturn0file0  
F‑PF‑03. **Margin Snapshots** for audit and analytics. fileciteturn0file0  
F‑PF‑04. **EA ↔ Bridge Logging** for raw message exchange debugging. fileciteturn0file0  
F‑PF‑05. **Config Snapshots** for last‑known‑good rollback/override. fileciteturn0file0

#### 2.3 User Characteristics
- **Quant/Strategy Engineer:** consumes ticks/orders for research and analytics.  
- **EA/Bridge Developer:** writes/reads integration logs, validates messaging and timing.  
- **Ops/Support:** inspects snapshots, runs health checks and pruning jobs.  
Roles/flows inferred directly from S1’s access patterns and use‑cases. fileciteturn0file0

#### 2.4 Constraints
- **Embedded DB (SQLite):** no external DB dependency by design. fileciteturn0file0  
- **Access via Python ORM or raw SQLite:** canonical access path; schema migration checks expected at startup. fileciteturn0file0  
- **Pruning/Retention:** automatic pruning for selected tables; optional archival to Parquet/cloud. fileciteturn0file0

#### 2.5 Assumptions and Dependencies
- **EA Bridge → DB:** writes `ticks` & `bridge_logs`. **Analytics** read from `orders`, `margin_snapshots`, `ticks`. **CLI Admin** writes `config_snapshots`. fileciteturn0file0  
- **Upstream Specs:** state management, margin rules, EA/bridge deployment, analytics/reporting are governed by [R‑A..D] and referenced by S1. fileciteturn0file0

---

### 3. Specific Requirements

#### 3.1 Functional Requirements and Architectural Decomposition

##### 3.1.1 System → Subsystem → Components → Modules (Persistence Focus)

- **System:** HUEY_P Trading System [context].
- **Subsystem:** **Persistence Layer (SQLite)** — embedded data store and exchange bus. Role: low‑latency state, durable logs, cross‑component exchange. fileciteturn0file0

  - **Component A:** **SQLite Database Instance**
    - **Role:** stores tables for ticks, orders, margin snapshots, bridge logs, config snapshots. fileciteturn0file0
    - **Dependencies:** local file system; accessed primarily by Python services and the EA bridge. fileciteturn0file0
    - **Modules (Tables):**
      1. **`ticks`**
         - **Role:** tick‑level bid/ask time series for replay/diagnostics.  
           **Indices:** `symbol, timestamp` (as specified). fileciteturn0file0
         - **Dependencies:** EA bridge writes; Analytics reads. **Produces:** durable tick stream. fileciteturn0file0
      2. **`orders`**
         - **Role:** end‑to‑end trade lifecycle journal (signal → broker result). fileciteturn0file0
         - **Dependencies:** EAs/bridges write; analytics/reporting read. **Produces:** auditable history. fileciteturn0file0
      3. **`margin_snapshots`**
         - **Role:** time‑stamped margin/account state for audits. fileciteturn0file0
         - **Dependencies:** Broker abstraction/margin model inputs; analytics reads. fileciteturn0file0
      4. **`bridge_logs`**
         - **Role:** raw EA↔Bridge messaging (“EA_TO_BRIDGE” / “BRIDGE_TO_EA”) for debugging & validation. fileciteturn0file0
         - **Dependencies:** EA bridge writes; developers/ops read. fileciteturn0file0
      5. **`config_snapshots`**
         - **Role:** last‑known‑good configuration copy for override/rollback. fileciteturn0file0
         - **Dependencies:** CLI/admin writes; services read on recovery. fileciteturn0file0

  - **Component B:** **Access Layer (Python ORM / Raw SQLite)**
    - **Role:** provides canonical, strongly‑typed DB access; may use SQLAlchemy/SQLModel or raw SQLite. fileciteturn0file0
    - **Dependencies:** Python runtime; migration tooling (`sqlite-utils`/Alembic) at startup. fileciteturn0file0

  - **Component C:** **Retention & Maintenance Jobs**
    - **Role:** scheduled pruning (ticks, bridge_logs), optional archival to Parquet/cloud, schema checks on boot. fileciteturn0file0
    - **Dependencies:** configuration policy; batch/CLI tooling. fileciteturn0file0

- **Cross‑Layer Interfaces (from S1):**
  - **EA Bridge → SQLite:** write path for ticks & bridge logs. fileciteturn0file0
  - **Analytics → SQLite:** read path for ticks, orders, margin. fileciteturn0file0
  - **CLI/Admin → SQLite:** write path for config snapshots. fileciteturn0file0

###### Requirements (IDs) — Persistence Layer

**FR‑PERS‑001 (Schema: ticks).** The system SHALL implement a `ticks` table with fields `{id PK, symbol, bid, ask, timestamp, source}` and an index on `(symbol, timestamp)` for low‑latency replay and diagnostics. fileciteturn0file0  
**FR‑PERS‑002 (Schema: orders).** The system SHALL implement an `orders` table capturing `{id PK, signal_id, symbol, action, lots, status, price, margin_used, created_at, updated_at}` to journal trade lifecycle events. fileciteturn0file0  
**FR‑PERS‑003 (Schema: margin_snapshots).** The system SHALL implement a `margin_snapshots` table for `{id PK, symbol, margin_required, account_balance, equity, timestamp}` to support margin audits. fileciteturn0file0  
**FR‑PERS‑004 (Schema: bridge_logs).** The system SHALL implement a `bridge_logs` table with `{id PK, timestamp, direction, content}` to capture EA↔Bridge messaging (“EA_TO_BRIDGE” / “BRIDGE_TO_EA”). fileciteturn0file0  
**FR‑PERS‑005 (Schema: config_snapshots).** The system SHALL implement a `config_snapshots` table with `{id PK, snapshot_time, config_hash, raw_yaml}` to persist last‑known‑good configurations. fileciteturn0file0  

**FR‑PERS‑006 (Access Layer).** The system SHOULD provide a Python ORM (or raw SQLite) access path for read/write operations aligned with the schema above. fileciteturn0file0  
**FR‑PERS‑007 (Writer Roles).** EA bridge MUST be able to write to `ticks` and `bridge_logs`; CLI/admin MUST be able to write to `config_snapshots`. fileciteturn0file0  
**FR‑PERS‑008 (Reader Roles).** Analytics MUST be able to read `orders`, `margin_snapshots`, and `ticks`. fileciteturn0file0  
**FR‑PERS‑009 (Pruning).** The system SHALL support auto‑pruning for `ticks` and `bridge_logs` older than a configurable retention window. fileciteturn0file0  
**FR‑PERS‑010 (Archival).** The system SHOULD support optional archival/offload of order history to Parquet or cloud storage via a task runner. fileciteturn0file0  
**FR‑PERS‑011 (Migration Check).** On startup, the system SHALL run a schema migration/verification step using `sqlite‑utils` or Alembic (or equivalent). fileciteturn0file0  
**FR‑PERS‑012 (Diagnostics).** The system MAY provide a CLI `sqlite_diagnose.py` to validate schema and surface anomalies, plus a web browser for inspection. fileciteturn0file0

##### 3.1.2 Other Subsystems (Outlined for Relationships / Traceability)

> These items are included to satisfy the request for a complete architectural map. Only statements directly supported by S1 are enumerated as requirements; all other details are **[TBD]** pending attachment of the referenced specs.

- **Data Sources [TBD].** Broker price feed(s), calendar/events, external analytics.  
  **Known dependencies to Persistence:** produces ticks consumed by `ticks`. fileciteturn0file0

- **Data Processing (Excel/VBA, Python) [TBD].** Feature engineering, analytics, reporting.  
  **Known dependencies:** reads `orders`, `margin_snapshots`, `ticks`. fileciteturn0file0

- **Communication/Bridges (C++, sockets, pipes) [TBD].** EA bridge writes ticks and logs.  
  **Known dependencies:** writes `ticks`, `bridge_logs`; reads configs (from snapshots as needed). fileciteturn0file0

- **Execution & Reentry (MQL4 EAs, logic systems) [TBD].** Generates orders, updates statuses.  
  **Known dependencies:** writes `orders`; may read margin/policy; interacts with bridge. **Trace refs via S1 integration map.** fileciteturn0file0

- **Configuration Management [TBD].** YAML/CSV configs, snapshots for rollback.  
  **Known dependencies:** writes to `config_snapshots`; consumers read on recovery. fileciteturn0file0

- **Monitoring, Logging, Deployment [TBD].** Ops dashboards, log drains, CI/CD.  
  **Known dependencies:** reads `bridge_logs` for EA/bridge telemetry; invokes pruning/archival jobs. fileciteturn0file0

#### 3.2 Performance Requirements
- **Low‑latency local access:** embedded design chosen to minimize dependency and latency for high‑frequency data handling. (Qualitative requirement; quantitative SLOs to be defined when upstream specs are attached.) fileciteturn0file0
- **Indexed Queries:** `ticks` indexed on `(symbol, timestamp)` to support replay & diagnostics efficiently. fileciteturn0file0

#### 3.3 Design Constraints
- **Embedded SQLite only** for persistence in this layer. fileciteturn0file0  
- **Access via Python ORM/raw SQLite**; **startup migration checks** required. fileciteturn0file0  
- **Retention policies** and **optional archival** for operational sustainability. fileciteturn0file0

---

### 4. Layered Decomposition (Explicit)

- **L1 Data Sources [TBD]:** external feeds → **L3 Persistence/ticks**.  
- **L2 Data Processing (Excel/VBA, Python) [TBD]:** reads **orders/margin/ticks** for analytics/report UI. fileciteturn0file0  
- **L3 Persistence (SQLite):** modules `ticks`, `orders`, `margin_snapshots`, `bridge_logs`, `config_snapshots`. fileciteturn0file0  
- **L4 Communication/Bridges [TBD]:** write path into L3 (`ticks`, `bridge_logs`). fileciteturn0file0  
- **L5 Execution & Reentry [TBD]:** interacts with bridges; read/write `orders` & margin data. fileciteturn0file0  
- **L6 Configuration Management [TBD]:** provides configs; snapshots in L3. fileciteturn0file0  
- **L7 Monitoring/Logging/Deployment [TBD]:** consumes `bridge_logs`, manages pruning/archival/migrations. fileciteturn0file0

---

### 5. Relationship Mapping & Explicit Flows

**Flow F‑1:** _Calendar/Price Feeds_ → **EA/Bridge** → **`ticks`** (L3) → _Analytics & Replay_. fileciteturn0file0  
**Flow F‑2:** _Signal Generation (EA)_ → **`orders`** (L3) → _Execution Result Updates_ → _Analytics/Reporting_. fileciteturn0file0  
**Flow F‑3:** **Bridge ↔ EA Messaging** → **`bridge_logs`** (L3) → _Debugging/Validation Dashboards_. fileciteturn0file0  
**Flow F‑4:** _Config authoring_ → **`config_snapshots`** (L3) → _Rollback/Recovery by services_. fileciteturn0file0  
**Flow F‑5:** _Ops tasks_ → **Pruning (ticks/bridge_logs)** and **Archival (orders → Parquet/cloud)**. fileciteturn0file0

> Relationships are hierarchical (L1→L7), sequential (signal→journal→analytics), and cross‑cutting (config/ops touch many layers). Derived from S1’s use‑cases, schema, and integration notes. fileciteturn0file0

---

### 6. Traceability

#### 6.1 Requirements → Sources
| Req ID | Source |
|---|---|
| FR‑PERS‑001..005 (schemas) | [S1] tables and DDL excerpts. fileciteturn0file0 |
| FR‑PERS‑006..008 (roles/access) | [S1] access patterns & read/write roles. fileciteturn0file0 |
| FR‑PERS‑009..011 (ops/maintenance) | [S1] retention & migration checks. fileciteturn0file0 |
| FR‑PERS‑012 (diagnostics/inspection) | [S1] optional enhancements. fileciteturn0file0 |

#### 6.2 Architecture Elements → Sources
| Element | Role/Dependency | Source |
|---|---|---|
| SQLite DB Instance | Embedded persistence & exchange bus | [S1] system role. fileciteturn0file0 |
| Access Layer (ORM) | Canonical typed access; startup checks | [S1] access patterns & maintenance. fileciteturn0file0 |
| Retention/Archival Jobs | Pruning, Parquet/cloud offload | [S1] retention & enhancements. fileciteturn0file0 |
| `ticks` | Replay/diagnostics; index on `(symbol,timestamp)` | [S1] schema. fileciteturn0file0 |
| `orders` | Trade lifecycle journal | [S1] schema. fileciteturn0file0 |
| `margin_snapshots` | Margin/account audit | [S1] schema. fileciteturn0file0 |
| `bridge_logs` | Raw EA↔Bridge messages | [S1] schema. fileciteturn0file0 |
| `config_snapshots` | Config rollback/override | [S1] schema. fileciteturn0file0 |

---

### 7. Completeness Check (Per Provided Sources)
- All persistence‑related systems/subsystems in the attached source are represented (DB instance, tables, access, retention, integration roles). fileciteturn0file0  
- Duplicates were consolidated under the Persistence Layer while preserving references to S1’s “Integration References” for future expansion ([R‑A..D], not attached here). fileciteturn0file0  
- Non‑persistence layers are included as **[TBD]** placeholders to maintain traceability and to be populated once their source documents are attached.

---

### Appendix A — DDL Summary (from S1)
- `ticks(id PK, symbol, bid, ask, timestamp, source)`; INDEX(symbol, timestamp)  
- `orders(id PK, signal_id, symbol, action, lots, status, price, margin_used, created_at, updated_at)`  
- `margin_snapshots(id PK, symbol, margin_required, account_balance, equity, timestamp)`  
- `bridge_logs(id PK, timestamp, direction, content)`  
- `config_snapshots(id PK, snapshot_time, config_hash, raw_yaml)`  
(See [S1] for exact DDL blocks and semantics.) fileciteturn0file0

