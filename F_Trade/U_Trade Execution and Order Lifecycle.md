# 11. Trade Execution and Order Lifecycle

## 11.1 Purpose

This document specifies the architecture, data models, event flow, and error handling logic for the Trade Execution Service in the enhanced Python-MT5/MT4-based trading system. It handles signal-to-order conversion, order placement, lifecycle state transitions, and broker feedback integration.

---

## 11.2 System Components

### 11.2.1 Trade Execution Service (`services/trade_execution_service.py`)

**Responsibilities:**

* Receive trade signals
* Convert signals to executable orders
* Send orders via broker interface (e.g., MetaTrader5)
* Track order states (PENDING → FILLED → CLOSED)
* Handle failures, rejections, slippage, and retry policies

### 11.2.2 Broker Interface Layer

**Supported Platforms:**

* MetaTrader 5 via Python API
* MT4 via Bridge (DLL or file-based)

**Pluggable Design:**

```python
class BrokerInterface(ABC):
    @abstractmethod
    def place_order(self, signal: SignalModel) -> OrderResult:
        pass

    @abstractmethod
    def get_order_status(self, order_id: str) -> OrderStatus:
        pass

    @abstractmethod
    def close_order(self, order_id: str) -> bool:
        pass
```

---

## 11.3 Order Lifecycle States

```text
RECEIVED → VALIDATED → SUBMITTED → FILLED → CLOSED
                          ↓
                     REJECTED/FAILED
```

### Lifecycle Enum

```python
class OrderState(Enum):
    RECEIVED = 'RECEIVED'
    VALIDATED = 'VALIDATED'
    SUBMITTED = 'SUBMITTED'
    FILLED = 'FILLED'
    CLOSED = 'CLOSED'
    FAILED = 'FAILED'
    REJECTED = 'REJECTED'
```

---

## 11.4 Execution Flow

### 11.4.1 From Signal to Execution

```python
async def handle_signal(signal: SignalModel):
    validate(signal)
    order = create_order_from_signal(signal)
    result = broker_interface.place_order(order)

    if result.success:
        track_order(result.order_id)
    else:
        log_failure(signal.id, result.error)
```

### 11.4.2 Signal to Order Mapping

```python
class OrderModel(BaseModel):
    symbol: str
    direction: str  # BUY or SELL
    volume: float
    entry_price: Optional[float]
    stop_loss: Optional[float]
    take_profit: Optional[float]
    strategy_id: str
    signal_id: UUID
```

---

## 11.5 Risk & Margin Checks

Before order placement:

* Validate free margin
* Check max leverage
* Limit order volume based on config policy

### Example Check:

```python
if not broker_interface.has_sufficient_margin(order.volume, order.symbol):
    raise RiskPolicyViolation("Insufficient margin")
```

---

## 11.6 Order Tracking and Feedback

* Orders are stored with broker-assigned IDs
* Periodically query broker for status updates
* Update order lifecycle
* Emit ORDER\_UPDATE events to message queue

---

## 11.7 Error Handling

| Error Type         | Handling Strategy                           |
| ------------------ | ------------------------------------------- |
| Rejected Order     | Retry up to 1x, then notify failure handler |
| Slippage Violation | Notify analytics + store for audit          |
| Timeout            | Trigger fallback broker (if multi-broker)   |

---

## 11.8 Future Extensions

* Trailing stop order types
* Multi-leg order support (bracket, OCO)
* Broker failover and execution queue
* Broker-specific adapter configuration
