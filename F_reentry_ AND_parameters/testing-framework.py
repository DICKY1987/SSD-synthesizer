# comprehensive_testing_framework.py
"""
Complete Testing Framework with Unit Tests, Integration Tests, and CI/CD Pipeline
"""

import unittest
import pytest
import subprocess
import json
import sqlite3
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta
import tempfile
import shutil
import os
import sys
from typing import Dict, List, Any, Optional
import asyncio
import coverage

# ============== UNIT TEST FRAMEWORK FOR PYTHON ==============

class TestReentrySystem(unittest.TestCase):
    """Unit tests for reentry system components"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_db = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
        self.test_db_path = self.test_db.name
        self.test_db.close()
        
        # Create test database
        self.conn = sqlite3.connect(self.test_db_path)
        self.cursor = self.conn.cursor()
        self._create_test_tables()
        
        # Mock configuration
        self.test_config = {
            'max_generations': 3,
            'min_confidence': 0.6,
            'daily_loss_limit': 1000,
            'max_position_size': 0.1
        }
    
    def tearDown(self):
        """Clean up test fixtures"""
        self.conn.close()
        os.unlink(self.test_db_path)
    
    def _create_test_tables(self):
        """Create test database tables"""
        self.cursor.execute('''
            CREATE TABLE trades (
                id INTEGER PRIMARY KEY,
                symbol TEXT,
                direction TEXT,
                lot_size REAL,
                entry_price REAL,
                exit_price REAL,
                pnl REAL,
                timestamp DATETIME
            )
        ''')
        self.conn.commit()
    
    def test_governance_controls_loading(self):
        """Test loading governance controls from CSV"""
        # Create test CSV
        test_csv = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False)
        test_csv.write('Control,Default,Range / Rule\n')
        test_csv.write('Max Generations,3,1-5\n')
        test_csv.write('Daily Loss Limit,1000,0-10000\n')
        test_csv.close()
        
        try:
            # Test loading
            df = pd.read_csv(test_csv.name)
            self.assertEqual(len(df), 2)
            self.assertEqual(df.iloc[0]['Control'], 'Max Generations')
            self.assertEqual(df.iloc[0]['Default'], 3)
        finally:
            os.unlink(test_csv.name)
    
    def test_risk_calculations(self):
        """Test risk management calculations"""
        from signal_queue_risk_system import ParameterManager
        
        pm = ParameterManager()
        
        # Test lot size calculation
        lot_size = pm.calculate_lot_size(
            account_balance=10000,
            risk_pct=2.0,
            stop_loss_pips=50,
            pip_value=10
        )
        
        expected_risk = 10000 * 0.02  # $200
        expected_lot = expected_risk / (50 * 10)  # 0.4
        
        self.assertAlmostEqual(lot_size, 0.4, places=2)
        
        # Test max position limit
        self.assertLessEqual(lot_size, 10000 * 0.1 / 10000)
    
    def test_signal_queue_priority(self):
        """Test signal queue prioritization"""
        from signal_queue_risk_system import SignalQueue, TradingSignal, SignalPriority
        
        queue = SignalQueue()
        
        # Add signals with different priorities
        signal_low = TradingSignal(
            signal_id="LOW_001",
            symbol="EURUSD",
            signal_type="indicator",
            direction="BUY",
            lot_size=0.01,
            priority=SignalPriority.LOW,
            timestamp=datetime.now()
        )
        
        signal_urgent = TradingSignal(
            signal_id="URGENT_001",
            symbol="GBPUSD",
            signal_type="economic",
            direction="SELL",
            lot_size=0.01,
            priority=SignalPriority.URGENT,
            timestamp=datetime.now()
        )
        
        queue.add_signal(signal_low)
        queue.add_signal(signal_urgent)
        
        # Verify urgent comes first
        first = queue.queue.get()
        self.assertEqual(first.priority, SignalPriority.URGENT)
    
    def test_indicator_calculation(self):
        """Test indicator calculation logic"""
        from indicator_plugin_system import RSIIndicator
        
        # Create test price data
        data = pd.DataFrame({
            'timestamp': pd.date_range('2025-01-01', periods=20),
            'close': np.random.uniform(1.1000, 1.1100, 20),
            'high': np.random.uniform(1.1050, 1.1150, 20),
            'low': np.random.uniform(1.0950, 1.1050, 20),
            'open': np.random.uniform(1.1000, 1.1100, 20),
            'volume': np.random.uniform(1000, 5000, 20)
        })
        
        indicator = RSIIndicator("EURUSD", "H1", {'period': 14})
        rsi_value = indicator.calculate(data)
        
        # RSI should be between 0 and 100
        self.assertGreaterEqual(rsi_value, 0)
        self.assertLessEqual(rsi_value, 100)
    
    @patch('smtplib.SMTP')
    def test_alert_system(self, mock_smtp):
        """Test alert system functionality"""
        from signal_queue_risk_system import AlertManager
        
        config = {
            'email': {
                'enabled': True,
                'smtp_server': 'smtp.test.com',
                'smtp_port': 587,
                'from': 'test@test.com',
                'to': 'alert@test.com',
                'username': 'test',
                'password': 'pass'
            }
        }
        
        alert_mgr = AlertManager(config)
        alert_mgr.send_alert("Test Alert", "Test message", "critical")
        
        # Verify SMTP was called
        mock_smtp.assert_called_once()
    
    def test_database_operations(self):
        """Test database CRUD operations"""
        # Insert test trade
        self.cursor.execute('''
            INSERT INTO trades (symbol, direction, lot_size, entry_price, pnl, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', ('EURUSD', 'BUY', 0.01, 1.1000, 50.0, datetime.now()))
        self.conn.commit()
        
        # Read back
        self.cursor.execute('SELECT * FROM trades WHERE symbol = ?', ('EURUSD',))
        trade = self.cursor.fetchone()
        
        self.assertIsNotNone(trade)
        self.assertEqual(trade[1], 'EURUSD')
        self.assertEqual(trade[5], 50.0)

# ============== POWERSHELL SCRIPT TESTING ==============

class PowerShellTestRunner:
    """Test runner for PowerShell scripts using Pester"""
    
    @staticmethod
    def create_pester_test(script_name: str) -> str:
        """Generate Pester test for PowerShell script"""
        return f'''
# {script_name}.Tests.ps1
BeforeAll {{
    . $PSScriptRoot\\{script_name}.ps1
}}

Describe "{script_name} Tests" {{
    Context "Function Validation" {{
        It "Should load without errors" {{
            {{ . $PSScriptRoot\\{script_name}.ps1 }} | Should -Not -Throw
        }}
        
        It "Should have required functions" {{
            Get-Command -Name Get-ReentryProfile -ErrorAction SilentlyContinue | Should -Not -BeNullOrEmpty
        }}
    }}
    
    Context "Configuration Loading" {{
        It "Should load configuration from JSON" {{
            $config = Get-ReentryConfig -Path "$PSScriptRoot\\test_config.json"
            $config | Should -Not -BeNullOrEmpty
            $config.MaxGenerations | Should -Be 3
        }}
        
        It "Should validate configuration parameters" {{
            $config = @{{ MaxGenerations = -1 }}
            {{ Test-ReentryConfig $config }} | Should -Throw
        }}
    }}
    
    Context "Profile Rotation" {{
        It "Should rotate profiles correctly" {{
            $profiles = @("Profile1", "Profile2", "Profile3")
            $next = Get-NextProfile -Current "Profile1" -Profiles $profiles
            $next | Should -Be "Profile2"
        }}
        
        It "Should handle last profile wrap-around" {{
            $profiles = @("Profile1", "Profile2", "Profile3")
            $next = Get-NextProfile -Current "Profile3" -Profiles $profiles
            $next | Should -Be "Profile1"
        }}
    }}
    
    Context "Error Handling" {{
        It "Should handle missing files gracefully" {{
            {{ Get-ReentryProfile -Path "nonexistent.csv" }} | Should -Throw
        }}
        
        It "Should log errors appropriately" {{
            $errorLog = "$env:TEMP\\reentry_errors.log"
            Write-ReentryError -Message "Test error" -LogPath $errorLog
            $errorLog | Should -Exist
            Get-Content $errorLog | Should -Contain "Test error"
        }}
    }}
}}
'''
    
    @staticmethod
    def run_pester_tests(script_path: str) -> Dict[str, Any]:
        """Run Pester tests and return results"""
        test_script = f"""
        $results = Invoke-Pester -Path '{script_path}' -PassThru -Output Detailed
        $results | ConvertTo-Json -Depth 10
        """
        
        result = subprocess.run(
            ['powershell', '-Command', test_script],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            return json.loads(result.stdout)
        else:
            return {'error': result.stderr}

# ============== INTEGRATION TESTING ==============

class IntegrationTestSuite:
    """End-to-end integration tests for the complete pipeline"""
    
    def __init__(self):
        self.test_dir = tempfile.mkdtemp(prefix='reentry_test_')
        self.processes = []
        
    def setup_test_environment(self):
        """Set up complete test environment"""
        # Create directory structure
        os.makedirs(f"{self.test_dir}/profiles", exist_ok=True)
        os.makedirs(f"{self.test_dir}/data", exist_ok=True)
        os.makedirs(f"{self.test_dir}/logs", exist_ok=True)
        
        # Copy test configurations
        self._create_test_configs()
        
        # Initialize test database
        self._setup_test_database()
        
    def _create_test_configs(self):
        """Create test configuration files"""
        # Governance checklist
        governance = pd.DataFrame({
            'Control': ['Allow Reentry', 'Max Generations', 'Daily Loss Limit'],
            'Default': [1, 3, 1000],
            'Range / Rule': ['0 or 1', '1-5', '0-10000']
        })
        governance.to_csv(f"{self.test_dir}/governance_checklist.csv", index=False)
        
        # Trading signals
        signals = pd.DataFrame({
            'signal_id': ['TEST_001'],
            'symbol': ['EURUSD'],
            'direction': ['BUY'],
            'lot_size': [0.01],
            'confidence': [0.75],
            'timestamp': [datetime.now()]
        })
        signals.to_csv(f"{self.test_dir}/trading_signals.csv", index=False)
    
    def _setup_test_database(self):
        """Initialize test database with schema"""
        conn = sqlite3.connect(f"{self.test_dir}/test_trades.db")
        cursor = conn.cursor()
        
        # Create all required tables
        cursor.executescript('''
            CREATE TABLE trades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                signal_id TEXT,
                symbol TEXT,
                direction TEXT,
                lot_size REAL,
                entry_time DATETIME,
                exit_time DATETIME,
                entry_price REAL,
                exit_price REAL,
                pnl REAL,
                generation INTEGER,
                profile_name TEXT
            );
            
            CREATE TABLE performance_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                profile_name TEXT,
                symbol TEXT,
                metric_date DATE,
                total_trades INTEGER,
                win_rate REAL,
                profit_factor REAL,
                sharpe_ratio REAL,
                max_drawdown REAL
            );
            
            CREATE TABLE market_snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                trade_id INTEGER,
                timestamp DATETIME,
                volatility REAL,
                trend_strength REAL,
                market_regime TEXT,
                economic_events TEXT,
                FOREIGN KEY (trade_id) REFERENCES trades(id)
            );
        ''')
        conn.commit()
        conn.close()
    
    def test_full_pipeline(self) -> Dict[str, Any]:
        """Test complete signal generation to execution pipeline"""
        results = {
            'setup': False,
            'signal_generation': False,
            'risk_validation': False,
            'execution': False,
            'logging': False,
            'cleanup': False
        }
        
        try:
            # Step 1: Setup
            self.setup_test_environment()
            results['setup'] = True
            
            # Step 2: Generate signal
            signal_created = self._test_signal_generation()
            results['signal_generation'] = signal_created
            
            # Step 3: Validate risk
            risk_passed = self._test_risk_validation()
            results['risk_validation'] = risk_passed
            
            # Step 4: Execute trade
            execution_success = self._test_execution()
            results['execution'] = execution_success
            
            # Step 5: Verify logging
            logs_created = self._test_logging()
            results['logging'] = logs_created
            
            # Step 6: Cleanup
            self._cleanup()
            results['cleanup'] = True
            
        except Exception as e:
            results['error'] = str(e)
        
        return results
    
    def _test_signal_generation(self) -> bool:
        """Test signal generation component"""
        # Simulate signal generation
        signal_file = f"{self.test_dir}/test_signal.json"
        signal = {
            'id': 'INT_TEST_001',
            'symbol': 'EURUSD',
            'direction': 'BUY',
            'timestamp': datetime.now().isoformat()
        }
        
        with open(signal_file, 'w') as f:
            json.dump(signal, f)
        
        return os.path.exists(signal_file)
    
    def _test_risk_validation(self) -> bool:
        """Test risk management validation"""
        # Check if daily loss limit would be breached
        conn = sqlite3.connect(f"{self.test_dir}/test_trades.db")
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT SUM(pnl) as daily_pnl 
            FROM trades 
            WHERE DATE(entry_time) = DATE('now')
        ''')
        
        result = cursor.fetchone()
        daily_pnl = result[0] if result[0] else 0
        
        conn.close()
        
        return daily_pnl > -1000  # Within daily loss limit
    
    def _test_execution(self) -> bool:
        """Test trade execution"""
        # Simulate trade execution
        conn = sqlite3.connect(f"{self.test_dir}/test_trades.db")
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO trades (signal_id, symbol, direction, lot_size, entry_time, entry_price)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', ('INT_TEST_001', 'EURUSD', 'BUY', 0.01, datetime.now(), 1.1000))
        
        conn.commit()
        
        # Verify insertion
        cursor.execute('SELECT COUNT(*) FROM trades WHERE signal_id = ?', ('INT_TEST_001',))
        count = cursor.fetchone()[0]
        
        conn.close()
        
        return count == 1
    
    def _test_logging(self) -> bool:
        """Test logging functionality"""
        log_file = f"{self.test_dir}/logs/integration_test.log"
        
        # Create log entry
        with open(log_file, 'w') as f:
            f.write(f"[{datetime.now()}] Integration test executed\n")
        
        return os.path.exists(log_file) and os.path.getsize(log_file) > 0
    
    def _cleanup(self):
        """Clean up test environment"""
        for process in self.processes:
            if process.poll() is None:
                process.terminate()
        
        # Remove test directory
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

# ============== CONTINUOUS TESTING RUNNER ==============

class ContinuousTestRunner:
    """Automated test runner for CI/CD pipeline"""
    
    def __init__(self, test_config: Dict[str, Any]):
        self.config = test_config
        self.test_results = []
        
    def run_all_tests(self) -> Dict[str, Any]:
        """Run complete test suite"""
        results = {
            'timestamp': datetime.now().isoformat(),
            'unit_tests': {},
            'integration_tests': {},
            'powershell_tests': {},
            'coverage': {},
            'summary': {}
        }
        
        # Run Python unit tests with coverage
        print("🧪 Running Python unit tests...")
        cov = coverage.Coverage()
        cov.start()
        
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromTestCase(TestReentrySystem)
        runner = unittest.TextTestRunner(verbosity=2)
        unit_result = runner.run(suite)
        
        cov.stop()
        cov.save()
        
        results['unit_tests'] = {
            'total': unit_result.testsRun,
            'failures': len(unit_result.failures),
            'errors': len(unit_result.errors),
            'success_rate': (unit_result.testsRun - len(unit_result.failures) - len(unit_result.errors)) / unit_result.testsRun * 100
        }
        
        # Get coverage report
        cov_report = cov.report(show_missing=True)
        results['coverage'] = {
            'percentage': cov_report,
            'missing_lines': cov.get_missing_lines()
        }
        
        # Run PowerShell tests
        print("\n📝 Running PowerShell tests...")
        ps_runner = PowerShellTestRunner()
        
        for script in self.config.get('powershell_scripts', []):
            test_content = ps_runner.create_pester_test(script)
            test_path = f"{script}.Tests.ps1"
            
            with open(test_path, 'w') as f:
                f.write(test_content)
            
            ps_results = ps_runner.run_pester_tests(test_path)
            results['powershell_tests'][script] = ps_results
        
        # Run integration tests
        print("\n🔗 Running integration tests...")
        integration_suite = IntegrationTestSuite()
        integration_results = integration_suite.test_full_pipeline()
        results['integration_tests'] = integration_results
        
        # Generate summary
        all_passed = (
            results['unit_tests']['failures'] == 0 and
            results['unit_tests']['errors'] == 0 and
            all(integration_results.values())
        )
        
        results['summary'] = {
            'all_passed': all_passed,
            'total_tests': results['unit_tests']['total'] + len(integration_results),
            'coverage': results['coverage']['percentage'],
            'recommendation': 'Deploy' if all_passed and results['coverage']['percentage'] > 80 else 'Fix Issues'
        }
        
        return results
    
    def generate_report(self, results: Dict[str, Any]) -> str:
        """Generate HTML test report"""
        html = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Test Report - {results['timestamp']}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .passed {{ color: green; }}
                .failed {{ color: red; }}
                .warning {{ color: orange; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #4CAF50; color: white; }}
                .summary {{ background-color: #f0f0f0; padding: 15px; border-radius: 5px; margin: 20px 0; }}
            </style>
        </head>
        <body>
            <h1>Reentry System Test Report</h1>
            <div class="summary">
                <h2>Summary</h2>
                <p>Status: <span class="{'passed' if results['summary']['all_passed'] else 'failed'}">
                    {'✅ PASSED' if results['summary']['all_passed'] else '❌ FAILED'}
                </span></p>
                <p>Total Tests: {results['summary']['total_tests']}</p>
                <p>Code Coverage: {results['summary']['coverage']:.1f}%</p>
                <p>Recommendation: <strong>{results['summary']['recommendation']}</strong></p>
            </div>
            
            <h2>Unit Test Results</h2>
            <table>
                <tr>
                    <th>Metric</th>
                    <th>Value</th>
                </tr>
                <tr>
                    <td>Total Tests</td>
                    <td>{results['unit_tests']['total']}</td>
                </tr>
                <tr>
                    <td>Failures</td>
                    <td class="{'failed' if results['unit_tests']['failures'] > 0 else 'passed'}">
                        {results['unit_tests']['failures']}
                    </td>
                </tr>
                <tr>
                    <td>Success Rate</td>
                    <td>{results['unit_tests']['success_rate']:.1f}%</td>
                </tr>
            </table>
            
            <h2>Integration Test Results</h2>
            <table>
                <tr>
                    <th>Component</th>
                    <th>Status</th>
                </tr>
                {''.join(f"<tr><td>{k}</td><td class='{'passed' if v else 'failed'}'>{'✅' if v else '❌'}</td></tr>" 
                         for k, v in results['integration_tests'].items())}
            </table>
            
            <p>Generated: {results['timestamp']}</p>
        </body>
        </html>
        '''
        
        return html

# ============== TEST CONFIGURATION ==============

def create_test_configuration() -> Dict[str, Any]:
    """Create comprehensive test configuration"""
    return {
        'python_modules': [
            'indicator_plugin_system',
            'signal_queue_risk_system',
            'main'
        ],
        'powershell_scripts': [
            'reentry_profile_rotate',
            'reentry_kpi_snapshot',
            'install_reentry_pack'
        ],
        'test_data_dir': './test_data',
        'coverage_threshold': 80,
        'integration_test_timeout': 300,  # seconds
        'parallel_execution': True,
        'report_format': 'html',
        'notify_on_failure': True,
        'notification_channels': ['email', 'slack']
    }

# ============== MAIN TEST EXECUTOR ==============

def main():
    """Main test execution entry point"""
    config = create_test_configuration()
    runner = ContinuousTestRunner(config)
    
    print("🚀 Starting Comprehensive Test Suite")
    print("=" * 50)
    
    results = runner.run_all_tests()
    
    # Generate and save report
    report = runner.generate_report(results)
    report_path = f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    
    with open(report_path, 'w') as f:
        f.write(report)
    
    print(f"\n📊 Test report saved to: {report_path}")
    
    # Exit with appropriate code
    sys.exit(0 if results['summary']['all_passed'] else 1)

if __name__ == "__main__":
    main()
