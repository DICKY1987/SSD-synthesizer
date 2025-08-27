# HUEY_P Trading Interface - Streamlined Version

A Python-based desktop trading interface for the HUEY_P algorithmic trading system. This streamlined version provides essential functionality for monitoring live trading metrics, analyzing trade history, and managing system settings.

## Features

### 📊 Live Dashboard
- Real-time EA state and recovery status monitoring
- Account metrics (equity, balance, daily P&L)
- Active positions tracking with unrealized P&L
- Risk management indicators
- System connection status

### 📈 Trade History
- Comprehensive trade history analysis
- Filtering by time period, symbol, and result
- Performance statistics (win rate, profit factor, drawdowns)
- Symbol-specific performance breakdown
- Data export functionality

### ⚡ System Status
- Connection health monitoring (Database, EA Bridge, MT4, Broker)
- System performance metrics (CPU, memory, network latency)
- Error log display and management
- Component status tracking
- Emergency controls and system restart options

### ⚙️ Settings Panel
- Interface configuration (window size, themes, refresh rates)
- Trading parameters (risk management, position sizing)
- Broker connection settings
- Advanced system configuration
- Configuration import/export

## System Requirements

- Python 3.8 or higher
- Windows 10/11 (for MT4 integration)
- Existing HUEY_P EA system with database
- Active C++ bridge for EA communication

## Installation

### 1. Setup Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r HUEY_PPYTH_requirements.txt
```

### 2. Configuration

1. **Copy configuration files** to your system:
   - `HUEY_PPYTH_config.yaml` - Main interface configuration
   - Create `Config/` directory if it doesn't exist
   - Ensure your existing HUEY_P configuration files are accessible

2. **Update database path** in `HUEY_PPYTH_config.yaml`:
   ```yaml
   database:
     path: "path/to/your/Database/trading_system.db"
   ```

3. **Configure EA bridge connection**:
   ```yaml
   ea_bridge:
     host: "localhost"
     port: 9999  # Match your C++ bridge port
   ```

### 3. Directory Structure

Ensure your directory structure matches:

```
TradingInterface/
├── HUEY_PPYTH_main.py
├── HUEY_PPYTH_config.yaml
├── HUEY_PPYTH_requirements.txt
├── core/
│   ├── HUEY_PPYTH_core__init__.py
│   ├── HUEY_PPYTH_app_controller.py
│   ├── HUEY_PPYTH_database_manager.py
│   ├── HUEY_PPYTH_ea_connector.py
│   └── HUEY_PPYTH_data_models.py
├── tabs/
│   ├── HUEY_PPYTH_tabs__init__.py
│   ├── HUEY_PPYTH_live_dashboard.py
│   ├── HUEY_PPYTH_trade_history.py
│   ├── HUEY_PPYTH_system_status.py
│   └── HUEY_PPYTH_settings_panel.py
└── Config/  # Your existing HUEY_P config directory
    ├── claude_trading_config.yaml
    ├── broker_settings.yaml
    └── pairs/
```

## Usage

### Starting the Interface

```bash
# Ensure virtual environment is activated
# Navigate to TradingInterface directory
python HUEY_PPYTH_main.py
```

### First-Time Setup

1. **Configure Database Connection**:
   - Go to Settings Panel → Advanced → Database
   - Set the correct path to your trading_system.db file
   - Save settings

2. **Configure EA Bridge**:
   - Go to Settings Panel → Broker → Connection
   - Verify EA Bridge Port matches your C++ bridge configuration
   - Test connection using System Status → Connection controls

3. **Verify System Health**:
   - Check System Status tab for all green indicators
   - Ensure Database and EA Bridge show "CONNECTED"
   - Verify heartbeat messages are being received

### Daily Operation

1. **Start your trading system components**:
   - MT4 terminal with HUEY_P EAs loaded
   - C++ bridge application
   - Database accessible

2. **Launch the interface**:
   ```bash
   python HUEY_PPYTH_main.py
   ```

3. **Monitor trading**:
   - **Live Dashboard**: Real-time monitoring of active trades and metrics
   - **Trade History**: Review completed trades and performance
   - **System Status**: Ensure all connections are healthy

## Key Components

### Core System

- **AppController**: Main application coordinator
- **DatabaseManager**: SQLite database interface with caching
- **EAConnector**: Communication with EA via C++ bridge using HUEY_P protocol
- **DataModels**: Type-safe data structures for all system data

### User Interface

- **LiveDashboard**: Real-time trading metrics and active positions
- **TradeHistory**: Historical analysis with filtering and statistics
- **SystemStatus**: Health monitoring and error management
- **SettingsPanel**: Configuration management with validation

### Communication Protocol

Uses the standard HUEY_P message protocol:
- **HEARTBEAT**: Connection health monitoring
- **STATUS_REQUEST/STATUS_RESPONSE**: System state queries
- **TRADE_UPDATE**: Live trade information
- **ERROR**: Error reporting and handling

## Troubleshooting

### Connection Issues

1. **Database Connection Failed**:
   - Verify database path in configuration
   - Check file permissions
   - Ensure database file exists and is not corrupted

2. **EA Bridge Connection Failed**:
   - Verify C++ bridge is running
   - Check port configuration matches
   - Ensure firewall allows connection
   - Verify MT4 EAs are loaded and active

3. **No Trade Data**:
   - Check if EAs have executed any trades
   - Verify database contains trade_results table
   - Check date filters in Trade History tab

### Performance Issues

1. **Slow Interface Response**:
   - Increase refresh interval in settings
   - Clear database cache (System Status → Clear Cache)
   - Reduce number of displayed trade history records

2. **High Memory Usage**:
   - Restart interface application
   - Check for memory leaks in logs
   - Reduce cache duration in advanced settings

### Data Issues

1. **Missing Trade History**:
   - Verify database connection
   - Check if trades are being written to database by EAs
   - Refresh trade history data manually

2. **Incorrect Metrics**:
   - Verify EA is sending correct data
   - Check for data synchronization issues
   - Clear cache and refresh all data

## Configuration Reference

### Main Configuration (`HUEY_PPYTH_config.yaml`)

```yaml
app:
  refresh_interval: 1000  # UI update frequency (ms)

database:
  path: "Database/trading_system.db"  # Path to SQLite database
  backup_on_start: true              # Create backup on startup

ea_bridge:
  host: "localhost"    # EA bridge host
  port: 9999          # EA bridge port
  timeout: 5          # Connection timeout (seconds)

display:
  theme: "clam"       # UI theme
  font_size: 10       # Interface font size
```

### Trading Configuration (External Files)

The interface reads from your existing HUEY_P configuration files:
- `Config/claude_trading_config.yaml` - Trading parameters
- `Config/broker_settings.yaml` - Broker connection settings
- `Config/pairs/*.yaml` - Symbol-specific configurations

## Support and Development

### Logging

Application logs are written to `huey_interface.log` with configurable detail levels.
Check System Status → Error Log for real-time log viewing.

### Extending the Interface

The modular design allows for easy extension:
- Add new tabs by implementing tab classes
- Extend data models for new metrics
- Add new alert types and notification methods
- Integrate additional data sources

### Integration with Existing HUEY_P System

This interface is designed to work seamlessly with your existing:
- MT4 Expert Advisors
- C++ communication bridge
- SQLite trading database
- Configuration management system

No changes are required to your existing trading logic or EAs.

## Version Information

- **Version**: 1.0.0
- **Python Compatibility**: 3.8+
- **HUEY_P Protocol**: 1.0
- **Database Schema**: Compatible with existing HUEY_P database

For support and updates, refer to your HUEY_P system documentation.