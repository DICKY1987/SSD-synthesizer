# HUEY_P Communication System - Comprehensive Troubleshooting Guide

## Quick Diagnostic Checklist

### **🔍 System Health Check (Run First)**
```bash
# Navigate to project directory
cd "C:\Users\Richard Wilks\Downloads\EEE\documentaion\eafix"

# Run comprehensive diagnostic
python simple_socket_test.py

# Expected output indicators:
# ✅ mt4_running: OK: PASS
# ✅ dll_available: OK: PASS  
# ❌ socket_5555: FAIL (Expected if EA not configured)
# ❌ socket_9999: FAIL (Expected if EA not configured)
# ✅ csv_communication: OK: PASS
```

### **⚡ Quick Status Summary**
| Component | Expected Status | Action if Failed |
|-----------|----------------|------------------|
| MT4 Terminal | RUNNING | Start MetaTrader 4 |
| DLL Available | AVAILABLE | Check DLL location |
| CSV Communication | WORKING | Check file permissions |
| Socket Communication | INACTIVE (normal) | Configure EA for socket mode |

---

## Problem Categories and Solutions

## 🔧 **1. CSV Communication Issues**

### **Problem: Signals not being processed**
**Symptoms:**
- Python creates CSV files successfully
- EA shows no signal activity in logs
- No responses in `trade_responses.csv`

#### **Diagnosis Steps:**
```bash
# 1. Check if CSV files are being created
ls -la "C:\Users\...\eafix\trading_signals.csv"

# 2. Verify EA is running and configured
# Open MT4 → Experts tab → Look for HUEY_P EA messages

# 3. Check EA configuration
# EA should show: "CSV monitoring enabled" in logs
```

#### **Solution Checklist:**
- [ ] ✅ **EA Configuration**: Ensure EA parameters are set:
  ```
  EnableCSVSignals = true
  EnableDLLSignals = false
  AutonomousMode = false
  CSVSignalFile = eafix\trading_signals.csv
  TimerIntervalSeconds = 15
  ```
- [ ] ✅ **EA Loaded**: Verify HUEY_P EA is active on a chart (green smiley face)
- [ ] ✅ **File Permissions**: MT4 must have read/write access to eafix directory
- [ ] ✅ **File Format**: CSV must match exact schema (see CSV_COMMUNICATION_PROTOCOL.md)

#### **Advanced Troubleshooting:**
```mql4
// Add to EA code for debugging CSV processing
void CheckCSVConfiguration() {
    Print("=== CSV Configuration Debug ===");
    Print("EnableCSVSignals: ", EnableCSVSignals);
    Print("CSVSignalFile: ", CSVSignalFile);
    Print("File exists: ", FileIsExist(CSVSignalFile));
    Print("Timer interval: ", TimerIntervalSeconds);
    Print("Last check time: ", TimeToString(lastCSVCheckTime));
    Print("===============================");
}
```

### **Problem: CSV files corrupted or empty**
**Symptoms:**
- Files created but contain no data
- "File access denied" errors in logs
- Partial signal data

#### **Root Causes and Solutions:**
1. **File Locking Issues**
   ```python
   # Python: Use atomic writes
   import tempfile
   
   def atomic_csv_write(file_path, data):
       temp_file = file_path + '.tmp'
       with open(temp_file, 'w', newline='') as f:
           writer = csv.writer(f)
           writer.writerows(data)
       
       # Atomic move
       os.replace(temp_file, file_path)
   ```

2. **Antivirus Interference**
   - Add MT4 directory to antivirus exclusions
   - Exclude `*.csv` files from real-time scanning

3. **Insufficient Permissions**
   ```bash
   # Windows: Run MT4 as Administrator
   # Or change folder permissions for MT4 data directory
   ```

### **Problem: High CSV communication latency**
**Symptoms:**
- Signals processed with >30 second delays
- Trade responses arrive very slowly

#### **Optimization Solutions:**
1. **Reduce Timer Interval**
   ```mql4
   // In EA parameters
   TimerIntervalSeconds = 5  // Minimum recommended: 5 seconds
   ```

2. **File System Optimization**
   ```python
   # Python: Use file watchers instead of polling
   from watchdog.observers import Observer
   from watchdog.events import FileSystemEventHandler
   
   class CSVFileWatcher(FileSystemEventHandler):
       def on_modified(self, event):
           if event.src_path.endswith('trade_responses.csv'):
               process_new_responses()
   ```

3. **Batch Processing**
   ```python
   # Process multiple signals in single CSV write
   def batch_signal_sender(signals, batch_size=5):
       for i in range(0, len(signals), batch_size):
           batch = signals[i:i+batch_size]
           write_signal_batch(batch)
   ```

---

## 🔌 **2. Socket Communication Issues**

### **Problem: Connection refused (Error 10061)**
**Symptoms:**
- Python client cannot connect to EA
- `simple_socket_test.py` shows FAIL for socket tests
- "No connection could be made" errors

#### **Diagnosis Steps:**
```bash
# 1. Check if EA is listening on ports
netstat -an | findstr :5555
netstat -an | findstr :9999

# 2. Verify MT4 is running
tasklist | findstr terminal.exe

# 3. Check Windows Firewall
# Windows Firewall → Allow an app → MetaTrader 4
```

#### **Step-by-Step Resolution:**

**Step 1: Verify EA is Loaded and Configured**
```mql4
// EA must have these settings:
EnableDLLSignals = true    // Enable socket communication
EnableCSVSignals = false   // Disable CSV (optional)
AutonomousMode = false     // Allow external signals
```

**Step 2: Enable DLL Imports in MT4**
1. Open MetaTrader 4
2. Tools → Options → Expert Advisors
3. ✅ Check "Allow DLL imports"
4. ✅ Check "Allow WebRequest for listed URL" (if using web features)

**Step 3: Verify DLL Location**
```bash
# DLL must be in correct location
dir "C:\Users\...\Terminal\...\MQL4\Libraries\MQL4_DLL_SocketBridge.dll"

# DLL should be ~31KB Win32 PE executable
```

**Step 4: Check EA Logs for DLL Initialization**
```mql4
// EA should show in Experts tab:
// "Socket initialized successfully on port: 5555"
// OR
// "Socket initialized successfully on alternative port: 9999"
```

### **Problem: DLL initialization fails**
**Symptoms:**
- EA logs show "Socket initialization failed"
- DLL import errors in Expert logs
- Socket functions return error codes

#### **DLL Troubleshooting Matrix:**

| Error Message | Cause | Solution |
|--------------|-------|----------|
| "DLL not found" | Missing DLL file | Copy DLL to MQL4/Libraries/ |
| "Invalid DLL format" | Wrong architecture | Rebuild DLL as Win32 |
| "Access denied" | Permissions issue | Run MT4 as Administrator |
| "DLL imports disabled" | MT4 settings | Enable DLL imports in Options |
| "Function not found" | DLL corruption | Rebuild DLL from source |

#### **DLL Rebuild Process:**
```bash
# 1. Navigate to DLL source
cd "C:\Users\...\eafix\MQL4_DLL_SocketBridge"

# 2. Clean previous builds
rmdir build /s /q

# 3. Create build directory
mkdir build
cd build

# 4. Generate VS project (Win32 architecture)
cmake .. -G "Visual Studio 17 2022" -A Win32

# 5. Build release version
cmake --build . --config Release

# 6. Copy to MT4 Libraries
copy Release\MQL4_DLL_SocketBridge.dll "C:\Users\...\MQL4\Libraries\"

# 7. Verify DLL
file MQL4_DLL_SocketBridge.dll
# Should show: "PE32 executable (DLL) Intel 80386"
```

### **Problem: Socket connection drops frequently**
**Symptoms:**
- Initial connection succeeds but drops after minutes
- Intermittent "Connection lost" messages
- Heartbeat failures

#### **Connection Stability Solutions:**

1. **Implement Robust Reconnection Logic**
   ```python
   class RobustSocketClient:
       def __init__(self):
           self.max_retries = 5
           self.retry_delay = 10  # seconds
           
       def connect_with_retry(self):
           for attempt in range(self.max_retries):
               try:
                   if self.connect():
                       return True
               except Exception as e:
                   print(f"Connection attempt {attempt + 1} failed: {e}")
                   time.sleep(self.retry_delay * (2 ** attempt))  # Exponential backoff
           return False
   ```

2. **Optimize Heartbeat Settings**
   ```python
   # Reduce heartbeat interval for faster detection
   heartbeat_interval = 15  # seconds (default: 30)
   heartbeat_timeout = 45   # seconds (3x interval)
   ```

3. **Connection Pooling (Advanced)**
   ```python
   class ConnectionPool:
       def __init__(self, pool_size=3):
           self.connections = []
           self.pool_size = pool_size
           
       def get_connection(self):
           # Return healthy connection from pool
           for conn in self.connections:
               if conn.is_healthy():
                   return conn
           
           # Create new connection if pool not full
           if len(self.connections) < self.pool_size:
               new_conn = self.create_connection()
               if new_conn:
                   self.connections.append(new_conn)
                   return new_conn
           
           return None
   ```

---

## 🗃️ **3. Database Connection Issues**

### **Problem: Database schema errors**
**Symptoms:**
- "no such column" errors in Python logs
- Python interface crashes on startup
- Trade history displays empty

#### **Database Repair Process:**
```python
# Run database schema fix
import sqlite3

def fix_database_schema():
    conn = sqlite3.connect('Database/trading_system.db')
    cursor = conn.cursor()
    
    # Add missing columns
    missing_columns = [
        'ALTER TABLE trade_results ADD COLUMN stop_loss REAL',
        'ALTER TABLE trade_results ADD COLUMN take_profit REAL', 
        'ALTER TABLE trade_results ADD COLUMN current_profit REAL'
    ]
    
    for sql in missing_columns:
        try:
            cursor.execute(sql)
            print(f"Added column: {sql}")
        except sqlite3.OperationalError as e:
            if 'duplicate column' not in str(e):
                print(f"Error: {e}")
    
    conn.commit()
    conn.close()

fix_database_schema()
```

### **Problem: Database file corruption**
**Symptoms:**
- "database disk image is malformed" errors
- Python interface won't start
- Trade data appears corrupted

#### **Database Recovery Steps:**
```bash
# 1. Create backup
copy "Database\trading_system.db" "Database\trading_system_corrupted.db"

# 2. Attempt SQLite repair
sqlite3 trading_system.db ".recover" > recovery.sql

# 3. Create new database from recovery
sqlite3 trading_system_repaired.db < recovery.sql

# 4. Replace original
copy "trading_system_repaired.db" "trading_system.db"
```

---

## 🔄 **4. Integration Issues**

### **Problem: Message format mismatches**
**Symptoms:**
- Signals sent but not executed
- "Invalid signal format" errors in EA logs
- Type conversion errors

#### **Message Validation System:**
```python
import jsonschema
from datetime import datetime

# Define signal schema
SIGNAL_SCHEMA = {
    "type": "object",
    "required": ["signal_id", "symbol", "direction", "lot_size"],
    "properties": {
        "signal_id": {"type": "string", "minLength": 1, "maxLength": 50},
        "symbol": {"type": "string", "pattern": "^[A-Z]{6}$"},
        "direction": {"type": "string", "enum": ["BUY", "SELL"]},
        "lot_size": {"type": "number", "minimum": 0.01, "maximum": 100.0},
        "stop_loss": {"type": "integer", "minimum": 0, "maximum": 1000},
        "take_profit": {"type": "integer", "minimum": 0, "maximum": 1000}
    }
}

def validate_signal(signal_data):
    try:
        jsonschema.validate(signal_data, SIGNAL_SCHEMA)
        return True, ""
    except jsonschema.ValidationError as e:
        return False, str(e)

# Usage
is_valid, error_msg = validate_signal(signal_data)
if not is_valid:
    print(f"Signal validation failed: {error_msg}")
```

### **Problem: Timing synchronization issues**
**Symptoms:**
- Signals processed out of order
- Duplicate signal processing
- Race conditions between systems

#### **Synchronization Solutions:**

1. **Signal ID Management**
   ```python
   import threading
   from datetime import datetime
   
   class SignalIDGenerator:
       def __init__(self):
           self.counter = 0
           self.lock = threading.Lock()
           
       def generate_id(self, prefix="SIGNAL"):
           with self.lock:
               self.counter += 1
               timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
               return f"{prefix}_{timestamp}_{self.counter:04d}"
   ```

2. **Message Sequencing**
   ```python
   class SequencedMessageSender:
       def __init__(self):
           self.sequence_number = 0
           
       def send_with_sequence(self, message_data):
           self.sequence_number += 1
           message_data['sequence'] = self.sequence_number
           message_data['timestamp'] = datetime.now().isoformat()
           return self.send_message(message_data)
   ```

3. **Duplicate Detection**
   ```mql4
   // EA-side duplicate detection
   class DuplicateDetector {
   private:
       string processedSignals[];
       datetime cleanupTime;
       
   public:
       bool IsSignalProcessed(string signalId) {
           // Check if signal already processed
           for (int i = 0; i < ArraySize(processedSignals); i++) {
               if (processedSignals[i] == signalId) {
                   return true;
               }
           }
           return false;
       }
       
       void MarkSignalProcessed(string signalId) {
           ArrayResize(processedSignals, ArraySize(processedSignals) + 1);
           processedSignals[ArraySize(processedSignals) - 1] = signalId;
           
           // Cleanup old signals (keep last 1000)
           if (ArraySize(processedSignals) > 1000) {
               ArrayRemove(processedSignals, 0, 100);
           }
       }
   };
   ```

---

## 🚨 **5. System-Wide Diagnostic Tools**

### **Comprehensive System Monitor**
```python
#!/usr/bin/env python3
"""
Advanced HUEY_P System Monitor
Provides real-time diagnostics and health monitoring
"""

import psutil
import sqlite3
import socket
import time
import json
from datetime import datetime
from pathlib import Path

class SystemMonitor:
    def __init__(self, mt4_path):
        self.mt4_path = Path(mt4_path)
        self.monitoring = False
        
    def run_full_diagnostic(self):
        """Run comprehensive system diagnostic"""
        print("🔍 HUEY_P System Diagnostic Report")
        print("=" * 60)
        
        results = {
            'mt4_status': self.check_mt4_status(),
            'dll_status': self.check_dll_status(),
            'database_status': self.check_database_status(),
            'csv_communication': self.check_csv_communication(),
            'socket_communication': self.check_socket_communication(),
            'file_permissions': self.check_file_permissions(),
            'system_resources': self.check_system_resources(),
            'ea_configuration': self.check_ea_configuration()
        }
        
        # Print detailed results
        self.print_diagnostic_results(results)
        
        # Generate recommendations
        self.generate_recommendations(results)
        
        return results
    
    def check_mt4_status(self):
        """Check MetaTrader 4 terminal status"""
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
                if proc.info['name'].lower() == 'terminal.exe':
                    return {
                        'running': True,
                        'pid': proc.info['pid'],
                        'cpu_usage': proc.info['cpu_percent'],
                        'memory_mb': proc.info['memory_info'].rss / 1024 / 1024,
                        'status': 'HEALTHY'
                    }
            
            return {'running': False, 'status': 'NOT_RUNNING'}
        except Exception as e:
            return {'running': False, 'error': str(e), 'status': 'ERROR'}
    
    def check_database_status(self):
        """Check database connectivity and schema"""
        db_path = self.mt4_path / "eafix" / "Database" / "trading_system.db"
        
        try:
            conn = sqlite3.connect(str(db_path), timeout=5)
            cursor = conn.cursor()
            
            # Check required tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            required_tables = ['trades', 'trade_results', 'system_status', 'error_log']
            missing_tables = [table for table in required_tables if table not in tables]
            
            # Check trade_results schema
            cursor.execute("PRAGMA table_info(trade_results)")
            columns = [row[1] for row in cursor.fetchall()]
            
            required_columns = ['stop_loss', 'take_profit', 'current_profit']
            missing_columns = [col for col in required_columns if col not in columns]
            
            conn.close()
            
            return {
                'accessible': True,
                'tables': len(tables),
                'missing_tables': missing_tables,
                'missing_columns': missing_columns,
                'status': 'HEALTHY' if not missing_tables and not missing_columns else 'NEEDS_REPAIR'
            }
            
        except Exception as e:
            return {
                'accessible': False,
                'error': str(e),
                'status': 'ERROR'
            }
    
    def check_csv_communication(self):
        """Test CSV communication system"""
        signals_file = self.mt4_path / "eafix" / "trading_signals.csv"
        responses_file = self.mt4_path / "eafix" / "trade_responses.csv"
        
        try:
            # Test write access
            test_signal = {
                'signal_id': f'TEST_{int(time.time())}',
                'symbol': 'EURUSD',
                'direction': 'BUY',
                'lot_size': 0.01,
                'stop_loss': 20,
                'take_profit': 40,
                'comment': 'Diagnostic Test',
                'timestamp': datetime.now().isoformat(),
                'confidence': 0.5,
                'strategy_id': 99999
            }
            
            # Write test signal
            with open(signals_file, 'w', newline='') as f:
                import csv
                writer = csv.DictWriter(f, fieldnames=test_signal.keys())
                writer.writeheader()
                writer.writerow(test_signal)
            
            # Check if responses file is accessible
            responses_accessible = responses_file.exists()
            if responses_accessible:
                with open(responses_file, 'r') as f:
                    pass  # Just check read access
            
            return {
                'signals_writable': True,
                'responses_accessible': responses_accessible,
                'test_signal_id': test_signal['signal_id'],
                'status': 'FUNCTIONAL'
            }
            
        except Exception as e:
            return {
                'signals_writable': False,
                'error': str(e),
                'status': 'ERROR'
            }
    
    def check_socket_communication(self):
        """Test socket communication on both ports"""
        results = {}
        
        for port in [5555, 9999]:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                result = sock.connect_ex(('localhost', port))
                sock.close()
                
                results[f'port_{port}'] = {
                    'listening': result == 0,
                    'status': 'LISTENING' if result == 0 else 'NOT_LISTENING'
                }
                
            except Exception as e:
                results[f'port_{port}'] = {
                    'listening': False,
                    'error': str(e),
                    'status': 'ERROR'
                }
        
        return results
    
    def print_diagnostic_results(self, results):
        """Print formatted diagnostic results"""
        
        # MT4 Status
        mt4 = results['mt4_status']
        status_icon = "✅" if mt4.get('running') else "❌"
        print(f"{status_icon} MT4 Terminal: {mt4.get('status')}")
        if mt4.get('running'):
            print(f"   PID: {mt4.get('pid')}, Memory: {mt4.get('memory_mb', 0):.1f}MB")
        
        # Database Status  
        db = results['database_status']
        status_icon = "✅" if db.get('accessible') else "❌"
        print(f"{status_icon} Database: {db.get('status')}")
        if db.get('missing_columns'):
            print(f"   Missing columns: {', '.join(db['missing_columns'])}")
        
        # CSV Communication
        csv_comm = results['csv_communication']
        status_icon = "✅" if csv_comm.get('signals_writable') else "❌"
        print(f"{status_icon} CSV Communication: {csv_comm.get('status')}")
        
        # Socket Communication
        socket_comm = results['socket_communication']
        for port_key, port_data in socket_comm.items():
            status_icon = "✅" if port_data.get('listening') else "❌"
            port = port_key.split('_')[1]
            print(f"{status_icon} Socket Port {port}: {port_data.get('status')}")
        
        print("\n" + "=" * 60)
    
    def generate_recommendations(self, results):
        """Generate specific recommendations based on diagnostic results"""
        print("🔧 RECOMMENDED ACTIONS:")
        
        recommendations = []
        
        # MT4 not running
        if not results['mt4_status'].get('running'):
            recommendations.append("🚀 Start MetaTrader 4 terminal")
        
        # Database issues
        db_status = results['database_status']
        if db_status.get('missing_columns'):
            recommendations.append("🗃️ Run database schema repair: python fix_database_schema.py")
        
        # Socket not listening
        socket_comm = results['socket_communication']
        all_sockets_down = all(not port_data.get('listening') for port_data in socket_comm.values())
        if all_sockets_down:
            recommendations.append("🔌 Configure EA for socket communication: EnableDLLSignals=true")
            recommendations.append("🔌 Ensure DLL imports are enabled in MT4 Options")
            recommendations.append("🔌 Verify HUEY_P EA is loaded on a chart")
        
        # CSV communication issues
        if results['csv_communication'].get('status') == 'ERROR':
            recommendations.append("📄 Check file permissions for MT4 eafix directory")
            recommendations.append("📄 Run MT4 as Administrator if permission issues persist")
        
        if not recommendations:
            recommendations.append("✨ System appears healthy - no immediate actions needed")
        
        for i, rec in enumerate(recommendations, 1):
            print(f"   {i}. {rec}")
        
        print("\n" + "=" * 60)

if __name__ == "__main__":
    mt4_path = "C:/Users/Richard Wilks/AppData/Roaming/MetaQuotes/Terminal/F2262CFAFF47C27887389DAB2852351A"
    
    monitor = SystemMonitor(mt4_path)
    results = monitor.run_full_diagnostic()
    
    # Optional: Save results to file
    with open('diagnostic_report.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print("📊 Full diagnostic report saved to: diagnostic_report.json")
```

### **Performance Monitoring Dashboard**
```python
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from collections import deque
import threading
import time

class PerformanceDashboard:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("HUEY_P System Monitor")
        self.root.geometry("1200x800")
        
        # Data storage
        self.timestamps = deque(maxlen=300)  # 5 minutes at 1-second intervals
        self.latency_data = deque(maxlen=300)
        self.throughput_data = deque(maxlen=300)
        self.error_counts = deque(maxlen=300)
        
        self.setup_gui()
        self.start_monitoring()
    
    def setup_gui(self):
        """Setup the monitoring dashboard GUI"""
        
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padding="10")
        
        # Status panel
        status_frame = ttk.LabelFrame(main_frame, text="System Status", padding="10")
        status_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.status_labels = {}
        status_items = [
            ("MT4 Status", "🔄 Checking..."),
            ("Socket Status", "🔄 Checking..."),
            ("CSV Status", "🔄 Checking..."),
            ("Database Status", "🔄 Checking..."),
            ("Last Update", "Never")
        ]
        
        for i, (label, initial_value) in enumerate(status_items):
            ttk.Label(status_frame, text=f"{label}:").grid(row=i//2, column=(i%2)*2, sticky="w", padx=(0, 10))
            self.status_labels[label] = ttk.Label(status_frame, text=initial_value, foreground="blue")
            self.status_labels[label].grid(row=i//2, column=(i%2)*2+1, sticky="w", padx=(0, 20))
        
        # Charts frame
        charts_frame = ttk.Frame(main_frame)
        charts_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create matplotlib figures
        self.fig, ((self.ax1, self.ax2), (self.ax3, self.ax4)) = plt.subplots(2, 2, figsize=(12, 6))
        self.fig.suptitle("HUEY_P Performance Metrics")
        
        # Setup axes
        self.ax1.set_title("Message Latency (ms)")
        self.ax1.set_xlabel("Time")
        self.ax1.set_ylabel("Latency (ms)")
        
        self.ax2.set_title("Throughput (msg/sec)")
        self.ax2.set_xlabel("Time") 
        self.ax2.set_ylabel("Messages/sec")
        
        self.ax3.set_title("Error Rate")
        self.ax3.set_xlabel("Time")
        self.ax3.set_ylabel("Errors/min")
        
        self.ax4.set_title("System Resources")
        self.ax4.set_xlabel("Component")
        self.ax4.set_ylabel("Usage %")
        
        # Embed in tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, charts_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(button_frame, text="Run Diagnostic", command=self.run_diagnostic).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Reset Data", command=self.reset_data).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Export Report", command=self.export_report).pack(side=tk.LEFT)
    
    def start_monitoring(self):
        """Start background monitoring thread"""
        self.monitoring_thread = threading.Thread(target=self.monitor_loop)
        self.monitoring_thread.daemon = True
        self.monitoring_thread.start()
    
    def monitor_loop(self):
        """Main monitoring loop"""
        while True:
            try:
                # Collect current metrics
                current_time = time.time()
                
                # Simulate data collection (replace with actual metrics)
                latency = self.measure_communication_latency()
                throughput = self.measure_message_throughput() 
                errors = self.count_recent_errors()
                
                # Update data collections
                self.timestamps.append(current_time)
                self.latency_data.append(latency)
                self.throughput_data.append(throughput)
                self.error_counts.append(errors)
                
                # Update GUI (thread-safe)
                self.root.after(0, self.update_gui)
                
                time.sleep(1)  # Update every second
                
            except Exception as e:
                print(f"Monitoring error: {e}")
                time.sleep(5)  # Wait longer on error
    
    def update_gui(self):
        """Update GUI elements with current data"""
        
        # Update status labels
        system_status = self.get_system_status()
        for label, value in system_status.items():
            if label in self.status_labels:
                self.status_labels[label].config(text=value)
        
        # Update charts
        if len(self.timestamps) > 1:
            times = list(self.timestamps)
            time_labels = [time.strftime('%H:%M:%S', time.localtime(t)) for t in times[-60:]]  # Last minute
            
            # Latency chart
            self.ax1.clear()
            self.ax1.plot(time_labels, list(self.latency_data)[-60:], 'b-', linewidth=2)
            self.ax1.set_title("Message Latency (ms)")
            self.ax1.set_xlabel("Time")
            self.ax1.set_ylabel("Latency (ms)")
            
            # Throughput chart
            self.ax2.clear()
            self.ax2.plot(time_labels, list(self.throughput_data)[-60:], 'g-', linewidth=2)
            self.ax2.set_title("Throughput (msg/sec)")
            
            # Error rate chart
            self.ax3.clear()
            self.ax3.plot(time_labels, list(self.error_counts)[-60:], 'r-', linewidth=2)
            self.ax3.set_title("Error Rate")
            
            # System resources (bar chart)
            self.ax4.clear()
            resources = self.get_resource_usage()
            if resources:
                self.ax4.bar(resources.keys(), resources.values())
                self.ax4.set_title("System Resources")
                self.ax4.set_ylabel("Usage %")
            
            self.canvas.draw()
    
    def run_diagnostic(self):
        """Run comprehensive system diagnostic"""
        # This would integrate with the SystemMonitor class above
        diagnostic_window = tk.Toplevel(self.root)
        diagnostic_window.title("System Diagnostic")
        diagnostic_window.geometry("800x600")
        
        text_widget = tk.Text(diagnostic_window, wrap=tk.WORD)
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Run diagnostic in separate thread
        def run_diagnostic_thread():
            # Integrate with SystemMonitor
            monitor = SystemMonitor("C:/Users/Richard Wilks/AppData/Roaming/MetaQuotes/Terminal/F2262CFAFF47C27887389DAB2852351A")
            results = monitor.run_full_diagnostic()
            
            # Display results in text widget
            diagnostic_window.after(0, lambda: display_results(results))
        
        def display_results(results):
            text_widget.delete(1.0, tk.END)
            text_widget.insert(tk.END, f"Diagnostic completed at: {datetime.now()}\n\n")
            text_widget.insert(tk.END, json.dumps(results, indent=2, default=str))
        
        threading.Thread(target=run_diagnostic_thread, daemon=True).start()
    
    def run(self):
        """Start the dashboard"""
        self.root.mainloop()

# Usage
if __name__ == "__main__":
    dashboard = PerformanceDashboard()
    dashboard.run()
```

---

## ⚡ **Emergency Recovery Procedures**

### **🆘 Complete System Reset (Nuclear Option)**
```bash
#!/bin/bash
# emergency_system_reset.sh

echo "🚨 EMERGENCY HUEY_P SYSTEM RESET"
echo "This will reset all communication systems to default state"
read -p "Are you sure? (yes/no): " confirm

if [ "$confirm" = "yes" ]; then
    echo "🔄 Stopping MT4..."
    taskkill /f /im terminal.exe 2>/dev/null
    
    echo "🔄 Cleaning communication files..."
    cd "C:/Users/Richard Wilks/AppData/Roaming/MetaQuotes/Terminal/F2262CFAFF47C27887389DAB2852351A/eafix"
    rm -f trading_signals.csv trade_responses.csv system_status.csv error_log.csv
    
    echo "🔄 Resetting database..."
    cd Database
    cp trading_system.db trading_system_backup_$(date +%Y%m%d_%H%M%S).db
    # Run database repair
    
    echo "🔄 Rebuilding DLL..."
    cd ../MQL4_DLL_SocketBridge
    ./build_dll.bat
    
    echo "✅ System reset complete"
    echo "📋 Next steps:"
    echo "   1. Start MetaTrader 4"
    echo "   2. Load HUEY_P EA on chart"
    echo "   3. Configure EA parameters"
    echo "   4. Run diagnostic test"
fi
```

### **🔧 Quick Fix Scripts**

#### **CSV Communication Quick Fix**
```python
#!/usr/bin/env python3
# quick_fix_csv.py

import os
import csv
from pathlib import Path
from datetime import datetime

def quick_fix_csv_communication():
    print("🔧 Quick CSV Communication Fix")
    
    mt4_path = Path("C:/Users/Richard Wilks/AppData/Roaming/MetaQuotes/Terminal/F2262CFAFF47C27887389DAB2852351A")
    eafix_path = mt4_path / "eafix"
    
    # Create directory if missing
    eafix_path.mkdir(exist_ok=True)
    
    # Create/reset CSV files with proper headers
    files_to_create = {
        'trading_signals.csv': ['signal_id', 'symbol', 'direction', 'lot_size', 'stop_loss', 'take_profit', 'comment', 'timestamp', 'confidence', 'strategy_id'],
        'trade_responses.csv': ['signal_id', 'trade_id', 'status', 'execution_price', 'timestamp', 'error_message'],
        'system_status.csv': ['timestamp', 'ea_state', 'balance', 'equity', 'margin_used', 'open_trades', 'last_error', 'connection_status'],
        'error_log.csv': ['timestamp', 'error_level', 'error_code', 'error_message', 'context', 'signal_id']
    }
    
    for filename, headers in files_to_create.items():
        file_path = eafix_path / filename
        
        with open(file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
        
        print(f"✅ Created/reset: {filename}")
    
    # Set proper permissions
    try:
        for filename in files_to_create:
            file_path = eafix_path / filename
            os.chmod(file_path, 0o666)  # Read/write for all
        print("✅ File permissions set")
    except Exception as e:
        print(f"⚠️ Could not set permissions: {e}")
    
    print("🎉 CSV communication system reset complete")

if __name__ == "__main__":
    quick_fix_csv_communication()
```

#### **Socket Communication Quick Fix**
```python
#!/usr/bin/env python3
# quick_fix_socket.py

import subprocess
import shutil
from pathlib import Path

def quick_fix_socket_communication():
    print("🔧 Quick Socket Communication Fix")
    
    mt4_path = Path("C:/Users/Richard Wilks/AppData/Roaming/MetaQuotes/Terminal/F2262CFAFF47C27887389DAB2852351A")
    dll_path = mt4_path / "MQL4" / "Libraries" / "MQL4_DLL_SocketBridge.dll"
    
    # Check DLL existence
    if not dll_path.exists():
        print("❌ DLL not found, attempting to rebuild...")
        
        source_path = Path("C:/Users/Richard Wilks/Downloads/EEE/documentaion/eafix/MQL4_DLL_SocketBridge")
        if source_path.exists():
            try:
                # Build DLL
                build_dir = source_path / "build"
                build_dir.mkdir(exist_ok=True)
                
                os.chdir(build_dir)
                subprocess.run(["cmake", "..", "-G", "Visual Studio 17 2022", "-A", "Win32"], check=True)
                subprocess.run(["cmake", "--build", ".", "--config", "Release"], check=True)
                
                # Copy to MT4
                built_dll = build_dir / "Release" / "MQL4_DLL_SocketBridge.dll"
                if built_dll.exists():
                    shutil.copy2(built_dll, dll_path)
                    print("✅ DLL rebuilt and installed")
                else:
                    print("❌ DLL build failed")
                    return False
                    
            except Exception as e:
                print(f"❌ DLL build error: {e}")
                return False
        else:
            print("❌ DLL source code not found")
            return False
    else:
        print("✅ DLL found")
    
    # Check DLL validity
    try:
        result = subprocess.run(["file", str(dll_path)], capture_output=True, text=True)
        if "PE32" in result.stdout and "DLL" in result.stdout:
            print("✅ DLL is valid Win32 PE executable")
        else:
            print("⚠️ DLL may be corrupted or wrong architecture")
    except:
        print("⚠️ Could not validate DLL (file command not available)")
    
    print("🎉 Socket communication system check complete")
    print("📋 Next steps:")
    print("   1. Start MetaTrader 4")
    print("   2. Tools → Options → Expert Advisors → ✅ Allow DLL imports")
    print("   3. Load HUEY_P EA with EnableDLLSignals=true")
    
    return True

if __name__ == "__main__":
    quick_fix_socket_communication()
```

This comprehensive troubleshooting guide provides systematic approaches to diagnose and resolve communication issues in the HUEY_P trading system, with automated diagnostic tools and quick-fix scripts for common problems.