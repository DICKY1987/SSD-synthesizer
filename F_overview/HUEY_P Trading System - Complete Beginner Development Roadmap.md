# HUEY_P Trading System - Complete Beginner Development Roadmap

**Target Audience**: Complete Programming Beginner  
**Total Estimated Duration**: 8-12 months (300-400 hours)  
**Development Approach**: Single Developer, Step-by-Step Learning  
**Complexity Level**: Advanced System for Beginners  

---

## **REALITY CHECK & EXPECTATIONS**

⚠️ **Important**: This is an enterprise-level trading system. As a complete beginner, expect:
- **Timeline**: 8-12 months of dedicated learning and development
- **Daily Commitment**: 2-3 hours minimum
- **Complexity**: You'll be learning 4 programming languages simultaneously
- **Patience Required**: Many concepts will be confusing initially - this is normal

**Success Mindset**: Focus on one small step at a time. Each day you'll build something that works.

---

## **PHASE 0: COMPLETE ENVIRONMENT SETUP (Week 1-2)**
*Estimated Time: 15-20 hours*

### **Day 1-2: Windows Environment Setup (4-6 hours)**

#### **Step 1: Install Core Development Tools (2 hours)**

**1.1 Install Visual Studio Code**
```powershell
# Download from: https://code.visualstudio.com/
# Choose "Windows x64 User Installer"
# During installation, check ALL boxes for:
# - Add to PATH
# - Register Code as editor for supported files
# - Add "Open with Code" actions
```

**1.2 Install Git for Windows**
```powershell
# Download from: https://git-scm.com/download/win
# During installation:
# - Use Visual Studio Code as Git's default editor
# - Use Git from the Windows Command Prompt
# - Use the OpenSSL library
# - Checkout Windows-style, commit Unix-style line endings
```

**1.3 Install Python 3.11**
```powershell
# Download from: https://www.python.org/downloads/
# CRITICAL: Check "Add Python to PATH"
# Choose "Customize installation"
# Check ALL optional features
# Advanced Options: Check "Add Python to environment variables"
```

**Validation Test:**
```powershell
# Open PowerShell and run:
python --version
# Should show: Python 3.11.x

git --version
# Should show: git version 2.x.x

code --version
# Should show: Visual Studio Code version
```

#### **Step 2: Install MetaTrader 4 (1 hour)**

**2.1 Download and Install MT4**
```powershell
# Go to any forex broker website (e.g., OANDA, FXCM)
# Download their MT4 platform
# Install with default settings
# Create a DEMO account (never use real money during development)
```

**2.2 Configure MT4 for Development**
```
1. Open MT4
2. Tools → Options → Expert Advisors
3. Check ALL boxes:
   ✓ Allow automated trading
   ✓ Allow DLL imports
   ✓ Allow imports of external experts
   ✓ Enable WebRequest for listed URLs
```

**Validation Test:**
```
1. In MT4, press F4 (MetaEditor should open)
2. File → New → Expert Advisor
3. Name: "TestEA"
4. Click through with defaults
5. Should create a basic EA template
```

#### **Step 3: Install C++ Development Tools (1-2 hours)**

**3.1 Install Visual Studio Community**
```powershell
# Download from: https://visualstudio.microsoft.com/vs/community/
# During installation, select:
# Workloads → "Desktop development with C++"
# Individual components → "Windows 10/11 SDK (latest version)"
```

**Validation Test:**
```powershell
# Create a test C++ file to verify installation
# We'll test this in Step 4
```

### **Day 3: Project Structure Setup (2-3 hours)**

#### **Step 4: Create Project Directory Structure**

**4.1 Create Main Project Folder**
```powershell
# Open PowerShell
cd C:\
mkdir TradingSystem
cd TradingSystem

# Create all necessary folders
mkdir Source
mkdir Source\Python
mkdir Source\MQL4
mkdir Source\CPP
mkdir Source\PowerShell
mkdir Config
mkdir Database
mkdir Scripts
mkdir Tests
mkdir Documentation
```

**4.2 Initialize Git Repository**
```powershell
# In C:\TradingSystem
git init
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Create .gitignore file
code .gitignore
```

**Copy this into .gitignore:**
```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/

# Database
*.db
*.sqlite3

# MQL4
*.ex4
*.ex5

# C++
*.obj
*.exe
*.dll
Debug/
Release/
x64/

# IDE
.vscode/
*.suo
*.user

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Configuration (we'll add specific files later)
config/production/
```

**4.3 Set Up Visual Studio Code Workspace**
```powershell
# In C:\TradingSystem
code .
```

**Install Required VS Code Extensions:**
1. Press `Ctrl+Shift+X` (Extensions panel)
2. Search and install:
   - **Python** (by Microsoft)
   - **PowerShell** (by Microsoft)
   - **C/C++** (by Microsoft)
   - **YAML** (by Red Hat)
   - **SQLite Viewer** (by qwtel)

### **Day 4-5: Programming Environment Validation (3-4 hours)**

#### **Step 5: Test All Development Environments**

**5.1 Test Python Environment (1 hour)**

Create your first Python file:
```powershell
# In C:\TradingSystem\Source\Python
code hello_trading.py
```

**Type this code exactly:**
```python
# HUEY_P_PY_hello_trading.py
# Your first Python program for the trading system

import sys
import datetime

def main():
    print("=== HUEY_P Trading System ===")
    print(f"Python version: {sys.version}")
    print(f"Current time: {datetime.datetime.now()}")
    print("Python environment: WORKING ✓")

if __name__ == "__main__":
    main()
```

**Run and test:**
```powershell
cd C:\TradingSystem\Source\Python
python hello_trading.py
```

**Expected output:**
```
=== HUEY_P Trading System ===
Python version: 3.11.x (main, ...)
Current time: 2025-01-XX XX:XX:XX.XXXXXX
Python environment: WORKING ✓
```

**5.2 Test MQL4 Environment (1 hour)**

**Create your first MQL4 Expert Advisor:**
```
1. Open MT4 → Press F4 (MetaEditor)
2. File → New → Expert Advisor
3. Name: HUEY_P_MQL4_test_EA
4. Click Next → Next → Finish
```

**Replace all code with:**
```mql4
//+------------------------------------------------------------------+
//| HUEY_P_MQL4_test_EA.mq4                                          |
//| Your first MQL4 Expert Advisor                                   |
//+------------------------------------------------------------------+
#property copyright "Trading System Beginner"
#property link      ""
#property version   "1.00"
#property strict

//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
{
    Print("=== HUEY_P Trading System Test EA ===");
    Print("EA initialized successfully");
    Print("Account number: ", AccountNumber());
    Print("Account balance: ", AccountBalance());
    Print("MQL4 environment: WORKING ✓");
    
    return(INIT_SUCCEEDED);
}

//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
{
    Print("Test EA removed - goodbye!");
}

//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
{
    // This runs on every price tick
    // For now, we'll just count ticks
    static int tickCount = 0;
    tickCount++;
    
    if(tickCount % 100 == 0) // Every 100 ticks
    {
        Print("Tick count: ", tickCount, " | Current price: ", Bid);
    }
}
```

**Compile and test:**
```
1. Press F7 (Compile)
2. Should show "0 errors, 0 warnings"
3. Go back to MT4
4. Navigate → Experts
5. Drag "HUEY_P_MQL4_test_EA" onto any chart
6. Check "Allow live trading" → OK
7. Look for smiley face on chart
8. Check Experts tab for log messages
```

**5.3 Test C++ Environment (1-2 hours)**

**Create your first C++ DLL:**
```
1. Open Visual Studio
2. File → New → Project
3. Visual C++ → Windows Desktop → Dynamic-Link Library (DLL)
4. Name: HUEY_P_CPP_test_bridge
5. Location: C:\TradingSystem\Source\CPP
```

**Replace the generated code with this simple test:**

**testbridge.h:**
```cpp
// HUEY_P_CPP_test_bridge.h
#pragma once

#ifdef TESTBRIDGE_EXPORTS
#define TESTBRIDGE_API __declspec(dllexport)
#else
#define TESTBRIDGE_API __declspec(dllimport)
#endif

// Simple test function for MQL4
extern "C" {
    TESTBRIDGE_API int __stdcall TestConnection();
    TESTBRIDGE_API int __stdcall AddNumbers(int a, int b);
}
```

**testbridge.cpp:**
```cpp
// HUEY_P_CPP_test_bridge.cpp
#include "pch.h"
#include "testbridge.h"
#include <iostream>

// Test if DLL is working
extern "C" int __stdcall TestConnection()
{
    std::cout << "C++ Bridge: Connection test successful!" << std::endl;
    return 42; // Magic number to verify it's working
}

// Simple math function to test parameter passing
extern "C" int __stdcall AddNumbers(int a, int b)
{
    int result = a + b;
    std::cout << "C++ Bridge: " << a << " + " << b << " = " << result << std::endl;
    return result;
}
```

**Build the DLL:**
```
1. Build → Build Solution (Ctrl+Shift+B)
2. Should build without errors
3. Find the .dll file in Debug folder
4. Copy it to C:\TradingSystem\Source\CPP\
```

**5.4 Test PowerShell Environment (30 minutes)**

Create your first PowerShell script:
```powershell
# In C:\TradingSystem\Source\PowerShell
code HUEY_P_PS1_test_system.ps1
```

**Type this code:**
```powershell
# HUEY_P_PS1_test_system.ps1
# Your first PowerShell script for the trading system

Write-Host "=== HUEY_P Trading System PowerShell Test ===" -ForegroundColor Green

# Test basic PowerShell functionality
Write-Host "PowerShell version: $($PSVersionTable.PSVersion)" -ForegroundColor Cyan
Write-Host "Operating System: $($env:OS)" -ForegroundColor Cyan
Write-Host "Computer Name: $($env:COMPUTERNAME)" -ForegroundColor Cyan

# Test file system access
$projectRoot = "C:\TradingSystem"
if (Test-Path $projectRoot) {
    Write-Host "Project directory found: ✓" -ForegroundColor Green
    
    # List project structure
    Write-Host "`nProject Structure:" -ForegroundColor Yellow
    Get-ChildItem $projectRoot -Directory | ForEach-Object {
        Write-Host "  📁 $($_.Name)" -ForegroundColor White
    }
} else {
    Write-Host "Project directory NOT found: ✗" -ForegroundColor Red
}

Write-Host "`nPowerShell environment: WORKING ✓" -ForegroundColor Green
```

**Run the test:**
```powershell
cd C:\TradingSystem\Source\PowerShell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\HUEY_P_PS1_test_system.ps1
```

### **Day 6-7: Install Additional Tools (3-4 hours)**

#### **Step 6: Database and Containerization Tools**

**6.1 Install SQLite (1 hour)**
```powershell
# Download SQLite tools from: https://www.sqlite.org/download.html
# Download "Precompiled Binaries for Windows"
# Extract to C:\sqlite
# Add C:\sqlite to PATH environment variable
```

**6.2 Install Docker Desktop (1-2 hours)**
```powershell
# Download from: https://www.docker.com/products/docker-desktop/
# Install with default settings
# Restart computer when prompted
# Start Docker Desktop after restart
```

**6.3 Install Python Packages (1 hour)**
```powershell
cd C:\TradingSystem
python -m pip install --upgrade pip

# Install core packages we'll need
pip install pandas numpy scikit-learn pyyaml asyncio aiofiles websockets python-dotenv

# Create requirements.txt file
code requirements.txt
```

**Copy this into requirements.txt:**
```txt
# HUEY_P Trading System - Python Dependencies
pandas==2.1.3
numpy==1.25.2
scikit-learn==1.3.2
pyyaml==6.0.1
python-dotenv==1.0.0
asyncio==3.4.3
aiofiles==23.2.1
websockets==12.0
sqlite-utils==3.35.2
structlog==23.2.0
```

**Install all requirements:**
```powershell
pip install -r requirements.txt
```

---

## **PHASE 1: FOUNDATION PROGRAMMING (Week 3-8)**
*Estimated Time: 60-80 hours*

### **Week 3-4: Basic Python Programming (20-25 hours)**

#### **Day 15-17: Python Basics Through Trading Examples (6-8 hours)**

**Learning Objective**: Understand variables, functions, and basic data types through trading concepts.

**Step 7: Create Your First Trading Data Processor**

**7.1 Understanding Variables and Data Types (2 hours)**

Create: `C:\TradingSystem\Source\Python\HUEY_P_PY_basics_01.py`

```python
# HUEY_P_PY_basics_01.py
# Learning Python basics through trading concepts

# Variables for trading data
currency_pair = "EURUSD"  # String
bid_price = 1.0850       # Float (decimal number)
ask_price = 1.0852       # Float
spread_points = 2        # Integer (whole number)
is_market_open = True    # Boolean (True/False)

# Print our first trading data
print("=== Trading Data Basics ===")
print(f"Currency Pair: {currency_pair}")
print(f"Bid Price: {bid_price}")
print(f"Ask Price: {ask_price}")
print(f"Spread: {spread_points} points")
print(f"Market Open: {is_market_open}")

# Calculate spread in pips (points / 10)
spread_pips = spread_points / 10
print(f"Spread in pips: {spread_pips}")

# Different data types
print(f"\nData Types:")
print(f"currency_pair is a {type(currency_pair)}")
print(f"bid_price is a {type(bid_price)}")
print(f"spread_points is a {type(spread_points)}")
print(f"is_market_open is a {type(is_market_open)}")
```

**Run and understand:**
```powershell
cd C:\TradingSystem\Source\Python
python HUEY_P_PY_basics_01.py
```

**Expected Output:**
```
=== Trading Data Basics ===
Currency Pair: EURUSD
Bid Price: 1.085
Ask Price: 1.0852
Spread: 2 points
Market Open: True
Spread in pips: 0.2

Data Types:
currency_pair is a <class 'str'>
bid_price is a <class 'float'>
spread_points is a <class 'int'>
is_market_open is a <class 'bool'>
```

**7.2 Working with Lists and Trading Data (2 hours)**

Create: `C:\TradingSystem\Source\Python\HUEY_P_PY_basics_02.py`

```python
# HUEY_P_PY_basics_02.py
# Working with lists of trading data

# List of currency pairs (our 30 pairs from the spec)
major_pairs = ["EURUSD", "GBPUSD", "USDJPY", "USDCHF", "AUDUSD", "USDCAD", "NZDUSD"]
cross_pairs = ["EURGBP", "EURJPY", "EURCHF", "GBPJPY", "GBPCHF", "CHFJPY"]
metal_pairs = ["XAUUSD", "XAGUSD"]

# All pairs combined
all_pairs = major_pairs + cross_pairs + metal_pairs

print("=== Trading Pairs Lists ===")
print(f"Major pairs ({len(major_pairs)}): {major_pairs}")
print(f"Cross pairs ({len(cross_pairs)}): {cross_pairs}")
print(f"Metal pairs ({len(metal_pairs)}): {metal_pairs}")
print(f"Total pairs: {len(all_pairs)}")

# Working with individual items
print(f"\nFirst major pair: {major_pairs[0]}")
print(f"Last metal pair: {metal_pairs[-1]}")

# Loop through all pairs (your first loop!)
print(f"\nAll {len(all_pairs)} trading pairs:")
for i, pair in enumerate(all_pairs):
    print(f"{i+1:2}. {pair}")

# List of prices (simulated market data)
eurusd_prices = [1.0850, 1.0851, 1.0849, 1.0852, 1.0848]
print(f"\nEURUSD last 5 prices: {eurusd_prices}")

# Calculate some basic statistics
highest_price = max(eurusd_prices)
lowest_price = min(eurusd_prices)
average_price = sum(eurusd_prices) / len(eurusd_prices)

print(f"Highest: {highest_price}")
print(f"Lowest: {lowest_price}")
print(f"Average: {average_price:.5f}")
```

**Test Your Understanding:**
```powershell
python HUEY_P_PY_basics_02.py
```

**7.3 Functions for Trading Calculations (2-3 hours)**

Create: `C:\TradingSystem\Source\Python\HUEY_P_PY_basics_03.py`

```python
# HUEY_P_PY_basics_03.py
# Creating functions for trading calculations

def calculate_spread(bid_price, ask_price):
    """
    Calculate spread in points
    Args:
        bid_price (float): Current bid price
        ask_price (float): Current ask price
    Returns:
        int: Spread in points
    """
    spread = ask_price - bid_price
    points = round(spread * 10000)  # Convert to points
    return points

def calculate_lot_size(account_balance, risk_percent, stop_loss_pips):
    """
    Calculate position size based on risk management
    Args:
        account_balance (float): Account balance in USD
        risk_percent (float): Risk percentage (e.g., 0.02 for 2%)
        stop_loss_pips (int): Stop loss in pips
    Returns:
        float: Lot size
    """
    risk_amount = account_balance * risk_percent
    pip_value = 10  # For EURUSD, 1 pip = $10 per standard lot
    max_loss = stop_loss_pips * pip_value
    
    if max_loss <= 0:
        return 0.01  # Minimum lot size
    
    lot_size = risk_amount / max_loss
    # Round to 2 decimal places and ensure minimum
    lot_size = max(0.01, round(lot_size, 2))
    return lot_size

def is_spread_acceptable(current_spread, max_spread):
    """
    Check if current spread is acceptable for trading
    Args:
        current_spread (int): Current spread in points
        max_spread (int): Maximum acceptable spread
    Returns:
        bool: True if spread is acceptable
    """
    return current_spread <= max_spread

# Test our functions
print("=== Trading Function Tests ===")

# Test spread calculation
bid = 1.0850
ask = 1.0852
spread = calculate_spread(bid, ask)
print(f"Bid: {bid}, Ask: {ask}")
print(f"Spread: {spread} points")

# Test lot size calculation
balance = 10000.0  # $10,000 account
risk = 0.02        # 2% risk per trade
stop_loss = 50     # 50 pip stop loss

lot_size = calculate_lot_size(balance, risk, stop_loss)
print(f"\nAccount: ${balance}")
print(f"Risk: {risk*100}%")
print(f"Stop Loss: {stop_loss} pips")
print(f"Calculated Lot Size: {lot_size}")

# Test spread acceptance
max_allowed_spread = 3
acceptable = is_spread_acceptable(spread, max_allowed_spread)
print(f"\nCurrent spread: {spread} points")
print(f"Max allowed: {max_allowed_spread} points")
print(f"Acceptable: {acceptable}")

# Test with multiple scenarios
print(f"\n=== Multiple Scenarios ===")
test_spreads = [1, 2, 3, 4, 5]
for test_spread in test_spreads:
    acceptable = is_spread_acceptable(test_spread, max_allowed_spread)
    status = "✓ TRADE" if acceptable else "✗ SKIP"
    print(f"Spread {test_spread} points: {status}")
```

**Advanced Testing:**
```powershell
python HUEY_P_PY_basics_03.py
```

#### **Day 18-21: File Handling and Configuration (8-10 hours)**

**Step 8: Working with Trading Configuration Files**

**8.1 Reading CSV Files (3 hours)**

Create: `C:\TradingSystem\Source\Python\HUEY_P_PY_csv_01.py`

```python
# HUEY_P_PY_csv_01.py
# Working with CSV files for trading configuration

import csv
import os

# First, let's create a sample parameter sets CSV file
def create_sample_parameter_file():
    """Create a sample parameter sets file"""
    parameters = [
        ["id", "stopLoss", "takeProfit", "trailingStop", "riskPercent", "maxPositions", "useTrailing", "description"],
        ["conservative", "200", "400", "50", "1.0", "1", "true", "Low risk strategy"],
        ["moderate", "150", "300", "40", "1.5", "2", "true", "Medium risk strategy"],
        ["aggressive", "100", "200", "30", "2.0", "3", "true", "High risk strategy"],
        ["scalping", "50", "100", "20", "0.5", "5", "false", "Quick trades"],
        ["swing", "300", "600", "100", "2.5", "1", "true", "Long term trades"]
    ]
    
    # Make sure directory exists
    config_dir = "C:\\TradingSystem\\Config"
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    
    filename = os.path.join(config_dir, "HUEY_P_CSV_parameter_sets.csv")
    
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(parameters)
    
    print(f"Created sample parameter file: {filename}")
    return filename

def read_parameter_sets(filename):
    """Read parameter sets from CSV file"""
    parameter_sets = {}
    
    try:
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                param_id = row['id']
                parameter_sets[param_id] = {
                    'stopLoss': int(row['stopLoss']),
                    'takeProfit': int(row['takeProfit']),
                    'trailingStop': int(row['trailingStop']),
                    'riskPercent': float(row['riskPercent']),
                    'maxPositions': int(row['maxPositions']),
                    'useTrailing': row['useTrailing'].lower() == 'true',
                    'description': row['description']
                }
                
        print(f"Successfully loaded {len(parameter_sets)} parameter sets")
        return parameter_sets
        
    except FileNotFoundError:
        print(f"Error: File {filename} not found!")
        return {}
    except Exception as e:
        print(f"Error reading file: {e}")
        return {}

def display_parameter_set(param_id, parameters):
    """Display a specific parameter set"""
    if param_id in parameters:
        param = parameters[param_id]
        print(f"\n=== {param_id.upper()} Strategy ===")
        print(f"Description: {param['description']}")
        print(f"Stop Loss: {param['stopLoss']} points")
        print(f"Take Profit: {param['takeProfit']} points")
        print(f"Trailing Stop: {param['trailingStop']} points")
        print(f"Risk Per Trade: {param['riskPercent']}%")
        print(f"Max Positions: {param['maxPositions']}")
        print(f"Use Trailing: {param['useTrailing']}")
    else:
        print(f"Parameter set '{param_id}' not found!")

# Main execution
print("=== Trading Parameter Sets Manager ===")

# Create sample file
csv_file = create_sample_parameter_file()

# Read the parameter sets
parameters = read_parameter_sets(csv_file)

# Display all available parameter sets
print(f"\nAvailable parameter sets:")
for param_id in parameters.keys():
    print(f"  - {param_id}")

# Display specific parameter sets
for param_id in ["conservative", "aggressive"]:
    display_parameter_set(param_id, parameters)

# Test parameter selection
print(f"\n=== Parameter Selection Test ===")
selected_strategy = "moderate"
if selected_strategy in parameters:
    selected_params = parameters[selected_strategy]
    print(f"Selected: {selected_strategy}")
    print(f"Will risk {selected_params['riskPercent']}% per trade")
    print(f"Stop loss: {selected_params['stopLoss']} points")
else:
    print(f"Strategy '{selected_strategy}' not available!")
```

**Test the CSV functionality:**
```powershell
python HUEY_P_PY_csv_01.py
```

**8.2 Working with YAML Configuration (3-4 hours)**

Create: `C:\TradingSystem\Source\Python\HUEY_P_PY_yaml_01.py`

```python
# HUEY_P_PY_yaml_01.py
# Working with YAML configuration files

import yaml
import os

def create_sample_system_config():
    """Create a sample system configuration YAML file"""
    
    config = {
        'system': {
            'name': 'HUEY_P_ClaudeCentric_Trading_System',
            'version': '1.0.0',
            'environment': 'development'
        },
        'bridge': {
            'host': '127.0.0.1',
            'primary_port': 8888,
            'secondary_port': 8889,
            'heartbeat_interval': 30,
            'timeout_seconds': 10
        },
        'database': {
            'path': 'C:\\TradingSystem\\Database\\trading_system.db',
            'backup_interval_hours': 6,
            'max_backups': 48
        },
        'risk_management': {
            'max_account_drawdown': 0.10,
            'max_concurrent_trades': 30,
            'default_risk_percent': 0.015,
            'max_spread_points': {
                'EURUSD': 3,
                'GBPUSD': 4,
                'USDJPY': 3,
                'default': 5
            }
        },
        'logging': {
            'level': 'DEBUG',
            'file_path': 'C:\\TradingSystem\\Logs\\trading.log',
            'max_file_size_mb': 100,
            'backup_count': 10
        }
    }
    
    config_dir = "C:\\TradingSystem\\Config"
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    
    filename = os.path.join(config_dir, "HUEY_P_YAML_system_config.yaml")
    
    with open(filename, 'w') as file:
        yaml.dump(config, file, default_flow_style=False, indent=2)
    
    print(f"Created system configuration: {filename}")
    return filename

def load_configuration(filename):
    """Load configuration from YAML file"""
    try:
        with open(filename, 'r') as file:
            config = yaml.safe_load(file)
        print(f"Configuration loaded successfully from {filename}")
        return config
    except FileNotFoundError:
        print(f"Error: Configuration file {filename} not found!")
        return None
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        return None

def get_config_value(config, key_path):
    """
    Get a configuration value using dot notation
    Example: get_config_value(config, 'bridge.primary_port')
    """
    keys = key_path.split('.')
    value = config
    
    try:
        for key in keys:
            value = value[key]
        return value
    except (KeyError, TypeError):
        print(f"Configuration key '{key_path}' not found!")
        return None

def display_configuration(config):
    """Display the loaded configuration in a readable format"""
    print("\n=== System Configuration ===")
    
    # System info
    system = config.get('system', {})
    print(f"System: {system.get('name', 'Unknown')}")
    print(f"Version: {system.get('version', 'Unknown')}")
    print(f"Environment: {system.get('environment', 'Unknown')}")
    
    # Bridge settings
    bridge = config.get('bridge', {})
    print(f"\nBridge Configuration:")
    print(f"  Host: {bridge.get('host', 'Unknown')}")
    print(f"  Primary Port: {bridge.get('primary_port', 'Unknown')}")
    print(f"  Heartbeat: every {bridge.get('heartbeat_interval', 'Unknown')} seconds")
    
    # Risk management
    risk = config.get('risk_management', {})
    print(f"\nRisk Management:")
    print(f"  Max Drawdown: {risk.get('max_account_drawdown', 'Unknown') * 100}%")
    print(f"  Max Trades: {risk.get('max_concurrent_trades', 'Unknown')}")
    print(f"  Default Risk: {risk.get('default_risk_percent', 'Unknown') * 100}%")
    
    # Spread limits
    spreads = risk.get('max_spread_points', {})
    print(f"  Spread Limits:")
    for pair, limit in spreads.items():
        if pair != 'default':
            print(f"    {pair}: {limit} points")
    print(f"    Others: {spreads.get('default', 'Unknown')} points")

# Main execution
print("=== YAML Configuration Manager ===")

# Create sample configuration
config_file = create_sample_system_config()

# Load the configuration
config = load_configuration(config_file)

if config:
    # Display the configuration
    display_configuration(config)
    
    # Test accessing specific values
    print(f"\n=== Configuration Value Tests ===")
    
    test_keys = [
        'bridge.primary_port',
        'risk_management.default_risk_percent',
        'risk_management.max_spread_points.EURUSD',
        'logging.level'
    ]
    
    for key in test_keys:
        value = get_config_value(config, key)
        print(f"{key}: {value}")
    
    # Test configuration for different environments
    print(f"\n=== Environment-Specific Settings ===")
    current_env = get_config_value(config, 'system.environment')
    print(f"Current environment: {current_env}")
    
    if current_env == 'development':
        print("Development mode settings:")
        print("  - Verbose logging enabled")
        print("  - Demo account only")
        print("  - Lower risk limits")
    elif current_env == 'production':
        print("Production mode settings:")
        print("  - Normal logging")
        print("  - Live account")
        print("  - Full risk limits")
```

**Test YAML functionality:**
```powershell
python HUEY_P_PY_yaml_01.py
```

### **Week 5-6: Basic MQL4 Programming (20-25 hours)**

#### **Day 22-25: MQL4 Fundamentals (8-10 hours)**

**Learning Objective**: Understand MQL4 syntax and create basic Expert Advisors.

**Step 9: Your First Trading Expert Advisor**

**9.1 Understanding MQL4 Structure (3 hours)**

```
1. Open MT4 → Press F4 (MetaEditor)
2. File → New → Expert Advisor
3. Name: HUEY_P_MQL4_learning_01
4. Delete all default code and type this:
```

```mql4
//+------------------------------------------------------------------+
//| HUEY_P_MQL4_learning_01.mq4                                     |
//| Learning MQL4 basics step by step                               |
//+------------------------------------------------------------------+
#property copyright "Trading System Beginner"
#property version   "1.00"
#property strict

// Input parameters that appear in EA settings dialog
input int    MagicNumber = 12345;          // Unique identifier for our trades
input double LotSize = 0.01;               // Trade size (0.01 = micro lot)
input int    StopLoss = 50;                // Stop loss in points
input int    TakeProfit = 100;             // Take profit in points
input string TradingComment = "Learning";   // Comment for trades

// Global variables
int g_tickCount = 0;        // Count how many ticks we've processed
bool g_tradeOpened = false; // Track if we have an open trade

//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//| This runs once when EA is attached to chart                     |
//+------------------------------------------------------------------+
int OnInit()
{
    // Print welcome message
    Print("=== HUEY_P Learning EA Started ===");
    Print("Magic Number: ", MagicNumber);
    Print("Lot Size: ", LotSize);
    Print("Stop Loss: ", StopLoss, " points");
    Print("Take Profit: ", TakeProfit, " points");
    
    // Check if trading is allowed
    if(!IsTradeAllowed())
    {
        Print("ERROR: Trading is not allowed! Check your settings.");
        return INIT_FAILED;
    }
    
    // Check account type
    if(IsDemo())
    {
        Print("Demo account detected - safe for learning ✓");
    }
    else
    {
        Print("WARNING: Live account detected!");
        Print("Learning EA should only run on demo accounts!");
        return INIT_FAILED;
    }
    
    Print("EA initialization completed successfully");
    return INIT_SUCCEEDED;
}

//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//| This runs when EA is removed from chart                         |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
{
    Print("=== HUEY_P Learning EA Stopped ===");
    Print("Total ticks processed: ", g_tickCount);
    Print("Goodbye!");
}

//+------------------------------------------------------------------+
//| Expert tick function                                             |
//| This runs on every price change (tick)                          |
//+------------------------------------------------------------------+
void OnTick()
{
    // Count this tick
    g_tickCount++;
    
    // Print market information every 50 ticks
    if(g_tickCount % 50 == 0)
    {
        PrintMarketInfo();
    }
    
    // Check if we can trade
    if(!IsTradeAllowed())
    {
        return; // Exit if trading not allowed
    }
    
    // Simple trading logic: Buy if we don't have a trade
    if(!g_tradeOpened && !HasOpenTrades())
    {
        // Only buy during certain hours (avoid major news times)
        int currentHour = Hour();
        if(currentHour >= 8 && currentHour <= 17) // 8 AM to 5 PM server time
        {
            OpenBuyTrade();
        }
    }
    
    // Update our trade tracking
    g_tradeOpened = HasOpenTrades();
}

//+------------------------------------------------------------------+
//| Print current market information                                 |
//+------------------------------------------------------------------+
void PrintMarketInfo()
{
    Print("=== Market Info (Tick #", g_tickCount, ") ===");
    Print("Symbol: ", Symbol());
    Print("Bid: ", DoubleToString(Bid, Digits));
    Print("Ask: ", DoubleToString(Ask, Digits));
    Print("Spread: ", MarketInfo(Symbol(), MODE_SPREAD), " points");
    Print("Time: ", TimeToString(TimeCurrent()));
    Print("Open trades: ", CountOpenTrades());
}

//+------------------------------------------------------------------+
//| Check if we have any open trades                                 |
//+------------------------------------------------------------------+
bool HasOpenTrades()
{
    return CountOpenTrades() > 0;
}

//+------------------------------------------------------------------+
//| Count how many trades are open with our magic number            |
//+------------------------------------------------------------------+
int CountOpenTrades()
{
    int count = 0;
    
    for(int i = 0; i < OrdersTotal(); i++)
    {
        if(OrderSelect(i, SELECT_BY_POS, MODE_TRADES))
        {
            if(OrderSymbol() == Symbol() && OrderMagicNumber() == MagicNumber)
            {
                count++;
            }
        }
    }
    
    return count;
}

//+------------------------------------------------------------------+
//| Open a buy trade                                                 |
//+------------------------------------------------------------------+
void OpenBuyTrade()
{
    double price = Ask;
    double sl = 0; // Stop loss price
    double tp = 0; // Take profit price
    
    // Calculate stop loss and take profit prices
    if(StopLoss > 0)
    {
        sl = price - (StopLoss * Point);
    }
    
    if(TakeProfit > 0)
    {
        tp = price + (TakeProfit * Point);
    }
    
    Print("=== Attempting to open BUY trade ===");
    Print("Price: ", DoubleToString(price, Digits));
    Print("Stop Loss: ", DoubleToString(sl, Digits));
    Print("Take Profit: ", DoubleToString(tp, Digits));
    
    // Place the order
    int ticket = OrderSend(
        Symbol(),           // Currency pair
        OP_BUY,            // Order type (Buy)
        LotSize,           // Lot size
        price,             // Price
        3,                 // Slippage (3 points)
        sl,                // Stop loss
        tp,                // Take profit
        TradingComment,    // Comment
        MagicNumber,       // Magic number
        0,                 // Expiration (0 = no expiration)
        clrGreen           // Arrow color
    );
    
    if(ticket > 0)
    {
        Print("SUCCESS: Buy order opened with ticket #", ticket);
        g_tradeOpened = true;
    }
    else
    {
        int error = GetLastError();
        Print("ERROR: Failed to open buy order. Error code: ", error);
        Print("Error description: ", ErrorDescription(error));
    }
}
```

**Compile and test:**
```
1. Press F7 (Compile)
2. Should show "0 errors, 0 warnings"
3. Go to MT4 main window
4. Drag EA onto EURUSD chart
5. In settings dialog:
   - Check "Allow live trading"
   - Set LotSize to 0.01
   - Click OK
6. Watch the Experts tab for log messages
```

**9.2 Understanding Market Data and Orders (3-4 hours)**

Create a more advanced EA:

```
File → New → Expert Advisor
Name: HUEY_P_MQL4_learning_02
```

```mql4
//+------------------------------------------------------------------+
//| HUEY_P_MQL4_learning_02.mq4                                     |
//| Understanding market data and order management                   |
//+------------------------------------------------------------------+
#property copyright "Trading System Beginner"
#property version   "1.00"
#property strict

// Input parameters
input double LotSize = 0.01;
input int    StopLoss = 50;
input int    TakeProfit = 100;
input int    MaxSpread = 5;
input int    MagicNumber = 12346;

// Global variables for market analysis
double g_previousBid = 0;
double g_previousAsk = 0;
int g_priceDirection = 0; // 1 = up, -1 = down, 0 = unchanged

//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
{
    Print("=== Advanced Learning EA Started ===");
    
    // Store initial prices
    g_previousBid = Bid;
    g_previousAsk = Ask;
    
    // Display account information
    PrintAccountInfo();
    
    return INIT_SUCCEEDED;
}

//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
{
    // Analyze price movement
    AnalyzePriceMovement();
    
    // Check trading conditions
    if(ShouldTrade())
    {
        // Simple strategy: follow the trend
        if(g_priceDirection == 1) // Price going up
        {
            if(!HasOpenBuyTrades())
            {
                OpenTrade(OP_BUY);
            }
        }
        else if(g_priceDirection == -1) // Price going down
        {
            if(!HasOpenSellTrades())
            {
                OpenTrade(OP_SELL);
            }
        }
    }
    
    // Manage existing trades
    ManageOpenTrades();
    
    // Update previous prices for next tick
    g_previousBid = Bid;
    g_previousAsk = Ask;
}

//+------------------------------------------------------------------+
//| Analyze price movement direction                                  |
//+------------------------------------------------------------------+
void AnalyzePriceMovement()
{
    double currentBid = Bid;
    double priceDifference = currentBid - g_previousBid;
    
    if(priceDifference > 0.00001) // Price went up (accounting for floating point precision)
    {
        g_priceDirection = 1;
    }
    else if(priceDifference < -0.00001) // Price went down
    {
        g_priceDirection = -1;
    }
    else
    {
        g_priceDirection = 0; // No significant change
    }
}

//+------------------------------------------------------------------+
//| Check if we should trade now                                     |
//+------------------------------------------------------------------+
bool ShouldTrade()
{
    // Check if trading is allowed
    if(!IsTradeAllowed())
    {
        return false;
    }
    
    // Check spread
    double currentSpread = MarketInfo(Symbol(), MODE_SPREAD);
    if(currentSpread > MaxSpread)
    {
        static datetime lastSpreadWarning = 0;
        if(TimeCurrent() - lastSpreadWarning > 60) // Warn only once per minute
        {
            Print("Spread too high: ", currentSpread, " points (max: ", MaxSpread, ")");
            lastSpreadWarning = TimeCurrent();
        }
        return false;
    }
    
    // Check if we already have too many trades
    if(CountAllOpenTrades() >= 1) // Limit to 1 trade for learning
    {
        return false;
    }
    
    // Don't trade during weekends or low-liquidity hours
    int dayOfWeek = DayOfWeek();
    int currentHour = Hour();
    
    if(dayOfWeek == 0 || dayOfWeek == 6) // Sunday or Saturday
    {
        return false;
    }
    
    if(currentHour < 6 || currentHour > 20) // Avoid low-liquidity hours
    {
        return false;
    }
    
    return true;
}

//+------------------------------------------------------------------+
//| Open a trade (buy or sell)                                       |
//+------------------------------------------------------------------+
void OpenTrade(int orderType)
{
    double price, sl, tp;
    color arrowColor;
    string orderTypeText;
    
    // Set price and calculate stops based on order type
    if(orderType == OP_BUY)
    {
        price = Ask;
        sl = (StopLoss > 0) ? price - (StopLoss * Point) : 0;
        tp = (TakeProfit > 0) ? price + (TakeProfit * Point) : 0;
        arrowColor = clrGreen;
        orderTypeText = "BUY";
    }
    else if(orderType == OP_SELL)
    {
        price = Bid;
        sl = (StopLoss > 0) ? price + (StopLoss * Point) : 0;
        tp = (TakeProfit > 0) ? price - (TakeProfit * Point) : 0;
        arrowColor = clrRed;
        orderTypeText = "SELL";
    }
    else
    {
        Print("ERROR: Invalid order type: ", orderType);
        return;
    }
    
    Print("=== Opening ", orderTypeText, " Trade ===");
    Print("Entry Price: ", DoubleToString(price, Digits));
    Print("Stop Loss: ", DoubleToString(sl, Digits));
    Print("Take Profit: ", DoubleToString(tp, Digits));
    Print("Lot Size: ", LotSize);
    
    int ticket = OrderSend(
        Symbol(),
        orderType,
        LotSize,
        price,
        3, // 3 points slippage
        sl,
        tp,
        "Learning EA v2",
        MagicNumber,
        0,
        arrowColor
    );
    
    if(ticket > 0)
    {
        Print("SUCCESS: ", orderTypeText, " order opened with ticket #", ticket);
    }
    else
    {
        int error = GetLastError();
        Print("ERROR: Failed to open ", orderTypeText, " order. Error: ", error, " - ", ErrorDescription(error));
    }
}

//+------------------------------------------------------------------+
//| Manage existing open trades                                      |
//+------------------------------------------------------------------+
void ManageOpenTrades()
{
    for(int i = OrdersTotal() - 1; i >= 0; i--)
    {
        if(OrderSelect(i, SELECT_BY_POS, MODE_TRADES))
        {
            if(OrderSymbol() == Symbol() && OrderMagicNumber() == MagicNumber)
            {
                // Simple trailing stop logic
                if(OrderType() == OP_BUY)
                {
                    double newSL = Bid - (StopLoss * Point);
                    if(newSL > OrderStopLoss() + (10 * Point)) // Only move if significant improvement
                    {
                        ModifyTrailingStop(OrderTicket(), newSL);
                    }
                }
                else if(OrderType() == OP_SELL)
                {
                    double newSL = Ask + (StopLoss * Point);
                    if(newSL < OrderStopLoss() - (10 * Point)) // Only move if significant improvement
                    {
                        ModifyTrailingStop(OrderTicket(), newSL);
                    }
                }
            }
        }
    }
}

//+------------------------------------------------------------------+
//| Modify trailing stop                                             |
//+------------------------------------------------------------------+
void ModifyTrailingStop(int ticket, double newStopLoss)
{
    bool result = OrderModify(
        ticket,
        OrderOpenPrice(),
        newStopLoss,
        OrderTakeProfit(),
        0,
        clrBlue
    );
    
    if(result)
    {
        Print("Trailing stop updated for ticket #", ticket, " to ", DoubleToString(newStopLoss, Digits));
    }
    else
    {
        int error = GetLastError();
        if(error != 1) // Ignore "no error" 
        {
            Print("Failed to modify trailing stop. Error: ", error);
        }
    }
}

//+------------------------------------------------------------------+
//| Check if we have open buy trades                                 |
//+------------------------------------------------------------------+
bool HasOpenBuyTrades()
{
    for(int i = 0; i < OrdersTotal(); i++)
    {
        if(OrderSelect(i, SELECT_BY_POS, MODE_TRADES))
        {
            if(OrderSymbol() == Symbol() && OrderMagicNumber() == MagicNumber && OrderType() == OP_BUY)
            {
                return true;
            }
        }
    }
    return false;
}

//+------------------------------------------------------------------+
//| Check if we have open sell trades                                |
//+------------------------------------------------------------------+
bool HasOpenSellTrades()
{
    for(int i = 0; i < OrdersTotal(); i++)
    {
        if(OrderSelect(i, SELECT_BY_POS, MODE_TRADES))
        {
            if(OrderSymbol() == Symbol() && OrderMagicNumber() == MagicNumber && OrderType() == OP_SELL)
            {
                return true;
            }
        }
    }
    return false;
}

//+------------------------------------------------------------------+
//| Count all open trades with our magic number                      |
//+------------------------------------------------------------------+
int CountAllOpenTrades()
{
    int count = 0;
    for(int i = 0; i < OrdersTotal(); i++)
    {
        if(OrderSelect(i, SELECT_BY_POS, MODE_TRADES))
        {
            if(OrderSymbol() == Symbol() && OrderMagicNumber() == MagicNumber)
            {
                count++;
            }
        }
    }
    return count;
}

//+------------------------------------------------------------------+
//| Print account information                                         |
//+------------------------------------------------------------------+
void PrintAccountInfo()
{
    Print("=== Account Information ===");
    Print("Account Number: ", AccountNumber());
    Print("Account Name: ", AccountName());
    Print("Account Company: ", AccountCompany());
    Print("Account Balance: $", DoubleToString(AccountBalance(), 2));
    Print("Account Equity: $", DoubleToString(AccountEquity(), 2));
    Print("Account Leverage: 1:", AccountLeverage());
    Print("Account Currency: ", AccountCurrency());
    Print("Demo Account: ", (IsDemo() ? "Yes" : "No"));
    Print("===========================");
}
```

#### **Day 26-28: File Operations in MQL4 (6-8 hours)**

**Step 10: Reading Configuration Files in MQL4**

**10.1 Create CSV Configuration Reader (4 hours)**

```
File → New → Include File (.mqh)
Name: HUEY_P_MQH_config_reader
```

```mql4
//+------------------------------------------------------------------+
//| HUEY_P_MQH_config_reader.mqh                                    |
//| Functions for reading CSV configuration files                    |
//+------------------------------------------------------------------+
#property copyright "Trading System Beginner"
#property strict

//+------------------------------------------------------------------+
//| Structure to hold parameter set data                             |
//+------------------------------------------------------------------+
struct ParameterSet
{
    string id;
    int stopLoss;
    int takeProfit;
    int trailingStop;
    double riskPercent;
    int maxPositions;
    bool useTrailing;
    string description;
};

//+------------------------------------------------------------------+
//| Read parameter sets from CSV file                                |
//+------------------------------------------------------------------+
bool ReadParameterSets(string filename, ParameterSet &paramSets[], int &count)
{
    // Initialize
    count = 0;
    
    // Try to open file
    int fileHandle = FileOpen(filename, FILE_READ | FILE_CSV | FILE_COMMON);
    
    if(fileHandle == INVALID_HANDLE)
    {
        Print("ERROR: Cannot open parameter file: ", filename);
        Print("Make sure file exists in MQL4/Files/Common/ folder");
        return false;
    }
    
    Print("Reading parameter sets from: ", filename);
    
    // Read header line (skip it)
    if(!FileIsEnding(fileHandle))
    {
        string header = FileReadString(fileHandle);
        Print("Header: ", header);
    }
    
    // Read data lines
    while(!FileIsEnding(fileHandle) && count < 50) // Max 50 parameter sets
    {
        if(FileIsLineEnding(fileHandle))
        {
            continue;
        }
        
        // Read each field
        string id = FileReadString(fileHandle);
        if(StringLen(id) == 0) break; // Empty line, stop reading
        
        string stopLossStr = FileReadString(fileHandle);
        string takeProfitStr = FileReadString(fileHandle);
        string trailingStopStr = FileReadString(fileHandle);
        string riskPercentStr = FileReadString(fileHandle);
        string maxPositionsStr = FileReadString(fileHandle);
        string useTrailingStr = FileReadString(fileHandle);
        string description = FileReadString(fileHandle);
        
        // Convert strings to appropriate types
        paramSets[count].id = id;
        paramSets[count].stopLoss = (int)StringToInteger(stopLossStr);
        paramSets[count].takeProfit = (int)StringToInteger(takeProfitStr);
        paramSets[count].trailingStop = (int)StringToInteger(trailingStopStr);
        paramSets[count].riskPercent = StringToDouble(riskPercentStr);
        paramSets[count].maxPositions = (int)StringToInteger(maxPositionsStr);
        paramSets[count].useTrailing = (StringToLower(useTrailingStr) == "true");
        paramSets[count].description = description;
        
        Print("Loaded parameter set [", count, "]: ", id);
        count++;
    }
    
    FileClose(fileHandle);
    Print("Successfully loaded ", count, " parameter sets");
    return true;
}

//+------------------------------------------------------------------+
//| Find parameter set by ID                                         |
//+------------------------------------------------------------------+
bool FindParameterSet(string searchId, ParameterSet &paramSets[], int count, ParameterSet &result)
{
    for(int i = 0; i < count; i++)
    {
        if(StringCompare(paramSets[i].id, searchId, false) == 0) // Case insensitive
        {
            result = paramSets[i];
            return true;
        }
    }
    
    Print("Parameter set '", searchId, "' not found!");
    return false;
}

//+------------------------------------------------------------------+
//| Print parameter set details                                      |
//+------------------------------------------------------------------+
void PrintParameterSet(ParameterSet &params)
{
    Print("=== Parameter Set: ", params.id, " ===");
    Print("Description: ", params.description);
    Print("Stop Loss: ", params.stopLoss, " points");
    Print("Take Profit: ", params.takeProfit, " points");
    Print("Trailing Stop: ", params.trailingStop, " points");
    Print("Risk Percent: ", DoubleToString(params.riskPercent, 2), "%");
    Print("Max Positions: ", params.maxPositions);
    Print("Use Trailing: ", (params.useTrailing ? "Yes" : "No"));
}

//+------------------------------------------------------------------+
//| Create sample parameter sets CSV file                            |
//+------------------------------------------------------------------+
bool CreateSampleParameterFile(string filename)
{
    int fileHandle = FileOpen(filename, FILE_WRITE | FILE_CSV | FILE_COMMON);
    
    if(fileHandle == INVALID_HANDLE)
    {
        Print("ERROR: Cannot create parameter file: ", filename);
        return false;
    }
    
    // Write header
    FileWrite(fileHandle, "id", "stopLoss", "takeProfit", "trailingStop", "riskPercent", "maxPositions", "useTrailing", "description");
    
    // Write sample data
    FileWrite(fileHandle, "conservative", "200", "400", "50", "1.0", "1", "true", "Low risk strategy");
    FileWrite(fileHandle, "moderate", "150", "300", "40", "1.5", "2", "true", "Medium risk strategy");
    FileWrite(fileHandle, "aggressive", "100", "200", "30", "2.0", "3", "true", "High risk strategy");
    FileWrite(fileHandle, "scalping", "50", "100", "20", "0.5", "5", "false", "Quick trades");
    FileWrite(fileHandle, "swing", "300", "600", "100", "2.5", "1", "true", "Long term trades");
    
    FileClose(fileHandle);
    Print("Sample parameter file created: ", filename);
    return true;
}

//+------------------------------------------------------------------+
//| Calculate lot size based on risk percentage                      |
//+------------------------------------------------------------------+
double CalculateLotSize(double riskPercent, int stopLossPoints)
{
    if(stopLossPoints <= 0)
    {
        Print("WARNING: Invalid stop loss points: ", stopLossPoints);
        return 0.01; // Minimum lot size
    }
    
    double accountBalance = AccountBalance();
    double riskAmount = accountBalance * (riskPercent / 100.0);
    
    // Calculate pip value (for EURUSD-like pairs)
    double pipValue = 10.0; // $10 per pip for 1 standard lot on EURUSD
    double pointValue = pipValue / 10.0; // $1 per point
    
    double maxLoss = stopLossPoints * pointValue;
    
    if(maxLoss <= 0)
    {
        return 0.01;
    }
    
    double lotSize = riskAmount / maxLoss;
    
    // Round to 2 decimal places and ensure minimum
    lotSize = MathMax(0.01, NormalizeDouble(lotSize, 2));
    
    // Respect maximum lot size limits
    double maxLot = MarketInfo(Symbol(), MODE_MAXLOT);
    lotSize = MathMin(lotSize, maxLot);
    
    Print("Risk calculation: Balance=", DoubleToString(accountBalance, 2), 
          " Risk%=", DoubleToString(riskPercent, 2),
          " RiskAmount=", DoubleToString(riskAmount, 2),
          " SL=", stopLossPoints, "pts",
          " → LotSize=", DoubleToString(lotSize, 2));
    
    return lotSize;
}
```

**10.2 Create EA that Uses Configuration Files (2-3 hours)**

```
File → New → Expert Advisor
Name: HUEY_P_MQL4_learning_03_config
```

```mql4
//+------------------------------------------------------------------+
//| HUEY_P_MQL4_learning_03_config.mq4                              |
//| Expert Advisor that reads configuration from CSV files          |
//+------------------------------------------------------------------+
#property copyright "Trading System Beginner"
#property version   "1.00"
#property strict

// Include our configuration reader
#include <HUEY_P_MQH_config_reader.mqh>

// Input parameters
input string ParameterSetFile = "HUEY_P_CSV_parameter_sets.csv";
input string SelectedStrategy = "moderate";  // Which strategy to use
input int MagicNumber = 12347;

// Global variables
ParameterSet g_parameterSets[50];  // Array to store all parameter sets
int g_parameterCount = 0;          // How many parameter sets loaded
ParameterSet g_currentParams;      // Currently selected parameter set
bool g_configLoaded = false;       // Flag to track if config is loaded

//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
{
    Print("=== Configuration-Based EA Started ===");
    Print("Parameter file: ", ParameterSetFile);
    Print("Selected strategy: ", SelectedStrategy);
    
    // Create sample file if it doesn't exist
    if(!FileIsExist(ParameterSetFile, FILE_COMMON))
    {
        Print("Parameter file not found. Creating sample file...");
        if(!CreateSampleParameterFile(ParameterSetFile))
        {
            Print("ERROR: Failed to create sample parameter file");
            return INIT_FAILED;
        }
    }
    
    // Load parameter sets from file
    if(!ReadParameterSets(ParameterSetFile, g_parameterSets, g_parameterCount))
    {
        Print("ERROR: Failed to load parameter sets");
        return INIT_FAILED;
    }
    
    // Find the selected strategy
    if(!FindParameterSet(SelectedStrategy, g_parameterSets, g_parameterCount, g_currentParams))
    {
        Print("ERROR: Selected strategy '", SelectedStrategy, "' not found");
        Print("Available strategies:");
        for(int i = 0; i < g_parameterCount; i++)
        {
            Print("  - ", g_parameterSets[i].id);
        }
        return INIT_FAILED;
    }
    
    // Display selected parameters
    Print("=== Selected Strategy Configuration ===");
    PrintParameterSet(g_currentParams);
    
    g_configLoaded = true;
    Print("EA initialization completed successfully");
    
    return INIT_SUCCEEDED;
}

//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
{
    Print("=== Configuration-Based EA Stopped ===");
    Print("Final trade count: ", CountMyTrades());
}

//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
{
    // Don't trade if configuration not loaded
    if(!g_configLoaded)
    {
        return;
    }
    
    // Don't trade if we've reached maximum positions
    if(CountMyTrades() >= g_currentParams.maxPositions)
    {
        return;
    }
    
    // Simple trading logic based on loaded parameters
    if(ShouldOpenTrade())
    {
        OpenTradeWithLoadedParams();
    }
    
    // Manage existing trades with trailing stops
    if(g_currentParams.useTrailing)
    {
        ManageTrailingStops();
    }
}

//+------------------------------------------------------------------+
//| Check if we should open a new trade                              |
//+------------------------------------------------------------------+
bool ShouldOpenTrade()
{
    // Basic checks
    if(!IsTradeAllowed()) return false;
    
    // Check spread
    double spread = MarketInfo(Symbol(), MODE_SPREAD);
    if(spread > 5) // Max 5 points spread
    {
        return false;
    }
    
    // Don't trade if we already have open positions
    if(CountMyTrades() > 0)
    {
        return false;
    }
    
    // Simple time filter
    int hour = Hour();
    if(hour < 8 || hour > 18)
    {
        return false;
    }
    
    // Simple trend detection (very basic)
    double ma_fast = iMA(Symbol(), PERIOD_M5, 10, 0, MODE_SMA, PRICE_CLOSE, 0);
    double ma_slow = iMA(Symbol(), PERIOD_M5, 20, 0, MODE_SMA, PRICE_CLOSE, 0);
    
    // Only trade if there's a clear trend
    return (MathAbs(ma_fast - ma_slow) > 10 * Point);
}

//+------------------------------------------------------------------+
//| Open trade using loaded parameters                               |
//+------------------------------------------------------------------+
void OpenTradeWithLoadedParams()
{
    // Calculate lot size based on risk percentage
    double lotSize = CalculateLotSize(g_currentParams.riskPercent, g_currentParams.stopLoss);
    
    // Determine trade direction
    double ma_fast = iMA(Symbol(), PERIOD_M5, 10, 0, MODE_SMA, PRICE_CLOSE, 0);
    double ma_slow = iMA(Symbol(), PERIOD_M5, 20, 0, MODE_SMA, PRICE_CLOSE, 0);
    
    int orderType;
    double price, sl, tp;
    color arrowColor;
    string comment;
    
    if(ma_fast > ma_slow) // Uptrend
    {
        orderType = OP_BUY;
        price = Ask;
        sl = price - (g_currentParams.stopLoss * Point);
        tp = price + (g_currentParams.takeProfit * Point);
        arrowColor = clrGreen;
        comment = "BUY-" + g_currentParams.id;
    }
    else // Downtrend
    {
        orderType = OP_SELL;
        price = Bid;
        sl = price + (g_currentParams.stopLoss * Point);
        tp = price - (g_currentParams.takeProfit * Point);
        arrowColor = clrRed;
        comment = "SELL-" + g_currentParams.id;
    }
    
    Print("=== Opening Trade with ", g_currentParams.id, " Strategy ===");
    Print("Order Type: ", (orderType == OP_BUY ? "BUY" : "SELL"));
    Print("Lot Size: ", DoubleToString(lotSize, 2));
    Print("Entry Price: ", DoubleToString(price, Digits));
    Print("Stop Loss: ", DoubleToString(sl, Digits), " (", g_currentParams.stopLoss, " points)");
    Print("Take Profit: ", DoubleToString(tp, Digits), " (", g_currentParams.takeProfit, " points)");
    
    int ticket = OrderSend(
        Symbol(),
        orderType,
        lotSize,
        price,
        3,
        sl,
        tp,
        comment,
        MagicNumber,
        0,
        arrowColor
    );
    
    if(ticket > 0)
    {
        Print("SUCCESS: Trade opened with ticket #", ticket);
    }
    else
    {
        int error = GetLastError();
        Print("ERROR: Failed to open trade. Error: ", error, " - ", ErrorDescription(error));
    }
}

//+------------------------------------------------------------------+
//| Manage trailing stops for open trades                            |
//+------------------------------------------------------------------+
void ManageTrailingStops()
{
    for(int i = OrdersTotal() - 1; i >= 0; i--)
    {
        if(OrderSelect(i, SELECT_BY_POS, MODE_TRADES))
        {
            if(OrderSymbol() == Symbol() && OrderMagicNumber() == MagicNumber)
            {
                double newSL = 0;
                bool shouldModify = false;
                
                if(OrderType() == OP_BUY)
                {
                    newSL = Bid - (g_currentParams.trailingStop * Point);
                    if(newSL > OrderStopLoss() + (5 * Point)) // Only move if 5+ points improvement
                    {
                        shouldModify = true;
                    }
                }
                else if(OrderType() == OP_SELL)
                {
                    newSL = Ask + (g_currentParams.trailingStop * Point);
                    if(newSL < OrderStopLoss() - (5 * Point)) // Only move if 5+ points improvement
                    {
                        shouldModify = true;
                    }
                }
                
                if(shouldModify)
                {
                    bool result = OrderModify(
                        OrderTicket(),
                        OrderOpenPrice(),
                        newSL,
                        OrderTakeProfit(),
                        0,
                        clrBlue
                    );
                    
                    if(result)
                    {
                        Print("Trailing stop updated for ticket #", OrderTicket(), 
                              " to ", DoubleToString(newSL, Digits));
                    }
                }
            }
        }
    }
}

//+------------------------------------------------------------------+
//| Count trades opened by this EA                                   |
//+------------------------------------------------------------------+
int CountMyTrades()
{
    int count = 0;
    for(int i = 0; i < OrdersTotal(); i++)
    {
        if(OrderSelect(i, SELECT_BY_POS, MODE_TRADES))
        {
            if(OrderSymbol() == Symbol() && OrderMagicNumber() == MagicNumber)
            {
                count++;
            }
        }
    }
    return count;
}
```

**Test the Configuration EA:**
```
1. Compile both files (the .mqh and .mq4)
2. Attach HUEY_P_MQL4_learning_03_config to a chart
3. In settings:
   - ParameterSetFile: HUEY_P_CSV_parameter_sets.csv
   - SelectedStrategy: moderate (or try "conservative", "aggressive")
   - MagicNumber: 12347
4. Watch the Experts log to see configuration loading
```

### **Week 7-8: Basic C++ and PowerShell (20-25 hours)**

#### **Day 29-32: Simple C++ DLL Development (10-12 hours)**

**Learning Objective**: Create a basic communication bridge between Python and MQL4.

**Step 11: Your First Communication DLL**

**11.1 Understanding C++ DLL Basics (4 hours)**

Create a new Visual Studio project:
```
1. Open Visual Studio
2. File → New → Project
3. Visual C++ → Windows Desktop → Dynamic-Link Library (DLL)
4. Name: HUEY_P_CPP_simple_bridge
5. Location: C:\TradingSystem\Source\CPP\
```

**Replace the default code with this simple bridge:**

**HUEY_P_CPP_simple_bridge.h:**
```cpp
// HUEY_P_CPP_simple_bridge.h
// Simple communication bridge between Python and MQL4

#pragma once

// DLL export macros
#ifdef SIMPLEBRIDGE_EXPORTS
#define SIMPLEBRIDGE_API __declspec(dllexport)
#else
#define SIMPLEBRIDGE_API __declspec(dllimport)
#endif

// Include necessary headers
#include <string>
#include <queue>
#include <mutex>

// Simple message structure
struct SimpleMessage
{
    char symbol[10];        // Currency pair (e.g., "EURUSD")
    char command[10];       // Trading command (e.g., "BUY", "SELL")
    double confidence;      // Signal confidence (0.0 to 1.0)
    int stopLoss;          // Stop loss in points
    int takeProfit;        // Take profit in points
    char timestamp[20];    // When signal was generated
};

// C-style functions for MQL4
extern "C" {
    // Initialize the bridge
    SIMPLEBRIDGE_API int __stdcall InitializeBridge();
    
    // Shutdown the bridge
    SIMPLEBRIDGE_API void __stdcall ShutdownBridge();
    
    // Add a message to the queue (called by Python)
    SIMPLEBRIDGE_API int __stdcall AddMessage(const char* symbol, const char* command, 
                                              double confidence, int stopLoss, int takeProfit);
    
    // Get next message from queue (called by MQL4)
    SIMPLEBRIDGE_API int __stdcall GetNextMessage(char* symbol, char* command, 
                                                  double* confidence, int* stopLoss, int* takeProfit);
    
    // Get status information
    SIMPLEBRIDGE_API int __stdcall GetMessageCount();
    SIMPLEBRIDGE_API int __stdcall GetBridgeStatus();
}
```

**HUEY_P_CPP_simple_bridge.cpp:**
```cpp
// HUEY_P_CPP_simple_bridge.cpp
// Implementation of simple communication bridge

#include "pch.h"
#include "HUEY_P_CPP_simple_bridge.h"
#include <iostream>
#include <ctime>
#include <cstring>

// Global variables
std::queue<SimpleMessage> g_messageQueue;
std::mutex g_queueMutex;
bool g_bridgeInitialized = false;

// Helper function to get current timestamp
void GetCurrentTimestamp(char* buffer, size_t bufferSize)
{
    time_t rawtime;
    struct tm timeinfo;
    time(&rawtime);
    localtime_s(&timeinfo, &rawtime);
    strftime(buffer, bufferSize, "%Y-%m-%d %H:%M:%S", &timeinfo);
}

// Helper function to safely copy strings
void SafeStringCopy(char* dest, const char* src, size_t destSize)
{
    strcpy_s(dest, destSize, src);
}

//+------------------------------------------------------------------+
//| Initialize the bridge                                            |
//+------------------------------------------------------------------+
extern "C" int __stdcall InitializeBridge()
{
    std::cout << "=== Initializing Simple Bridge ===" << std::endl;
    
    try 
    {
        // Clear any existing messages
        std::lock_guard<std::mutex> lock(g_queueMutex);
        
        // Clear the queue
        while (!g_messageQueue.empty()) 
        {
            g_messageQueue.pop();
        }
        
        g_bridgeInitialized = true;
        std::cout << "Bridge initialized successfully" << std::endl;
        return 1; // Success
    }
    catch (const std::exception& e)
    {
        std::cout << "Error initializing bridge: " << e.what() << std::endl;
        return -1; // Error
    }
}

//+------------------------------------------------------------------+
//| Shutdown the bridge                                              |
//+------------------------------------------------------------------+
extern "C" void __stdcall ShutdownBridge()
{
    std::cout << "=== Shutting Down Simple Bridge ===" << std::endl;
    
    std::lock_guard<std::mutex> lock(g_queueMutex);
    
    // Clear all messages
    while (!g_messageQueue.empty()) 
    {
        g_messageQueue.pop();
    }
    
    g_bridgeInitialized = false;
    std::cout << "Bridge shutdown complete" << std::endl;
}

//+------------------------------------------------------------------+
//| Add a message to the queue                                       |
//+------------------------------------------------------------------+
extern "C" int __stdcall AddMessage(const char* symbol, const char* command, 
                                   double confidence, int stopLoss, int takeProfit)
{
    if (!g_bridgeInitialized)
    {
        std::cout << "Error: Bridge not initialized!" << std::endl;
        return -1;
    }
    
    try 
    {
        SimpleMessage msg;
        
        // Copy data to message structure
        SafeStringCopy(msg.symbol, symbol, sizeof(msg.symbol));
        SafeStringCopy(msg.command, command, sizeof(msg.command));
        msg.confidence = confidence;
        msg.stopLoss = stopLoss;
        msg.takeProfit = takeProfit;
        GetCurrentTimestamp(msg.timestamp, sizeof(msg.timestamp));
        
        // Add to queue (thread-safe)
        {
            std::lock_guard<std::mutex> lock(g_queueMutex);
            g_messageQueue.push(msg);
        }
        
        std::cout << "Message added: " << symbol << " " << command 
                  << " (confidence: " << confidence << ")" << std::endl;
        
        return 1; // Success
    }
    catch (const std::exception& e)
    {
        std::cout << "Error adding message: " << e.what() << std::endl;
        return -1; // Error
    }
}

//+------------------------------------------------------------------+
//| Get next message from queue                                      |
//+------------------------------------------------------------------+
extern "C" int __stdcall GetNextMessage(char* symbol, char* command, 
                                       double* confidence, int* stopLoss, int* takeProfit)
{
    if (!g_bridgeInitialized)
    {
        return -1; // Bridge not initialized
    }
    
    std::lock_guard<std::mutex> lock(g_queueMutex);
    
    if (g_messageQueue.empty())
    {
        return 0; // No messages available
    }
    
    try 
    {
        SimpleMessage msg = g_messageQueue.front();
        g_messageQueue.pop();
        
        // Copy data to output parameters
        SafeStringCopy(symbol, msg.symbol, 10);
        SafeStringCopy(command, msg.command, 10);
        *confidence = msg.confidence;
        *stopLoss = msg.stopLoss;
        *takeProfit = msg.takeProfit;
        
        std::cout << "Message retrieved: " << msg.symbol << " " << msg.command << std::endl;
        
        return 1; // Success - message retrieved
    }
    catch (const std::exception& e)
    {
        std::cout << "Error getting message: " << e.what() << std::endl;
        return -1; // Error
    }
}

//+------------------------------------------------------------------+
//| Get number of messages in queue                                  |
//+------------------------------------------------------------------+
extern "C" int __stdcall GetMessageCount()
{
    if (!g_bridgeInitialized)
    {
        return -1;
    }
    
    std::lock_guard<std::mutex> lock(g_queueMutex);
    return static_cast<int>(g_messageQueue.size());
}

//+------------------------------------------------------------------+
//| Get bridge status                                                |
//+------------------------------------------------------------------+
extern "C" int __stdcall GetBridgeStatus()
{
    if (!g_bridgeInitialized)
    {
        return 0; // Not initialized
    }
    
    return 1; // Running normally
}
```

**Build the DLL:**
```
1. Build → Build Solution (Ctrl+Shift+B)
2. Should compile without errors
3. Find HUEY_P_CPP_simple_bridge.dll in the Debug folder
4. Copy it to C:\TradingSystem\Source\CPP\
```

**11.2 Test the DLL with Python (3 hours)**

Create a Python test script:

**C:\TradingSystem\Source\Python\HUEY_P_PY_test_bridge.py:**
```python
# HUEY_P_PY_test_bridge.py
# Test the C++ bridge from Python side

import ctypes
import time
import os

# Load the DLL
def load_bridge_dll():
    """Load the C++ bridge DLL"""
    dll_path = r"C:\TradingSystem\Source\CPP\HUEY_P_CPP_simple_bridge.dll"
    
    if not os.path.exists(dll_path):
        print(f"ERROR: DLL not found at {dll_path}")
        print("Make sure you compiled the C++ bridge DLL first!")
        return None
    
    try:
        # Load the DLL
        bridge = ctypes.CDLL(dll_path)
        
        # Define function signatures
        # InitializeBridge() -> int
        bridge.InitializeBridge.restype = ctypes.c_int
        bridge.InitializeBridge.argtypes = []
        
        # ShutdownBridge() -> void
        bridge.ShutdownBridge.restype = None
        bridge.ShutdownBridge.argtypes = []
        
        # AddMessage(symbol, command, confidence, stopLoss, takeProfit) -> int
        bridge.AddMessage.restype = ctypes.c_int
        bridge.AddMessage.argtypes = [ctypes.c_char_p, ctypes.c_char_p, 
                                     ctypes.c_double, ctypes.c_int, ctypes.c_int]
        
        # GetMessageCount() -> int
        bridge.GetMessageCount.restype = ctypes.c_int
        bridge.GetMessageCount.argtypes = []
        
        # GetBridgeStatus() -> int
        bridge.GetBridgeStatus.restype = ctypes.c_int
        bridge.GetBridgeStatus.argtypes = []
        
        print("✓ Bridge DLL loaded successfully")
        return bridge
        
    except Exception as e:
        print(f"ERROR loading DLL: {e}")
        return None

def test_bridge_functionality():
    """Test all bridge functions"""
    print("=== Testing C++ Bridge from Python ===")
    
    # Load the bridge
    bridge = load_bridge_dll()
    if not bridge:
        return False
    
    # Test 1: Initialize bridge
    print("\n1. Initializing bridge...")
    result = bridge.InitializeBridge()
    if result == 1:
        print("   ✓ Bridge initialized successfully")
    else:
        print("   ✗ Bridge initialization failed")
        return False
    
    # Test 2: Check initial status
    print("\n2. Checking bridge status...")
    status = bridge.GetBridgeStatus()
    print(f"   Bridge status: {status} (1 = running, 0 = stopped)")
    
    # Test 3: Check initial message count
    print("\n3. Checking initial message count...")
    count = bridge.GetMessageCount()
    print(f"   Initial message count: {count}")
    
    # Test 4: Add some test messages
    print("\n4. Adding test messages...")
    
    test_messages = [
        ("EURUSD", "BUY", 0.85, 50, 100),
        ("GBPUSD", "SELL", 0.75, 60, 120),
        ("USDJPY", "BUY", 0.90, 40, 80),
    ]
    
    for symbol, command, confidence, sl, tp in test_messages:
        result = bridge.AddMessage(
            symbol.encode('utf-8'),
            command.encode('utf-8'),
            confidence,
            sl,
            tp
        )
        
        if result == 1:
            print(f"   ✓ Added: {symbol} {command} (confidence: {confidence})")
        else:
            print(f"   ✗ Failed to add: {symbol} {command}")
    
    # Test 5: Check message count after adding
    print("\n5. Checking message count after adding...")
    count = bridge.GetMessageCount()
    print(f"   Message count: {count}")
    
    # Test 6: Monitor messages for a few seconds
    print("\n6. Monitoring message queue...")
    for i in range(10):
        count = bridge.GetMessageCount()
        print(f"   Messages in queue: {count}")
        time.sleep(1)
        
        if count == 0:
            print("   (All messages consumed by MQL4 EA, or no EA running)")
            break
    
    # Test 7: Shutdown bridge
    print("\n7. Shutting down bridge...")
    bridge.ShutdownBridge()
    print("   ✓ Bridge shutdown complete")
    
    print("\n=== Bridge Test Complete ===")
    return True

def send_continuous_signals():
    """Send signals continuously for testing with MT4"""
    print("=== Continuous Signal Sender ===")
    print("This will send trading signals every 10 seconds")
    print("Attach an EA to MT4 to see it receive these signals")
    print("Press Ctrl+C to stop")
    
    bridge = load_bridge_dll()
    if not bridge:
        return
    
    # Initialize bridge
    result = bridge.InitializeBridge()
    if result != 1:
        print("Failed to initialize bridge")
        return
    
    try:
        signal_count = 0
        
        while True:
            signal_count += 1
            
            # Alternate between different signals
            if signal_count % 3 == 1:
                symbol, command, confidence = "EURUSD", "BUY", 0.80
            elif signal_count % 3 == 2:
                symbol, command, confidence = "GBPUSD", "SELL", 0.75
            else:
                symbol, command, confidence = "USDJPY", "BUY", 0.85
            
            # Add the signal
            result = bridge.AddMessage(
                symbol.encode('utf-8'),
                command.encode('utf-8'),
                confidence,
                50,  # Stop loss
                100  # Take profit
            )
            
            if result == 1:
                print(f"Signal #{signal_count}: {symbol} {command} (confidence: {confidence})")
            else:
                print(f"Failed to send signal #{signal_count}")
            
            # Check queue status
            count = bridge.GetMessageCount()
            print(f"   Messages in queue: {count}")
            
            # Wait 10 seconds
            time.sleep(10)
            
    except KeyboardInterrupt:
        print("\nStopping signal sender...")
        bridge.ShutdownBridge()
        print("Bridge shutdown complete")

if __name__ == "__main__":
    print("Bridge Test Options:")
    print("1. Run basic functionality test")
    print("2. Send continuous signals (for MT4 testing)")
    
    choice = input("Enter choice (1 or 2): ")
    
    if choice == "1":
        test_bridge_functionality()
    elif choice == "2":
        send_continuous_signals()
    else:
        print("Invalid choice")
```

**Test the Python-DLL connection:**
```powershell
cd C:\TradingSystem\Source\Python
python HUEY_P_PY_test_bridge.py
# Choose option 1 for basic test
```

**11.3 Create MQL4 EA to Test Bridge (3-4 hours)**

Create an EA that uses the bridge:

**HUEY_P_MQL4_bridge_test.mq4:**
```mql4
//+------------------------------------------------------------------+
//| HUEY_P_MQL4_bridge_test.mq4                                     |
//| Test EA for C++ bridge communication                            |
//+------------------------------------------------------------------+
#property copyright "Trading System Beginner"
#property version   "1.00"
#property strict

// DLL imports
#import "HUEY_P_CPP_simple_bridge.dll"
   int InitializeBridge();
   void ShutdownBridge();
   int GetNextMessage(string &symbol, string &command, double &confidence, int &stopLoss, int &takeProfit);
   int GetMessageCount();
   int GetBridgeStatus();
#import

// Input parameters
input int CheckIntervalSeconds = 5;   // How often to check for messages
input bool PrintDebugInfo = true;    // Show debug information
input int MagicNumber = 12348;       // Magic number for trades

// Global variables
datetime g_lastCheck = 0;
int g_totalMessagesReceived = 0;
bool g_bridgeConnected = false;

//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
{
    Print("=== Bridge Test EA Started ===");
    
    // Initialize the bridge
    int result = InitializeBridge();
    if(result == 1)
    {
        Print("✓ Bridge initialized successfully");
        g_bridgeConnected = true;
    }
    else
    {
        Print("✗ Bridge initialization failed");
        g_bridgeConnected = false;
        return INIT_FAILED;
    }
    
    // Check bridge status
    int status = GetBridgeStatus();
    Print("Bridge status: ", status, " (1 = running, 0 = stopped)");
    
    // Initial message count
    int messageCount = GetMessageCount();
    Print("Initial messages in queue: ", messageCount);
    
    Print("EA will check for messages every ", CheckIntervalSeconds, " seconds");
    Print("Bridge Test EA initialization complete");
    
    return INIT_SUCCEEDED;
}

//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
{
    Print("=== Bridge Test EA Stopping ===");
    Print("Total messages received: ", g_totalMessagesReceived);
    
    if(g_bridgeConnected)
    {
        ShutdownBridge();
        Print("Bridge shutdown complete");
    }
}

//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
{
    // Only check for messages periodically, not on every tick
    if(TimeCurrent() - g_lastCheck >= CheckIntervalSeconds)
    {
        CheckForMessages();
        g_lastCheck = TimeCurrent();
    }
}

//+------------------------------------------------------------------+
//| Check for and process incoming messages                          |
//+------------------------------------------------------------------+
void CheckForMessages()
{
    if(!g_bridgeConnected)
    {
        return;
    }
    
    // Check how many messages are waiting
    int messageCount = GetMessageCount();
    
    if(PrintDebugInfo && messageCount > 0)
    {
        Print("Messages available: ", messageCount);
    }
    
    // Process all available messages
    while(messageCount > 0)
    {
        ProcessNextMessage();
        messageCount = GetMessageCount();
    }
}

//+------------------------------------------------------------------+
//| Process a single message from the bridge                         |
//+------------------------------------------------------------------+
void ProcessNextMessage()
{
    string symbol = "";
    string command = "";
    double confidence = 0.0;
    int stopLoss = 0;
    int takeProfit = 0;
    
    // Get the next message
    int result = GetNextMessage(symbol, command, confidence, stopLoss, takeProfit);
    
    if(result == 1) // Success
    {
        g_totalMessagesReceived++;
        
        Print("=== Message #", g_totalMessagesReceived, " Received ===");
        Print("Symbol: ", symbol);
        Print("Command: ", command);
        Print("Confidence: ", DoubleToString(confidence, 2));
        Print("Stop Loss: ", stopLoss, " points");
        Print("Take Profit: ", takeProfit, " points");
        
        // Only process messages for our current symbol
        if(symbol == Symbol())
        {
            ProcessTradingSignal(command, confidence, stopLoss, takeProfit);
        }
        else
        {
            Print("Message for different symbol (", symbol, "), ignoring");
        }
    }
    else if(result == 0)
    {
        // No messages available (shouldn't happen in this context)
        if(PrintDebugInfo)
        {
            Print("No messages available");
        }
    }
    else
    {
        Print("Error retrieving message: ", result);
    }
}

//+------------------------------------------------------------------+
//| Process a trading signal                                          |
//+------------------------------------------------------------------+
void ProcessTradingSignal(string command, double confidence, int stopLossPoints, int takeProfitPoints)
{
    Print("=== Processing Trading Signal ===");
    Print("Command: ", command);
    Print("Confidence: ", DoubleToString(confidence, 2));
    
    // For testing
	
	
```mql4
//+------------------------------------------------------------------+
//| Process a trading signal                                          |
//+------------------------------------------------------------------+
void ProcessTradingSignal(string command, double confidence, int stopLossPoints, int takeProfitPoints)
{
    Print("=== Processing Trading Signal ===");
    Print("Command: ", command);
    Print("Confidence: ", DoubleToString(confidence, 2));
    
    // For testing, we'll only simulate trades, not actually place them
    // You can enable real trading later by changing this flag
    bool SIMULATE_ONLY = true;
    
    if(SIMULATE_ONLY)
    {
        SimulateTrade(command, confidence, stopLossPoints, takeProfitPoints);
        return;
    }
    
    // Check basic trading conditions
    if(!IsTradeAllowed())
    {
        Print("Trading not allowed");
        return;
    }
    
    // Check confidence threshold
    if(confidence < 0.7)
    {
        Print("Confidence too low (", DoubleToString(confidence, 2), "), skipping trade");
        return;
    }
    
    // Check if we already have trades
    if(CountOpenTrades() > 0)
    {
        Print("Already have open trades, skipping");
        return;
    }
    
    // Execute the trade based on command
    if(command == "BUY")
    {
        ExecuteBuyOrder(stopLossPoints, takeProfitPoints);
    }
    else if(command == "SELL")
    {
        ExecuteSellOrder(stopLossPoints, takeProfitPoints);
    }
    else
    {
        Print("Unknown command: ", command);
    }
}

//+------------------------------------------------------------------+
//| Simulate a trade (for testing purposes)                          |
//+------------------------------------------------------------------+
void SimulateTrade(string command, double confidence, int stopLossPoints, int takeProfitPoints)
{
    Print("=== SIMULATING TRADE (Not Real) ===");
    Print("Would execute: ", command);
    Print("Entry price would be: ", (command == "BUY" ? DoubleToString(Ask, Digits) : DoubleToString(Bid, Digits)));
    Print("Stop Loss: ", stopLossPoints, " points");
    Print("Take Profit: ", takeProfitPoints, " points");
    Print("Confidence: ", DoubleToString(confidence, 2));
    Print("================================");
}

//+------------------------------------------------------------------+
//| Execute a buy order                                               |
//+------------------------------------------------------------------+
void ExecuteBuyOrder(int stopLossPoints, int takeProfitPoints)
{
    double price = Ask;
    double sl = (stopLossPoints > 0) ? price - (stopLossPoints * Point) : 0;
    double tp = (takeProfitPoints > 0) ? price + (takeProfitPoints * Point) : 0;
    
    Print("Executing BUY order:");
    Print("  Price: ", DoubleToString(price, Digits));
    Print("  SL: ", DoubleToString(sl, Digits));
    Print("  TP: ", DoubleToString(tp, Digits));
    
    int ticket = OrderSend(
        Symbol(),
        OP_BUY,
        0.01,  // Micro lot for testing
        price,
        3,
        sl,
        tp,
        "Bridge Test",
        MagicNumber,
        0,
        clrGreen
    );
    
    if(ticket > 0)
    {
        Print("✓ BUY order placed successfully, ticket: ", ticket);
    }
    else
    {
        int error = GetLastError();
        Print("✗ BUY order failed, error: ", error, " - ", ErrorDescription(error));
    }
}

//+------------------------------------------------------------------+
//| Execute a sell order                                              |
//+------------------------------------------------------------------+
void ExecuteSellOrder(int stopLossPoints, int takeProfitPoints)
{
    double price = Bid;
    double sl = (stopLossPoints > 0) ? price + (stopLossPoints * Point) : 0;
    double tp = (takeProfitPoints > 0) ? price - (takeProfitPoints * Point) : 0;
    
    Print("Executing SELL order:");
    Print("  Price: ", DoubleToString(price, Digits));
    Print("  SL: ", DoubleToString(sl, Digits));
    Print("  TP: ", DoubleToString(tp, Digits));
    
    int ticket = OrderSend(
        Symbol(),
        OP_SELL,
        0.01,  // Micro lot for testing
        price,
        3,
        sl,
        tp,
        "Bridge Test",
        MagicNumber,
        0,
        clrRed
    );
    
    if(ticket > 0)
    {
        Print("✓ SELL order placed successfully, ticket: ", ticket);
    }
    else
    {
        int error = GetLastError();
        Print("✗ SELL order failed, error: ", error, " - ", ErrorDescription(error));
    }
}

//+------------------------------------------------------------------+
//| Count open trades with our magic number                          |
//+------------------------------------------------------------------+
int CountOpenTrades()
{
    int count = 0;
    for(int i = 0; i < OrdersTotal(); i++)
    {
        if(OrderSelect(i, SELECT_BY_POS, MODE_TRADES))
        {
            if(OrderSymbol() == Symbol() && OrderMagicNumber() == MagicNumber)
            {
                count++;
            }
        }
    }
    return count;
}
```

**Complete Bridge Test (1 hour):**
```
1. Copy HUEY_P_CPP_simple_bridge.dll to MT4/Libraries/ folder
2. Compile HUEY_P_MQL4_bridge_test.mq4
3. Attach EA to EURUSD chart
4. Run Python script: python HUEY_P_PY_test_bridge.py (choose option 2)
5. Watch Experts tab in MT4 - you should see messages being received
```

#### **Day 33-35: Basic PowerShell Automation (8-10 hours)**

**Learning Objective**: Create scripts to automate system deployment and monitoring.

**Step 12: Your First PowerShell Automation Scripts**

**12.1 Understanding PowerShell Basics (3 hours)**

Create: `C:\TradingSystem\Source\PowerShell\HUEY_P_PS1_basics_01.ps1`

```powershell
# HUEY_P_PS1_basics_01.ps1
# Learning PowerShell basics for trading system automation

# Set error handling
$ErrorActionPreference = "Stop"

Write-Host "=== PowerShell Basics for Trading System ===" -ForegroundColor Green

# Variables and basic operations
$TradingSystemPath = "C:\TradingSystem"
$MT4Path = "C:\Program Files (x86)\MetaTrader 4"
$PythonCommand = "python"

Write-Host "`nBasic Variables:" -ForegroundColor Yellow
Write-Host "  Trading System Path: $TradingSystemPath"
Write-Host "  MT4 Path: $MT4Path"
Write-Host "  Python Command: $PythonCommand"

# Working with paths
Write-Host "`nPath Operations:" -ForegroundColor Yellow

# Check if directories exist
if (Test-Path $TradingSystemPath) {
    Write-Host "  ✓ Trading system directory exists" -ForegroundColor Green
    
    # List subdirectories
    $SubDirs = Get-ChildItem $TradingSystemPath -Directory
    Write-Host "  Subdirectories found: $($SubDirs.Count)"
    
    foreach ($dir in $SubDirs) {
        Write-Host "    📁 $($dir.Name)" -ForegroundColor White
    }
} else {
    Write-Host "  ✗ Trading system directory not found!" -ForegroundColor Red
}

# Check if MT4 exists
if (Test-Path $MT4Path) {
    Write-Host "  ✓ MetaTrader 4 found" -ForegroundColor Green
} else {
    Write-Host "  ⚠️  MetaTrader 4 path not found (may be different location)" -ForegroundColor Yellow
}

# Working with processes
Write-Host "`nProcess Management:" -ForegroundColor Yellow

# Check if MT4 is running
$MT4Process = Get-Process -Name "terminal64" -ErrorAction SilentlyContinue
if ($MT4Process) {
    Write-Host "  ✓ MetaTrader 4 is currently running" -ForegroundColor Green
    Write-Host "    Process ID: $($MT4Process.Id)"
    Write-Host "    Memory usage: $([math]::Round($MT4Process.WorkingSet / 1MB, 2)) MB"
} else {
    Write-Host "  ℹ️  MetaTrader 4 is not currently running" -ForegroundColor Cyan
}

# Check if Python is available
Write-Host "`nPython Environment:" -ForegroundColor Yellow
try {
    $PythonVersion = & python --version 2>&1
    Write-Host "  ✓ Python available: $PythonVersion" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Python not found in PATH!" -ForegroundColor Red
}

# Working with files
Write-Host "`nFile Operations:" -ForegroundColor Yellow

# Create a sample configuration file
$ConfigPath = Join-Path $TradingSystemPath "temp_config.txt"
$ConfigContent = @"
# Sample Trading System Configuration
SystemName=HUEY_P_ClaudeCentric
Version=1.0.0
Environment=Development
LastUpdated=$(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
"@

try {
    $ConfigContent | Out-File -FilePath $ConfigPath -Encoding UTF8
    Write-Host "  ✓ Created sample config file: $ConfigPath" -ForegroundColor Green
    
    # Read it back
    $ReadContent = Get-Content $ConfigPath
    Write-Host "  ✓ Config file contains $($ReadContent.Count) lines" -ForegroundColor Green
    
    # Clean up
    Remove-Item $ConfigPath
    Write-Host "  ✓ Cleaned up temporary file" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Error working with config file: $($_.Exception.Message)" -ForegroundColor Red
}

# Function examples
function Test-TradingSystemHealth {
    param(
        [string]$SystemPath
    )
    
    Write-Host "`nTesting Trading System Health..." -ForegroundColor Yellow
    
    $RequiredFolders = @("Source", "Config", "Database", "Scripts")
    $HealthScore = 0
    
    foreach ($folder in $RequiredFolders) {
        $FolderPath = Join-Path $SystemPath $folder
        if (Test-Path $FolderPath) {
            Write-Host "  ✓ $folder folder exists" -ForegroundColor Green
            $HealthScore++
        } else {
            Write-Host "  ✗ $folder folder missing" -ForegroundColor Red
        }
    }
    
    $HealthPercentage = ($HealthScore / $RequiredFolders.Count) * 100
    Write-Host "`nSystem Health: $HealthScore/$($RequiredFolders.Count) ($HealthPercentage%)" -ForegroundColor Cyan
    
    return $HealthPercentage
}

# Call the function
$SystemHealth = Test-TradingSystemHealth -SystemPath $TradingSystemPath

# Arrays and loops
Write-Host "`nWorking with Currency Pairs:" -ForegroundColor Yellow

$MajorPairs = @("EURUSD", "GBPUSD", "USDJPY", "USDCHF", "AUDUSD", "USDCAD", "NZDUSD")
$CrossPairs = @("EURGBP", "EURJPY", "EURCHF", "GBPJPY", "GBPCHF", "CHFJPY")

Write-Host "  Major pairs ($($MajorPairs.Count)):" -ForegroundColor White
foreach ($pair in $MajorPairs) {
    Write-Host "    • $pair" -ForegroundColor Gray
}

Write-Host "  Cross pairs ($($CrossPairs.Count)):" -ForegroundColor White
foreach ($pair in $CrossPairs) {
    Write-Host "    • $pair" -ForegroundColor Gray
}

# Hashtables (like Python dictionaries)
Write-Host "`nParameter Configuration:" -ForegroundColor Yellow

$TradingParameters = @{
    "conservative" = @{
        "StopLoss" = 200
        "TakeProfit" = 400
        "RiskPercent" = 1.0
    }
    "aggressive" = @{
        "StopLoss" = 100
        "TakeProfit" = 200
        "RiskPercent" = 2.0
    }
}

foreach ($strategy in $TradingParameters.Keys) {
    $params = $TradingParameters[$strategy]
    Write-Host "  Strategy: $strategy" -ForegroundColor White
    Write-Host "    Stop Loss: $($params.StopLoss) points" -ForegroundColor Gray
    Write-Host "    Take Profit: $($params.TakeProfit) points" -ForegroundColor Gray
    Write-Host "    Risk: $($params.RiskPercent)%" -ForegroundColor Gray
}

Write-Host "`n=== PowerShell Basics Complete ===" -ForegroundColor Green
```

**Test the PowerShell basics:**
```powershell
cd C:\TradingSystem\Source\PowerShell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\HUEY_P_PS1_basics_01.ps1
```

**12.2 System Monitoring Script (3-4 hours)**

Create: `C:\TradingSystem\Source\PowerShell\HUEY_P_PS1_monitor_system.ps1`

```powershell
# HUEY_P_PS1_monitor_system.ps1
# System monitoring script for trading system

param(
    [string]$LogFile = "C:\TradingSystem\Logs\system_monitor.log",
    [int]$IntervalSeconds = 30,
    [switch]$Continuous
)

$ErrorActionPreference = "Stop"

# Create logs directory if it doesn't exist
$LogDir = Split-Path $LogFile -Parent
if (-not (Test-Path $LogDir)) {
    New-Item -ItemType Directory -Path $LogDir -Force | Out-Null
}

function Write-Log {
    param(
        [string]$Message,
        [string]$Level = "INFO"
    )
    
    $Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $LogEntry = "[$Timestamp] [$Level] $Message"
    
    # Write to console with color
    $Color = switch ($Level) {
        "ERROR" { "Red" }
        "WARN"  { "Yellow" }
        "INFO"  { "White" }
        "SUCCESS" { "Green" }
        default { "White" }
    }
    
    Write-Host $LogEntry -ForegroundColor $Color
    
    # Write to log file
    $LogEntry | Out-File -FilePath $LogFile -Append -Encoding UTF8
}

function Test-MT4Status {
    Write-Log "Checking MetaTrader 4 status..."
    
    # Look for MT4 processes
    $MT4Processes = Get-Process -Name "terminal*" -ErrorAction SilentlyContinue
    
    if ($MT4Processes) {
        foreach ($process in $MT4Processes) {
            $MemoryMB = [math]::Round($process.WorkingSet / 1MB, 2)
            Write-Log "MT4 Process found: PID $($process.Id), Memory: $MemoryMB MB" "SUCCESS"
        }
        return $true
    } else {
        Write-Log "No MT4 processes found" "WARN"
        return $false
    }
}

function Test-PythonServices {
    Write-Log "Checking Python services..."
    
    # Check if Python is available
    try {
        $PythonVersion = & python --version 2>&1
        Write-Log "Python available: $PythonVersion" "SUCCESS"
    } catch {
        Write-Log "Python not available in PATH" "ERROR"
        return $false
    }
    
    # Check for Python processes that might be our trading services
    $PythonProcesses = Get-Process -Name "python*" -ErrorAction SilentlyContinue
    
    if ($PythonProcesses) {
        foreach ($process in $PythonProcesses) {
            $MemoryMB = [math]::Round($process.WorkingSet / 1MB, 2)
            Write-Log "Python process found: PID $($process.Id), Memory: $MemoryMB MB" "INFO"
        }
        return $true
    } else {
        Write-Log "No Python processes found" "WARN"
        return $false
    }
}

function Test-DatabaseStatus {
    Write-Log "Checking database status..."
    
    $DatabasePath = "C:\TradingSystem\Database\trading_system.db"
    
    if (Test-Path $DatabasePath) {
        $DbFile = Get-Item $DatabasePath
        $SizeMB = [math]::Round($DbFile.Length / 1MB, 2)
        $LastModified = $DbFile.LastWriteTime
        
        Write-Log "Database file exists: $SizeMB MB, modified: $LastModified" "SUCCESS"
        
        # Check if database was modified recently (within last hour)
        $TimeDiff = (Get-Date) - $LastModified
        if ($TimeDiff.TotalMinutes -lt 60) {
            Write-Log "Database recently active (last modified $([math]::Round($TimeDiff.TotalMinutes, 1)) minutes ago)" "SUCCESS"
        } else {
            Write-Log "Database not recently modified (last modified $([math]::Round($TimeDiff.TotalHours, 1)) hours ago)" "WARN"
        }
        
        return $true
    } else {
        Write-Log "Database file not found: $DatabasePath" "ERROR"
        return $false
    }
}

function Test-BridgeStatus {
    Write-Log "Checking bridge DLL status..."
    
    $BridgePath = "C:\TradingSystem\Source\CPP\HUEY_P_CPP_simple_bridge.dll"
    
    if (Test-Path $BridgePath) {
        $BridgeFile = Get-Item $BridgePath
        $SizeKB = [math]::Round($BridgeFile.Length / 1KB, 2)
        
        Write-Log "Bridge DLL exists: $SizeKB KB" "SUCCESS"
        
        # Check if DLL is in MT4 Libraries folder
        $MT4LibraryPath = "C:\Users\$env:USERNAME\AppData\Roaming\MetaQuotes\Terminal\*\MQL4\Libraries\HUEY_P_CPP_simple_bridge.dll"
        $MT4DLLs = Get-ChildItem $MT4LibraryPath -ErrorAction SilentlyContinue
        
        if ($MT4DLLs) {
            Write-Log "Bridge DLL found in MT4 Libraries folder" "SUCCESS"
        } else {
            Write-Log "Bridge DLL not found in MT4 Libraries folder" "WARN"
        }
        
        return $true
    } else {
        Write-Log "Bridge DLL not found: $BridgePath" "ERROR"
        return $false
    }
}

function Test-ConfigurationFiles {
    Write-Log "Checking configuration files..."
    
    $ConfigDir = "C:\TradingSystem\Config"
    $RequiredConfigs = @(
        "HUEY_P_CSV_parameter_sets.csv",
        "HUEY_P_YAML_system_config.yaml"
    )
    
    $ConfigsFound = 0
    
    foreach ($config in $RequiredConfigs) {
        $ConfigPath = Join-Path $ConfigDir $config
        if (Test-Path $ConfigPath) {
            Write-Log "Configuration file found: $config" "SUCCESS"
            $ConfigsFound++
        } else {
            Write-Log "Configuration file missing: $config" "WARN"
        }
    }
    
    return ($ConfigsFound -eq $RequiredConfigs.Count)
}

function Get-SystemPerformance {
    Write-Log "Checking system performance..."
    
    # CPU usage
    $CPU = Get-Counter "\Processor(_Total)\% Processor Time" -SampleInterval 1 -MaxSamples 3
    $CPUAverage = ($CPU.CounterSamples | Measure-Object CookedValue -Average).Average
    $CPUPercent = [math]::Round($CPUAverage, 2)
    
    # Memory usage
    $Memory = Get-CimInstance Win32_OperatingSystem
    $TotalMemoryGB = [math]::Round($Memory.TotalVisibleMemorySize / 1MB, 2)
    $FreeMemoryGB = [math]::Round($Memory.FreePhysicalMemory / 1MB, 2)
    $UsedMemoryGB = $TotalMemoryGB - $FreeMemoryGB
    $MemoryPercent = [math]::Round(($UsedMemoryGB / $TotalMemoryGB) * 100, 2)
    
    # Disk space
    $Disk = Get-CimInstance Win32_LogicalDisk -Filter "DeviceID='C:'"
    $TotalSpaceGB = [math]::Round($Disk.Size / 1GB, 2)
    $FreeSpaceGB = [math]::Round($Disk.FreeSpace / 1GB, 2)
    $UsedSpaceGB = $TotalSpaceGB - $FreeSpaceGB
    $DiskPercent = [math]::Round(($UsedSpaceGB / $TotalSpaceGB) * 100, 2)
    
    Write-Log "CPU Usage: $CPUPercent%" "INFO"
    Write-Log "Memory Usage: $UsedMemoryGB GB / $TotalMemoryGB GB ($MemoryPercent%)" "INFO"
    Write-Log "Disk Usage: $UsedSpaceGB GB / $TotalSpaceGB GB ($DiskPercent%)" "INFO"
    
    # Alert on high usage
    if ($CPUPercent -gt 80) {
        Write-Log "HIGH CPU USAGE DETECTED: $CPUPercent%" "WARN"
    }
    if ($MemoryPercent -gt 80) {
        Write-Log "HIGH MEMORY USAGE DETECTED: $MemoryPercent%" "WARN"
    }
    if ($DiskPercent -gt 90) {
        Write-Log "LOW DISK SPACE WARNING: $DiskPercent% used" "WARN"
    }
}

function Invoke-SystemCheck {
    Write-Log "=== Starting Trading System Health Check ===" "INFO"
    
    $OverallHealth = @{
        "MT4" = Test-MT4Status
        "Python" = Test-PythonServices
        "Database" = Test-DatabaseStatus
        "Bridge" = Test-BridgeStatus
        "Configuration" = Test-ConfigurationFiles
    }
    
    Get-SystemPerformance
    
    # Calculate overall health score
    $HealthyComponents = ($OverallHealth.Values | Where-Object { $_ -eq $true }).Count
    $TotalComponents = $OverallHealth.Count
    $HealthPercent = [math]::Round(($HealthyComponents / $TotalComponents) * 100, 2)
    
    Write-Log "=== Health Check Summary ===" "INFO"
    Write-Log "Healthy Components: $HealthyComponents / $TotalComponents ($HealthPercent%)" "INFO"
    
    foreach ($component in $OverallHealth.Keys) {
        $status = if ($OverallHealth[$component]) { "✓ HEALTHY" } else { "✗ ISSUES" }
        $level = if ($OverallHealth[$component]) { "SUCCESS" } else { "WARN" }
        Write-Log "$component : $status" $level
    }
    
    if ($HealthPercent -ge 80) {
        Write-Log "Overall system status: HEALTHY" "SUCCESS"
    } elseif ($HealthPercent -ge 60) {
        Write-Log "Overall system status: DEGRADED" "WARN"
    } else {
        Write-Log "Overall system status: CRITICAL" "ERROR"
    }
    
    Write-Log "=== Health Check Complete ===" "INFO"
    
    return $HealthPercent
}

# Main execution
Write-Log "Trading System Monitor started" "INFO"
Write-Log "Log file: $LogFile" "INFO"

if ($Continuous) {
    Write-Log "Running in continuous mode (every $IntervalSeconds seconds)" "INFO"
    Write-Log "Press Ctrl+C to stop" "INFO"
    
    try {
        while ($true) {
            Invoke-SystemCheck | Out-Null
            Start-Sleep -Seconds $IntervalSeconds
        }
    } catch [System.Management.Automation.PipelineStoppedException] {
        Write-Log "Monitor stopped by user" "INFO"
    }
} else {
    $HealthScore = Invoke-SystemCheck
    Write-Log "Single health check complete. Health score: $HealthScore%" "INFO"
}
```

**Test the monitoring script:**
```powershell
# Single check
.\HUEY_P_PS1_monitor_system.ps1

# Continuous monitoring (stop with Ctrl+C)
.\HUEY_P_PS1_monitor_system.ps1 -Continuous -IntervalSeconds 60
```

**12.3 Deployment Automation Script (2-3 hours)**

Create: `C:\TradingSystem\Source\PowerShell\HUEY_P_PS1_deploy_system.ps1`

```powershell
# HUEY_P_PS1_deploy_system.ps1
# Deployment automation script for trading system

param(
    [ValidateSet("Development", "Testing", "Production")]
    [string]$Environment = "Development",
    
    [switch]$SkipBackup,
    [switch]$Force,
    [switch]$ValidateOnly
)

$ErrorActionPreference = "Stop"

# Configuration
$SystemRoot = "C:\TradingSystem"
$MT4DataPath = "$env:APPDATA\MetaQuotes\Terminal"
$BackupPath = "$SystemRoot\Backups\$(Get-Date -Format 'yyyyMMdd_HHmmss')"

function Write-DeployLog {
    param(
        [string]$Message,
        [string]$Level = "INFO"
    )
    
    $Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $LogEntry = "[$Timestamp] [$Level] $Message"
    
    $Color = switch ($Level) {
        "ERROR" { "Red" }
        "WARN"  { "Yellow" }
        "INFO"  { "White" }
        "SUCCESS" { "Green" }
        "STEP" { "Cyan" }
        default { "White" }
    }
    
    Write-Host $LogEntry -ForegroundColor $Color
}

function Test-Prerequisites {
    Write-DeployLog "Checking deployment prerequisites..." "STEP"
    
    $Prerequisites = @{
        "SystemRoot" = $SystemRoot
        "MT4DataPath" = $MT4DataPath
        "PythonAvailable" = $null
        "BridgeDLL" = "$SystemRoot\Source\CPP\HUEY_P_CPP_simple_bridge.dll"
    }
    
    $AllGood = $true
    
    # Check system root
    if (-not (Test-Path $SystemRoot)) {
        Write-DeployLog "System root directory not found: $SystemRoot" "ERROR"
        $AllGood = $false
    } else {
        Write-DeployLog "System root found" "SUCCESS"
    }
    
    # Check MT4 data path
    if (-not (Test-Path $MT4DataPath)) {
        Write-DeployLog "MT4 data directory not found: $MT4DataPath" "ERROR"
        $AllGood = $false
    } else {
        Write-DeployLog "MT4 data directory found" "SUCCESS"
    }
    
    # Check Python
    try {
        $PythonVersion = & python --version 2>&1
        Write-DeployLog "Python available: $PythonVersion" "SUCCESS"
    } catch {
        Write-DeployLog "Python not available in PATH" "ERROR"
        $AllGood = $false
    }
    
    # Check bridge DLL
    if (-not (Test-Path $Prerequisites["BridgeDLL"])) {
        Write-DeployLog "Bridge DLL not found: $($Prerequisites['BridgeDLL'])" "ERROR"
        $AllGood = $false
    } else {
        Write-DeployLog "Bridge DLL found" "SUCCESS"
    }
    
    return $AllGood
}

function Backup-CurrentSystem {
    if ($SkipBackup) {
        Write-DeployLog "Skipping backup (SkipBackup flag set)" "WARN"
        return $true
    }
    
    Write-DeployLog "Creating system backup..." "STEP"
    
    try {
        # Create backup directory
        New-Item -ItemType Directory -Path $BackupPath -Force | Out-Null
        Write-DeployLog "Backup directory created: $BackupPath" "INFO"
        
        # Backup critical directories
        $BackupItems = @{
            "Config" = "$SystemRoot\Config"
            "Database" = "$SystemRoot\Database"
            "Source" = "$SystemRoot\Source"
        }
        
        foreach ($item in $BackupItems.Keys) {
            $SourcePath = $BackupItems[$item]
            $DestPath = Join-Path $BackupPath $item
            
            if (Test-Path $SourcePath) {
                Copy-Item -Path $SourcePath -Destination $DestPath -Recurse -Force
                Write-DeployLog "Backed up: $item" "SUCCESS"
            } else {
                Write-DeployLog "Backup source not found: $SourcePath" "WARN"
            }
        }
        
        # Create backup manifest
        $BackupManifest = @{
            "Timestamp" = Get-Date
            "Environment" = $Environment
            "SystemVersion" = "1.0.0"
            "BackupPath" = $BackupPath
        }
        
        $BackupManifest | ConvertTo-Json | Out-File -FilePath (Join-Path $BackupPath "backup_manifest.json")
        
        Write-DeployLog "Backup completed successfully" "SUCCESS"
        return $true
        
    } catch {
        Write-DeployLog "Backup failed: $($_.Exception.Message)" "ERROR"
        return $false
    }
}

function Deploy-BridgeDLL {
    Write-DeployLog "Deploying bridge DLL..." "STEP"
    
    $SourceDLL = "$SystemRoot\Source\CPP\HUEY_P_CPP_simple_bridge.dll"
    
    if (-not (Test-Path $SourceDLL)) {
        Write-DeployLog "Source DLL not found: $SourceDLL" "ERROR"
        return $false
    }
    
    # Find MT4 terminal directories
    $TerminalDirs = Get-ChildItem -Path $MT4DataPath -Directory | Where-Object { $_.Name -match "^[A-F0-9]{32}$" }
    
    if (-not $TerminalDirs) {
        Write-DeployLog "No MT4 terminal directories found in $MT4DataPath" "ERROR"
        return $false
    }
    
    $Deployed = 0
    
    foreach ($terminalDir in $TerminalDirs) {
        $LibrariesPath = Join-Path $terminalDir.FullName "MQL4\Libraries"
        
        if (Test-Path $LibrariesPath) {
            $DestPath = Join-Path $LibrariesPath "HUEY_P_CPP_simple_bridge.dll"
            
            try {
                Copy-Item -Path $SourceDLL -Destination $DestPath -Force
                Write-DeployLog "DLL deployed to: $($terminalDir.Name)" "SUCCESS"
                $Deployed++
            } catch {
                Write-DeployLog "Failed to deploy DLL to: $($terminalDir.Name) - $($_.Exception.Message)" "ERROR"
            }
        }
    }
    
    if ($Deployed -gt 0) {
        Write-DeployLog "Bridge DLL deployed to $Deployed terminal(s)" "SUCCESS"
        return $true
    } else {
        Write-DeployLog "Failed to deploy bridge DLL to any terminals" "ERROR"
        return $false
    }
}

function Deploy-MQL4Files {
    Write-DeployLog "Deploying MQL4 files..." "STEP"
    
    $SourceInclude = "$SystemRoot\Source\MQL4"
    
    if (-not (Test-Path $SourceInclude)) {
        Write-DeployLog "MQL4 source directory not found: $SourceInclude" "WARN"
        return $true  # Not critical for basic deployment
    }
    
    # Find terminal directories
    $TerminalDirs = Get-ChildItem -Path $MT4DataPath -Directory | Where-Object { $_.Name -match "^[A-F0-9]{32}$" }
    
    $Deployed = 0
    
    foreach ($terminalDir in $TerminalDirs) {
        $MQL4Path = Join-Path $terminalDir.FullName "MQL4"
        
        if (Test-Path $MQL4Path) {
            # Deploy .mqh files to Include directory
            $IncludeFiles = Get-ChildItem -Path $SourceInclude -Filter "*.mqh" -ErrorAction SilentlyContinue
            if ($IncludeFiles) {
                $IncludePath = Join-Path $MQL4Path "Include"
                foreach ($file in $IncludeFiles) {
                    try {
                        Copy-Item -Path $file.FullName -Destination $IncludePath -Force
                        Write-DeployLog "Deployed include file: $($file.Name)" "SUCCESS"
                    } catch {
                        Write-DeployLog "Failed to deploy include file: $($file.Name)" "ERROR"
                    }
                }
            }
            
            # Deploy .mq4 files to Experts directory
            $ExpertFiles = Get-ChildItem -Path $SourceInclude -Filter "*.mq4" -ErrorAction SilentlyContinue
            if ($ExpertFiles) {
                $ExpertsPath = Join-Path $MQL4Path "Experts"
                foreach ($file in $ExpertFiles) {
                    try {
                        Copy-Item -Path $file.FullName -Destination $ExpertsPath -Force
                        Write-DeployLog "Deployed expert file: $($file.Name)" "SUCCESS"
                    } catch {
                        Write-DeployLog "Failed to deploy expert file: $($file.Name)" "ERROR"
                    }
                }
            }
            
            $Deployed++
        }
    }
    
    Write-DeployLog "MQL4 files deployed to $Deployed terminal(s)" "SUCCESS"
    return $true
}

function Deploy-ConfigurationFiles {
    Write-DeployLog "Deploying configuration files..." "STEP"
    
    $ConfigSource = "$SystemRoot\Config"
    
    if (-not (Test-Path $ConfigSource)) {
        Write-DeployLog "Configuration directory not found: $ConfigSource" "ERROR"
        return $false
    }
    
    # Find terminal directories
    $TerminalDirs = Get-ChildItem -Path $MT4DataPath -Directory | Where-Object { $_.Name -match "^[A-F0-9]{32}$" }
    
    $Deployed = 0
    
    foreach ($terminalDir in $TerminalDirs) {
        $FilesPath = Join-Path $terminalDir.FullName "MQL4\Files"
        
        if (Test-Path $FilesPath) {
            # Deploy CSV configuration files
            $CSVFiles = Get-ChildItem -Path $ConfigSource -Filter "*.csv" -Recurse
            
            foreach ($csvFile in $CSVFiles) {
                try {
                    Copy-Item -Path $csvFile.FullName -Destination $FilesPath -Force
                    Write-DeployLog "Deployed config file: $($csvFile.Name)" "SUCCESS"
                } catch {
                    Write-DeployLog "Failed to deploy config file: $($csvFile.Name)" "ERROR"
                }
            }
            
            $Deployed++
        }
    }
    
    Write-DeployLog "Configuration files deployed to $Deployed terminal(s)" "SUCCESS"
    return $true
}

function Install-PythonDependencies {
    Write-DeployLog "Installing Python dependencies..." "STEP"
    
    $RequirementsFile = "$SystemRoot\requirements.txt"
    
    if (-not (Test-Path $RequirementsFile)) {
        Write-DeployLog "Requirements file not found: $RequirementsFile" "WARN"
        return $true  # Not critical
    }
    
    try {
        Write-DeployLog "Installing packages from requirements.txt..." "INFO"
        & pip install -r $RequirementsFile
        Write-DeployLog "Python dependencies installed successfully" "SUCCESS"
        return $true
    } catch {
        Write-DeployLog "Failed to install Python dependencies: $($_.Exception.Message)" "ERROR"
        return $false
    }
}

function Start-Services {
    Write-DeployLog "Starting trading system services..." "STEP"
    
    # For now, just validate that we can start Python scripts
    $PythonTestScript = "$SystemRoot\Source\Python\HUEY_P_PY_test_bridge.py"
    
    if (Test-Path $PythonTestScript) {
        Write-DeployLog "Python test script found - services can be started manually" "SUCCESS"
    } else {
        Write-DeployLog "Python test script not found" "WARN"
    }
    
    # Check if MT4 is running
    $MT4Process = Get-Process -Name "terminal*" -ErrorAction SilentlyContinue
    if ($MT4Process) {
        Write-DeployLog "MT4 is running - EAs can be attached manually" "SUCCESS"
    } else {
        Write-DeployLog "MT4 is not running - start MT4 and attach EAs manually" "INFO"
    }
    
    return $true
}

function Invoke-PostDeploymentValidation {
    Write-DeployLog "Running post-deployment validation..." "STEP"
    
    # Check deployed files
    $ValidationResults = @{}
    
    # Check if bridge DLL was deployed
    $TerminalDirs = Get-ChildItem -Path $MT4DataPath -Directory | Where-Object { $_.Name -match "^[A-F0-9]{32}$" }
    $BridgeDLLFound = $false
    
    foreach ($terminalDir in $TerminalDirs) {
        $DLLPath = Join-Path $terminalDir.FullName "MQL4\Libraries\HUEY_P_CPP_simple_bridge.dll"
        if (Test-Path $DLLPath) {
            $BridgeDLLFound = $true
            break
        }
    }
    
    $ValidationResults["BridgeDLL"] = $BridgeDLLFound
    
    # Check configuration files
    $ConfigFileFound = $false
    foreach ($terminalDir in $TerminalDirs) {
        $ConfigPath = Join-Path $terminalDir.FullName "MQL4\Files\HUEY_P_CSV_parameter_sets.csv"
        if (Test-Path $ConfigPath) {
            $ConfigFileFound = $true
            break
        }
    }
    
    $ValidationResults["ConfigFiles"] = $ConfigFileFound
    
    # Report validation results
    foreach ($check in $ValidationResults.Keys) {
        $status = if ($ValidationResults[$check]) { "✓ PASS" } else { "✗ FAIL" }
        $level = if ($ValidationResults[$check]) { "SUCCESS" } else { "ERROR" }
        Write-DeployLog "Validation - $check : $status" $level
    }
    
    $PassedChecks = ($ValidationResults.Values | Where-Object { $_ -eq $true }).Count
    $TotalChecks = $ValidationResults.Count
    
    Write-DeployLog "Validation Results: $PassedChecks/$TotalChecks checks passed" "INFO"
    
    return ($PassedChecks -eq $TotalChecks)
}

# Main deployment process
function Invoke-Deployment {
    Write-DeployLog "=== HUEY_P Trading System Deployment ===" "STEP"
    Write-DeployLog "Environment: $Environment" "INFO"
    Write-DeployLog "Validation Only: $ValidateOnly" "INFO"
    
    # Step 1: Check prerequisites
    if (-not (Test-Prerequisites)) {
        Write-DeployLog "Prerequisites check failed - aborting deployment" "ERROR"
        return $false
    }
    
    if ($ValidateOnly) {
        Write-DeployLog "Validation complete - no deployment performed" "INFO"
        return $true
    }
    
    # Step 2: Backup current system
    if (-not (Backup-CurrentSystem)) {
        if (-not $Force) {
            Write-DeployLog "Backup failed and Force flag not set - aborting deployment" "ERROR"
            return $false
        } else {
            Write-DeployLog "Backup failed but Force flag set - continuing deployment" "WARN"
        }
    }
    
    # Step 3: Deploy bridge DLL
    if (-not (Deploy-BridgeDLL)) {
        Write-DeployLog "Bridge DLL deployment failed" "ERROR"
        return $false
    }
    
    # Step 4: Deploy MQL4 files
    if (-not (Deploy-MQL4Files)) {
        Write-DeployLog "MQL4 files deployment failed" "ERROR"
        return $false
    }
    
    # Step 5: Deploy configuration files
    if (-not (Deploy-ConfigurationFiles)) {
        Write-DeployLog "Configuration files deployment failed" "ERROR"
        return $false
    }
    
    # Step 6: Install Python dependencies
    if (-not (Install-PythonDependencies)) {
        Write-DeployLog "Python dependencies installation failed" "ERROR"
        return $false
    }
    
    # Step 7: Start services
    if (-not (Start-Services)) {
        Write-DeployLog "Services startup failed" "ERROR"
        return $false
    }
    
    # Step 8: Post-deployment validation
    if (-not (Invoke-PostDeploymentValidation)) {
        Write-DeployLog "Post-deployment validation failed" "ERROR"
        return $false
    }
    
    Write-DeployLog "=== Deployment Completed Successfully ===" "SUCCESS"
    Write-DeployLog "Backup location: $BackupPath" "INFO"
    Write-DeployLog "Next steps:" "INFO"
    Write-DeployLog "  1. Start MT4 terminal" "INFO"
    Write-DeployLog "  2. Attach HUEY_P_MQL4_bridge_test EA to a chart" "INFO"
    Write-DeployLog "  3. Run: python HUEY_P_PY_test_bridge.py" "INFO"
    
    return $true
}

# Execute deployment
$DeploymentSuccess = Invoke-Deployment

if ($DeploymentSuccess) {
    exit 0
} else {
    exit 1
}
```

**Test the deployment script:**
```powershell
# Validate prerequisites only
.\HUEY_P_PS1_deploy_system.ps1 -ValidateOnly

# Full deployment to development
.\HUEY_P_PS1_deploy_system.ps1 -Environment Development
```

---

## **PHASE 2: BASIC INTEGRATION (Week 9-12)**
*Estimated Time: 40-50 hours*

### **Week 9-10: Simple Signal System (15-20 hours)**

#### **Day 36-40: Create Your First Signal Generator (15-20 hours)**

**Learning Objective**: Build a complete signal generation and execution pipeline.

**Step 13: Simple Python Signal Generator**

**13.1 Create Basic Signal Service (6-8 hours)**

Create: `C:\TradingSystem\Source\Python\HUEY_P_PY_signal_service_basic.py`

```python
# HUEY_P_PY_signal_service_basic.py
# Basic signal generation service for trading system

import time
import random
import ctypes
import os
import threading
import signal
import sys
from datetime import datetime, timedelta
import json

class TradingSignalGenerator:
    def __init__(self):
        self.bridge = None
        self.running = False
        self.signal_count = 0
        self.bridge_dll_path = r"C:\TradingSystem\Source\CPP\HUEY_P_CPP_simple_bridge.dll"
        
        # Trading parameters
        self.currency_pairs = ["EURUSD", "GBPUSD", "USDJPY"]
        self.signal_strategies = {
            "trend_following": {"confidence_range": (0.7, 0.9), "sl": 50, "tp": 100},
            "momentum": {"confidence_range": (0.6, 0.8), "sl": 40, "tp": 80},
            "reversal": {"confidence_range": (0.75, 0.95), "sl": 60, "tp": 120}
        }
        
        # Signal generation settings
        self.min_signal_interval = 30  # Minimum seconds between signals for same pair
        self.last_signal_time = {}  # Track last signal time per pair
        
        print("TradingSignalGenerator initialized")
        print(f"Currency pairs: {self.currency_pairs}")
        print(f"Strategies: {list(self.signal_strategies.keys())}")
    
    def load_bridge_dll(self):
        """Load the C++ bridge DLL"""
        if not os.path.exists(self.bridge_dll_path):
            print(f"ERROR: Bridge DLL not found at {self.bridge_dll_path}")
            print("Make sure you compiled the C++ bridge and it's in the correct location")
            return False
        
        try:
            # Load the DLL
            self.bridge = ctypes.CDLL(self.bridge_dll_path)
            
            # Define function signatures
            self.bridge.InitializeBridge.restype = ctypes.c_int
            self.bridge.InitializeBridge.argtypes = []
            
            self.bridge.ShutdownBridge.restype = None
            self.bridge.ShutdownBridge.argtypes = []
            
            self.bridge.AddMessage.restype = ctypes.c_int
            self.bridge.AddMessage.argtypes = [ctypes.c_char_p, ctypes.c_char_p, 
                                              ctypes.c_double, ctypes.c_int, ctypes.c_int]
            
            self.bridge.GetMessageCount.restype = ctypes.c_int
            self.bridge.GetMessageCount.argtypes = []
            
            self.bridge.GetBridgeStatus.restype = ctypes.c_int
            self.bridge.GetBridgeStatus.argtypes = []
            
            print("✓ Bridge DLL loaded successfully")
            return True
            
        except Exception as e:
            print(f"ERROR loading bridge DLL: {e}")
            return False
    
    def initialize_bridge(self):
        """Initialize the bridge connection"""
        if not self.bridge:
            return False
        
        try:
            result = self.bridge.InitializeBridge()
            if result == 1:
                print("✓ Bridge initialized successfully")
                return True
            else:
                print(f"✗ Bridge initialization failed (result: {result})")
                return False
        except Exception as e:
            print(f"ERROR initializing bridge: {e}")
            return False
    
    def shutdown_bridge(self):
        """Shutdown the bridge connection"""
        if self.bridge:
            try:
                self.bridge.ShutdownBridge()
                print("✓ Bridge shutdown complete")
            except Exception as e:
                print(f"ERROR shutting down bridge: {e}")
    
    def generate_signal(self):
        """Generate a random trading signal (simulating ML model output)"""
        # Select random currency pair
        pair = random.choice(self.currency_pairs)
        
        # Check if enough time has passed since last signal for this pair
        current_time = datetime.now()
        if pair in self.last_signal_time:
            time_diff = (current_time - self.last_signal_time[pair]).total_seconds()
            if time_diff < self.min_signal_interval:
                return None  # Too soon for another signal
        
        # Select random strategy
        strategy_name = random.choice(list(self.signal_strategies.keys()))
        strategy = self.signal_strategies[strategy_name]
        
        # Generate random signal parameters
        direction = random.choice(["BUY", "SELL"])
        confidence_min, confidence_max = strategy["confidence_range"]
        confidence = round(random.uniform(confidence_min, confidence_max), 2)
        
        # Add some realistic variation to stops
        sl_base = strategy["sl"]
        tp_base = strategy["tp"]
        sl = sl_base + random.randint(-10, 10)  # ±10 points variation
        tp = tp_base + random.randint(-20, 20)  # ±20 points variation
        
        signal = {
            "pair": pair,
            "direction": direction,
            "confidence": confidence,
            "stop_loss": sl,
            "take_profit": tp,
            "strategy": strategy_name,
            "timestamp": current_time.isoformat()
        }
        
        # Update last signal time for this pair
        self.last_signal_time[pair] = current_time
        
        return signal
    
    def send_signal_to_bridge(self, signal):
        """Send signal to the bridge for MT4 to receive"""
        if not self.bridge:
            print("ERROR: Bridge not initialized")
            return False
        
        try:
            result = self.bridge.AddMessage(
                signal["pair"].encode('utf-8'),
                signal["direction"].encode('utf-8'),
                signal["confidence"],
                signal["stop_loss"],
                signal["take_profit"]
            )
            
            if result == 1:
                self.signal_count += 1
                print(f"✓ Signal #{self.signal_count} sent: {signal['pair']} {signal['direction']} "
                      f"(confidence: {signal['confidence']}, strategy: {signal['strategy']})")
                return True
            else:
                print(f"✗ Failed to send signal (result: {result})")
                return False
                
        except Exception as e:
            print(f"ERROR sending signal: {e}")
            return False
    
    def get_bridge_status(self):
        """Get current bridge status information"""
        if not self.bridge:
            return {"status": "disconnected", "message_count": 0}
        
        try:
            status = self.bridge.GetBridgeStatus()
            message_count = self.bridge.GetMessageCount()
            
            return {
                "status": "connected" if status == 1 else "disconnected",
                "message_count": message_count,
                "bridge_status_code": status
            }
        except Exception as e:
            print(f"ERROR getting bridge status: {e}")
            return {"status": "error", "message_count": 0}
    
    def print_status(self):
        """Print current service status"""
        bridge_status = self.get_bridge_status()
        
        print(f"\n=== Signal Service Status ===")
        print(f"Running: {self.running}")
        print(f"Total signals sent: {self.signal_count}")
        print(f"Bridge status: {bridge_status['status']}")
        print(f"Messages in queue: {bridge_status['message_count']}")
        print(f"Active pairs: {len(self.currency_pairs)}")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 29)
    
    def signal_handler(self, signum, frame):
        """Handle Ctrl+C gracefully"""
        print("\nReceived stop signal. Shutting down gracefully...")
        self.running = False
    
    def run_continuous(self, signal_interval=60, status_interval=300):
        """Run the signal generator continuously"""
        print(f"\n=== Starting Continuous Signal Generation ===")
        print(f"Signal interval: {signal_interval} seconds")
        print(f"Status update interval: {status_interval} seconds")
        print("Press Ctrl+C to stop\n")
        
        # Set up signal handler for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        
        self.running = True
        last_status_time = time.time()
        
        try:
            while self.running:
                current_time = time.time()
                
                # Generate and send signal
                trading_signal = self.generate_signal()
                if trading_signal:
                    success = self.send_signal_to_bridge(trading_signal)
                    if not success:
                        print("Warning: Failed to send signal to bridge")
                
                # Print status update periodically
                if current_time - last_status_time >= status_interval:
                    self.print_status()
                    last_status_time = current_time
                
                # Wait for next signal
                time.sleep(signal_interval)
                
        except KeyboardInterrupt:
            print("\nStopping signal generation...")
        
        self.running = False
        print("Signal generation stopped")
    
    def run_demo_mode(self, num_signals=10, interval=10):
        """Run in demo mode - send a fixed number of signals"""
        print(f"\n=== Demo Mode: Sending {num_signals} signals ===")
        print(f"Interval: {interval} seconds between signals\n")
        
        for i in range(num_signals):
            print(f"Generating signal {i+1}/{num_signals}...")
            
            signal_data = self.generate_signal()
            if signal_data:
                success = self.send_signal_to_bridge(signal_data)
                if success:
                    print(f"  Signal sent successfully")
                else:
                    print(f"  Failed to send signal")
            else:
                print(f"  No signal generated (too soon for this pair)")
            
            # Print bridge status
            status = self.get_bridge_status()
            print(f"  Bridge status: {status['status']}, Queue: {status['message_count']} messages")
            
            if i < num_signals - 1:  # Don't sleep after last signal
                print(f"  Waiting {interval} seconds...\n")
                time.sleep(interval)
        
        print(f"\nDemo complete. Total signals sent: {self.signal_count}")

def main():
    print("=== HUEY_P Trading Signal Service ===")
    
    # Create signal generator
    generator = TradingSignalGenerator()
    
    # Load and initialize bridge
    if not generator.load_bridge_dll():
        print("Failed to load bridge DLL. Exiting.")
        return
    
    if not generator.initialize_bridge():
        print("Failed to initialize bridge. Exiting.")
        return
    
    # Menu system
    while True:
        print("\nSignal Service Options:")
        print("1. Run continuous signal generation")
        print("2. Run demo mode (10 signals)")
        print("3. Send single test signal")
        print("4. Check bridge status")
        print("5. Exit")
        
        choice = input("Enter choice (1-5): ").strip()
        
        if choice == "1":
            try:
                interval = int(input("Signal interval in seconds (default 60): ") or "60")
                generator.run_continuous(signal_interval=interval)
            except ValueError:
                print("Invalid interval. Using default of 60 seconds.")
                generator.run_continuous()
        
        elif choice == "2":
            generator.run_demo_mode()
        
        elif choice == "3":
            signal_data = generator.generate_signal()
            if signal_data:
                print(f"Generated signal: {signal_data}")
                success = generator.send_signal_to_bridge(signal_data)
                print(f"Send result: {'Success' if success else 'Failed'}")
            else:
                print("No signal generated (may be too soon for any pair)")
        
        elif choice == "4":
            generator.print_status()
        
        elif choice == "5":
            break
        
        else:
            print("Invalid choice. Please enter 1-5.")
    
    # Cleanup
    generator.shutdown_bridge()
    print("Signal service stopped.")

if __name__ == "__main__":
    main()
```

**Test the signal service:**
```powershell
cd C:\TradingSystem\Source\Python
python HUEY_P_PY_signal_service_basic.py
# Choose option 2 for demo mode first
```

**13.2 Create Advanced EA for Signal Processing (4-6 hours)**

Create: `C:\TradingSystem\Source\MQL4\HUEY_P_MQL4_signal_processor.mq4`

```mql4
//+------------------------------------------------------------------+
//| HUEY_P_MQL4_signal_processor.mq4                                |
//| Advanced EA for processing signals from Python service          |
//+------------------------------------------------------------------+
#property copyright "Trading System Beginner"
#property version   "1.00"
#property strict

// Include our configuration reader
#include <HUEY_P_MQH_config_reader.mqh>

// DLL imports
#import "HUEY_P_CPP_simple_bridge.dll"
   int InitializeBridge();
   void ShutdownBridge();
   int GetNextMessage(string &symbol, string &command, double &confidence, int &stopLoss, int &takeProfit);
   int GetMessageCount();
   int GetBridgeStatus();
#import

// Input parameters
input string ConfigFile = "HUEY_P_CSV_parameter_sets.csv";
input string DefaultStrategy = "moderate";
input int MagicNumber = 13001;
input int MaxOpenTrades = 1;
input double MinConfidence = 0.70;
input int MaxSpreadPoints = 5;
input bool EnableTrading = false;  // Safety switch - set to true to enable real trading
input int SignalCheckInterval = 5; // Seconds between signal checks

// Global variables
bool g_bridgeInitialized = false;
datetime g_lastSignalCheck = 0;
int g_totalSignalsReceived = 0;
int g_totalSignalsProcessed = 0;
int g_totalTradesOpened = 0;

// Configuration
ParameterSet g_parameterSets[50];
int g_parameterCount = 0;
ParameterSet g_defaultParams;

// Signal statistics
struct SignalStats {
    string pair;
    int received;
    int processed;
    int trades_opened;
    datetime last_signal;
};

SignalStats g_signalStats[10]; // Track stats for up to 10 pairs
int g_statsCount = 0;

//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
{
    Print("=== Signal Processor EA Starting ===");
    Print("Symbol: ", Symbol());
    Print("Config file: ", ConfigFile);
    Print("Default strategy: ", DefaultStrategy);
    Print("Magic number: ", MagicNumber);
    Print("Trading enabled: ", (EnableTrading ? "YES" : "NO - SIMULATION ONLY"));
    
    // Load parameter sets
    if(!LoadParameterConfiguration())
    {
        Print("ERROR: Failed to load parameter configuration");
        return INIT_FAILED;
    }
    
    // Initialize bridge
    if(!InitializeTradingBridge())
    {
        Print("ERROR: Failed to initialize trading bridge");
        return INIT_FAILED;
    }
    
    // Initialize signal statistics
    InitializeSignalStats();
    
    Print("Signal Processor EA initialized successfully");
    PrintCurrentConfiguration();
    
    return INIT_SUCCEEDED;
}

//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
{
    Print("=== Signal Processor EA Stopping ===");
    PrintFinalStatistics();
    
    if(g_bridgeInitialized)
    {
        ShutdownBridge();
        Print("Bridge connection closed");
    }
}

//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
{
    // Check for signals periodically, not on every tick
    if(TimeCurrent() - g_lastSignalCheck >= SignalCheckInterval)
    {
        CheckAndProcessSignals();
        g_lastSignalCheck = TimeCurrent();
    }
}

//+------------------------------------------------------------------+
//| Load parameter configuration                                     |
//+------------------------------------------------------------------+
bool LoadParameterConfiguration()
{
    Print("Loading parameter configuration...");
    
    // Create sample file if it doesn't exist
    if(!FileIsExist(ConfigFile, FILE_COMMON))
    {
        Print("Parameter file not found. Creating sample file...");
        if(!CreateSampleParameterFile(ConfigFile))
        {
            return false;
        }
    }
    
    // Load parameters
    if(!ReadParameterSets(ConfigFile, g_parameterSets, g_parameterCount))
    {
        return false;
    }
    
    // Find default strategy
    if(!FindParameterSet(DefaultStrategy, g_parameterSets, g_parameterCount, g_defaultParams))
    {
        Print("Default strategy not found, using first available");
        if(g_parameterCount > 0)
        {
            g_defaultParams = g_parameterSets[0];
        }
        else
        {
            return false;
        }
    }
    
    Print("Default parameters loaded:");
    PrintParameterSet(g_defaultParams);
    
    return true;
}

//+------------------------------------------------------------------+
//| Initialize trading bridge                                        |
//+------------------------------------------------------------------+
bool InitializeTradingBridge()
{
    Print("Initializing trading bridge...");
    
    int result = InitializeBridge();
    if(result == 1)
    {
        g_bridgeInitialized = true;
        Print("Bridge initialized successfully");
        
        // Check initial status
        int status = GetBridgeStatus();
        int messageCount = GetMessageCount();
        Print("Bridge status: ", status, ", Initial messages: ", messageCount);
        
        return true;
    }
    else
    {
        Print("Bridge initialization failed. Result: ", result);
        return false;
    }
}

//+------------------------------------------------------------------+
//| Initialize signal statistics tracking                            |
//+------------------------------------------------------------------+
void InitializeSignalStats()
{
    // Initialize stats for common pairs
    string commonPairs[] = {"EURUSD", "GBPUSD", "USDJPY", "USDCHF", "AUDUSD", "USDCAD", "NZDUSD"};
    
    for(int i = 0; i < ArraySize(commonPairs) && i < 10; i++)
    {
        g_signalStats[i].pair = commonPairs[i];
        g_signalStats[i].received = 0;
        g_signalStats[i].processed = 0;
        g_signalStats[i].trades_opened = 0;
        g_signalStats[i].last_signal = 0;
        g_statsCount++;
    }
}

//+------------------------------------------------------------------+
//| Check for and process incoming signals                           |
//+------------------------------------------------------------------+
void CheckAndProcessSignals()
{
    if(!g_bridgeInitialized)
    {
        return;
    }
    
    int messageCount = GetMessageCount();
    
    // Process all available messages
    while(messageCount > 0)
    {
        ProcessNextSignal();
        messageCount = GetMessageCount();
    }
}

//+------------------------------------------------------------------+
//| Process a single signal from the bridge                          |
//+------------------------------------------------------------------+
void ProcessNextSignal()
{
    string symbol = "";
    string command = "";
    double confidence = 0.0;
    int stopLoss = 0;
    int takeProfit = 0;
    
    // Get the signal
    int result = GetNextMessage(symbol, command, confidence, stopLoss, takeProfit);
    
    if(result != 1)
    {
        return; // No message or error
    }
    
    g_totalSignalsReceived++;
    UpdateSignalStats(symbol, "received");
    
    Print("=== Signal #", g_totalSignalsReceived, " Received ===");
    Print("Symbol: ", symbol);
    Print("Command: ", command);
    Print("Confidence: ", DoubleToString(confidence, 2));
    Print("Stop Loss: ", stopLoss, " points");
    Print("Take Profit: ", takeProfit, " points");
    
    // Only process signals for our symbol
    if(symbol != Symbol())
    {
        Print("Signal for different symbol, ignoring");
        return;
    }
    
    // Process the signal
    bool processed = ProcessTradingSignal(symbol, command, confidence, stopLoss, takeProfit);
    
    if(processed)
    {
        g_totalSignalsProcessed++;
        UpdateSignalStats(symbol, "processed");
    }
}

//+------------------------------------------------------------------+
//| Process a trading signal                                          |
//+------------------------------------------------------------------+
bool ProcessTradingSignal(string symbol, string command, double confidence, int stopLossPoints, int takeProfitPoints)
{
    Print("=== Processing Trading Signal ===");
    
    // Pre-flight checks
    if(!PreTradeValidation(confidence))
    {
        Print("Signal failed pre-trade validation");
        return false;
    }
    
    // Check if we should trade this signal
    if(!ShouldExecuteTrade())
    {
        Print("Trade execution criteria not met");
        return false;
    }
    
    // Calculate lot size using our risk management
    double lotSize = CalculateLotSize(g_defaultParams.riskPercent, stopLossPoints);
    
    Print("Calculated lot size: ", DoubleToString(lotSize, 2));
    
    if(!EnableTrading)
    {
        Print("=== SIMULATION MODE ===");
        SimulateTrade(command, confidence, stopLossPoints, takeProfitPoints, lotSize);
        return true;
    }
    
    // Execute real trade
    bool success = ExecuteRealTrade(command, confidence, stopLossPoints, takeProfitPoints, lotSize);
    
    if(success)
    {
        g_totalTradesOpened++;
        UpdateSignalStats(Symbol(), "trades_opened");
    }
    
    return success;
}

//+------------------------------------------------------------------+
//| Pre-trade validation checks                                      |
//+------------------------------------------------------------------+
bool PreTradeValidation(double confidence)
{
    // Check confidence threshold
    if(confidence < MinConfidence)
    {
        Print("Confidence too low: ", DoubleToString(confidence, 2), " < ", DoubleToString(MinConfidence, 2));
        return false;
    }
    
    // Check trading allowed
    if(!IsTradeAllowed())
    {
        Print("Trading not allowed by broker/EA settings");
        return false;
    }
    
    // Check spread
    double currentSpread = MarketInfo(Symbol(), MODE_SPREAD);
    if(currentSpread > MaxSpreadPoints)
    {
        Print("Spread too high: ", currentSpread, " > ", MaxSpreadPoints);
        return false;
    }
    
    // Check market hours (basic check)
    int dayOfWeek = DayOfWeek();
    if(dayOfWeek == 0 || dayOfWeek == 6) // Weekend
    {
        Print("Weekend - market closed");
        return false;
    }
    
    return true;
}

//+------------------------------------------------------------------+
//| Check if we should execute a trade                               |
//+------------------------------------------------------------------+
bool ShouldExecuteTrade()
{
    // Check maximum open trades
    int openTrades = CountMyOpenTrades();
    if(openTrades >= MaxOpenTrades)
    {
        Print("Maximum open trades reached: ", openTrades, "/", MaxOpenTrades);
        return false;
    }
    
    // Check account equity/margin
    double equity = AccountEquity();
    double margin = AccountMargin();
    double freeMargin = AccountFreeMargin();
    
    if(freeMargin < 100) // Minimum $100 free margin
    {
        Print("Insufficient free margin: $", DoubleToString(freeMargin, 2));
        return false;
    }
    
    return true;
}

//+------------------------------------------------------------------+
//| Execute real trade                                                |
//+------------------------------------------------------------------+
bool ExecuteRealTrade(string command, double confidence, int stopLossPoints, int takeProfitPoints, double lotSize)
{
    int orderType;
    double price, sl, tp;
    color arrowColor;
    
    if(command == "BUY")
    {
        orderType = OP_BUY;
        price = Ask;
        sl = (stopLossPoints > 0) ? price - (stopLossPoints * Point) : 0;
        tp = (takeProfitPoints > 0) ? price + (takeProfitPoints * Point) : 0;
        arrowColor = clrGreen;
    }
    else if(command == "SELL")
    {
        orderType = OP_SELL;
        price = Bid;
        sl = (stopLossPoints > 0) ? price + (stopLossPoints * Point) : 0;
        tp = (takeProfitPoints > 0) ? price - (takeProfitPoints * Point) : 0;
        arrowColor = clrRed;
    }
    else
    {
        Print("Unknown command: ", command);
        return false;
    }
    
    string tradeComment = StringConcatenate("SignalEA-", DoubleToString(confidence, 2));
    
    Print("Executing ", command, " trade:");
    Print("  Price: ", DoubleToString(price, Digits));
    Print("  Lot size: ", DoubleToString(lotSize, 2));
    Print("  Stop loss: ", DoubleToString(sl, Digits));
    Print("  Take profit: ", DoubleToString(tp, Digits));
    
    int ticket = OrderSend(
        Symbol(),
        orderType,
        lotSize,
        price,
        3, // 3 points slippage
        sl,
        tp,
        tradeComment,
        MagicNumber,
        0,
        arrowColor
    );
    
    if(ticket > 0)
    {
        Print("✓ Trade executed successfully. Ticket: ", ticket);
        return true;
    }
    else
    {
        int error = GetLastError();
        Print("✗ Trade execution failed. Error: ", error, " - ", ErrorDescription(error));
        return false;
    }
}

//+------------------------------------------------------------------+
//| Simulate trade (for testing without real execution)             |
//+------------------------------------------------------------------+
void SimulateTrade(string command, double confidence, int stopLossPoints, int takeProfitPoints, double lotSize)
{
    double price = (command == "BUY") ? Ask : Bid;
    double sl = 0, tp = 0;
    
    if(command == "BUY")
    {
        sl = (stopLossPoints > 0) ? price - (stopLossPoints * Point) : 0;
        tp = (takeProfitPoints > 0) ? price + (takeProfitPoints * Point) : 0;
    }
    else
    {
        sl = (stopLossPoints > 0) ? price + (stopLossPoints * Point) : 0;
        tp = (takeProfitPoints > 0) ? price - (takeProfitPoints * Point) : 0;
    }
    
    Print("=== SIMULATED TRADE ===");
    Print("Action: ", command);
    Print("Entry: ", DoubleToString(price, Digits));
    Print("Lot size: ", DoubleToString(lotSize, 2));
    Print("Stop loss: ", DoubleToString(sl, Digits), " (", stopLossPoints, " points)");
    Print("Take profit: ", DoubleToString(tp, Digits), " (", takeProfitPoints, " points)");
    Print("Confidence: ", DoubleToString(confidence, 2));
    Print("======================");
}

//+------------------------------------------------------------------+
//| Count open trades with our magic number                          |
//+------------------------------------------------------------------+
int CountMyOpenTrades()
{
    int count = 0;
    for(int i = 0; i < OrdersTotal(); i++)
    {
        if(OrderSelect(i, SELECT_BY_POS, MODE_TRADES))
        {
            if(OrderSymbol() == Symbol() && OrderMagicNumber() == MagicNumber)
            {
                count++;
            }
        }
    }
    return count;
}

//+------------------------------------------------------------------+
//| Update signal statistics                                          |
//+------------------------------------------------------------------+
void UpdateSignalStats(string pair, string statType)
{
    for(int i = 0; i < g_statsCount; i++)
    {
        if(g_signalStats[i].pair == pair)
        {
            if(statType == "received")
            {
                g_signalStats[i].received++;
                g_signalStats[i].last_signal = TimeCurrent();
            }
            else if(statType == "processed")
            {
                g_signalStats[i].processed++;
            }
            else if(statType == "trades_opened")
            {
                g_signalStats[i].trades_opened++;
            }
            return;
        }
    }
}

//+------------------------------------------------------------------+
//| Print current configuration                                       |
//+------------------------------------------------------------------+
void PrintCurrentConfiguration()
{
    Print("=== Current Configuration ===");
    Print("Trading enabled: ", (EnableTrading ? "YES" : "NO"));
    Print("Min confidence: ", DoubleToString(MinConfidence, 2));
    Print("Max spread: ", MaxSpreadPoints, " points");
    Print("Max open trades: ", MaxOpenTrades);
    Print("Signal check interval: ", SignalCheckInterval, " seconds");
    Print("Current parameters: ", g_defaultParams.id);
    Print("=============================");
}

//+------------------------------------------------------------------+
//| Print final statistics                                            |
//+------------------------------------------------------------------+
void PrintFinalStatistics()
{
    Print("=== Final Statistics ===");
    Print("Total signals received: ", g_totalSignalsReceived);
    Print("Total signals processed: ", g_totalSignalsProcessed);
    Print("Total trades opened: ", g_totalTradesOpened);
    Print("Current open trades: ", CountMyOpenTrades());
    
    if(g_totalSignalsReceived > 0)
    {
        double processRate = (double)g_totalSignalsProcessed / g_totalSignalsReceived * 100;
        Print("Signal processing rate: ", DoubleToString(processRate, 1), "%");
    }
    
    Print("Per-pair statistics:");
    for(int i = 0; i < g_statsCount; i++)
    {
        if(g_signalStats[i].received > 0)
        {
            Print("  ", g_signalStats[i].pair, ": R=", g_signalStats[i].received, 
                  " P=", g_signalStats[i].processed, " T=", g_signalStats[i].trades_opened);
        }
    }
    Print("=======================");
}
```

**Test the complete signal processing system:**
```
1. Compile HUEY_P_MQL4_signal_processor.mq4
2. Attach it to EURUSD chart with these settings:
   - EnableTrading: false (simulation mode)
   - MinConfidence: 0.70
   - MaxOpenTrades: 1
3. Run the Python signal service
4. Watch the EA process signals in simulation mode
```

### **Week 11-12: Database Integration (15-20 hours)**

#### **Day 41-45: Create Database System (15-20 hours)**

**Step 14: Database Integration and Logging**

**14.1 Create Database Schema (3-4 hours)**

Create: `C:\TradingSystem\Database\HUEY_P_SQL_create_schema.sql`

```sql
-- HUEY_P_SQL_create_schema.sql
-- Database schema for trading system

-- Enable foreign key constraints
PRAGMA foreign_keys = ON;

-- Table to store all generated signals
CREATE TABLE IF NOT EXISTS signals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    signal_uuid TEXT UNIQUE NOT NULL,           -- Unique identifier for each signal
    symbol TEXT NOT NULL,                       -- Currency pair (e.g., 'EURUSD')
    direction TEXT NOT NULL CHECK (direction IN ('BUY', 'SELL')), -- Trade direction
    confidence REAL NOT NULL CHECK (confidence >= 0.0 AND confidence <= 1.0), -- ML confidence
    strategy_name TEXT NOT NULL,                -- Strategy that generated signal
    stop_loss_points INTEGER,                   -- Stop loss in points
    take_profit_points INTEGER,                 -- Take profit in points
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- When signal was created
    sent_to_bridge_at TIMESTAMP,                -- When sent to MT4 bridge
    metadata TEXT,                              -- JSON metadata (optional)
    
    -- Indexes for performance
    INDEX idx_signals_symbol (symbol),
    INDEX idx_signals_generated_at (generated_at),
    INDEX idx_signals_strategy (strategy_name)
);

-- Table to store trade executions
CREATE TABLE IF NOT EXISTS trades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    signal_uuid TEXT,                           -- Link to originating signal
    mt4_ticket INTEGER UNIQUE,                  -- MT4 ticket number
    symbol TEXT NOT NULL,                       -- Currency pair
    direction TEXT NOT NULL CHECK (direction IN ('BUY', 'SELL')), -- Trade direction
    lot_size REAL NOT NULL CHECK (lot_size > 0), -- Position size
    entry_price REAL NOT NULL,                  -- Entry price
    stop_loss_price REAL,                       -- Stop loss price
    take_profit_price REAL,                     -- Take profit price
    exit_price REAL,                            -- Exit price (when closed)
    opened_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- When trade opened
    closed_at TIMESTAMP,                        -- When trade closed
    pnl REAL DEFAULT 0.0,                      -- Profit/Loss in account currency
    commission REAL DEFAULT 0.0,               -- Commission paid
    swap REAL DEFAULT 0.0,                     -- Swap/rollover
    status TEXT DEFAULT 'OPEN' CHECK (status IN ('OPEN', 'CLOSED', 'CANCELLED')), -- Trade status
    close_reason TEXT,                          -- Why trade was closed
    magic_number INTEGER,                       -- EA magic number
    comment TEXT,                               -- Trade comment
    
    -- Foreign key relationship
    FOREIGN KEY (signal_uuid) REFERENCES signals (signal_uuid),
    
    -- Indexes
    INDEX idx_trades_symbol (symbol),
    INDEX idx_trades_opened_at (opened_at),
    INDEX idx_trades_status (status),
    INDEX idx_trades_mt4_ticket (mt4_ticket)
);

-- Table to store system performance metrics
CREATE TABLE IF NOT EXISTS performance_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date_recorded DATE NOT NULL,               -- Date of measurement
    symbol TEXT,                               -- Specific pair (NULL = overall)
    total_signals INTEGER DEFAULT 0,           -- Total signals generated
    signals_processed INTEGER DEFAULT 0,       -- Signals that resulted in trades
    trades_opened INTEGER DEFAULT 0,           -- Trades opened
    trades_closed INTEGER DEFAULT 0,           -- Trades closed
    total_pnl REAL DEFAULT 0.0,               -- Total profit/loss
    win_rate REAL DEFAULT 0.0,                -- Win rate (0.0 to 1.0)
    avg_win REAL DEFAULT 0.0,                 -- Average winning trade
    avg_loss REAL DEFAULT 0.0,                -- Average losing trade
    max_drawdown REAL DEFAULT 0.0,            -- Maximum drawdown
    sharpe_ratio REAL,                         -- Risk-adjusted return
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Ensure one record per date per symbol
    UNIQUE (date_recorded, symbol),
    
    -- Indexes
    INDEX idx_performance_date (date_recorded),
    INDEX idx_performance_symbol (symbol)
);

-- Table to store system configuration changes
CREATE TABLE IF NOT EXISTS config_changes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    change_type TEXT NOT NULL,                  -- Type of change
    component TEXT NOT NULL,                    -- Which component changed
    old_value TEXT,                            -- Previous value
    new_value TEXT,                            -- New value
    changed_by TEXT,                           -- Who made the change
    change_reason TEXT,                        -- Why change was made
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Indexes
    INDEX idx_config_changes_component (component),
    INDEX idx_config_changes_date (changed_at)
);

-- Table to store signal strategy performance
CREATE TABLE IF NOT EXISTS strategy_performance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    strategy_name TEXT NOT NULL,
    symbol TEXT NOT NULL,
    date_recorded DATE NOT NULL,
    signals_generated INTEGER DEFAULT 0,
    signals_traded INTEGER DEFAULT 0,
    total_pnl REAL DEFAULT 0.0,
    win_count INTEGER DEFAULT 0,
    loss_count INTEGER DEFAULT 0,
    avg_confidence REAL DEFAULT 0.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Unique constraint
    UNIQUE (strategy_name, symbol, date_recorded),
    
    -- Indexes
    INDEX idx_strategy_perf_name (strategy_name),
    INDEX idx_strategy_perf_symbol (symbol),
    INDEX idx_strategy_perf_date (date_recorded)
);

-- Table to store system health metrics
CREATE TABLE IF NOT EXISTS system_health (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    component TEXT NOT NULL,                    -- Component name
    status TEXT NOT NULL CHECK (status IN ('HEALTHY', 'DEGRADED', 'CRITICAL', 'DOWN')),
    cpu_usage REAL,                            -- CPU usage percentage
    memory_usage REAL,                         -- Memory usage percentage
    response_time_ms INTEGER,                  -- Response time in milliseconds
    error_count INTEGER DEFAULT 0,             -- Number of errors since last check
    last_error TEXT,                           -- Last error message
    additional_info TEXT,                      -- Additional JSON info
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Indexes
    INDEX idx_health_component (component),
    INDEX idx_health_recorded_at (recorded_at),
    INDEX idx_health_status (status)
);

-- Create views for common queries

-- View: Daily trading summary
CREATE VIEW IF NOT EXISTS daily_trading_summary AS
SELECT 
    DATE(opened_at) as trade_date,
    symbol,
    COUNT(*) as total_trades,
    SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) as winning_trades,
    SUM(CASE WHEN pnl < 0 THEN 1 ELSE 0 END) as losing_trades,
    SUM(pnl) as total_pnl,
    AVG(pnl) as avg_pnl,
    MAX(pnl) as best_trade,
    MIN(pnl) as worst_trade,
    ROUND(SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as win_rate
FROM trades 
WHERE status = 'CLOSED'
GROUP BY DATE(opened_at), symbol
ORDER BY trade_date DESC, symbol;

-- View: Signal to trade conversion rates
CREATE VIEW IF NOT EXISTS signal_conversion_rates AS
SELECT 
    s.strategy_name,
    s.symbol,
    COUNT(s.id) as signals_generated,
    COUNT(t.id) as trades_executed,
    ROUND(COUNT(t.id) * 100.0 / COUNT(s.id), 2) as conversion_rate,
    AVG(s.confidence) as avg_confidence
FROM signals s
LEFT JOIN trades t ON s.signal_uuid = t.signal_uuid
GROUP BY s.strategy_name, s.symbol
ORDER BY conversion_rate DESC;

-- View: Current open positions
CREATE VIEW IF NOT EXISTS open_positions AS
SELECT 
    mt4_ticket,
    symbol,
    direction,
    lot_size,
    entry_price,
    stop_loss_price,
    take_profit_price,
    opened_at,
    comment,
    ROUND((julianday('now') - julianday(opened_at)) * 24, 2) as hours_open
FROM trades 
WHERE status = 'OPEN'
ORDER BY opened_at;

-- Insert initial configuration record
INSERT OR IGNORE INTO config_changes (change_type, component, new_value, changed_by, change_reason)
VALUES ('INITIALIZATION', 'DATABASE', '1.0.0', 'SYSTEM', 'Initial database schema creation');

-- Insert sample data for testing
INSERT OR IGNORE INTO signals (
    signal_uuid, symbol, direction, confidence, strategy_name, 
    stop_loss_points, take_profit_points, generated_at
) VALUES 
('TEST001', 'EURUSD', 'BUY', 0.85, 'trend_following', 50, 100, datetime('now', '-1 hour')),
('TEST002', 'GBPUSD', 'SELL', 0.75, 'momentum', 60, 120, datetime('now', '-30 minutes')),
('TEST003', 'USDJPY', 'BUY', 0.90, 'reversal', 40, 80, datetime('now', '-15 minutes'));

-- Create triggers for automatic calculations

-- Trigger: Update performance metrics when trade is closed
CREATE TRIGGER IF NOT EXISTS update_performance_on_trade_close
AFTER UPDATE OF status ON trades
WHEN NEW.status = 'CLOSED' AND OLD.status = 'OPEN'
BEGIN
    -- Insert or update daily performance metrics
    INSERT OR REPLACE INTO performance_metrics (
        date_recorded, symbol, total_pnl, trades_closed
    ) VALUES (
        DATE(NEW.closed_at), 
        NEW.symbol,
        COALESCE((SELECT total_pnl FROM performance_metrics 
                 WHERE date_recorded = DATE(NEW.closed_at) AND symbol = NEW.symbol), 0) + NEW.pnl,
        COALESCE((SELECT trades_closed FROM performance_metrics 
                 WHERE date_recorded = DATE(NEW.closed_at) AND symbol = NEW.symbol), 0) + 1
    );
END;

-- Trigger: Log signal creation
CREATE TRIGGER IF NOT EXISTS log_signal_creation
AFTER INSERT ON signals
BEGIN
    UPDATE performance_metrics 
    SET total_signals = total_signals + 1
    WHERE date_recorded = DATE(NEW.generated_at) AND symbol = NEW.symbol;
    
    -- Create entry if doesn't exist
    INSERT OR IGNORE INTO performance_metrics (date_recorded, symbol, total_signals)
    VALUES (DATE(NEW.generated_at), NEW.symbol, 1);
END;

-- Cleanup old data procedure (commented out - run manually)
/*
-- Delete system health records older than 30 days
DELETE FROM system_health WHERE recorded_at < datetime('now', '-30 days');

-- Delete performance metrics older than 1 year  
DELETE FROM performance_metrics WHERE created_at < datetime('now', '-1 year');

-- Archive closed trades older than 6 months to separate table
CREATE TABLE IF NOT EXISTS trades_archive AS SELECT * FROM trades WHERE 1=0;
INSERT INTO trades_archive SELECT * FROM trades 
WHERE status = 'CLOSED' AND closed_at < datetime('now', '-6 months');
DELETE FROM trades WHERE status = 'CLOSED' AND closed_at < datetime('now', '-6 months');
*/

-- Display schema creation summary
SELECT 'Database schema created successfully' as status;
SELECT 'Tables created: ' || COUNT(*) as info FROM sqlite_master WHERE type='table';
SELECT 'Views created: ' || COUNT(*) as info FROM sqlite_master WHERE type='view';
SELECT 'Triggers created: ' || COUNT(*) as info FROM sqlite_master WHERE type='trigger';
```

**14.2 Database Manager Python Module (4-5 hours)**

Create: `C:\TradingSystem\Source\Python\HUEY_P_PY_database_manager.py`

```python
# HUEY_P_PY_database_manager.py
# Database management module for trading system

import sqlite3
import json
import uuid
import threading
from datetime import datetime, date
from typing import Optional, List, Dict, Any, Tuple
from pathlib import Path

class TradingDatabaseManager:
    def __init__(self, db_path: str = r"C:\TradingSystem\Database\trading_system.db"):
        """
        Initialize database manager
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.connection = None
        self.lock = threading.Lock()  # Thread safety
        
        # Ensure database directory exists
        db_dir = Path(db_path).parent
        db_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"Database manager initialized: {db_path}")
    
    def connect(self) -> bool:
        """Connect to database and initialize schema if needed"""
        try:
            self.connection = sqlite3.connect(
                self.db_path, 
                check_same_thread=False,  # Allow multi-threading
                timeout=10.0  # 10 second timeout
            )
            
            # Enable foreign keys and WAL mode for better performance
            self.connection.execute("PRAGMA foreign_keys = ON")
            self.connection.execute("PRAGMA journal_mode = WAL")
            self.connection.execute("PRAGMA synchronous = NORMAL")
            
            # Set row factory for dict-like access
            self.connection.row_factory = sqlite3.Row
            
            print("✓ Database connected successfully")
            
            # Initialize schema if tables don't exist
            return self._initialize_schema()
            
        except sqlite3.Error as e:
            print(f"✗ Database connection error: {e}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            self.connection = None
            print("Database connection closed")
    
    def _initialize_schema(self) -> bool:
        """Initialize database schema if not exists"""
        try:
            # Check if tables exist
            cursor = self.connection.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='signals'"
            )
            
            if not cursor.fetchone():
                print("Initializing database schema...")
                
                # Read and execute schema file
                schema_path = Path(__file__).parent.parent.parent / "Database" / "HUEY_P_SQL_create_schema.sql"
                
                if schema_path.exists():
                    with open(schema_path, 'r') as f:
                        schema_sql = f.read()
                    
                    # Execute schema creation
                    self.connection.executescript(schema_sql)
                    self.connection.commit()
                    print("✓ Database schema initialized")
                else:
                    print(f"⚠️  Schema file not found: {schema_path}")
                    # Create basic tables manually
                    self._create_basic_schema()
            else:
                print("✓ Database schema already exists")
            
            return True
            
        except sqlite3.Error as e:
            print(f"✗ Schema initialization error: {e}")
            return False
    
    def _create_basic_schema(self):
        """Create basic schema if schema file not found"""
        basic_schema = """
        CREATE TABLE IF NOT EXISTS signals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            signal_uuid TEXT UNIQUE NOT NULL,
            symbol TEXT NOT NULL,
            direction TEXT NOT NULL,
            confidence REAL NOT NULL,
            strategy_name TEXT NOT NULL,
            stop_loss_points INTEGER,
            take_profit_points INTEGER,
            generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            sent_to_bridge_at TIMESTAMP,
            metadata TEXT
        );
        
        CREATE TABLE IF NOT EXISTS trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            signal_uuid TEXT,
            mt4_ticket INTEGER UNIQUE,
            symbol TEXT NOT NULL,
            direction TEXT NOT NULL,
            lot_size REAL NOT NULL,
            entry_price REAL NOT NULL,
            stop_loss_price REAL,
            take_profit_price REAL,
            exit_price REAL,
            opened_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            closed_at TIMESTAMP,
            pnl REAL DEFAULT 0.0,
            status TEXT DEFAULT 'OPEN',
            magic_number INTEGER,
            comment TEXT
        );
        """
        
        self.connection.executescript(basic_schema)
        self.connection.commit()
        print("✓ Basic schema created")
    
    # SIGNAL MANAGEMENT METHODS
    
    def log_signal(self, signal_data: Dict[str, Any]) -> str:
        """
        Log a generated trading signal

```python
    def log_signal(self, signal_data: Dict[str, Any]) -> str:
        """
        Log a generated trading signal
        
        Args:
            signal_data: Dictionary containing signal information
            
        Returns:
            str: Signal UUID if successful, None if failed
        """
        with self.lock:
            try:
                # Generate unique ID if not provided
                signal_uuid = signal_data.get('uuid', str(uuid.uuid4()))
                
                # Prepare metadata
                metadata = {}
                for key in ['raw_features', 'model_version', 'market_conditions']:
                    if key in signal_data:
                        metadata[key] = signal_data[key]
                
                metadata_json = json.dumps(metadata) if metadata else None
                
                cursor = self.connection.execute("""
                    INSERT INTO signals (
                        signal_uuid, symbol, direction, confidence, strategy_name,
                        stop_loss_points, take_profit_points, generated_at, metadata
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    signal_uuid,
                    signal_data['symbol'],
                    signal_data['direction'],
                    signal_data['confidence'],
                    signal_data['strategy_name'],
                    signal_data.get('stop_loss_points'),
                    signal_data.get('take_profit_points'),
                    signal_data.get('generated_at', datetime.now()),
                    metadata_json
                ))
                
                self.connection.commit()
                
                print(f"✓ Signal logged: {signal_uuid} - {signal_data['symbol']} {signal_data['direction']}")
                return signal_uuid
                
            except sqlite3.Error as e:
                print(f"✗ Error logging signal: {e}")
                return None
    
    def mark_signal_sent(self, signal_uuid: str) -> bool:
        """Mark signal as sent to bridge"""
        with self.lock:
            try:
                cursor = self.connection.execute("""
                    UPDATE signals 
                    SET sent_to_bridge_at = ?
                    WHERE signal_uuid = ?
                """, (datetime.now(), signal_uuid))
                
                self.connection.commit()
                
                if cursor.rowcount > 0:
                    print(f"✓ Signal marked as sent: {signal_uuid}")
                    return True
                else:
                    print(f"⚠️  Signal not found for marking sent: {signal_uuid}")
                    return False
                    
            except sqlite3.Error as e:
                print(f"✗ Error marking signal sent: {e}")
                return False
    
    def get_signals(self, symbol: Optional[str] = None, limit: int = 100) -> List[Dict]:
        """
        Get recent signals
        
        Args:
            symbol: Filter by symbol (None for all)
            limit: Maximum number of records
            
        Returns:
            List of signal dictionaries
        """
        try:
            if symbol:
                cursor = self.connection.execute("""
                    SELECT * FROM signals 
                    WHERE symbol = ?
                    ORDER BY generated_at DESC 
                    LIMIT ?
                """, (symbol, limit))
            else:
                cursor = self.connection.execute("""
                    SELECT * FROM signals 
                    ORDER BY generated_at DESC 
                    LIMIT ?
                """, (limit,))
            
            return [dict(row) for row in cursor.fetchall()]
            
        except sqlite3.Error as e:
            print(f"✗ Error getting signals: {e}")
            return []
    
    # TRADE MANAGEMENT METHODS
    
    def log_trade_opened(self, trade_data: Dict[str, Any]) -> bool:
        """
        Log a trade that was opened
        
        Args:
            trade_data: Dictionary containing trade information
            
        Returns:
            bool: Success status
        """
        with self.lock:
            try:
                cursor = self.connection.execute("""
                    INSERT INTO trades (
                        signal_uuid, mt4_ticket, symbol, direction, lot_size,
                        entry_price, stop_loss_price, take_profit_price,
                        opened_at, status, magic_number, comment
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    trade_data.get('signal_uuid'),
                    trade_data['mt4_ticket'],
                    trade_data['symbol'],
                    trade_data['direction'],
                    trade_data['lot_size'],
                    trade_data['entry_price'],
                    trade_data.get('stop_loss_price'),
                    trade_data.get('take_profit_price'),
                    trade_data.get('opened_at', datetime.now()),
                    'OPEN',
                    trade_data.get('magic_number'),
                    trade_data.get('comment')
                ))
                
                self.connection.commit()
                
                print(f"✓ Trade logged: Ticket #{trade_data['mt4_ticket']} - "
                      f"{trade_data['symbol']} {trade_data['direction']}")
                return True
                
            except sqlite3.Error as e:
                print(f"✗ Error logging trade: {e}")
                return False
    
    def log_trade_closed(self, mt4_ticket: int, close_data: Dict[str, Any]) -> bool:
        """
        Log trade closure
        
        Args:
            mt4_ticket: MT4 ticket number
            close_data: Dictionary with closure information
            
        Returns:
            bool: Success status
        """
        with self.lock:
            try:
                cursor = self.connection.execute("""
                    UPDATE trades SET
                        exit_price = ?,
                        closed_at = ?,
                        pnl = ?,
                        commission = ?,
                        swap = ?,
                        status = 'CLOSED',
                        close_reason = ?
                    WHERE mt4_ticket = ?
                """, (
                    close_data['exit_price'],
                    close_data.get('closed_at', datetime.now()),
                    close_data['pnl'],
                    close_data.get('commission', 0.0),
                    close_data.get('swap', 0.0),
                    close_data.get('close_reason', 'UNKNOWN'),
                    mt4_ticket
                ))
                
                self.connection.commit()
                
                if cursor.rowcount > 0:
                    print(f"✓ Trade closed: Ticket #{mt4_ticket} - PnL: ${close_data['pnl']:.2f}")
                    return True
                else:
                    print(f"⚠️  Trade not found for closure: Ticket #{mt4_ticket}")
                    return False
                    
            except sqlite3.Error as e:
                print(f"✗ Error closing trade: {e}")
                return False
    
    def get_open_trades(self, symbol: Optional[str] = None) -> List[Dict]:
        """Get currently open trades"""
        try:
            if symbol:
                cursor = self.connection.execute("""
                    SELECT * FROM trades 
                    WHERE status = 'OPEN' AND symbol = ?
                    ORDER BY opened_at DESC
                """, (symbol,))
            else:
                cursor = self.connection.execute("""
                    SELECT * FROM trades 
                    WHERE status = 'OPEN'
                    ORDER BY opened_at DESC
                """)
            
            return [dict(row) for row in cursor.fetchall()]
            
        except sqlite3.Error as e:
            print(f"✗ Error getting open trades: {e}")
            return []
    
    def get_trade_history(self, symbol: Optional[str] = None, days: int = 30) -> List[Dict]:
        """Get trade history"""
        try:
            if symbol:
                cursor = self.connection.execute("""
                    SELECT * FROM trades 
                    WHERE symbol = ? AND opened_at > datetime('now', '-{} days')
                    ORDER BY opened_at DESC
                """.format(days), (symbol,))
            else:
                cursor = self.connection.execute("""
                    SELECT * FROM trades 
                    WHERE opened_at > datetime('now', '-{} days')
                    ORDER BY opened_at DESC
                """.format(days))
            
            return [dict(row) for row in cursor.fetchall()]
            
        except sqlite3.Error as e:
            print(f"✗ Error getting trade history: {e}")
            return []
    
    # PERFORMANCE ANALYSIS METHODS
    
    def calculate_daily_performance(self, target_date: Optional[date] = None) -> Dict[str, Any]:
        """Calculate performance metrics for a specific date"""
        if not target_date:
            target_date = date.today()
        
        try:
            # Get daily trading summary
            cursor = self.connection.execute("""
                SELECT * FROM daily_trading_summary 
                WHERE trade_date = ?
            """, (target_date.isoformat(),))
            
            daily_data = [dict(row) for row in cursor.fetchall()]
            
            # Calculate overall metrics
            total_trades = sum(row['total_trades'] for row in daily_data)
            total_pnl = sum(row['total_pnl'] for row in daily_data)
            total_winning = sum(row['winning_trades'] for row in daily_data)
            
            overall_win_rate = (total_winning / total_trades * 100) if total_trades > 0 else 0
            
            return {
                'date': target_date.isoformat(),
                'total_trades': total_trades,
                'total_pnl': total_pnl,
                'win_rate': round(overall_win_rate, 2),
                'by_pair': daily_data
            }
            
        except sqlite3.Error as e:
            print(f"✗ Error calculating daily performance: {e}")
            return {}
    
    def get_strategy_performance(self, days: int = 30) -> List[Dict]:
        """Get strategy performance analysis"""
        try:
            cursor = self.connection.execute("""
                SELECT 
                    s.strategy_name,
                    COUNT(s.id) as signals_generated,
                    COUNT(t.id) as trades_executed,
                    COALESCE(SUM(t.pnl), 0) as total_pnl,
                    AVG(s.confidence) as avg_confidence,
                    COUNT(CASE WHEN t.pnl > 0 THEN 1 END) as winning_trades,
                    COUNT(CASE WHEN t.pnl < 0 THEN 1 END) as losing_trades
                FROM signals s
                LEFT JOIN trades t ON s.signal_uuid = t.signal_uuid
                WHERE s.generated_at > datetime('now', '-{} days')
                GROUP BY s.strategy_name
                ORDER BY total_pnl DESC
            """.format(days))
            
            results = []
            for row in cursor.fetchall():
                row_dict = dict(row)
                
                # Calculate additional metrics
                total_trades = row_dict['trades_executed']
                if total_trades > 0:
                    row_dict['conversion_rate'] = round(
                        (total_trades / row_dict['signals_generated']) * 100, 2
                    )
                    row_dict['win_rate'] = round(
                        (row_dict['winning_trades'] / total_trades) * 100, 2
                    )
                else:
                    row_dict['conversion_rate'] = 0
                    row_dict['win_rate'] = 0
                
                results.append(row_dict)
            
            return results
            
        except sqlite3.Error as e:
            print(f"✗ Error getting strategy performance: {e}")
            return []
    
    # SYSTEM HEALTH METHODS
    
    def log_system_health(self, component: str, status: str, metrics: Dict[str, Any]) -> bool:
        """Log system health metrics"""
        with self.lock:
            try:
                cursor = self.connection.execute("""
                    INSERT INTO system_health (
                        component, status, cpu_usage, memory_usage, 
                        response_time_ms, error_count, last_error, additional_info
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    component,
                    status,
                    metrics.get('cpu_usage'),
                    metrics.get('memory_usage'),
                    metrics.get('response_time_ms'),
                    metrics.get('error_count', 0),
                    metrics.get('last_error'),
                    json.dumps(metrics.get('additional_info', {}))
                ))
                
                self.connection.commit()
                return True
                
            except sqlite3.Error as e:
                print(f"✗ Error logging system health: {e}")
                return False
    
    def get_system_health_status(self) -> Dict[str, Any]:
        """Get current system health status"""
        try:
            # Get latest health record for each component
            cursor = self.connection.execute("""
                SELECT component, status, recorded_at, cpu_usage, memory_usage, 
                       response_time_ms, error_count
                FROM system_health sh1
                WHERE recorded_at = (
                    SELECT MAX(recorded_at) 
                    FROM system_health sh2 
                    WHERE sh2.component = sh1.component
                )
                ORDER BY component
            """)
            
            components = [dict(row) for row in cursor.fetchall()]
            
            # Calculate overall system status
            if not components:
                overall_status = "UNKNOWN"
            elif any(c['status'] == 'CRITICAL' for c in components):
                overall_status = "CRITICAL"
            elif any(c['status'] == 'DEGRADED' for c in components):
                overall_status = "DEGRADED"
            else:
                overall_status = "HEALTHY"
            
            return {
                'overall_status': overall_status,
                'components': components,
                'last_updated': max(c['recorded_at'] for c in components) if components else None
            }
            
        except sqlite3.Error as e:
            print(f"✗ Error getting system health: {e}")
            return {'overall_status': 'ERROR', 'components': []}
    
    # UTILITY METHODS
    
    def backup_database(self, backup_path: str) -> bool:
        """Create database backup"""
        try:
            backup = sqlite3.connect(backup_path)
            self.connection.backup(backup)
            backup.close()
            
            print(f"✓ Database backed up to: {backup_path}")
            return True
            
        except sqlite3.Error as e:
            print(f"✗ Database backup error: {e}")
            return False
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        try:
            stats = {}
            
            # Table sizes
            tables = ['signals', 'trades', 'performance_metrics', 'system_health']
            for table in tables:
                cursor = self.connection.execute(f"SELECT COUNT(*) as count FROM {table}")
                stats[f"{table}_count"] = cursor.fetchone()['count']
            
            # Database file size
            db_path = Path(self.db_path)
            if db_path.exists():
                stats['db_size_mb'] = round(db_path.stat().st_size / (1024 * 1024), 2)
            
            # Recent activity
            cursor = self.connection.execute("""
                SELECT COUNT(*) as count FROM signals 
                WHERE generated_at > datetime('now', '-24 hours')
            """)
            stats['signals_last_24h'] = cursor.fetchone()['count']
            
            cursor = self.connection.execute("""
                SELECT COUNT(*) as count FROM trades 
                WHERE opened_at > datetime('now', '-24 hours')
            """)
            stats['trades_last_24h'] = cursor.fetchone()['count']
            
            return stats
            
        except sqlite3.Error as e:
            print(f"✗ Error getting database stats: {e}")
            return {}
    
    def cleanup_old_data(self, days_to_keep: int = 90) -> bool:
        """Clean up old data beyond retention period"""
        with self.lock:
            try:
                # Clean old system health records
                cursor = self.connection.execute("""
                    DELETE FROM system_health 
                    WHERE recorded_at < datetime('now', '-{} days')
                """.format(days_to_keep))
                
                deleted_health = cursor.rowcount
                
                # Don't delete signals/trades - they're valuable for analysis
                # But you could archive them to a separate table
                
                self.connection.commit()
                
                print(f"✓ Cleaned up {deleted_health} old health records")
                return True
                
            except sqlite3.Error as e:
                print(f"✗ Error cleaning up data: {e}")
                return False

def test_database_operations():
    """Test all database operations"""
    print("=== Testing Database Operations ===")
    
    # Initialize database
    db = TradingDatabaseManager()
    
    if not db.connect():
        print("Failed to connect to database")
        return
    
    try:
        # Test 1: Log a signal
        print("\n1. Testing signal logging...")
        signal_data = {
            'symbol': 'EURUSD',
            'direction': 'BUY',
            'confidence': 0.85,
            'strategy_name': 'test_strategy',
            'stop_loss_points': 50,
            'take_profit_points': 100
        }
        
        signal_uuid = db.log_signal(signal_data)
        if signal_uuid:
            print(f"   ✓ Signal logged with UUID: {signal_uuid}")
            
            # Mark as sent
            db.mark_signal_sent(signal_uuid)
        
        # Test 2: Log a trade
        print("\n2. Testing trade logging...")
        trade_data = {
            'signal_uuid': signal_uuid,
            'mt4_ticket': 12345678,
            'symbol': 'EURUSD',
            'direction': 'BUY',
            'lot_size': 0.01,
            'entry_price': 1.0850,
            'stop_loss_price': 1.0800,
            'take_profit_price': 1.0950,
            'magic_number': 13001,
            'comment': 'Test trade'
        }
        
        if db.log_trade_opened(trade_data):
            print("   ✓ Trade logged successfully")
            
            # Close the trade
            close_data = {
                'exit_price': 1.0920,
                'pnl': 70.0,
                'close_reason': 'TAKE_PROFIT'
            }
            
            db.log_trade_closed(12345678, close_data)
        
        # Test 3: Get data
        print("\n3. Testing data retrieval...")
        
        signals = db.get_signals(limit=5)
        print(f"   Retrieved {len(signals)} signals")
        
        trades = db.get_trade_history(days=1)
        print(f"   Retrieved {len(trades)} trades")
        
        # Test 4: Performance analysis
        print("\n4. Testing performance analysis...")
        
        daily_perf = db.calculate_daily_performance()
        print(f"   Daily performance: {daily_perf.get('total_trades', 0)} trades")
        
        strategy_perf = db.get_strategy_performance(days=1)
        print(f"   Strategy performance: {len(strategy_perf)} strategies analyzed")
        
        # Test 5: System health
        print("\n5. Testing system health logging...")
        
        health_metrics = {
            'cpu_usage': 45.2,
            'memory_usage': 67.8,
            'response_time_ms': 25,
            'error_count': 0
        }
        
        db.log_system_health('TEST_COMPONENT', 'HEALTHY', health_metrics)
        
        health_status = db.get_system_health_status()
        print(f"   System health: {health_status.get('overall_status', 'UNKNOWN')}")
        
        # Test 6: Database stats
        print("\n6. Testing database statistics...")
        
        stats = db.get_database_stats()
        print(f"   Database size: {stats.get('db_size_mb', 0)} MB")
        print(f"   Total signals: {stats.get('signals_count', 0)}")
        print(f"   Total trades: {stats.get('trades_count', 0)}")
        
        print("\n=== All Database Tests Completed Successfully ===")
        
    except Exception as e:
        print(f"\n✗ Database test error: {e}")
    
    finally:
        db.disconnect()

if __name__ == "__main__":
    test_database_operations()
```

**14.3 Integrate Database with Signal Service (4-5 hours)**

Create: `C:\TradingSystem\Source\Python\HUEY_P_PY_enhanced_signal_service.py`

```python
# HUEY_P_PY_enhanced_signal_service.py
# Enhanced signal service with database integration

import time
import random
import threading
import signal
import sys
import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

from HUEY_P_PY_database_manager import TradingDatabaseManager
from HUEY_P_PY_signal_service_basic import TradingSignalGenerator

class EnhancedTradingSignalService:
    def __init__(self):
        """Initialize enhanced signal service with database integration"""
        
        # Initialize database
        self.db = TradingDatabaseManager()
        self.db_connected = False
        
        # Initialize basic signal generator
        self.signal_generator = TradingSignalGenerator()
        
        # Service configuration
        self.service_name = "HUEY_P_Enhanced_Signal_Service"
        self.version = "1.0.0"
        self.started_at = datetime.now()
        
        # Statistics tracking
        self.stats = {
            'signals_generated': 0,
            'signals_sent': 0,
            'database_errors': 0,
            'bridge_errors': 0,
            'uptime_start': self.started_at
        }
        
        # Enhanced strategy configuration
        self.enhanced_strategies = {
            "trend_following_v2": {
                "confidence_range": (0.75, 0.95),
                "sl_range": (40, 60),
                "tp_range": (80, 120),
                "market_conditions": ["trending", "volatile"],
                "active_hours": (8, 18),  # GMT hours
                "max_daily_signals": 10
            },
            "momentum_scalp": {
                "confidence_range": (0.65, 0.85),
                "sl_range": (20, 40),
                "tp_range": (40, 80),
                "market_conditions": ["high_volume", "news_driven"],
                "active_hours": (9, 17),
                "max_daily_signals": 20
            },
            "reversal_hunter": {
                "confidence_range": (0.80, 0.95),
                "sl_range": (50, 80),
                "tp_range": (100, 150),
                "market_conditions": ["oversold", "overbought"],
                "active_hours": (6, 20),
                "max_daily_signals": 5
            }
        }
        
        # Daily signal tracking per strategy
        self.daily_signal_count = {}
        self.reset_daily_counts()
        
        print(f"Enhanced Signal Service initialized")
        print(f"Service: {self.service_name} v{self.version}")
        print(f"Enhanced strategies: {len(self.enhanced_strategies)}")
    
    def reset_daily_counts(self):
        """Reset daily signal counts (called at start of new day)"""
        current_date = datetime.now().date()
        self.daily_signal_count = {
            'date': current_date,
            'by_strategy': {strategy: 0 for strategy in self.enhanced_strategies.keys()}
        }
    
    def initialize_services(self) -> bool:
        """Initialize all required services"""
        print("Initializing services...")
        
        # Connect to database
        if not self.db.connect():
            print("✗ Failed to connect to database")
            return False
        
        self.db_connected = True
        print("✓ Database connected")
        
        # Initialize bridge
        if not self.signal_generator.load_bridge_dll():
            print("✗ Failed to load bridge DLL")
            return False
        
        if not self.signal_generator.initialize_bridge():
            print("✗ Failed to initialize bridge")
            return False
        
        print("✓ Bridge initialized")
        
        # Log service startup
        self._log_system_health("STARTUP", {"version": self.version})
        
        return True
    
    def shutdown_services(self):
        """Shutdown all services gracefully"""
        print("Shutting down services...")
        
        # Log final statistics
        self._log_system_health("SHUTDOWN", self.stats)
        
        # Shutdown bridge
        if self.signal_generator.bridge:
            self.signal_generator.shutdown_bridge()
        
        # Disconnect database
        if self.db_connected:
            self.db.disconnect()
        
        print("Services shutdown complete")
    
    def generate_enhanced_signal(self) -> Optional[Dict[str, Any]]:
        """Generate enhanced signal with more sophisticated logic"""
        
        # Check if it's a new day and reset counters
        current_date = datetime.now().date()
        if self.daily_signal_count['date'] != current_date:
            self.reset_daily_counts()
        
        # Select strategy based on current conditions
        strategy_name = self._select_optimal_strategy()
        
        if not strategy_name:
            return None  # No suitable strategy for current conditions
        
        strategy_config = self.enhanced_strategies[strategy_name]
        
        # Check daily signal limits
        if self.daily_signal_count['by_strategy'][strategy_name] >= strategy_config['max_daily_signals']:
            return None  # Daily limit reached for this strategy
        
        # Check active hours
        current_hour = datetime.now().hour
        start_hour, end_hour = strategy_config['active_hours']
        if not (start_hour <= current_hour <= end_hour):
            return None  # Outside active hours
        
        # Select currency pair based on strategy
        pair = self._select_pair_for_strategy(strategy_name)
        
        # Check minimum interval since last signal for this pair
        if not self._can_signal_pair(pair):
            return None
        
        # Generate signal parameters
        confidence_min, confidence_max = strategy_config['confidence_range']
        sl_min, sl_max = strategy_config['sl_range']
        tp_min, tp_max = strategy_config['tp_range']
        
        signal = {
            'uuid': str(uuid.uuid4()),
            'symbol': pair,
            'direction': random.choice(['BUY', 'SELL']),
            'confidence': round(random.uniform(confidence_min, confidence_max), 3),
            'strategy_name': strategy_name,
            'stop_loss_points': random.randint(sl_min, sl_max),
            'take_profit_points': random.randint(tp_min, tp_max),
            'generated_at': datetime.now(),
            'market_conditions': strategy_config['market_conditions'],
            'metadata': {
                'service_version': self.version,
                'daily_signal_number': self.daily_signal_count['by_strategy'][strategy_name] + 1,
                'enhanced_features': True
            }
        }
        
        # Update tracking
        self.daily_signal_count['by_strategy'][strategy_name] += 1
        self.signal_generator.last_signal_time[pair] = datetime.now()
        
        return signal
    
    def _select_optimal_strategy(self) -> Optional[str]:
        """Select optimal strategy based on current market conditions"""
        
        # Simple time-based strategy selection for demo
        current_hour = datetime.now().hour
        
        if 8 <= current_hour <= 12:  # Morning - trend following
            return "trend_following_v2"
        elif 12 <= current_hour <= 16:  # Afternoon - momentum
            return "momentum_scalp"
        elif 16 <= current_hour <= 20:  # Evening - reversal
            return "reversal_hunter"
        else:
            return None  # Quiet hours
    
    def _select_pair_for_strategy(self, strategy_name: str) -> str:
        """Select currency pair based on strategy"""
        
        strategy_pairs = {
            "trend_following_v2": ["EURUSD", "GBPUSD", "USDJPY"],
            "momentum_scalp": ["EURUSD", "GBPUSD", "USDCHF"],
            "reversal_hunter": ["EURUSD", "USDJPY", "AUDUSD"]
        }
        
        return random.choice(strategy_pairs.get(strategy_name, ["EURUSD"]))
    
    def _can_signal_pair(self, pair: str) -> bool:
        """Check if enough time has passed for this pair"""
        if pair not in self.signal_generator.last_signal_time:
            return True
        
        last_signal = self.signal_generator.last_signal_time[pair]
        time_diff = (datetime.now() - last_signal).total_seconds()
        
        # Minimum 2 minutes between signals for same pair
        return time_diff >= 120
    
    def process_signal(self, signal: Dict[str, Any]) -> bool:
        """Process a signal through the complete pipeline"""
        
        try:
            # Step 1: Log signal to database
            if self.db_connected:
                signal_uuid = self.db.log_signal(signal)
                if not signal_uuid:
                    self.stats['database_errors'] += 1
                    print(f"⚠️  Failed to log signal to database")
                    return False
                
                signal['uuid'] = signal_uuid
            
            # Step 2: Send signal to bridge
            bridge_success = self.signal_generator.send_signal_to_bridge(signal)
            
            if bridge_success:
                self.stats['signals_sent'] += 1
                
                # Step 3: Mark signal as sent in database
                if self.db_connected:
                    self.db.mark_signal_sent(signal['uuid'])
                
                print(f"✓ Signal processed successfully: {signal['symbol']} {signal['direction']} "
                      f"(strategy: {signal['strategy_name']}, confidence: {signal['confidence']})")
                
                return True
            else:
                self.stats['bridge_errors'] += 1
                print(f"✗ Failed to send signal to bridge")
                return False
        
        except Exception as e:
            print(f"✗ Error processing signal: {e}")
            return False
    
    def _log_system_health(self, event_type: str, data: Dict[str, Any]):
        """Log system health and events to database"""
        if not self.db_connected:
            return
        
        try:
            health_data = {
                'cpu_usage': None,  # Could add system monitoring here
                'memory_usage': None,
                'response_time_ms': None,
                'error_count': self.stats.get('database_errors', 0) + self.stats.get('bridge_errors', 0),
                'additional_info': {
                    'event_type': event_type,
                    'data': data,
                    'stats': self.stats
                }
            }
            
            status = "HEALTHY"
            if health_data['error_count'] > 10:
                status = "DEGRADED"
            elif health_data['error_count'] > 50:
                status = "CRITICAL"
            
            self.db.log_system_health(self.service_name, status, health_data)
            
        except Exception as e:
            print(f"Failed to log system health: {e}")
    
    def print_detailed_status(self):
        """Print detailed service status"""
        uptime = datetime.now() - self.stats['uptime_start']
        
        print(f"\n=== {self.service_name} Status ===")
        print(f"Version: {self.version}")
        print(f"Uptime: {uptime}")
        print(f"Started: {self.stats['uptime_start'].strftime('%Y-%m-%d %H:%M:%S')}")
        
        print(f"\nSignal Statistics:")
        print(f"  Generated: {self.stats['signals_generated']}")
        print(f"  Sent to Bridge: {self.stats['signals_sent']}")
        print(f"  Success Rate: {(self.stats['signals_sent'] / max(self.stats['signals_generated'], 1) * 100):.1f}%")
        
        print(f"\nError Statistics:")
        print(f"  Database Errors: {self.stats['database_errors']}")
        print(f"  Bridge Errors: {self.stats['bridge_errors']}")
        
        print(f"\nDaily Signal Count ({self.daily_signal_count['date']}):")
        for strategy, count in self.daily_signal_count['by_strategy'].items():
            max_daily = self.enhanced_strategies[strategy]['max_daily_signals']
            print(f"  {strategy}: {count}/{max_daily}")
        
        # Bridge status
        if self.signal_generator.bridge:
            bridge_status = self.signal_generator.get_bridge_status()
            print(f"\nBridge Status:")
            print(f"  Status: {bridge_status['status']}")
            print(f"  Queue: {bridge_status['message_count']} messages")
        
        # Database statistics
        if self.db_connected:
            try:
                db_stats = self.db.get_database_stats()
                print(f"\nDatabase Statistics:")
                print(f"  Signals (24h): {db_stats.get('signals_last_24h', 'N/A')}")
                print(f"  Trades (24h): {db_stats.get('trades_last_24h', 'N/A')}")
                print(f"  DB Size: {db_stats.get('db_size_mb', 'N/A')} MB")
            except Exception as e:
                print(f"  Database stats error: {e}")
        
        print("=" * 40)
    
    def run_continuous_enhanced(self, signal_interval: int = 90, status_interval: int = 300):
        """Run enhanced continuous signal generation"""
        
        print(f"\n=== Starting Enhanced Signal Service ===")
        print(f"Signal interval: {signal_interval} seconds")
        print(f"Status interval: {status_interval} seconds")
        print(f"Enhanced strategies: {len(self.enhanced_strategies)}")
        print("Press Ctrl+C to stop\n")
        
        # Set up graceful shutdown
        def signal_handler(signum, frame):
            print("\nReceived stop signal. Shutting down gracefully...")
            self.signal_generator.running = False
        
        signal.signal(signal.SIGINT, signal_handler)
        
        self.signal_generator.running = True
        last_status_time = time.time()
        
        try:
            while self.signal_generator.running:
                current_time = time.time()
                
                # Generate enhanced signal
                enhanced_signal = self.generate_enhanced_signal()
                
                if enhanced_signal:
                    self.stats['signals_generated'] += 1
                    
                    # Process through complete pipeline
                    success = self.process_signal(enhanced_signal)
                    
                    if not success:
                        print("⚠️  Signal processing failed")
                else:
                    print("ℹ️  No signal generated (conditions not met)")
                
                # Print status update periodically
                if current_time - last_status_time >= status_interval:
                    self.print_detailed_status()
                    
                    # Log periodic health check
                    self._log_system_health("PERIODIC_CHECK", {
                        'signals_in_interval': self.stats['signals_generated']
                    })
                    
                    last_status_time = current_time
                
                # Wait for next signal
                time.sleep(signal_interval)
        
        except KeyboardInterrupt:
            print("\nStopping enhanced signal service...")
        
        self.signal_generator.running = False
        print("Enhanced signal service stopped")
    
    def run_analysis_mode(self):
        """Run in analysis mode - show database insights"""
        print("\n=== Database Analysis Mode ===")
        
        if not self.db_connected:
            print("Database not connected")
            return
        
        try:
            # Recent signals analysis
            signals = self.db.get_signals(limit=20)
            print(f"\nRecent Signals: {len(signals)}")
            
            if signals:
                strategies = {}
                for sig in signals:
                    strategy = sig['strategy_name']
                    strategies[strategy] = strategies.get(strategy, 0) + 1
                
                print("Strategy distribution:")
                for strategy, count in strategies.items():
                    print(f"  {strategy}: {count}")
            
            # Strategy performance
            strategy_perf = self.db.get_strategy_performance(days=7)
            print(f"\nStrategy Performance (7 days): {len(strategy_perf)} strategies")
            
            for perf in strategy_perf:
                print(f"  {perf['strategy_name']}:")
                print(f"    Signals: {perf['signals_generated']}")
                print(f"    Trades: {perf['trades_executed']}")
                print(f"    Conversion: {perf.get('conversion_rate', 0):.1f}%")
                print(f"    P&L: ${perf['total_pnl']:.2f}")
                print(f"    Win Rate: {perf.get('win_rate', 0):.1f}%")
            
            # Daily performance
            daily_perf = self.db.calculate_daily_performance()
            print(f"\nToday's Performance:")
            print(f"  Total Trades: {daily_perf.get('total_trades', 0)}")
            print(f"  Total P&L: ${daily_perf.get('total_pnl', 0):.2f}")
            print(f"  Win Rate: {daily_perf.get('win_rate', 0):.1f}%")
            
            # System health
            health = self.db.get_system_health_status()
            print(f"\nSystem Health: {health.get('overall_status', 'UNKNOWN')}")
            for component in health.get('components', []):
                print(f"  {component['component']}: {component['status']}")
        
        except Exception as e:
            print(f"Analysis error: {e}")

def main():
    """Main function for enhanced signal service"""
    print("=== HUEY_P Enhanced Trading Signal Service ===")
    
    # Create enhanced service
    service = EnhancedTradingSignalService()
    
    # Initialize services
    if not service.initialize_services():
        print("Failed to initialize services. Exiting.")
        return
    
    try:
        # Service menu
        while True:
            print("\nEnhanced Signal Service Options:")
            print("1. Run continuous enhanced signal generation")
            print("2. Run analysis mode (database insights)")
            print("3. Generate single enhanced signal")
            print("4. Show service status")
            print("5. Test database connection")
            print("6. Exit")
            
            choice = input("Enter choice (1-6): ").strip()
            
            if choice == "1":
                try:
                    interval = int(input("Signal interval in seconds (default 90): ") or "90")
                    service.run_continuous_enhanced(signal_interval=interval)
                except ValueError:
                    print("Invalid interval. Using default of 90 seconds.")
                    service.run_continuous_enhanced()
            
            elif choice == "2":
                service.run_analysis_mode()
            
            elif choice == "3":
                signal_data = service.generate_enhanced_signal()
                if signal_data:
                    print(f"Generated enhanced signal:")
                    for key, value in signal_data.items():
                        if key != 'metadata':
                            print(f"  {key}: {value}")
                    
                    # Ask if user wants to process it
                    process = input("Process this signal? (y/n): ").lower() == 'y'
                    if process:
                        success = service.process_signal(signal_data)
                        print(f"Processing result: {'Success' if success else 'Failed'}")
                else:
                    print("No signal generated (conditions not met)")
            
            elif choice == "4":
                service.print_detailed_status()
            
            elif choice == "5":
                if service.db_connected:
                    stats = service.db.get_database_stats()
                    print("Database connection: ✓ Connected")
                    print(f"Database stats: {stats}")
                else:
                    print("Database connection: ✗ Not connected")
            
            elif choice == "6":
                break
            
            else:
                print("Invalid choice. Please enter 1-6.")
    
    finally:
        # Cleanup
        service.shutdown_services()
        print("Enhanced signal service stopped.")

if __name__ == "__main__":
    main()
```

**Test the complete enhanced system:**
```powershell
cd C:\TradingSystem\Source\Python

# First test database operations
python HUEY_P_PY_database_manager.py

# Then test enhanced signal service
python HUEY_P_PY_enhanced_signal_service.py
# Choose option 4 to see status, then option 3 to generate a signal
```

**14.4 Create Database Reporting Dashboard (3-4 hours)**

Create: `C:\TradingSystem\Source\Python\HUEY_P_PY_trading_dashboard.py`

```python
# HUEY_P_PY_trading_dashboard.py
# Simple text-based trading dashboard with database insights

import time
import os
from datetime import datetime, date, timedelta
from typing import Dict, List, Any

from HUEY_P_PY_database_manager import TradingDatabaseManager

class TradingDashboard:
    def __init__(self):
        """Initialize trading dashboard"""
        self.db = TradingDatabaseManager()
        self.db_connected = False
        self.last_update = None
        
        # Dashboard configuration
        self.refresh_interval = 30  # seconds
        self.auto_refresh = False
        
        print("Trading Dashboard initialized")
    
    def connect_database(self) -> bool:
        """Connect to trading database"""
        try:
            if self.db.connect():
                self.db_connected = True
                print("✓ Database connected")
                return True
            else:
                print("✗ Database connection failed")
                return False
        except Exception as e:
            print(f"✗ Database connection error: {e}")
            return False
    
    def clear_screen(self):
        """Clear the console screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self):
        """Print dashboard header"""
        print("=" * 80)
        print(" " * 25 + "HUEY_P TRADING DASHBOARD")
        print("=" * 80)
        print(f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
    
    def show_overview(self):
        """Show trading overview"""
        try:
            # Get database stats
            stats = self.db.get_database_stats()
            
            # Get today's performance
            today_perf = self.db.calculate_daily_performance()
            
            # Get open positions
            open_trades = self.db.get_open_trades()
            
            print("📊 TRADING OVERVIEW")
            print("-" * 40)
            print(f"Database Size: {stats.get('db_size_mb', 'N/A')} MB")
            print(f"Total Signals: {stats.get('signals_count', 0):,}")
            print(f"Total Trades: {stats.get('trades_count', 0):,}")
            print()
            
            print("📈 TODAY'S PERFORMANCE")
            print("-" * 40)
            print(f"Trades: {today_perf.get('total_trades', 0)}")
            print(f"P&L: ${today_perf.get('total_pnl', 0):.2f}")
            print(f"Win Rate: {today_perf.get('win_rate', 0):.1f}%")
            print()
            
            print("🔴 OPEN POSITIONS")
            print("-" * 40)
            if open_trades:
                for trade in open_trades[:5]:  # Show first 5
                    hours_open = (datetime.now() - datetime.fromisoformat(trade['opened_at'])).total_seconds() / 3600
                    print(f"#{trade['mt4_ticket']} {trade['symbol']} {trade['direction']} "
                          f"{trade['lot_size']} lots ({hours_open:.1f}h)")
                
                if len(open_trades) > 5:
                    print(f"... and {len(open_trades) - 5} more")
            else:
                print("No open positions")
            
            print()
            
        except Exception as e:
            print(f"Error showing overview: {e}")
    
    def show_recent_signals(self, limit: int = 10):
        """Show recent signals"""
        try:
            signals = self.db.get_signals(limit=limit)
            
            print("📡 RECENT SIGNALS")
            print("-" * 80)
            print(f"{'Time':<20} {'Symbol':<8} {'Dir':<4} {'Conf':<6} {'Strategy':<15} {'SL':<4} {'TP':<4}")
            print("-" * 80)
            
            for signal in signals:
                generated_at = datetime.fromisoformat(signal['generated_at'])
                time_str = generated_at.strftime('%m-%d %H:%M:%S')
                
                print(f"{time_str:<20} {signal['symbol']:<8} {signal['direction']:<4} "
                      f"{signal['confidence']:<6.2f} {signal['strategy_name']:<15} "
                      f"{signal['stop_loss_points'] or 'N/A':<4} {signal['take_profit_points'] or 'N/A':<4}")
            
            print()
            
        except Exception as e:
            print(f"Error showing recent signals: {e}")
    
    def show_strategy_performance(self, days: int = 7):
        """Show strategy performance analysis"""
        try:
            strategy_perf = self.db.get_strategy_performance(days=days)
            
            print(f"🎯 STRATEGY PERFORMANCE ({days} days)")
            print("-" * 80)
            print(f"{'Strategy':<20} {'Signals':<8} {'Trades':<7} {'Conv%':<6} {'P&L':<10} {'Win%':<6}")
            print("-" * 80)
            
            for perf in strategy_perf:
                conv_rate = perf.get('conversion_rate', 0)
                win_rate = perf.get('win_rate', 0)
                pnl = perf['total_pnl']
                
                print(f"{perf['strategy_name']:<20} {perf['signals_generated']:<8} "
                      f"{perf['trades_executed']:<7} {conv_rate:<6.1f} "
                      f"${pnl:<9.2f} {win_rate:<6.1f}")
            
            print()
            
        except Exception as e:
            print(f"Error showing strategy performance: {e}")
    
    def show_daily_summary(self, days: int = 7):
        """Show daily trading summary"""
        try:
            print(f"📅 DAILY SUMMARY (Last {days} days)")
            print("-" * 70)
            print(f"{'Date':<12} {'Trades':<7} {'P&L':<10} {'Win%':<6} {'Best':<8} {'Worst':<8}")
            print("-" * 70)
            
            for i in range(days):
                check_date = date.today() - timedelta(days=i)
                daily_perf = self.db.calculate_daily_performance(check_date)
                
                if daily_perf.get('total_trades', 0) > 0:
                    # Calculate best and worst from pair data
                    best_pnl = 0
                    worst_pnl = 0
                    
                    for pair_data in daily_perf.get('by_pair', []):
                        if pair_data['total_pnl'] > best_pnl:
                            best_pnl = pair_data['total_pnl']
                        if pair_data['total_pnl'] < worst_pnl:
                            worst_pnl = pair_data['total_pnl']
                    
                    print(f"{check_date.strftime('%m-%d'):<12} "
                          f"{daily_perf['total_trades']:<7} "
                          f"${daily_perf['total_pnl']:<9.2f} "
                          f"{daily_perf['win_rate']:<6.1f} "
                          f"${best_pnl:<7.2f} ${worst_pnl:<7.2f}")
                else:
                    print(f"{check_date.strftime('%m-%d'):<12} {'0':<7} {'$0.00':<10} {'N/A':<6} {'N/A':<8} {'N/A':<8}")
            
            print()
            
        except Exception as e:
            print(f"Error showing daily summary: {e}")
    
    def show_system_health(self):
        """Show system health status"""
        try:
            health = self.db.get_system_health_status()
            
            print("🏥 SYSTEM HEALTH")
            print("-" * 50)
            print(f"Overall Status: {health.get('overall_status', 'UNKNOWN')}")
            print()
            
            components = health.get('components', [])
            if components:
                print(f"{'Component':<20} {'Status':<10} {'Last Update':<20}")
                print("-" * 50)
                
                for comp in components:
                    last_update = comp['recorded_at']
                    if last_update:
                        update_time = datetime.fromisoformat(last_update)
                        time_ago = datetime.now() - update_time
                        if time_ago.total_seconds() < 3600:  # Less than 1 hour
                            time_str = f"{int(time_ago.total_seconds() / 60)}m ago"
                        else:
                            time_str = f"{int(time_ago.total_seconds() / 3600)}h ago"
                    else:
                        time_str = "Never"
                    
                    print(f"{comp['component']:<20} {comp['status']:<10} {time_str:<20}")
            else:
                print("No health data available")
            
            print()
            
        except Exception as e:
            print(f"Error showing system health: {e}")
    
    def show_trade_analysis(self):
        """Show detailed trade analysis"""
        try:
            # Get recent trades
            recent_trades = self.db.get_trade_history(days=7)
            
            print("💹 TRADE ANALYSIS (7 days)")
            print("-" * 80)
            
            if not recent_trades:
                print("No trades in the last 7 days")
                print()
                return
            
            # Calculate statistics
            total_trades = len(recent_trades)
            winning_trades = [t for t in recent_trades if t['pnl'] > 0]
            losing_trades = [t for t in recent_trades if t['pnl'] < 0]
            
            total_pnl = sum(t['pnl'] for t in recent_trades)
            avg_win = sum(t['pnl'] for t in winning_trades) / len(winning_trades) if winning_trades else 0
            avg_loss = sum(t['pnl'] for t in losing_trades) / len(losing_trades) if losing_trades else 0
            
            win_rate = len(winning_trades) / total_trades * 100 if total_trades > 0 else 0
            
            print(f"Total Trades: {total_trades}")
            print(f"Winning Trades: {len(winning_trades)} ({win_rate:.1f}%)")
            print(f"Losing Trades: {len(losing_trades)}")
            print(f"Total P&L: ${total_pnl:.2f}")
            print(f"Average Win: ${avg_win:.2f}")
            print(f"Average Loss: ${avg_loss:.2f}")
            
            if avg_loss != 0:
                profit_factor = abs(avg_win * len(winning_trades)) / abs(avg_loss * len(losing_trades))
                print(f"Profit Factor: {profit_factor:.2f}")
            
            print()
            
            # Show recent trades
            print("Recent Trades:")
            print(f"{'Date':<12} {'Symbol':<8} {'Dir':<4} {'Size':<6} {'P&L':<8} {'Status':<8}")
            print("-" * 60)
            
            for trade in recent_trades[:10]:  # Show last 10
                opened_date = datetime.fromisoformat(trade['opened_at']).strftime('%m-%d %H:%M')
                pnl_str = f"${trade['pnl']:.2f}" if trade['pnl'] else "Open"
                
                print(f"{opened_date:<12} {trade['symbol']:<8} {trade['direction']:<4} "
                      f"{trade['lot_size']:<6.2f} {pnl_str:<8} {trade['status']:<8}")
            
            print()
            
        except Exception as e:
            print(f"Error showing trade analysis: {e}")
    
    def display_full_dashboard(self):
        """Display the complete dashboard"""
        if not self.db_connected:
            print("❌ Database not connected. Please connect first.")
            return
        
        self.clear_screen()
        self.print_header()
        
        try:
            self.show_overview()
            self.show_recent_signals(5)
            self.show_strategy_performance(7)
            self.show_daily_summary(5)
            self.show_system_health()
            
            print("=" * 80)
            print("Commands: (r)efresh | (f)ull analysis | (h)elp | (q)uit")
            
            self.last_update = datetime.now()
            
        except Exception as e:
            print(f"Error displaying dashboard: {e}")
    
    def run_interactive(self):
        """Run interactive dashboard"""
        print("🚀 Starting Interactive Trading Dashboard")
        print("Commands: (r)efresh | (a)uto refresh | (f)ull analysis | (h)elp | (q)uit")
        print()
        
        if not self.connect_database():
            return
        
        # Initial display
        self.display_full_dashboard()
        
        while True:
            try:
                if self.auto_refresh:
                    print(f"\nAuto-refresh in {self.refresh_interval}s... (Press Enter to stop)")
                    
                    # Wait for input or timeout
                    import select
                    import sys
                    
                    ready, _, _ = select.select([sys.stdin], [], [], self.refresh_interval)
                    
                    if ready:
                        command = sys.stdin.readline().strip().lower()
                        if command:
                            self.auto_refresh = False
                    else:
                        command = 'r'  # Auto refresh
                else:
                    command = input("\nEnter command: ").strip().lower()
                
                if command == 'q' or command == 'quit':
                    break
                
                elif command == 'r' or command == 'refresh':
                    self.display_full_dashboard()
                
                elif command == 'a' or command == 'auto':
                    self.auto_refresh = not self.auto_refresh
                    status = "enabled" if self.auto_refresh else "disabled"
                    print(f"Auto-refresh {status}")
                    
                    if self.auto_refresh:
                        self.display_full_dashboard()
                
                elif command == 'f' or command == 'full':
                    self.clear_screen()
                    self.print_header()
                    self.show_overview()
                    self.show_recent_signals(15)
                    self.show_strategy_performance(14)
                    self.show_daily_summary(14)
                    self.show_trade_analysis()
                    self.show_system_health()
                
                elif command == 'h' or command == 'help':
                    print("\n📖 Dashboard Commands:")
                    print("  r, refresh    - Refresh dashboard display")
                    print("  a, auto       - Toggle auto-refresh mode")
                    print("  f, full       - Show full analysis")
                    print("  h, help       - Show this help")
                    print("  q, quit       - Exit dashboard")
                
                else:
                    if command:
                        print(f"Unknown command: {command}. Type 'h' for help.")
            
            except KeyboardInterrupt:
                print("\n\n👋 Dashboard stopped by user")
                break
            
            except Exception as e:
                print(f"\n❌ Dashboard error: {e}")
                print("Type 'q' to quit or 'r' to refresh")
        
        self.db.disconnect()
        print("\n✅ Dashboard session ended")

def main():
    """Main function for trading dashboard"""
    dashboard = TradingDashboard()
    
    try:
        dashboard.run_interactive()
    except Exception as e:
        print(f"Dashboard startup error: {e}")

if __name__ == "__main__":
    main()
```

**Test the complete system:**
```powershell
# Terminal 1: Start the enhanced signal service
cd C:\TradingSystem\Source\Python
python HUEY_P_PY_enhanced_signal_service.py
# Choose option 1 for continuous generation

# Terminal 2: Start the dashboard
python HUEY_P_PY_trading_dashboard.py
# Use 'a' for auto-refresh to see real-time updates

# Terminal 3: Test MT4 EA
# Open MT4, attach HUEY_P_MQL4_signal_processor to EURUSD chart
# Watch it receive and process signals
```

---

## **VALIDATION & TESTING CHECKLIST**

After completing Phase 2, you should have:

### **✅ Working Components:**
- [ ] Database schema created and functional
- [ ] Enhanced signal service generating varied signals
- [ ] Database manager logging all signals and trades
- [ ] Dashboard showing real-time system status
- [ ] MT4 EA processing signals with database integration

### **✅ Integration Tests:**
1. **Signal Flow Test:**
   ```
   Python generates signal → Database logs it → Bridge sends it → MT4 receives it → Database logs trade
   ```

2. **Database Operations Test:**
   ```
   All CRUD operations work
   Performance metrics calculated correctly
   System health monitoring functional
   ```

3. **Error Handling Test:**
   ```
   Database connection fails gracefully
   Bridge failures trigger fallbacks
   Invalid signals are rejected
   ```

### **✅ Performance Benchmarks:**
- Signal generation to MT4 receipt: < 100ms
- Database operations: < 50ms each
- Dashboard refresh: < 2 seconds
- System can handle 1 signal per minute continuously

---

## **NEXT PHASE PREVIEW**

**Phase 3 (Week 13-16): Production-Ready System**
- Real market data integration
- Advanced ML models
- Complete 30-pair deployment
- Production monitoring
- Performance optimization

This roadmap has taken you from complete beginner to having a working, database-integrated trading system. Each step builds practical skills while creating real, functional components that work together as a complete trading platform.

The system you've built is already quite sophisticated and demonstrates all the key concepts needed for algorithmic trading systems. With the foundation you now have, you're ready to tackle more advanced features and eventually deploy a production trading system.		