File: CSVConfigAdapter.mqh

Basic Identification

Purpose: csv_config_adapter.txt CSV-based Configuration Reader - Provides a flexible configuration system that reads parameters from CSV files with auto-save functionality and file watching capabilities
File Type: MQL4 Include File
File Extension: .mqh


System Integration and Dependencies

Dependencies (What this file needs):

Includes/Imports: csv_config_adapter.txt ../Interfaces/IConfigProvider.mqh, ../Core/EventBusCore.mqh, ../Core/LoggerCore.mqh
DLL Imports: N/A
Configuration Files Read: csv_config_adapter.txt config.csv (default), supports custom filenames


Dependents (What other files need this file):

Any component requiring configuration management


Communication Channels Used:

csv_config_adapter.txt File I/O for CSV configuration files, Event Bus for configuration change notifications




Code and Logic Attributes

Primary Language: MQL4
Key Functions/Classes: csv_config_adapter.txt CSVConfigAdapter class implementing IConfigProvider and IEventHandler, GetString(), GetInt(), GetDouble(), GetBool(), SetParameter(), LoadConfiguration(), SaveConfiguration()
Configuration Parameters Defined/Used: csv_config_adapter.txt configFilename, autoSave, watchFile, checkInterval plus dynamic parameter storage


Deployment and Location

Expected Directory Path: {mt4_terminal_root}\MQL4\Include
Generation/Deployment Method: Copied to MT4 Include directory by deployment scripts




File: ErrorRecovery.mqh

Basic Identification

Purpose: error_recovery_mqh.txt Comprehensive system for error handling and recovery in MQL4, including strategies like retry, backoff, and fallback with recovery state management
File Type: MQL4 Include File
File Extension: .mqh


System Integration and Dependencies

Dependencies (What this file needs):

Includes/Imports: N/A
DLL Imports: N/A
Configuration Files Read: N/A


Dependents (What other files need this file):

MQL4 components requiring error handling and recovery


Communication Channels Used:

N/A - Internal error management




Code and Logic Attributes

Primary Language: MQL4
Key Functions/Classes: error_recovery_mqh.txt InitializeErrorRecovery(), LogError(), ClassifyErrorSeverity(), AttemptAutoRecovery(), ExecuteWithRetry()
Configuration Parameters Defined/Used: error_recovery_mqh.txt Recovery states (NORMAL, DEGRADED, EMERGENCY), error severity levels (LOW, MEDIUM, HIGH, CRITICAL), retry configuration (max_retries, retry_delay_seconds, backoff_multiplier)


Deployment and Location

Expected Directory Path: {mt4_terminal_root}\MQL4\Include
Generation/Deployment Method: Copied to MT4 Include directory by deployment scripts




File: MetricsEventHandler.mqh

Basic Identification

Purpose: MetricsEventHandler.txt Updates Metrics on Trading Events - Handles performance tracking and metrics collection for trading activities
File Type: MQL4 Include File
File Extension: .mqh


System Integration and Dependencies

Dependencies (What this file needs):

Includes/Imports: MetricsEventHandler.txt ../Core/EventBusCore.mqh, ../Core/LoggerCore.mqh, ../Core/MetricsCore.mqh
DLL Imports: N/A
Configuration Files Read: N/A


Dependents (What other files need this file):

Event-driven trading systems requiring metrics collection


Communication Channels Used:

MetricsEventHandler.txt Event Bus for receiving trading events, File I/O for session reports




Code and Logic Attributes

Primary Language: MQL4
Key Functions/Classes: MetricsEventHandler.txt MetricsEventHandler class implementing IEventHandler, HandlePositionChange(), HandleTradeSignal(), GenerateSessionReport()
Configuration Parameters Defined/Used: MetricsEventHandler.txt metricsUpdateInterval, session tracking variables, milestone thresholds


Deployment and Location

Expected Directory Path: {mt4_terminal_root}\MQL4\Include
Generation/Deployment Method: Copied to MT4 Include directory by deployment scripts




File: RiskEventHandler.mqh

Basic Identification

Purpose: RiskEventHandler.txt Processes Risk-Related Events - Centralized risk management with real-time monitoring and threshold enforcement
File Type: MQL4 Include File
File Extension: .mqh


System Integration and Dependencies

Dependencies (What this file needs):

Includes/Imports: RiskEventHandler.txt ../Core/EventBusCore.mqh, ../Core/LoggerCore.mqh, ../Core/RiskCore.mqh, ../Core/NotificationCore.mqh
DLL Imports: N/A
Configuration Files Read: N/A


Dependents (What other files need this file):

Trading systems requiring risk management and monitoring


Communication Channels Used:

RiskEventHandler.txt Event Bus for risk events, Notification system for alerts




Code and Logic Attributes

Primary Language: MQL4
Key Functions/Classes: RiskEventHandler.txt RiskEventHandler class implementing IEventHandler, HandlePositionChange(), HandleRiskUpdate(), UpdateDrawdown()
Configuration Parameters Defined/Used: RiskEventHandler.txt criticalRiskThreshold, warningRiskThreshold, maxConsecutiveLosses, maxDailyDrawdown


Deployment and Location

Expected Directory Path: {mt4_terminal_root}\MQL4\Include
Generation/Deployment Method: Copied to MT4 Include directory by deployment scripts



MQL4 Expert Advisors

File: TradingEA_EURUSD.mq4

Basic Identification

Purpose: production_mt4_template.txt Production Ready Template EA for EURUSD - Copy this file for each currency pair, change TRADING_PAIR only
File Type: MQL4 Expert Advisor
File Extension: .mq4


System Integration and Dependencies

Dependencies (What this file needs):

Includes/Imports: N/A (self-contained template)
DLL Imports: N/A
Configuration Files Read: production_mt4_template.txt Signal files, Response files (CSV format)


Dependents (What other files need this file):

Python signal generator (writes signals to CSV)


Communication Channels Used:

production_mt4_template.txt File-based communication via CSV files for signals and responses




Code and Logic Attributes

Primary Language: MQL4
Key Functions/Classes: production_mt4_template.txt OnInit(), OnTick(), OnDeinit(), ProcessSignal(), CheckAndProcessSignals(), ValidateAccountConditions()
Configuration Parameters Defined/Used: production_mt4_template.txt TRADING_PAIR, LOT_SIZE, ENABLE_TRADING, ENABLE_LOGGING, MAGIC_NUMBER_BASE, SLIPPAGE


Deployment and Location

Expected Directory Path: {mt4_terminal_root}\MQL4\Experts
Generation/Deployment Method: production_mt4_template.txt Compiled from template by deployment scripts, copied for each trading pair




File: SignalReceiver.mq4

Basic Identification

Purpose: SignalReceiver.txt Socket-based signal receiver EA that uses a custom C++ DLL for TCP/IP communication
File Type: MQL4 Expert Advisor
File Extension: .mq4


System Integration and Dependencies

Dependencies (What this file needs):

Includes/Imports: N/A
DLL Imports: SignalReceiver.txt SocketBridge.dll (StartServer(), StopServer(), GetNextSignal())
Configuration Files Read: N/A


Dependents (What other files need this file):

External signal sources sending TCP/IP signals


Communication Channels Used:

SignalReceiver.txt TCP/IP Socket server on configurable port (default 8888)




Code and Logic Attributes

Primary Language: MQL4
Key Functions/Classes: SignalReceiver.txt OnInit(), OnDeinit(), OnTimer(), ProcessSignal()
Configuration Parameters Defined/Used: SignalReceiver.txt ListenPort, Lots, Slippage, MagicNumber


Deployment and Location

Expected Directory Path: {mt4_terminal_root}\MQL4\Experts
Generation/Deployment Method: Compiled and deployed with DLL dependency




File: Enhanced EA with Reentry Logic

Basic Identification

Purpose: reentry_logic_ea.txt Enhanced EA Template with Reentry Logic - Implements die-roll reentry system based on trade outcomes
File Type: MQL4 Expert Advisor Template
File Extension: .mq4


System Integration and Dependencies

Dependencies (What this file needs):

Includes/Imports: reentry_logic_ea.txt <TradingEACore.mqh>, <BridgeInterface.mqh>
DLL Imports: N/A
Configuration Files Read: reentry_logic_ea.txt EURUSD_config.csv, EURUSD_reentry.csv


Dependents (What other files need this file):

Database for reentry chain tracking


Communication Channels Used:

File-based configuration, Database logging




Code and Logic Attributes

Primary Language: MQL4
Key Functions/Classes: reentry_logic_ea.txt CReentryLogic class, DetermineNextAction(), ExecuteReentryAction(), ProcessClosedTrade()
Configuration Parameters Defined/Used: reentry_logic_ea.txt ENABLE_REENTRY_SYSTEM, REENTRY_DELAY_SECONDS, REENTRY_ACTION_* parameters


Deployment and Location

Expected Directory Path: {mt4_terminal_root}\MQL4\Experts
Generation/Deployment Method: Template for generating reentry-enabled EAs



Python Service Files

File: reentry_python_integration.py

Basic Identification

Purpose: reentry_python_integration.py Reentry System Integration for Multi-EA Trading System - Handles reentry analytics, optimization, and monitoring
File Type: Python Service
File Extension: .py


System Integration and Dependencies

Dependencies (What this file needs):

Includes/Imports: reentry_python_integration.py sqlite3, pandas, numpy, datetime, json, logging, dataclasses, enum
DLL Imports: N/A
Configuration Files Read: Database connections, CSV configuration files


Dependents (What other files need this file):

Reentry monitoring service, optimization scripts


Communication Channels Used:

reentry_python_integration.py Database connections (SQLite), File I/O for configuration and reports




Code and Logic Attributes

Primary Language: Python
Key Functions/Classes: reentry_python_integration.py ReentryAnalytics, ReentryConfigManager, ReentryMonitoringService classes, analyze_action_performance(), calculate_optimal_parameters()
Configuration Parameters Defined/Used: reentry_python_integration.py Database path, pair symbols, optimization parameters, performance thresholds


Deployment and Location

Expected Directory Path: {trading_system_root}\Python\services\reentry
Generation/Deployment Method: Part of Python service deployment



PowerShell Scripts and Modules

File: PathManager.psm1

Basic Identification

Purpose: PathManager.psm1 Trading System Path Management Module - Provides safe, centralized path management for MT4 trading system development
File Type: PowerShell Module
File Extension: .psm1


System Integration and Dependencies

Dependencies (What this file needs):

Includes/Imports: N/A
DLL Imports: N/A
Configuration Files Read: PathManager.psm1 paths_config.txt configuration file


Dependents (What other files need this file):

All PowerShell deployment and management scripts


Communication Channels Used:

File I/O for configuration reading




Code and Logic Attributes

Primary Language: PowerShell
Key Functions/Classes: PathManager.psm1 Initialize-PathManager, Get-TradingSystemPath, Get-SourcePath, Get-MT4Path, Copy-ToMT4, Deploy-AllFiles, Show-PathConfiguration
Configuration Parameters Defined/Used: PathManager.psm1 Path mappings (base_paths, source_paths, mt4_paths, build_paths, deployment_mappings, backup_paths, utility_paths)


Deployment and Location

Expected Directory Path: {trading_system_root}\Scripts
Generation/Deployment Method: Source module, loaded by other scripts




File: Backup_Current.ps1

Basic Identification

Purpose: Backup_Current.ps1 Database Backup Automation Script - Comprehensive backup solution for trading system database
File Type: PowerShell Script
File Extension: .ps1


System Integration and Dependencies

Dependencies (What this file needs):

Includes/Imports: Backup_Current.ps1 PathManager.psm1 module
DLL Imports: N/A
Configuration Files Read: Path configuration via PathManager


Dependents (What other files need this file):

Automated backup scheduling, maintenance procedures


Communication Channels Used:

Backup_Current.ps1 Database connections (SQLite, PostgreSQL), File I/O, Cloud storage APIs (S3, Azure)




Code and Logic Attributes

Primary Language: PowerShell
Key Functions/Classes: Backup_Current.ps1 Backup-SqliteDatabase(), Backup-PostgresDatabase(), Compress-Backup(), Encrypt-Backup(), Test-BackupIntegrity()
Configuration Parameters Defined/Used: Backup_Current.ps1 DatabaseType, DatabasePath, BackupType, RetentionDays, CloudProvider, compression and encryption options


Deployment and Location

Expected Directory Path: {trading_system_root}\Scripts
Generation/Deployment Method: Scheduled execution for automated backups



Configuration and Data Files

File: Reentry Configuration Structure

Basic Identification

Purpose: reentry_config_structure.txt Reentry Configuration Template - Defines configuration structure for 30-EA architecture with multiple profiles
File Type: Configuration Template/Documentation
File Extension: .csv/.yaml (multiple formats)


System Integration and Dependencies

Dependencies (What this file needs):

Includes/Imports: N/A
DLL Imports: N/A
Configuration Files Read: N/A


Dependents (What other files need this file):

reentry_config_structure.txt Reentry-enabled EAs, Python optimization services, PowerShell deployment scripts


Communication Channels Used:

File I/O for configuration reading




Code and Logic Attributes

Primary Language: CSV/YAML Configuration
Key Functions/Classes: N/A - Configuration templates
Configuration Parameters Defined/Used: reentry_config_structure.txt Action types (NO_REENTRY, REDUCE_SIZE, SAME_TRADE, INCREASE_SIZE, AGGRESSIVE), size multipliers, delay seconds, confidence adjustments, safety limits


Deployment and Location

Expected Directory Path: {mt4_terminal_root}\MQL4\Files\config and {trading_system_root}\Python\config
Generation/Deployment Method: reentry_config_structure.txt Generated by PowerShell deployment scripts, deployed to multiple locations




File: requirements.txt

Basic Identification

Purpose: requirements.txt Trading System Python Dependencies - Complete list of Python packages required for the trading system
File Type: Python Dependencies List
File Extension: .txt


System Integration and Dependencies

Dependencies (What this file needs):

Includes/Imports: N/A
DLL Imports: N/A
Configuration Files Read: N/A


Dependents (What other files need this file):

Python environment setup, Docker containers, deployment scripts


Communication Channels Used:

N/A




Code and Logic Attributes

Primary Language: Text (pip format)
Key Functions/Classes: N/A - Dependencies list
Configuration Parameters Defined/Used: requirements.txt Core dependencies (numpy, pandas, pyyaml), database libraries (sqlite3, sqlalchemy), network/communication (asyncio, aiohttp, websockets), analysis tools (scikit-learn, matplotlib), development tools (pytest, black, mypy)


Deployment and Location

Expected Directory Path: {trading_system_root}\Python
Generation/Deployment Method: Used by pip install and Docker builds



Documentation Files

File: claude_signal_spec.md

Basic Identification

Purpose: claude_signal_spec.md Claude-Compatible Signal Generation Specification - Complete technical specification for Claude-based signal generation
File Type: Markdown Documentation
File Extension: .md


System Integration and Dependencies

Dependencies (What this file needs):

Includes/Imports: N/A
DLL Imports: N/A
Configuration Files Read: N/A


Dependents (What other files need this file):

Signal generation implementations, AI model training


Communication Channels Used:

N/A




Code and Logic Attributes

Primary Language: Markdown
Key Functions/Classes: N/A - Specification document
Configuration Parameters Defined/Used: claude_signal_spec.md Signal generation logic, confidence calculation, direction selection, strategy ID format, CSV output format, health monitoring criteria


Deployment and Location

Expected Directory Path: Documentation directory
Generation/Deployment Method: Reference specification for development




File: signal_generation_spec.md

Basic Identification

Purpose: signal_generation_spec.md Claude Trading System - Signal Generation Technical Reference - Complete technical specification for signal generation service
File Type: Markdown Documentation
File Extension: .md


System Integration and Dependencies

Dependencies (What this file needs):

Includes/Imports: N/A
DLL Imports: N/A
Configuration Files Read: N/A


Dependents (What other files need this file):

Signal generation service implementations


Communication Channels Used:

N/A




Code and Logic Attributes

Primary Language: Markdown
Key Functions/Classes: N/A - Technical specification
Configuration Parameters Defined/Used: signal_generation_spec.md Signal trigger conditions, confidence determination, direction selection logic, strategy ID generation, file output format, health & quality control


Deployment and Location

Expected Directory Path: Documentation directory
Generation/Deployment Method: Technical reference for developers




File: reentry_deployment_guide.md

Basic Identification

Purpose: reentry_deployment_guide.md Reentry System Deployment Guide - Complete Implementation Guide for 30-EA Architecture
File Type: Markdown Documentation
File Extension: .md


System Integration and Dependencies

Dependencies (What this file needs):

Includes/Imports: N/A
DLL Imports: N/A
Configuration Files Read: N/A


Dependents (What other files need this file):

Deployment procedures, system implementation


Communication Channels Used:

N/A




Code and Logic Attributes

Primary Language: Markdown
Key Functions/Classes: N/A - Deployment guide
Configuration Parameters Defined/Used: reentry_deployment_guide.md Pre-deployment checklist, component deployment procedures, integration testing, production deployment, monitoring and optimization


Deployment and Location

Expected Directory Path: Documentation directory
Generation/Deployment Method: Implementation guide for operations




File: TROUBLESHOOTING.md

Basic Identification

Purpose: TROUBLESHOOTING.md Trading System Troubleshooting Guide - Comprehensive guide for resolving common issues with the Enhanced Trading System
File Type: Markdown Documentation
File Extension: .md


System Integration and Dependencies

Dependencies (What this file needs):

Includes/Imports: N/A
DLL Imports: N/A
Configuration Files Read: N/A


Dependents (What other files need this file):

Operations and maintenance procedures


Communication Channels Used:

N/A




Code and Logic Attributes

Primary Language: Markdown
Key Functions/Classes: N/A - Troubleshooting guide
Configuration Parameters Defined/Used: TROUBLESHOOTING.md Installation issues, communication issues, signal processing issues, database issues, trading logic issues, performance issues, advanced troubleshooting techniques


Deployment and Location

Expected Directory Path: Documentation directory
Generation/Deployment Method: Operations reference guide




File: UserManual.txt

Basic Identification

Purpose: UserManual.txt TRADING SYSTEM USER MANUAL - Comprehensive user documentation for the automated trading solution
File Type: Text Documentation
File Extension: .txt


System Integration and Dependencies

Dependencies (What this file needs):

Includes/Imports: N/A
DLL Imports: N/A
Configuration Files Read: N/A


Dependents (What other files need this file):

End user operations


Communication Channels Used:

N/A




Code and Logic Attributes

Primary Language: Plain text
Key Functions/Classes: N/A - User documentation
Configuration Parameters Defined/Used: UserManual.txt System overview, supported currency pairs (30 pairs), installation guide, configuration system, operation procedures, troubleshooting, advanced features, maintenance tasks


Deployment and Location

Expected Directory Path: Documentation directory
Generation/Deployment Method: User reference documentation




File: comprehensive_readme.txt

Basic Identification

Purpose: comprehensive_readme.txt Enhanced Trading System - Complete Implementation - Main project README with comprehensive system overview
File Type: Text Documentation
File Extension: .txt


System Integration and Dependencies

Dependencies (What this file needs):

Includes/Imports: N/A
DLL Imports: N/A
Configuration Files Read: N/A


Dependents (What other files need this file):

Project overview and setup


Communication Channels Used:

N/A




Code and Logic Attributes

Primary Language: Plain text
Key Functions/Classes: N/A - Project documentation
Configuration Parameters Defined/Used: comprehensive_readme.txt Fixed critical issues, complete file structure, quick start guide, configuration system, key features, troubleshooting, performance optimizations


Deployment and Location

Expected Directory Path: Project root
Generation/Deployment Method: Main project documentation



Template and Logic Files

File: EA CSV Logic Explained

Basic Identification

Purpose: ea_csv_logic_explained.txt Logic and Calculations Behind the EA CSV File - Explains the purpose, logic, and calculation basis for EA-compatible CSV files
File Type: Documentation/Logic Specification
File Extension: .txt


System Integration and Dependencies

Dependencies (What this file needs):

Includes/Imports: N/A
DLL Imports: N/A
Configuration Files Read: N/A


Dependents (What other files need this file):

CSV file generators, EA implementations


Communication Channels Used:

N/A




Code and Logic Attributes

Primary Language: Text documentation
Key Functions/Classes: N/A - Logic explanation
Configuration Parameters Defined/Used: ea_csv_logic_explained.txt CSV execution flow, column descriptions (id, symbol, eventName, impact, tradeEnabled, entryTimeStr, slPips, tpPips, bufferPips, lotInput, winStartStr, winEndStr, magicNumber, strategy, notes), key calculations (lot size, execution checks)


Deployment and Location

Expected Directory Path: Documentation directory
Generation/Deployment Method: Reference documentation for CSV file structure




File: SignalProcessing_Template.txt

Basic Identification

Purpose: SignalProcessing_Template.txt CORRECT SIGNAL PROCESSING TEMPLATE - Template showing proper signal processing implementation
File Type: Code Template
File Extension: .txt


System Integration and Dependencies

Dependencies (What this file needs):

Includes/Imports: N/A
DLL Imports: N/A
Configuration Files Read: N/A


Dependents (What other files need this file):

EA implementations requiring signal processing


Communication Channels Used:

N/A




Code and Logic Attributes

Primary Language: MQL4 template
Key Functions/Classes: SignalProcessing_Template.txt ProcessSignal(), CheckForNewSignals(), ReadNextSignal()
Configuration Parameters Defined/Used: Signal data structures and processing logic


Deployment and Location

Expected Directory Path: Templates directory
Generation/Deployment Method: Reference template for development