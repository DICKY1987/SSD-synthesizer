# 📘 Comprehensive System Documentation (Filled from Sources)

## 1.0 System Overview & Architecture
**1.1 Purpose and Scope**  
The `MQL4_DLL_SocketBridge` is a Windows DLL providing socket communication between the MetaTrader 4 (MT4) Expert Advisor (EA) and external applications such as a Python interface. It enables real-time bidirectional communication for trading signals and monitoring【16†MQL4_DLL_SocketBridge】.

**1.2 Architectural Diagrams (C4, component, network)**  
_Not provided in documents._

**1.3 Data Flow Diagrams (DFDs)**  
_Not provided in documents._

**1.4 Stakeholders & Responsibilities**  
_Not provided._

**1.5 Trading Philosophy & Strategic Approach**  
Referenced in HUEY_P integration: DLL used to bridge MT4 Expert Advisor with Python-driven strategies and external monitoring【14†DLL_REQUIREMENTS】.  

---

## 2.0 Data Models & Persistence
**2.1 Logical Data Model**  
_Not explicitly defined._

**2.2 Physical Database Schema**  
_Not in provided docs._

**2.3 State Management & Persistence Rules**  
Buffered message queuing with thread safety implemented inside DLL【16†MQL4_DLL_SocketBridge】.

**2.4 Data Retention & Archival Policies**  
_Not specified._

**2.5 Terminal-Specific Persistence Mechanisms**  
MT4 requires the DLL placed in `<MT4_Data_Folder>\MQL4\Libraries\` and parameters like `EnableDLLSignals` and `ListenPort` configured in EA【14†DLL_REQUIREMENTS】.  

---

## 3.0 Interfaces & APIs
**3.1 API Specifications**  
Custom C++ DLL API exported to MT4【13†DLL_BUILD_SUMMARY】【16†MQL4_DLL_SocketBridge】.

**3.2 Detailed Endpoint Contracts**  
Exported functions include:  
- `StartServer`, `StopServer`, `GetLastMessage`, `GetCommunicationStatus`, `SocketIsConnected`, `GetLastSocketError`, `SocketSendHeartbeat`, `SendMessageToClient`, `GetConnectedClientCount`, `SetDebugMode`【13†DLL_BUILD_SUMMARY】.

**3.3 Function-Level Contracts**  
See API reference for expected inputs/outputs【16†MQL4_DLL_SocketBridge】.

**3.4 Integration Points**  
- MT4 EA (MQL4 code)  
- Python monitoring interface  
- External trading applications【16†MQL4_DLL_SocketBridge】  

**3.5 Communication Contracts (Runtime Bridges)**  
- Protocol: TCP sockets (localhost, default port 5555, fallback 9999)  
- Message format: UTF-8 text or JSON, newline-delimited, max 4096 bytes【13†DLL_BUILD_SUMMARY】【14†DLL_REQUIREMENTS】【16†MQL4_DLL_SocketBridge】  
- Heartbeats every 30 seconds【13†DLL_BUILD_SUMMARY】  
- Error codes via `GetLastSocketError()`  

**3.6 Signal Queueing & Ordering Guarantees**  
Message queuing implemented with thread safety【16†MQL4_DLL_SocketBridge】.  

**3.7 Legacy Integration Modules**  
DLL bridge (C++ socket server for MT4)【14†DLL_REQUIREMENTS】.  

---

## 4.0 Core Logic & Behavior
**4.1 Business Logic & Algorithms**  
The DLL provides server-side socket communication for EA-to-Python message relay【16†MQL4_DLL_SocketBridge】.

**4.2 Error Handling & Exception Strategy**  
- Comprehensive error reporting (`GetLastSocketError`)  
- Warnings noted during build: `inet_ntoa` deprecation, `localtime` safety【13†DLL_BUILD_SUMMARY】  

**4.3 Edge Case Specifications**  
Fallback to CSV file-based signals if DLL unavailable【14†DLL_REQUIREMENTS】.

**4.4 Embedded Annotations**  
_Not covered._

**4.5 Safety Controls**  
- Localhost binding (127.0.0.1)  
- Single-client restriction  
- Input validation and buffer overflow protection【13†DLL_BUILD_SUMMARY】【16†MQL4_DLL_SocketBridge】  

**4.6 Adaptive Reentry Logic**  
_Not included in these documents._

---

## 5.0 Deployment & Operations
**5.1 Infrastructure & Environment Requirements**  
- Windows OS (10/11)  
- Visual Studio 2019/2022 Build Tools  
- CMake 3.10+ (4.1.0 confirmed)  
- Windows SDK【13†DLL_BUILD_SUMMARY】【16†MQL4_DLL_SocketBridge】  

**5.2 Dependency Specifications**  
- `ws2_32.lib` (Windows socket library)【15†CMakeCache】  
- Kernel32, user32, and standard Windows libraries auto-linked【15†CMakeCache】  

**5.3 Configuration & Secrets Management**  
MT4 EA configuration requires `EnableDLLSignals=true`, `ListenPort=5555`【13†DLL_BUILD_SUMMARY】【14†DLL_REQUIREMENTS】.  

**5.4 Build & Deployment Process**  
- Build via CMake + Visual Studio (Release, Win32 target)【13†DLL_BUILD_SUMMARY】【17†CMakeLists.txt】  
- DLL output copied to `<MT4_Installation>/MQL4/Libraries/`【14†DLL_REQUIREMENTS】  

**5.5 Operational Runbooks**  
- Enable DLL imports in MT4  
- Restart MT4 after placement  
- Launch Python interface via `python huey_main.py`【13†DLL_BUILD_SUMMARY】  

**5.6 Broker/Terminal Failover SOP**  
CSV signals available if DLL unavailable【14†DLL_REQUIREMENTS】.  

**5.7 Observability & SLOs**  
Debug logging can be enabled via `SetDebugMode(true)`【16†MQL4_DLL_SocketBridge】.  

---

## 6.0 Non-Functional Requirements (NFRs)
**6.1 Performance**  
Max message size: 4096 bytes【13†DLL_BUILD_SUMMARY】【16†MQL4_DLL_SocketBridge】.

**6.2 Scalability**  
Single client connection only【13†DLL_BUILD_SUMMARY】.

**6.3 Availability & Reliability**  
- Thread-safe implementation  
- Recovery via error handling functions【13†DLL_BUILD_SUMMARY】【16†MQL4_DLL_SocketBridge】  

**6.4 Auditing & Logging**  
Debug logs via `SetDebugMode`【16†MQL4_DLL_SocketBridge】.  

**6.5 Deterministic Replay & Time Sync**  
_Not included._

**6.6 Immutable Audit Logging**  
_Not covered._

**6.7 Temporal/Regional Handling**  
_Not covered._

---

## 7.0 Security Specifications
- Localhost-only binding【13†DLL_BUILD_SUMMARY】【16†MQL4_DLL_SocketBridge】  
- No authentication (note: production should add auth)【16†MQL4_DLL_SocketBridge】  
- Input validation for buffer overflows【13†DLL_BUILD_SUMMARY】  

---

## 8.0 Model Governance (for AI/Trading Systems)  
_Not covered in these DLL-specific docs._

---

## 9.0 Requirements Traceability (RTM Layer)  
REQ-001: System SHALL provide socket-based communication between MT4 EA and Python client via `MQL4_DLL_SocketBridge.dll`【14†DLL_REQUIREMENTS】【16†MQL4_DLL_SocketBridge】.  

---

## 10.0 Cross-View Linking  
DLL requirements linked to EA integration points (`EnableDLLSignals`, `ListenPort`)【14†DLL_REQUIREMENTS】.  

---

## 11.0 Export Strategy  
The system builds as a 32-bit DLL (`MQL4_DLL_SocketBridge.dll`) and is deployed into MT4 for EA-to-Python communication【13†DLL_BUILD_SUMMARY】【14†DLL_REQUIREMENTS】.  
