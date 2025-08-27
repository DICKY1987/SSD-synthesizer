# MT4 Signal Interface Specification

**Version:** 1.0.0  
**Document Status:** Authoritative Source of Truth  
**Created:** July 2025  
**System:** HUEY_P_ClaudeCentric Trading System  

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Signal Data Requirements](#2-signal-data-requirements)
3. [Communication Channels](#3-communication-channels)
4. [Signal Message Formats](#4-signal-message-formats)
5. [Validation Framework](#5-validation-framework)
6. [Error Handling](#6-error-handling)
7. [Performance Requirements](#7-performance-requirements)
8. [Implementation Templates](#8-implementation-templates)
9. [Testing and Validation](#9-testing-and-validation)

---

## 1. Executive Summary

This document defines the standardized interface between trading signal generators and the MT4 execution engine. **Regardless of signal generation method or transmission channel, all signals must conform to this specification** to ensure reliable execution.

### 1.1 Key Principles

- **Standardized Input Concept**: All signals use identical data structures regardless of generation or transmission method
- **Three-Tier Communication**: Automatic failover between Socket → Named Pipes → File-based communication
- **Strict Validation**: All signals undergo comprehensive validation before execution
- **Performance Optimization**: Sub-10ms processing overhead (excluding broker latency)

---

## 2. Signal Data Requirements

### 2.1 Core Signal Structure

All signals must include the following standardized message structure:

```json
{
    "message_type": "SIGNAL",
    "message_id": "unique_identifier",
    "timestamp": 1672531200.123,
    "source": "signal_generator_name", 
    "version": "1.0",
    "payload": {
        // Signal-specific data (see Section 2.2)
    }
}
```

### 2.2 Required Payload Fields

| Field | Type | Description | Example | Validation Rules |
|-------|------|-------------|---------|------------------|
| `symbol` | string | Currency pair identifier | "EURUSD" | Must match MT4 symbol names, uppercase |
| `action` | string | Trade direction | "BUY" or "SELL" | Enum: BUY, SELL |
| `confidence` | number | Signal confidence score | 0.85 | Range: 0.0-1.0, required for execution |
| `strategy_id` | string | Unique strategy identifier | "ml_momentum_v2" | Max 50 chars, alphanumeric + underscore |
| `signal_time` | number | Signal generation timestamp | 1672531200.123 | Unix timestamp with milliseconds |

### 2.3 Optional Payload Fields

| Field | Type | Description | Example | Default Behavior |
|-------|------|-------------|---------|------------------|
| `stop_loss` | number | Stop loss in pips | 50 | Uses parameter set default |
| `take_profit` | number | Take profit in pips | 100 | Uses parameter set default |
| `lot_size` | number | Position size | 0.01 | Calculated from risk percentage |
| `magic_number` | number | EA magic number override | 12345 | Uses EA default |
| `entry_price` | number | Specific entry price | 1.0850 | Uses market price |
| `parameters` | object | Additional strategy data | `{"rsi_value": 35.2}` | Optional metadata |

### 2.4 Parameter Set Integration

Signals are mapped to predefined parameter sets through the `strategy_id` field:

1. **Signal Processing**: The `strategy_id` is looked up in `signal_id_mapping.csv`
2. **Parameter Resolution**: Mapped to a parameter set ID from `all_10_parameter_sets.csv`
3. **Trade Execution**: Parameters are applied unless overridden by signal fields

**Parameter Set Schema:**
```csv
id,stopLoss,takeProfit,trailingStop,riskPercent,maxPositions,useTrailing,description
aggressive,200,400,50,1.5,2,true,"High risk parameters"
conservative,100,200,25,0.5,1,false,"Low risk parameters"
```

---

## 3. Communication Channels

### 3.1 Hierarchical Communication Fallback

The system implements automatic failover across three communication channels:

```
Primary:    TCP Socket (Port 8888)
Secondary:  Named Pipes (\\.\pipe\HUEY_P_ClaudeCentric_SignalPipe)
Tertiary:   File System (/MQL4/Files/current_signal.csv)
```

### 3.2 Channel-Specific Considerations

#### 3.2.1 TCP Socket Communication
- **Protocol**: Binary framed JSON over TCP
- **Message Framing**: 4-byte little-endian length header + UTF-8 JSON
- **Performance**: Lowest latency, highest throughput
- **Error Handling**: Automatic reconnection with exponential backoff

#### 3.2.2 Named Pipes Communication
- **Protocol**: Windows Named Pipes with JSON payload
- **Message Format**: Identical to socket protocol
- **Performance**: Medium latency, reliable local communication
- **Use Case**: Fallback when socket connection fails

#### 3.2.3 File-Based Communication
- **Protocol**: Atomic file operations with CSV/JSON format
- **File Location**: `/MQL4/Files/current_signal.csv`
- **Atomic Operations**: Write to `.tmp`, then rename to prevent race conditions
- **Performance**: Highest latency, most reliable fallback

---

## 4. Signal Message Formats

### 4.1 JSON Format (Socket/Named Pipes)

**Complete Signal Example:**
```json
{
    "message_type": "SIGNAL",
    "message_id": "sig_20250703_142530_001",
    "timestamp": 1672531200.123,
    "source": "python",
    "version": "1.0",
    "payload": {
        "symbol": "EURUSD",
        "action": "BUY",
        "confidence": 0.85,
        "strategy_id": "ml_momentum_v2",
        "signal_time": 1672531200.123,
        "stop_loss": 50,
        "take_profit": 100,
        "lot_size": 0.01,
        "magic_number": 12345,
        "parameters": {
            "entry_price": 1.0850,
            "rsi_value": 35.2,
            "ma_trend": "UP"
        }
    }
}
```

### 4.2 CSV Format (File-Based)

**File Format for `current_signal.csv`:**
```csv
message_id,timestamp,symbol,action,confidence,strategy_id,stop_loss,take_profit,lot_size,parameters
sig_20250703_142530_001,1672531200.123,EURUSD,BUY,0.85,ml_momentum_v2,50,100,0.01,"{""entry_price"":1.0850}"
```

### 4.3 Binary Transport Protocol

**Socket Message Structure:**
```
[4 bytes] Message Length (little-endian)
[N bytes] UTF-8 JSON Payload
```

**Example Binary Frame:**
```
0x7B000000  // Length: 123 bytes
{"message_type":"SIGNAL",...}  // JSON payload
```

---

## 5. Validation Framework

### 5.1 Signal Validation Pipeline

```
Input Signal → Format Validation → Business Rules → Parameter Resolution → Execution Queue
```

### 5.2 Validation Rules

#### 5.2.1 Format Validation
- **JSON Schema**: Must conform to signal schema
- **Required Fields**: All mandatory fields present
- **Data Types**: Correct type for each field
- **Encoding**: Valid UTF-8 encoding

#### 5.2.2 Business Rules Validation
- **Symbol Validation**: Must be active trading symbol
- **Confidence Threshold**: Minimum 0.1 for execution
- **Strategy Mapping**: `strategy_id` must exist in mapping file
- **Time Validation**: Signal timestamp within acceptable range (±5 minutes)

#### 5.2.3 Trading Rules Validation
- **Market Hours**: Trading allowed for the symbol
- **Spread Check**: Current spread within acceptable limits
- **Position Limits**: Maximum positions not exceeded
- **Risk Management**: Position size within risk limits

### 5.3 Validation Response Codes

| Code | Description | Action |
|------|-------------|--------|
| 0 | Valid signal | Proceed to execution |
| 100 | Invalid format | Reject signal |
| 101 | Missing required field | Reject signal |
| 102 | Invalid data type | Reject signal |
| 200 | Unknown symbol | Reject signal |
| 201 | Confidence too low | Reject signal |
| 202 | Strategy not mapped | Reject signal |
| 300 | Market closed | Queue for later |
| 301 | Spread too wide | Retry with delay |
| 302 | Position limit reached | Reject signal |

---

## 6. Error Handling

### 6.1 Communication Errors

**Error Hierarchy:**
1. **Socket Errors**: Automatic failover to Named Pipes
2. **Pipe Errors**: Automatic failover to File System
3. **File Errors**: System alert and manual intervention required

### 6.2 Execution Errors

**Retry Logic for Common MT4 Errors:**
- **Error 130** (Invalid Stops): Adjust stops and retry (max 3 attempts)
- **Error 136** (No Prices): Wait and retry with exponential backoff
- **Error 138** (Requote): Accept new price if within tolerance

### 6.3 Error Response Format

```json
{
    "message_type": "ERROR",
    "message_id": "err_20250703_142530_001",
    "timestamp": 1672531201.456,
    "source": "mql4",
    "version": "1.0",
    "payload": {
        "original_signal_id": "sig_20250703_142530_001",
        "error_code": 130,
        "error_message": "Invalid stops",
        "retry_count": 1,
        "max_retries": 3,
        "next_retry_time": 1672531202.456
    }
}
```

---

## 7. Performance Requirements

### 7.1 Latency Targets

| Component | Target Latency | Maximum Latency |
|-----------|----------------|-----------------|
| Signal Reception | < 1ms | 5ms |
| Validation | < 1ms | 3ms |
| Parameter Resolution | < 1ms | 2ms |
| Order Preparation | < 2ms | 5ms |
| Status Reporting | < 5ms | 10ms |
| **Total Overhead** | **< 10ms** | **25ms** |

*Note: Broker execution time (20-50ms) not included*

### 7.2 Throughput Requirements

- **Signal Processing**: 100 signals/second sustained
- **Concurrent EAs**: 30 currency pairs simultaneously
- **Communication Channels**: 1000 messages/second per channel

---

## 8. Implementation Templates

### 8.1 Python Signal Generator Template

```python
import json
import time
import uuid
from typing import Dict, Any, Optional

class MT4SignalGenerator:
    def __init__(self, source_name: str):
        self.source = source_name
        self.version = "1.0"
    
    def create_signal(self, 
                     symbol: str,
                     action: str,
                     confidence: float,
                     strategy_id: str,
                     stop_loss: Optional[int] = None,
                     take_profit: Optional[int] = None,
                     lot_size: Optional[float] = None,
                     parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Create a standardized MT4 signal.
        
        Args:
            symbol: Currency pair (e.g., "EURUSD")
            action: "BUY" or "SELL"
            confidence: Signal confidence (0.0-1.0)
            strategy_id: Unique strategy identifier
            stop_loss: Stop loss in pips (optional)
            take_profit: Take profit in pips (optional)
            lot_size: Position size (optional)
            parameters: Additional strategy parameters (optional)
        
        Returns:
            Standardized signal dictionary
        """
        # Validate required parameters
        if not symbol or not action or not strategy_id:
            raise ValueError("Missing required signal parameters")
        
        if confidence < 0.0 or confidence > 1.0:
            raise ValueError("Confidence must be between 0.0 and 1.0")
        
        if action not in ["BUY", "SELL"]:
            raise ValueError("Action must be 'BUY' or 'SELL'")
        
        # Create signal payload
        payload = {
            "symbol": symbol.upper(),
            "action": action.upper(),
            "confidence": confidence,
            "strategy_id": strategy_id,
            "signal_time": time.time()
        }
        
        # Add optional parameters
        if stop_loss is not None:
            payload["stop_loss"] = stop_loss
        if take_profit is not None:
            payload["take_profit"] = take_profit
        if lot_size is not None:
            payload["lot_size"] = lot_size
        if parameters is not None:
            payload["parameters"] = parameters
        
        # Create complete message
        signal = {
            "message_type": "SIGNAL",
            "message_id": f"sig_{int(time.time())}_{uuid.uuid4().hex[:8]}",
            "timestamp": time.time(),
            "source": self.source,
            "version": self.version,
            "payload": payload
        }
        
        return signal
    
    def validate_signal(self, signal: Dict[str, Any]) -> bool:
        """Validate signal format before transmission."""
        required_fields = ["message_type", "message_id", "timestamp", "source", "version", "payload"]
        payload_required = ["symbol", "action", "confidence", "strategy_id", "signal_time"]
        
        # Check message structure
        for field in required_fields:
            if field not in signal:
                return False
        
        # Check payload structure
        payload = signal.get("payload", {})
        for field in payload_required:
            if field not in payload:
                return False
        
        return True

# Usage Example
generator = MT4SignalGenerator("my_strategy")

signal = generator.create_signal(
    symbol="EURUSD",
    action="BUY",
    confidence=0.85,
    strategy_id="momentum_v1",
    stop_loss=50,
    take_profit=100,
    parameters={"rsi": 30.5, "ma_trend": "UP"}
)

if generator.validate_signal(signal):
    print("Signal ready for transmission")
    print(json.dumps(signal, indent=2))
```

### 8.2 Signal Validation Checklist

**Pre-Transmission Validation:**
- [ ] All required fields present
- [ ] Data types correct
- [ ] Symbol format valid (uppercase, known pair)
- [ ] Action is "BUY" or "SELL"
- [ ] Confidence between 0.0 and 1.0
- [ ] Strategy ID mapped in configuration
- [ ] Timestamp reasonable (within ±5 minutes)
- [ ] JSON format valid
- [ ] Message size under limit (1KB recommended)

**Post-Reception Validation:**
- [ ] Message received intact
- [ ] Validation rules passed
- [ ] Parameter set resolved
- [ ] Trading conditions met
- [ ] Risk management approved

---

## 9. Testing and Validation

### 9.1 Signal Testing Framework

**Test Categories:**
1. **Format Testing**: Validate message structure and encoding
2. **Communication Testing**: Test all three communication channels
3. **Performance Testing**: Measure latency and throughput
4. **Error Testing**: Verify error handling and recovery
5. **Integration Testing**: End-to-end signal to execution

### 9.2 Test Signal Examples

**Valid Minimum Signal:**
```json
{
    "message_type": "SIGNAL",
    "message_id": "test_001",
    "timestamp": 1672531200.123,
    "source": "test",
    "version": "1.0",
    "payload": {
        "symbol": "EURUSD",
        "action": "BUY",
        "confidence": 0.75,
        "strategy_id": "test_strategy",
        "signal_time": 1672531200.123
    }
}
```

**Signal with All Optional Fields:**
```json
{
    "message_type": "SIGNAL",
    "message_id": "test_002",
    "timestamp": 1672531200.123,
    "source": "test",
    "version": "1.0",
    "payload": {
        "symbol": "GBPUSD",
        "action": "SELL",
        "confidence": 0.92,
        "strategy_id": "advanced_test",
        "signal_time": 1672531200.123,
        "stop_loss": 30,
        "take_profit": 80,
        "lot_size": 0.05,
        "magic_number": 54321,
        "parameters": {
            "entry_price": 1.2650,
            "volatility": 0.015,
            "momentum": "STRONG_DOWN"
        }
    }
}
```

### 9.3 Performance Benchmarks

**Communication Channel Performance:**
- Socket: 1-3ms average latency
- Named Pipes: 3-5ms average latency  
- File System: 10-50ms average latency

**Processing Performance:**
- Validation: <1ms per signal
- Parameter Resolution: <1ms per signal
- Total Processing: <10ms per signal

---

## Conclusion

This specification provides the complete framework for developing signals that interface with the MT4 execution engine. **All signal generators must implement this specification exactly** to ensure reliable execution regardless of communication channel or generation method.

**Key Success Factors:**
- Follow the standardized signal format exactly
- Implement proper validation before transmission
- Handle communication failures gracefully
- Test across all communication channels
- Monitor performance metrics

For implementation support and additional resources, refer to the system's technical documentation and sample code provided in the project repository.