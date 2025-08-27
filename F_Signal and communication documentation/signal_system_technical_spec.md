# MT4 Signal System - Technical Specification Document

**Project Name:** MT4 Multi-Source Signal Execution System  
**Document Version:** 1.0  
**Date:** August 15, 2025  
**Status:** Final Specification  
**Document Classification:** Internal Technical Documentation

## INPUT_BLOCK

```yaml
# 1. Core Details
business_domain: "Financial Services - Algorithmic Trading"
project_name: "MT4 Multi-Source Signal Execution System"
goals_and_success_criteria: |
  - Achieve sub-10ms signal processing latency (excluding broker execution)
  - Support 30 concurrent currency pair EAs with 99.9% signal delivery reliability
  - Implement risk-adaptive parameter management with 10 distinct risk profiles
  - Provide three-tier communication failover ensuring zero signal loss
  - Enable reentry logic for failed/partial trades with performance tracking
stakeholders_and_owners:
  - name: "Trading System Architect"
    role: "Principal Systems Architect"
    email: "architect@trading.system"
  - name: "Risk Management Team"
    role: "Risk Control"
    email: "risk@trading.system"

# 2. Technical Context
operating_environments: "Windows 10/11; MT4 Terminal; Local development and production"
compliance_regulatory_context: "Financial trading regulations; Risk management compliance"
data_classification: "Internal, Trading Signals, Financial Data"
performance_reliability_targets:
  SLOs: "99.9% signal delivery success rate; 99.5% trade execution success rate"
  latency_budgets: "Signal processing < 10ms; Communication failover < 100ms"
integration_points:
  - system: "MT4 Terminal"
    interface: "MQL4 EA Integration"
    purpose: "Trade execution and market data"
  - system: "Python Analytics Engine"
    interface: "TCP Socket/Named Pipes/File System"
    purpose: "Signal generation and ML analytics"
  - system: "Economic Calendar System"
    interface: "CSV Data Feed"
    purpose: "News-based signal generation"

# 3. Diagram Inputs
diagram_inputs:
  views: ["Context", "Container", "Component", "Dataflow", "Deployment"]
  components: ["Signal Generator", "Strategy Mapper", "Parameter Resolver", "Communication Bridge", "MT4 EA", "Risk Manager", "Reentry Logic", "Analytics Engine"]
  interactions:
    - "External signal sources send signals via three-tier communication"
    - "Strategy Mapper resolves strategy ID to parameter set ID"
    - "Parameter Resolver loads risk management parameters"
    - "MT4 EA executes trades with resolved parameters"
    - "Reentry Logic handles failed/partial trades"
```

---

## Table of Contents

1. [Introduction](#10-introduction)
   - 1.1 [Business Goals & Success Criteria](#11-business-goals--success-criteria)
   - 1.2 [Scope (In/Out)](#12-scope-inout)
   - 1.3 [Stakeholders & Owners](#13-stakeholders--owners)
   - 1.4 [Definitions, Acronyms, and Abbreviations](#14-definitions-acronyms-and-abbreviations)

2. [System Architecture](#20-system-architecture)
   - 2.1 [Architectural Goals & Constraints](#21-architectural-goals--constraints)
   - 2.2 [Architecture Diagrams](#22-architecture-diagrams)

3. [Functional & Non-Functional Requirements](#30-functional--non-functional-requirements)
   - 3.1 [Functional Requirements](#31-functional-requirements)
   - 3.2 [Performance & Reliability](#32-performance--reliability)
   - 3.3 [Scalability & Capacity Planning](#33-scalability--capacity-planning)
   - 3.4 [Security Architecture](#34-security-architecture)
   - 3.5 [Accessibility & Localization](#35-accessibility--localization)
   - 3.6 [Observability](#36-observability)

4. [Data Architecture](#40-data-architecture)
   - 4.1 [Data Models](#41-data-models)
   - 4.2 [Data Governance](#42-data-governance)

---

## 1.0 Introduction

### 1.1 Business Goals & Success Criteria

**Primary Business Goals:**
1. **Signal Processing Performance**: Achieve sub-10ms signal processing latency (excluding broker execution time)
2. **Reliability**: Maintain 99.9% signal delivery success rate across all communication channels
3. **Scalability**: Support 30 concurrent currency pair Expert Advisors (EAs) simultaneously
4. **Risk Management**: Implement 10 distinct risk profiles with dynamic parameter selection
5. **Fault Tolerance**: Provide three-tier communication failover ensuring zero signal loss
6. **Trade Recovery**: Enable intelligent reentry logic for failed/partial trades

**Success Criteria:**
- Signal-to-execution latency under 10ms (measured from signal receipt to MT4 order placement)
- 99.5% trade execution success rate post-validation
- Support for 4 distinct signal sources (AI/ML, Technical, Manual, Economic Calendar)
- Zero data loss during communication channel failures
- Complete audit trail for all signals and executions

### 1.2 Scope (In/Out)

**In Scope:**
- Multi-source signal generation and processing
- Strategy ID to parameter set mapping system
- Three-tier communication failover (Socket → Named Pipes → File System)
- Risk-adaptive parameter management (10 parameter sets)
- MT4 EA integration for 30 currency pairs
- Reentry logic for failed/partial trades
- SQLite-based state tracking and analytics
- Python-based signal analytics and generation
- Real-time validation and error handling

**Out of Scope:**
- Broker selection and account management
- Market data provision (relies on MT4 broker feed)
- Portfolio optimization across multiple accounts
- Web-based user interface development
- Mobile application development
- Integration with external portfolio management systems

### 1.3 Stakeholders & Owners

| Role | Name | Responsibilities | Contact |
|------|------|------------------|---------|
| Principal Systems Architect | Trading System Architect | Overall system design, technical decisions | architect@trading.system |
| Risk Management Lead | Risk Management Team | Parameter set definitions, risk validation | risk@trading.system |
| Development Team Lead | Development Team | Implementation, testing, deployment | dev@trading.system |
| Operations Lead | Operations Team | System monitoring, maintenance | ops@trading.system |

### 1.4 Definitions, Acronyms, and Abbreviations

| Term | Definition |
|------|------------|
| **EA** | Expert Advisor - MT4 automated trading program |
| **MQL4** | MetaQuotes Language 4 - Programming language for MT4 |
| **Strategy ID** | Unique identifier mapping signals to parameter sets |
| **Parameter Set** | Risk management configuration (stop loss, take profit, etc.) |
| **Signal UUID** | Universally Unique Identifier for signal tracking |
| **Three-Tier Communication** | Socket → Named Pipes → File System failover |
| **Reentry Logic** | System for handling failed/partial trade scenarios |
| **RCI System** | Regional-Country-Impact identifier system |
| **SQLite State Tracking** | Database for signal and execution audit trail |

---

## 2.0 System Architecture

### 2.1 Architectural Goals & Constraints

**Architectural Goals:**
1. **Modularity**: Support multiple independent signal sources
2. **Reliability**: Three-tier communication failover with automatic recovery
3. **Performance**: Sub-10ms signal processing with minimal overhead
4. **Maintainability**: Hybrid modular procedural programming approach
5. **Auditability**: Complete signal-to-execution tracking
6. **Risk Control**: Dynamic parameter selection based on signal characteristics

**Technical Constraints:**
1. **Platform Limitation**: MQL4 language only (no MQL5 features)
2. **Native Functions Only**: No non-native functions unless explicitly specified
3. **File System Access**: Limited to MT4 Files directory structure
4. **Communication Protocols**: TCP, Named Pipes, and File-based only
5. **Database**: SQLite for state persistence (lightweight, embedded)

**Design Principles:**
- **Fail-Safe**: System defaults to most conservative parameters on errors
- **Idempotent**: Signal processing produces consistent results
- **Atomic**: File operations use atomic write patterns (temp → rename)
- **Stateless**: Each signal processed independently
- **Traceable**: Every operation logged with correlation IDs

### 2.2 Architecture Diagrams

#### 2.2.1 System Context Diagram

```xml
<mxfile host="drawio" modified="2025-08-15" agent="5.0" version="24.6.4">
  <diagram id="system-context" name="System Context">
    <mxGraphModel dx="1422" dy="794" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="827" pageHeight="1169">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <mxCell id="system-core" value="MT4 Signal System" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=14;fontStyle=1" vertex="1" parent="1">
          <mxGeometry x="350" y="300" width="200" height="100" as="geometry"/>
        </mxCell>
        <mxCell id="ai-signals" value="AI/ML Signal&#xa;Generator" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6" vertex="1" parent="1">
          <mxGeometry x="100" y="150" width="120" height="60" as="geometry"/>
        </mxCell>
        <mxCell id="technical-signals" value="Technical&#xa;Indicator System" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6" vertex="1" parent="1">
          <mxGeometry x="100" y="250" width="120" height="60" as="geometry"/>
        </mxCell>
        <mxCell id="calendar-signals" value="Economic&#xa;Calendar System" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6" vertex="1" parent="1">
          <mxGeometry x="100" y="350" width="120" height="60" as="geometry"/>
        </mxCell>
        <mxCell id="manual-signals" value="Manual Entry&#xa;Interface" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6" vertex="1" parent="1">
          <mxGeometry x="100" y="450" width="120" height="60" as="geometry"/>
        </mxCell>
        <mxCell id="mt4-terminal" value="MT4 Terminal&#xa;(30 Currency EAs)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656" vertex="1" parent="1">
          <mxGeometry x="650" y="300" width="120" height="100" as="geometry"/>
        </mxCell>
        <mxCell id="broker" value="Forex Broker&#xa;Execution" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450" vertex="1" parent="1">
          <mxGeometry x="650" y="500" width="120" height="60" as="geometry"/>
        </mxCell>
        <mxCell id="analytics" value="Analytics &&#xa;Monitoring" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366" vertex="1" parent="1">
          <mxGeometry x="350" y="500" width="120" height="60" as="geometry"/>
        </mxCell>
        <!-- Connections -->
        <mxCell edge="1" parent="1" source="ai-signals" target="system-core">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell edge="1" parent="1" source="technical-signals" target="system-core">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell edge="1" parent="1" source="calendar-signals" target="system-core">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell edge="1" parent="1" source="manual-signals" target="system-core">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell edge="1" parent="1" source="system-core" target="mt4-terminal">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell edge="1" parent="1" source="mt4-terminal" target="broker">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell edge="1" parent="1" source="system-core" target="analytics">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

#### 2.2.2 Container Diagram

```xml
<mxfile host="drawio" modified="2025-08-15" agent="5.0" version="24.6.4">
  <diagram id="container-diagram" name="Container Architecture">
    <mxGraphModel dx="1422" dy="794" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="827" pageHeight="1169">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <mxCell id="signal-sources" value="Signal Sources" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;fontSize=12;fontStyle=1" vertex="1" parent="1">
          <mxGeometry x="50" y="100" width="150" height="400" as="geometry"/>
        </mxCell>
        <mxCell id="communication-bridge" value="Communication Bridge&#xa;(Socket/Pipes/Files)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=10" vertex="1" parent="1">
          <mxGeometry x="250" y="200" width="120" height="80" as="geometry"/>
        </mxCell>
        <mxCell id="signal-processor" value="Signal Processor&#xa;(Validation/Routing)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=10" vertex="1" parent="1">
          <mxGeometry x="250" y="320" width="120" height="80" as="geometry"/>
        </mxCell>
        <mxCell id="strategy-mapper" value="Strategy Mapper&#xa;(ID→ParameterSet)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontSize=10" vertex="1" parent="1">
          <mxGeometry x="420" y="200" width="120" height="80" as="geometry"/>
        </mxCell>
        <mxCell id="parameter-resolver" value="Parameter Resolver&#xa;(Risk Management)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontSize=10" vertex="1" parent="1">
          <mxGeometry x="420" y="320" width="120" height="80" as="geometry"/>
        </mxCell>
        <mxCell id="mt4-ea-cluster" value="MT4 EA Cluster&#xa;(30 Currency Pairs)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;fontSize=10" vertex="1" parent="1">
          <mxGeometry x="590" y="200" width="120" height="200" as="geometry"/>
        </mxCell>
        <mxCell id="reentry-engine" value="Reentry Logic Engine" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;fontSize=10" vertex="1" parent="1">
          <mxGeometry x="420" y="450" width="120" height="60" as="geometry"/>
        </mxCell>
        <mxCell id="sqlite-db" value="SQLite Database&#xa;(State Tracking)" style="shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#e1d5e7;strokeColor=#9673a6;fontSize=10" vertex="1" parent="1">
          <mxGeometry x="250" y="450" width="120" height="80" as="geometry"/>
        </mxCell>
        <!-- Configuration Files -->
        <mxCell id="config-files" value="Configuration Files&#xa;• signal_id_mapping.csv&#xa;• all_10_parameter_sets.csv&#xa;• reentry_configs/" style="shape=note;whiteSpace=wrap;html=1;backgroundOutline=1;fontColor=#000000;darkOpacity=0.05;fillColor=#FFF9B2;strokeColor=none;fillStyle=solid;direction=west;gradientDirection=north;gradientColor=#FFF2A1;shadow=1;size=20;pointerEvents=1;" vertex="1" parent="1">
          <mxGeometry x="50" y="550" width="200" height="100" as="geometry"/>
        </mxCell>
        <!-- Connections with labels -->
        <mxCell edge="1" parent="1" source="signal-sources" target="communication-bridge">
          <mxGeometry relative="1" as="geometry">
            <mxLabel component="label" relative="1" as="geometry" x="-0.5" y="0" value="Signals"/>
          </mxGeometry>
        </mxCell>
        <mxCell edge="1" parent="1" source="communication-bridge" target="signal-processor">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell edge="1" parent="1" source="signal-processor" target="strategy-mapper">
          <mxGeometry relative="1" as="geometry">
            <mxLabel component="label" relative="1" as="geometry" x="-0.5" y="0" value="Strategy ID"/>
          </mxGeometry>
        </mxCell>
        <mxCell edge="1" parent="1" source="strategy-mapper" target="parameter-resolver">
          <mxGeometry relative="1" as="geometry">
            <mxLabel component="label" relative="1" as="geometry" x="-0.5" y="0" value="Parameter Set ID"/>
          </mxGeometry>
        </mxCell>
        <mxCell edge="1" parent="1" source="parameter-resolver" target="mt4-ea-cluster">
          <mxGeometry relative="1" as="geometry">
            <mxLabel component="label" relative="1" as="geometry" x="-0.5" y="0" value="Execution Config"/>
          </mxGeometry>
        </mxCell>
        <mxCell edge="1" parent="1" source="mt4-ea-cluster" target="reentry-engine">
          <mxGeometry relative="1" as="geometry">
            <mxLabel component="label" relative="1" as="geometry" x="-0.5" y="0" value="Trade Results"/>
          </mxGeometry>
        </mxCell>
        <mxCell edge="1" parent="1" source="reentry-engine" target="sqlite-db">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell edge="1" parent="1" source="signal-processor" target="sqlite-db">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

#### 2.2.3 Component Diagram

```xml
<mxfile host="drawio" modified="2025-08-15" agent="5.0" version="24.6.4">
  <diagram id="component-diagram" name="Component Architecture">
    <mxGraphModel dx="1422" dy="794" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="827" pageHeight="1169">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <!-- Core Components -->
        <mxCell id="signal-trigger-handler" value="SignalTriggerHandler&#xa;• ProcessIncomingSignal()&#xa;• ValidateSignalFormat()&#xa;• GenerateSignalUUID()" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;align=left;fontSize=9" vertex="1" parent="1">
          <mxGeometry x="50" y="50" width="160" height="80" as="geometry"/>
        </mxCell>
        <mxCell id="strategy-resolver" value="StrategyResolver&#xa;• LookupStrategyMapping()&#xa;• LoadParameterSetConfig()&#xa;• ValidateParameterSet()" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;align=left;fontSize=9" vertex="1" parent="1">
          <mxGeometry x="250" y="50" width="160" height="80" as="geometry"/>
        </mxCell>
        <mxCell id="parameter-loader" value="ParameterSetLoader&#xa;• LoadParameterSet()&#xa;• ValidateRiskLimits()&#xa;• CalculatePositionSize()" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;align=left;fontSize=9" vertex="1" parent="1">
          <mxGeometry x="450" y="50" width="160" height="80" as="geometry"/>
        </mxCell>
        <mxCell id="signal-builder" value="SignalBuilder&#xa;• CreateTradeSignal()&#xa;• ApplyParameterOverrides()&#xa;• GenerateOrderComment()" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;align=left;fontSize=9" vertex="1" parent="1">
          <mxGeometry x="650" y="50" width="160" height="80" as="geometry"/>
        </mxCell>
        <!-- Communication Components -->
        <mxCell id="tcp-socket" value="TCPSocketHandler&#xa;• ConnectToSocket()&#xa;• SendBinaryMessage()&#xa;• HandleReconnection()" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;align=left;fontSize=9" vertex="1" parent="1">
          <mxGeometry x="50" y="200" width="160" height="80" as="geometry"/>
        </mxCell>
        <mxCell id="named-pipes" value="NamedPipeHandler&#xa;• OpenPipe()&#xa;• WriteMessage()&#xa;• HandlePipeErrors()" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;align=left;fontSize=9" vertex="1" parent="1">
          <mxGeometry x="250" y="200" width="160" height="80" as="geometry"/>
        </mxCell>
        <mxCell id="file-system" value="FileSystemHandler&#xa;• WriteAtomicFile()&#xa;• ReadSignalFile()&#xa;• CleanupTempFiles()" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;align=left;fontSize=9" vertex="1" parent="1">
          <mxGeometry x="450" y="200" width="160" height="80" as="geometry"/>
        </mxCell>
        <!-- MT4 Components -->
        <mxCell id="ea-core" value="CTradingEACore&#xa;• ProcessSignal()&#xa;• ExecuteTrade()&#xa;• ManagePositions()" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;align=left;fontSize=9" vertex="1" parent="1">
          <mxGeometry x="50" y="350" width="160" height="80" as="geometry"/>
        </mxCell>
        <mxCell id="bridge-interface" value="CBridgeInterface&#xa;• ReceiveSignal()&#xa;• SendResponse()&#xa;• HandleFailover()" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;align=left;fontSize=9" vertex="1" parent="1">
          <mxGeometry x="250" y="350" width="160" height="80" as="geometry"/>
        </mxCell>
        <mxCell id="reentry-logic" value="CReentryLogic&#xa;• AnalyzeTradeResult()&#xa;• DetermineReentryAction()&#xa;• ExecuteReentry()" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;align=left;fontSize=9" vertex="1" parent="1">
          <mxGeometry x="450" y="350" width="160" height="80" as="geometry"/>
        </mxCell>
        <!-- Data Components -->
        <mxCell id="csv-manager" value="CSVDataManager&#xa;• LoadMappingFile()&#xa;• LoadParameterSets()&#xa;• ValidateDataIntegrity()" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;align=left;fontSize=9" vertex="1" parent="1">
          <mxGeometry x="650" y="200" width="160" height="80" as="geometry"/>
        </mxCell>
        <mxCell id="sqlite-manager" value="SQLiteManager&#xa;• LogSignalEvent()&#xa;• TrackTradeExecution()&#xa;• QueryPerformance()" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;align=left;fontSize=9" vertex="1" parent="1">
          <mxGeometry x="650" y="350" width="160" height="80" as="geometry"/>
        </mxCell>
        <!-- Connections -->
        <mxCell edge="1" parent="1" source="signal-trigger-handler" target="strategy-resolver">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell edge="1" parent="1" source="strategy-resolver" target="parameter-loader">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell edge="1" parent="1" source="parameter-loader" target="signal-builder">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell edge="1" parent="1" source="signal-builder" target="tcp-socket">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell edge="1" parent="1" source="tcp-socket" target="named-pipes">
          <mxGeometry relative="1" as="geometry">
            <mxLabel component="label" relative="1" as="geometry" x="-0.5" y="0" value="Failover"/>
          </mxGeometry>
        </mxCell>
        <mxCell edge="1" parent="1" source="named-pipes" target="file-system">
          <mxGeometry relative="1" as="geometry">
            <mxLabel component="label" relative="1" as="geometry" x="-0.5" y="0" value="Failover"/>
          </mxGeometry>
        </mxCell>
        <mxCell edge="1" parent="1" source="file-system" target="bridge-interface">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell edge="1" parent="1" source="bridge-interface" target="ea-core">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell edge="1" parent="1" source="ea-core" target="reentry-logic">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell edge="1" parent="1" source="strategy-resolver" target="csv-manager">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell edge="1" parent="1" source="ea-core" target="sqlite-manager">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

#### 2.2.4 Dataflow Diagram

```xml
<mxfile host="drawio" modified="2025-08-15" agent="5.0" version="24.6.4">
  <diagram id="dataflow-diagram" name="Signal Processing Dataflow">
    <mxGraphModel dx="1422" dy="794" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="827" pageHeight="1169">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <!-- Data Stores -->
        <mxCell id="signal-mapping-store" value="D1: signal_id_mapping.csv&#xa;strategyId → parameterSetId" style="shape=partialRectangle;whiteSpace=wrap;html=1;left=0;right=0;fillColor=#f8cecc;strokeColor=#b85450;fontSize=10" vertex="1" parent="1">
          <mxGeometry x="50" y="400" width="180" height="50" as="geometry"/>
        </mxCell>
        <mxCell id="parameter-store" value="D2: all_10_parameter_sets.csv&#xa;Risk management configs" style="shape=partialRectangle;whiteSpace=wrap;html=1;left=0;right=0;fillColor=#f8cecc;strokeColor=#b85450;fontSize=10" vertex="1" parent="1">
          <mxGeometry x="280" y="400" width="180" height="50" as="geometry"/>
        </mxCell>
        <mxCell id="reentry-store" value="D3: reentry_configs/&#xa;Per-pair reentry rules" style="shape=partialRectangle;whiteSpace=wrap;html=1;left=0;right=0;fillColor=#f8cecc;strokeColor=#b85450;fontSize=10" vertex="1" parent="1">
          <mxGeometry x="510" y="400" width="180" height="50" as="geometry"/>
        </mxCell>
        <mxCell id="sqlite-store" value="D4: SQLite Database&#xa;Signal/execution tracking" style="shape=partialRectangle;whiteSpace=wrap;html=1;left=0;right=0;fillColor=#f8cecc;strokeColor=#b85450;fontSize=10" vertex="1" parent="1">
          <mxGeometry x="50" y="500" width="180" height="50" as="geometry"/>
        </mxCell>
        <!-- External Entities -->
        <mxCell id="signal-sources-entity" value="E1: Signal Sources&#xa;(AI/ML, Technical, Manual, News)" style="shape=partialRectangle;whiteSpace=wrap;html=1;left=0;right=0;fillColor=#e1d5e7;strokeColor=#9673a6;fontSize=10" vertex="1" parent="1">
          <mxGeometry x="50" y="50" width="200" height="50" as="geometry"/>
        </mxCell>
        <mxCell id="mt4-entity" value="E2: MT4 Terminal&#xa;(Trade execution)" style="shape=partialRectangle;whiteSpace=wrap;html=1;left=0;right=0;fillColor=#e1d5e7;strokeColor=#9673a6;fontSize=10" vertex="1" parent="1">
          <mxGeometry x="550" y="50" width="150" height="50" as="geometry"/>
        </mxCell>
        <!-- Processes -->
        <mxCell id="process-1" value="P1: Signal Reception&#xa;& Validation" style="ellipse;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=10" vertex="1" parent="1">
          <mxGeometry x="100" y="150" width="100" height="60" as="geometry"/>
        </mxCell>
        <mxCell id="process-2" value="P2: Strategy ID&#xa;Resolution" style="ellipse;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=10" vertex="1" parent="1">
          <mxGeometry x="90" y="280" width="100" height="60" as="geometry"/>
        </mxCell>
        <mxCell id="process-3" value="P3: Parameter Set&#xa;Loading" style="ellipse;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=10" vertex="1" parent="1">
          <mxGeometry x="320" y="280" width="100" height="60" as="geometry"/>
        </mxCell>
        <mxCell id="process-4" value="P4: Trade Signal&#xa;Building" style="ellipse;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=10" vertex="1" parent="1">
          <mxGeometry x="450" y="150" width="100" height="60" as="geometry"/>
        </mxCell>
        <mxCell id="process-5" value="P5: Trade Execution&#xa;& Monitoring" style="ellipse;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=10" vertex="1" parent="1">
          <mxGeometry x="575" y="150" width="100" height="60" as="geometry"/>
        </mxCell>
        <mxCell id="process-6" value="P6: Reentry Logic&#xa;Processing" style="ellipse;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=10" vertex="1" parent="1">
          <mxGeometry x="550" y="280" width="100" height="60" as="geometry"/>
        </mxCell>
        <!-- Data Flows -->
        <mxCell edge="1" parent="1" source="signal-sources-entity" target="process-1">
          <mxGeometry relative="1" as="geometry">
            <mxLabel component="label" relative="1" as="geometry" x="-0.5" y="0" value="Raw Signal"/>
          </mxGeometry>
        </mxCell>
        <mxCell edge="1" parent="1" source="process-1" target="process-2">
          <mxGeometry relative="1" as="geometry">
            <mxLabel component="label" relative="1" as="geometry" x="-0.5" y="0" value="Validated Signal"/>
          </mxGeometry>
        </mxCell>
        <mxCell edge="1" parent="1" source="process-2" target="signal-mapping-store">
          <mxGeometry relative="1" as="geometry">
            <mxLabel component="label" relative="1" as="geometry" x="-0.5" y="0" value="Strategy ID Lookup"/>
          </mxGeometry>
        </mxCell>
        <mxCell edge="1" parent="1" source="signal-mapping-store" target="process-2">
          <mxGeometry relative="1" as="geometry">
            <mxLabel component="label" relative="1" as="geometry" x="-0.5" y="0" value="Parameter Set ID"/>
          </mxGeometry>
        </mxCell>
        <mxCell edge="1" parent="1" source="process-2" target="process-3">
          <mxGeometry relative="1" as="geometry">
            <mxLabel component="label" relative="1" as="geometry" x="-0.5" y="0" value="Parameter Request"/>
          </mxGeometry>
        </mxCell>
        <mxCell edge="1" parent="1" source="process-3" target="parameter-store">
          <mxGeometry relative="1" as="geometry">
            <mxLabel component="label" relative="1" as="geometry" x="-0.5" y="0" value="Parameter Lookup"/>
          </mxGeometry>
        </mxCell>
        <mxCell edge="1" parent="1" source="parameter-store" target="process-3">
          <mxGeometry relative="1" as="geometry">
            <mxLabel component="label" relative="1" as="geometry" x="-0.5" y="0" value="Risk Config"/>
          </mxGeometry>
        </mxCell>
        <mxCell edge="1" parent="1" source="process-3" target="process-4">
          <mxGeometry relative="1" as="geometry">
            <mxLabel component="label" relative="1" as="geometry" x="-0.5" y="0" value="Complete Config"/>
          </mxGeometry>
        </mxCell>
        <mxCell edge="1" parent="1" source="process-4" target="process-5">
          <mxGeometry relative="1" as="geometry">
            <mxLabel component="label" relative="1" as="geometry" x="-0.5" y="0" value="Execution Signal"/>
          </mxGeometry>
        </mxCell>
        <mxCell edge="1" parent="1" source="process-5" target="mt4-entity">
          <mxGeometry relative="1" as="geometry">
            <mxLabel component="label" relative="1" as="geometry" x="-0.5" y="0" value="Trade Order"/>
          </mxGeometry>
        </mxCell>
        <mxCell edge="1" parent="1" source="mt4-entity" target="process-5">
          <mxGeometry relative="1" as="geometry">
            <mxLabel component="label" relative="1" as="geometry" x="-0.5" y="0" value="Execution Result"/>
          </mxGeometry>
        </mxCell>
        <mxCell edge="1" parent="1" source="process-5" target="process-6">
          <mxGeometry relative="1" as="geometry">
            <mxLabel component="label" relative="1" as="geometry" x="-0.5" y="0" value="Trade Outcome"/>
          </mxGeometry>
        </mxCell>
        <mxCell edge="1" parent="1" source="process-6" target="reentry-store">
          <mxGeometry relative="1" as="geometry">
            <mxLabel component="label" relative="1" as="geometry" x="-0.5" y="0" value="Reentry Rules Lookup"/>
          </mxGeometry>
        </mxCell>
        <mxCell edge="1" parent="1" source="reentry-store" target="process-6">
          <mxGeometry relative="1" as="geometry">
            <mxLabel component="label" relative="1" as="geometry" x="-0.5" y="0" value="Reentry Config"/>
          </mxGeometry>
        </mxCell>
        <mxCell edge="1" parent="1" source="process-5" target="sqlite-store">
          <mxGeometry relative="1" as="geometry">
            <mxLabel component="label" relative="1" as="geometry" x="-0.5" y="0" value="Execution Log"/>
          </mxGeometry>
        </mxCell>
        <mxCell edge="1" parent="1" source="process-1" target="sqlite-store">
          <mxGeometry relative="1" as="geometry">
            <mxLabel component="label" relative="1" as="geometry" x="-0.5" y="0" value="Signal Log"/>
          </mxGeometry>
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

#### 2.2.5 Deployment Diagram

```xml
<mxfile host="drawio" modified="2025-08-15" agent="5.0" version="24.6.4">
  <diagram id="deployment-diagram" name="Deployment Architecture">
    <mxGraphModel dx="1422" dy="794" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="827" pageHeight="1169">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <!-- Physical Nodes -->
        <mxCell id="trading-workstation" value="Trading Workstation&#xa;Windows 10/11" style="shape=cube;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;darkOpacity=0.05;darkOpacity2=0.1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=12;fontStyle=1" vertex="1" parent="1">
          <mxGeometry x="100" y="100" width="600" height="400" as="geometry"/>
        </mxCell>
        <!-- Software Components on Workstation -->
        <mxCell id="mt4-terminal-node" value="MT4 Terminal&#xa;MetaTrader 4.exe" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontSize=10" vertex="1" parent="1">
          <mxGeometry x="130" y="140" width="120" height="60" as="geometry"/>
        </mxCell>
        <mxCell id="ea-cluster-node" value="EA Cluster&#xa;30 Currency EAs" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;fontSize=10" vertex="1" parent="1">
          <mxGeometry x="130" y="220" width="120" height="60" as="geometry"/>
        </mxCell>
        <mxCell id="python-service-node" value="Python Services&#xa;Signal Analytics" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;fontSize=10" vertex="1" parent="1">
          <mxGeometry x="280" y="140" width="120" height="60" as="geometry"/>
        </mxCell>
        <mxCell id="communication-bridge-node" value="Communication Bridge&#xa;Socket/Pipes/Files" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;fontSize=10" vertex="1" parent="1">
          <mxGeometry x="430" y="140" width="120" height="60" as="geometry"/>
        </mxCell>
        <mxCell id="sqlite-node" value="SQLite Database&#xa;Local State Storage" style="shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#e1d5e7;strokeColor=#9673a6;fontSize=10" vertex="1" parent="1">
          <mxGeometry x="280" y="220" width="120" height="80" as="geometry"/>
        </mxCell>
        <mxCell id="config-files-node" value="Configuration Files&#xa;CSV, JSON configs" style="shape=folder;whiteSpace=wrap;html=1;fillColor=#FFF9B2;strokeColor=#d6b656;fontSize=10" vertex="1" parent="1">
          <mxGeometry x="430" y="220" width="120" height="60" as="geometry"/>
        </mxCell>
        <!-- File System Structure -->
        <mxCell id="file-structure" value="File System Structure&#xa;C:\Users\[User]\AppData\Roaming\MetaQuotes\Terminal\[ID]\&#xa;├── MQL4\&#xa;│   ├── Experts\ (30 EAs)&#xa;│   ├── Include\ (Shared libraries)&#xa;│   └── Files\&#xa;│       ├── Signals\ (Signal inputs)&#xa;│       ├── Responses\ (Execution outputs)&#xa;│       ├── Configs\ (Parameter sets)&#xa;│       └── Logs\ (System logs)&#xa;├── Python\&#xa;│   ├── services\ (Analytics, ML)&#xa;│   ├── data\ (Market data, signals)&#xa;│   └── config\ (Service configs)&#xa;└── Database\&#xa;    └── trading_system.db (SQLite)" style="shape=note;whiteSpace=wrap;html=1;backgroundOutline=1;fontColor=#000000;darkOpacity=0.05;fillColor=#FFF9B2;strokeColor=none;fillStyle=solid;direction=west;gradientDirection=north;shadow=1;size=20;pointerEvents=1;fontSize=8;align=left" vertex="1" parent="1">
          <mxGeometry x="130" y="320" width="420" height="160" as="geometry"/>
        </mxCell>
        <!-- External Connections -->
        <mxCell id="broker-server" value="Forex Broker&#xa;Trading Server" style="shape=cloud;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;fontSize=10" vertex="1" parent="1">
          <mxGeometry x="750" y="200" width="120" height="80" as="geometry"/>
        </mxCell>
        <mxCell id="data-provider" value="Market Data&#xa;Provider" style="shape=cloud;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;fontSize=10" vertex="1" parent="1">
          <mxGeometry x="750" y="100" width="120" height="80" as="geometry"/>
        </mxCell>
        <!-- Network Connections -->
        <mxCell edge="1" parent="1" source="mt4-terminal-node" target="broker-server">
          <mxGeometry relative="1" as="geometry">
            <mxLabel component="label" relative="1" as="geometry" x="-0.5" y="0" value="FIX/TCP&#xa;Trade Orders"/>
          </mxGeometry>
        </mxCell>
        <mxCell edge="1" parent="1" source="mt4-terminal-node" target="data-provider">
          <mxGeometry relative="1" as="geometry">
            <mxLabel component="label" relative="1" as="geometry" x="-0.5" y="0" value="TCP&#xa;Price Feed"/>
          </mxGeometry>
        </mxCell>
        <!-- Internal Connections -->
        <mxCell edge="1" parent="1" source="python-service-node" target="communication-bridge-node">
          <mxGeometry relative="1" as="geometry">
            <mxLabel component="label" relative="1" as="geometry" x="-0.5" y="0" value="TCP Socket&#xa;Port 8888"/>
          </mxGeometry>
        </mxCell>
        <mxCell edge="1" parent="1" source="communication-bridge-node" target="ea-cluster-node">
          <mxGeometry relative="1" as="geometry">
            <mxLabel component="label" relative="1" as="geometry" x="-0.5" y="0" value="Named Pipes&#xa;File System"/>
          </mxGeometry>
        </mxCell>
        <mxCell edge="1" parent="1" source="ea-cluster-node" target="mt4-terminal-node">
          <mxGeometry relative="1" as="geometry">
            <mxLabel component="label" relative="1" as="geometry" x="-0.5" y="0" value="MQL4 API"/>
          </mxGeometry>
        </mxCell>
        <mxCell edge="1" parent="1" source="ea-cluster-node" target="sqlite-node">
          <mxGeometry relative="1" as="geometry">
            <mxLabel component="label" relative="1" as="geometry" x="-0.5" y="0" value="State Logging"/>
          </mxGeometry>
        </mxCell>
        <mxCell edge="1" parent="1" source="ea-cluster-node" target="config-files-node">
          <mxGeometry relative="1" as="geometry">
            <mxLabel component="label" relative="1" as="geometry" x="-0.5" y="0" value="Config Read"/>
          </mxGeometry>
        </mxCell>
        <mxCell edge="1" parent="1" source="python-service-node" target="sqlite-node">
          <mxGeometry relative="1" as="geometry">
            <mxLabel component="label" relative="1" as="geometry" x="-0.5" y="0" value="Analytics"/>
          </mxGeometry>
        </mxCell>
        <!-- Deployment Notes -->
        <mxCell id="deployment-notes" value="Deployment Requirements:&#xa;• Windows 10/11 with .NET Framework 4.8+&#xa;• MetaTrader 4 Terminal (Build 1400+)&#xa;• Python 3.8+ with required packages&#xa;• SQLite 3.0+ (embedded)&#xa;• TCP Port 8888 available&#xa;• File system permissions for MT4 data directory&#xa;• Minimum 4GB RAM, 100GB storage&#xa;• Network connectivity to broker (HTTPS/FIX)" style="shape=note;whiteSpace=wrap;html=1;backgroundOutline=1;fontColor=#000000;darkOpacity=0.05;fillColor=#D4E1F5;strokeColor=none;fillStyle=solid;direction=west;gradientDirection=north;shadow=1;size=20;pointerEvents=1;fontSize=9;align=left" vertex="1" parent="1">
          <mxGeometry x="50" y="550" width="300" height="120" as="geometry"/>
        </mxCell>
        <mxCell id="security-notes" value="Security Considerations:&#xa;• All communication encrypted via broker TLS&#xa;• Local file system access only&#xa;• No external API dependencies&#xa;• SQLite database file-level encryption&#xa;• MT4 account credentials managed by platform&#xa;• Configuration files contain no sensitive data&#xa;• Python services run with minimal privileges" style="shape=note;whiteSpace=wrap;html=1;backgroundOutline=1;fontColor=#000000;darkOpacity=0.05;fillColor=#FFE6CC;strokeColor=none;fillStyle=solid;direction=west;gradientDirection=north;shadow=1;size=20;pointerEvents=1;fontSize=9;align=left" vertex="1" parent="1">
          <mxGeometry x="400" y="550" width="300" height="120" as="geometry"/>
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

---

## 3.0 Functional & Non-Functional Requirements

### 3.1 Functional Requirements

#### 3.1.1 Signal Processing Requirements

| Requirement ID | Description | Acceptance Criteria |
|----------------|-------------|-------------------|
| **FR-001** | **Multi-Source Signal Reception** | System must accept signals from 4 distinct sources: AI/ML (20001-20003), Technical Indicators (12345-12354), Economic Calendar (50001-50002), and Manual Entry (60001) |
| **FR-002** | **Strategy ID Resolution** | System must map incoming strategy IDs to parameter set IDs using signal_id_mapping.csv with 100% accuracy |
| **FR-003** | **Parameter Set Loading** | System must load 1 of 10 risk parameter sets based on resolved parameter set ID |
| **FR-004** | **Signal Validation** | System must validate signal format, confidence thresholds, market conditions, and risk limits before execution |
| **FR-005** | **Three-Tier Communication** | System must implement automatic failover: TCP Socket (primary) → Named Pipes (secondary) → File System (tertiary) |

#### 3.1.2 Risk Management Requirements

| Requirement ID | Description | Acceptance Criteria |
|----------------|-------------|-------------------|
| **FR-006** | **Dynamic Risk Profiles** | System must support 10 parameter sets ranging from Ultra Conservative (0.5% risk) to High Risk (3.0% risk) |
| **FR-007** | **Confidence Filtering** | System must reject signals below parameter set confidence threshold (0.45-0.7 range) |
| **FR-008** | **Position Limits** | System must enforce maximum concurrent positions per parameter set (1-7 positions) |
| **FR-009** | **Stop Loss Management** | System must apply stop losses from 20-70 pips based on parameter set |
| **FR-010** | **Take Profit Management** | System must apply take profits from 40-140 pips based on parameter set |

#### 3.1.3 Trade Execution Requirements

| Requirement ID | Description | Acceptance Criteria |
|----------------|-------------|-------------------|
| **FR-011** | **Multi-Currency Support** | System must support 30 concurrent currency pair EAs |
| **FR-012** | **Atomic Trade Execution** | Each signal must result in exactly one trade attempt with complete audit trail |
| **FR-013** | **Execution Response Tracking** | System must log execution results (SUCCESS/FAILED/PARTIAL) with timestamps and details |
| **FR-014** | **Slippage Handling** | System must handle broker slippage and requotes with retry logic |
| **FR-015** | **Magic Number Management** | System must assign unique magic numbers for trade identification and management |

#### 3.1.4 Reentry Logic Requirements

| Requirement ID | Description | Acceptance Criteria |
|----------------|-------------|-------------------|
| **FR-016** | **Trade Outcome Analysis** | System must classify trade outcomes into 6 categories: SL, Partial Loss, Breakeven, Partial TP, TP, Beyond TP |
| **FR-017** | **Reentry Decision Matrix** | System must support 5 reentry actions: NO_REENTRY, REDUCE_SIZE, SAME_SIZE, INCREASE_SIZE, REVERSE_POSITION |
| **FR-018** | **Per-Pair Configuration** | System must load reentry rules from per-currency pair CSV files |
| **FR-019** | **Reentry Delay Management** | System must implement configurable delays (0-300 seconds) before reentry attempts |
| **FR-020** | **Reentry Chain Tracking** | System must track related trades in reentry chains for performance analysis |

### 3.2 Performance & Reliability

#### 3.2.1 Service Level Indicators (SLIs) & Objectives (SLOs)

| Metric | SLI | SLO | Measurement Method |
|--------|-----|-----|------------------|
| **Signal Processing Latency** | Time from signal receipt to MT4 execution call | 99th percentile < 10ms | High-resolution timestamps in signal processing pipeline |
| **Signal Delivery Success Rate** | Percentage of signals successfully delivered to MT4 | ≥ 99.9% | (Successful deliveries / Total signals) × 100 |
| **Trade Execution Success Rate** | Percentage of valid signals resulting in successful trades | ≥ 99.5% | (Successful executions / Valid signals) × 100 |
| **Communication Failover Time** | Time to switch between communication channels | < 100ms | Channel switching timestamps |
| **System Availability** | Percentage of time system is operational | ≥ 99.5% | Uptime monitoring over 24-hour periods |

#### 3.2.2 Latency Requirements

| Operation | Target Latency | Maximum Acceptable | Measurement Point |
|-----------|----------------|-------------------|------------------|
| **Signal Validation** | < 1ms | 5ms | Signal receipt to validation complete |
| **Strategy ID Lookup** | < 1ms | 3ms | Strategy ID to parameter set ID resolution |
| **Parameter Set Loading** | < 2ms | 5ms | Parameter set ID to loaded configuration |
| **Signal Building** | < 2ms | 5ms | Parameter application to complete signal |
| **Communication Transfer** | < 3ms | 10ms | Signal transmission across channels |
| **Total Processing** | < 10ms | 25ms | End-to-end signal processing |

#### 3.2.3 Throughput Requirements

| Metric | Target | Peak Capacity | Notes |
|--------|--------|---------------|-------|
| **Signals per Second** | 100 signals/sec | 500 signals/sec | Across all 30 currency pairs |
| **Concurrent EAs** | 30 EAs | 30 EAs | One EA per currency pair (hard limit) |
| **Database Writes** | 1000 writes/sec | 2000 writes/sec | SQLite transaction capacity |
| **File Operations** | 200 ops/sec | 500 ops/sec | CSV reads and atomic writes |

### 3.3 Scalability & Capacity Planning

#### 3.3.1 Scaling Strategy

**Current Capacity:**
- **30 Currency Pairs**: One EA per major forex pair
- **4 Signal Sources**: AI/ML, Technical, Manual, Economic Calendar
- **10 Parameter Sets**: Covering risk spectrum from ultra-conservative to high-risk
- **3 Communication Channels**: Socket, Named Pipes, File System

**Scaling Dimensions:**
1. **Currency Pair Scaling**: Add exotic pairs (limited by MT4 terminal capacity)
2. **Signal Source Scaling**: Add new signal generators (crypto, commodities, indices)
3. **Parameter Set Scaling**: Add specialized parameter sets for market conditions
4. **Geographic Scaling**: Multiple trading sessions with regional parameter sets

#### 3.3.2 Resource Forecasts

| Resource | Current Usage | 6-Month Forecast | 12-Month Forecast | Scaling Trigger |
|----------|---------------|------------------|------------------|-----------------|
| **CPU Usage** | 15-25% | 25-35% | 35-50% | > 70% sustained |
| **Memory Usage** | 2-4 GB | 4-6 GB | 6-8 GB | > 80% of available |
| **Disk I/O** | 50-100 IOPS | 100-200 IOPS | 200-400 IOPS | > 500 IOPS sustained |
| **Network Traffic** | 1-5 MB/hour | 5-15 MB/hour | 15-30 MB/hour | Bandwidth saturation |
| **Database Size** | 100 MB/month | 200 MB/month | 500 MB/month | > 10 GB total |

### 3.4 Security Architecture

#### 3.4.1 Threat Model (STRIDE Analysis)

| Threat Category | Threat Description | Impact | Mitigation Strategy |
|-----------------|-------------------|--------|-------------------|
| **Spoofing** | Malicious signals injected into system | High - Unauthorized trading | Signal source validation, authentication tokens |
| **Tampering** | Configuration files modified | High - Risk parameter changes | File integrity checks, read-only permissions |
| **Repudiation** | Trade actions denied by user | Medium - Audit trail gaps | Complete logging with timestamps and signatures |
| **Information Disclosure** | Trading strategy parameters exposed | Medium - Competitive disadvantage | Local file system only, encryption for sensitive data |
| **Denial of Service** | Signal processing overwhelmed | High - Trading interruption | Rate limiting, circuit breakers, failover channels |
| **Elevation of Privilege** | Unauthorized access to MT4 functions | High - Account compromise | Principle of least privilege, MT4 built-in security |

#### 3.4.2 Data Protection Strategy

**Data Classification:**
- **Public**: System status, basic performance metrics
- **Internal**: Configuration parameters, signal statistics
- **Confidential**: Trading signals, execution results, account information
- **Restricted**: Broker credentials, API keys (managed by MT4)

**Protection Measures:**
| Data Type | Storage | Transmission | Access Control |
|-----------|---------|--------------|---------------|
| **Configuration Files** | Local file system, read-only | None (local only) | File system permissions |
| **Signal Data** | Memory + SQLite | Local IPC only | Process isolation |
| **Trade Results** | SQLite database | None (local only) | Database file permissions |
| **Audit Logs** | Local log files | Optional secure export | Append-only, rotation |

#### 3.4.3 Authentication & Authorization

**Authentication Strategy:**
- **MT4 Integration**: Relies on MT4 platform authentication
- **Local Components**: File system permissions and process isolation
- **No External Auth**: System operates entirely locally

**Authorization Matrix:**
| Component | Read Config | Write Signals | Execute Trades | View Logs |
|-----------|-------------|---------------|----------------|-----------|
| **Signal Generators** | No | Yes | No | No |
| **Signal Processor** | Yes | No | No | Yes |
| **MT4 EAs** | Yes | No | Yes | Yes |
| **Analytics Engine** | Yes | No | No | Yes |

### 3.5 Accessibility & Localization

#### 3.5.1 System Accessibility

**MQL4 Code Accessibility:**
- **Code Documentation**: Comprehensive inline comments for all functions
- **Function Naming**: Clear, descriptive names following MQL4 conventions
- **Error Messages**: Detailed error descriptions with suggested resolutions
- **Logging Levels**: Configurable verbosity for different user skill levels

**Configuration Accessibility:**
- **CSV Format**: Human-readable configuration files
- **Parameter Documentation**: Description field for each parameter set
- **Validation Messages**: Clear feedback for configuration errors

#### 3.5.2 Internationalization Strategy

**Multi-Language Support:**
- **Primary Language**: English (system default)
- **Error Messages**: English with error codes for translation
- **Configuration**: ASCII-based CSV files for universal compatibility
- **Logging**: UTC timestamps with ISO 8601 format

**Regional Considerations:**
- **Number Formats**: Decimal points (not commas) for all numeric values
- **Date Formats**: ISO 8601 (YYYY-MM-DD) for consistency
- **Currency Symbols**: ISO currency codes (EUR, USD, GBP, etc.)
- **Time Zones**: All timestamps in broker time zone with UTC offset

### 3.6 Observability

#### 3.6.1 Logging Strategy

**Log Levels:**
| Level | Usage | Example |
|-------|-------|---------|
| **ERROR** | System failures, trade execution errors | "Failed to execute trade: Error 130 - Invalid stops" |
| **WARN** | Recoverable issues, failover events | "TCP socket failed, switching to Named Pipes" |
| **INFO** | Normal operations, signal processing | "Signal 12345 processed successfully, executed EURUSD BUY 0.01" |
| **DEBUG** | Detailed processing steps | "Strategy ID 12345 mapped to Parameter Set 1" |
| **TRACE** | Fine-grained execution flow | "Loading parameter set from all_10_parameter_sets.csv" |

**Log Structure:**
```
[TIMESTAMP] [LEVEL] [COMPONENT] [CORRELATION_ID] MESSAGE
[2025-08-15 14:30:15.123] [INFO] [SignalProcessor] [sig_001] Strategy ID 12345 mapped to Parameter Set 1
```

#### 3.6.2 Metrics Collection

**System Metrics:**
| Metric Name | Type | Description | Collection Frequency |
|-------------|------|-------------|-------------------|
| `signals_received_total` | Counter | Total signals received by source | Real-time |
| `signals_processed_total` | Counter | Successfully processed signals | Real-time |
| `signals_rejected_total` | Counter | Rejected signals with reason | Real-time |
| `signal_processing_duration_ms` | Histogram | Signal processing latency | Per signal |
| `trades_executed_total` | Counter | Successful trade executions | Real-time |
| `trades_failed_total` | Counter | Failed trade executions with error code | Real-time |
| `communication_channel_active` | Gauge | Currently active communication channel (0=Socket, 1=Pipes, 2=File) | Every 5 seconds |
| `parameter_set_usage` | Counter | Usage count per parameter set | Per signal |

**Business Metrics:**
| Metric Name | Type | Description | Collection Frequency |
|-------------|------|-------------|-------------------|
| `reentry_actions_total` | Counter | Reentry actions by type | Per reentry |
| `profit_loss_realized` | Gauge | Realized P&L by currency pair | Per trade close |
| `position_count_active` | Gauge | Active positions by currency pair | Every 10 seconds |
| `confidence_score_avg` | Gauge | Average signal confidence by source | Hourly |

#### 3.6.3 Tracing & Correlation

**Correlation Strategy:**
- **Signal UUID**: Unique identifier tracking signal from generation to execution
- **Trade Chain ID**: Links original trade to reentry trades
- **Session ID**: Groups related operations within processing session

**Distributed Tracing:**
```
Signal Lifecycle Trace:
├── Signal Generation [span_id: gen_001]
├── Signal Validation [span_id: val_001, parent: gen_001]
├── Strategy Resolution [span_id: res_001, parent: val_001]
├── Parameter Loading [span_id: par_001, parent: res_001]
├── Trade Execution [span_id: exe_001, parent: par_001]
└── Reentry Processing [span_id: ren_001, parent: exe_001]
```

#### 3.6.4 Dashboard Requirements

**Real-Time Dashboard Components:**

1. **Signal Flow Overview**
   - Signals per minute by source
   - Processing latency trends
   - Communication channel status
   - Rejection rate by reason

2. **Trade Execution Monitor**
   - Active positions by currency pair
   - Execution success rate
   - P&L trends by parameter set
   - Error distribution

3. **System Health**
   - CPU and memory usage
   - File system status
   - Database performance
   - Communication channel performance

4. **Risk Management**
   - Parameter set utilization
   - Risk exposure by currency
   - Confidence score distributions
   - Reentry action effectiveness

---

## 4.0 Data Architecture

### 4.1 Data Models

#### 4.1.1 Core Signal Data Structure

```sql
-- Signal Processing Schema
CREATE TABLE signals (
    signal_uuid TEXT PRIMARY KEY,
    source_type TEXT NOT NULL, -- 'AI', 'TECHNICAL', 'MANUAL', 'CALENDAR'
    strategy_id TEXT NOT NULL,
    parameter_set_id INTEGER NOT NULL,
    symbol TEXT NOT NULL,
    action TEXT NOT NULL, -- 'BUY', 'SELL'
    confidence REAL NOT NULL,
    signal_timestamp INTEGER NOT NULL,
    processing_timestamp INTEGER NOT NULL,
    status TEXT NOT NULL, -- 'RECEIVED', 'VALIDATED', 'EXECUTED', 'REJECTED'
    rejection_reason TEXT,
    FOREIGN KEY (parameter_set_id) REFERENCES parameter_sets(id)
);

-- Parameter Sets Configuration
CREATE TABLE parameter_sets (
    id INTEGER PRIMARY KEY,
    stop_loss INTEGER NOT NULL,
    take_profit INTEGER NOT NULL,
    trailing_stop INTEGER NOT NULL,
    risk_percent REAL NOT NULL,
    max_positions INTEGER NOT NULL,
    entry_delay INTEGER NOT NULL,
    confidence_threshold REAL NOT NULL,
    use_trailing INTEGER NOT NULL, -- 0 or 1
    description TEXT NOT NULL
);

-- Trade Execution Results
CREATE TABLE trades (
    trade_id TEXT PRIMARY KEY,
    signal_uuid TEXT NOT NULL,
    mt4_ticket INTEGER,
    symbol TEXT NOT NULL,
    action TEXT NOT NULL,
    lot_size REAL NOT NULL,
    entry_price REAL,
    stop_loss REAL,
    take_profit REAL,
    execution_timestamp INTEGER NOT NULL,
    status TEXT NOT NULL, -- 'PENDING', 'FILLED', 'FAILED', 'CLOSED'
    error_code INTEGER,
    error_message TEXT,
    magic_number INTEGER NOT NULL,
    FOREIGN KEY (signal_uuid) REFERENCES signals(signal_uuid)
);

-- Reentry Chain Tracking
CREATE TABLE reentry_chains (
    chain_id TEXT PRIMARY KEY,
    original_trade_id TEXT NOT NULL,
    symbol TEXT NOT NULL,
    strategy_id TEXT NOT NULL,
    chain_start_timestamp INTEGER NOT NULL,
    chain_status TEXT NOT NULL, -- 'ACTIVE', 'COMPLETED', 'ABANDONED'
    total_trades INTEGER DEFAULT 1,
    realized_pnl REAL DEFAULT 0.0,
    FOREIGN KEY (original_trade_id) REFERENCES trades(trade_id)
);

-- Reentry Actions Log
CREATE TABLE reentry_actions (
    action_id TEXT PRIMARY KEY,
    chain_id TEXT NOT NULL,
    parent_trade_id TEXT NOT NULL,
    action_type TEXT NOT NULL, -- 'NO_REENTRY', 'REDUCE_SIZE', etc.
    exit_reason TEXT NOT NULL, -- 'SL', 'PARTIAL_LOSS', etc.
    action_timestamp INTEGER NOT NULL,
    delay_seconds INTEGER NOT NULL,
    size_multiplier REAL NOT NULL,
    confidence_adjustment REAL NOT NULL,
    new_trade_id TEXT,
    FOREIGN KEY (chain_id) REFERENCES reentry_chains(chain_id),
    FOREIGN KEY (parent_trade_id) REFERENCES trades(trade_id),
    FOREIGN KEY (new_trade_id) REFERENCES trades(trade_id)
);
```

#### 4.1.2 Configuration Data Model

```csv
# signal_id_mapping.csv Structure
strategyId,parameterSetId,description
12345,1,"RSI Oversold Signal - Use ultra conservative parameters"
12346,2,"EMA Crossover - Standard conservative approach"
# ... 18 more strategy mappings

# all_10_parameter_sets.csv Structure  
id,stopLoss,takeProfit,trailingStop,riskPercent,maxPositions,entryDelay,confidenceThreshold,useTrailing,description
1,20,40,15,0.5,2,300,0.7,1,"Ultra Conservative - Minimal risk with tight controls"
2,30,60,20,1.0,3,180,0.65,1,"Conservative - Balanced risk with moderate targets"
# ... 8 more parameter sets

# Per-Currency Reentry Configuration (e.g., EURUSD_reentry.csv)
Action,Type,SizeMultiplier,DelaySeconds,ConfidenceAdjustment,Parameters
1,NO_REENTRY,0.0,0,1.0,"Stop loss - no reentry"
2,REDUCE_SIZE,0.5,30,1.1,"Partial loss - reduce position size"
# ... 4 more reentry rules
```

#### 4.1.3 Entity Relationship Diagram

```
[Signal Sources] 1---N [Signals]
       |                   |
       |                   | 1
       |                   |
       |                   N
       |              [Strategy Mapping] 1---N [Parameter Sets]
       |                   |                        |
       |                   |                        | 1
       |                   |                        |
       |                   |                        N
       N                   N                   [Trades]
[Reentry Chains] 1---N [Reentry Actions]           |
       |                                            | 1
       |                                            |
       |                                            N
       1----------------------------------------[Trade Results]
```

### 4.2 Data Governance

#### 4.2.1 Data Classification & Handling

| Data Category | Classification | Retention Policy | Access Control | Backup Requirements |
|---------------|----------------|------------------|----------------|-------------------|
| **Signal Data** | Internal | 90 days active, 1 year archive | Process-level isolation | Daily local backup |
| **Trade Results** | Confidential | 7 years (regulatory) | File system permissions | Daily + weekly offsite |
| **Configuration** | Internal | Permanent (versioned) | Read-only for most processes | Version control system |
| **System Logs** | Internal | 30 days active, 90 days archive | Append-only access | Daily rotation + compression |
| **Performance Metrics** | Internal | 1 year active, 3 years archive | Analytics engine only | Weekly aggregated backup |

#### 4.2.2 Data Quality Standards

**Validation Rules:**
| Field | Validation Rule | Error Handling |
|-------|----------------|----------------|
| **Signal UUID** | Must be valid UUID v4 format | Reject signal, log error |
| **Strategy ID** | Must exist in signal_id_mapping.csv | Use DEFAULT_STRATEGY (60001) |
| **Confidence** | Range 0.0-1.0, required for execution | Reject if outside range |
| **Symbol** | Must match MT4 symbol format | Reject signal, log error |
| **Timestamps** | Must be within ±5 minutes of current time | Accept with warning |
| **Parameter Set ID** | Must exist in all_10_parameter_sets.csv | Use Parameter Set 1 (conservative) |

**Data Integrity Checks:**
- **Referential Integrity**: All foreign keys must reference valid records
- **Temporal Consistency**: Signal timestamp ≤ execution timestamp
- **Business Logic**: Trade lot size must align with risk percentage
- **Configuration Consistency**: Parameter sets must have valid ranges

#### 4.2.3 PII/PHI Handling

**Data Types Present:**
- **No PII**: System does not collect personal information
- **No PHI**: System does not handle health information  
- **Financial Data**: Trade results and P&L (considered sensitive business data)

**Sensitive Data Protection:**
| Data Type | Protection Method | Access Restriction |
|-----------|------------------|-------------------|
| **Account Numbers** | Managed by MT4 platform | Not stored in system |
| **Trade P&L** | Local file system only | No network transmission |
| **Strategy Parameters** | Local configuration files | File system permissions |
| **System Credentials** | Environment variables only | Never logged or stored |

#### 4.2.4 Data Retention & Archival

**Retention Schedule:**
```
Signal Processing Data:
├── Active Period: 90 days (high-performance SQLite)
├── Archive Period: 1 year (compressed SQLite)
└── Disposal: Secure deletion after 1 year

Trade Results:
├── Active Period: 1 year (operational access)
├── Archive Period: 7 years (regulatory compliance)
└── Long-term: Encrypted cold storage

Configuration Data:
├── Current: Live configuration files
├── Versioned: Git repository with full history
└── Backup: Daily snapshots with 30-day retention

System Logs:
├── Real-time: Last 7 days uncompressed
├── Compressed: 30 days compressed logs
└── Archive: 90 days minimal logging
```

**Archival Process:**
1. **Daily Job**: Compress logs older than 7 days
2. **Weekly Job**: Archive signal data older than 90 days
3. **Monthly Job**: Backup configuration versions
4. **Quarterly Job**: Validate archive integrity
5. **Annual Job**: Secure disposal of expired data

---

This completes the comprehensive Technical Specification Document for the MT4 Signal System. The document provides detailed architecture, requirements, and implementation guidance for all system components while maintaining strict adherence to the specified structure and requirements.