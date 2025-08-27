# realtime_monitoring_server.py
"""
WebSocket Server for Real-Time Dashboard Updates and Governance Violation Alerts
"""

import asyncio
import websockets
import json
import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
import psutil
import os
from typing import Dict, List, Any, Set
from dataclasses import dataclass, asdict
import threading
import queue

# ============== MONITORING DATA STRUCTURES ==============

@dataclass
class SystemMetrics:
    """System performance metrics"""
    cpu_percent: float
    memory_percent: float
    disk_usage: float
    network_latency: float
    db_queries_per_second: int
    mt4_bridge_status: str
    risk_monitor_status: str
    
@dataclass
class TradingMetrics:
    """Trading performance metrics"""
    daily_pnl: float
    win_rate: float
    active_positions: int
    drawdown: float
    profit_factor: float
    sharpe_ratio: float
    
@dataclass
class GovernanceViolation:
    """Governance rule violation"""
    rule: str
    current_value: Any
    limit_value: Any
    severity: str  # 'warning', 'violation', 'critical'
    timestamp: datetime
    message: str

# ============== GOVERNANCE MONITOR ==============

class GovernanceMonitor:
    """Monitor for governance rule violations"""
    
    def __init__(self, config_path: str = "governance_checklist.csv"):
        self.rules = self._load_rules(config_path)
        self.violations_queue = queue.Queue()
        self.current_state = {}
        
    def _load_rules(self, config_path: str) -> Dict:
        """Load governance rules from CSV"""
        try:
            df = pd.read_csv(config_path)
            rules = {}
            for _, row in df.iterrows():
                rules[row['Control']] = {
                    'default': row['Default'],
                    'range': row['Range / Rule'],
                    'action': row.get('Failure Action', 'alert')
                }
            return rules
        except Exception as e:
            logging.error(f"Failed to load governance rules: {e}")
            return {}
    
    def check_violations(self, current_metrics: Dict) -> List[GovernanceViolation]:
        """Check for governance violations"""
        violations = []
        
        # Check Max Generations
        if 'max_generations' in current_metrics:
            max_gen = self.rules.get('Max Generations', {}).get('default', 3)
            if current_metrics['max_generations'] > max_gen:
                violations.append(GovernanceViolation(
                    rule='Max Generations',
                    current_value=current_metrics['max_generations'],
                    limit_value=max_gen,
                    severity='violation',
                    timestamp=datetime.now(),
                    message=f"Generation {current_metrics['max_generations']} exceeds limit of {max_gen}"
                ))
        
        # Check Daily Loss Limit
        if 'daily_pnl' in current_metrics:
            daily_limit = self.rules.get('Daily Loss Limit', {}).get('default', 1000)
            if current_metrics['daily_pnl'] < -daily_limit:
                violations.append(GovernanceViolation(
                    rule='Daily Loss Limit',
                    current_value=current_metrics['daily_pnl'],
                    limit_value=-daily_limit,
                    severity='critical',
                    timestamp=datetime.now(),
                    message=f"Daily loss ${current_metrics['daily_pnl']:.2f} exceeds limit of ${daily_limit}"
                ))
        
        # Check Max Position Size
        if 'position_size' in current_metrics:
            max_size = self.rules.get('Max Position Size', {}).get('default', 0.1)
            if current_metrics['position_size'] > max_size:
                violations.append(GovernanceViolation(
                    rule='Max Position Size',
                    current_value=current_metrics['position_size'],
                    limit_value=max_size,
                    severity='violation',
                    timestamp=datetime.now(),
                    message=f"Position size {current_metrics['position_size']:.2f} exceeds limit of {max_size}"
                ))
        
        # Check Spread Guard
        if 'spread' in current_metrics:
            max_spread = self.rules.get('Spread Guard', {}).get('default', 3)
            if current_metrics['spread'] > max_spread:
                violations.append(GovernanceViolation(
                    rule='Spread Guard',
                    current_value=current_metrics['spread'],
                    limit_value=max_spread,
                    severity='warning',
                    timestamp=datetime.now(),
                    message=f"Spread {current_metrics['spread']:.1f} pips exceeds limit of {max_spread}"
                ))
        
        # Check Min Confidence
        if 'confidence' in current_metrics:
            min_conf = self.rules.get('Min Confidence', {}).get('default', 0.6)
            if current_metrics['confidence'] < min_conf:
                violations.append(GovernanceViolation(
                    rule='Min Confidence',
                    current_value=current_metrics['confidence'],
                    limit_value=min_conf,
                    severity='warning',
                    timestamp=datetime.now(),
                    message=f"Confidence {current_metrics['confidence']:.2f} below minimum of {min_conf}"
                ))
        
        return violations

# ============== REAL-TIME DATA COLLECTOR ==============

class RealTimeDataCollector:
    """Collect real-time trading and system data"""
    
    def __init__(self, db_path: str = "reentry_trades.db"):
        self.db_path = db_path
        self.last_query_time = datetime.now()
        self.query_count = 0
        
    def get_trading_metrics(self) -> TradingMetrics:
        """Get current trading metrics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Daily P/L
            cursor.execute('''
                SELECT COALESCE(SUM(pnl), 0) 
                FROM trades 
                WHERE DATE(entry_time) = DATE('now')
            ''')
            daily_pnl = cursor.fetchone()[0] or 0
            
            # Win rate
            cursor.execute('''
                SELECT 
                    COUNT(CASE WHEN pnl > 0 THEN 1 END) as wins,
                    COUNT(*) as total
                FROM trades
                WHERE entry_time >= datetime('now', '-7 days')
            ''')
            wins, total = cursor.fetchone()
            win_rate = (wins / total * 100) if total > 0 else 0
            
            # Active positions
            cursor.execute('''
                SELECT COUNT(*) 
                FROM trades 
                WHERE exit_time IS NULL
            ''')
            active_positions = cursor.fetchone()[0] or 0
            
            # Calculate drawdown
            cursor.execute('''
                SELECT pnl 
                FROM trades 
                WHERE entry_time >= datetime('now', '-30 days')
                ORDER BY entry_time
            ''')
            pnls = [row[0] for row in cursor.fetchall() if row[0] is not None]
            
            if pnls:
                cumsum = pd.Series(pnls).cumsum()
                running_max = cumsum.cummax()
                drawdown_series = cumsum - running_max
                drawdown = abs(drawdown_series.min() / running_max.max() * 100) if running_max.max() > 0 else 0
            else:
                drawdown = 0
            
            # Profit factor
            cursor.execute('''
                SELECT 
                    COALESCE(SUM(CASE WHEN pnl > 0 THEN pnl END), 0) as gross_profit,
                    COALESCE(SUM(CASE WHEN pnl < 0 THEN ABS(pnl) END), 0) as gross_loss
                FROM trades
                WHERE entry_time >= datetime('now', '-30 days')
            ''')
            gross_profit, gross_loss = cursor.fetchone()
            profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else 0
            
            # Sharpe ratio (simplified)
            if len(pnls) > 1:
                returns = pd.Series(pnls).pct_change().dropna()
                if len(returns) > 0 and returns.std() > 0:
                    sharpe_ratio = (returns.mean() / returns.std()) * np.sqrt(252)
                else:
                    sharpe_ratio = 0
            else:
                sharpe_ratio = 0
            
            conn.close()
            
            # Track query rate
            self.query_count += 7
            
            return TradingMetrics(
                daily_pnl=daily_pnl,
                win_rate=win_rate,
                active_positions=active_positions,
                drawdown=drawdown,
                profit_factor=profit_factor,
                sharpe_ratio=sharpe_ratio
            )
            
        except Exception as e:
            logging.error(f"Error getting trading metrics: {e}")
            return TradingMetrics(0, 0, 0, 0, 0, 0)
    
    def get_system_metrics(self) -> SystemMetrics:
        """Get current system metrics"""
        try:
            # Calculate queries per second
            now = datetime.now()
            elapsed = (now - self.last_query_time).total_seconds()
            if elapsed > 0:
                qps = self.query_count / elapsed
                if elapsed > 10:  # Reset counter every 10 seconds
                    self.query_count = 0
                    self.last_query_time = now
            else:
                qps = 0
            
            # Check MT4 bridge (simplified - would check actual connection)
            mt4_status = "Active"  # In production, check actual connection
            
            # Check risk monitor
            risk_monitor_status = "Active"  # In production, check process status
            
            return SystemMetrics(
                cpu_percent=psutil.cpu_percent(interval=0.1),
                memory_percent=psutil.virtual_memory().percent,
                disk_usage=psutil.disk_usage('/').percent,
                network_latency=12.5,  # In production, measure actual latency
                db_queries_per_second=int(qps),
                mt4_bridge_status=mt4_status,
                risk_monitor_status=risk_monitor_status
            )
        except Exception as e:
            logging.error(f"Error getting system metrics: {e}")
            return SystemMetrics(0, 0, 0, 0, 0, "Unknown", "Unknown")
    
    def get_equity_curve(self, days: int = 30) -> Dict:
        """Get equity curve data"""
        try:
            conn = sqlite3.connect(self.db_path)
            
            query = '''
                SELECT 
                    DATE(entry_time) as date,
                    SUM(pnl) OVER (ORDER BY entry_time) as cumulative_pnl
                FROM trades
                WHERE entry_time >= datetime('now', ? || ' days')
                ORDER BY entry_time
            '''
            
            df = pd.read_sql_query(query, conn, params=(-days,))
            conn.close()
            
            if not df.empty:
                # Resample to daily
                df['date'] = pd.to_datetime(df['date'])
                df = df.groupby('date').last().reset_index()
                
                # Add starting balance
                starting_balance = 10000
                df['equity'] = starting_balance + df['cumulative_pnl']
                
                return {
                    'labels': df['date'].dt.strftime('%m/%d').tolist(),
                    'values': df['equity'].tolist()
                }
            else:
                return {'labels': [], 'values': []}
                
        except Exception as e:
            logging.error(f"Error getting equity curve: {e}")
            return {'labels': [], 'values': []}

# ============== WEBSOCKET SERVER ==============

class MonitoringWebSocketServer:
    """WebSocket server for real-time dashboard updates"""
    
    def __init__(self, host: str = 'localhost', port: int = 8765):
        self.host = host
        self.port = port
        self.clients: Set[websockets.WebSocketServerProtocol] = set()
        self.data_collector = RealTimeDataCollector()
        self.governance_monitor = GovernanceMonitor()
        self.update_interval = 1  # seconds
        self.running = False
        
    async def register(self, websocket):
        """Register new client"""
        self.clients.add(websocket)
        logging.info(f"Client connected. Total clients: {len(self.clients)}")
        
        # Send initial data
        await self.send_update(websocket)
    
    async def unregister(self, websocket):
        """Unregister client"""
        self.clients.remove(websocket)
        logging.info(f"Client disconnected. Total clients: {len(self.clients)}")
    
    async def send_update(self, websocket):
        """Send update to specific client"""
        try:
            data = self.collect_data()
            await websocket.send(json.dumps(data, default=str))
        except Exception as e:
            logging.error(f"Error sending update: {e}")
    
    async def broadcast_update(self):
        """Broadcast update to all clients"""
        if self.clients:
            data = self.collect_data()
            message = json.dumps(data, default=str)
            
            # Send to all clients
            disconnected = set()
            for client in self.clients:
                try:
                    await client.send(message)
                except websockets.exceptions.ConnectionClosed:
                    disconnected.add(client)
            
            # Remove disconnected clients
            for client in disconnected:
                self.clients.remove(client)
    
    def collect_data(self) -> Dict:
        """Collect all monitoring data"""
        # Get metrics
        trading_metrics = self.data_collector.get_trading_metrics()
        system_metrics = self.data_collector.get_system_metrics()
        
        # Check for violations
        current_state = {
            'daily_pnl': trading_metrics.daily_pnl,
            'max_generations': 2,  # Would get from actual system
            'position_size': 0.05,  # Would get from actual system
            'spread': 1.5,  # Would get from broker
            'confidence': 0.75  # Would get from signal
        }
        
        violations = self.governance_monitor.check_violations(current_state)
        
        # Format alerts
        alerts = []
        for violation in violations:
            alerts.append({
                'type': violation.severity,
                'title': f'{violation.rule} Violation',
                'message': violation.message,
                'timestamp': violation.timestamp.isoformat()
            })
        
        # Get equity curve
        equity_curve = self.data_collector.get_equity_curve(30)
        
        # Compile all data
        return {
            'metrics': asdict(trading_metrics),
            'system_health': {
                'cpu': system_metrics.cpu_percent,
                'memory': system_metrics.memory_percent,
                'disk': system_metrics.disk_usage,
                'network': system_metrics.network_latency,
                'db_qps': system_metrics.db_queries_per_second,
                'mt4_bridge': system_metrics.mt4_bridge_status,
                'risk_monitor': system_metrics.risk_monitor_status
            },
            'equity_curve': equity_curve,
            'alerts': alerts,
            'timestamp': datetime.now().isoformat()
        }
    
    async def handle_client(self, websocket, path):
        """Handle client connection"""
        await self.register(websocket)
        try:
            async for message in websocket:
                # Handle client messages if needed
                data = json.loads(message)
                if data.get('action') == 'refresh':
                    await self.send_update(websocket)
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            await self.unregister(websocket)
    
    async def update_loop(self):
        """Main update loop"""
        while self.running:
            await self.broadcast_update()
            await asyncio.sleep(self.update_interval)
    
    async def start_server(self):
        """Start WebSocket server"""
        self.running = True
        
        # Start update loop
        update_task = asyncio.create_task(self.update_loop())
        
        # Start WebSocket server
        async with websockets.serve(self.handle_client, self.host, self.port):
            logging.info(f"WebSocket server started on ws://{self.host}:{self.port}")
            await asyncio.Future()  # Run forever

# ============== ALERT DISPATCHER ==============

class AlertDispatcher:
    """Dispatch alerts to various channels"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.alert_history = []
        self.alert_cooldown = {}  # Prevent alert spam
        
    def dispatch_alert(self, violation: GovernanceViolation):
        """Dispatch alert based on severity"""
        
        # Check cooldown
        cooldown_key = f"{violation.rule}_{violation.severity}"
        if cooldown_key in self.alert_cooldown:
            last_alert = self.alert_cooldown[cooldown_key]
            if (datetime.now() - last_alert).seconds < 300:  # 5 minute cooldown
                return
        
        # Log alert
        self.alert_history.append(violation)
        self.alert_cooldown[cooldown_key] = datetime.now()
        
        # Dispatch based on severity
        if violation.severity == 'critical':
            self._send_critical_alert(violation)
        elif violation.severity == 'violation':
            self._send_violation_alert(violation)
        else:
            self._send_warning_alert(violation)
    
    def _send_critical_alert(self, violation: GovernanceViolation):
        """Send critical alerts (SMS + Email + Dashboard)"""
        logging.critical(f"CRITICAL VIOLATION: {violation.message}")
        
        # In production, would send SMS and email
        # For now, just log
        print(f"🚨 CRITICAL: {violation.message}")
    
    def _send_violation_alert(self, violation: GovernanceViolation):
        """Send violation alerts (Email + Dashboard)"""
        logging.error(f"VIOLATION: {violation.message}")
        print(f"⚠️  VIOLATION: {violation.message}")
    
    def _send_warning_alert(self, violation: GovernanceViolation):
        """Send warning alerts (Dashboard only)"""
        logging.warning(f"WARNING: {violation.message}")
        print(f"⚡ WARNING: {violation.message}")

# ============== MAIN SERVER ==============

async def main():
    """Main server entry point"""
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Initialize server
    server = MonitoringWebSocketServer()
    
    print("=" * 60)
    print("🚀 Real-Time Monitoring Server")
    print("=" * 60)
    print(f"WebSocket: ws://localhost:8765")
    print(f"Dashboard: Open monitoring_dashboard.html in browser")
    print(f"Update Rate: Every {server.update_interval} second(s)")
    print("=" * 60)
    print("Press Ctrl+C to stop")
    print()
    
    # Create sample database if it doesn't exist
    if not os.path.exists("reentry_trades.db"):
        print("Creating sample database...")
        conn = sqlite3.connect("reentry_trades.db")
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT,
                direction TEXT,
                lot_size REAL,
                entry_time DATETIME,
                exit_time DATETIME,
                entry_price REAL,
                exit_price REAL,
                pnl REAL
            )
        ''')
        
        # Insert sample trades
        sample_trades = [
            ('EURUSD', 'BUY', 0.01, datetime.now() - timedelta(hours=5), 
             datetime.now() - timedelta(hours=4), 1.1000, 1.1020, 20),
            ('GBPUSD', 'SELL', 0.01, datetime.now() - timedelta(hours=3),
             datetime.now() - timedelta(hours=2), 1.2500, 1.2480, 20),
            ('USDJPY', 'BUY', 0.01, datetime.now() - timedelta(hours=1),
             None, 110.00, None, None)
        ]
        
        for trade in sample_trades:
            cursor.execute('''
                INSERT INTO trades (symbol, direction, lot_size, entry_time, 
                                  exit_time, entry_price, exit_price, pnl)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', trade)
        
        conn.commit()
        conn.close()
        print("✓ Sample database created")
    
    try:
        # Start server
        await server.start_server()
    except KeyboardInterrupt:
        print("\n👋 Shutting down server...")
        server.running = False

if __name__ == "__main__":
    asyncio.run(main())
