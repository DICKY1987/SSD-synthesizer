# 12. Broker Abstraction and Margin Model

## 12.1 Purpose

This document defines the design, interfaces, and operational constraints for integrating multiple brokers into the trading system. It also specifies a unified margin and leverage policy model for validating trades prior to execution.

---

## 12.2 Goals

* Enable support for multiple broker APIs (MT5, MT4, future REST/WS brokers)
* Abstract trading operations behind a common interface
* Provide consistent margin checking across brokers
* Enable fallback and primary/secondary routing logic

---

## 12.3 Broker Abstraction Layer

### Interface Contract

```python
class BrokerAdapter(ABC):
    @abstractmethod
    def initialize(self, config: Dict[str, Any]) -> None:
        pass

    @abstractmethod
    def place_order(self, order: OrderModel) -> OrderResult:
        pass

    @abstractmethod
    def close_order(self, order_id: str) -> bool:
        pass

    @abstractmethod
    def get_account_info(self) -> AccountInfo:
        pass

    @abstractmethod
    def has_sufficient_margin(self, symbol: str, volume: float) -> bool:
        pass
```

### Adapter Examples

* `MT5BrokerAdapter` — uses MetaTrader5 Python API
* `MT4BridgeAdapter` — communicates via DLL, pipe, or file-based bridge
* `OANDABrokerAdapter` — placeholder for RESTful integration

---

## 12.4 Broker Configuration Schema

```yaml
brokers:
  mt5:
    adapter: MT5BrokerAdapter
    login: 123456
    password: env:MT5_PASS
    server: MetaQuotes-Demo
    default: true

  mt4:
    adapter: MT4BridgeAdapter
    bridge_type: named_pipe
    bridge_path: "C:/bridge/pipe"
```

---

## 12.5 Margin and Leverage Validation

### AccountInfo Model

```python
class AccountInfo(BaseModel):
    balance: float
    equity: float
    margin: float
    free_margin: float
    leverage: int
    currency: str
```

### Margin Rule Enforcement

* Trade volume must not exceed available free margin
* Leverage rule: `required_margin = notional / leverage`

```python
def check_margin(account: AccountInfo, order: OrderModel) -> bool:
    notional = order.volume * get_symbol_price(order.symbol)
    required = notional / account.leverage
    return account.free_margin >= required
```

---

## 12.6 Broker Failover Logic

### Primary/Secondary Routing

* Default broker defined in config
* If failure (timeout/rejection), system attempts fallback broker

### Bridge Health Integration

* Failover honors bridge health status from `BridgeHealthMonitor`

```python
if not broker.place_order(order):
    fallback = broker_router.get_fallback(order.symbol)
    fallback.place_order(order)
```

---

## 12.7 Extensions

* Broker latency monitoring
* Broker fill quality scoring
* Real-time margin stress testing
* Exposure caps by symbol or sector
