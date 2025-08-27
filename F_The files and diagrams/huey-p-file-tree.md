# HUEY_P_ClaudeCentric System File Structure

```
HUEY_P_ClaudeCentric/
│
├── MT4/                                    # MetaTrader 4 Components
│   ├── Experts/                            # Expert Advisors (30 currency pairs)
│   │   ├── TRADING_MQL4_EURUSD_EA.mq4
│   │   ├── TRADING_MQL4_GBPUSD_EA.mq4
│   │   ├── TRADING_MQL4_USDJPY_EA.mq4
│   │   ├── TRADING_MQL4_USDCHF_EA.mq4
│   │   ├── TRADING_MQL4_USDCAD_EA.mq4
│   │   ├── TRADING_MQL4_AUDUSD_EA.mq4
│   │   ├── TRADING_MQL4_NZDUSD_EA.mq4
│   │   ├── TRADING_MQL4_EURGBP_EA.mq4
│   │   ├── TRADING_MQL4_EURJPY_EA.mq4
│   │   ├── TRADING_MQL4_EURCHF_EA.mq4
│   │   ├── TRADING_MQL4_EURAUD_EA.mq4
│   │   ├── TRADING_MQL4_EURCAD_EA.mq4
│   │   ├── TRADING_MQL4_GBPJPY_EA.mq4
│   │   ├── TRADING_MQL4_GBPCHF_EA.mq4
│   │   ├── TRADING_MQL4_GBPAUD_EA.mq4
│   │   ├── TRADING_MQL4_GBPCAD_EA.mq4
│   │   ├── TRADING_MQL4_AUDJPY_EA.mq4
│   │   ├── TRADING_MQL4_AUDCHF_EA.mq4
│   │   ├── TRADING_MQL4_AUDCAD_EA.mq4
│   │   ├── TRADING_MQL4_AUDNZD_EA.mq4
│   │   ├── TRADING_MQL4_CADJPY_EA.mq4
│   │   ├── TRADING_MQL4_CADCHF_EA.mq4
│   │   ├── TRADING_MQL4_CHFJPY_EA.mq4
│   │   ├── TRADING_MQL4_NZDJPY_EA.mq4
│   │   ├── TRADING_MQL4_NZDCHF_EA.mq4
│   │   ├── TRADING_MQL4_NZDCAD_EA.mq4
│   │   ├── TRADING_MQL4_XAUUSD_EA.mq4    # Gold
│   │   ├── TRADING_MQL4_XAGUSD_EA.mq4    # Silver
│   │   ├── TRADING_MQL4_[PAIR28]_EA.mq4
│   │   └── TRADING_MQL4_[PAIR30]_EA.mq4
│   │
│   ├── Include/                            # MQL4 Include Files
│   │   ├── TRADING_MQH_Core.mqh           # Core trading functions
│   │   ├── TRADING_MQH_Bridge.mqh         # Bridge communication
│   │   ├── TRADING_MQH_Reentry.mqh        # Reentry logic
│   │   └── TRADING_MQH_Utils.mqh          # Utility functions
│   │
│   ├── Libraries/                          # DLL Libraries
│   │   └── TRADING_DLL_SocketBridge.dll   # C++ Socket Bridge
│   │
│   └── Files/                              # CSV Configuration Files
│       ├── TRADING_CSV_parameter_sets.csv
│       ├── TRADING_CSV_signal_mapping.csv
│       ├── TRADING_CSV_reentry_mapping.csv
│       └── current_signal.csv              # Real-time signal file
│
├── Python/                                 # Python Backend
│   ├── src/
│   │   ├── services/                       # Core Services
│   │   │   ├── TRADING_PY_signal_service.py      # ML signal generation
│   │   │   ├── TRADING_PY_analytics_service.py   # Performance analytics
│   │   │   ├── TRADING_PY_risk_service.py        # Risk management
│   │   │   ├── TRADING_PY_monitoring_service.py  # System monitoring
│   │   │   └── TRADING_PY_bridge_service.py      # Bridge management
│   │   │
│   │   ├── models/                         # Data Models
│   │   │   ├── TRADING_PY_signal_models.py       # Signal entities
│   │   │   ├── TRADING_PY_trade_models.py        # Trade entities
│   │   │   ├── TRADING_PY_market_models.py       # Market data
│   │   │   └── TRADING_PY_ml_models.py           # ML model wrappers
│   │   │
│   │   ├── ml/                             # Machine Learning
│   │   │   ├── TRADING_PY_ensemble_model.py      # Ensemble predictor
│   │   │   ├── TRADING_PY_feature_engine.py      # Feature extraction
│   │   │   ├── TRADING_PY_model_trainer.py       # Model training
│   │   │   └── models/                            # Saved ML models
│   │   │       ├── signal_classifier.pkl
│   │   │       ├── confidence_regressor.pkl
│   │   │       └── risk_predictor.pkl
│   │   │
│   │   └── utils/                          # Utilities
│   │       ├── TRADING_PY_config_manager.py      # Configuration loader
│   │       ├── TRADING_PY_logger.py              # Logging utility
│   │       ├── TRADING_PY_metrics.py             # Performance metrics
│   │       └── TRADING_PY_database.py            # Database operations
│   │
│   ├── tests/                              # Test Suite
│   │   ├── unit/
│   │   │   ├── TRADING_PY_test_signals.py
│   │   │   ├── TRADING_PY_test_bridges.py
│   │   │   └── TRADING_PY_test_models.py
│   │   ├── integration/
│   │   │   ├── TRADING_PY_test_integration.py
│   │   │   └── TRADING_PY_test_e2e.py
│   │   └── fixtures/                       # Test data
│   │       └── test_market_data.csv
│   │
│   ├── requirements.txt                    # Python dependencies
│   ├── setup.py                           # Package setup
│   └── README.md                          # Python documentation
│
├── Config/                                 # Configuration Files
│   ├── TRADING_YAML_system_config.yaml    # Main system config
│   ├── TRADING_YAML_risk_config.yaml      # Risk parameters
│   ├── TRADING_YAML_ml_config.yaml        # ML model config
│   │
│   ├── pairs/                              # Per-pair configurations
│   │   ├── TRADING_YAML_EURUSD_config.yaml
│   │   ├── TRADING_YAML_GBPUSD_config.yaml
│   │   ├── TRADING_YAML_USDJPY_config.yaml
│   │   └── ... (27 more pair configs)
│   │
│   ├── environments/                       # Environment configs
│   │   ├── TRADING_YAML_development.yaml
│   │   ├── TRADING_YAML_testing.yaml
│   │   └── TRADING_YAML_production.yaml
│   │
│   └── production/                         # Production overrides
│       └── TRADING_YAML_production_config.yaml
│
├── Database/                               # Database Files
│   ├── TRADING_SQL_schema.sql             # Database schema
│   ├── TRADING_SQL_migrations.sql         # Schema migrations
│   ├── TRADING_SQL_seed_data.sql          # Initial data
│   ├── TRADING_DB_trading_system.db       # Main SQLite database
│   │
│   └── backups/                            # Database backups
│       ├── TRADING_DB_backup_daily.db
│       ├── TRADING_DB_backup_weekly.db
│       └── TRADING_DB_backup_[timestamp].db
│
├── Scripts/                                # Deployment & Management Scripts
│   ├── deployment/
│   │   ├── TRADING_PS1_deploy_all.ps1     # Master deployment
│   │   ├── TRADING_PS1_deploy_eas.ps1     # Deploy EAs
│   │   ├── TRADING_PS1_deploy_python.ps1  # Deploy Python
│   │   └── TRADING_PS1_rollback.ps1       # Rollback script
│   │
│   ├── maintenance/
│   │   ├── TRADING_PS1_monitor_system.ps1 # System monitoring
│   │   ├── TRADING_PS1_backup_database.ps1
│   │   ├── TRADING_PS1_clean_logs.ps1
│   │   └── TRADING_PS1_health_check.ps1
│   │
│   ├── startup/
│   │   ├── TRADING_BAT_start_services.bat # Windows startup
│   │   ├── TRADING_PS1_start_python.ps1
│   │   └── TRADING_PS1_start_mt4.ps1
│   │
│   └── utilities/
│       ├── TRADING_PS1_update_config.ps1
│       ├── TRADING_PS1_sync_pairs.ps1
│       └── TRADING_SH_linux_deploy.sh     # Linux deployment
│
├── Bridge/                                 # Communication Bridge
│   ├── src/
│   │   ├── TRADING_CPP_socket_bridge.cpp  # Socket implementation
│   │   ├── TRADING_CPP_named_pipes.cpp    # Named pipes
│   │   └── TRADING_CPP_file_bridge.cpp    # File-based fallback
│   │
│   ├── include/
│   │   ├── TRADING_H_bridge_interface.h
│   │   └── TRADING_H_message_protocol.h
│   │
│   └── build/
│       └── TRADING_DLL_SocketBridge.dll    # Compiled DLL
│
├── Logs/                                   # Log Files
│   ├── mt4/                                # MT4 logs
│   │   ├── experts/
│   │   └── journal/
│   │
│   ├── python/                             # Python service logs
│   │   ├── signal_service.log
│   │   ├── analytics_service.log
│   │   └── error.log
│   │
│   └── system/                             # System logs
│       ├── deployment.log
│       └── monitoring.log
│
├── Documentation/                          # System Documentation
│   ├── HUEY_P_ClaudeCentric system.md     # Main documentation
│   ├── TRADING_MD_api_reference.md        # API documentation
│   ├── TRADING_MD_deployment_guide.md     # Deployment guide
│   ├── TRADING_MD_troubleshooting.md      # Troubleshooting
│   │
│   └── diagrams/                           # Architecture diagrams
│       ├── system_architecture.png
│       ├── data_flow.png
│       └── deployment_flow.png
│
├── Tests/                                  # System-level Tests
│   ├── backtesting/
│   │   ├── TRADING_PY_backtest_runner.py
│   │   └── results/
│   │
│   └── performance/
│       ├── TRADING_PY_latency_test.py
│       └── TRADING_PY_load_test.py
│
├── Docker/                                 # Container Configuration
│   ├── Dockerfile.python                   # Python service container
│   ├── docker-compose.yml                  # Multi-container setup
│   └── .dockerignore
│
├── .env                                    # Environment variables
├── .gitignore                              # Git ignore file
├── LICENSE                                 # License file
└── README.md                               # Project README
```

## Key Directory Descriptions:

### MT4/
Contains all MetaTrader 4 components including 30 individual Expert Advisors (one per currency pair), shared include files for core functionality, the Socket Bridge DLL, and CSV configuration files.

### Python/
Houses the intelligent backend with ML-based signal generation, analytics services, risk management, and system monitoring. Includes comprehensive test suite and utilities.

### Config/
Stores all YAML configuration files organized by system components, currency pairs, and deployment environments.

### Database/
Contains SQLite database files, schema definitions, migrations, and automated backup structure.

### Scripts/
PowerShell and batch scripts for automated deployment, system monitoring, maintenance tasks, and health checks.

### Bridge/
C++ implementation of the three-tier communication bridge (Socket, Named Pipes, File-based) with compiled DLL.

### Documentation/
Comprehensive system documentation including technical specifications, API references, deployment guides, and architectural diagrams.