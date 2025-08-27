# 2. Hierarchical Communication Architecture - Corrected Specification

## 2.1 Hierarchical Bridge Fallback System

### 2.1.1 Bridge Hierarchy Definition with Precise State Management

**Primary-Secondary-Tertiary Pattern** with explicit state management and coordination `Enhanced Python-Dominant Trading System Technical Monograph - Remediated.md`:

#### Bridge Definitions

**Primary: DLL+Socket Bridge**
- **Technology:** C++ DLL maintaining persistent TCP connections to Python services
- **Target Latency:** <10ms for critical signals (measured: message queued → acknowledgment received)
- **Success Criteria:** Message delivered + acknowledgment received within latency threshold + response validation passed
- **Failure Criteria:** Any of: timeout (>10ms), connection lost, malformed response, acknowledgment missing
- **Circuit Breaker:** 3 consecutive failures → 30-second timeout
- **Recovery Requirement:** 10 consecutive successes within 5-minute window

**Secondary: Named Pipes Bridge**
- **Technology:** Windows named pipes for local inter-process communication
- **Target Latency:** <50ms (measured: pipe write → pipe read confirmation)
- **Success Criteria:** Message written + read confirmation + data integrity validated
- **Failure Criteria:** Any of: timeout (>50ms), pipe broken, access denied, data corruption
- **Circuit Breaker:** 5 consecutive failures → 60-second timeout
- **Recovery Requirement:** 15 consecutive successes within 10-minute window

**Tertiary: Enhanced File-Based Bridge**
- **Technology:** RAM disk utilization, atomic operations, compression, batching
- **Target Latency:** <500ms (measured: file write → file read + processing complete)
- **Success Criteria:** File written atomically + read successfully + checksum validated
- **Failure Criteria:** Any of: timeout (>500ms), file corruption, disk full, access denied
- **Circuit Breaker:** 10 consecutive failures → 120-second timeout
- **Recovery Requirement:** 20 consecutive successes within 15-minute window

### 2.1.2 Complete State Machine Definition

#### Bridge States
```python
enum BridgeState {
    HEALTHY,        # Operational, meeting performance targets
    DEGRADED,       # Operational but performance issues detected
    FAILED,         # Non-operational, circuit breaker triggered
    RECOVERING,     # Attempting recovery, limited testing
    MAINTENANCE     # Administratively disabled
}

enum CircuitBreakerState {
    CLOSED,         # Normal operation
    OPEN,           # Blocking all traffic
    HALF_OPEN       # Testing with limited traffic
}
```

#### State Transition Rules

**HEALTHY → DEGRADED Conditions:**
- Latency exceeds target by >20% for 3 consecutive operations
- Success rate drops below 95% over 10-operation window
- 2 consecutive failures (but less than circuit breaker threshold)

**DEGRADED → FAILED Conditions:**
- Circuit breaker threshold reached (3/5/10 consecutive failures)
- Latency exceeds target by >100% for any single operation
- Critical system error (connection lost, process crashed)

**FAILED → RECOVERING Conditions:**
- Circuit breaker timeout elapsed
- Administrative recovery command issued
- Dependency health restored (if failure due to dependency)

**RECOVERING → HEALTHY Conditions:**
- Required consecutive successes achieved
- Latency within target range for entire success window
- No errors during recovery period

**RECOVERING → FAILED Conditions:**
- Any failure during recovery period
- Recovery timeout exceeded (2x normal circuit breaker timeout)

#### Circuit Breaker Implementation

```python
class BridgeCircuitBreaker:
    def __init__(self, bridge_name: str, failure_threshold: int, timeout_seconds: int):
        self.bridge_name = bridge_name
        self.failure_threshold = failure_threshold
        self.timeout_seconds = timeout_seconds
        self.state = CircuitBreakerState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None
        self.last_test_time = None
        self.test_request_count = 0
        
    def can_execute(self) -> bool:
        """Determine if operation can be executed through this bridge"""
        if self.state == CircuitBreakerState.CLOSED:
            return True
        elif self.state == CircuitBreakerState.OPEN:
            return self._should_attempt_reset()
        elif self.state == CircuitBreakerState.HALF_OPEN:
            return self._can_test()
        return False
    
    def _should_attempt_reset(self) -> bool:
        """Check if circuit breaker should transition to half-open"""
        if self.last_failure_time is None:
            return True
        time_since_failure = (datetime.now() - self.last_failure_time).total_seconds()
        return time_since_failure >= self.timeout_seconds
    
    def _can_test(self) -> bool:
        """Determine if test request can be sent in half-open state"""
        # Limit test frequency to prevent flooding
        if self.last_test_time is None:
            return True
        time_since_test = (datetime.now() - self.last_test_time).total_seconds()
        return time_since_test >= 5  # Minimum 5 seconds between tests
    
    def record_success(self) -> CircuitBreakerState:
        """Record successful operation and update state"""
        if self.state == CircuitBreakerState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self._get_recovery_requirement():
                self.state = CircuitBreakerState.CLOSED
                self.failure_count = 0
                self.success_count = 0
                self.logger.info(f"Circuit breaker closed for {self.bridge_name}")
        elif self.state == CircuitBreakerState.CLOSED:
            self.failure_count = 0  # Reset failure count on success
            
        return self.state
    
    def record_failure(self) -> CircuitBreakerState:
        """Record failed operation and update state"""
        self.failure_count += 1
        self.last_failure_time = datetime.now()
        self.success_count = 0  # Reset success count on failure
        
        if self.state == CircuitBreakerState.CLOSED:
            if self.failure_count >= self.failure_threshold:
                self.state = CircuitBreakerState.OPEN
                self.logger.warning(f"Circuit breaker opened for {self.bridge_name}")
        elif self.state == CircuitBreakerState.HALF_OPEN:
            self.state = CircuitBreakerState.OPEN
            self.logger.warning(f"Circuit breaker reopened for {self.bridge_name} during recovery")
            
        return self.state
    
    def attempt_test(self) -> bool:
        """Attempt test operation in half-open state"""
        if self.state == CircuitBreakerState.OPEN and self._should_attempt_reset():
            self.state = CircuitBreakerState.HALF_OPEN
            self.success_count = 0
            self.test_request_count = 0
            self.logger.info(f"Circuit breaker half-opened for {self.bridge_name}")
            
        if self.state == CircuitBreakerState.HALF_OPEN and self._can_test():
            self.last_test_time = datetime.now()
            self.test_request_count += 1
            return True
            
        return False
```

### 2.1.3 Bridge Health Monitor Implementation with Complete Logic

```python
class BridgeHealthMonitor:
    def __init__(self):
        self.metrics_window = 100  # Last 100 operations
        self.success_threshold = 0.95  # 95% success rate
        self.latency_thresholds = {
            'dll_socket': 10,    # 10ms
            'named_pipes': 50,   # 50ms  
            'file_based': 500    # 500ms
        }
        
        # State tracking with complete transition logic
        self.bridge_states = {
            'dll_socket': BridgeState.HEALTHY,
            'named_pipes': BridgeState.HEALTHY,
            'file_based': BridgeState.HEALTHY
        }
        
        # Circuit breakers with bridge-specific configuration
        self.circuit_breakers = {
            'dll_socket': BridgeCircuitBreaker('dll_socket', 3, 30),
            'named_pipes': BridgeCircuitBreaker('named_pipes', 5, 60),
            'file_based': BridgeCircuitBreaker('file_based', 10, 120)
        }
        
        # Performance tracking
        self.metrics_collector = MetricsCollector(window_size=100)
        self.operation_history = defaultdict(list)  # Track recent operations
        
        # State transition coordination
        self.state_transition_lock = threading.Lock()
        self.pending_transitions = {}
        
    def evaluate_bridge_health(self, bridge_id: str, operation_result: OperationResult) -> BridgeState:
        """Evaluate bridge health based on operation result with complete logic"""
        
        # Record operation in history
        self.operation_history[bridge_id].append(operation_result)
        
        # Maintain sliding window
        if len(self.operation_history[bridge_id]) > self.metrics_window:
            self.operation_history[bridge_id].pop(0)
        
        # Calculate current metrics
        recent_operations = self.operation_history[bridge_id][-10:]  # Last 10 operations
        if not recent_operations:
            return self.bridge_states[bridge_id]
            
        success_rate = sum(1 for op in recent_operations if op.success) / len(recent_operations)
        avg_latency = sum(op.latency_ms for op in recent_operations if op.success) / max(1, sum(1 for op in recent_operations if op.success))
        
        current_state = self.bridge_states[bridge_id]
        target_latency = self.latency_thresholds[bridge_id]
        
        # State transition logic with hysteresis
        if current_state == BridgeState.HEALTHY:
            if success_rate < self.success_threshold or avg_latency > target_latency * 1.2:
                return self._transition_state(bridge_id, BridgeState.DEGRADED, 
                                            f"Performance degraded: success_rate={success_rate:.2%}, latency={avg_latency:.1f}ms")
                                            
        elif current_state == BridgeState.DEGRADED:
            if success_rate >= self.success_threshold and avg_latency <= target_latency:
                return self._transition_state(bridge_id, BridgeState.HEALTHY,
                                            f"Performance recovered: success_rate={success_rate:.2%}, latency={avg_latency:.1f}ms")
            elif self.circuit_breakers[bridge_id].state == CircuitBreakerState.OPEN:
                return self._transition_state(bridge_id, BridgeState.FAILED,
                                            "Circuit breaker opened")
                                            
        elif current_state == BridgeState.FAILED:
            if self.circuit_breakers[bridge_id].state == CircuitBreakerState.HALF_OPEN:
                return self._transition_state(bridge_id, BridgeState.RECOVERING,
                                            "Circuit breaker testing recovery")
            elif self.circuit_breakers[bridge_id].state == CircuitBreakerState.CLOSED:
                return self._transition_state(bridge_id, BridgeState.HEALTHY,
                                            "Circuit breaker closed - full recovery")
                                            
        elif current_state == BridgeState.RECOVERING:
            if self.circuit_breakers[bridge_id].state == CircuitBreakerState.CLOSED:
                return self._transition_state(bridge_id, BridgeState.HEALTHY,
                                            "Recovery completed successfully")
            elif self.circuit_breakers[bridge_id].state == CircuitBreakerState.OPEN:
                return self._transition_state(bridge_id, BridgeState.FAILED,
                                            "Recovery failed - circuit breaker reopened")
        
        return current_state
    
    def _transition_state(self, bridge_id: str, new_state: BridgeState, reason: str) -> BridgeState:
        """Perform atomic state transition with coordination"""
        with self.state_transition_lock:
            old_state = self.bridge_states[bridge_id]
            
            if old_state == new_state:
                return new_state
            
            # Validate transition is allowed
            if not self._is_valid_transition(old_state, new_state):
                self.logger.error(f"Invalid state transition for {bridge_id}: {old_state} → {new_state}")
                return old_state
            
            # Record pending transition
            transition_id = f"{bridge_id}_{int(time.time())}"
            self.pending_transitions[transition_id] = {
                'bridge_id': bridge_id,
                'old_state': old_state,
                'new_state': new_state,
                'reason': reason,
                'timestamp': datetime.now()
            }
            
            # Update state
            self.bridge_states[bridge_id] = new_state
            
            # Log transition
            self.logger.info(f"Bridge {bridge_id} state transition: {old_state} → {new_state} - {reason}")
            
            # Notify coordination layer
            self._notify_state_transition(bridge_id, old_state, new_state, reason)
            
            # Complete transition
            del self.pending_transitions[transition_id]
            
            return new_state
    
    def _is_valid_transition(self, old_state: BridgeState, new_state: BridgeState) -> bool:
        """Validate state transition is allowed"""
        valid_transitions = {
            BridgeState.HEALTHY: [BridgeState.DEGRADED, BridgeState.MAINTENANCE],
            BridgeState.DEGRADED: [BridgeState.HEALTHY, BridgeState.FAILED],
            BridgeState.FAILED: [BridgeState.RECOVERING, BridgeState.MAINTENANCE],
            BridgeState.RECOVERING: [BridgeState.HEALTHY, BridgeState.FAILED],
            BridgeState.MAINTENANCE: [BridgeState.HEALTHY, BridgeState.DEGRADED, BridgeState.FAILED]
        }
        
        return new_state in valid_transitions.get(old_state, [])
```

## 2.2 Event-Driven Message System with Complete Persistence

### 2.2.1 Event-Driven Core with Precise Definitions

**Event Triggers** with exact thresholds and measurement definitions:

#### Market Data Event Definition
```python
class MarketDataEvent:
    def __init__(self, symbol: str, bid: Decimal, ask: Decimal, timestamp: datetime):
        self.symbol = symbol
        self.bid = bid
        self.ask = ask
        self.timestamp = timestamp
        self.spread = ask - bid
        self.mid_price = (bid + ask) / 2
        
    def is_significant_move(self, previous_event: 'MarketDataEvent') -> bool:
        """Determine if price move exceeds significance threshold"""
        if previous_event is None:
            return True
            
        # Calculate pip value based on currency pair
        pip_value = Decimal('0.0001') if 'JPY' not in self.symbol else Decimal('0.01')
        threshold = pip_value * Decimal('0.1')  # 0.1 pip threshold
        
        price_change = abs(self.mid_price - previous_event.mid_price)
        return price_change >= threshold
    
    def calculate_price_change_pips(self, previous_event: 'MarketDataEvent') -> Decimal:
        """Calculate price change in pips"""
        if previous_event is None:
            return Decimal('0')
            
        pip_value = Decimal('0.0001') if 'JPY' not in self.symbol else Decimal('0.01')
        price_change = self.mid_price - previous_event.mid_price
        return price_change / pip_value
```

#### Signal Generation Event Definition
```python
class SignalGenerationEvent:
    def __init__(self, signal: SignalModel, confidence: float, strategy_id: str):
        self.signal = signal
        self.confidence = confidence
        self.strategy_id = strategy_id
        self.timestamp = datetime.now()
        
    def meets_transmission_criteria(self) -> bool:
        """Check if signal meets criteria for transmission"""
        return (
            self.confidence > 0.7 and  # Minimum confidence threshold
            self.signal.is_valid() and  # Signal validation passed
            self.signal.symbol is not None and  # Required fields present
            self.signal.direction in ['BUY', 'SELL']
        )
```

### 2.2.2 Smart Batching Strategy with Complete Logic

```python
class SmartBatcher:
    def __init__(self):
        # Timing configuration with precise definitions
        self.batch_windows = {
            'market_data': 100,      # 100ms collection window
            'signal_transmission': 1000,  # 1 second transmission window
            'analytics': 30000       # 30 second analytics window
        }
        
        # Priority handling
        self.priority_bypass_enabled = True
        self.critical_latency_threshold = 5  # 5ms max delay for critical
        
        # Batch management
        self.batch_queues = {
            'market_data': [],
            'signal_transmission': [],
            'analytics': []
        }
        
        self.last_batch_times = {
            'market_data': datetime.now(),
            'signal_transmission': datetime.now(),
            'analytics': datetime.now()
        }
        
        # Overflow handling
        self.max_batch_sizes = {
            'market_data': 1000,    # Max 1000 data points per batch
            'signal_transmission': 100,  # Max 100 signals per batch
            'analytics': 50         # Max 50 analytics requests per batch
        }
        
        # State management
        self.processing_locks = {
            'market_data': threading.Lock(),
            'signal_transmission': threading.Lock(),
            'analytics': threading.Lock()
        }
        
    def add_to_batch(self, queue_type: str, item: Any, priority: Priority = Priority.NORMAL) -> BatchResult:
        """Add item to batch with complete overflow and priority handling"""
        
        if queue_type not in self.batch_queues:
            raise ValueError(f"Unknown queue type: {queue_type}")
        
        # Priority bypass for critical items
        if priority == Priority.CRITICAL and self.priority_bypass_enabled:
            return self._process_critical_item(queue_type, item)
        
        with self.processing_locks[queue_type]:
            # Check batch overflow
            if len(self.batch_queues[queue_type]) >= self.max_batch_sizes[queue_type]:
                # Force process existing batch
                self._force_process_batch(queue_type)
            
            # Add item with metadata
            batch_item = {
                'item': item,
                'priority': priority,
                'timestamp': datetime.now(),
                'queue_type': queue_type
            }
            
            self.batch_queues[queue_type].append(batch_item)
            
            # Check if batch should be processed
            if self._should_process_batch(queue_type):
                return self._process_batch(queue_type)
            
            return BatchResult(queued=True, batch_size=len(self.batch_queues[queue_type]))
    
    def _should_process_batch(self, queue_type: str) -> bool:
        """Determine if batch should be processed with complete timing logic"""
        current_time = datetime.now()
        last_batch_time = self.last_batch_times[queue_type]
        time_since_batch = (current_time - last_batch_time).total_seconds() * 1000
        
        window_ms = self.batch_windows[queue_type]
        
        return time_since_batch >= window_ms
    
    def _process_critical_item(self, queue_type: str, item: Any) -> BatchResult:
        """Process critical item immediately with latency tracking"""
        start_time = datetime.now()
        
        try:
            # Process immediately
            result = self._process_single_item(item)
            
            end_time = datetime.now()
            latency_ms = (end_time - start_time).total_seconds() * 1000
            
            # Validate critical latency requirement
            if latency_ms > self.critical_latency_threshold:
                self.logger.warning(
                    f"Critical item processing exceeded threshold: {latency_ms:.2f}ms > {self.critical_latency_threshold}ms"
                )
            
            return BatchResult(
                processed=True,
                critical_bypass=True,
                latency_ms=latency_ms,
                batch_size=1
            )
            
        except Exception as e:
            self.logger.error(f"Critical item processing failed: {e}")
            return BatchResult(error=str(e), critical_bypass=True)
    
    def _process_batch(self, queue_type: str) -> BatchResult:
        """Process batch with complete error handling and metrics"""
        if not self.batch_queues[queue_type]:
            return BatchResult(processed=True, batch_size=0)
        
        start_time = datetime.now()
        batch_to_process = self.batch_queues[queue_type].copy()
        self.batch_queues[queue_type].clear()
        self.last_batch_times[queue_type] = start_time
        
        try:
            # Sort by priority and timestamp
            batch_to_process.sort(key=lambda x: (x['priority'].value, x['timestamp']))
            
            # Process items
            results = []
            for batch_item in batch_to_process:
                try:
                    result = self._process_single_item(batch_item['item'])
                    results.append(result)
                except Exception as e:
                    self.logger.error(f"Item processing failed in batch: {e}")
                    results.append({'error': str(e), 'item_id': getattr(batch_item['item'], 'id', 'unknown')})
            
            end_time = datetime.now()
            processing_time_ms = (end_time - start_time).total_seconds() * 1000
            
            return BatchResult(
                processed=True,
                batch_size=len(batch_to_process),
                processing_time_ms=processing_time_ms,
                successful_items=len([r for r in results if 'error' not in r]),
                failed_items=len([r for r in results if 'error' in r]),
                results=results
            )
            
        except Exception as e:
            # Restore batch on processing failure
            self.batch_queues[queue_type].extend(batch_to_process)
            self.logger.error(f"Batch processing failed for {queue_type}: {e}")
            return BatchResult(error=str(e), batch_size=len(batch_to_process))
```

### 2.2.3 Message Persistence and Safety with Complete Guarantees

```python
class MessagePersistenceManager:
    def __init__(self):
        self.redis_client = redis.Redis(url=config.REDIS_URL, decode_responses=True)
        self.dead_letter_queue = DeadLetterQueue()
        self.message_journal = MessageJournal()
        self.delivery_tracker = DeliveryTracker()
        
        # Delivery guarantee configuration
        self.delivery_timeouts = {
            DeliveryGuarantee.EXACTLY_ONCE: 60,      # 60 seconds
            DeliveryGuarantee.AT_LEAST_ONCE: 30,     # 30 seconds
            DeliveryGuarantee.BEST_EFFORT: 10        # 10 seconds
        }
        
        self.retry_policies = {
            DeliveryGuarantee.EXACTLY_ONCE: ExponentialBackoff(initial=1, max_delay=30, max_retries=5),
            DeliveryGuarantee.AT_LEAST_ONCE: ExponentialBackoff(initial=1, max_delay=15, max_retries=3),
            DeliveryGuarantee.BEST_EFFORT: ExponentialBackoff(initial=1, max_delay=5, max_retries=1)
        }
        
    async def persist_message(self, message: Message, delivery_guarantee: DeliveryGuarantee) -> PersistenceResult:
        """Persist message with complete delivery guarantee implementation"""
        
        # Validate message
        validation_result = self._validate_message(message)
        if not validation_result.is_valid:
            return PersistenceResult(
                success=False,
                error=f"Message validation failed: {validation_result.errors}",
                message_id=message.id
            )
        
        # Create journal entry
        journal_entry = self.message_journal.create_entry(
            message_id=message.id,
            message_type=message.type,
            content_hash=hashlib.sha256(message.content.encode()).hexdigest(),
            timestamp=datetime.now(),
            delivery_guarantee=delivery_guarantee
        )
        
        try:
            # Persistence strategy based on guarantee
            if delivery_guarantee == DeliveryGuarantee.EXACTLY_ONCE:
                result = await self._persist_exactly_once(message)
            elif delivery_guarantee == DeliveryGuarantee.AT_LEAST_ONCE:
                result = await self._persist_at_least_once(message)
            else:
                result = await self._persist_best_effort(message)
            
            # Update journal
            self.message_journal.update_entry(journal_entry.id, 
                                            status='PERSISTED' if result.success else 'FAILED',
                                            details=result.details)
            
            return result
            
        except Exception as e:
            self.message_journal.update_entry(journal_entry.id, 
                                            status='ERROR',
                                            details=str(e))
            return PersistenceResult(
                success=False,
                error=str(e),
                message_id=message.id
            )
    
    async def _persist_exactly_once(self, message: Message) -> PersistenceResult:
        """Implement exactly-once delivery with complete deduplication"""
        
        # Generate idempotency key
        idempotency_key = f"msg:{message.id}:{hashlib.sha256(message.content.encode()).hexdigest()}"
        
        # Check for existing message
        existing_result = await self.redis_client.get(f"result:{idempotency_key}")
        if existing_result:
            # Message already processed
            result_data = json.loads(existing_result)
            return PersistenceResult(
                success=True,
                message_id=message.id,
                duplicate_detected=True,
                original_timestamp=result_data['timestamp']
            )
        
        # Atomic persistence with deduplication
        pipeline = self.redis_client.pipeline()
        
        # Set message with expiration
        pipeline.setex(f"msg:{message.id}", 
                      self.delivery_timeouts[DeliveryGuarantee.EXACTLY_ONCE], 
                      message.content)
        
        # Set idempotency tracking
        pipeline.setex(f"key:{idempotency_key}", 
                      self.delivery_timeouts[DeliveryGuarantee.EXACTLY_ONCE],
                      json.dumps({
                          'message_id': message.id,
                          'timestamp': datetime.now().isoformat(),
                          'status': 'PERSISTED'
                      }))
        
        # Set result tracking  
        pipeline.setex(f"result:{idempotency_key}",
                      self.delivery_timeouts[DeliveryGuarantee.EXACTLY_ONCE],
                      json.dumps({
                          'message_id': message.id,
                          'timestamp': datetime.now().isoformat(),
                          'guarantee': 'EXACTLY_ONCE'
                      }))
        
        await pipeline.execute()
        
        return PersistenceResult(
            success=True,
            message_id=message.id,
            persistence_method='exactly_once',
            expiration_time=datetime.now() + timedelta(seconds=self.delivery_timeouts[DeliveryGuarantee.EXACTLY_ONCE])
        )
    
    async def handle_failed_delivery(self, message: Message, error: Exception, delivery_guarantee: DeliveryGuarantee) -> RetryResult:
        """Handle failed message delivery with complete retry logic"""
        
        retry_policy = self.retry_policies[delivery_guarantee]
        retry_count = self.delivery_tracker.get_retry_count(message.id)
        
        # Check if retries exhausted
        if retry_count >= retry_policy.max_retries:
            # Move to dead letter queue
            dlq_result = await self.dead_letter_queue.add_message(
                message=message,
                error=str(error),
                retry_count=retry_count,
                final_attempt_time=datetime.now(),
                delivery_guarantee=delivery_guarantee
            )
            
            return RetryResult(
                should_retry=False,
                moved_to_dlq=True,
                dlq_id=dlq_result.id,
                reason=f"Max retries exceeded: {retry_count}/{retry_policy.max_retries}"
            )
        
        # Calculate retry delay
        retry_delay = retry_policy.calculate_delay(retry_count)
        
        # Check if error is retryable
        if not self._is_retryable_error(error):
            # Move to dead letter queue immediately
            dlq_result = await self.dead_letter_queue.add_message(
                message=message,
                error=str(error),
                retry_count=retry_count,
                final_attempt_time=datetime.now(),
                delivery_guarantee=delivery_guarantee,
                reason="Non-retryable error"
            )
            
            return RetryResult(
                should_retry=False,
                moved_to_dlq=True,
                dlq_id=dlq_result.id,
                reason=f"Non-retryable error: {error}"
            )
        
        # Schedule retry
        retry_time = datetime.now() + timedelta(seconds=retry_delay)
        
        self.delivery_tracker.schedule_retry(
            message_id=message.id,
            retry_at=retry_time,
            retry_count=retry_count + 1,
            previous_error=str(error)
        )
        
        return RetryResult(
            should_retry=True,
            retry_at=retry_time,
            retry_count=retry_count + 1,
            retry_delay=retry_delay
        )
    
    def _is_retryable_error(self, error: Exception) -> bool:
        """Determine if error is retryable with specific classification"""
        
        # Non-retryable error patterns
        non_retryable_patterns = [
            "invalid.*message.*format",
            "authentication.*failed",
            "permission.*denied",
            "message.*too.*large",
            "invalid.*destination",
            "message.*expired"
        ]
        
        error_message = str(error).lower()
        
        for pattern in non_retryable_patterns:
            if re.search(pattern, error_message):
                return False
        
        # Retryable error patterns
        retryable_patterns = [
            "connection.*timeout",
            "network.*error",
            "service.*unavailable",
            "temporary.*failure",
            "rate.*limit.*exceeded",
            "resource.*temporarily.*unavailable"
        ]
        
        for pattern in retryable_patterns:
            if re.search(pattern, error_message):
                return True
        
        # Default to retryable for unknown errors
        return True
```

## 2.3 UUID-Based Lifecycle Management with Complete Tracking

### 2.3.1 UUID Generation and Validation Strategy

```python
class SignalLifecycleManager:
    def __init__(self):
        self.db = SQLiteDB('signal_lifecycle.db')
        self.reconciliation_interval = 3600  # 1 hour
        self.uuid_validator = UUIDValidator()
        self.state_transition_rules = StateTransitionRules()
        
        # Lifecycle state definitions
        self.valid_states = [
            'GENERATED',      # Signal created
            'VALIDATED',      # Signal passed validation
            'TRANSMITTED',    # Signal sent to bridge
            'ACKNOWLEDGED',   # Bridge confirmed receipt
            'EXECUTED',       # Trade order placed
            'FILLED',         # Order execution confirmed
            'MONITORED',      # Position being tracked
            'CLOSED',         # Position closed
            'ANALYZED',       # Post-trade analysis complete
            'ORPHANED'        # Lost tracking/incomplete
        ]
        
        # State transition matrix
        self.allowed_transitions = {
            'GENERATED': ['VALIDATED', 'ORPHANED'],
            'VALIDATED': ['TRANSMITTED', 'ORPHANED'],
            'TRANSMITTED': ['ACKNOWLEDGED', 'ORPHANED'],
            'ACKNOWLEDGED': ['EXECUTED', 'ORPHANED'],
            'EXECUTED': ['FILLED', 'ORPHANED'],
            'FILLED': ['MONITORED', 'ORPHANED'],
            'MONITORED': ['CLOSED', 'ORPHANED'],
            'CLOSED': ['ANALYZED'],
            'ANALYZED': [],  # Terminal state
            'ORPHANED': []   # Terminal state
        }
        
    def create_signal(self, symbol: str, direction: str, confidence: float, strategy_id: str) -> SignalModel:
        """Create signal with UUID and complete lifecycle initialization"""
        
        # Generate UUID with validation
        signal_uuid = self.uuid_validator.generate_uuid()
        
        # Validate input parameters
        if not self._validate_signal_parameters(symbol, direction, confidence, strategy_id):
            raise ValueError("Invalid signal parameters")
        
        # Create signal model
        signal = SignalModel(
            id=signal_uuid,
            symbol=symbol,
            direction=direction,
            confidence=confidence,
            strategy_id=strategy_id,
            state='GENERATED',
            created_at=datetime.now(),
            metadata={
                'creation_source': 'signal_service',
                'validation_pending': True,
                'lifecycle_version': '1.0'
            }
        )
        
        # Initialize lifecycle record with complete tracking
        lifecycle_record = SignalLifecycleRecord(
            signal_uuid=signal_uuid,
            current_state='GENERATED',
            state_history=[{
                'state': 'GENERATED',
                'timestamp': datetime.now().isoformat(),
                'details': 'Signal created',
                'source': 'signal_service'
            }],
            correlation_data={},
            performance_metrics={},
            error_log=[]
        )
        
        # Atomic persistence
        with self.db.transaction():
            self.db.store_signal_record(signal, lifecycle_record)
            
        self.logger.info(f"Signal created with lifecycle tracking: {signal_uuid}")
        return signal
    
    def update_lifecycle_state(self, signal_uuid: str, new_state: str, 
                              metadata: Dict[str, Any] = None,
                              correlation_id: str = None) -> StateTransitionResult:
        """Update signal lifecycle state with complete validation and tracking"""
        
        # Validate UUID format
        if not self.uuid_validator.is_valid_uuid(signal_uuid):
            return StateTransitionResult(
                success=False,
                error="Invalid UUID format",
                signal_uuid=signal_uuid
            )
        
        # Validate new state
        if new_state not in self.valid_states:
            return StateTransitionResult(
                success=False,
                error=f"Invalid state: {new_state}",
                signal_uuid=signal_uuid
            )
        
        with self.db.transaction():
            # Get current record
            current_record = self.db.get_signal_lifecycle_record(signal_uuid)
            if not current_record:
                return StateTransitionResult(
                    success=False,
                    error="Signal record not found",
                    signal_uuid=signal_uuid
                )
            
            # Validate state transition
            if not self._is_valid_state_transition(current_record.current_state, new_state):
                return StateTransitionResult(
                    success=False,
                    error=f"Invalid transition: {current_record.current_state} → {new_state}",
                    signal_uuid=signal_uuid,
                    current_state=current_record.current_state
                )
            
            # Create state history entry
            state_entry = {
                'state': new_state,
                'timestamp': datetime.now().isoformat(),
                'previous_state': current_record.current_state,
                'details': metadata.get('details', f'State updated to {new_state}') if metadata else f'State updated to {new_state}',
                'source': metadata.get('source', 'system') if metadata else 'system',
                'correlation_id': correlation_id
            }
            
            # Update record
            current_record.current_state = new_state
            current_record.state_history.append(state_entry)
            current_record.last_updated = datetime.now()
            
            # Update correlation data if provided
            if correlation_id:
                current_record.correlation_data[new_state] = correlation_id
            
            # Store updated record
            self.db.update_signal_lifecycle_record(current_record)
            
            # Trigger cross-system synchronization for critical states
            if new_state in ['EXECUTED', 'FILLED', 'CLOSED']:
                self._trigger_cross_system_sync(signal_uuid, new_state, correlation_id)
            
            return StateTransitionResult(
                success=True,
                signal_uuid=signal_uuid,
                old_state=state_entry['previous_state'],
                new_state=new_state,
                transition_timestamp=datetime.now(),
                correlation_id=correlation_id
            )
    
    def _is_valid_state_transition(self, current_state: str, new_state: str) -> bool:
        """Validate state transition against rules matrix"""
        return new_state in self.allowed_transitions.get(current_state, [])
    
    def _trigger_cross_system_sync(self, signal_uuid: str, state: str, correlation_id: str):
        """Trigger synchronization across systems for critical state changes"""
        
        sync_targets = []
        
        if state == 'EXECUTED':
            sync_targets = ['mt4_interface', 'risk_manager']
        elif state == 'FILLED':
            sync_targets = ['portfolio_manager', 'analytics_service']
        elif state == 'CLOSED':
            sync_targets = ['performance_tracker', 'reporting_service']
        
        for target in sync_targets:
            try:
                self._send_sync_notification(target, signal_uuid, state, correlation_id)
            except Exception as e:
                self.logger.error(f"Failed to sync with {target} for signal {signal_uuid}: {e}")
    
    async def perform_lifecycle_reconciliation(self) -> ReconciliationResult:
        """Perform comprehensive lifecycle reconciliation with complete orphan handling"""
        
        reconciliation_start = datetime.now()
        
        # Find potentially orphaned signals
        orphan_candidates = self.db.find_stale_signals(
            max_age_hours=24,
            exclude_states=['ANALYZED', 'ORPHANED']
        )
        
        orphaned_count = 0
        recovered_count = 0
        error_count = 0
        
        for signal_uuid in orphan_candidates:
            try:
                # Attempt cross-system correlation
                correlation_result = await self._attempt_signal_correlation(signal_uuid)
                
                if correlation_result.found_correlation:
                    # Update state based on correlation
                    self.update_lifecycle_state(
                        signal_uuid,
                        correlation_result.inferred_state,
                        metadata={
                            'details': 'State recovered through reconciliation',
                            'source': 'reconciliation_service',
                            'correlation_method': correlation_result.method
                        },
                        correlation_id=correlation_result.correlation_id
                    )
                    recovered_count += 1
                else:
                    # Mark as orphaned
                    self.update_lifecycle_state(
                        signal_uuid,
                        'ORPHANED',
                        metadata={
                            'details': 'No correlation found during reconciliation',
                            'source': 'reconciliation_service',
                            'orphaned_at': datetime.now().isoformat()
                        }
                    )
                    orphaned_count += 1
                    
            except Exception as e:
                self.logger.error(f"Reconciliation error for signal {signal_uuid}: {e}")
                error_count += 1
        
        reconciliation_end = datetime.now()
        
        return ReconciliationResult(
            processed_signals=len(orphan_candidates),
            orphaned_signals=orphaned_count,
            recovered_signals=recovered_count,
            error_count=error_count,
            duration_seconds=(reconciliation_end - reconciliation_start).total_seconds(),
            timestamp=reconciliation_end
        )
```

## 2.4 Configuration Management with Complete Conflict Resolution

### 2.4.1 5-Tier Configuration Hierarchy with Precise Resolution

```python
class ConfigurationManager:
    def __init__(self):
        # Tier definitions with TTL and precedence
        self.configuration_tiers = [
            ConfigurationTier(
                name="excel_overrides",
                precedence=1,  # Highest precedence
                ttl_hours=24,
                description="Emergency manual overrides via Excel interface"
            ),
            ConfigurationTier(
                name="runtime_updates", 
                precedence=2,
                ttl_hours=1,
                description="Temporary runtime API updates"
            ),
            ConfigurationTier(
                name="environment_variables",
                precedence=3,
                ttl_hours=None,  # No expiration
                description="Deployment environment overrides"
            ),
            ConfigurationTier(
                name="configuration_files",
                precedence=4, 
                ttl_hours=None,
                description="Environment-specific configuration files"
            ),
            ConfigurationTier(
                name="system_defaults",
                precedence=5,  # Lowest precedence
                ttl_hours=None,
                description="Hardcoded system defaults"
            )
        ]
        
        # Configuration storage per tier
        self.tier_configurations = {}
        for tier in self.configuration_tiers:
            self.tier_configurations[tier.name] = ConfigurationStore(tier)
        
        # Conflict resolution
        self.conflict_resolver = ConfigurationConflictResolver()
        self.resolved_configuration = {}
        self.resolution_metadata = {}
        
    def resolve_configuration(self, key: str) -> ConfigurationValue:
        """Resolve configuration using complete hierarchical precedence with conflict tracking"""
        
        resolution_start = datetime.now()
        
        # Collect values from all tiers
        tier_values = {}
        conflicts = []
        
        for tier in self.configuration_tiers:
            store = self.tier_configurations[tier.name]
            
            # Check TTL expiration
            if tier.ttl_hours is not None:
                if store.is_expired(key, tier.ttl_hours):
                    store.remove_expired_value(key)
                    continue
            
            # Get value if exists
            value = store.get_value(key)
            if value is not None:
                tier_values[tier.name] = ConfigurationTierValue(
                    value=value,
                    tier=tier,
                    timestamp=store.get_timestamp(key),
                    source=store.get_source(key)
                )
        
        # No values found
        if not tier_values:
            raise ConfigurationKeyNotFoundError(f"Configuration key not found: {key}")
        
        # Single value - no conflict
        if len(tier_values) == 1:
            tier_name, tier_value = next(iter(tier_values.items()))
            return ConfigurationValue(
                key=key,
                value=tier_value.value,
                source_tier=tier_name,
                precedence=tier_value.tier.precedence,
                resolution_method='single_source',
                conflicts=[]
            )
        
        # Multiple values - resolve conflicts
        winning_tier = min(tier_values.keys(), key=lambda t: tier_values[t].tier.precedence)
        winning_value = tier_values[winning_tier]
        
        # Record conflicts
        for tier_name, tier_value in tier_values.items():
            if tier_name != winning_tier:
                conflicts.append(ConfigurationConflict(
                    key=key,
                    losing_tier=tier_name,
                    losing_value=tier_value.value,
                    losing_precedence=tier_value.tier.precedence,
                    winning_tier=winning_tier,
                    winning_value=winning_value.value,
                    winning_precedence=winning_value.tier.precedence
                ))
        
        # Apply conflict resolution validation
        validation_result = self.conflict_resolver.validate_resolution(
            key, winning_value.value, conflicts
        )
        
        if not validation_result.is_valid:
            raise ConfigurationConflictError(
                f"Configuration conflict validation failed for {key}: {validation_result.errors}"
            )
        
        # Store resolution metadata
        resolution_metadata = ConfigurationResolutionMetadata(
            key=key,
            resolution_timestamp=datetime.now(),
            resolution_duration_ms=(datetime.now() - resolution_start).total_seconds() * 1000,
            conflicts_detected=len(conflicts),
            resolution_method='hierarchical_precedence',
            validation_passed=True
        )
        
        self.resolution_metadata[key] = resolution_metadata
        
        return ConfigurationValue(
            key=key,
            value=winning_value.value,
            source_tier=winning_tier,
            precedence=winning_value.tier.precedence,
            resolution_method='hierarchical_precedence',
            conflicts=conflicts,
            metadata=resolution_metadata
        )
    
    def hot_reload_configuration(self, tier_name: str, updates: Dict[str, Any]) -> HotReloadResult:
        """Perform hot reload with atomic updates and rollback capability"""
        
        if tier_name not in self.tier_configurations:
            return HotReloadResult(
                success=False,
                error=f"Unknown configuration tier: {tier_name}"
            )
        
        store = self.tier_configurations[tier_name]
        
        # Create backup for rollback
        backup = store.create_backup()
        rollback_id = f"backup_{int(time.time())}"
        
        try:
            # Validate all updates first
            validation_errors = []
            for key, value in updates.items():
                validation_result = self.conflict_resolver.validate_configuration_value(key, value)
                if not validation_result.is_valid:
                    validation_errors.extend(validation_result.errors)
            
            if validation_errors:
                return HotReloadResult(
                    success=False,
                    error="Validation failed",
                    validation_errors=validation_errors
                )
            
            # Apply updates atomically
            store.begin_transaction()
            
            updated_keys = []
            for key, value in updates.items():
                store.set_value(key, value, source=f"{tier_name}_hot_reload")
                updated_keys.append(key)
            
            store.commit_transaction()
            
            # Test configuration after update
            test_result = self._test_updated_configuration(updated_keys)
            
            if not test_result.success:
                # Rollback on test failure
                store.restore_backup(backup)
                return HotReloadResult(
                    success=False,
                    error="Configuration test failed after update",
                    test_errors=test_result.errors,
                    rollback_performed=True
                )
            
            # Clear affected resolved values
            for key in updated_keys:
                self.resolved_configuration.pop(key, None)
                self.resolution_metadata.pop(key, None)
            
            return HotReloadResult(
                success=True,
                updated_keys=updated_keys,
                tier_name=tier_name,
                backup_id=rollback_id,
                test_result=test_result
            )
            
        except Exception as e:
            # Rollback on exception
            store.restore_backup(backup)
            return HotReloadResult(
                success=False,
                error=str(e),
                rollback_performed=True
            )
    
    def _test_updated_configuration(self, updated_keys: List[str]) -> ConfigurationTestResult:
        """Test updated configuration for consistency and validity"""
        
        test_errors = []
        
        for key in updated_keys:
            try:
                # Attempt to resolve configuration
                resolved_value = self.resolve_configuration(key)
                
                # Test dependent configurations
                dependent_keys = self.conflict_resolver.get_dependent_keys(key)
                for dep_key in dependent_keys:
                    try:
                        self.resolve_configuration(dep_key)
                    except Exception as e:
                        test_errors.append(f"Dependent configuration {dep_key} failed: {e}")
                
            except Exception as e:
                test_errors.append(f"Configuration resolution failed for {key}: {e}")
        
        return ConfigurationTestResult(
            success=len(test_errors) == 0,
            errors=test_errors,
            tested_keys=updated_keys
        )
```
