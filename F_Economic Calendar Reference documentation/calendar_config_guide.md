# Economic Calendar System - Configuration and Usage Guide
## MQL4 Implementation with 5 Anticipation Events

### 🎯 System Overview

This system processes economic calendar CSV files and generates **5 anticipation events** for each high/medium impact event, creating a comprehensive trading calendar with:

- **Original Events**: High and Medium impact economic events (CHF excluded)
- **5 Anticipation Events**: Generated at 1, 2, 4, 8, and 12 hours before each original event
- **Equity Market Events**: Tokyo, London, and New York market opens
- **Strategy IDs**: 5-digit RCI (Regional-Country-Impact) codes for each event
- **Currency Mapping**: Automatic country-to-currency conversion

---

## 🔧 Configuration Settings

### Anticipation Hours Configuration
```mql4
// Default configuration: 1, 2, 4, 8, 12 hours before events
int AnticipationHours[MAX_ANTICIPATION_EVENTS] = {1, 2, 4, 8, 12};

// To change anticipation timing, use:
UpdateAnticipationHours(1, 3, 6, 12, 24); // New timing: 1h, 3h, 6h, 12h, 24h
```

### Event Naming Format
```
Original Event: "Non-Farm Payrolls - USD - High"

Generated Anticipation Events:
- "#1H Before Non-Farm Payrolls Anticipation - USD - High"
- "#2H Before Non-Farm Payrolls Anticipation - USD - High" 
- "#4H Before Non-Farm Payrolls Anticipation - USD - High"
- "#8H Before Non-Farm Payrolls Anticipation - USD - High"
- "#12H Before Non-Farm Payrolls Anticipation - USD - High"
```

---

## 🗺️ Country to Currency Mapping

| Region | Country | Currency Code | Strategy Region |
|--------|---------|---------------|-----------------|
| **North America** | USA/US | USD | 1 |
| | Canada | CAD | 1 |
| | Mexico | MXN | 1 |
| **Europe** | EUR/Eurozone | EUR | 2 |
| | UK/United Kingdom | GBP | 2 |
| | Switzerland | CHF | **EXCLUDED** |
| **Asia-Pacific** | Japan | JPY | 3 |
| | Australia | AUD | 3 |
| | New Zealand | NZD | 3 |
| | China | CNY | 3 |
| | South Korea | KRW | 3 |
| | Singapore | SGD | 3 |
| | Hong Kong | HKD | 3 |
| | India | INR | 3 |
| **Latin America** | Brazil | BRL | 4 |
| **Middle East/Africa** | South Africa | ZAR | 5 |
| | Turkey | TRY | 5 |
| | Russia | RUB | 5 |

---

## 🆔 Strategy ID Generation System

### 5-Digit RCI Format: [R][CC][I][X]
- **R**: Region Code (1 digit)
- **CC**: Country Code (2 digits)
- **I**: Impact Level (1 digit: 2=Medium, 3=High)
- **X**: Checksum (1 digit)

### Examples:
```
USA High Impact: 10132
- Region: 1 (North America)
- Country: 01 (USA)
- Impact: 3 (High)
- Checksum: 2

EUR Medium Impact: 20123
- Region: 2 (Europe)
- Country: 01 (EUR)
- Impact: 2 (Medium)
- Checksum: 3

JPY High Impact: 30137
- Region: 3 (Asia-Pacific)
- Country: 01 (JPY)
- Impact: 3 (High)
- Checksum: 7
```

### Anticipation Event Strategy IDs:
Anticipation events get **+1000** added to the original strategy ID:
- Original: 10132 → Anticipation: 11132

---

## 📅 Equity Market Events

Automatically added for each trading day:

| Market | Time (CST) | Currency | Event Type |
|--------|------------|----------|------------|
| **Tokyo Open** | 21:00 | JPY | EQT-OPEN |
| **London Open** | 02:00 | EUR | EQT-OPEN |
| **New York Open** | 08:30 | USD | EQT-OPEN |

**Special Strategy IDs for Equity Events:**
- Tokyo Open: 83015
- London Open: 82015  
- New York Open: 81015

---

## 📊 Event Processing Pipeline

### Input CSV Format (ForexFactory):
```csv
Title,Country,Date,Time,Impact,Forecast,Previous,URL
"Non-Farm Payrolls","USA","2024-01-05","08:30","High","185K","199K",""
"ECB Interest Rate Decision","EUR","2024-01-25","07:45","High","4.50%","4.50%",""
```

### Processing Steps:
1. **Read CSV** → Parse economic events
2. **Filter Events** → Keep only High/Medium impact, exclude CHF
3. **Generate Anticipation** → Create 5 anticipation events per original
4. **Add Equity Events** → Inject market open events
5. **Sort Chronologically** → Order by time with conflict resolution
6. **Generate Output CSV** → Final trading calendar

### Output CSV Format:
```csv
Date,Time,Event Name,Country,Currency,Impact,Event Type,Strategy ID,Hours Before,Priority,Offset Minutes
2024-01-05,02:30,"#6H Before Non-Farm Payrolls Anticipation - USD - High",USA,USD,High,ANTICIPATION,11132,6,20,-1
2024-01-05,04:30,"#4H Before Non-Farm Payrolls Anticipation - USD - High",USA,USD,High,ANTICIPATION,11132,4,20,-1
2024-01-05,06:30,"#2H Before Non-Farm Payrolls Anticipation - USD - High",USA,USD,High,ANTICIPATION,11132,2,20,-1
2024-01-05,07:30,"#1H Before Non-Farm Payrolls Anticipation - USD - High",USA,USD,High,ANTICIPATION,11132,1,20,-1
2024-01-05,08:30,"Non-Farm Payrolls",USA,USD,High,EMO-E,10132,0,100,-3
```

---

## ⚙️ Usage Instructions

### 1. Basic Setup
```mql4
// Initialize the system
int OnInit()
{
   Print("Economic Calendar System Initialized");
   Print(GetAnticipationConfig());
   return INIT_SUCCEEDED;
}
```

### 2. Process Calendar File
```mql4
// Process ForexFactory CSV file
bool success = ProcessEconomicCalendar("ff_calendar_thisweek.csv");
if(success)
{
   Print("Calendar processed successfully!");
   Print("Total events with anticipation: ", TotalEventsWithAnticipation);
}
```

### 3. Change Anticipation Timing
```mql4
// Update anticipation hours (example: 1h, 3h, 6h, 12h, 24h)
UpdateAnticipationHours(1, 3, 6, 12, 24);
Print(GetAnticipationConfig());

// Reprocess calendar with new timing
ProcessEconomicCalendar("ff_calendar_thisweek.csv");
```

### 4. Test Individual Functions
```mql4
// Test country mapping
string currency = MapCountryToCurrency("USA");        // Returns "USD"
string currency2 = MapCountryToCurrency("Japan");     // Returns "JPY"

// Test strategy ID generation
int strategyID = GenerateStrategyID("USA", "High");    // Returns 10132
int strategyID2 = GenerateStrategyID("EUR", "Medium"); // Returns 20123

// Test anticipation generation
EconomicEvent originalEvent;
originalEvent.event_time = TimeCurrent() + 3600; // 1 hour from now
originalEvent.event_name = "Test Event";
originalEvent.country = "USA";
originalEvent.currency = "USD";
originalEvent.impact = "High";

EconomicEvent anticipationEvents[];
GenerateAnticipationEvents(originalEvent, anticipationEvents);
// Creates 5 anticipation events at 1h, 2h, 4h, 8h, 12h before
```

---

## 🎛️ Advanced Configuration

### Event Priority System
```mql4
// Priority levels for chronological sorting
#define EVENT_EMO_E      100    // Highest priority
#define EVENT_EMO_A      80     
#define EVENT_EQT_OPEN   60     
#define EVENT_EQT_CLOSE  50     
#define EVENT_ANTICIPATION 20   // Lowest priority
```

### Offset Timing Rules
```mql4
// Trigger offsets (minutes before event)
EMO-E (High Impact):    -3 minutes
EMO-A (Medium Impact):  -2 minutes  
EQT-OPEN (Equity):      -5 minutes
ANTICIPATION:           -1 minute
```

### Time Conflict Resolution
Events closer than 5 minutes apart are automatically separated:
- Higher priority events keep their original time
- Lower priority events are moved ±5 minutes to avoid conflicts

---

## 📈 Capital Preservation Features

The system includes built-in risk management focused on capital preservation:

1. **Event Filtering**: Only trades on significant market events (High/Medium impact)
2. **CHF Exclusion**: Automatically excludes Swiss Franc events (low liquidity)
3. **Time Conflict Resolution**: Prevents overlapping signals
4. **Anticipation Trading**: Allows position entry before major announcements
5. **Equity Market Awareness**: Tracks major market open times
6. **Performance-Based Adjustments**: Strategy IDs link to performance-based parameter sets

---

## 🔄 Integration with Trading System

The generated CSV feeds directly into your MT4-Excel trading infrastructure:

1. **Strategy ID Lookup**: Use 5-digit codes to fetch trading parameters
2. **Performance Oscillator**: Map strategy performance to parameter sets
3. **Risk Assessment**: Adjust position sizing based on recent performance
4. **Signal Generation**: Convert calendar events to trading signals
5. **Trade Execution**: Send signals to MT4 Expert Advisors

This system transforms raw economic calendar data into a sophisticated, timing-precise trading calendar that maximizes opportunities while prioritizing capital preservation.