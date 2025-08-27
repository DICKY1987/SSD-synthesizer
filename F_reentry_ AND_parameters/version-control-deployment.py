# version_control_deployment.py
"""
Complete Version Control, CI/CD Pipeline, and Enhanced Database Schema
with Profile A/B Testing and Performance Tracking
"""

import git
import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import yaml
import hashlib
import shutil
import os
import subprocess
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
import logging
from enum import Enum

# ============== GIT VERSION CONTROL SYSTEM ==============

class GitVersionControl:
    """Git-based version control for trading system configurations"""
    
    def __init__(self, repo_path: str = "."):
        self.repo_path = repo_path
        self.repo = self._init_repo()
        
    def _init_repo(self) -> git.Repo:
        """Initialize or open git repository"""
        try:
            repo = git.Repo(self.repo_path)
        except git.InvalidGitRepositoryError:
            repo = git.Repo.init(self.repo_path)
            self._create_gitignore()
            self._initial_commit()
        return repo
    
    def _create_gitignore(self):
        """Create .gitignore for trading system"""
        gitignore_content = """
# Trading System Gitignore
*.pyc
__pycache__/
*.db
*.db-journal
*.log
logs/
backups/
*.bak
.env
credentials.json
api_keys.json
*.pem
*.key
test_reports/
coverage_reports/
.coverage
*.swp
.DS_Store
Thumbs.db

# Sensitive trading data
live_trades.csv
account_credentials.json
broker_config.json

# Temporary files
*.tmp
temp/
cache/

# IDE
.vscode/
.idea/
*.sublime-*

# Virtual environments
venv/
env/
ENV/
"""
        with open(os.path.join(self.repo_path, '.gitignore'), 'w') as f:
            f.write(gitignore_content)
    
    def _initial_commit(self):
        """Create initial commit"""
        self.repo.index.add(['.gitignore'])
        self.repo.index.commit("Initial commit: Trading system repository initialized")
    
    def create_config_branch(self, branch_name: str, description: str):
        """Create new branch for configuration changes"""
        current = self.repo.active_branch
        new_branch = self.repo.create_head(branch_name)
        new_branch.checkout()
        
        # Create branch info file
        branch_info = {
            'branch': branch_name,
            'created': datetime.now().isoformat(),
            'description': description,
            'parent': current.name
        }
        
        with open('.branch_info.json', 'w') as f:
            json.dump(branch_info, f, indent=2)
        
        self.repo.index.add(['.branch_info.json'])
        self.repo.index.commit(f"Create branch: {description}")
        
        return new_branch
    
    def tag_release(self, version: str, message: str):
        """Tag a release version"""
        tag = self.repo.create_tag(
            version,
            message=message,
            ref=self.repo.head.commit
        )
        return tag
    
    def get_config_history(self, file_path: str, limit: int = 10) -> List[Dict]:
        """Get configuration change history"""
        history = []
        
        for commit in self.repo.iter_commits(paths=file_path, max_count=limit):
            history.append({
                'hash': commit.hexsha[:8],
                'author': str(commit.author),
                'date': datetime.fromtimestamp(commit.committed_date),
                'message': commit.message.strip(),
                'files': list(commit.stats.files.keys())
            })
        
        return history
    
    def rollback_config(self, commit_hash: str, files: List[str] = None):
        """Rollback configuration to specific commit"""
        commit = self.repo.commit(commit_hash)
        
        if files:
            # Rollback specific files
            for file in files:
                self.repo.git.checkout(commit_hash, '--', file)
        else:
            # Full rollback
            self.repo.head.reset(commit, index=True, working_tree=True)
        
        return f"Rolled back to {commit_hash[:8]}: {commit.message}"

# ============== DEPLOYMENT PIPELINE ==============

class DeploymentStage(Enum):
    """Deployment stages"""
    DEV = "development"
    TEST = "testing"
    STAGING = "staging"
    PRODUCTION = "production"

@dataclass
class DeploymentConfig:
    """Deployment configuration"""
    stage: DeploymentStage
    version: str
    timestamp: datetime
    config_files: List[str]
    validation_passed: bool = False
    tests_passed: bool = False
    rollback_version: Optional[str] = None

class DeploymentPipeline:
    """Automated deployment pipeline with validation and rollback"""
    
    def __init__(self, repo_path: str = "."):
        self.git = GitVersionControl(repo_path)
        self.deployments: Dict[DeploymentStage, DeploymentConfig] = {}
        self.deployment_history = []
        
    def validate_configuration(self, config_path: str) -> Tuple[bool, List[str]]:
        """Validate configuration before deployment"""
        errors = []
        
        try:
            # Load configuration
            if config_path.endswith('.json'):
                with open(config_path) as f:
                    config = json.load(f)
            elif config_path.endswith('.yaml'):
                with open(config_path) as f:
                    config = yaml.safe_load(f)
            else:
                errors.append(f"Unsupported config format: {config_path}")
                return False, errors
            
            # Validate required fields
            required_fields = ['max_generations', 'daily_loss_limit', 'max_position_size']
            for field in required_fields:
                if field not in config:
                    errors.append(f"Missing required field: {field}")
            
            # Validate value ranges
            if 'max_generations' in config:
                if not 1 <= config['max_generations'] <= 10:
                    errors.append("max_generations must be between 1 and 10")
            
            if 'daily_loss_limit' in config:
                if config['daily_loss_limit'] <= 0:
                    errors.append("daily_loss_limit must be positive")
            
            if 'max_position_size' in config:
                if not 0 < config['max_position_size'] <= 1:
                    errors.append("max_position_size must be between 0 and 1")
            
        except Exception as e:
            errors.append(f"Configuration load error: {str(e)}")
        
        return len(errors) == 0, errors
    
    def run_pre_deployment_tests(self) -> Tuple[bool, Dict]:
        """Run tests before deployment"""
        results = {
            'unit_tests': False,
            'integration_tests': False,
            'config_validation': False,
            'database_migration': False
        }
        
        # Run unit tests
        try:
            result = subprocess.run(
                ['python', '-m', 'pytest', 'tests/', '-v'],
                capture_output=True,
                timeout=300
            )
            results['unit_tests'] = result.returncode == 0
        except Exception as e:
            logging.error(f"Unit tests failed: {e}")
        
        # Run integration tests
        try:
            from comprehensive_testing_framework import IntegrationTestSuite
            suite = IntegrationTestSuite()
            test_results = suite.test_full_pipeline()
            results['integration_tests'] = all(test_results.values())
        except Exception as e:
            logging.error(f"Integration tests failed: {e}")
        
        # Validate configurations
        config_files = ['governance_checklist.csv', 'reentry_profile_template.csv']
        all_valid = True
        for config in config_files:
            if os.path.exists(config):
                valid, _ = self.validate_configuration(config)
                all_valid = all_valid and valid
        results['config_validation'] = all_valid
        
        # Check database migrations
        results['database_migration'] = self._check_database_migrations()
        
        return all(results.values()), results
    
    def _check_database_migrations(self) -> bool:
        """Check if database migrations are up to date"""
        try:
            conn = sqlite3.connect('reentry_trades.db')
            cursor = conn.cursor()
            
            # Check for migration table
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name='schema_migrations'
            """)
            
            if not cursor.fetchone():
                # Create migration table
                cursor.execute("""
                    CREATE TABLE schema_migrations (
                        version INTEGER PRIMARY KEY,
                        applied_at DATETIME,
                        description TEXT
                    )
                """)
                conn.commit()
            
            conn.close()
            return True
        except Exception as e:
            logging.error(f"Database migration check failed: {e}")
            return False
    
    def deploy(self, stage: DeploymentStage, version: str, 
               config_files: List[str]) -> Dict[str, Any]:
        """Deploy configuration to specific stage"""
        deployment = DeploymentConfig(
            stage=stage,
            version=version,
            timestamp=datetime.now(),
            config_files=config_files
        )
        
        # Validate configurations
        for config in config_files:
            valid, errors = self.validate_configuration(config)
            if not valid:
                return {
                    'success': False,
                    'stage': stage.value,
                    'errors': errors
                }
        
        deployment.validation_passed = True
        
        # Run tests for staging and production
        if stage in [DeploymentStage.STAGING, DeploymentStage.PRODUCTION]:
            tests_passed, test_results = self.run_pre_deployment_tests()
            deployment.tests_passed = tests_passed
            
            if not tests_passed:
                return {
                    'success': False,
                    'stage': stage.value,
                    'errors': ['Tests failed', test_results]
                }
        
        # Store current version for rollback
        if stage in self.deployments:
            deployment.rollback_version = self.deployments[stage].version
        
        # Deploy files
        deployment_dir = f"deployments/{stage.value}"
        os.makedirs(deployment_dir, exist_ok=True)
        
        for config in config_files:
            shutil.copy2(config, deployment_dir)
        
        # Create deployment manifest
        manifest = asdict(deployment)
        manifest['stage'] = stage.value
        manifest['timestamp'] = deployment.timestamp.isoformat()
        
        with open(f"{deployment_dir}/deployment_manifest.json", 'w') as f:
            json.dump(manifest, f, indent=2)
        
        # Update deployment record
        self.deployments[stage] = deployment
        self.deployment_history.append(deployment)
        
        # Git tag the deployment
        self.git.tag_release(
            f"{stage.value}-{version}",
            f"Deploy {version} to {stage.value}"
        )
        
        return {
            'success': True,
            'stage': stage.value,
            'version': version,
            'timestamp': deployment.timestamp.isoformat()
        }
    
    def rollback(self, stage: DeploymentStage) -> Dict[str, Any]:
        """Rollback to previous deployment"""
        if stage not in self.deployments:
            return {
                'success': False,
                'error': f"No deployment found for {stage.value}"
            }
        
        current = self.deployments[stage]
        
        if not current.rollback_version:
            return {
                'success': False,
                'error': "No previous version to rollback to"
            }
        
        # Find rollback deployment in history
        rollback_deployment = None
        for deployment in self.deployment_history:
            if deployment.stage == stage and deployment.version == current.rollback_version:
                rollback_deployment = deployment
                break
        
        if not rollback_deployment:
            return {
                'success': False,
                'error': f"Rollback version {current.rollback_version} not found"
            }
        
        # Perform rollback
        deployment_dir = f"deployments/{stage.value}"
        rollback_dir = f"deployments/{stage.value}_rollback_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Backup current deployment
        shutil.copytree(deployment_dir, rollback_dir)
        
        # Restore previous version
        for config in rollback_deployment.config_files:
            rollback_file = f"deployments/{stage.value}_v{rollback_deployment.version}/{config}"
            if os.path.exists(rollback_file):
                shutil.copy2(rollback_file, deployment_dir)
        
        # Update deployment record
        self.deployments[stage] = rollback_deployment
        
        return {
            'success': True,
            'stage': stage.value,
            'rolled_back_to': rollback_deployment.version,
            'rolled_back_from': current.version,
            'timestamp': datetime.now().isoformat()
        }

# ============== ENHANCED DATABASE SCHEMA ==============

class EnhancedDatabaseSchema:
    """Enhanced database schema with performance tracking and A/B testing"""
    
    def __init__(self, db_path: str = "reentry_trades_enhanced.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.create_schema()
    
    def create_schema(self):
        """Create enhanced database schema"""
        
        # Performance metrics table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS performance_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                profile_name TEXT NOT NULL,
                symbol TEXT NOT NULL,
                timeframe TEXT DEFAULT 'H1',
                metric_date DATE NOT NULL,
                total_trades INTEGER DEFAULT 0,
                winning_trades INTEGER DEFAULT 0,
                losing_trades INTEGER DEFAULT 0,
                win_rate REAL DEFAULT 0,
                profit_factor REAL DEFAULT 0,
                sharpe_ratio REAL DEFAULT 0,
                sortino_ratio REAL DEFAULT 0,
                max_drawdown REAL DEFAULT 0,
                avg_win REAL DEFAULT 0,
                avg_loss REAL DEFAULT 0,
                largest_win REAL DEFAULT 0,
                largest_loss REAL DEFAULT 0,
                consecutive_wins INTEGER DEFAULT 0,
                consecutive_losses INTEGER DEFAULT 0,
                recovery_factor REAL DEFAULT 0,
                expectancy REAL DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(profile_name, symbol, metric_date)
            )
        ''')
        
        # Market condition snapshots
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS market_snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                trade_id INTEGER,
                timestamp DATETIME NOT NULL,
                symbol TEXT NOT NULL,
                volatility_atr REAL,
                volatility_std REAL,
                trend_strength REAL,
                trend_direction TEXT,
                market_regime TEXT,
                session TEXT,
                spread REAL,
                volume REAL,
                rsi_value REAL,
                macd_signal TEXT,
                economic_events TEXT,
                news_sentiment REAL,
                correlation_matrix TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (trade_id) REFERENCES trades(id)
            )
        ''')
        
        # Profile version history
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS profile_versions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                profile_name TEXT NOT NULL,
                version INTEGER NOT NULL,
                config_json TEXT NOT NULL,
                parameters TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                created_by TEXT,
                change_description TEXT,
                parent_version INTEGER,
                is_active BOOLEAN DEFAULT 0,
                performance_score REAL,
                UNIQUE(profile_name, version)
            )
        ''')
        
        # A/B testing framework
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS ab_tests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                test_name TEXT NOT NULL UNIQUE,
                description TEXT,
                start_date DATETIME NOT NULL,
                end_date DATETIME,
                status TEXT DEFAULT 'running',
                control_profile TEXT NOT NULL,
                variant_profile TEXT NOT NULL,
                allocation_ratio REAL DEFAULT 0.5,
                min_sample_size INTEGER DEFAULT 100,
                confidence_level REAL DEFAULT 0.95,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # A/B test results
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS ab_test_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                test_id INTEGER NOT NULL,
                profile_name TEXT NOT NULL,
                trade_count INTEGER DEFAULT 0,
                total_pnl REAL DEFAULT 0,
                win_rate REAL DEFAULT 0,
                profit_factor REAL DEFAULT 0,
                sharpe_ratio REAL DEFAULT 0,
                max_drawdown REAL DEFAULT 0,
                avg_trade_duration INTEGER,
                statistical_significance REAL,
                p_value REAL,
                confidence_interval_lower REAL,
                confidence_interval_upper REAL,
                recommendation TEXT,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (test_id) REFERENCES ab_tests(id)
            )
        ''')
        
        # Enhanced trades table with profile tracking
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS trades_enhanced (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                signal_id TEXT UNIQUE,
                symbol TEXT NOT NULL,
                direction TEXT NOT NULL,
                lot_size REAL NOT NULL,
                entry_time DATETIME,
                exit_time DATETIME,
                entry_price REAL,
                exit_price REAL,
                stop_loss REAL,
                take_profit REAL,
                pnl REAL,
                pnl_pips REAL,
                commission REAL DEFAULT 0,
                swap REAL DEFAULT 0,
                generation INTEGER DEFAULT 0,
                profile_name TEXT,
                profile_version INTEGER,
                ab_test_id INTEGER,
                market_snapshot_id INTEGER,
                execution_time_ms INTEGER,
                slippage REAL DEFAULT 0,
                tags TEXT,
                notes TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (ab_test_id) REFERENCES ab_tests(id),
                FOREIGN KEY (market_snapshot_id) REFERENCES market_snapshots(id)
            )
        ''')
        
        # Create indexes for performance
        self.cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_trades_symbol_time 
            ON trades_enhanced(symbol, entry_time)
        ''')
        
        self.cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_performance_profile_date 
            ON performance_metrics(profile_name, metric_date)
        ''')
        
        self.cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_market_snapshots_trade 
            ON market_snapshots(trade_id, timestamp)
        ''')
        
        self.cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_profile_versions_active 
            ON profile_versions(profile_name, is_active)
        ''')
        
        # Create triggers for updated_at
        self.cursor.execute('''
            CREATE TRIGGER IF NOT EXISTS update_trades_timestamp 
            AFTER UPDATE ON trades_enhanced
            BEGIN
                UPDATE trades_enhanced SET updated_at = CURRENT_TIMESTAMP 
                WHERE id = NEW.id;
            END
        ''')
        
        self.conn.commit()
    
    def calculate_performance_metrics(self, profile_name: str, 
                                     symbol: str, date: datetime) -> Dict:
        """Calculate and store performance metrics for a profile"""
        
        # Get trades for the profile
        self.cursor.execute('''
            SELECT pnl, entry_time, exit_time, lot_size
            FROM trades_enhanced
            WHERE profile_name = ? AND symbol = ? 
            AND DATE(entry_time) <= DATE(?)
            ORDER BY entry_time
        ''', (profile_name, symbol, date))
        
        trades = self.cursor.fetchall()
        
        if not trades:
            return {}
        
        # Calculate metrics
        pnls = [t[0] for t in trades if t[0] is not None]
        winning_trades = [p for p in pnls if p > 0]
        losing_trades = [p for p in pnls if p < 0]
        
        metrics = {
            'total_trades': len(trades),
            'winning_trades': len(winning_trades),
            'losing_trades': len(losing_trades),
            'win_rate': len(winning_trades) / len(trades) * 100 if trades else 0,
            'profit_factor': sum(winning_trades) / abs(sum(losing_trades)) if losing_trades else 0,
            'avg_win': np.mean(winning_trades) if winning_trades else 0,
            'avg_loss': np.mean(losing_trades) if losing_trades else 0,
            'largest_win': max(winning_trades) if winning_trades else 0,
            'largest_loss': min(losing_trades) if losing_trades else 0,
            'expectancy': np.mean(pnls) if pnls else 0
        }
        
        # Calculate Sharpe Ratio
        if len(pnls) > 1:
            returns = pd.Series(pnls).pct_change().dropna()
            if len(returns) > 0 and returns.std() > 0:
                metrics['sharpe_ratio'] = (returns.mean() / returns.std()) * np.sqrt(252)
            else:
                metrics['sharpe_ratio'] = 0
        else:
            metrics['sharpe_ratio'] = 0
        
        # Calculate max drawdown
        cumsum = pd.Series(pnls).cumsum()
        running_max = cumsum.cummax()
        drawdown = cumsum - running_max
        metrics['max_drawdown'] = abs(drawdown.min()) if len(drawdown) > 0 else 0
        
        # Store metrics
        self.cursor.execute('''
            INSERT OR REPLACE INTO performance_metrics
            (profile_name, symbol, metric_date, total_trades, winning_trades, 
             losing_trades, win_rate, profit_factor, sharpe_ratio, max_drawdown,
             avg_win, avg_loss, largest_win, largest_loss, expectancy)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (profile_name, symbol, date.date(), metrics['total_trades'],
              metrics['winning_trades'], metrics['losing_trades'],
              metrics['win_rate'], metrics['profit_factor'],
              metrics['sharpe_ratio'], metrics['max_drawdown'],
              metrics['avg_win'], metrics['avg_loss'],
              metrics['largest_win'], metrics['largest_loss'],
              metrics['expectancy']))
        
        self.conn.commit()
        return metrics
    
    def create_ab_test(self, test_name: str, control_profile: str,
                      variant_profile: str, description: str = None) -> int:
        """Create new A/B test"""
        self.cursor.execute('''
            INSERT INTO ab_tests (test_name, description, start_date, 
                                 control_profile, variant_profile)
            VALUES (?, ?, ?, ?, ?)
        ''', (test_name, description, datetime.now(), control_profile, variant_profile))
        
        self.conn.commit()
        return self.cursor.lastrowid
    
    def update_ab_test_results(self, test_id: int):
        """Update A/B test results with statistical analysis"""
        # Get test configuration
        self.cursor.execute('''
            SELECT control_profile, variant_profile, confidence_level
            FROM ab_tests WHERE id = ?
        ''', (test_id,))
        
        test_config = self.cursor.fetchone()
        if not test_config:
            return
        
        control_profile, variant_profile, confidence_level = test_config
        
        # Calculate results for each profile
        for profile in [control_profile, variant_profile]:
            self.cursor.execute('''
                SELECT COUNT(*), SUM(pnl), AVG(pnl)
                FROM trades_enhanced
                WHERE profile_name = ? AND ab_test_id = ?
            ''', (profile, test_id))
            
            trade_count, total_pnl, avg_pnl = self.cursor.fetchone()
            
            if trade_count and trade_count > 0:
                # Calculate win rate
                self.cursor.execute('''
                    SELECT COUNT(*) FROM trades_enhanced
                    WHERE profile_name = ? AND ab_test_id = ? AND pnl > 0
                ''', (profile, test_id))
                
                wins = self.cursor.fetchone()[0]
                win_rate = (wins / trade_count) * 100 if trade_count > 0 else 0
                
                # Store results
                self.cursor.execute('''
                    INSERT OR REPLACE INTO ab_test_results
                    (test_id, profile_name, trade_count, total_pnl, win_rate)
                    VALUES (?, ?, ?, ?, ?)
                ''', (test_id, profile, trade_count, total_pnl or 0, win_rate))
        
        # Perform statistical significance test
        self._calculate_statistical_significance(test_id)
        
        self.conn.commit()
    
    def _calculate_statistical_significance(self, test_id: int):
        """Calculate statistical significance for A/B test"""
        # Simplified Z-test for win rates
        self.cursor.execute('''
            SELECT profile_name, trade_count, win_rate
            FROM ab_test_results
            WHERE test_id = ?
        ''', (test_id,))
        
        results = self.cursor.fetchall()
        
        if len(results) == 2:
            profile1, n1, p1 = results[0]
            profile2, n2, p2 = results[1]
            
            if n1 > 30 and n2 > 30:  # Sufficient sample size
                # Calculate pooled proportion
                p_pool = ((p1 * n1) + (p2 * n2)) / (n1 + n2)
                
                # Calculate standard error
                se = np.sqrt(p_pool * (1 - p_pool) * ((1/n1) + (1/n2)))
                
                # Calculate z-score
                if se > 0:
                    z_score = (p1 - p2) / se
                    
                    # Calculate p-value (two-tailed)
                    from scipy import stats
                    p_value = 2 * (1 - stats.norm.cdf(abs(z_score)))
                    
                    # Update with statistical significance
                    significance = p_value < 0.05
                    
                    recommendation = "No significant difference"
                    if significance:
                        if p1 > p2:
                            recommendation = f"Use {profile1} - significantly better"
                        else:
                            recommendation = f"Use {profile2} - significantly better"
                    
                    for profile in [profile1, profile2]:
                        self.cursor.execute('''
                            UPDATE ab_test_results
                            SET statistical_significance = ?, p_value = ?, 
                                recommendation = ?
                            WHERE test_id = ? AND profile_name = ?
                        ''', (significance, p_value, recommendation, test_id, profile))

# ============== ENHANCED PROFILE TEMPLATE ==============

def create_enhanced_profile_template(output_path: str = "enhanced_reentry_profile.csv"):
    """Create enhanced reentry profile template with diverse strategies"""
    
    profile_data = [
        # Headers
        ['Action', 'Type', 'SizeMultiplier', 'DelaySeconds', 'ConfidenceAdjustment', 'Parameters'],
        
        # Enhanced action configurations
        [1, 'NO_REENTRY', 0.0, 300, 0.0, ''],
        [2, 'REDUCE_SIZE', 0.5, 180, -0.1, 'reduce_factor=0.5;min_size=0.01'],
        [3, 'SAME_TRADE', 1.0, 120, 0.0, 'use_original_sl=true'],
        [4, 'INCREASE_SIZE', 1.5, 60, 0.1, 'max_increase=2.0;scale_with_confidence=true'],
        [5, 'MARTINGALE', 2.0, 30, 0.2, 'max_multiplier=4.0;reset_on_win=true'],
        [6, 'REVERSE', 1.0, 0, 0.3, 'reverse_immediately=true;use_opposite_signal=true']
    ]
    
    # Create DataFrame
    df = pd.DataFrame(profile_data[1:], columns=profile_data[0])
    
    # Add metadata as comments
    with open(output_path, 'w') as f:
        f.write("# Enhanced Reentry Profile Template\n")
        f.write("# Version: 2.0\n")
        f.write(f"# Generated: {datetime.now().isoformat()}\n")
        f.write("# Action Types:\n")
        f.write("#   NO_REENTRY: Skip reentry for this action bucket\n")
        f.write("#   REDUCE_SIZE: Decrease position size\n")
        f.write("#   SAME_TRADE: Maintain same size and direction\n")
        f.write("#   INCREASE_SIZE: Increase position size\n")
        f.write("#   MARTINGALE: Double down strategy\n")
        f.write("#   REVERSE: Reverse position direction\n")
        f.write("#   WAIT_SIGNAL: Wait for next signal\n")
        f.write("#   CUSTOM: Custom logic defined in parameters\n")
        f.write("#\n")
        
        # Write data
        df.to_csv(f, index=False)
    
    return df

# ============== MAIN IMPLEMENTATION ==============

def main():
    """Main implementation and demonstration"""
    
    print("🚀 Initializing Enhanced Trading System Infrastructure")
    print("=" * 60)
    
    # Initialize Git version control
    print("\n📚 Setting up version control...")
    git_control = GitVersionControl()
    
    # Create feature branch
    branch = git_control.create_config_branch(
        "feature/enhanced-profiles",
        "Add enhanced reentry profiles with A/B testing"
    )
    print(f"✓ Created branch: {branch.name}")
    
    # Initialize deployment pipeline
    print("\n🚢 Setting up deployment pipeline...")
    pipeline = DeploymentPipeline()
    
    # Create enhanced profile template
    print("\n📝 Creating enhanced profile template...")
    profile_df = create_enhanced_profile_template()
    print(f"✓ Created profile with {len(profile_df)} action configurations")
    
    # Initialize enhanced database
    print("\n💾 Setting up enhanced database schema...")
    db = EnhancedDatabaseSchema()
    print("✓ Database schema created with:")
    print("  - Performance metrics tracking")
    print("  - Market condition snapshots")
    print("  - Profile version history")
    print("  - A/B testing framework")
    
    # Create sample A/B test
    print("\n🧪 Creating sample A/B test...")
    test_id = db.create_ab_test(
        test_name="martingale_vs_conservative",
        control_profile="conservative_v1",
        variant_profile="martingale_v1",
        description="Test aggressive vs conservative reentry strategies"
    )
    print(f"✓ A/B test created with ID: {test_id}")
    
    # Deploy to staging
    print("\n🎯 Deploying to staging environment...")
    deployment_result = pipeline.deploy(
        stage=DeploymentStage.STAGING,
        version="2.0.0",
        config_files=["enhanced_reentry_profile.csv", "governance_checklist.csv"]
    )
    
    if deployment_result['success']:
        print(f"✓ Successfully deployed version {deployment_result['version']} to {deployment_result['stage']}")
    else:
        print(f"✗ Deployment failed: {deployment_result['errors']}")
    
    # Calculate sample performance metrics
    print("\n📊 Calculating performance metrics...")
    metrics = db.calculate_performance_metrics(
        profile_name="conservative_v1",
        symbol="EURUSD",
        date=datetime.now()
    )
    
    if metrics:
        print("✓ Performance metrics calculated:")
        print(f"  - Win Rate: {metrics.get('win_rate', 0):.1f}%")
        print(f"  - Profit Factor: {metrics.get('profit_factor', 0):.2f}")
        print(f"  - Sharpe Ratio: {metrics.get('sharpe_ratio', 0):.2f}")
    
    print("\n✅ Infrastructure setup complete!")
    print("\nNext steps:")
    print("1. Run comprehensive tests: python comprehensive_testing_framework.py")
    print("2. View dashboard: Open monitoring_dashboard.html in browser")
    print("3. Deploy to production: pipeline.deploy(DeploymentStage.PRODUCTION, ...)")
    print("4. Monitor A/B tests: Check ab_test_results table")
    
    # Close database connection
    db.conn.close()

if __name__ == "__main__":
    main()
