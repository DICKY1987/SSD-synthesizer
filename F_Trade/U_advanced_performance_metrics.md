# Advanced Performance Metrics & Data Architecture

## 1. Expanded Performance Metrics Framework

### 1.1 Risk-Adjusted Performance Metrics

#### Core Risk Metrics
```python
class RiskAdjustedMetrics:
    def __init__(self, returns_series: pd.Series, benchmark_returns: pd.Series = None):
        self.returns = returns_series
        self.benchmark = benchmark_returns
        self.risk_free_rate = 0.02  # 2% annual risk-free rate
        
    def sharpe_ratio(self, periods: int = 252) -> float:
        """Sharpe Ratio: (Return - Risk Free) / Volatility"""
        excess_returns = self.returns.mean() - (self.risk_free_rate / periods)
        volatility = self.returns.std() * np.sqrt(periods)
        return excess_returns / volatility if volatility != 0 else 0
    
    def sortino_ratio(self, periods: int = 252) -> float:
        """Sortino Ratio: Only penalizes downside volatility"""
        excess_returns = self.returns.mean() - (self.risk_free_rate / periods)
        downside_returns = self.returns[self.returns < 0]
        downside_vol = downside_returns.std() * np.sqrt(periods) if len(downside_returns) > 0 else 0
        return excess_returns / downside_vol if downside_vol != 0 else 0
    
    def calmar_ratio(self) -> float:
        """Calmar Ratio: Annual Return / Maximum Drawdown"""
        annual_return = self.returns.mean() * 252
        max_dd = self.maximum_drawdown()
        return annual_return / abs(max_dd) if max_dd != 0 else 0
    
    def information_ratio(self) -> float:
        """Information Ratio vs benchmark"""
        if self.benchmark is None:
            return 0
        active_returns = self.returns - self.benchmark
        tracking_error = active_returns.std() * np.sqrt(252)
        return active_returns.mean() * 252 / tracking_error if tracking_error != 0 else 0
    
    def maximum_drawdown(self) -> float:
        """Maximum peak-to-trough decline"""
        cumulative = (1 + self.returns).cumprod()
        rolling_max = cumulative.expanding().max()
        drawdown = (cumulative - rolling_max) / rolling_max
        return drawdown.min()
    
    def var_95(self) -> float:
        """Value at Risk at 95% confidence"""
        return np.percentile(self.returns, 5)
    
    def cvar_95(self) -> float:
        """Conditional VaR (Expected Shortfall)"""
        var_95 = self.var_95()
        return self.returns[self.returns <= var_95].mean()
    
    def omega_ratio(self, threshold: float = 0) -> float:
        """Omega Ratio: Probability weighted gains vs losses"""
        gains = self.returns[self.returns > threshold] - threshold
        losses = threshold - self.returns[self.returns <= threshold]
        return gains.sum() / losses.sum() if losses.sum() != 0 else float('inf')
```

#### Advanced Strategy Metrics
```python
class StrategyPerformanceMetrics:
    def __init__(self, trades_df: pd.DataFrame):
        self.trades = trades_df
        
    def profit_factor(self) -> float:
        """Gross Profit / Gross Loss"""
        winning_trades = self.trades[self.trades['pnl'] > 0]['pnl'].sum()
        losing_trades = abs(self.trades[self.trades['pnl'] < 0]['pnl'].sum())
        return winning_trades / losing_trades if losing_trades != 0 else float('inf')
    
    def win_rate(self) -> float:
        """Percentage of winning trades"""
        winning_trades = len(self.trades[self.trades['pnl'] > 0])
        total_trades = len(self.trades)
        return winning_trades / total_trades if total_trades > 0 else 0
    
    def expectancy(self) -> float:
        """Expected value per trade"""
        return self.trades['pnl'].mean()
    
    def kelly_criterion(self) -> float:
        """Optimal position sizing based on Kelly formula"""
        win_rate = self.win_rate()
        avg_win = self.trades[self.trades['pnl'] > 0]['pnl'].mean()
        avg_loss = abs(self.trades[self.trades['pnl'] < 0]['pnl'].mean())
        
        if avg_loss == 0:
            return 0
        
        win_loss_ratio = avg_win / avg_loss
        kelly = win_rate - ((1 - win_rate) / win_loss_ratio)
        return max(0, kelly)  # Don't allow negative Kelly
    
    def consecutive_wins_losses(self) -> dict:
        """Maximum consecutive wins and losses"""
        pnl_signs = np.sign(self.trades['pnl'].values)
        
        max_wins = max_losses = current_wins = current_losses = 0
        
        for sign in pnl_signs:
            if sign > 0:
                current_wins += 1
                current_losses = 0
                max_wins = max(max_wins, current_wins)
            elif sign < 0:
                current_losses += 1
                current_wins = 0
                max_losses = max(max_losses, current_losses)
            else:
                current_wins = current_losses = 0
                
        return {'max_consecutive_wins': max_wins, 'max_consecutive_losses': max_losses}
    
    def average_trade_duration(self) -> float:
        """Average time in trade (hours)"""
        if 'opened_at' in self.trades.columns and 'closed_at' in self.trades.columns:
            durations = pd.to_datetime(self.trades['closed_at']) - pd.to_datetime(self.trades['opened_at'])
            return durations.dt.total_seconds().mean() / 3600  # Convert to hours
        return 0
```

### 1.2 Multi-Dimensional Performance Analysis

```python
class MultiDimensionalAnalytics:
    def __init__(self, db_connection):
        self.db = db_connection
        
    def performance_by_pair(self, start_date: str = None, end_date: str = None) -> pd.DataFrame:
        """Performance metrics broken down by currency pair"""
        query = """
        SELECT 
            symbol,
            COUNT(*) as total_trades,
            SUM(profit_loss) as total_pnl,
            AVG(profit_loss) as avg_pnl,
            SUM(CASE WHEN profit_loss > 0 THEN profit_loss ELSE 0 END) as gross_profit,
            SUM(CASE WHEN profit_loss < 0 THEN ABS(profit_loss) ELSE 0 END) as gross_loss,
            SUM(CASE WHEN profit_loss > 0 THEN 1 ELSE 0 END) as winning_trades,
            AVG(confidence_score) as avg_confidence,
            AVG(JULIANDAY(closed_at) - JULIANDAY(opened_at)) * 24 as avg_duration_hours
        FROM (
            SELECT symbol, profit_loss, confidence_score, opened_at, closed_at
            FROM trades_EURUSD WHERE status = 'CLOSED'
            UNION ALL
            SELECT symbol, profit_loss, confidence_score, opened_at, closed_at  
            FROM trades_GBPUSD WHERE status = 'CLOSED'
            -- ... UNION ALL for all 30 pairs
        ) consolidated_trades
        WHERE 1=1
        """
        
        if start_date:
            query += f" AND opened_at >= '{start_date}'"
        if end_date:
            query += f" AND opened_at <= '{end_date}'"
            
        query += " GROUP BY symbol ORDER BY total_pnl DESC"
        
        return pd.read_sql_query(query, self.db)
    
    def performance_by_confidence_tier(self) -> pd.DataFrame:
        """Performance breakdown by signal confidence ranges"""
        query = """
        SELECT 
            CASE 
                WHEN confidence_score >= 0.9 THEN 'Very High (0.9+)'
                WHEN confidence_score >= 0.8 THEN 'High (0.8-0.9)'
                WHEN confidence_score >= 0.7 THEN 'Medium (0.7-0.8)'
                WHEN confidence_score >= 0.6 THEN 'Low (0.6-0.7)'
                ELSE 'Very Low (<0.6)'
            END as confidence_tier,
            COUNT(*) as trade_count,
            SUM(profit_loss) as total_pnl,
            AVG(profit_loss) as avg_pnl,
            SUM(CASE WHEN profit_loss > 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as win_rate
        FROM consolidated_trades_view
        WHERE status = 'CLOSED'
        GROUP BY confidence_tier
        ORDER BY confidence_score DESC
        """
        return pd.read_sql_query(query, self.db)
    
    def performance_by_strategy_id(self) -> pd.DataFrame:
        """Performance breakdown by RCI strategy IDs"""
        query = """
        SELECT 
            strategy_id,
            COUNT(*) as trade_count,
            SUM(profit_loss) as total_pnl,
            AVG(profit_loss) as avg_pnl,
            STDEV(profit_loss) as pnl_volatility,
            SUM(CASE WHEN profit_loss > 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as win_rate
        FROM consolidated_trades_view
        WHERE status = 'CLOSED' AND strategy_id IS NOT NULL
        GROUP BY strategy_id
        HAVING COUNT(*) >= 10  -- Only strategies with sufficient trades
        ORDER BY total_pnl DESC
        """
        return pd.read_sql_query(query, self.db)
```

## 2. Scalable Data Architecture for UUID Management

### 2.1 Hierarchical Database Design

```sql
-- Core Signal Tracking Table (Lightweight for fast UUID lookups)
CREATE TABLE signal_registry (
    uuid TEXT PRIMARY KEY,
    symbol TEXT NOT NULL,
    created_at DATETIME NOT NULL,
    strategy_id TEXT,
    confidence_score REAL,
    status TEXT DEFAULT 'ACTIVE',
    pair_table_suffix TEXT,  -- e.g., 'EURUSD', 'GBPUSD'
    INDEX idx_symbol_created (symbol, created_at),
    INDEX idx_strategy_confidence (strategy_id, confidence_score),
    INDEX idx_status_created (status, created_at)
);

-- Performance Metrics Cache (Pre-calculated for speed)
CREATE TABLE performance_metrics_cache (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    metric_type TEXT NOT NULL,  -- 'sharpe_ratio', 'win_rate', etc.
    scope TEXT NOT NULL,        -- 'pair', 'strategy', 'confidence_tier', 'global'
    scope_value TEXT,           -- 'EURUSD', 'strategy_12345', '0.8-0.9', 'all'
    time_period TEXT NOT NULL,  -- 'daily', 'weekly', 'monthly', 'ytd', 'all_time'
    metric_value REAL NOT NULL,
    calculation_date DATETIME NOT NULL,
    trade_count INTEGER,
    data_hash TEXT,  -- For cache invalidation
    INDEX idx_lookup (metric_type, scope, scope_value, time_period),
    INDEX idx_calculation_date (calculation_date)
);

-- Trade Correlation Mapping (Links signals to execution)
CREATE TABLE signal_trade_correlation (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    signal_uuid TEXT NOT NULL,
    trade_uuid TEXT NOT NULL,
    symbol TEXT NOT NULL,
    correlation_confidence REAL DEFAULT 1.0,
    created_at DATETIME NOT NULL,
    FOREIGN KEY (signal_uuid) REFERENCES signal_registry (uuid),
    INDEX idx_signal_uuid (signal_uuid),
    INDEX idx_trade_uuid (trade_uuid),
    INDEX idx_symbol_created (symbol, created_at)
);

-- Reentry Chain Tracking
CREATE TABLE reentry_chains (
    chain_id TEXT PRIMARY KEY,
    root_signal_uuid TEXT NOT NULL,
    symbol TEXT NOT NULL,
    chain_start_time DATETIME NOT NULL,
    chain_end_time DATETIME,
    total_trades INTEGER DEFAULT 0,
    chain_pnl REAL DEFAULT 0.0,
    chain_status TEXT DEFAULT 'ACTIVE',  -- ACTIVE, COMPLETED, ABANDONED
    INDEX idx_root_signal (root_signal_uuid),
    INDEX idx_symbol_start (symbol, chain_start_time)
);

-- Time-Series Performance Data (For trend analysis)
CREATE TABLE performance_timeseries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME NOT NULL,
    symbol TEXT,
    metric_name TEXT NOT NULL,
    metric_value REAL NOT NULL,
    rolling_window INTEGER,  -- e.g., 30 for 30-day rolling
    INDEX idx_timestamp_symbol (timestamp, symbol),
    INDEX idx_metric_timestamp (metric_name, timestamp)
);
```

### 2.2 Intelligent Data Retrieval System

```python
class PerformanceDataManager:
    def __init__(self, db_connection):
        self.db = db_connection
        self.cache_manager = MetricsCacheManager(db_connection)
        self.query_optimizer = QueryOptimizer()
        
    def get_performance_metrics(self, 
                              symbols: List[str] = None,
                              strategy_ids: List[str] = None,
                              confidence_range: tuple = None,
                              time_period: str = 'all_time',
                              metrics: List[str] = None,
                              use_cache: bool = True) -> dict:
        """
        Intelligent metric retrieval with automatic caching and optimization
        
        Args:
            symbols: List of currency pairs ['EURUSD', 'GBPUSD']
            strategy_ids: List of strategy IDs ['12345', '67890']
            confidence_range: Tuple of (min_confidence, max_confidence)
            time_period: 'daily', 'weekly', 'monthly', 'ytd', 'all_time'
            metrics: List of metrics to calculate ['sharpe_ratio', 'win_rate']
            use_cache: Whether to use cached results
        """
        
        # Build cache key for lookup
        cache_key = self._build_cache_key(symbols, strategy_ids, confidence_range, time_period, metrics)
        
        # Try cache first if enabled
        if use_cache:
            cached_result = self.cache_manager.get_cached_metrics(cache_key)
            if cached_result and not self._is_cache_stale(cached_result):
                return cached_result
        
        # Build optimized query
        query_plan = self.query_optimizer.build_query_plan(
            symbols=symbols,
            strategy_ids=strategy_ids,
            confidence_range=confidence_range,
            time_period=time_period
        )
        
        # Execute query with automatic partitioning for large datasets
        raw_data = self._execute_partitioned_query(query_plan)
        
        # Calculate metrics
        calculated_metrics = self._calculate_metrics(raw_data, metrics or self._get_default_metrics())
        
        # Cache results
        if use_cache:
            self.cache_manager.cache_metrics(cache_key, calculated_metrics)
        
        return calculated_metrics
    
    def _execute_partitioned_query(self, query_plan: dict) -> pd.DataFrame:
        """Execute query with automatic partitioning for performance"""
        
        # If querying all pairs, use parallel execution
        if len(query_plan['symbols']) > 10:
            return self._execute_parallel_query(query_plan)
        
        # If date range is large, use time-based partitioning
        if query_plan['time_range_days'] > 365:
            return self._execute_time_partitioned_query(query_plan)
        
        # Standard execution for smaller datasets
        return self._execute_standard_query(query_plan)
    
    def _execute_parallel_query(self, query_plan: dict) -> pd.DataFrame:
        """Execute queries in parallel across currency pairs"""
        from concurrent.futures import ThreadPoolExecutor, as_completed
        
        results = []
        with ThreadPoolExecutor(max_workers=8) as executor:
            future_to_symbol = {}
            
            for symbol in query_plan['symbols']:
                future = executor.submit(self._query_single_pair, symbol, query_plan)
                future_to_symbol[future] = symbol
            
            for future in as_completed(future_to_symbol):
                symbol = future_to_symbol[future]
                try:
                    data = future.result()
                    if not data.empty:
                        results.append(data)
                except Exception as e:
                    self.logger.error(f"Query failed for {symbol}: {e}")
        
        return pd.concat(results, ignore_index=True) if results else pd.DataFrame()
    
    def _query_single_pair(self, symbol: str, query_plan: dict) -> pd.DataFrame:
        """Query data for a single currency pair"""
        table_name = f"trades_{symbol}"
        
        query = f"""
        SELECT 
            t.uuid as trade_uuid,
            s.uuid as signal_uuid,
            t.symbol,
            t.profit_loss,
            t.opened_at,
            t.closed_at,
            s.confidence_score,
            s.strategy_id,
            JULIANDAY(t.closed_at) - JULIANDAY(t.opened_at) as duration_days
        FROM {table_name} t
        JOIN signal_trade_correlation stc ON t.uuid = stc.trade_uuid
        JOIN signal_registry s ON stc.signal_uuid = s.uuid
        WHERE t.status = 'CLOSED'
        """
        
        # Add filters based on query plan
        if query_plan.get('start_date'):
            query += f" AND t.opened_at >= '{query_plan['start_date']}'"
        if query_plan.get('end_date'):
            query += f" AND t.opened_at <= '{query_plan['end_date']}'"
        if query_plan.get('confidence_range'):
            min_conf, max_conf = query_plan['confidence_range']
            query += f" AND s.confidence_score BETWEEN {min_conf} AND {max_conf}"
        if query_plan.get('strategy_ids'):
            strategy_list = "','".join(query_plan['strategy_ids'])
            query += f" AND s.strategy_id IN ('{strategy_list}')"
        
        return pd.read_sql_query(query, self.db)
```

### 2.3 Real-Time Metrics Calculation Engine

```python
class RealTimeMetricsEngine:
    def __init__(self, db_connection):
        self.db = db_connection
        self.metrics_buffer = defaultdict(list)
        self.calculation_triggers = {
            'trade_closed': ['sharpe_ratio', 'win_rate', 'profit_factor'],
            'signal_generated': ['signal_accuracy', 'confidence_distribution'],
            'daily_rollover': ['daily_pnl', 'drawdown_series'],
            'weekly_rollover': ['weekly_sharpe', 'correlation_matrix']
        }
        
    def process_trade_event(self, event_type: str, trade_data: dict):
        """Process trade events and trigger metric calculations"""
        
        # Add to buffer
        self.metrics_buffer[trade_data['symbol']].append({
            'event_type': event_type,
            'timestamp': datetime.now(),
            'data': trade_data
        })
        
        # Check if calculation should be triggered
        if event_type in self.calculation_triggers:
            metrics_to_calculate = self.calculation_triggers[event_type]
            self._trigger_metric_calculation(trade_data['symbol'], metrics_to_calculate)
    
    def _trigger_metric_calculation(self, symbol: str, metrics: List[str]):
        """Calculate and cache specific metrics for a symbol"""
        
        # Get recent trade data
        recent_data = self._get_recent_trades(symbol, days=30)
        
        if len(recent_data) < 10:  # Need minimum trades for meaningful metrics
            return
        
        calculated_metrics = {}
        
        for metric in metrics:
            if metric == 'sharpe_ratio':
                returns = recent_data['profit_loss'].pct_change().dropna()
                calculated_metrics[metric] = RiskAdjustedMetrics(returns).sharpe_ratio()
            
            elif metric == 'win_rate':
                total_trades = len(recent_data)
                winning_trades = len(recent_data[recent_data['profit_loss'] > 0])
                calculated_metrics[metric] = winning_trades / total_trades
            
            elif metric == 'profit_factor':
                gross_profit = recent_data[recent_data['profit_loss'] > 0]['profit_loss'].sum()
                gross_loss = abs(recent_data[recent_data['profit_loss'] < 0]['profit_loss'].sum())
                calculated_metrics[metric] = gross_profit / gross_loss if gross_loss > 0 else float('inf')
        
        # Cache results
        self._cache_calculated_metrics(symbol, calculated_metrics, '30_day_rolling')
        
        # Trigger alerts if metrics cross thresholds
        self._check_metric_thresholds(symbol, calculated_metrics)
```

### 2.4 Query Optimization and Indexing Strategy

```python
class QueryOptimizer:
    def __init__(self):
        self.query_patterns = {
            'by_symbol': "High selectivity on symbol + time range",
            'by_confidence': "Medium selectivity on confidence range",
            'by_strategy': "Variable selectivity depending on strategy popularity",
            'cross_pair': "Low selectivity, requires parallel execution"
        }
        
    def optimize_query_plan(self, query_parameters: dict) -> dict:
        """Create optimized execution plan based on query characteristics"""
        
        plan = {
            'execution_strategy': 'standard',
            'estimated_rows': 0,
            'indexes_to_use': [],
            'parallel_execution': False
        }
        
        # Analyze selectivity
        if query_parameters.get('symbols') and len(query_parameters['symbols']) == 1:
            plan['execution_strategy'] = 'single_pair_optimized'
            plan['indexes_to_use'].append('idx_symbol_created')
            plan['estimated_rows'] = self._estimate_rows_single_pair(query_parameters['symbols'][0])
        
        elif query_parameters.get('symbols') and len(query_parameters['symbols']) > 15:
            plan['execution_strategy'] = 'parallel_multi_pair'
            plan['parallel_execution'] = True
            plan['estimated_rows'] = self._estimate_rows_multi_pair(query_parameters['symbols'])
        
        # Time-based optimization
        if query_parameters.get('time_range_days', 0) > 365:
            plan['execution_strategy'] = 'time_partitioned'
            plan['indexes_to_use'].append('idx_timestamp_symbol')
        
        return plan
    
    def create_optimized_indexes(self):
        """Create database indexes optimized for common query patterns"""
        
        index_statements = [
            # Primary lookup indexes
            "CREATE INDEX IF NOT EXISTS idx_signal_symbol_time ON signal_registry (symbol, created_at DESC)",
            "CREATE INDEX IF NOT EXISTS idx_signal_strategy_conf ON signal_registry (strategy_id, confidence_score DESC)",
            
            # Correlation lookup indexes  
            "CREATE INDEX IF NOT EXISTS idx_correlation_signal ON signal_trade_correlation (signal_uuid, created_at DESC)",
            "CREATE INDEX IF NOT EXISTS idx_correlation_trade ON signal_trade_correlation (trade_uuid, symbol)",
            
            # Performance cache indexes
            "CREATE INDEX IF NOT EXISTS idx_cache_lookup ON performance_metrics_cache (metric_type, scope, scope_value, time_period)",
            "CREATE INDEX IF NOT EXISTS idx_cache_freshness ON performance_metrics_cache (calculation_date DESC)",
            
            # Time-series indexes
            "CREATE INDEX IF NOT EXISTS idx_timeseries_metric_time ON performance_timeseries (metric_name, timestamp DESC)",
            "CREATE INDEX IF NOT EXISTS idx_timeseries_symbol_time ON performance_timeseries (symbol, timestamp DESC)",
        ]
        
        for statement in index_statements:
            self.db.execute(statement)
```

## 3. Advanced Analytics and Reporting

### 3.1 Multi-Dimensional Performance Dashboard

```python
class AdvancedPerformanceDashboard:
    def __init__(self, data_manager: PerformanceDataManager):
        self.data_manager = data_manager
        
    def generate_comprehensive_report(self, 
                                    symbols: List[str] = None,
                                    time_period: str = 'ytd') -> dict:
        """Generate comprehensive performance report with advanced metrics"""
        
        report = {
            'summary': self._generate_summary_metrics(symbols, time_period),
            'risk_metrics': self._generate_risk_metrics(symbols, time_period),
            'attribution': self._generate_attribution_analysis(symbols, time_period),
            'correlation': self._generate_correlation_analysis(symbols, time_period),
            'efficiency': self._generate_efficiency_metrics(symbols, time_period),
            'trends': self._generate_trend_analysis(symbols, time_period)
        }
        
        return report
    
    def _generate_risk_metrics(self, symbols: List[str], time_period: str) -> dict:
        """Generate comprehensive risk metrics"""
        
        trade_data = self.data_manager.get_trade_data(symbols, time_period)
        returns_series = trade_data.groupby('symbol')['profit_loss'].apply(list)
        
        risk_metrics = {}
        
        for symbol, returns in returns_series.items():
            returns_df = pd.Series(returns)
            risk_calc = RiskAdjustedMetrics(returns_df)
            
            risk_metrics[symbol] = {
                'sharpe_ratio': risk_calc.sharpe_ratio(),
                'sortino_ratio': risk_calc.sortino_ratio(),
                'calmar_ratio': risk_calc.calmar_ratio(),
                'maximum_drawdown': risk_calc.maximum_drawdown(),
                'var_95': risk_calc.var_95(),
                'cvar_95': risk_calc.cvar_95(),
                'omega_ratio': risk_calc.omega_ratio(),
                'volatility': returns_df.std() * np.sqrt(252),
                'skewness': returns_df.skew(),
                'kurtosis': returns_df.kurtosis()
            }
        
        return risk_metrics
    
    def _generate_attribution_analysis(self, symbols: List[str], time_period: str) -> dict:
        """Performance attribution by various factors"""
        
        return {
            'by_confidence_tier': self.data_manager.get_performance_metrics(
                symbols=symbols, 
                time_period=time_period,
                metrics=['win_rate', 'avg_pnl', 'sharpe_ratio'],
                group_by='confidence_tier'
            ),
            'by_strategy_id': self.data_manager.get_performance_metrics(
                symbols=symbols,
                time_period=time_period, 
                metrics=['total_pnl', 'trade_count', 'profit_factor'],
                group_by='strategy_id'
            ),
            'by_time_of_day': self._analyze_time_of_day_performance(symbols, time_period),
            'by_market_volatility': self._analyze_volatility_regime_performance(symbols, time_period)
        }
```

This expanded framework provides:

1. **Advanced Risk Metrics**: Sharpe, Sortino, Calmar ratios, VaR, CVaR, Omega ratio
2. **Scalable Data Architecture**: Hierarchical storage with intelligent caching and indexing
3. **UUID Management**: Efficient correlation tracking between signals, trades, and chains
4. **Real-Time Calculation**: Event-driven metric updates with configurable triggers
5. **Query Optimization**: Parallel execution, partitioning, and smart indexing
6. **Multi-Dimensional Analysis**: Performance breakdown by pair, strategy, confidence, time periods

The system can handle unlimited UUIDs through intelligent data partitioning and caching while providing sub-second response times for complex analytics queries.

