# CSV Communication Protocol - Detailed Specification

## Protocol Overview

The CSV Communication Protocol enables reliable file-based message exchange between Python applications and the HUEY_P Expert Advisor. This protocol serves as the primary fallback mechanism when socket communication is unavailable.

---

## File Structure and Locations

### **Base Directory Structure**
```
MT4_DATA_FOLDER/eafix/
├── trading_signals.csv      # Python → EA (Signal Input)
├── trade_responses.csv      # EA → Python (Trade Confirmations)
├── system_status.csv        # EA → Python (System Health)
├── error_log.csv           # EA → Python (Error Reports)
├── heartbeat.csv           # EA → Python (Connection Status)
└── signal_archive/         # Processed signal backup
    ├── YYYY-MM-DD/
    │   ├── processed_signals_HHMMSS.csv
    │   └── failed_signals_HHMMSS.csv
    └── cleanup_log.csv
```

### **File Access Patterns**
- **Python**: Read/Write access to all files
- **EA**: Read access to `trading_signals.csv`, Write access to response files
- **Atomic Operations**: All writes use temporary files with atomic moves
- **File Locking**: Cooperative locking using lock files (`.lock` extensions)

---

## Message Flow Architecture

### **Signal Processing Flow**
```
┌─────────────────┐  1. Generate Signal   ┌────────────────────┐
│ Python Strategy │ ───────────────────► │ Signal Generator   │
│   Application   │                      │    Component       │
└─────────────────┘                      └────────────────────┘
                                                    │
                                        2. Validate Signal
                                                    ▼
                                         ┌────────────────────┐
                                         │ Signal Validator   │
                                         │ - Schema Check     │
                                         │ - Risk Limits      │
                                         │ - Market Hours     │
                                         └────────────────────┘
                                                    │
                                        3. Write to CSV
                                                    ▼
                                         ┌────────────────────┐
                                         │ trading_signals    │
                                         │     .csv           │
                                         │ (Atomic Write)     │
                                         └────────────────────┘
                                                    │
                                        4. File Monitor (15s)
                                                    ▼
                                         ┌────────────────────┐
                                         │ HUEY_P EA          │
                                         │ CSV Manager        │
                                         │ - File Change      │
                                         │ - Parse Signals    │
                                         │ - Validate Data    │
                                         └────────────────────┘
                                                    │
                                        5. Process Signal
                                                    ▼
                                         ┌────────────────────┐
                                         │ Trade Execution    │
                                         │ - Risk Check       │
                                         │ - Order Placement  │
                                         │ - Error Handling   │
                                         └────────────────────┘
                                                    │
                                        6. Write Response
                                                    ▼
                                         ┌────────────────────┐
                                         │ trade_responses    │
                                         │     .csv           │
                                         │ (Append Mode)      │
                                         └────────────────────┘
                                                    │
                                        7. Monitor Response
                                                    ▼
                                         ┌────────────────────┐
                                         │ Python Response    │
                                         │    Monitor         │
                                         │ - File Watcher     │
                                         │ - Parse Results    │
                                         │ - Update UI        │
                                         └────────────────────┘
```

---

## CSV File Specifications

### **1. Trading Signals File (`trading_signals.csv`)**

#### **Schema Definition**
```csv
signal_id,symbol,direction,lot_size,stop_loss,take_profit,comment,timestamp,confidence,strategy_id,priority,expiry,validation_hash
```

#### **Field Specifications**

| Field | Type | Required | Length | Valid Values | Description |
|-------|------|----------|--------|--------------|-------------|
| `signal_id` | String | ✅ | 1-50 | Alphanumeric + underscore | Unique identifier for tracking |
| `symbol` | String | ✅ | 6-7 | MT4 symbols (EURUSD, etc.) | Trading instrument |
| `direction` | String | ✅ | 3-4 | BUY, SELL | Order type |
| `lot_size` | Float | ✅ | - | 0.01-100.0 | Position size |
| `stop_loss` | Integer | ❌ | - | 0-1000 | Stop loss in points |
| `take_profit` | Integer | ❌ | - | 0-1000 | Take profit in points |
| `comment` | String | ❌ | 0-63 | Any | Order comment |
| `timestamp` | String | ✅ | 26 | ISO 8601 format | Signal creation time |
| `confidence` | Float | ❌ | - | 0.0-1.0 | Signal confidence score |
| `strategy_id` | Integer | ❌ | - | 1-99999 | Strategy identifier |
| `priority` | Integer | ❌ | - | 1-10 | Processing priority |
| `expiry` | String | ❌ | 26 | ISO 8601 format | Signal expiration |
| `validation_hash` | String | ❌ | 32 | MD5 hash | Data integrity check |

#### **Example Records**
```csv
signal_id,symbol,direction,lot_size,stop_loss,take_profit,comment,timestamp,confidence,strategy_id,priority,expiry,validation_hash
SIGNAL_20250815_001,EURUSD,BUY,0.01,20,40,Breakout Strategy,2025-08-15T15:45:00.123456,0.85,12345,5,2025-08-15T16:45:00.000000,a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
SIGNAL_20250815_002,GBPUSD,SELL,0.02,30,60,Reversal Pattern,2025-08-15T15:46:15.789012,0.72,12346,3,2025-08-15T17:46:15.000000,b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7
```

#### **Validation Rules**
- **Unique Signal IDs**: No duplicate `signal_id` values within 24-hour period
- **Symbol Validation**: Must match available MT4 trading instruments
- **Market Hours**: Signals only processed during market hours for the instrument
- **Risk Limits**: `lot_size` must not exceed account risk parameters
- **Timestamp Format**: Must be valid ISO 8601 format with timezone
- **Expiry Logic**: Expired signals (past `expiry` time) are automatically rejected

### **2. Trade Responses File (`trade_responses.csv`)**

#### **Schema Definition**
```csv
signal_id,trade_id,status,execution_price,actual_lot_size,execution_time,slippage,commission,swap,error_code,error_message,processing_time_ms
```

#### **Status Values**
| Status | Description | Next Action |
|--------|-------------|-------------|
| `EXECUTED` | Trade successfully placed | Monitor position |
| `FAILED` | Trade execution failed | Check error message |
| `PENDING` | Order pending activation | Wait for market conditions |
| `CANCELLED` | Signal cancelled | No further action |
| `PARTIAL` | Partial execution | Monitor remaining quantity |
| `EXPIRED` | Signal expired | Generate new signal |
| `REJECTED` | Risk limits exceeded | Adjust parameters |

#### **Example Records**
```csv
signal_id,trade_id,status,execution_price,actual_lot_size,execution_time,slippage,commission,swap,error_code,error_message,processing_time_ms
SIGNAL_20250815_001,123456,EXECUTED,1.12450,0.01,2025-08-15T15:45:12.345678,0.3,-0.07,0.00,0,,234
SIGNAL_20250815_002,0,FAILED,0.00000,0.00,2025-08-15T15:46:30.123456,0.0,0.00,0.00,4108,Invalid ticket,156
SIGNAL_20250815_003,123457,PARTIAL,1.26789,0.01,2025-08-15T15:47:05.987654,1.2,-0.05,0.00,0,Partial fill: 0.01/0.02,445
```

### **3. System Status File (`system_status.csv`)**

#### **Schema Definition**
```csv
timestamp,ea_state,account_balance,account_equity,used_margin,free_margin,margin_level,open_positions,pending_orders,daily_profit,daily_trades,last_error,connection_status,cpu_usage,memory_usage
```

#### **EA States**
- `INITIALIZING`: EA starting up
- `ACTIVE`: Normal operation, ready for signals
- `TRADING`: Currently processing trades
- `PAUSED`: Trading paused (risk limits hit)
- `ERROR`: System error state
- `SHUTDOWN`: EA shutting down

#### **Example Record**
```csv
timestamp,ea_state,account_balance,account_equity,used_margin,free_margin,margin_level,open_positions,pending_orders,daily_profit,daily_trades,last_error,connection_status,cpu_usage,memory_usage
2025-08-15T15:48:00.000000,ACTIVE,10000.00,10234.56,156.78,9877.78,6535.42,3,1,234.56,12,ERR_NO_ERROR,CONNECTED,2.3,45.2
```

### **4. Error Log File (`error_log.csv`)**

#### **Schema Definition**
```csv
timestamp,error_level,error_code,error_message,context,signal_id,function_name,line_number,stack_trace,recovery_action
```

#### **Error Levels**
- `INFO`: Informational messages
- `WARNING`: Non-critical issues
- `ERROR`: Serious errors affecting operation
- `CRITICAL`: System-threatening errors

#### **Example Records**
```csv
timestamp,error_level,error_code,error_message,context,signal_id,function_name,line_number,stack_trace,recovery_action
2025-08-15T15:49:12.345678,ERROR,4108,Invalid ticket,OrderClose operation,SIGNAL_20250815_004,ClosePosition,1245,OrderClose->TradeManager->StateManager,Position marked as closed
2025-08-15T15:49:45.123456,WARNING,134,Not enough money,Insufficient margin for trade,SIGNAL_20250815_005,PlaceOrder,892,PlaceOrder->RiskManager,Signal rejected due to margin
```

---

## File Operations and Locking

### **Atomic Write Operations**

#### **Python Implementation**
```python
import csv
import os
import tempfile
from pathlib import Path
import fcntl  # Unix systems
import msvcrt  # Windows systems

class AtomicCSVWriter:
    def __init__(self, file_path):
        self.file_path = Path(file_path)
        self.lock_file = Path(str(file_path) + '.lock')
    
    def write_signal(self, signal_data):
        """Atomically write signal to CSV file"""
        try:
            # Create lock file
            with open(self.lock_file, 'w') as lock:
                if os.name == 'nt':  # Windows
                    msvcrt.locking(lock.fileno(), msvcrt.LK_NBLCK, 1)
                else:  # Unix-like
                    fcntl.flock(lock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                
                # Write to temporary file
                temp_file = self.file_path.with_suffix('.tmp')
                with open(temp_file, 'w', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=signal_data.keys())
                    writer.writeheader()
                    writer.writerow(signal_data)
                
                # Atomic move
                if os.name == 'nt':
                    temp_file.replace(self.file_path)
                else:
                    os.rename(str(temp_file), str(self.file_path))
                
            # Remove lock file
            self.lock_file.unlink(missing_ok=True)
            return True
            
        except (IOError, OSError) as e:
            print(f"Write failed: {e}")
            self.lock_file.unlink(missing_ok=True)
            return False
```

#### **MQL4 Implementation**
```mql4
class AtomicCSVReader {
private:
    string filePath;
    string lockPath;
    
public:
    bool WaitForFileAvailable(int timeoutSeconds = 30) {
        datetime startTime = TimeCurrent();
        
        while (TimeCurrent() - startTime < timeoutSeconds) {
            // Check for lock file
            if (!FileIsExist(lockPath)) {
                return true;
            }
            
            Sleep(100); // Wait 100ms
        }
        
        LogWarning("File lock timeout: " + filePath);
        return false;
    }
    
    bool ReadSignals(TradingSignal& signals[]) {
        if (!WaitForFileAvailable()) {
            return false;
        }
        
        int handle = FileOpen(filePath, FILE_READ | FILE_CSV);
        if (handle == INVALID_HANDLE) {
            LogError("Cannot open file: " + filePath);
            return false;
        }
        
        // Skip header
        if (!FileIsEnding(handle)) {
            FileReadString(handle);
        }
        
        // Read all signals
        ArrayResize(signals, 0);
        while (!FileIsEnding(handle)) {
            TradingSignal signal = ParseCSVRow(handle);
            if (ValidateSignal(signal)) {
                ArrayResize(signals, ArraySize(signals) + 1);
                signals[ArraySize(signals) - 1] = signal;
            }
        }
        
        FileClose(handle);
        return true;
    }
};
```

### **File Monitoring and Change Detection**

#### **Python File Watcher**
```python
import time
import hashlib
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class CSVFileMonitor(FileSystemEventHandler):
    def __init__(self, callback_function):
        self.callback = callback_function
        self.file_hashes = {}
        self.last_modified = {}
    
    def on_modified(self, event):
        if event.is_directory:
            return
            
        file_path = event.src_path
        if not file_path.endswith('.csv'):
            return
            
        # Check if file actually changed (content hash)
        try:
            current_hash = self._calculate_file_hash(file_path)
            last_hash = self.file_hashes.get(file_path)
            
            if current_hash != last_hash:
                self.file_hashes[file_path] = current_hash
                self.callback(file_path, 'modified')
                
        except Exception as e:
            print(f"Error monitoring file {file_path}: {e}")
    
    def _calculate_file_hash(self, file_path):
        """Calculate MD5 hash of file content"""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

# Usage
def on_file_changed(file_path, event_type):
    print(f"File {file_path} was {event_type}")
    # Process the changed file
    
monitor = CSVFileMonitor(on_file_changed)
observer = Observer()
observer.schedule(monitor, path='/path/to/csv/files', recursive=False)
observer.start()
```

#### **MQL4 File Change Detection**
```mql4
class FileChangeDetector {
private:
    struct FileState {
        string fileName;
        datetime lastModified;
        long fileSize;
        int checksum;
    };
    
    FileState fileStates[];
    
public:
    bool HasFileChanged(string fileName) {
        int index = FindFileIndex(fileName);
        
        // Get current file stats
        datetime currentModified = (datetime)FileGetInteger(fileName, FILE_MODIFY_DATE);
        long currentSize = FileSize(fileName);
        
        if (index == -1) {
            // New file - add to tracking
            AddFileToTracking(fileName, currentModified, currentSize);
            return true;
        }
        
        // Check if changed
        if (fileStates[index].lastModified != currentModified || 
            fileStates[index].fileSize != currentSize) {
            
            // Update tracking info
            fileStates[index].lastModified = currentModified;
            fileStates[index].fileSize = currentSize;
            return true;
        }
        
        return false;
    }
    
    void UpdateFileState(string fileName) {
        if (HasFileChanged(fileName)) {
            LogInfo("File changed detected: " + fileName);
            ProcessFileChange(fileName);
        }
    }
};
```

---

## Error Handling and Recovery

### **Error Classification System**

#### **Signal Processing Errors**
```csv
Error Code,Category,Description,Recovery Action,Retry Allowed
1001,VALIDATION,Invalid signal format,Skip signal,No
1002,VALIDATION,Missing required field,Skip signal,No
1003,VALIDATION,Invalid symbol,Skip signal,No
1004,VALIDATION,Invalid lot size,Adjust lot size,Yes
1005,VALIDATION,Expired signal,Skip signal,No
1006,VALIDATION,Duplicate signal ID,Skip signal,No
```

#### **Trade Execution Errors**
```csv
Error Code,Category,Description,Recovery Action,Retry Allowed
2001,EXECUTION,Insufficient margin,Reduce lot size,Yes
2002,EXECUTION,Market closed,Queue for reopening,Yes
2003,EXECUTION,Invalid price,Retry with current price,Yes
2004,EXECUTION,Too many requests,Implement backoff,Yes
2005,EXECUTION,Trade disabled,Skip signal,No
2006,EXECUTION,Invalid stops,Adjust stop levels,Yes
```

#### **System Errors**
```csv
Error Code,Category,Description,Recovery Action,Retry Allowed
3001,SYSTEM,File access denied,Check permissions,Yes
3002,SYSTEM,Disk full,Clean up old files,Yes
3003,SYSTEM,Memory allocation failed,Restart EA,No
3004,SYSTEM,Database connection lost,Reconnect,Yes
3005,SYSTEM,Configuration error,Load defaults,Yes
```

### **Recovery Strategies**

#### **Automatic Recovery Logic**
```mql4
class ErrorRecoveryManager {
private:
    struct RecoveryRule {
        int errorCode;
        string recoveryAction;
        int maxRetries;
        int backoffSeconds;
        bool autoRecover;
    };
    
    RecoveryRule recoveryRules[];
    
public:
    bool HandleError(int errorCode, string context, int attempt = 1) {
        RecoveryRule rule = GetRecoveryRule(errorCode);
        
        if (rule.errorCode == 0) {
            LogError("Unknown error code: " + IntegerToString(errorCode));
            return false;
        }
        
        if (attempt > rule.maxRetries) {
            LogError("Max retries exceeded for error: " + IntegerToString(errorCode));
            return false;
        }
        
        // Log recovery attempt
        LogInfo("Attempting recovery for error " + IntegerToString(errorCode) + 
                ", attempt " + IntegerToString(attempt) + "/" + IntegerToString(rule.maxRetries));
        
        // Apply recovery action
        bool success = ExecuteRecoveryAction(rule.recoveryAction, context);
        
        if (!success && rule.autoRecover) {
            // Wait before retry
            Sleep(rule.backoffSeconds * 1000);
            return HandleError(errorCode, context, attempt + 1);
        }
        
        return success;
    }
    
    bool ExecuteRecoveryAction(string action, string context) {
        if (action == "REDUCE_LOT_SIZE") {
            return ReduceLotSize(context);
        }
        else if (action == "RETRY_WITH_CURRENT_PRICE") {
            return RetryWithCurrentPrice(context);
        }
        else if (action == "SKIP_SIGNAL") {
            return SkipCurrentSignal(context);
        }
        else if (action == "RESTART_EA") {
            return InitiateEARestart();
        }
        
        return false;
    }
};
```

---

## Performance Optimization

### **Batch Processing**
```python
class BatchSignalProcessor:
    def __init__(self, batch_size=10, flush_interval=30):
        self.batch_size = batch_size
        self.flush_interval = flush_interval
        self.signal_batch = []
        self.last_flush = time.time()
    
    def add_signal(self, signal):
        self.signal_batch.append(signal)
        
        # Check if batch is full or time to flush
        if (len(self.signal_batch) >= self.batch_size or 
            time.time() - self.last_flush >= self.flush_interval):
            self.flush_batch()
    
    def flush_batch(self):
        if not self.signal_batch:
            return
            
        try:
            # Write all signals in single operation
            self._write_signals_batch(self.signal_batch)
            print(f"Flushed batch of {len(self.signal_batch)} signals")
            
            # Clear batch
            self.signal_batch.clear()
            self.last_flush = time.time()
            
        except Exception as e:
            print(f"Batch flush failed: {e}")
```

### **File Compression and Archival**
```python
import gzip
import shutil
from datetime import datetime, timedelta

class CSVArchiveManager:
    def __init__(self, archive_directory, retention_days=30):
        self.archive_dir = Path(archive_directory)
        self.retention_days = retention_days
        
    def archive_old_files(self):
        """Archive files older than retention period"""
        cutoff_date = datetime.now() - timedelta(days=self.retention_days)
        
        for csv_file in self.get_csv_files():
            file_date = datetime.fromtimestamp(csv_file.stat().st_mtime)
            
            if file_date < cutoff_date:
                self.compress_and_archive(csv_file, file_date)
    
    def compress_and_archive(self, file_path, file_date):
        """Compress file and move to archive"""
        try:
            # Create archive directory structure
            archive_path = (self.archive_dir / 
                          file_date.strftime('%Y-%m-%d') / 
                          file_path.name)
            archive_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Compress file
            compressed_path = archive_path.with_suffix('.gz')
            with open(file_path, 'rb') as f_in:
                with gzip.open(compressed_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            
            # Remove original
            file_path.unlink()
            print(f"Archived: {file_path} -> {compressed_path}")
            
        except Exception as e:
            print(f"Archive failed for {file_path}: {e}")
```

---

## Integration Examples

### **Complete Signal Processing Example**

#### **Python Signal Sender**
```python
import csv
import hashlib
import time
from datetime import datetime, timedelta
from pathlib import Path

class TradingSignalSender:
    def __init__(self, mt4_path):
        self.csv_writer = AtomicCSVWriter(Path(mt4_path) / "eafix" / "trading_signals.csv")
        self.response_monitor = CSVResponseMonitor(Path(mt4_path) / "eafix" / "trade_responses.csv")
        
    def send_signal(self, symbol, direction, lot_size, stop_loss=0, take_profit=0, 
                   strategy_id=1001, confidence=0.8, expiry_minutes=60):
        """Send complete trading signal with all validation"""
        
        # Generate unique signal ID
        signal_id = f"SIGNAL_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hash(time.time()) % 1000:03d}"
        
        # Create signal data
        signal_data = {
            'signal_id': signal_id,
            'symbol': symbol,
            'direction': direction,
            'lot_size': lot_size,
            'stop_loss': stop_loss,
            'take_profit': take_profit,
            'comment': f'Strategy_{strategy_id}',
            'timestamp': datetime.now().isoformat(),
            'confidence': confidence,
            'strategy_id': strategy_id,
            'priority': 5,
            'expiry': (datetime.now() + timedelta(minutes=expiry_minutes)).isoformat(),
            'validation_hash': self._calculate_validation_hash(signal_data)
        }
        
        # Send signal
        if self.csv_writer.write_signal(signal_data):
            print(f"Signal sent: {signal_id}")
            
            # Wait for response
            return self.wait_for_response(signal_id, timeout=120)
        
        return None
    
    def _calculate_validation_hash(self, signal_data):
        """Calculate MD5 hash for data integrity"""
        hash_string = f"{signal_data['signal_id']}{signal_data['symbol']}{signal_data['direction']}{signal_data['lot_size']}"
        return hashlib.md5(hash_string.encode()).hexdigest()
    
    def wait_for_response(self, signal_id, timeout=60):
        """Wait for trade response"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            responses = self.response_monitor.check_new_responses()
            
            for response in responses:
                if response['signal_id'] == signal_id:
                    print(f"Response received: {response}")
                    return response
            
            time.sleep(2)  # Check every 2 seconds
        
        print(f"Timeout waiting for response to signal: {signal_id}")
        return None

# Usage example
sender = TradingSignalSender("C:/Users/.../MT4_Data/")

# Send a buy signal
response = sender.send_signal(
    symbol='EURUSD',
    direction='BUY', 
    lot_size=0.01,
    stop_loss=20,
    take_profit=40,
    strategy_id=1001,
    confidence=0.85
)

if response and response['status'] == 'EXECUTED':
    print(f"Trade executed successfully: {response['trade_id']}")
else:
    print("Trade failed or timed out")
```

This comprehensive CSV communication protocol documentation provides all the technical details needed to implement and troubleshoot the file-based communication system in the HUEY_P trading platform.