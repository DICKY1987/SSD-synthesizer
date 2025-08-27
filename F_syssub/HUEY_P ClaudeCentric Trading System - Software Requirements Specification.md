HUEY_P ClaudeCentric Trading System - Software Requirements Specification
Document Version: 1.0
Date: August 26, 2025
Classification: System Architecture Requirements
1. Introduction
1.1 Purpose
This Software Requirements Specification (SRS) defines the complete architecture and requirements for the HUEY_P ClaudeCentric Trading System, a sophisticated multi-component hybrid trading system designed for automated execution on MetaTrader 4 (MT4). This document consolidates architectural information from the technical manual, technical specification, dependency manifest, and reentry matrix documentation to provide a comprehensive view of system requirements and constraints.
Sources: huey_p_technical_manual.md (Section 1.1), huey_p_tech_spec.md (Section 1.1)
1.2 Scope
The HUEY_P system encompasses automated algorithmic trading capabilities with comprehensive monitoring and risk management across multiple currency pairs. The system integrates:

Proactive Event-Based Trading: Automated analysis of economic calendar data for anticipatory trading signals
Reactive Outcome-Based Reentry: Dynamic trade management analyzing outcomes for strategic reentry actions
Multi-Bridge Communication: Redundant communication pathways ensuring system reliability
30-Pair Trading Coverage: Comprehensive forex market coverage across major, cross, and metals pairs
Reduced Multi-Dimensional Reentry Matrix: 652 combinations per symbol with bounded complexity

Sources: huey_p_technical_manual.md (Section 1.2), dependency_manifest.yml (system overview), most_acurate_matirx_doc.md (Section 1.2)
1.3 Definitions, Acronyms, and Abbreviations
TermDefinitionSourceEAExpert Advisor - Automated trading program for MetaTrader 4huey_p_tech_spec.mdMQL4MetaQuotes Language 4 - Programming language for MT4 EAshuey_p_tech_spec.mdDLLDynamic Link Library - Windows executable libraryhuey_p_tech_spec.mdStraddleTrading strategy placing simultaneous BuyStop and SellStop ordershuey_p_tech_spec.mdReentry MatrixMulti-dimensional decision system for trade continuation logicmost_acurate_matirx_doc.mdSignal IntegrationCommunication bridge transferring signals between componentshuey_p_technical_manual.mdEconomic Calendar SystemVBA-based component processing economic event datahuey_p_technical_manual.mdBridge Health MonitorPowerShell-based system monitoring communication pathwaysdependency_manifest.yml
1.4 References

huey_p_technical_manual.md - HUEY_P ClaudeCentric Trading System Technical Manual v1.0
huey_p_tech_spec.md - HUEY_P Trading System Technical Specification Document v1.0
dependency_manifest.yml - Trading System Dependency Management Configuration
most_acurate_matirx_doc.md - Reduced Multi-Dimensional Reentry Matrix System v3.0

1.5 Overview
This SRS is organized into three main sections following IEEE 830 standards. Section 2 provides overall product description including perspective, functions, and constraints. Section 3 details specific functional and performance requirements organized by system layers and components. Each requirement includes traceability to source documents and dependency relationships.
2. Overall Description
2.1 Product Perspective
The HUEY_P ClaudeCentric Trading System operates as a sophisticated multi-layer architecture integrating multiple technologies and platforms:
System Architecture Overview (huey_p_technical_manual.md Section 1.2, huey_p_tech_spec.md Section 2.2):

Data Sources Layer: Economic calendar feeds, market data streams, configuration files
Processing Layer: VBA/Excel calendar processing, Python service orchestration
Communication Layer: Multi-protocol bridges (DLL+Socket, Named Pipes, File-based)
Execution Layer: MQL4 Expert Advisors across 30 currency pairs
Persistence Layer: SQLite databases, CSV/YAML configuration storage
Management Layer: PowerShell orchestration, health monitoring

The system implements a hybrid approach combining proactive event-based trading with reactive outcome-based adaptation, operating within the MetaTrader 4 ecosystem while extending capabilities through external Python and PowerShell components.
Sources: huey_p_technical_manual.md (Section 2.1), huey_p_tech_spec.md (Section 2.1), dependency_manifest.yml (system architecture)
2.2 Product Functions
Primary System Functions:
F1. Economic Calendar Processing (huey_p_technical_manual.md Section 5)

Import and transform economic calendar CSV data
Generate anticipation events (1-hour, 2-hour, 4-hour intervals)
Convert raw calendar data into actionable trading signals
Handle timezone conversions and event filtering

F2. Multi-Source Signal Generation (dependency_manifest.yml services section)

SignalService with ML-powered signal generation
MarketDataService for real-time data aggregation
Seven canonical signal types: ECO_HIGH, ECO_MED, ANTICIPATION_1HR, ANTICIPATION_8HR, EQUITY_OPEN_ASIA, EQUITY_OPEN_EUROPE, EQUITY_OPEN_USA, ALL_INDICATORS

F3. Multi-Protocol Communication (huey_p_tech_spec.md Section 2.2, dependency_manifest.yml bridges)

Primary: DLL+Socket Bridge (target <10ms latency, 1000 ops/sec)
Secondary: Named Pipes Bridge (target <50ms latency, 500 ops/sec)
Tertiary: File-based Bridge (target <500ms latency, 10 ops/sec)
Automatic failover chain with health monitoring

F4. Automated Trade Execution (huey_p_technical_manual.md Section 3)

Straddle trading strategy implementation
Dynamic risk management and lot sizing
State machine-based execution control
30 concurrent EA instances across currency pairs

F5. Reentry Decision Matrix (most_acurate_matirx_doc.md)

652 combinations per symbol (4D matrix: Signal × Duration × Outcome × Future Proximity)
Conditional duration logic for ECO_HIGH/ECO_MED signals
Hard limit after R2 generation to prevent runaway chains
Performance tracking and adaptive optimization

Sources: All four source documents contribute to function definitions
2.3 User Characteristics
Primary Users (huey_p_tech_spec.md Section 1.3):
U1. System Architect/Lead Developer

Technical expertise: Expert-level MQL4, Python, C++, PowerShell, VBA
Responsibilities: System architecture, EA development, integration
Interface: Direct code modification, configuration management

U2. Trading Operations Team

Technical expertise: Intermediate trading platform knowledge
Responsibilities: Day-to-day monitoring, parameter adjustment
Interface: Python monitoring dashboard, Excel configuration panels

U3. Risk Management

Technical expertise: Basic system understanding, advanced risk analysis
Responsibilities: Risk parameter validation, compliance oversight
Interface: Analytics reports, alert notifications

2.4 Constraints
C1. Platform Constraints (huey_p_tech_spec.md Section 2.1)

Windows Dependency: MT4 platform requires Windows operating system
32-bit Architecture: MT4 DLLs must be compiled for 32-bit architecture
Single Broker Limitation: System designed for single MT4 instance per deployment
MT4 Framework Limitations: Bounded by MetaTrader 4 capabilities and restrictions

C2. Performance Constraints (huey_p_tech_spec.md Section 3.2)

Trade execution latency: <200ms p99 for order placement
Signal processing latency: <100ms p95 for validation completion
Database response time: <50ms p95 for standard operations
System availability: 99.95% during trading hours

C3. Complexity Constraints (most_acurate_matirx_doc.md Section 1.1)

Maximum 2 reentry generations (R1, R2) with hard stop
652 combinations per symbol (deterministic limit)
Conditional duration logic only for ECO_HIGH/ECO_MED signals

C4. Regulatory Constraints (huey_p_technical_manual.md Section 8.1)

Trade history retention: 7 years for compliance
Audit trail completeness for all trading decisions
Error logging and performance monitoring requirements

2.5 Assumptions and Dependencies
A1. External Market Dependencies (huey_p_tech_spec.md Section 2.4)

Stable internet connection for market data feeds
Broker server availability during trading hours
Economic calendar data source reliability and timeliness

A2. Technology Stack Dependencies (dependency_manifest.yml validation section)

Windows 10/11 Professional operating system
Python 3.8+ environment with required libraries
Visual Studio 2019+ for C++ DLL compilation
SQLite database engine availability

A3. Trading Environment Assumptions (huey_p_technical_manual.md Section 1.3)

Standard forex market hours (Sunday 23:00 GMT - Friday 22:00 GMT)
Typical spreads and execution conditions from broker
Economic calendar events occur as scheduled with minimal last-minute changes

3. Specific Requirements
3.1 Functional Requirements
3.1.1 Data Sources Layer
3.1.1.1 Economic Calendar Import System
FR-001: The system SHALL automatically detect and import economic calendar CSV files from designated directories.

Implementation: VBA Calendar Import Engine (huey_p_technical_manual.md Section 5.2)
File Patterns: Support multiple naming patterns including "ff_calendar*.csv", "economiccalendar*.csv"
Processing Frequency: Configurable with default every 30 seconds during trading hours
Error Handling: Graceful failure with fallback to cached data

FR-002: The system SHALL validate calendar file format and data integrity before processing.

Validation Rules: Required columns, date format verification, timezone conversion validation
Source: huey_p_technical_manual.md Section 5.3
Fallback: Reject invalid files with detailed error logging

3.1.1.2 External Market Data Integration
FR-003: The system SHALL maintain real-time market data connections with sub-100ms latency SLA.

Implementation: MarketDataService (dependency_manifest.yml services section)
Interface: WebSocket connection to external market feed
Fallback Strategy: Cached data with staleness warnings
Health Monitoring: Continuous connection status validation

3.1.2 Data Processing Layer
3.1.2.1 VBA Calendar Processing Pipeline
FR-004: The system SHALL transform raw calendar data into structured trading events.

Components: Data Store Manager, Calendar Data Processor, Event Trigger Engine (huey_p_technical_manual.md Section 5.1)
Processing Steps: Import → Validate → Transform → Generate Anticipation → Trigger
Anticipation Events: Generate 1hr, 2hr, 4hr advance events for high/medium impact events

FR-005: The system SHALL perform timezone conversion from source timezone to CST.

Implementation: Automatic DST detection and adjustment (huey_p_technical_manual.md Section 5.3.2)
Validation: Cross-reference with multiple timezone sources
Accuracy Requirement: ±5 minute tolerance for event timing

3.1.2.2 Python Service Orchestration
FR-006: The SignalService SHALL generate ML-powered trading signals with explainable AI.

Dependencies: MarketDataService, ConfigurationService (dependency_manifest.yml)
Signal Types: Seven canonical types with regional and temporal specificity
Performance Target: Signal generation within 5000ms timeout
Fallback: Rule-based signals when ML service unavailable

FR-007: The AnalyticsService SHALL provide real-time portfolio risk analysis and performance metrics.

Data Sources: MarketDataService, SQLite trade history
Metrics: Risk analytics, performance reports, drawdown analysis
Update Frequency: Real-time for active positions, hourly for historical analysis

3.1.3 Communication Layer
3.1.3.1 Multi-Bridge Architecture
FR-008: The system SHALL implement redundant communication bridges with automatic failover.

Primary Bridge: DLL+Socket (Port 8001, <10ms target latency) (dependency_manifest.yml bridges)
Secondary Bridge: Named Pipes (<50ms target latency)
Tertiary Bridge: File-based with PowerShell monitoring (<500ms target latency)
Failover Logic: Automatic cascade through bridge hierarchy

FR-009: The BridgeHealthMonitor SHALL continuously monitor bridge connectivity and coordinate failover.

Implementation: PowerShell script with 30-second intervals (dependency_manifest.yml)
Health Indicators: Response time, throughput, error rates
Action: Automatic bridge switching when primary fails

3.1.3.2 Communication Protocol
FR-010: The system SHALL implement standardized message protocol for inter-component communication.

Message Types: HEARTBEAT, STATUS_REQUEST, STATUS_RESPONSE, TRADE_UPDATE, ERROR (huey_p_tech_spec.md Section 6.1)
Format: JSON with schema validation
Rate Limiting: Configurable per message type with burst allowance

3.1.4 Execution Layer
3.1.4.1 MQL4 Expert Advisor Core
FR-011: The system SHALL execute straddle trading strategies across 30 currency pairs simultaneously.

EA Architecture: Class-based design with StateManager, SignalManager, LogManager (huey_p_technical_manual.md Section 3.1)
Coverage: 7 major pairs, 21 cross pairs, 2 precious metals (dependency_manifest.yml)
Magic Numbers: Unique identification per EA instance

FR-012: Each EA SHALL implement comprehensive state management and recovery capabilities.

States: IDLE, ORDERS_PLACED, TRADE_TRIGGERED, PAUSED (huey_p_technical_manual.md Section 3.1.1)
Recovery: Automatic state restoration after MT4 restart
Circuit Breakers: Emergency stop on consecutive errors or drawdown limits

3.1.4.2 Dynamic Risk Management
FR-013: The system SHALL calculate position sizes dynamically based on account equity and risk parameters.

Algorithm: Risk percentage-based with volatility adjustment (huey_p_technical_manual.md Section 3.2.2)
Constraints: Min/max lot sizes, margin safety checks, maximum position limits
Real-time Adjustment: Automatic adjustment based on account performance

FR-014: The system SHALL enforce circuit breaker controls for risk protection.

Daily Drawdown: Configurable percentage limit (default 5%)
Consecutive Losses: Automatic lot size reduction after threshold
Emergency Stop: Immediate halt on critical account conditions

3.1.4.3 Reentry Logic System
FR-015: The system SHALL implement the Reduced Multi-Dimensional Reentry Matrix for adaptive trade management.

Matrix Dimensions: 4D matrix over Signal × Duration × Outcome × Future Proximity (most_acurate_matirx_doc.md Section 1.1)
Combinations: 652 per symbol (deterministic)
Generation Limit: Hard stop after R2 generation
Conditional Logic: Duration categories only for ECO_HIGH/ECO_MED signals

FR-016: The reentry system SHALL categorize trade outcomes and determine appropriate responses.

Outcome Categories: FULL_SL, PARTIAL_LOSS, BREAKEVEN, PARTIAL_PROFIT, FULL_TP, BEYOND_TP
Actions: NO_REENTRY, SAME_TRADE, REVERSE, INCREASE_SIZE, REDUCE_SIZE, AGGRESSIVE
Future Proximity: IMMEDIATE (0-15min), SHORT (16-60min), LONG (61-480min), EXTENDED (481-1440min)

3.1.5 Persistence Layer
3.1.5.1 Database Management
FR-017: The system SHALL maintain comprehensive trade history and system state in SQLite database.

Schema: Split structure for original vs reentry combinations (most_acurate_matirx_doc.md Section 6)
Tables: trades_SYMBOL, reentry_combinations, combination_performance, reentry_chains
Retention: 7-year trade history for regulatory compliance
Backup: Automated daily backups with rotation policy

FR-018: The database SHALL track reentry chain performance and bounded generation limits.

Chain Tracking: Complete audit trail of reentry sequences
Performance Metrics: Win rate, average P&L, execution statistics per combination
Generation Enforcement: Hard constraint preventing chains beyond R2

3.1.5.2 Configuration Management
FR-019: The system SHALL support hierarchical configuration with hot-reload capabilities.

Structure: YAML master config with CSV parameter files (huey_p_technical_manual.md Section 7.1)
Hot Reload: Python services support runtime configuration updates
Validation: Schema validation and constraint checking before application

FR-020: The ConfigurationService SHALL distribute configuration updates across all system components.

Implementation: PowerShell-based distribution system (dependency_manifest.yml)
Scope: Master config changes affect all services and EAs
Fallback: Automatic reversion on validation failures

3.1.6 Management Layer
3.1.6.1 Health Monitoring
FR-021: The system SHALL implement comprehensive health monitoring across all components.

Health Files: Component-specific status files with timestamp validation (dependency_manifest.yml validation)
EA Heartbeats: Per-pair CSV heartbeat files updated every 30 seconds
Service Health: Python services maintain health indicators with 2-minute freshness requirement

FR-022: The system SHALL provide automated dependency validation and impact analysis.

Validation Script: Python-based dependency checker with 652 total validations per symbol
Impact Analysis: Change impact assessment with testing and deployment recommendations
Pre-commit Integration: Git hooks for automatic validation on code changes

3.1.6.2 Performance Monitoring
FR-023: The system SHALL track and report performance metrics across all layers.

Execution Timing: Function-level performance monitoring with statistical analysis (huey_p_technical_manual.md Section 3.3)
Resource Usage: CPU, memory, disk usage tracking
Trading Performance: Win rates, profit factors, drawdown analysis by strategy and pair

3.2 Performance Requirements
3.2.1 Latency Requirements
PR-001: Signal processing latency SHALL NOT exceed 100ms p95 for critical operations.

Measurement: Signal receipt to validation completion
Components: SignalService, bridge communication, EA processing
Source: huey_p_tech_spec.md Section 3.2

PR-002: Trade execution latency SHALL NOT exceed 200ms p99 from signal to broker order.

Path: Signal generation → Bridge → EA → MT4 → Broker
Excludes: Broker processing time and market conditions
Monitoring: Continuous latency measurement with alerting

3.2.2 Throughput Requirements
PR-003: The DLL+Socket bridge SHALL support minimum 1000 operations per second.

Operations: Message passing between Python services and MQL4 EAs
Degradation: Graceful performance degradation under load
Failover: Automatic switch to Named Pipes bridge if throughput drops below 500 ops/sec

3.2.3 Availability Requirements
PR-004: System availability SHALL be 99.95% during trading hours (Sunday 23:00 GMT - Friday 22:00 GMT).

Measurement: Uptime of critical path components
Downtime Budget: Maximum 2.2 minutes per week
Recovery: Automated restart and recovery procedures

3.2.4 Scalability Requirements
PR-005: The system SHALL support concurrent operation across 30 currency pairs with linear resource scaling.

Resource Growth: Memory usage proportional to 652 × symbol_count
Processing: Independent EA processing per currency pair
Bottlenecks: Shared components (database, bridges) designed for concurrent access

3.3 Design Constraints
3.3.1 Technology Constraints
DC-001: All MQL4 Expert Advisors SHALL be compiled for 32-bit architecture for MT4 compatibility.

Compiler: MetaEditor with 32-bit target
DLL Integration: C++ DLLs must also be compiled for 32-bit
Source: huey_p_tech_spec.md Section 2.1

DC-002: The system SHALL operate within Windows ecosystem due to MT4 platform requirements.

Operating System: Windows 10/11 Professional
File System: NTFS with appropriate security permissions
Services: Windows services for background processing

3.3.2 Complexity Constraints
DC-003: Reentry chains SHALL be limited to maximum R2 generation to prevent unbounded complexity.

Enforcement: Hard stops in ReentryChainExecutor (most_acurate_matirx_doc.md Section 9)
Rationale: Prevent exponential growth of decision trees
Exception Handling: Graceful termination with detailed logging

DC-004: Signal types SHALL be limited to seven canonical types with conditional duration logic.

Signal Enumeration: ECO_HIGH, ECO_MED, ANTICIPATION_1HR, ANTICIPATION_8HR, EQUITY_OPEN_ASIA, EQUITY_OPEN_EUROPE, EQUITY_OPEN_USA, ALL_INDICATORS
Duration Logic: Only ECO_HIGH/ECO_MED signals use duration categories
Validation: Strict enumeration checking with constraint violations logged

3.3.3 Storage Constraints
DC-005: Database design SHALL optimize for 652 combinations per symbol with split table structure.

Schema: Separate tables for original vs reentry combinations (most_acurate_matirx_doc.md Section 6)
Indexing: Optimized indexes for combination lookup performance
Growth: Bounded growth proportional to number of currency pairs and trade volume

This SRS provides a comprehensive architectural view synthesized from all four source documents, maintaining traceability while organizing information in a structured, IEEE 830-compliant format. Each requirement references its source documentation and includes implementation details where specified in the original materials.RetryDIdentified the processes and sub processes of the systemEditMapped out comprehensive system processes and sub-processes systematically.The user is asking me to identify the processes and sub-processes of the HUEY_P trading system based on the documentation I've analyzed. I need to extract and organize the various processes that occur within this system, breaking them down into main processes and their constituent sub-processes.
Looking at the documentation, I can identify several major process flows:

Economic Calendar Processing
Signal Generation and Processing
Communication Bridge Management
Trade Execution and Management
Reentry Decision Processing
Data Persistence and Management
System Health Monitoring
Configuration Management
Performance Analysis and Reporting

Let me break each of these down into their sub-processes based on the technical documentation.
From the technical manual, I can see detailed process flows for:

Calendar import and processing pipeline
Signal generation and validation
Bridge communication with failover
Trade execution state machine
Reentry matrix decision logic
Database operations
Health monitoring and validation

From the tech spec, I can see the process requirements and constraints.
From the dependency manifest, I can see the orchestration processes.
From the reentry matrix doc, I can see the detailed reentry decision processes.
Let me organize this systematically.HUEY_P Trading System - Process and Sub-Process Identification
Based on analysis of the system architecture documentation, the HUEY_P trading system operates through nine major processes with detailed sub-process hierarchies:
1. Economic Calendar Processing
Primary Process: Transform raw economic calendar data into actionable trading signals
1.1 Calendar Import Process

1.1.1 File Detection and Validation

Monitor Downloads folder for calendar CSV files
Apply pattern matching (ff_calendar*.csv, economiccalendar*.csv)
Validate file format and integrity
Archive processed files


1.1.2 Data Parsing and Transformation

Parse CSV structure with error handling
Convert timestamps to CST with DST adjustment
Filter events by impact level and currency relevance
Quality score assignment and validation



1.2 Event Processing Pipeline

1.2.1 Anticipation Event Generation

Generate 1hr, 2hr, 4hr advance events for high/medium impact
Calculate optimal trigger timing offsets
Resolve scheduling conflicts between overlapping events


1.2.2 Equity Market Event Integration

Add Tokyo, London, New York market open events
Regional-specific timing and impact classification
Currency pair relevance mapping



1.3 Signal Staging Process

1.3.1 Parameter Set Assignment

Rotate through 4 parameter sets for diversification
Map event characteristics to optimal parameter configurations
Apply trading profile adjustments (conservative/moderate/aggressive)


1.3.2 Signal Export and Distribution

Generate CSV signal files for MQL4 consumption
Update signal entry system with new triggers
Coordinate with bridge communication systems



2. Signal Generation and Processing
Primary Process: Generate and validate trading signals from multiple sources
2.1 Multi-Source Signal Aggregation

2.1.1 Calendar-Based Signal Processing

Process economic event triggers with timing precision
Apply impact-based confidence scoring
Handle anticipation vs actual event differentiation


2.1.2 Technical Analysis Signal Integration

Process indicator-based signals (ALL_INDICATORS type)
Validate technical signal quality and timing
Merge with fundamental analysis from calendar events


2.1.3 External Signal Reception

Monitor CSV files for external signal sources
Parse and validate JSON signal formats from DLL socket
Apply signal source priority and conflict resolution



2.2 Signal Validation and Enhancement

2.2.1 Market Condition Analysis

Assess current spread conditions and market hours
Evaluate proximity to future economic events
Apply time-based filters and blackout periods


2.2.2 Risk Assessment and Sizing

Calculate appropriate position sizes based on signal confidence
Apply account equity and risk percentage constraints
Validate against maximum position limits


2.2.3 Signal Quality Scoring

Combine confidence metrics from multiple sources
Apply historical performance weighting
Generate final signal strength assessment



3. Communication Bridge Management
Primary Process: Maintain reliable communication pathways between system components
3.1 Bridge Health Monitoring

3.1.1 Primary Bridge (DLL+Socket) Management

Monitor TCP socket connection on port 8001
Track latency and throughput metrics (<10ms target)
Detect connection failures and initiate recovery


3.1.2 Secondary Bridge (Named Pipes) Oversight

Monitor Windows named pipe connectivity
Track performance metrics (<50ms target)
Manage backup communication queue


3.1.3 Tertiary Bridge (File-Based) Supervision

Monitor file system access and permissions
PowerShell script coordination for file operations
Handle slowest but most reliable communication path



3.2 Failover Orchestration

3.2.1 Automatic Bridge Switching

Detect primary bridge failures within 30 seconds
Execute seamless failover to secondary systems
Maintain message queues during transitions


3.2.2 Recovery and Restoration

Attempt primary bridge reconnection
Validate restored connections before switching back
Log all failover events for analysis



3.3 Message Processing and Routing

3.3.1 Protocol Message Handling

Process HEARTBEAT, STATUS_REQUEST, TRADE_UPDATE messages
Apply rate limiting and burst controls
Route messages to appropriate destination services


3.3.2 Error Handling and Retry Logic

Implement exponential backoff for failed messages
Maintain dead letter queues for undeliverable messages
Generate alerts for persistent communication failures



4. Trade Execution and Management
Primary Process: Execute trading strategies across 30 currency pairs
4.1 State Machine Management

4.1.1 State Transition Control

Manage IDLE → ORDERS_PLACED → TRADE_TRIGGERED → PAUSED states
Validate state transitions and handle edge cases
Persist state information for recovery after MT4 restarts


4.1.2 Error Recovery and Circuit Breakers

Detect and respond to consecutive error conditions
Implement emergency stops for account protection
Coordinate recovery procedures across multiple EAs



4.2 Straddle Order Management

4.2.1 Order Placement and Validation

Calculate Buy Stop and Sell Stop prices with distance parameters
Validate stop loss and take profit levels against broker constraints
Apply slippage tolerance and retry logic for order placement


4.2.2 Order Monitoring and Adjustment

Track pending order status and expiration times
Handle partial fills and order modifications
Cancel opposite orders when one side triggers



4.3 Dynamic Risk Management

4.3.1 Position Sizing Calculation

Calculate lot sizes based on risk percentage and stop loss distance
Apply account equity fluctuation adjustments
Enforce minimum/maximum lot size constraints


4.3.2 Account Protection Monitoring

Track daily drawdown against configured limits
Monitor margin usage and available equity
Implement automatic trading halts for risk protection



5. Reentry Decision Processing
Primary Process: Analyze trade outcomes and determine reentry actions using 4D matrix
5.1 Outcome Classification

5.1.1 Trade Result Analysis

Categorize outcomes: FULL_SL, PARTIAL_LOSS, BREAKEVEN, PARTIAL_PROFIT, FULL_TP, BEYOND_TP
Calculate actual vs expected performance metrics
Determine trade duration for ECO_HIGH/ECO_MED categorization


5.1.2 Context Assessment

Evaluate future event proximity (IMMEDIATE, SHORT, LONG, EXTENDED)
Assess market conditions and volatility environment
Apply signal-specific contextual factors



5.2 Matrix Lookup and Decision

5.2.1 Combination Identification

Generate standardized combination ID using colon-delimited format
Apply conditional duration logic for ECO signal types
Validate against generation limits (max R2)


5.2.2 Action Determination

Lookup matrix cell configuration for specific combination
Apply user overrides and performance-based adjustments
Generate reentry parameters: action type, size multiplier, delay, confidence adjustment



5.3 Reentry Execution Control

5.3.1 Safety Validation

Verify generation limits and attempt constraints
Validate account conditions and risk limits
Check market hours and spread conditions


5.3.2 Parameter Application and Execution

Apply size multipliers and confidence adjustments
Implement specified delays before reentry
Execute new trade with modified parameters



6. Data Persistence and Management
Primary Process: Store and manage trade data, configurations, and system state
6.1 Database Operations

6.1.1 Trade History Management

Insert trade records with complete execution details
Update trades with close information and P&L calculations
Maintain reentry chain linkages and generation tracking


6.1.2 Matrix Configuration Storage

Store original combinations (28 per symbol)
Store reentry combinations (624 per symbol)
Track user modifications and performance statistics



6.2 Configuration Management

6.2.1 Hierarchical Configuration Loading

Load YAML master configurations with validation
Process CSV parameter files with constraint checking
Apply configuration inheritance and override logic


6.2.2 Hot Reload Processing

Detect configuration file changes
Validate new configurations before application
Coordinate updates across Python services and MQL4 EAs



6.3 Backup and Archival

6.3.1 Automated Backup Procedures

Daily database backups with compression
Configuration file versioning and archival
Log file rotation with retention policies


6.3.2 Data Recovery and Validation

Validate backup integrity and completeness
Implement recovery procedures for data corruption
Maintain 7-year trade history for regulatory compliance



7. System Health Monitoring
Primary Process: Monitor system components and ensure operational reliability
7.1 Component Health Assessment

7.1.1 Service Health Validation

Monitor Python service health files with 2-minute freshness requirement
Validate EA heartbeat files updated every 30 seconds
Check bridge connectivity status and performance metrics


7.1.2 Dependency Validation

Verify all 652 combinations per symbol are accessible
Validate file system permissions and access
Check database connectivity and table integrity



7.2 Performance Monitoring

7.2.1 Latency and Throughput Tracking

Monitor signal processing latency (<100ms p95)
Track trade execution latency (<200ms p99)
Measure bridge communication performance


7.2.2 Resource Utilization Assessment

Monitor CPU and memory usage across all components
Track disk usage and database growth
Alert on resource threshold breaches



7.3 Alert and Notification Management

7.3.1 Critical Alert Processing

Generate immediate alerts for system failures
Escalate persistent issues with increasing severity
Coordinate with external notification systems


7.3.2 Performance Degradation Detection

Identify gradual performance degradation trends
Predict potential system issues before failures
Generate preventive maintenance recommendations



8. Configuration Management
Primary Process: Manage system configuration across multiple components and environments
8.1 Configuration Distribution

8.1.1 Multi-Component Synchronization

Distribute master configuration changes to all Python services
Deploy EA-specific configurations to MQL4 components
Coordinate PowerShell script configuration updates


8.1.2 Version Control and Rollback

Maintain configuration version history
Implement automatic rollback on validation failures
Track configuration changes with audit trails



8.2 Profile Management

8.2.1 Trading Profile Deployment

Deploy conservative/moderate/aggressive profile variants
Apply profile-specific parameter adjustments
Coordinate profile changes across currency pairs


8.2.2 Reentry Profile Configuration

Manage 652 combinations per symbol across profiles
Apply conditional logic for ECO vs non-ECO signals
Validate profile consistency and completeness



9. Performance Analysis and Reporting
Primary Process: Analyze system performance and generate insights for optimization
9.1 Trading Performance Analysis

9.1.1 Strategy Performance Evaluation

Calculate win rates, profit factors, and Sharpe ratios by strategy type
Analyze performance by currency pair and market conditions
Generate daily, weekly, and monthly performance reports


9.1.2 Reentry Matrix Effectiveness Assessment

Track performance of each matrix combination
Identify high and low performing reentry patterns
Generate recommendations for matrix optimization



9.2 System Performance Analysis

9.2.1 Component Performance Profiling

Analyze function-level execution times and bottlenecks
Track memory usage patterns and optimization opportunities
Generate system performance trending reports


9.2.2 Operational Efficiency Assessment

Measure bridge utilization and failover frequencies
Analyze signal processing efficiency and accuracy
Generate operational improvement recommendations



These processes operate continuously and concurrently, with complex interdependencies managed through the multi-bridge communication system and coordinated by the PowerShell management layer. The system's architecture ensures that process failures in non-critical components don't compromise core trading functionality, while providing comprehensive monitoring and recovery capabilities.