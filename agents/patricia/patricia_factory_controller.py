#!/usr/bin/env python3
"""
Patricia Factory Controller
Integrates Patricia with Dark Factory pipeline for quality control
"""

import sqlite3
import json
import sys
from pathlib import Path
from datetime import datetime

class PatriciaFactoryController:
    """Patricia's interface to the Dark Factory"""
    
    DB_PATH = "/root/.openclaw/workspace/data/factory/dark_factory.db"
    
    def __init__(self):
        self.db_path = Path(self.DB_PATH)
        print("🌑 Patricia Factory Controller initialized")
    
    def get_factory_metrics(self) -> dict:
        """Retrieve current factory metrics for analysis"""
        conn = sqlite3.connect(self.DB_PATH)
        c = conn.cursor()
        
        # Get order counts by status
        c.execute('''
            SELECT status, COUNT(*) FROM production_orders 
            GROUP BY status
        ''')
        status_counts = dict(c.fetchall())
        
        # Get recent orders
        c.execute('''
            SELECT id, product_name, status, stage, priority, created_at
            FROM production_orders
            ORDER BY created_at DESC
            LIMIT 10
        ''')
        recent_orders = [
            {
                "id": row[0],
                "product": row[1],
                "status": row[2],
                "stage": row[3],
                "priority": row[4],
                "created": row[5]
            }
            for row in c.fetchall()
        ]
        
        # Calculate cycle times for completed orders
        c.execute('''
            SELECT AVG(
                julianday(completed_at) - julianday(started_at)
            ) FROM production_orders 
            WHERE completed_at IS NOT NULL
        ''')
        avg_cycle_time = c.fetchone()[0] or 0
        
        conn.close()
        
        return {
            "timestamp": datetime.now().isoformat(),
            "status_summary": status_counts,
            "recent_orders": recent_orders,
            "avg_cycle_time_days": round(avg_cycle_time, 2),
            "total_orders": sum(status_counts.values()),
            "active_orders": status_counts.get('in_progress', 0) + status_counts.get('production', 0)
        }
    
    def analyze_for_defects(self) -> list:
        """Patricia's defect detection analysis"""
        conn = sqlite3.connect(self.DB_PATH)
        c = conn.cursor()
        
        defects = []
        
        # Check for stalled orders (over 48 hours in same stage)
        c.execute('''
            SELECT id, product_name, status, last_updated
            FROM production_orders
            WHERE status NOT IN ('completed', 'delivered')
            AND datetime(last_updated) < datetime('now', '-2 days')
        ''')
        stalled = c.fetchall()
        for row in stalled:
            defects.append({
                "type": "STALLED_ORDER",
                "order_id": row[0],
                "product": row[1],
                "current_status": row[2],
                "last_update": row[3],
                "severity": "HIGH",
                "recommendation": "Escalate or auto-advance"
            })
        
        # Check for high-priority orders stuck in queue
        c.execute('''
            SELECT id, product_name, priority, created_at
            FROM production_orders
            WHERE status = 'queued' AND priority = 'high'
            ORDER BY created_at
        ''')
        urgent_queued = c.fetchall()
        for row in urgent_queued:
            defects.append({
                "type": "HIGH_PRIORITY_DELAY",
                "order_id": row[0],
                "product": row[1],
                "priority": row[2],
                "queued_since": row[3],
                "severity": "MEDIUM",
                "recommendation": "Prioritize processing"
            })
        
        conn.close()
        return defects
    
    def generate_six_sigma_report(self) -> dict:
        """Generate Six Sigma quality report"""
        metrics = self.get_factory_metrics()
        defects = self.analyze_for_defects()
        
        total_orders = metrics['total_orders']
        defect_count = len(defects)
        
        # Calculate sigma level (simplified)
        if total_orders > 0:
            dpmo = (defect_count / total_orders) * 1_000_000
            # Simplified sigma calculation
            if dpmo > 0:
                sigma = max(0, 6 - (dpmo / 100_000))
            else:
                sigma = 6.0
        else:
            dpmo = 0
            sigma = 0.0
        
        return {
            "report_type": "Six Sigma Quality Assessment",
            "generated_by": "Patricia",
            "timestamp": datetime.now().isoformat(),
            "metrics": {
                "total_orders": total_orders,
                "active_orders": metrics['active_orders'],
                "avg_cycle_time_days": metrics['avg_cycle_time_days'],
                "defects_detected": defect_count,
                "dpmo": round(dpmo, 2),
                "sigma_level": round(sigma, 2),
                "target_sigma": 6.0,
                "improvement_gap": round(6.0 - sigma, 2)
            },
            "defects": defects,
            "recommendations": self._generate_recommendations(defects, metrics)
        }
    
    def _generate_recommendations(self, defects, metrics) -> list:
        """Generate improvement recommendations"""
        recommendations = []
        
        stalled_count = len([d for d in defects if d['type'] == 'STALLED_ORDER'])
        if stalled_count > 0:
            recommendations.append({
                "priority": "HIGH",
                "action": "Implement auto-advance for stalled orders",
                "impact": f"Clear {stalled_count} stalled orders",
                "owner": "Pipeline Automation"
            })
        
        urgent_count = len([d for d in defects if d['type'] == 'HIGH_PRIORITY_DELAY'])
        if urgent_count > 0:
            recommendations.append({
                "priority": "MEDIUM",
                "action": "Review high-priority queue processing",
                "impact": f"Accelerate {urgent_count} urgent orders",
                "owner": "Production Manager"
            })
        
        if metrics['avg_cycle_time_days'] > 7:
            recommendations.append({
                "priority": "MEDIUM",
                "action": "Conduct cycle time analysis",
                "impact": "Reduce average processing time",
                "owner": "Process Engineer"
            })
        
        return recommendations
    
    def update_factory_status(self) -> bool:
        """Patricia updates factory status with her analysis"""
        report = self.generate_six_sigma_report()
        
        # Save report
        report_path = Path("/root/.openclaw/workspace/agent_sandboxes/patricia/reports")
        report_path.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = report_path / f"factory_assessment_{timestamp}.json"
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"📊 Patricia's report saved: {report_file}")
        
        # Print summary
        print("\n" + "="*60)
        print("📋 PATRICIA'S SIX SIGMA FACTORY ASSESSMENT")
        print("="*60)
        print(f"Sigma Level: {report['metrics']['sigma_level']}/6.0")
        print(f"Defects: {report['metrics']['defects_detected']}")
        print(f"DPMO: {report['metrics']['dpmo']}")
        print(f"Active Orders: {report['metrics']['active_orders']}")
        print(f"Avg Cycle Time: {report['metrics']['avg_cycle_time_days']} days")
        print("\n📌 Top Recommendations:")
        for rec in report['recommendations'][:3]:
            print(f"  • [{rec['priority']}] {rec['action']}")
        print("="*60)
        
        return True
    
    def run_factory_tick(self):
        """Patricia runs one factory monitoring tick"""
        print("🔍 Patricia analyzing factory...")
        self.update_factory_status()
        print("✅ Factory tick complete\n")


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Patricia Factory Controller')
    parser.add_argument('command', choices=['status', 'analyze', 'report', 'tick'])
    args = parser.parse_args()
    
    controller = PatriciaFactoryController()
    
    if args.command == 'status':
        metrics = controller.get_factory_metrics()
        print(json.dumps(metrics, indent=2))
    
    elif args.command == 'analyze':
        defects = controller.analyze_for_defects()
        print(json.dumps(defects, indent=2))
    
    elif args.command == 'report':
        report = controller.generate_six_sigma_report()
        print(json.dumps(report, indent=2))
    
    elif args.command == 'tick':
        controller.run_factory_tick()


if __name__ == "__main__":
    main()
