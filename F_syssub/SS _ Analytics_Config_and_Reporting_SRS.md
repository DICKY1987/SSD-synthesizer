# Software Requirements Specification (SRS)  
## Analytics Config & Reporting Subsystem (IEEE 830-style)

---

## 1. Introduction

### 1.1 Purpose
This SRS specifies the architecture and requirements for the **Analytics Config & Reporting Subsystem** that provides configurable analytics, KPI computation, alerting, and reporting for the broader trading system. It defines structure, configuration interfaces, UI requirements, data sources, and threshold/alert behaviors. 

### 1.2 Scope
The subsystem:
- Ingests execution outcomes and signal metrics.
- Computes and serves KPIs.
- Accepts Excel/JSON-based configuration.
- Renders reporting views and exports.
- Emits alerts and optional strategy deactivation actions when thresholds are breached. 

### 1.3 Definitions, Acronyms, Abbreviations
- **KPI**: Key Performance Indicator (e.g., win rate, drawdown).  
- **Strategy ID**: Configurable identifier for a trading strategy.  
- **Config Workbook**: `analytics_config.xlsx` with defined sheets.  
- **Alert Thresholds**: Config values triggering actions/notifications.  

### 1.4 References
- **Source Specification**: *U_Analytics Config and Report UI.md*, §§14.1–14.7. 

### 1.5 Overview
Section 2 describes the product’s architecture, layers, and users. Section 3 provides detailed functional and non-functional requirements mapped to components and modules with traceable identifiers and citations to the source specification.

---

## 2. Overall Description

### 2.1 Product Perspective (Architecture & Layers)
**System → Subsystems → Components → Modules**

- **System**: Analytics Config & Reporting  
  - **Subsystem A**: Analytics Service  
    - **Component A1**: KPI Engine (computes win rate, avg return, drawdown, exposure)  
    - **Component A2**: Query API (REST or in-memory)  
  - **Subsystem B**: Configuration Ingestion  
    - **Component B1**: Excel Loader (`analytics_config.xlsx`)  
    - **Component B2**: JSON Override Loader  
    - **Module B1.1**: Sheet `strategy_config` (strategy_id, active, min_confidence, max_risk, note)  
    - **Module B1.2**: Sheet `metrics` (metric_id, label, enabled, format)  
  - **Subsystem C**: Reporting UI  
    - **Component C1**: Frontends (Streamlit / Dash/Flask)  
    - **Component C2**: Excel Exporter  
    - **Module C1.1**: Strategy Performance Summary (by Strategy ID)  
    - **Module C1.2**: Signal Quality Breakdown (by confidence bin)  
    - **Module C1.3**: Trade Outcome Attribution (ML vs rule-based)  
    - **Module C1.4**: Margin & Risk Utilization Charts  
  - **Subsystem D**: Alerting & Thresholds  
    - **Component D1**: Threshold Registry (drawdown_percent, win_rate_min, avg_slippage_max)  
    - **Component D2**: Action Pipeline (emit ALERT, optional strategy deactivation, webhook/email notify)  

**Layered Decomposition**
- **Data Sources**: signal metadata (UUID, confidence); trade results (PnL, slippage, duration); risk eval; broker feedback.  
- **Data Processing (Excel/VBA, Python)**: KPI computation; threshold evaluation.  
- **Communication/Bridges (C++/sockets/pipes)**: Query interface (REST/in-memory); outbound webhook/email for alerts.  
- **Execution & Reentry (MQL4 EAs, logic)**: Optional strategy deactivation signal (downstream to execution).  
- **Persistence (SQL, CSV/YAML configs)**: Excel config; JSON override; Excel exports (reports).  
- **Configuration Management**: Workbook sheets (`strategy_config`, `metrics`) define runtime behavior.  
- **Monitoring, Logging, Deployment**: Not specified—deferred to platform standards; UI options suggested.  

**Key Relationships / Flows**
- **Data**: *(Signals/Trades/Risk/Broker)* → **Analytics Service (KPI Engine)** → **Reporting UI & Query API**.  
- **Config**: *Excel/JSON* → **Config Ingestion** → **KPI/Alert behaviors, View toggles**.  
- **Alerting**: *Threshold breach* → **ALERT** → *(optional)* **Strategy Deactivation** → **Webhook/Email Notification**.  

### 2.2 Product Functions
- Compute and expose KPIs via API/UI.  
- Load configuration from Excel with JSON overrides; drive strategy selection, thresholds, backtest filters.  
- Render dashboards (performance, signal quality, attribution, risk utilization) and export to Excel.  
- Enforce alert thresholds and trigger actions/notifications.  

### 2.3 User Characteristics
- **Analyst/Trader**: Configures strategies/thresholds; views dashboards.  
- **Manager/Stakeholder**: Consumes Excel exports and summaries.  

### 2.4 Constraints
- Config is primarily Excel-based with optional JSON override.  
- UI technologies suggested (Streamlit/Dash/Flask); choice affects deployment.  

### 2.5 Assumptions and Dependencies
- Upstream systems reliably provide required data fields.  
- Alert delivery channels (webhook/email) are available and reachable.  

---

## 3. Specific Requirements

### 3.1 Functional Requirements

#### 3.1.1 Subsystem A — Analytics Service
- **FR-AN-001**: The system shall ingest trade execution outcomes and signal metrics.  
- **FR-AN-002**: The system shall compute KPIs including win rate, average return, drawdown, and exposure.  
- **FR-AN-003**: The system shall provide a queryable interface via REST or in-memory API.  

**Dependencies**: Consumes **Data Sources**; Produces **KPIs** to UI/API.  

#### 3.1.2 Subsystem B — Configuration Ingestion
- **FR-CI-001**: The subsystem shall read `analytics_config.xlsx` and apply configuration.  
- **FR-CI-002**: The subsystem shall accept an optional JSON override that supersedes workbook fields.  
- **FR-CI-003**: The subsystem shall expose the `strategy_config` sheet fields (strategy_id, active, min_confidence, max_risk, note).  
- **FR-CI-004**: The subsystem shall expose the `metrics` sheet fields (metric_id, label, enabled, format).  
- **FR-CI-005**: Configuration shall allow strategy selection, metric thresholds, and backtest duration/filters.  

**Dependencies**: Consumes Excel/JSON; Produces runtime settings for Analytics/Reporting/Alerting.  

#### 3.1.3 Subsystem C — Reporting UI
- **FR-UI-001**: The UI shall be implemented using Streamlit or Dash/Flask, with equivalent capabilities.  
- **FR-UI-002**: The UI shall present the following views: (a) Strategy Performance Summary; (b) Signal Quality Breakdown; (c) Trade Outcome Attribution; (d) Margin & Risk Utilization Charts.  
- **FR-UI-003**: The UI shall support Excel export for external stakeholders.  

**Dependencies**: Consumes KPIs/config; Produces dashboards and Excel files.  

#### 3.1.4 Subsystem D — Alerting & Thresholds
- **FR-AL-001**: The system shall load threshold values `drawdown_percent`, `win_rate_min`, and `avg_slippage_max` from configuration.  
- **FR-AL-002**: Upon threshold breach, the system shall emit an ALERT event.  
- **FR-AL-003**: The system shall support optional automatic deactivation of a Strategy ID.  
- **FR-AL-004**: The system shall notify via webhook and/or email following an alert.  

**Dependencies**: Consumes KPIs and thresholds; Produces ALERTs, notifications, and optional strategy control actions.  

#### 3.1.5 Data Interfaces (Upstream/Downstream Contracts)
- **DI-UP-001**: **Upstream Inputs** shall include: signal UUID & confidence; trade PnL, slippage, duration; risk utilization; broker order-fill quality.  
- **DI-DN-001**: **Downstream Outputs** shall include: KPI dataset (queryable); dashboard views; Excel exports; ALERT events; optional deactivation signal; webhook/email messages.  

### 3.2 Performance Requirements
- **PR-001**: KPI computation shall support interactive dashboard usage (exact latency targets TBD in platform NFRs).  
- **PR-002**: Alert evaluation shall occur promptly upon data refresh to ensure timely notifications.  

### 3.3 Design Constraints
- **DC-001**: Configuration artifacts must be maintained in `analytics_config.xlsx` with optional JSON overrides to enable non-technical control.  
- **DC-002**: UI should be implemented with one of the specified frameworks to meet rapid dashboarding needs.  
- **DC-003**: Threshold identifiers and semantics must match the YAML schema names provided.  

---

### (Informative) Completeness Check
All systems/subsystems from the provided source are represented:
- **Analytics Service** ✓  
- **Configuration Ingestion (Excel/JSON)** ✓  
- **Excel Config Sheets (`strategy_config`, `metrics`)** ✓  
- **Reporting UI (frontends, core views, export)** ✓  
- **Data Sources** ✓  
- **Alerting & Thresholds (YAML & pipeline)** ✓  
- **Future Enhancements** captured as roadmap (non-requirements). ✓  

---

### Relationship Mapping (concise)
**Signals/Trades/Risk/Broker** → **KPI Engine** → **Reporting UI / API** → **Users**  
**Config (Excel/JSON)** → **Config Loader** → **KPI/Views/Thresholds**  
**Threshold Breach** → **ALERT** → *(optional)* **Deactivate Strategy** → **Webhook/Email**
