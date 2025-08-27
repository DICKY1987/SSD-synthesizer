# Software Requirements Specification (SRS)
## HUEY_P Trading System — Architectural Decomposition (Systems → Subsystems → Components → Modules)

> Source basis: *U_1_Comprehensive_Component & Service Blueprint* (the “Blueprint”). Where the Blueprint itself cites other documents (e.g., *Enhanced Python-Dominant Trading System Technical Monograph – Updated/Remediated*), those cross-references are noted.

---

## 1. Introduction

### 1.1 Purpose  
This SRS consolidates the architectural information from the Blueprint into an IEEE-830–style document. It delivers a precise, traceable decomposition from Systems → Subsystems → Components → Modules, layered views, dependency mapping, interfaces, performance constraints, and explicit source traceability.

### 1.2 Scope  
In scope (from the Blueprint):
- Python Core Services: **Market Data Service**, **Signal Generation Service**, **Analytics Service**, **Communication Service**, **Configuration Service**.  
Out of scope (mentioned at ecosystem level but not fully specified in the Blueprint): detailed Excel/VBA pipelines, full MT4 EA logic internals, and DB schema definitions; these are referenced only insofar as the Python services interface with them.

### 1.3 Definitions, Acronyms, Abbreviations  
- **EA**: Expert Advisor (MT4/MetaTrader 4 automated strategy).  
- **MT4**: MetaTrader 4 trading platform.  
- **RCI**: Regional-Country-Impact strategy ID scheme (5-digit).  
- **VaR/CVaR**: Value at Risk / Conditional Value at Risk.  
- **SLA**: Service Level Agreement.  
- **TTL**: Time-to-Live (cache).  
- **Ack**: Acknowledgment (message receipt).  
- **QPS**: Queries per second.  
- **UUID**: Universally Unique Identifier.  
- **SHAP**: SHapley Additive exPlanations.

### 1.4 References  
- *U_1_Comprehensive_Component & Service Blueprint* (primary).  
- Blueprint cross-references: *Enhanced Python-Dominant Trading System Technical Monograph – Updated*; *… – Remediated* (cited by the Blueprint for thresholds, behaviors, and model details).

### 1.5 Overview  
Section 2 presents the product perspective, layered architecture, and high-level relationships. Section 3 enumerates specific requirements by subsystem/function, including inputs/outputs, dependencies, constraints, and performance targets with traceability to the Blueprint.

---

## 2. Overall Description

### 2.1 Product Perspective  
The HUEY_P Trading System is a service-oriented architecture centered on Python services that:  
- ingest and cleanse market/calendar/news data,  
- generate explainable trading signals with strategy IDs,  
- route and adapt messages to MT4 via bridges,  
- analyze portfolio risk/performance, and  
- manage configuration with hot-reload, audit, and distribution.  

#### 2.1.1 Layered Decomposition (explicit)
- **Data Sources**
  - WebSocket market feeds; Broker APIs; Economic calendar APIs; News APIs.  
- **Data Processing (Python; Excel/VBA referenced)**
  - Python: feature engineering, indicators, microstructure analysis, sentiment retrieval; ML ensemble; SHAP explainability. (Excel/VBA not detailed in Blueprint.)  
- **Communication / Bridges (C++/OS IPC surfaces referenced)**
  - Bridge Manager orchestrating **dll_socket**, **named_pipes**, **memory_mapped**, **file_based**; JSON↔CSV adaptation for MT4; message serialization; circuit-breaker + backoff.  
- **Execution & Reentry (MT4 EAs, logic systems referenced)**
  - Execution contracts via Communication Service with ack tracking; MT4-compatible CSV payloads; lifecycle updates. (EA internals not detailed in Blueprint.)  
- **Persistence**
  - Redis cache (currency strength, last prices, TTL); audit/change logs; risk/analytics outputs (reporting artifacts implied).  
- **Configuration Management**
  - Central store, schema validation, versioning, hot-reload coordination, distribution, rollback, audit.  
- **Monitoring, Logging, Deployment**
  - Metrics collectors; alert service; message trackers; configuration audit logs; health flags/heartbeats. (CI/CD not specified.)  

#### 2.1.2 Systems → Subsystems → Components → Modules (map)
- **System A: Market Data & Signal System**
  - *Subsystem A1: Market Data Service*  
    - Components: WebSocketManager, ConnectionPool, LatencyTracker, OutlierDetector, DataInterpolator, CorrelationMatrixCalculator, EigenvalueDecomposer, MetricsCollector, Redis cache client.  
  - *Subsystem A2: Signal Generation Service*  
    - Components: Ensemble models (RF/SVM/NN), CNN pattern detector w/ attention, FeatureProcessors, RCI System, EconomicCalendarClient, StatisticalSignificanceValidator, BacktestingEngine, MonteCarloSimulator, SHAPExplainer, DecisionTreeVisualizer, NLPExplanationGenerator, LifecycleManager hook, Logger/Heartbeat.  
- **System B: Communication & Execution Integration**
  - *Subsystem B1: Communication Service*  
    - Components: BridgeManager; active bridges (dll_socket, named_pipes, memory_mapped, file_based); JSONCSVConverter; MessageSerializer; CircuitBreaker; ExponentialBackoffPolicy; MessageTracker; AcknowledgmentValidator; FailoverCoordinator.  
  - *Subsystem B2: Execution Interface (MT4 Contract)*  
    - Components: CSV adapter, Ack tracking, lifecycle hooks. (Implements interface promises for MT4 EAs; EA internals are external.)  
- **System C: Risk & Analytics**
  - *Subsystem C1: Analytics Service*  
    - Components: VaRCalculator, CVaRCalculator, DynamicCorrelationAnalyzer, RegimeDetector, FactorAnalyzer, ReturnDecomposer, MLFeedbackIntegrator, MPTOptimizer, OutcomeTracker, ReportGenerator, FeedbackPipeline, PerformanceMonitor.  
- **System D: Configuration**
  - *Subsystem D1: Configuration Service*  
    - Components: ConfigurationStore, ConfigurationVersionManager, FileWatcher, HotReloadCoordinator, JSONSchemaValidator, ConfigurationConflictResolver, ConfigurationDistributor, ConfigAcknowledgmentTracker, ConfigurationChangeTracker, ConfigurationAuditLogger.  

### 2.2 Product Functions (high level)
- Acquire/cleanse market & event data with latency/QoS monitoring.  
- Generate explainable signals with strategy IDs, validation tiers, and lifecycle states.  
- Route messages with adaptive bridge selection, protocol adaptation, ack tracking, and failover.  
- Perform portfolio-level risk and attribution analyses with regime detection and alerts.  
- Manage configuration centrally with validation, versioning, hot-reload, and audit.  

### 2.3 User Characteristics  
- **Quants/Researchers**, **Algo Developers (Python/MT4)**, **SRE/DevOps**, **Risk/Compliance Analysts**, **Traders**.

### 2.4 Constraints  
- Real-time operation with strict latency targets; external API reliability; MT4 CSV protocol compatibility; persistent audit requirements; schema-validated configs; circuit-breaker and backoff policies for resilience.  

### 2.5 Assumptions and Dependencies  
- Broker, calendar, and news APIs available and authenticated; Redis, RabbitMQ/Redis pub-sub reachable; Alerting channel configured; MT4 endpoint reachable through at least one bridge; configuration schemas defined.  

---

## 3. Specific Requirements

### 3.1 Functional Requirements

#### 3.1.1 Market Data Service (Subsystem A1)
**Role**: Aggregate real-time prices/events, enforce SLA, cleanse data, compute currency strength, publish standardized `MarketDataModel`.  
**Dependencies (consumes/produces)**  
- Consumes: WebSocket feeds, Broker APIs, Calendar/News APIs.  
- Produces: `MarketDataModel` events; Redis cache entries (last price, currency strength), Alerts, Metrics.  
**Key Behaviors & Interfaces**  
- Track per-symbol latency; reconnect on failures; outlier detection → interpolation; compute correlation/eigenvalue-based strength when “significant move”; SLA breach → alert; publish MARKET_EVENT.  
**Triggers**: message arrival; connection failure; quality threshold breach.  
**Fault Tolerance**: automatic reconnection/backoff; use cached/interpolated data on anomalies.  

#### 3.1.2 Signal Generation Service (Subsystem A2)
**Role**: Build features, infer via RF/SVM/NN ensembles + CNN attention, integrate economic events → RCI strategy ID, validate (statistical/backtest/Monte Carlo), generate explainable `SignalModel`, publish `SIGNAL_CREATED`.  
**Dependencies**  
- Consumes: `MarketDataModel`, calendar events, config updates, trade outcome feedback.  
- Produces: `SignalModel` with SHAP/decision path/NLP explanation, lifecycle events, performance metrics.  
**Key Behaviors**  
- 5-second inference timeout w/ circuit-breaker; fallback to rule-based if ML unavailable; confidence aggregation; ID generation via RCI; tiered validation; SHAP + natural-language rationale.  
**Triggers**: significant market deltas; economic events; confidence > threshold.  

#### 3.1.3 Communication Service (Subsystem B1)
**Role**: Intelligent message routing to MT4/other targets via bridges; JSON↔CSV adaptation; ack validation; delivery metrics; failover.  
**Dependencies**  
- Consumes: Messages from services (e.g., `SignalModel`, lifecycle updates).  
- Produces: Delivered payloads via selected bridge; ack tracking records; alerts/metrics; failover events.  
**Key Behaviors**  
- Optimal bridge selection; if circuit-open → fallback bridge; MT4 targets use CSV adapter; exponential backoff on failure; recursive retry w/ escalation; per-message latency tracking; 30-second expected ack window.  
**Triggers**: message arrival; bridge health change; ack timeout.  

#### 3.1.4 Execution Interface / Reentry Contract (Subsystem B2)
**Role**: Provide a stable, MT4-compatible execution interface (transport + format + ack semantics) so EAs can place/manage orders and report outcomes back to Python services. (EA internals are external to this SRS; this defines the integration contract surfaced by Communication Service.)  
**Requirements**  
- **Transport**: dll_socket | named_pipes | memory_mapped | file_based (hierarchical fallback).  
- **Format**: CSV payloads for MT4; lifecycle/ack IDs in payload; strict schema versioning.  
- **Acks**: Ack validator must match original message UUID within timeout; invalid or missing ack → retry/escalate and alert.  

#### 3.1.5 Analytics Service (Subsystem C1)
**Role**: Portfolio risk (VaR/CVaR), dynamic correlation + regime detection, factor attribution, ML feedback integration, MPT recommendations, alerts, and reporting.  
**Dependencies**  
- Consumes: positions/exposure, market data, trade outcomes, economic events.  
- Produces: `RiskMetrics`, alerts (VaR breach, correlation spike), attribution reports, optimization suggestions.  
**Key Behaviors**  
- Monte Carlo & historical VaR; CVaR; regime detection; factor exposure; return decomposition; integrate ML performance signals; threshold checks → alerts.  

#### 3.1.6 Configuration Service (Subsystem D1)
**Role**: Central config store, schema validation, versioning, hot-reload, distribution, rollback, audit.  
**Dependencies**  
- Consumes: config files (YAML), API updates, file system events, service queries.  
- Produces: validated config objects with versions; reload events; distribution outcomes; audit/change records.  
**Key Behaviors**  
- Merge base + environment overrides; JSON-schema validation; precedence rules; atomic version creation; coordinated hot-reload w/ rollback on failure; change tracking w/ who/what/when; audit logging.  

#### 3.1.7 Monitoring, Logging & Observability (cross-cutting)
**Role**: Centralize metrics, health, alerts, audit trails.  
**Requirements**  
- Metrics: processing/latency per symbol/service; success rates per bridge; SLA violations; model performance trends.  
- Alerts: performance (SLA), trading (VaR breach, correlation spike), system (bridge failures).  
- Audit: configuration access/changes; message delivery/acks; lifecycle events.  

#### 3.1.8 Persistence (cross-cutting)
**Role**: Low-latency caches and durable records for analytics/reports and audits.  
**Requirements**  
- Redis for last price, currency strength (TTL=300s), and transient state; durable storage for risk/attribution reports and configuration audit logs (storage tech not specified by Blueprint).  

### 3.2 Performance Requirements
- **Market Data SLA**: ≤ **100 ms** per message (alert on breach).  
- **Signal Inference Timeout**: **5 s** with circuit-breaker and safe fallback.  
- **Ack Timeout (MT4)**: **30 s** expected; retry/backoff and escalate on miss.  
- **Significant Move Threshold**: **0.1 pip** (majors) for strength/correlation updates.  
- **Risk Thresholds**: VaR breach ≥ **5%**; correlation spike ≥ **0.8**; drawdown limit **15%** (alerts).  
- **Cache TTL**: currency strength **300 s**.  

### 3.3 Design Constraints
- **Protocol Compatibility**: MT4 requires CSV payloads; JSON↔CSV conversion mandated for target=MT4.  
- **Bridge Options**: dll_socket / named_pipes / memory_mapped / file_based; hierarchical fallback with circuit-breaker & exponential backoff.  
- **Tech Dependencies**: Redis, RabbitMQ and/or Redis pub/sub; JWT for API auth; schema-validated YAML configs; Python service stack.  

---

## 4. Traceability Summary (Manual vs. Spec vs. Both)
- All concrete service behaviors, thresholds, and interfaces listed here originate from the **Blueprint** (primary “spec” for this SRS). Where thresholds/behaviors are marked as coming from the *Monograph – Updated/Remediated*, that information is cited **via** the Blueprint’s own references (i.e., “spec → references”).  

---

## 5. Relationship Mapping & Flows (hierarchical/sequential/cross-cutting)

### 5.1 Core End-to-End Flow (Textual)
1) **Market Data Service** → publishes `MarketDataModel` (SLA-guarded, cleansed; Redis updates for last price/strength).  
2) **Signal Generation Service** → consumes market data & calendar events → features/ML ensemble/CNN → validates & explains → publishes `SignalModel` (UUID, strategy ID, confidence).  
3) **Communication Service** → selects optimal bridge → adapts JSON→CSV for MT4 → delivers to EA → tracks ack (≤30 s), retries/failover if needed.  
4) **Analytics Service** → ingests positions/outcomes + market data → computes VaR/CVaR, correlation/regime, attribution → alerts on breaches and produces reports.  
5) **Configuration Service** → supplies validated, versioned configs to all services; watches files/API updates → coordinates hot-reload & rollback; logs audits/changes.  

### 5.2 Cross-Cutting Relationships
- **Monitoring/Alerts** span all services (SLA, bridge health, VaR/correlation thresholds, config failures).  
- **Redis** spans data, signal, and strength caching; **Audit & Change Logs** span configuration and communication lifecycles.  

---

## 6. Completeness Check (against the Blueprint)
- Represented systems/subsystems from the Blueprint: **Market Data**, **Signal Generation**, **Communication (bridges, adaptation, ack)**, **Analytics (risk/attribution)**, **Configuration (versioning, hot-reload, audit)** — **Yes**.  
- Layers explicitly separated and populated using Blueprint content — **Yes** (Data Sources; Data Processing (Python); Communication/Bridges; Execution Integration; Persistence; Config Mgmt; Monitoring/Logging).  
- Items referenced but **not** detailed in the Blueprint are flagged as external/contractual (e.g., Excel/VBA internals; MT4 EA logic; long-term data store schemas).  
- Duplicates consolidated; all Blueprint references preserved in section-level traceability.

---

### Appendix A — Decomposition Tables (Condensed)

**A.1 Subsystem to Component Map (sample)**  
- *Market Data Service*: WebSocketManager; ConnectionPool; LatencyTracker; OutlierDetector; DataInterpolator; CorrelationMatrixCalculator; EigenvalueDecomposer; MetricsCollector; Redis client.  
- *Signal Generation Service*: Ensemble Models (RF/SVM/NN); CNN + attention; FeatureProcessors; RCI System; EconomicCalendarClient; StatisticalSignificanceValidator; BacktestingEngine; MonteCarloSimulator; SHAPExplainer; DecisionTreeVisualizer; NLPExplanationGenerator; Lifecycle hooks.  
- *Communication Service*: BridgeManager; dll_socket/named_pipes/memory_mapped/file_based; JSONCSVConverter; MessageSerializer; CircuitBreaker; ExponentialBackoffPolicy; MessageTracker; AcknowledgmentValidator; FailoverCoordinator.  
- *Analytics Service*: VaRCalculator; CVaRCalculator; DynamicCorrelationAnalyzer; RegimeDetector; FactorAnalyzer; ReturnDecomposer; MLFeedbackIntegrator; MPTOptimizer; OutcomeTracker; ReportGenerator; FeedbackPipeline; PerformanceMonitor.  
- *Configuration Service*: ConfigurationStore; ConfigurationVersionManager; FileWatcher; HotReloadCoordinator; JSONSchemaValidator; ConfigurationConflictResolver; ConfigurationDistributor; ConfigAcknowledgmentTracker; ConfigurationChangeTracker; ConfigurationAuditLogger.  

**A.2 Interface/Contract Highlights (sample)**  
- **To MT4**: CSV payloads + UUID + ack semantics; bridge hierarchy + retries + backoff; 30-s ack window.  
- **To Cache**: Redis keys for `last_price:{symbol}`, `currency_strength:{symbol}` with TTL=300s.  
- **To Risk**: `RiskMetrics` packages with matrices/regimes; thresholds generate alerts.  
- **To Config Consumers**: validated versioned blobs; hot-reload orchestration; full audit chain.  

---
