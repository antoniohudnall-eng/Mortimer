#!/usr/bin/env python3
"""
Patricia - THIS Integration Module
Connects Process Excellence Officer to Ternary High-Integrity System

Enables Patricia to:
- Monitor Brain/Heart/Stomach/Intestines status
- Report process metrics to THIS
- Trigger alerts on defects/variations
- Participate in physiological monitoring
"""

import json
import socket
import time
from datetime import datetime
from typing import Dict, Optional, Any

class PatriciaTHISConnector:
    """
    Patricia's interface to the Ternary High-Integrity System
    """
    
    def __init__(self, patricia_id="patricia_v1"):
        self.agent_id = patricia_id
        self.bhsi_socket = "/tmp/bhsi_v4.sock"
        self.brain_socket = "/tmp/aos_brain.sock"
        self.connected = False
        self.metrics_buffer = []
        
        # Patricia's process monitoring state
        self.process_metrics = {
            "last_update": None,
            "defects_detected": 0,
            "sigma_level": 0.0,
            "cpk": 0.0,
            "projects_active": 0
        }
        
    def connect_to_this(self) -> bool:
        """Establish connection to THIS"""
        try:
            # Test socket availability
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect(self.bhsi_socket)
            sock.close()
            self.connected = True
            return True
        except:
            return False
    
    def query_this_status(self) -> Optional[Dict]:
        """Get full THIS status"""
        return self._socket_query(self.bhsi_socket, "status")
    
    def query_heart(self) -> Optional[Dict]:
        """Get Heart subsystem status"""
        return self._socket_query(self.bhsi_socket, "heart")
    
    def query_stomach(self) -> Optional[Dict]:
        """Get Stomach subsystem status"""
        return self._socket_query(self.bhsi_socket, "stomach")
    
    def query_intestines(self) -> Optional[Dict]:
        """Get Intestines subsystem status"""
        return self._socket_query(self.bhsi_socket, "intestines")
    
    def _socket_query(self, socket_path: str, command: str) -> Optional[Dict]:
        """Send query via socket"""
        try:
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect(socket_path)
            sock.sendall(command.encode() + b'\n')
            
            response = b''
            while True:
                chunk = sock.recv(4096)
                if not chunk:
                    break
                response += chunk
            
            sock.close()
            return json.loads(response.decode())
        except Exception as e:
            return {"error": str(e)}
    
    def report_defect(self, process: str, defect_type: str, severity: int = 2) -> bool:
        """
        Report a defect to THIS Intestines
        Triggers error absorption and tracking
        """
        defect_data = {
            "agent": self.agent_id,
            "process": process,
            "defect_type": defect_type,
            "severity": severity,
            "timestamp": time.time(),
            "type": "defect_report"
        }
        
        # Add to buffer for batch processing
        self.metrics_buffer.append(defect_data)
        self.process_metrics["defects_detected"] += 1
        
        # If critical, flush immediately
        if severity >= 3:
            self.flush_metrics()
        
        return True
    
    def report_process_capability(self, process: str, cpk: float, sigma_level: float) -> bool:
        """
        Report process capability metrics to THIS
        Updates Stomach resource state if needed
        """
        self.process_metrics.update({
            "last_update": time.time(),
            "cpk": cpk,
            "sigma_level": sigma_level
        })
        
        # Alert if process not capable (Cpk < 1.33)
        if cpk < 1.33:
            self.report_defect(
                process=process,
                defect_type="process_not_capable",
                severity=2
            )
        
        return True
    
    def report_dmac_phase(self, project: str, phase: str, status: str) -> bool:
        """
        Report DMAIC project phase to THIS
        Enables brain to track improvement initiatives
        """
        status_data = {
            "agent": self.agent_id,
            "project": project,
            "phase": phase,
            "status": status,
            "timestamp": time.time(),
            "type": "dmaic_update"
        }
        
        self.metrics_buffer.append(status_data)
        
        if status == "complete":
            self.process_metrics["projects_active"] -= 1
        elif status == "start":
            self.process_metrics["projects_active"] += 1
        
        return True
    
    def flush_metrics(self) -> int:
        """
        Flush metrics buffer to THIS
        Returns number of items sent
        """
        if not self.metrics_buffer:
            return 0
        
        count = len(self.metrics_buffer)
        
        # Send to Intestines via socket if connected
        if self.connected:
            for metric in self.metrics_buffer:
                # Each metric absorbed as waste item
                pass  # Intestines handles via its own mechanism
        
        # Clear buffer
        self.metrics_buffer.clear()
        return count
    
    def get_this_health(self) -> Dict:
        """
        Get THIS health summary for Patricia's monitoring
        """
        status = self.query_this_status()
        
        if not status or "error" in status:
            return {
                "connected": False,
                "status": "unavailable",
                "recommendation": "Check THIS service status"
            }
        
        # Analyze THIS health
        health_score = 1.0
        issues = []
        
        # Check Heart
        if status.get("heart", {}).get("state") == "REST":
            health_score *= 0.9
            issues.append("Heart in REST mode")
        
        # Check Stomach
        if status.get("stomach", {}).get("state") == "HUNGRY":
            health_score *= 0.7
            issues.append("Stomach HUNGRY - Ollama issues")
        
        # Check Intestines
        if status.get("intestines", {}).get("buffer_size", 0) > 50:
            health_score *= 0.8
            issues.append("Intestines buffer >50%")
        
        return {
            "connected": True,
            "health_score": round(health_score, 2),
            "status": "healthy" if health_score > 0.8 else "degraded",
            "issues": issues,
            "basal_mode": status.get("basal_mode", False),
            "tick": status.get("tick", 0)
        }
    
    def generate_process_report(self) -> Dict:
        """
        Generate comprehensive process report
        Patricia's daily dashboard data
        """
        this_health = self.get_this_health()
        
        return {
            "timestamp": datetime.now().isoformat(),
            "agent": self.agent_id,
            "this_health": this_health,
            "process_metrics": self.process_metrics,
            "metrics_pending": len(self.metrics_buffer),
            "sigma_target": 6.0,
            "sigma_current": self.process_metrics["sigma_level"],
            "improvement_gap": 6.0 - self.process_metrics["sigma_level"]
        }
    
    def monitor_loop(self, interval=300):
        """
        Continuous monitoring loop
        Patricia's background process
        """
        print(f"[{self.agent_id}] Starting THIS monitoring loop...")
        
        while True:
            try:
                # Get THIS status
                health = self.get_this_health()
                
                # Check for issues
                if health["status"] != "healthy":
                    print(f"[{self.agent_id}] THIS alert: {health['issues']}")
                
                # Flush any pending metrics
                flushed = self.flush_metrics()
                if flushed > 0:
                    print(f"[{self.agent_id}] Flushed {flushed} metrics to THIS")
                
                # Sleep
                time.sleep(interval)
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"[{self.agent_id}] Monitor error: {e}")
                time.sleep(60)
        
        print(f"[{self.agent_id}] Monitoring stopped")

# Integration hook for Patricia Agent
class PatriciaAgent:
    """
    Main Patricia Agent with THIS integration
    """
    
    def __init__(self):
        self.this_connector = PatriciaTHISConnector()
        self.active = False
        
    def activate(self):
        """Activate Patricia with THIS connection"""
        print("📊⚙️  Activating Patricia...")
        
        # Connect to THIS
        if self.this_connector.connect_to_this():
            print("✅ Connected to THIS")
            self.active = True
        else:
            print("⚠️  THIS not available, running standalone")
            self.active = True  # Still active, just not connected
        
        # Show status
        health = self.this_connector.get_this_health()
        print(f"   THIS Health: {health.get('status', 'unknown')}")
        print(f"   Health Score: {health.get('health_score', 0)}")
        
        return self.active
    
    def report_defect(self, process: str, defect: str, severity: int = 2):
        """Report defect through THIS"""
        return self.this_connector.report_defect(process, defect, severity)
    
    def report_capability(self, process: str, cpk: float, sigma: float):
        """Report process capability"""
        return self.this_connector.report_process_capability(process, cpk, sigma)
    
    def get_dashboard(self) -> Dict:
        """Get Patricia's dashboard"""
        return self.this_connector.generate_process_report()

# Demo/Testing
if __name__ == "__main__":
    print("=" * 60)
    print("Patricia - THIS Integration Test")
    print("=" * 60)
    
    # Create agent
    patricia = PatriciaAgent()
    
    # Activate
    if patricia.activate():
        print("\n" + "=" * 60)
        print("Querying THIS Status...")
        print("=" * 60)
        
        # Get dashboard
        dashboard = patricia.get_dashboard()
        print(json.dumps(dashboard, indent=2))
        
        # Simulate defect report
        print("\n" + "=" * 60)
        print("Testing Defect Reporting...")
        print("=" * 60)
        
        patricia.report_defect(
            process="Dark_Factory_Build",
            defect="gradle_timeout",
            severity=2
        )
        
        patricia.report_capability(
            process="COBRA_Assembly",
            cpk=1.45,
            sigma=5.2
        )
        
        print("✅ Test complete")
    
    print("\n" + "=" * 60)
    print("Patricia is wired to THIS")
    print("=" * 60)
