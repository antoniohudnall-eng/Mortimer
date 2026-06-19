#!/usr/bin/env python3
"""
Build Patricia's Complete Queue
Consolidates all incomplete jobs across AGI Company for Patricia to manage
"""

import sqlite3
import json
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict

class PatriciaQueueBuilder:
    """Builds Patricia's complete work queue from all sources"""
    
    DB_PATH = "/root/.openclaw/workspace/data/factory/dark_factory.db"
    WORKSPACE = "/root/.openclaw/workspace"
    
    def __init__(self):
        self.queue = []
        print("🌑 Patricia Queue Builder initialized")
    
    def scan_dark_factory_orders(self) -> List[Dict]:
        """Get all incomplete Dark Factory orders"""
        conn = sqlite3.connect(self.DB_PATH)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        
        c.execute('''
            SELECT id, product_name, product_type, status, stage, priority,
                   datetime(created_at) as created, metadata
            FROM production_orders
            WHERE status NOT IN ('completed', 'delivered')
            ORDER BY priority DESC, created_at ASC
        ''')
        
        orders = []
        for row in c.fetchall():
            meta = json.loads(row['metadata']) if row['metadata'] else {}
            orders.append({
                "source": "Dark Factory",
                "id": row['id'],
                "title": row['product_name'],
                "type": row['product_type'],
                "status": row['status'],
                "stage": row['stage'],
                "priority": row['priority'],
                "created": row['created'],
                "client": meta.get('client', 'AGI Company'),
                "assigned_to": "Patricia",
                "category": "Production"
            })
        
        conn.close()
        return orders
    
    def scan_compliance_items(self) -> List[Dict]:
        """Scan for compliance tracking items"""
        items = []
        
        # Read COMPLIANCE_TRACKING.md for pending items
        compliance_file = Path(f"{self.WORKSPACE}/AGI_COMPANY/subsidiaries/PERFORMANCE_SUPPLY_DEPOT/products/COMPLIANCE_TRACKING.md")
        if compliance_file.exists():
            content = compliance_file.read_text()
            
            # Look for PENDING items
            if "PENDING" in content:
                items.append({
                    "source": "Compliance Tracking",
                    "id": "COMP-2026-ANNUAL-RECERT",
                    "title": "Annual Compliance Recertification 2026",
                    "type": "compliance_review",
                    "status": "pending",
                    "stage": 0,
                    "priority": "high",
                    "created": "2026-01-01",
                    "client": "AGI Company Board",
                    "assigned_to": "Patricia",
                    "category": "Governance"
                })
            
            # Look for agents with [DATE] placeholder
            date_placeholders = re.findall(r'\|\s*(\w+)\s*\|.*\|\s*\[DATE\]\s*\|', content)
            for agent in date_placeholders[:10]:  # Limit to first 10
                items.append({
                    "source": "Compliance Tracking",
                    "id": f"COMP-SIGN-{agent}",
                    "title": f"Executive Handbook Acknowledgment - {agent}",
                    "type": "acknowledgment",
                    "status": "pending",
                    "stage": 0,
                    "priority": "normal",
                    "created": "2026-01-01",
                    "client": agent,
                    "assigned_to": "Patricia",
                    "category": "Governance"
                })
        
        return items
    
    def scan_security_items(self) -> List[Dict]:
        """Scan for security-related incomplete items"""
        items = []
        
        # Check security alerts
        security_alerts = Path(f"{self.WORKSPACE}/security/alerts.json")
        if security_alerts.exists():
            try:
                with open(security_alerts) as f:
                    alerts = json.load(f)
                    for alert in alerts.get('alerts', []):
                        if alert.get('status') != 'resolved':
                            items.append({
                                "source": "Security Monitoring",
                                "id": f"SEC-{alert.get('id', 'UNKNOWN')}",
                                "title": alert.get('message', 'Security Alert'),
                                "type": "security",
                                "status": alert.get('status', 'open'),
                                "stage": 0,
                                "priority": alert.get('severity', 'medium'),
                                "created": alert.get('timestamp', datetime.now().isoformat()),
                                "client": "SENTINEL",
                                "assigned_to": "Patricia",
                                "category": "Security"
                            })
            except:
                pass
        
        return items
    
    def scan_scraper_queue(self) -> List[Dict]:
        """Scan for data scraper queue items"""
        items = []
        
        scraper_queue = Path(f"{self.WORKSPACE}/data/scraper/queue_status.json")
        if scraper_queue.exists():
            try:
                with open(scraper_queue) as f:
                    data = json.load(f)
                    queue_count = data.get('queue_items', 0)
                    if queue_count > 0:
                        items.append({
                            "source": "Data Scraper",
                            "id": "SCRAPER-QUEUE-001",
                            "title": f"Lead Scraper Queue ({queue_count} items)",
                            "type": "data_processing",
                            "status": "queued",
                            "stage": 0,
                            "priority": "normal",
                            "created": data.get('timestamp', '2026-04-05'),
                            "client": "Captain",
                            "assigned_to": "Patricia",
                            "category": "Data"
                        })
            except:
                pass
        
        return items
    
    def scan_report_backlog(self) -> List[Dict]:
        """Scan for incomplete reports"""
        items = []
        
        reports_dir = Path(f"{self.WORKSPACE}/reports")
        if reports_dir.exists():
            # Check for reports that might need follow-up
            report_files = list(reports_dir.glob("*.md"))
            for report_file in report_files[:5]:  # Check first 5
                content = report_file.read_text()
                
                # Look for incomplete markers
                if "PENDING" in content or "TODO" in content or "INCOMPLETE" in content:
                    items.append({
                        "source": "Reports",
                        "id": f"REPORT-{report_file.stem.upper()}",
                        "title": f"Complete Report: {report_file.stem.replace('_', ' ').title()}",
                        "type": "documentation",
                        "status": "in_progress",
                        "stage": 1,
                        "priority": "low",
                        "created": datetime.now().isoformat(),
                        "client": "AGI Company",
                        "assigned_to": "Patricia",
                        "category": "Documentation"
                    })
        
        return items
    
    def build_complete_queue(self) -> Dict:
        """Build Patricia's complete queue from all sources"""
        print("🔍 Scanning for incomplete work across AGI Company...")
        
        # Collect from all sources
        self.queue = []
        
        print("  📦 Scanning Dark Factory...")
        self.queue.extend(self.scan_dark_factory_orders())
        
        print("  📋 Scanning Compliance items...")
        self.queue.extend(self.scan_compliance_items())
        
        print("  🔒 Scanning Security items...")
        self.queue.extend(self.scan_security_items())
        
        print("  🌐 Scanning Data Scraper...")
        self.queue.extend(self.scan_scraper_queue())
        
        print("  📄 Scanning Reports...")
        self.queue.extend(self.scan_report_backlog())
        
        # Sort by priority
        priority_order = {"urgent": 0, "high": 1, "normal": 2, "low": 3}
        self.queue.sort(key=lambda x: (priority_order.get(x['priority'], 2), x['created']))
        
        # Generate summary
        by_category = {}
        by_priority = {}
        for item in self.queue:
            by_category[item['category']] = by_category.get(item['category'], 0) + 1
            by_priority[item['priority']] = by_priority.get(item['priority'], 0) + 1
        
        return {
            "generated_at": datetime.now().isoformat(),
            "total_items": len(self.queue),
            "by_category": by_category,
            "by_priority": by_priority,
            "queue": self.queue
        }
    
    def save_queue(self, queue_data: Dict):
        """Save queue to file"""
        queue_path = Path(f"{self.WORKSPACE}/agent_sandboxes/patricia/data")
        queue_path.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        queue_file = queue_path / f"patricia_queue_{timestamp}.json"
        
        with open(queue_file, 'w') as f:
            json.dump(queue_data, f, indent=2)
        
        print(f"\n✅ Queue saved: {queue_file}")
        return queue_file
    
    def generate_report(self, queue_data: Dict) -> str:
        """Generate human-readable queue report"""
        report = f"""
╔══════════════════════════════════════════════════════════════════════════╗
║                    🌑 PATRICIA'S COMPLETE WORK QUEUE                       ║
╠══════════════════════════════════════════════════════════════════════════╣
║ Generated: {queue_data['generated_at']}
║ Total Items: {queue_data['total_items']}
╠══════════════════════════════════════════════════════════════════════════╣
║ SUMMARY BY CATEGORY
║ ─────────────────────────────────────────────────────────────────────────"""
        
        for cat, count in sorted(queue_data['by_category'].items(), key=lambda x: -x[1]):
            report += f"\n║  • {cat:<15}: {count:>3} items"
        
        report += """
╠══════════════════════════════════════════════════════════════════════════╣
║ SUMMARY BY PRIORITY
║ ─────────────────────────────────────────────────────────────────────────"""
        
        priority_emojis = {"urgent": "🚨", "high": "🔴", "normal": "🟡", "low": "🟢"}
        for prio, count in sorted(queue_data['by_priority'].items(), key=lambda x: {"urgent": 0, "high": 1, "normal": 2, "low": 3}.get(x[0], 2)):
            emoji = priority_emojis.get(prio, "⚪")
            report += f"\n║  {emoji} {prio.upper():<8}: {count:>3} items"
        
        report += """
╠══════════════════════════════════════════════════════════════════════════╣
║ DETAILED QUEUE (Top 20)
║ ─────────────────────────────────────────────────────────────────────────"""
        
        for i, item in enumerate(queue_data['queue'][:20], 1):
            emoji = priority_emojis.get(item['priority'], "⚪")
            status_emoji = {
                'queued': '⏳', 'in_progress': '🔧', 'pending': '📋',
                'open': '🔓', 'stalled': '⛔'
            }.get(item['status'], '⏳')
            
            report += f"""
║ {i:2d}. {emoji} [{item['category']}] {item['title'][:45]}
║     ID: {item['id']:<30} Status: {status_emoji} {item['status']}
║     Source: {item['source']:<20} Client: {item['client']}"""
        
        if len(queue_data['queue']) > 20:
            report += f"\n║\n║ ... and {len(queue_data['queue']) - 20} more items"
        
        report += """
╚══════════════════════════════════════════════════════════════════════════╝
"""
        
        return report
    
    def import_to_patricia(self, queue_data: Dict):
        """Import items into Patricia's database"""
        conn = sqlite3.connect(self.DB_PATH)
        c = conn.cursor()
        
        imported = 0
        for item in queue_data['queue']:
            # Skip if already exists
            c.execute('SELECT 1 FROM production_orders WHERE id = ?', (item['id'],))
            if c.fetchone():
                continue
            
            # Add to production orders as a project
            c.execute('''
                INSERT INTO production_orders
                (id, product_name, product_type, quantity, status, stage, priority, metadata, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                item['id'],
                item['title'],
                item['type'],
                1,
                item['status'],
                item['stage'],
                item['priority'],
                json.dumps({
                    'client': item['client'],
                    'source': item['source'],
                    'category': item['category'],
                    'assigned_to': item['assigned_to']
                }),
                item['created']
            ))
            imported += 1
        
        conn.commit()
        conn.close()
        
        print(f"✅ Imported {imported} new items to Patricia's queue")
        return imported


def main():
    builder = PatriciaQueueBuilder()
    
    # Build complete queue
    queue_data = builder.build_complete_queue()
    
    # Generate and print report
    report = builder.generate_report(queue_data)
    print(report)
    
    # Save to file
    queue_file = builder.save_queue(queue_data)
    
    # Import to Patricia's database
    imported = builder.import_to_patricia(queue_data)
    
    print(f"\n📊 Summary:")
    print(f"   • Total items found: {queue_data['total_items']}")
    print(f"   • New items imported: {imported}")
    print(f"   • Queue file: {queue_file}")


if __name__ == "__main__":
    main()
