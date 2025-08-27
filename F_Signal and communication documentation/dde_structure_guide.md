# MT4 DDE Structure Guide for Trading System

## Overview
This document defines the exact DDE structure required for real-time price feeds from MT4 to the Excel-based trading system. The DDE integration feeds into the `PriceFeeds` worksheet and is monitored by the `price_monitor.bas` module.

---

## MT4 Terminal Requirements

### **1. MT4 DDE Server Configuration**
**Location:** MT4 Terminal → Tools → Options → Server
- ✅ **Enable DDE server** must be checked
- ✅ MT4 terminal must be **online and connected** to broker
- ✅ Symbols must be visible in **Market Watch** window
- ⚠️ DDE only works when **new ticks arrive** (ADVISE mode)

### **2. Symbol Requirements**
**Required symbols in MT4 Market Watch:**
- EURUSD, GBPUSD, USDJPY, USDCHF, AUDUSD, USDCAD, NZDUSD
- **Add symbols:** Right-click Market Watch → Show All → Select required pairs
- **Verify ticks:** Ensure bid/ask prices change periodically

---

## Excel DDE Configuration

### **1. Excel Settings Required**
**Location:** Excel → Tools → Options → International
- ✅ **Enable Translation formula entry** (critical for DDE)
- ✅ **Automatic calculation** enabled
- ✅ **Enable background refresh** for external data

### **2. PriceFeeds Worksheet DDE Structure**

```
Row 1: Headers
A1: Symbol | B1: Bid | C1: Ask | D1: Spread | E1: LastUpdate | F1: Source

Row 2: EURUSD
A2: EURUSD
B2: =MT4|BID!EURUSD
C2: =MT4|ASK!EURUSD  
D2: =C2-B2
E2: =MT4|TIME!EURUSD
F2: =IF(ISERROR(B2),"ERROR",IF(B2="N/A","WAITING","ACTIVE"))

Row 3: GBPUSD
A3: GBPUSD
B3: =MT4|BID!GBPUSD
C3: =MT4|ASK!GBPUSD
D3: =C3-B3
E3: =MT4|TIME!GBPUSD
F3: =IF(ISERROR(B3),"ERROR",IF(B3="N/A","WAITING","ACTIVE"))

[Continue pattern for all symbols...]
```

### **3. DDE Formula Syntax**
**Correct MT4 DDE Format:**
```
=MT4|BID!EURUSD     → Current bid price
=MT4|ASK!EURUSD     → Current ask price  
=MT4|HIGH!EURUSD    → Daily high price
=MT4|LOW!EURUSD     → Daily low price
=MT4|TIME!EURUSD    → Last update time
=MT4|QUOTE!EURUSD   → Complete quote string
```

**❌ Common Mistakes:**
```
=MT4|QUOTE!EURUSD.BID    (Wrong - don't use .BID suffix)
=MT4|EURUSD!BID          (Wrong - reversed order)
=DDE("MT4","BID","EURUSD") (Works but not recommended)
```

---

## VBA Integration Structure

### **1. price_monitor.bas DDE Functions**

```vba
' Updated UpdatePriceFeeds function
Public Function UpdatePriceFeeds() As Boolean
    On Error GoTo ErrorHandler
    
    If Not m_isInitialized Then Exit Function
    
    Dim ws As Worksheet
    Set ws = ThisWorkbook.Worksheets("PriceFeeds")
    
    Dim l_activeFeeds As Long
    l_activeFeeds = 0
    
    ' Check each symbol's DDE status
    Dim i As Long
    For i = 2 To 8 ' Rows 2-8 for 7 major pairs
        If ValidateDDEFeed(i, ws) Then
            l_activeFeeds = l_activeFeeds + 1
        End If
    Next i
    
    ' Update overall DDE status
    UpdateDDEConnectionStatus l_activeFeeds
    
    UpdatePriceFeeds = (l_activeFeeds > 0)
    Exit Function
    
ErrorHandler:
    UpdatePriceFeeds = False
End Function

Private Function ValidateDDEFeed(row As Long, ws As Worksheet) As Boolean
    ' Check if DDE feed is working for this symbol
    Dim l_bidValue As Variant
    Dim l_sourceStatus As String
    
    l_bidValue = ws.Cells(row, 2).Value    ' Bid price
    l_sourceStatus = ws.Cells(row, 6).Value ' Source status
    
    ' Check for DDE errors
    If IsError(l_bidValue) Then
        ws.Cells(row, 6).Value = "ERROR"
        ValidateDDEFeed = False
    ElseIf l_bidValue = "N/A" Or l_bidValue = "#N/A" Then
        ws.Cells(row, 6).Value = "WAITING"
        ValidateDDEFeed = False
    ElseIf IsNumeric(l_bidValue) And l_bidValue > 0 Then
        ws.Cells(row, 6).Value = "ACTIVE"
        ValidateDDEFeed = True
    Else
        ws.Cells(row, 6).Value = "INVALID"
        ValidateDDEFeed = False
    End If
End Function
```

### **2. DDE Connection Management**

```vba
Public Function InitializeDDEConnections() As Boolean
    ' Verify MT4 DDE server availability
    On Error GoTo ErrorHandler
    
    ' Test connection with simple DDE request
    Dim l_testChannel As Long
    l_testChannel = Application.DDEInitiate("MT4", "BID")
    
    If l_testChannel <> 0 Then
        Application.DDETerminate l_testChannel
        m_ddeStatus = "CONNECTED"
        InitializeDDEConnections = True
    Else
        m_ddeStatus = "FAILED"
        InitializeDDEConnections = False
    End If
    
    Exit Function
    
ErrorHandler:
    m_ddeStatus = "ERROR: " & Err.Description
    InitializeDDEConnections = False
End Function
```

---

## Error Handling Structure

### **1. DDE Status Monitoring**
**Possible DDE States:**
- **ACTIVE** - Receiving live prices
- **WAITING** - Connected but no new ticks (shows N/A)
- **ERROR** - DDE formula error (#REF!, #NAME?, etc.)
- **STALE** - Last update > 5 minutes ago
- **DISCONNECTED** - MT4 terminal offline

### **2. Fallback Mechanisms**

**Priority Order:**
1. **Live DDE feeds** (preferred)
2. **Last known prices** (if DDE temporary failure)
3. **Manual price entry** (emergency mode)
4. **Disable price-based signals** (safety mode)

**Implementation in price_monitor.bas:**
```vba
Private Function GetReliablePrice(symbol As String, priceType As String) As Double
    ' Try DDE first
    Dim l_ddePrice As Double
    l_ddePrice = GetDDEPrice(symbol, priceType)
    
    If l_ddePrice > 0 Then
        ' Update cache with fresh price
        UpdatePriceCache symbol, priceType, l_ddePrice
        GetReliablePrice = l_ddePrice
    Else
        ' Fall back to cached price
        GetReliablePrice = GetCachedPrice(symbol, priceType)
    End If
End Function
```

---

## System Integration Points

### **1. Health Monitoring Integration**
**In health_monitor.bas:**
- Monitor DDE connection status
- Alert when feeds go stale
- Track DDE error frequency

### **2. Configuration Requirements**
**In ConfigStore worksheet:**
```
CATEGORY    PARAMETER           VALUE       TYPE
DDE         ENABLED            TRUE        BOOLEAN
DDE         TIMEOUT_SECONDS    300         INTEGER  
DDE         RETRY_ATTEMPTS     3           INTEGER
DDE         FALLBACK_MODE      CACHE       STRING
```

### **3. Dashboard Display**
**In MainDashboard (A4:B10):**
```
DDE Status:     [ACTIVE/ERROR/WAITING]
Active Feeds:   [5/7 symbols]
Last Update:    [timestamp]
Error Count:    [daily error count]
```

---

## Troubleshooting Guide

### **Common DDE Issues:**

**1. "N/A" in all price cells**
- ✅ Check MT4 "Enable DDE server" setting
- ✅ Verify symbols in Market Watch
- ✅ Wait for new ticks to arrive
- ✅ Check Excel "Translation formula entry"

**2. "#NAME?" error**
- ✅ Verify exact DDE syntax: `=MT4|BID!EURUSD`
- ✅ Check Excel DDE settings
- ✅ Restart Excel and MT4

**3. Prices not updating**
- ✅ Verify MT4 is online (see connection status)
- ✅ Check if market is open
- ✅ Verify broker data feed is active

**4. "Application-defined error"**
- ✅ MT4 terminal may be closed
- ✅ DDE server may be disabled
- ✅ Windows DDE service issues

### **Diagnostic Commands:**
```vba
' Test DDE availability
Public Function TestDDEConnection() As String
    On Error Resume Next
    Dim l_channel As Long
    l_channel = Application.DDEInitiate("MT4", "BID")
    
    If Err.Number = 0 Then
        Application.DDETerminate l_channel
        TestDDEConnection = "DDE Available"
    Else
        TestDDEConnection = "DDE Error: " & Err.Description
    End If
End Function
```

---

## Implementation Checklist

### **Pre-Implementation:**
- [ ] MT4 terminal installed and configured
- [ ] DDE server enabled in MT4
- [ ] Required symbols added to Market Watch
- [ ] Excel translation settings configured

### **Implementation Steps:**
- [ ] Create DDE formulas in PriceFeeds worksheet
- [ ] Update price_monitor.bas with DDE functions
- [ ] Add error handling and fallback logic
- [ ] Test with live MT4 connection
- [ ] Implement health monitoring

### **Testing Verification:**
- [ ] All 7 symbols show "ACTIVE" status
- [ ] Prices update when market moves
- [ ] Error handling works when MT4 disconnected
- [ ] Fallback to cached prices functions
- [ ] System continues operating during DDE failures

This structure ensures reliable price feeds while maintaining system stability when DDE connections fail.