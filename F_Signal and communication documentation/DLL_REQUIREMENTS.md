# DLL Requirements and Setup Guide

## Critical Missing Component: MQL4_DLL_SocketBridge.dll

### Overview
The HUEY_P trading system requires a custom DLL for communication between the MT4 Expert Advisor and the Python interface. This DLL is **NOT included** in the codebase and must be obtained or compiled separately.

### Required DLL
- **File**: `MQL4_DLL_SocketBridge.dll`
- **Location**: Must be placed in `<MT4_Data_Folder>\MQL4\Libraries\`
- **Purpose**: Enables socket-based communication between EA and Python

### DLL Functions (as referenced in EA code)
The DLL must implement these exported functions:
```cpp
int  StartServer(int port, int hWnd, int messageId);
void StopServer();
int  GetLastMessage(char buffer[], int maxSize);
int  GetCommunicationStatus();
bool SocketIsConnected(int socketId);
const char* GetLastSocketError();
bool SocketSendHeartbeat(int socketId);
```

### Communication Protocol
- **Default Port**: 5555 (configurable via `ListenPort` parameter)
- **Fallback Port**: 9999 (Python interface)
- **Protocol**: TCP socket communication
- **Messages**: Structured JSON or delimited text

### Alternative Solutions (if DLL unavailable)

#### Option 1: File-Based Communication
- Enable CSV signals: `EnableCSVSignals = true`
- Use `trading_signals.csv` for signal exchange
- Less real-time but functional for basic operation

#### Option 2: Disable External Signals
- Set `EnableDLLSignals = false`
- Set `AutonomousMode = true` 
- EA operates independently without Python interface
- Python interface runs in monitoring-only mode

#### Option 3: Mock DLL Creation
Create a stub DLL with minimal functionality for testing:
```cpp
// Minimal stub implementation
extern "C" __declspec(dllexport) int StartServer(int port, int hWnd, int messageId) {
    return 1; // Success
}

extern "C" __declspec(dllexport) void StopServer() {
    // No-op
}

extern "C" __declspec(dllexport) int GetLastMessage(char buffer[], int maxSize) {
    return 0; // No messages
}
// ... implement other functions as stubs
```

### System Dependencies
The DLL likely depends on Windows socket libraries:
- `wsock32.dll` (automatically available on Windows)
- `ws2_32.dll` (automatically available on Windows)

### Testing Without DLL
1. **Set EA Parameters**:
   ```
   EnableDLLSignals = false
   AutonomousMode = true
   ```

2. **Python Interface**:
   - Will show "EA bridge connection failed" (expected)
   - Can still demonstrate UI functionality
   - Database operations work independently

### Next Steps
1. **Contact Developer**: Obtain the original DLL source or binary
2. **Develop Custom DLL**: Create socket bridge using Windows API
3. **Use Alternative Communication**: Implement file-based or database-based communication
4. **Testing Setup**: Use mock/stub DLL for development

### Current System Status
✅ **Python Interface**: Functional (with connection warnings)  
✅ **MQL4 EA Code**: Complete and compilable  
❌ **Socket Communication**: Blocked without DLL  
✅ **File-based Fallback**: Available as alternative  

The system can operate in limited mode without the DLL by using CSV signals or autonomous operation.