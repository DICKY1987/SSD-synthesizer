# Software Requirements Specification (SRS)
## HUEY_P_ClaudeCentric Trading System Architecture

**Version:** 1.0  
**Date:** August 26, 2025  
**Document Type:** IEEE 830-Style Architecture Specification

---

## 4. Complete System Architecture Decomposition

### 4.1 System Layer Mapping

```
┌─────────────────────────────────────────────────────────────────┐
│                    PRESENTATION & INTERFACE LAYER              │
├─────────────────────────────────────────────────────────────────┤
│ • MetaTrader 4 Terminal (MQL4 Expert Advisors)                │
│ • Excel-based Configuration Interface                          │
│ • Monitoring Dashboards                                        │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                    COMMUNICATION & BRIDGE LAYER                │
├─────────────────────────────────────────────────────────────────┤
│ • C++ DLL Bridge (SocketBridge.dll)                           │
│ • Hierarchical Communication System                            │
│   - DLL+Socket Bridge (Primary)                               │
│   - Named Pipes Bridge (Secondary)                            │
│   - File-based Bridge (Tertiary)                              │
│ • Bridge Health Monitor                                        │
│ • Protocol Adaptation (JSON ↔ CSV)                            │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                    PYTHON BACKEND SERVICES LAYER               │
├─────────────────────────────────────────────────────────────────┤
│ • Signal Generation Service (ML Ensemble + Explainable AI)    │
│ • Market Data Service (WebSocket + Currency Strength)         │
│ • Analytics Service (VaR/CVaR + Risk Management)              │
│ • Communication Service (Message Broker + Persistence)        │
│ • Configuration Service (Hot-reload + Version Control)        │
│ • Alert Router (Classification + Escalation)                  │
│ • Feedback Pipeline (ML Retraining Triggers)                  │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                    DATA PROCESSING & ANALYTICS LAYER           │
├─────────────────────────────────────────────────────────────────┤
│ • Economic Calendar Integration (RCI Strategy IDs)            │
│ • Risk Calculation Engine (Excel-based + Python hybrid)       │
│ • Performance Attribution Analysis                            │
│ • Correlation Matrix Calculator                               │
│ • Monte Carlo Simulation Engine                               │
│ • Feature Engineering Pipeline                                │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                    PERSISTENCE & STATE MANAGEMENT LAYER        │
├─────────────────────────────────────────────────────────────────┤
│ • Lifecycle Manager (UUID-based State Tracking)               │
│ • Database Layer (SQLite + Schema Management)                 │
│ • Configuration Storage (YAML + CSV + Version Control)        │
│ • Redis Cache (Currency Strength + TTL Management)            │
│ • File-based Storage (CSV exports + Atomic operations)        │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                    INFRASTRUCTURE & DEPLOYMENT LAYER           │
├─────────────────────────────────────────────────────────────────┤
│ • Docker Containerization (Python services isolation)         │
│ • PowerShell Deployment Scripts                               │
│ • System Health Monitoring                                    │
│ • Backup & Recovery System                                    │
│ • Environment Segregation (Simulation vs. Live)               │
└─────────────────────────────────────────────────────────────────┘
```

### 4.2 Component Relationship Matrix

| Source Component | Target Component | Data Flow Type | Trigger | Source Doc |
|------------------|------------------|----------------|---------|------------|
| Market Data Service | Signal Generation Service | MarketDataModel events | Price change > 0.1 pip | U_1, U_2 |
| Signal Generation Service | Communication Service | SignalModel with UUID | ML confidence > 0.7 | U_1, U_3 |
| Communication Service | C++ DLL Bridge | JSON signals | Message queue processing | U_1, U_2 |
| C++ DLL Bridge | MQL4 Expert Advisors | CSV-formatted signals | Bridge polling | Manual Section 02 |
| Expert Advisors | Database | Trade confirmations | Order execution | Manual Section 06 |
| Economic Calendar | Strategy ID Generator | Calendar events | Event import | Economic Calendar Doc |
| Risk Calculator | Expert Advisors | Adjusted parameters | Risk score changes | Economic Calendar Doc |
| Analytics Service | Alert Router | Risk threshold breaches | VaR/Correlation limits | U_1, U_3 |
| Configuration Service | All Services | Configuration updates | Hot-reload triggers | U_1, Manual Section 04 |
| Lifecycle Manager | All Components | State synchronization | UUID state changes | U_3, U_2 |

### 4.3 Data Flow Sequence Diagrams

#### 4.3.1 Signal Generation to Trade Execution Flow

```
[Market Data Provider] 
        ↓ WebSocket feed
[Market Data Service] 
        ↓ MarketDataModel event (if >0.1 pip change)
[Signal Generation Service] 
        ↓ ML ensemble processing (5s timeout)
        ↓ Economic calendar strategy ID generation
        ↓ SHAP explainability analysis
[SignalModel with UUID] 
        ↓ Message queue publication
[Communication Service] 
        ↓ Bridge selection (hierarchical fallback)
        ↓ JSON→CSV protocol adaptation
[C++ DLL Bridge] 
        ↓ Thread-safe queue management
        ↓ MQL4 function calls (GetNextSignal)
[Expert Advisor (Currency-specific)] 
        ↓ CSV parameter lookup
        ↓ Risk management validation
        ↓ OrderSend() execution
[MT4 Trading Server] 
        ↓ Trade confirmation
[Lifecycle Manager] 
        ↓ UUID state update (EXECUTED → FILLED)
[Database Persistence]
```

#### 4.3.2 Risk Management Feedback Loop

```
[Trade Execution Confirmation] 
        ↓ Trade outcome classification (6 categories)
[Feedback Pipeline] 
        ↓ Performance attribution analysis
[Analytics Service] 
        ↓ VaR/CVaR recalculation
        ↓ Correlation matrix update
        ↓ ML model performance assessment
[Risk Threshold Monitoring] 
        ↓ Alert generation (if thresholds breached)
[Alert Router] 
        ↓ Severity/category classification
        ↓ Time-based routing rules
[Excel Risk Calculator] 
        ↓ Parameter adjustment calculation
        ↓ Position sizing modification
[Configuration Service] 
        ↓ Hot-reload parameter updates
[Expert Advisors] 
        ↓ Adjusted trading behavior
```

### 4.4 Module-Level Component Breakdown

#### 4.4.1 Signal Generation Service Modules

**Source**: Spec U_1, Section 1.1.1 + Spec U_3, Section 3.1

```
SignalGenerationService/
├── ensemble_models/
│   ├── RandomForestModel
│   ├── SVMModel  
│   ├── NeuralNetworkModel
│   └── CNNPatternRecognition
├── feature_engineering/
│   ├── TechnicalIndicatorCalculator
│   ├── MarketMicrostructureAnalyzer
│   ├── SentimentDataProcessor
│   └── AttentionMechanism
├── explainability/
│   ├── SHAPExplainer
│   ├── DecisionTreeVisualizer
│   └── NLPExplanationGenerator
├── validation/
│   ├── StatisticalSignificanceValidator
│   ├── BacktestingEngine
│   └── MonteCarloSimulator
├── strategy_integration/
│   ├── RegionalCountryImpactSystem (RCI)
│   └── EconomicCalendarClient
└── plugin_management/
    ├── PluginResourceManager
    ├── PluginSandbox
    └── ResourceMonitor
```

#### 4.4.2 Communication Bridge Modules

**Source**: Manual Section 02 + Spec U_2, Section 2.1

```
CommunicationBridge/
├── dll_bridge/
│   ├── SocketBridge.dll (C++ implementation)
│   ├── ListenerThread
│   ├── WorkerThread
│   └── MessageQueue (thread-safe FIFO)
├── bridge_manager/
│   ├── HierarchicalBridgeSelector
│   ├── FailoverCoordinator
│   └── BridgeHealthMonitor
├── protocol_adaptation/
│   ├── JSONCSVConverter
│   ├── MessageSerializer
│   └── AcknowledgmentValidator
├── persistence/
│   ├── MessagePersistenceManager
│   ├── DeadLetterQueue
│   └── DeliveryTracker
└── error_handling/
    ├── CircuitBreaker
    ├── ExponentialBackoffPolicy
    └── RetryManager
```

#### 4.4.3 MQL4 Expert Advisor Framework Modules  

**Source**: Manual Section 01

```
MQL4Framework/
├── expert_advisors/
│   ├── HUEY_P_MQL4_EURUSD_EA.mq4 (30 currency pairs)
│   └── [29 other currency-specific EAs]
├── include_libraries/
│   ├── CommunicationManager.mqh
│   ├── TradingCore.mqh
│   ├── ExecutionEngine.mqh
│   ├── FileManager.mqh
│   ├── TimeManager.mqh
│   ├── ErrorRecovery.mqh
│   └── Logging.mqh
├── data_files/
│   ├── all_10_parameter_sets.csv
│   ├── signal_id_mapping.csv
│   ├── reentry_close_result_mapping.csv
│   └── current_signal.csv (fallback communication)
└── event_handlers/
    ├── OnInit() (initialization & CSV loading)
    ├── OnDeinit() (cleanup & graceful shutdown)
    └── OnTick() (lightweight polling & execution)
```

### 4.5 Configuration Management Component Hierarchy

**Source**: Manual Section 04 + Spec U_1, Section 1.1.5 + Spec U_2, Section 2.4

#### 4.5.1 5-Tier Configuration Architecture

```
ConfigurationManagement/
├── tier_1_excel_overrides/
│   ├── EmergencyParameterOverrides.xlsx
│   └── TradingParameterAdjustments.xlsx
├── tier_2_runtime_updates/
│   ├── APIConfigurationEndpoint
│   ├── HotReloadTriggers
│   └── TemporaryParameterChanges
├── tier_3_environment_variables/
│   ├── TRADING_ENV (production/development)
│   ├── DATABASE_PATH
│   └── REDIS_URL
├── tier_4_configuration_files/
│   ├── system_config.yaml
│   ├── risk_config.yaml
│   ├── ml_config.yaml
│   └── environments/
│       ├── production.yaml
│       ├── development.yaml
│       └── simulation.yaml
├── tier_5_system_defaults/
│   ├── HardcodedDefaults.py
│   └── BaselineParameters.yaml
└── management_components/
    ├── ConfigurationVersionManager
    ├── HotReloadCoordinator
    ├── ConflictResolver
    ├── SchemaValidator
    └── AuditLogger
```

#### 4.5.2 Configuration Resolution Process

```python
# Configuration Resolution Logic (Source: Spec U_2, Section 2.4)
def resolve_configuration(key: str) -> ConfigurationValue:
    """5-tier hierarchical precedence resolution"""
    
    # Collect from all tiers (highest precedence first)
    tier_values = {
        'excel_overrides': get_excel_override(key),      # Precedence 1
        'runtime_updates': get_runtime_update(key),      # Precedence 2  
        'environment_vars': get_env_variable(key),       # Precedence 3
        'config_files': get_config_file_value(key),     # Precedence 4
        'system_defaults': get_default_value(key)       # Precedence 5
    }
    
    # Apply TTL expiration rules
    for tier, value in tier_values.items():
        if has_expired(tier, key, value):
            tier_values[tier] = None
    
    # Select winning value (highest precedence)
    winning_value = next((v for v in tier_values.values() if v is not None), None)
    
    # Conflict resolution and validation
    conflicts = detect_conflicts(tier_values)
    validation_result = validate_configuration(key, winning_value)
    
    return ConfigurationValue(
        key=key,
        value=winning_value,
        precedence=get_winning_precedence(tier_values),
        conflicts=conflicts,
        validation=validation_result
    )
```

### 4.6 Cross-Cutting Concerns Implementation

#### 4.6.1 UUID-Based Lifecycle Tracking

**Source**: Spec U_3, Section 3.3 + Spec U_2, Section 2.3

```
LifecycleManagement/
├── uuid_generation/
│   ├── UUIDValidator
│   └── SignalUUIDGenerator
├── state_machine/
│   ├── LifecycleState enum:
│   │   ├── GENERATED
│   │   ├── VALIDATED  
│   │   ├── TRANSMITTED
│   │   ├── ACKNOWLEDGED
│   │   ├── EXECUTED
│   │   ├── FILLED
│   │   ├── MONITORED
│   │   ├── CLOSED
│   │   ├── ANALYZED
│   │   └── ORPHANED
│   └── StateTransitionValidator
├── cross_system_sync/
│   ├── PythonStateTracker
│   ├── MT4StateTracker
│   ├── ExcelStateTracker
│   └── ConflictResolver (timestamp-based authority)
├── persistence/
│   ├── SQLiteLifecycleStore
│   ├── TransactionManager
│   └── ReconciliationEngine (1-hour intervals)
└── monitoring/
    ├── OrphanDetector (7-day threshold)
    ├── StateAuditLogger
    └── SynchronizationReporter
```

#### 4.6.2 Economic Calendar Strategy ID System

**Source**: Economic Calendar Strategy ID Generation.txt

```
EconomicCalendarIntegration/
├── data_ingestion/
│   ├── CalendarCSVParser (ff_calendar_thisweek.csv)
│   ├── CountryImpactFilter (exclude CHF, Low impact)
│   └── EventValidator
├── strategy_id_generation/
│   ├── RegionalCountryImpactSystem/
│   │   ├── region_mapping/
│   │   │   ├── North America (1): USA(01), CAD(02), MXN(03)
│   │   │   ├── Europe (2): EUR(01), GBP(02)  
│   │   │   ├── Asia-Pacific (3): JPY(01), AUD(02), NZD(03), etc.
│   │   │   ├── Latin America (4): BRL(01)
│   │   │   ├── Middle East/Africa (5): ZAR(01), TRY(02), RUB(03)
│   │   │   └── Other (9): [Catchall]
│   │   ├── impact_encoding/
│   │   │   ├── Medium Impact (2)
│   │   │   └── High Impact (3)
│   │   └── checksum_calculation/
│   │       └── (region + country + impact) % 10
│   └── StrategyIDValidator (5-digit format validation)
├── parameter_mapping/
│   ├── StrategyToParameterSetMapper
│   ├── ParameterSetLookupTable
│   └── DefaultParameterFallback
└── excel_integration/
    ├── VBAHashCalculator (alternative implementation)
    ├── CollisionDetector
    └── TestSuiteGenerator
```

### 4.7 Error Handling & Resilience Architecture

#### 4.7.1 Circuit Breaker Implementation Matrix

**Source**: Spec U_2, Section 2.1 + Spec U_3

| Component | Failure Threshold | Timeout Period | Recovery Requirement | Source Reference |
|-----------|------------------|----------------|---------------------|------------------|
| DLL+Socket Bridge | 3 consecutive failures | 30 seconds | 10 consecutive successes (5-min window) | U_2, Section 2.1.1 |
| Named Pipes Bridge | 5 consecutive failures | 60 seconds | 15 consecutive successes (10-min window) | U_2, Section 2.1.1 |  
| File-based Bridge | 10 consecutive failures | 120 seconds | 20 consecutive successes (15-min window) | U_2, Section 2.1.1 |
| Signal Generation | 3 consecutive timeouts | 30 seconds | 5 successful generations | U_3, Section 3.1 |
| Market Data Feed | 5 connection failures | 60 seconds | 10 successful data points | U_1, Section 1.1.2 |
| ML Model Inference | 3 consecutive failures | 30 seconds | 5 successful predictions | U_1, Section 1.1.1 |

#### 4.7.2 Fallback Mechanism Hierarchy

```
ErrorHandling/
├── primary_operations/
│   ├── DLL+SocketBridge → NamedPipesBridge → FileBasedBridge
│   ├── MLEnsemble → RuleBasedSignals → ManualOverride  
│   ├── LiveMarketData → CachedData → HistoricalData
│   └── DatabasePersistence → FilePersistence → InMemoryStorage
├── recovery_procedures/
│   ├── ExponentialBackoffPolicy
│   ├── CircuitBreakerManager
│   ├── HealthCheckScheduler
│   └── FailoverCoordinator
├── alert_escalation/
│   ├── AutomaticFailover → OperatorNotification → ManualIntervention
│   ├── SystemDegradation → PerformanceAlert → CriticalAlert  
│   └── DataQualityIssues → ValidationAlert → DataSourceSwitch
└── simulation_isolation/
    ├── EnvironmentValidator
    ├── DatabasePathIsolation
    ├── BridgeDisconnection
    └── MockDataGeneration
```

---

## 5. Traceability Matrix

### 5.1 Source Document Coverage

| System Component | Manual Reference | Specification Reference | Combined Requirements |
|------------------|------------------|------------------------|----------------------|
| **Python Backend Services** | Section 03 | U_1 (Complete), U_3 (Detailed) | ✓ Comprehensive |
| **C++ Communication Bridge** | Section 02 (Basic) | U_2 (Detailed Architecture) | ✓ Comprehensive |  
| **MQL4 Expert Advisors** | Section 01 (Complete) | - | ✓ Complete from Manual |
| **Configuration Management** | Section 04 (Basic) | U_1 (Detailed), U_2 (Advanced) | ✓ Enhanced by Spec |
| **Economic Calendar Integration** | - | Economic Calendar Doc (Complete) | ✓ Complete from Spec |
| **Database Schema** | Section 06 (API Contract) | U_3 (Enhanced) | ✓ Comprehensive |
| **Deployment & Operations** | Section 05 (Complete) | - | ✓ Complete from Manual |
| **Testing Strategy** | TESTING_STRATEGY.md | - | ✓ Complete from Manual |
| **Backup & Recovery** | BACKUP_AND_RECOVERY.md | - | ✓ Complete from Manual |
| **Risk Management** | - | Economic Calendar Doc (Excel-based) | ✓ Complete from Spec |

### 5.2 Requirements Enhancement by Specifications

**Areas where Specifications significantly enhance Manual coverage:**

1. **Communication Architecture** (Spec U_2):
   - Added hierarchical bridge fallback with quantitative thresholds
   - Detailed state machine implementation with circuit breakers
   - Message persistence with delivery guarantees
   - UUID-based lifecycle management with cross-system synchronization

2. **Service Architecture** (Spec U_3):  
   - Plugin-based resource management with sandbox isolation
   - Bridge health monitoring with 5-second polling intervals
   - Alert routing with severity classification and escalation chains
   - ML feedback pipeline with automated retraining triggers

3. **Core Services** (Spec U_1):
   - Ensemble ML models with explainable AI (SHAP, decision trees)
   - VaR/CVaR calculation with Monte Carlo simulation
   - Dynamic correlation analysis with regime detection
   - Hot-reload configuration management with atomic updates

4. **Economic Calendar Integration** (Economic Calendar Doc):
   - 5-digit Regional-Country-Impact (RCI) strategy ID system
   - Excel-based risk calculation with parameter adjustment formulas
   - Country/impact filtering logic (exclude CHF, Low impact)
   - Time-based trading filters around economic events

### 5.3 Gap Analysis

**Areas covered only in Manual (not enhanced by Specifications):**
- MQL4 Expert Advisor implementation details
- PowerShell deployment scripts and procedures  
- Docker containerization setup and management
- Backup and recovery operational procedures
- Testing methodologies and validation approaches

**Areas covered only in Specifications (new additions):**
- Plugin sandbox architecture with resource limits
- Advanced circuit breaker implementations
- Cross-system lifecycle synchronization mechanisms
- Economic calendar-based strategy ID generation
- Excel-based risk management calculations

---

This comprehensive SRS document provides complete traceability from the source documents to specific architectural requirements, ensuring that all system components, their relationships, and implementation constraints are fully captured and mapped according to IEEE 830 standards.