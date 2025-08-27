# MQL4_DLL_SocketBridge

A Windows DLL that provides socket communication between MetaTrader 4 Expert Advisors and external applications (Python interface).

## Overview

This DLL implements a TCP socket server that allows real-time bidirectional communication between:
- MT4 Expert Advisor (MQL4 code)
- Python monitoring interface
- External trading applications

## Features

- **TCP Socket Server**: Listens on configurable port (default 5555)
- **Single Client Support**: One Python client connection at a time
- **Message Queuing**: Buffered message handling with thread safety
- **Heartbeat Monitoring**: Connection health checking
- **Windows Message Integration**: Optional MT4 window message notifications
- **Debug Logging**: Configurable debug output to console
- **Error Handling**: Comprehensive error reporting and recovery

## Build Requirements

- **Visual Studio 2019** or later with C++ build tools
- **CMake 3.10** or later
- **Windows SDK**
- **Windows 10/11** (32-bit or 64-bit, but DLL must be 32-bit for MT4)

## Building the DLL

### Option 1: Using the Build Script (Recommended)
```batch
cd MQL4_DLL_SocketBridge
build_dll.bat
```

### Option 2: Manual CMake Build
```batch
mkdir build
cd build
cmake .. -G "Visual Studio 16 2019" -A Win32
cmake --build . --config Release
```

The compiled DLL will be located at: `build/Release/MQL4_DLL_SocketBridge.dll`

## Installation

1. **Copy DLL**: Place `MQL4_DLL_SocketBridge.dll` in your MT4 installation directory:
   ```
   <MT4_Installation_Path>\MQL4\Libraries\MQL4_DLL_SocketBridge.dll
   ```

2. **Enable DLL Imports**: In MT4:
   - Tools → Options → Expert Advisors
   - Check "Allow DLL imports"
   - Restart MT4

3. **Load EA**: Load the HUEY_P Expert Advisor with DLL signals enabled:
   ```mql4
   EnableDLLSignals = true
   ListenPort = 5555  // or your preferred port
   ```

## API Reference

### Core Functions (called by MT4 EA)

```cpp
// Start the socket server
int StartServer(int port, int hWnd, int messageId);

// Stop the server and close all connections
void StopServer();

// Get the next message from client (non-blocking)
int GetLastMessage(char buffer[], int maxSize);

// Check server and connection status
int GetCommunicationStatus();

// Check if a client is connected
bool SocketIsConnected(int socketId);

// Get last error message
const char* GetLastSocketError();

// Send heartbeat to client
bool SocketSendHeartbeat(int socketId);
```

### Extended Functions

```cpp
// Send custom message to client
bool SendMessageToClient(const char* message);

// Get number of connected clients (0 or 1)
int GetConnectedClientCount();

// Enable/disable debug logging
void SetDebugMode(bool enabled);
```

### Status Constants

```cpp
#define STATUS_CONNECTED    1   // Client connected
#define STATUS_DISCONNECTED 0   // Server running, no client
#define STATUS_ERROR       -1   // Server error or not running
```

## Communication Protocol

### Message Format
- **Text-based**: UTF-8 encoded strings
- **Delimiter**: Messages should be newline-terminated (`\n`)
- **Max Size**: 4096 bytes per message
- **Encoding**: Plain text or JSON formatted

### Standard Messages

#### From Python to MT4:
```json
{"type": "SIGNAL", "action": "BUY", "symbol": "EURUSD", "price": 1.1234}
{"type": "STATUS_REQUEST"}
{"type": "HEARTBEAT"}
```

#### From MT4 to Python:
```json
{"type": "TRADE_UPDATE", "ticket": 12345, "profit": 25.50, "symbol": "EURUSD"}
{"type": "STATUS_RESPONSE", "state": "TRADE_TRIGGERED", "equity": 5000.00}
{"type": "HEARTBEAT"}
```

## Usage Example

### MT4 EA Code
```mql4
// Global variables
int g_socket_status = STATUS_ERROR;
string g_last_message = "";

// OnInit()
int OnInit() {
    // Start socket server on port 5555
    g_socket_status = StartServer(5555, 0, 0);
    
    if (g_socket_status == STATUS_CONNECTED) {
        Print("Socket server started successfully");
    } else {
        Print("Failed to start socket server: ", GetLastSocketError());
    }
    
    return INIT_SUCCEEDED;
}

// OnTick()
void OnTick() {
    // Check for new messages
    char buffer[4096];
    int msg_length = GetLastMessage(buffer, 4096);
    
    if (msg_length > 0) {
        g_last_message = CharArrayToString(buffer);
        Print("Received message: ", g_last_message);
        ProcessMessage(g_last_message);
    }
    
    // Send heartbeat every 30 seconds
    static datetime last_heartbeat = 0;
    if (TimeCurrent() - last_heartbeat >= 30) {
        SocketSendHeartbeat(0);
        last_heartbeat = TimeCurrent();
    }
}

// OnDeinit()
void OnDeinit(const int reason) {
    StopServer();
    Print("Socket server stopped");
}
```

### Python Client Code
```python
import socket
import json
import threading
import time

class MT4Bridge:
    def __init__(self, host='localhost', port=5555):
        self.host = host
        self.port = port
        self.socket = None
        self.connected = False
        
    def connect(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.connected = True
            print(f"Connected to MT4 bridge at {self.host}:{self.port}")
            return True
        except Exception as e:
            print(f"Failed to connect: {e}")
            return False
    
    def send_message(self, message):
        if not self.connected:
            return False
        try:
            self.socket.send(message.encode('utf-8'))
            return True
        except Exception as e:
            print(f"Send failed: {e}")
            self.connected = False
            return False
    
    def receive_messages(self):
        while self.connected:
            try:
                data = self.socket.recv(4096)
                if data:
                    message = data.decode('utf-8')
                    self.handle_message(message)
                else:
                    break
            except Exception as e:
                print(f"Receive error: {e}")
                break
        self.connected = False
    
    def handle_message(self, message):
        print(f"Received from MT4: {message}")
        # Process message here
        
    def send_signal(self, action, symbol, price):
        signal = {
            "type": "SIGNAL",
            "action": action,
            "symbol": symbol,
            "price": price
        }
        return self.send_message(json.dumps(signal))

# Usage
bridge = MT4Bridge()
if bridge.connect():
    # Start message receiver thread
    receiver_thread = threading.Thread(target=bridge.receive_messages)
    receiver_thread.daemon = True
    receiver_thread.start()
    
    # Send a trading signal
    bridge.send_signal("BUY", "EURUSD", 1.1234)
```

## Troubleshooting

### Common Issues

1. **DLL Not Found**
   - Ensure DLL is in correct MT4/MQL4/Libraries/ folder
   - Check that "Allow DLL imports" is enabled in MT4 settings
   - Verify DLL is 32-bit (MT4 requirement)

2. **Connection Refused**
   - Check if port is already in use
   - Verify Windows firewall settings
   - Ensure MT4 EA has called StartServer()

3. **Messages Not Received**
   - Check message format and size limits
   - Verify client is properly connected
   - Enable debug mode for detailed logging

4. **Build Errors**
   - Ensure Visual Studio C++ build tools are installed
   - Check CMake version (3.10+ required)
   - Verify Windows SDK is available

### Debug Mode

Enable debug logging in your EA:
```mql4
SetDebugMode(true);  // Call this in OnInit()
```

This will output detailed connection and message information to the console.

## Security Considerations

- **Local Connections Only**: Server binds to localhost (127.0.0.1) by default
- **No Authentication**: This is a basic implementation - add authentication for production use
- **Port Management**: Use non-standard ports to avoid conflicts
- **Input Validation**: Validate all received messages before processing
- **Resource Limits**: Message queue is limited to prevent memory exhaustion

## License

This DLL is provided as a defensive security tool for legitimate trading system integration. Use responsibly and in accordance with your broker's terms of service.