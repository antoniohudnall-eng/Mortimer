#!/usr/bin/env python3
"""
Dark Factory Pipeline Manager
Ongoing production pipeline with THIS integration and automated processing
"""

import os
import sqlite3
import json
import time
import uuid
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
import logging

# Setup logging - works in both CI and local environments
log_dir = os.environ.get('DF_LOG_DIR', '/var/log/dark_factory')
log_file = os.path.join(log_dir, 'pipeline.log')

# Try to ensure log directory exists, fallback to local if needed
try:
    os.makedirs(log_dir, exist_ok=True)
    handlers = [logging.FileHandler(log_file), logging.StreamHandler()]
except (OSError, PermissionError):
    # CI or restricted environment - use local logs in the repo
    script_dir = os.path.dirname(os.path.abspath(__file__))
    local_log = os.path.join(script_dir, 'logs', 'pipeline.log')
    os.makedirs(os.path.dirname(local_log), exist_ok=True)
    handlers = [logging.FileHandler(local_log), logging.StreamHandler()]
    log_file = local_log

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=handlers
)
logger = logging.getLogger('DarkFactoryPipeline')

class DarkFactoryPipeline:
    """Manages the ongoing Dark Factory production pipeline"""
    
    VERSION = "1.1.0"
    DB_PATH = "/root/.openclaw/workspace/data/factory/dark_factory.db"
    
    # Production stages
    STAGES = [
        "queued",           # 0 - Waiting to start
        "design",           # 1 - Design phase
        "vendor_sourcing",  # 2 - Finding vendors
        "procurement",      # 3 - Ordering materials
        "production",       # 4 - Manufacturing
        "assembly",         # 5 - Putting it together
        "qc",               # 6 - Quality control
        "packaging",        # 7 - Packaging
        "shipping_prep",    # 8 - Ready to ship
        "distribution",     # 9 - In transit
        "delivered"         # 10 - Complete
    ]
    
    def __init__(self):
        self.db_path = Path(self.DB_PATH)
        self.ensure_db()
        logger.info(f"🌑 Dark Factory Pipeline v{self.VERSION} initialized")
    
    def ensure_db(self):
        """Ensure database exists with proper schema"""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(self.DB_PATH)
        c = conn.cursor()
        
        # Production orders table
        c.execute('''
            CREATE TABLE IF NOT EXISTS production_orders (
                id TEXT PRIMARY KEY,
                product_name TEXT NOT NULL,
                product_type TEXT NOT NULL,
                quantity INTEGER DEFAULT 1,
                status TEXT DEFAULT 'queued',
                stage INTEGER DEFAULT 0,
                total_stages INTEGER DEFAULT 10,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                started_at TIMESTAMP,
                completed_at TIMESTAMP,
                priority TEXT DEFAULT 'normal',
                assigned_agents TEXT,
                metadata TEXT,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Pipeline metrics table
        c.execute('''
            CREATE TABLE IF NOT EXISTS pipeline_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                orders_queued INTEGER DEFAULT 0,
                orders_in_progress INTEGER DEFAULT 0,
                orders_completed INTEGER DEFAULT 0,
                avg_processing_time REAL,
                defect_count INTEGER DEFAULT 0,
                sigma_level REAL DEFAULT 0.0
            )
        ''')
        
        # Patricia integration log
        c.execute('''
            CREATE TABLE IF NOT EXISTS patricia_reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id TEXT,
                report_type TEXT,
                status TEXT,
                metrics TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("✅ Database schema verified")
    
    def add_order(self, product_name: str, product_type: str, 
                  quantity: int = 1, priority: str = "normal",
                  client: str = None, metadata: Dict = None) -> str:
        """Add a new order to the pipeline"""
        order_id = f"DF-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"
        
        conn = sqlite3.connect(self.DB_PATH)
        c = conn.cursor()
        c.execute('''
            INSERT INTO production_orders 
            (id, product_name, product_type, quantity, status, stage, priority, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (order_id, product_name, product_type, quantity, 'queued', 0, priority,
              json.dumps(metadata or {})))
        conn.commit()
        conn.close()
        
        logger.info(f"📦 New order added: {order_id} - {product_name} x{quantity}")
        self.sync_to_github(f"New order: {order_id}")
        return order_id
    
    def advance_order(self, order_id: str) -> bool:
        """Advance an order to the next stage"""
        conn = sqlite3.connect(self.DB_PATH)
        c = conn.cursor()
        
        c.execute('SELECT stage, status FROM production_orders WHERE id = ?', (order_id,))
        result = c.fetchone()
        
        if not result:
            logger.error(f"❌ Order not found: {order_id}")
            conn.close()
            return False
        
        current_stage, status = result
        
        if status == 'completed':
            logger.warning(f"⚠️ Order {order_id} already completed")
            conn.close()
            return False
        
        new_stage = current_stage + 1
        new_status = self.STAGES[min(new_stage, len(self.STAGES) - 1)]
        
        # Mark as started if advancing from queued
        started_at = None
        if current_stage == 0:
            started_at = datetime.now().isoformat()
        
        # Mark completed if at final stage
        completed_at = None
        if new_stage >= len(self.STAGES) - 1:
            completed_at = datetime.now().isoformat()
            new_status = 'completed'
            logger.info(f"✅ Order {order_id} COMPLETED!")
        
        c.execute('''
            UPDATE production_orders 
            SET stage = ?, status = ?, started_at = COALESCE(?, started_at),
                completed_at = ?, last_updated = ?
            WHERE id = ?
        ''', (new_stage, new_status, started_at, completed_at, 
              datetime.now().isoformat(), order_id))
        
        conn.commit()
        conn.close()
        
        stage_name = self.STAGES[new_stage] if new_stage < len(self.STAGES) else "completed"
        logger.info(f"⏩ Order {order_id} advanced to: {stage_name}")
        
        # Report to Patricia
        self.report_to_patricia(order_id, "stage_advanced", {"stage": stage_name})
        
        return True
    
    def get_queue(self, status_filter: str = None) -> List[Dict]:
        """Get current pipeline queue"""
        conn = sqlite3.connect(self.DB_PATH)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        
        if status_filter:
            c.execute('''
                SELECT * FROM production_orders 
                WHERE status = ? 
                ORDER BY priority DESC, created_at ASC
            ''', (status_filter,))
        else:
            c.execute('''
                SELECT * FROM production_orders 
                WHERE status != 'completed'
                ORDER BY priority DESC, stage DESC, created_at ASC
            ''')
        
        orders = [dict(row) for row in c.fetchall()]
        conn.close()
        return orders
    
    def get_metrics(self) -> Dict:
        """Get pipeline metrics"""
        conn = sqlite3.connect(self.DB_PATH)
        c = conn.cursor()
        
        c.execute('SELECT COUNT(*) FROM production_orders WHERE status = "queued"')
        queued = c.fetchone()[0]
        
        c.execute('SELECT COUNT(*) FROM production_orders WHERE status NOT IN ("queued", "completed", "delivered")')
        in_progress = c.fetchone()[0]
        
        c.execute('SELECT COUNT(*) FROM production_orders WHERE status IN ("completed", "delivered")')
        completed = c.fetchone()[0]
        
        c.execute('''
            SELECT AVG(
                julianday(completed_at) - julianday(started_at)
            ) FROM production_orders 
            WHERE completed_at IS NOT NULL
        ''')
        avg_time = c.fetchone()[0] or 0
        
        conn.close()
        
        return {
            "queued": queued,
            "in_progress": in_progress,
            "completed": completed,
            "avg_days": round(avg_time, 2) if avg_time else 0,
            "timestamp": datetime.now().isoformat()
        }
    
    def report_to_patricia(self, order_id: str, report_type: str, data: Dict):
        """Send report to Patricia/THIS system"""
        conn = sqlite3.connect(self.DB_PATH)
        c = conn.cursor()
        c.execute('''
            INSERT INTO patricia_reports (order_id, report_type, status, metrics)
            VALUES (?, ?, ?, ?)
        ''', (order_id, report_type, 'pending', json.dumps(data)))
        conn.commit()
        conn.close()
        
        # Try to notify Patricia if available
        try:
            patricia_path = "/root/.openclaw/workspace/agent_sandboxes/patricia/patricia_this_integration.py"
            if Path(patricia_path).exists():
                subprocess.run([
                    "python3", patricia_path, 
                    "--report", json.dumps({
                        "order_id": order_id,
                        "type": report_type,
                        "data": data
                    })
                ], capture_output=True, timeout=10)
                logger.info(f"📊 Reported to Patricia: {order_id}")
        except Exception as e:
            logger.debug(f"Patricia notification skipped: {e}")
    
    def bubblewrap_build(self, project_path: str, output_name: str, 
                        package_name: str = "com.agicorp.app",
                        shortcuts: List[Dict] = None) -> Dict:
        """
        Build Android APK from PWA using Bubblewrap CLI
        
        Args:
            project_path: Path to PWA manifest.json directory
            output_name: Output APK name (without extension)
            package_name: Android package ID
            shortcuts: List of app shortcuts
            
        Returns:
            Dict with build status, paths, and metadata
        """
        import shutil
        
        result = {
            "status": "failed",
            "order_id": None,
            "apk_path": None,
            "aab_path": None,
            "keystore_path": None,
            "errors": []
        }
        
        # Check for bubblewrap CLI
        bubblewrap = shutil.which("bubblewrap") or "npx @bubblewrap/cli"
        
        try:
            # Create order for tracking
            order_id = self.add_order(
                product_name=f"{output_name} (Bubblewrap APK)",
                product_type="mobile_android",
                priority="high",
                metadata={
                    "build_type": "bubblewrap",
                    "project_path": project_path,
                    "package_name": package_name
                }
            )
            result["order_id"] = order_id
            
            logger.info(f"🛠️ Starting Bubblewrap build: {output_name}")
            self.advance_order(order_id)
            
            # Check if manifest.json exists
            manifest_path = Path(project_path) / "manifest.json"
            if not manifest_path.exists():
                # Create a basic manifest if missing
                logger.warning(f"No manifest.json found at {manifest_path}, creating default")
                default_manifest = {
                    "name": output_name,
                    "short_name": output_name[:12],
                    "start_url": "/",
                    "display": "standalone",
                    "theme_color": "#2563eb",
                    "background_color": "#ffffff"
                }
                with open(manifest_path, 'w') as f:
                    json.dump(default_manifest, f, indent=2)
            
            # Run bubblewrap init
            logger.info(f"📦 Initializing Bubblewrap project...")
            init_result = subprocess.run(
                [bubblewrap, "init", "--manifest", str(manifest_path), 
                 "--directory", f"/tmp/bubblewrap/{output_name}"],
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if init_result.returncode != 0:
                result["errors"].append(f"Init failed: {init_result.stderr}")
                logger.error(f"❌ Bubblewrap init failed: {init_result.stderr}")
                return result
            
            self.advance_order(order_id)
            
            # Build APK
            logger.info(f"🔨 Building APK...")
            build_dir = f"/tmp/bubblewrap/{output_name}"
            build_result = subprocess.run(
                [bubblewrap, "build"],
                cwd=build_dir,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if build_result.returncode != 0:
                result["errors"].append(f"Build failed: {build_result.stderr}")
                logger.error(f"❌ Bubblewrap build failed: {build_result.stderr}")
                return result
            
            self.advance_order(order_id)
            
            # Find output files
            build_path = Path(build_dir)
            apk_files = list(build_path.glob("*.apk"))
            aab_files = list(build_path.glob("*.aab"))
            
            # Move to factory output
            output_dir = "/root/.openclaw/workspace/data/factory/output"
            Path(output_dir).mkdir(parents=True, exist_ok=True)
            
            if apk_files:
                dest_apk = f"{output_dir}/{output_name}.apk"
                shutil.copy(apk_files[0], dest_apk)
                result["apk_path"] = dest_apk
                logger.info(f"✅ APK created: {dest_apk}")
            
            if aab_files:
                dest_aab = f"{output_dir}/{output_name}.aab"
                shutil.copy(aab_files[0], dest_aab)
                result["aab_path"] = dest_aab
                logger.info(f"✅ AAB created: {dest_aab}")
            
            # Copy keystore for future updates
            keystore_files = list(build_path.glob("*.keystore")) + list(build_path.glob("*.jks"))
            if keystore_files:
                dest_key = f"{output_dir}/{output_name}.keystore"
                shutil.copy(keystore_files[0], dest_key)
                result["keystore_path"] = dest_key
            
            result["status"] = "success"
            self.advance_order(order_id)
            
            logger.info(f"🎉 Bubblewrap build complete: {output_name}")
            
        except subprocess.TimeoutExpired:
            result["errors"].append("Build timed out after 5 minutes")
            logger.error("⏱️ Bubblewrap build timed out")
        except Exception as e:
            result["errors"].append(str(e))
            logger.error(f"❌ Bubblewrap build error: {e}")
        
        return result
    
    def check_bubblewrap(self) -> Dict:
        """Check if Bubblewrap CLI is available and install if needed"""
        import shutil
        
        result = {
            "installed": False,
            "version": None,
            "path": None
        }
        
        # Check for npx
        npx = shutil.which("npx")
        if not npx:
            result["error"] = "npx not found - install Node.js"
            return result
        
        # Check for bubblewrap
        try:
            check = subprocess.run(
                ["npx", "@bubblewrap/cli", "--version"],
                capture_output=True,
                text=True,
                timeout=30
            )
            if check.returncode == 0:
                result["installed"] = True
                result["version"] = check.stdout.strip()
                result["path"] = "npx @bubblewrap/cli"
                logger.info(f"✅ Bubblewrap available: {result['version']}")
            else:
                logger.info("ℹ️ Bubblewrap not cached, will install on first use")
                result["installed"] = True  # npx will install it
                result["path"] = "npx @bubblewrap/cli"
        except Exception as e:
            result["error"] = str(e)
            logger.error(f"❌ Bubblewrap check failed: {e}")
        
        return result
    
    def sync_to_github(self, message: str = "Pipeline update"):
        """Sync state to GitHub"""
        try:
            workspace = "/root/.openclaw/workspace"
            subprocess.run(
                ["git", "add", "-A"],
                cwd=workspace, capture_output=True, timeout=10
            )
            subprocess.run(
                ["git", "commit", "-m", f"Dark Factory: {message}"],
                cwd=workspace, capture_output=True, timeout=10
            )
            subprocess.run(
                ["git", "push", "origin", "master"],
                cwd=workspace, capture_output=True, timeout=30
            )
            logger.info("☁️ Synced to GitHub")
        except Exception as e:
            logger.debug(f"GitHub sync skipped: {e}")
    
    def run_pipeline_tick(self):
        """Process one pipeline tick - advance orders, check status"""
        logger.info("🔄 Running pipeline tick...")
        
        # Get orders ready to advance (simulate processing time)
        conn = sqlite3.connect(self.DB_PATH)
        c = conn.cursor()
        
        # Advance orders that have been in current stage long enough
        # (In real system, this would check external APIs, vendor status, etc.)
        c.execute('''
            SELECT id, stage, status, last_updated FROM production_orders
            WHERE status NOT IN ('completed', 'queued')
            AND datetime(last_updated) < datetime('now', '-1 hour')
            ORDER BY priority DESC, stage ASC
            LIMIT 3
        ''')
        
        ready_orders = c.fetchall()
        conn.close()
        
        for order_id, stage, status, last_updated in ready_orders:
            self.advance_order(order_id)
            time.sleep(0.5)  # Rate limiting
        
        # Update metrics
        metrics = self.get_metrics()
        conn = sqlite3.connect(self.DB_PATH)
        c = conn.cursor()
        c.execute('''
            INSERT INTO pipeline_metrics 
            (orders_queued, orders_in_progress, orders_completed, avg_processing_time)
            VALUES (?, ?, ?, ?)
        ''', (metrics['queued'], metrics['in_progress'], 
              metrics['completed'], metrics['avg_days']))
        conn.commit()
        conn.close()
        
        logger.info(f"📈 Metrics: {metrics['queued']} queued, "
                   f"{metrics['in_progress']} active, "
                   f"{metrics['completed']} completed")
        
        return metrics
    
    def generate_report(self) -> str:
        """Generate a status report"""
        metrics = self.get_metrics()
        queue = self.get_queue()
        
        report = f"""
╔══════════════════════════════════════════════════════════════╗
║           🌑 DARK FACTORY PIPELINE REPORT                    ║
╠══════════════════════════════════════════════════════════════╣
║ Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC
╠══════════════════════════════════════════════════════════════╣
║ METRICS
║ ─────────────────────────────────────────────────────────────
║  • Queued:      {metrics['queued']:>3} orders
║  • In Progress:  {metrics['in_progress']:>3} orders  
║  • Completed:   {metrics['completed']:>3} orders
║  • Avg Time:    {metrics['avg_days']:>5.1f} days
╠══════════════════════════════════════════════════════════════╣
║ ACTIVE ORDERS
║ ─────────────────────────────────────────────────────────────"""
        
        for order in queue[:10]:
            status_emoji = {
                'queued': '⏳',
                'design': '🎨',
                'production': '🔧',
                'qc': '🔍',
                'distribution': '🚚',
            }.get(order['status'], '⏳')
            
            report += f"\n║  {status_emoji} {order['id'][:20]:<20} | {order['product_name'][:25]:<25} | {order['status']:<12}"
        
        if len(queue) > 10:
            report += f"\n║  ... and {len(queue) - 10} more orders"
        
        report += """
╚══════════════════════════════════════════════════════════════╝"""
        
        return report
    
    def run_continuous(self, interval_seconds: int = 300):
        """Run pipeline continuously"""
        logger.info(f"🚀 Starting continuous pipeline (tick every {interval_seconds}s)")
        
        while True:
            try:
                self.run_pipeline_tick()
                logger.info(f"⏱️  Sleeping {interval_seconds}s...")
                time.sleep(interval_seconds)
            except KeyboardInterrupt:
                logger.info("🛑 Pipeline stopped by user")
                break
            except Exception as e:
                logger.error(f"❌ Pipeline error: {e}")
                time.sleep(60)  # Retry after 1 min on error


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Dark Factory Pipeline')
    parser.add_argument('command', choices=[
        'status', 'queue', 'add', 'advance', 'tick', 'report', 'run', 'bubblewrap', 'check-bubblewrap'
    ])
    parser.add_argument('--product', '-p', help='Product name')
    parser.add_argument('--type', '-t', help='Product type')
    parser.add_argument('--quantity', '-q', type=int, default=1)
    parser.add_argument('--priority', default='normal', 
                       choices=['low', 'normal', 'high', 'urgent'])
    parser.add_argument('--client', '-c', help='Client name')
    parser.add_argument('--order-id', '-o', help='Order ID to advance')
    parser.add_argument('--interval', '-i', type=int, default=300,
                       help='Tick interval in seconds')
    parser.add_argument('--output', help='Output name for bubblewrap builds')
    parser.add_argument('--package', help='Android package name for bubblewrap')
    
    args = parser.parse_args()
    
    pipeline = DarkFactoryPipeline()
    
    if args.command == 'status':
        print(json.dumps(pipeline.get_metrics(), indent=2))
    
    elif args.command == 'queue':
        queue = pipeline.get_queue()
        for order in queue:
            print(f"{order['id']} | {order['product_name']} | {order['status']} | {order['priority']}")
    
    elif args.command == 'add':
        if not args.product:
            print("Error: --product required")
            return
        order_id = pipeline.add_order(
            product_name=args.product,
            product_type=args.type or 'general',
            quantity=args.quantity,
            priority=args.priority,
            client=args.client
        )
        print(f"Created order: {order_id}")
    
    elif args.command == 'advance':
        if not args.order_id:
            print("Error: --order-id required")
            return
        success = pipeline.advance_order(args.order_id)
        print(f"Advanced: {'✅' if success else '❌'}")
    
    elif args.command == 'tick':
        metrics = pipeline.run_pipeline_tick()
        print(json.dumps(metrics, indent=2))
    
    elif args.command == 'report':
        print(pipeline.generate_report())
    
    elif args.command == 'run':
        pipeline.run_continuous(args.interval)
    
    elif args.command == 'check-bubblewrap':
        status = pipeline.check_bubblewrap()
        print(json.dumps(status, indent=2))
    
    elif args.command == 'bubblewrap':
        if not args.product:
            print("Error: --product (project path) required")
            print("Example: python3 dark_factory_pipeline.py bubblewrap --product /path/to/pwa --type ClientOutreach")
            return
        result = pipeline.bubblewrap_build(
            project_path=args.product,
            output_name=args.output or args.type or "app",
            package_name=args.package or args.client or "com.agicorp.app"
        )
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
