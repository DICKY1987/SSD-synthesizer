# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a sophisticated hybrid MetaTrader 4 (MT4) Expert Advisor trading system with a Python-based monitoring interface. The system combines automated MQL4 trading logic with real-time Python analysis, monitoring, and management tools.

**Location**: MetaTrader 4 terminal directory for Forex.com-Live trading account  
**Terminal ID**: `F2262CFAFF47C27887389DAB2852351A`  
**System**: HUEY_P Trading System with Python Interface

## Core Architecture Components

### MQL4 Expert Advisor Layer
- **Main EA**: HUEY_P_EA_ExecutionEngine_8 (7000+ line sophisticated trading system)
- **Strategy**: Straddle orders with dynamic risk management and adaptive parameters
- **Communication**: Socket-based via `MQL4_DLL_SocketBridge.dll` for Python interface
- **State Management**: Multi-state system (IDLE → ORDERS_PLACED → TRADE_TRIGGERED → PAUSED)

### Python Interface System
**Modular Architecture**:
```
core/           - Core application components (AppController, DatabaseManager, EAConnector)
tabs/           - UI tab implementations (LiveDashboard, TradeHistory, SystemStatus)
widgets/        - Reusable UI components (StatusIndicators, Charts, TradeTable)
utils/          - Utility functions (calculations, circuit_breaker, config_validator)
```

### Communication Bridge
- **Primary**: Socket communication via DLL bridge (ports 5555/9999)
- **Fallback**: CSV-based file communication when socket unavailable
- **Protocol**: Structured message types (HEARTBEAT, STATUS_REQUEST, TRADE_UPDATE, ERROR)

## Development Commands

### Python Environment Setup
```bash
# Set up Python environment
python -m venv venv
venv\Scripts\activate
pip install -r huey_requirements.txt

# Main interface applications
python huey_main.py                    # Primary trading interface
python tkinter_main_ui.py             # Alternative tkinter interface
python floating_timer_ui.py           # Minimal floating timer display
```

### Database Operations
```bash
# Database management
python init_database.py               # Initialize/reset database
python test_database_operations.py    # Test database functionality
python fix_database_schema.py         # Fix schema issues if needed

# Database location: Database/trading_system.db (SQLite)
# Automated backups: Database/trading_system.backup_*.db
```

### MQL4 Development & Testing
```bash
# Compilation (MetaTrader 4 MetaEditor required)
# Use Ctrl+F7 in MetaEditor or MT4's built-in compiler

# Testing framework
.\run_mql4_tests.ps1                   # PowerShell script for automated MQL4 testing
.\run_mql4_tests.ps1 -CompileOnly      # Compilation only
.\run_mql4_tests.ps1 -RunTests -GenerateReport  # Full test with HTML report
```

### DLL Building (if required)
```bash
# Navigate to DLL directory
cd MQL4_DLL_SocketBridge

# Build DLL (requires Visual Studio 2019+ and CMake)
build_dll.bat

# Alternative manual build
cmake .. -G "Visual Studio 16 2019" -A Win32
cmake --build . --config Release

# Test DLL functionality
python test_exports.py
python simple_test.py
```

### System Testing & Integration
```bash
# Communication bridge testing
python test_ea_python_communication.py    # EA-Python bridge validation
python test_signal_processing.py          # Signal processing validation  
python test_system_integration.py         # Full system integration tests
python test_config_manager.py            # Configuration management tests

# Individual component testing
python test_integration.py               # System integration tests
python test_port_5555.py                # Port connectivity testing
```

### Monitoring & Diagnostics
```bash
# System health monitoring
bridge_diagnostic.ps1                    # Bridge diagnostic script
emergency_bridge_recovery.ps1           # Emergency recovery procedures

# Performance monitoring
python simple_socket_test.py            # Basic socket connectivity test
```

## Key Configuration Files

### Main Configuration (`huey_config.txt`)
YAML-structured configuration covering:
- Application settings (window size, refresh intervals)
- Database configuration (path, backup settings, timeouts)  
- EA bridge settings (host, ports, retry logic, heartbeat)
- Display preferences (theme, fonts, auto-refresh)
- Logging configuration (levels, file rotation)
- Alert thresholds (profit/loss, drawdown, equity)

### EA Configuration (set via MT4 interface)
```mql4
// Core operation modes
bool AutonomousMode = true;        // Internal trading vs external signals
bool EnableDLLSignals = true;      // Socket-based external communication
bool EnableCSVSignals = false;     // File-based fallback communication

// Risk management
double RiskPercent = 1.0;          // Risk per trade as % of equity
double MaxLotSize = 1.0;           // Position size cap
double SafeMarginPercentage = 50.0; // Margin utilization limit

// Advanced debugging and validation
bool EnableAdvancedDebug = true;   // Enhanced logging system
bool EnableStateValidation = true; // State integrity checking
bool EnablePortfolioRisk = true;   // Portfolio-wide risk assessment
```

## Multi-Mode Operation

### Full Integration Mode (Recommended)
- EA: `AutonomousMode = true`, `EnableDLLSignals = true`
- Python: Full GUI with real-time EA communication
- Requires: `MQL4_DLL_SocketBridge.dll` properly deployed

### Monitoring-Only Mode (DLL-free operation)
- EA: `AutonomousMode = true`, `EnableDLLSignals = false`  
- Python: Runs with expected connection warnings, full analysis capabilities
- Use when DLL deployment is not feasible

### CSV Signal Mode (Alternative communication)
- EA: `EnableCSVSignals = true`, `EnableDLLSignals = false`
- Python: File-based signal generation and monitoring
- Uses: `trading_signals.csv`, `trade_responses.csv`

## Critical Development Guidelines

### MQL4 Development Constraints
- **NEVER rewrite** the entire EA file - only modify specific sections
- **STRICTLY MQL4 syntax** - NO MQL5 functions, structures, or keywords
- **Compilation**: ONLY use MetaTrader 4 MetaEditor (Ctrl+F7)
- **New features**: MUST be controlled by input parameters with safe defaults
- **Backward compatibility**: ALL existing functionality must be preserved

### Error Handling Architecture
- **Enhanced Classification**: 50+ error codes including DLL-specific errors (5000+ range)
- **Circuit Breaker**: Automatic EA pause after consecutive errors
- **Recovery Actions**: Automatic retry logic for transient failures
- **Logging**: Class-based `LogManager` system with structured output

### Database Design Patterns  
- **SQLite backend** with automatic backup strategy
- **Connection pooling** with timeout and retry mechanisms
- **Schema validation** with automated migration capabilities
- **Performance optimization** through caching and batch operations

### Python Architecture Principles
- **Modular design** with clear separation between core/tabs/widgets/utils
- **Async communication** with connection health monitoring
- **Configuration-driven** behavior with runtime validation
- **Error resilience** with graceful degradation when EA unavailable

## System Deployment Workflow

### Pre-Deployment Checklist
1. **DLL Compilation**: Ensure `MQL4_DLL_SocketBridge.dll` is built (31,232 bytes expected)
2. **Database Initialization**: Run `python init_database.py` for clean setup
3. **MT4 Configuration**: Enable DLL imports in Expert Advisor settings  
4. **Port Availability**: Verify ports 5555/9999 are available for communication
5. **File Permissions**: Ensure MT4 has read/write access to Libraries folder

### Live Deployment Steps
1. **Copy DLL**: `MQL4_DLL_SocketBridge.dll` → `<MT4_Installation>\MQL4\Libraries\`
2. **Load EA**: Place EA in `<MT4_Installation>\MQL4\Experts\` and attach to chart
3. **Start Python**: Launch `python huey_main.py` for monitoring interface
4. **Verify Connection**: Check socket communication in System Status tab
5. **Monitor Performance**: Use live dashboard for real-time system health

### System Recovery Procedures
- **Bridge Recovery**: Run `emergency_bridge_recovery.ps1` for communication issues
- **Database Recovery**: Use backup files in `Database/` with timestamp naming
- **EA Recovery**: Restart EA with `EnableStateValidation = true` for integrity checking
- **Python Recovery**: Restart interface - automatic reconnection with EA

## File Dependencies & External Requirements

### Required External Files
- `MQL4_DLL_SocketBridge.dll` - Core communication bridge (compile from source)
- Windows socket libraries - `wsock32.dll`, `ws2_32.dll` (system libraries)
- MT4 sound files - `ok.wav`, `expert.wav`, `alert.wav` etc. (in MT4\Sounds\)

### Optional CSV Data Files (MT4\Files\ folder)
- `trading_signals.csv` - External signal input (when `EnableCSVSignals = true`)
- `NewsCalendar.csv` - Economic events for trade filtering
- `TimeFilters.csv` - Trading blackout periods
- Generated logs - `HUEY_P_Log.txt`, daily CSV files

### Python Dependencies
Core requirements in `huey_requirements.txt`:
- Data: `pandas>=2.0.0`, `numpy>=1.24.0`
- GUI: `matplotlib>=3.7.0`, `plotly>=5.17.0` (tkinter built-in)
- Config: `PyYAML>=6.0`, `python-dateutil>=2.8.0`
- Network: `requests>=2.31.0`, `websockets>=11.0`
- System: `psutil>=5.9.0`, `colorlog>=6.7.0`
- Optional: `ttkthemes>=3.2.2`, `pystray>=0.19.4`, `seaborn>=0.12.0`

## Documentation Reference

### Primary Documentation Files
- `DEPLOYMENT_GUIDE.md` - Complete system deployment procedures  
- `DLL_REQUIREMENTS.md` - DLL setup and troubleshooting guide
- `COMMUNICATION_SYSTEM_DOCUMENTATION.md` - Protocol specifications
- `SOCKET_COMMUNICATION_PROTOCOL.md` - Technical communication details

### System Status (Current)
✅ **Python Interface**: Fully operational with modular architecture  
✅ **MQL4 EA Code**: Production-ready (7000+ lines, class-based architecture)  
✅ **Database System**: SQLite with automated backups and schema validation  
✅ **Testing Framework**: PowerShell-based MQL4 testing with HTML reporting  
❗ **Socket Communication**: Requires DLL deployment (see `DLL_REQUIREMENTS.md`)  
✅ **CSV Fallback**: File-based communication alternative available

This system represents a production-grade automated trading platform with enterprise-level risk management, comprehensive monitoring, and defensive security measures. All modifications must prioritize system stability and risk control.