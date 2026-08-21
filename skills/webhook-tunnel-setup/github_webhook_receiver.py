#!/usr/bin/env python3
"""
GitHub Webhook Receiver — Miles Communication Pipe
Captain's Order: 2026-02-22 17:08 UTC

Receives GitHub push events from performance-supply-depot
Alerts immediately when Miles commits
"""

import os
import sys
import json
import hmac
import hashlib
import logging
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

# Configuration
WEBHOOK_PORT = 9001
WEBHOOK_SECRET = os.environ.get('GITHUB_WEBHOOK_SECRET', 'AOCROS-WEBHOOK-2025')
LOG_PATH = '/var/log/openclaw/webhook/'
MILES_REPO = 'performance-supply-depot'
NOTIFICATION_PIPE = '/root/.openclaw/workspace/pipes/webhook/notifications/'

# Ensure directories exist
Path(LOG_PATH).mkdir(parents=True, exist_ok=True)
Path(NOTIFICATION_PIPE).mkdir(parents=True, exist_ok=True)

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler(f'{LOG_PATH}webhook_receiver.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class WebhookHandler(BaseHTTPRequestHandler):
    """Handle incoming GitHub webhooks"""
    
    def log_message(self, format, *args):
        """Override to use our logger"""
        logger.info(f"{self.address_string()} - {format % args}")
    
    def do_POST(self):
        """Process webhook POST requests"""
        try:
            # Get headers
            event_type = self.headers.get('X-GitHub-Event', 'unknown')
            signature = self.headers.get('X-Hub-Signature-256', '')
            content_length = int(self.headers.get('Content-Length', 0))
            
            # Read payload
            payload = self.rfile.read(content_length)
            
            # Verify signature
            if not self._verify_signature(payload, signature):
                self._send_response(401, 'Unauthorized')
                logger.warning("Invalid webhook signature")
                return
            
            # Parse JSON
            data = json.loads(payload.decode('utf-8'))
            
            # Handle events
            if event_type == 'push':
                self._handle_push(data)
            elif event_type == 'ping':
                self._handle_ping(data)
            else:
                logger.info(f"Received event: {event_type}")
            
            self._send_response(200, 'OK')
            
        except Exception as e:
            logger.error(f"Error processing webhook: {e}")
            self._send_response(500, 'Internal Server Error')
    
    def _verify_signature(self, payload, signature):
        """Verify GitHub webhook signature"""
        if not signature:
            return False
        
        mac = hmac.new(
            WEBHOOK_SECRET.encode('utf-8'),
            payload,
            hashlib.sha256
        )
        expected = 'sha256=' + mac.hexdigest()
        return hmac.compare_digest(expected, signature)
    
    def _handle_push(self, data):
        """Process push event from GitHub"""
        repo_name = data.get('repository', {}).get('name', 'unknown')
        ref = data.get('ref', '')
        commits = data.get('commits', [])
        pusher = data.get('pusher', {}).get('name', 'unknown')
        
        # Only process Miles' repo
        if repo_name != MILES_REPO:
            logger.info(f"Ignoring push to {repo_name}")
            return
        
        # Only process main branch
        if 'main' not in ref and 'master' not in ref:
            logger.info(f"Ignoring push to {ref}")
            return
        
        logger.info(f"🚨 MILES COMMIT DETECTED — {len(commits)} commits")
        
        # Create notification
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        notification = {
            'timestamp': datetime.utcnow().isoformat(),
            'type': 'miles_commit',
            'repository': repo_name,
            'branch': ref,
            'pusher': pusher,
            'commit_count': len(commits),
            'commits': [
                {
                    'id': c.get('id', '')[:8],
                    'message': c.get('message', ''),
                    'author': c.get('author', {}).get('name', 'unknown'),
                    'files': c.get('added', []) + c.get('modified', []) + c.get('removed', [])
                }
                for c in commits
            ]
        }
        
        # Write notification
        notification_file = f"{NOTIFICATION_PIPE}miles_{timestamp}.json"
        with open(notification_file, 'w') as f:
            json.dump(notification, f, indent=2)
        
        # Write urgent alert for immediate display
        alert_file = f"{NOTIFICATION_PIPE}ALERT_MILES_ACTIVE"
        with open(alert_file, 'w') as f:
            f.write(f"""MILES COMMIT — {datetime.utcnow().strftime('%H:%M:%S')} UTC
Repository: {repo_name}
Commits: {len(commits)}
Latest: {commits[0].get('message', 'N/A') if commits else 'N/A'}
Author: {commits[0].get('author', {}).get('name', 'unknown') if commits else 'unknown'}

File: {notification_file}
""")
        
        # Also log to webhook log
        with open(f"{LOG_PATH}miles_commits.log", 'a') as f:
            f.write(f"{datetime.utcnow().isoformat()} | {len(commits)} commits | {commits[0].get('message', 'N/A')[:50] if commits else 'N/A'}\n")
        
        logger.info(f"✅ Notification written to {notification_file}")
    
    def _handle_ping(self, data):
        """Handle GitHub ping event"""
        logger.info("Received ping from GitHub — webhook configured correctly")
    
    def _send_response(self, code, message):
        """Send HTTP response"""
        self.send_response(code)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write(message.encode())


def create_systemd_service():
    """Generate systemd service file for auto-start"""
    service_content = '''[Unit]
Description=OpenClaw GitHub Webhook Receiver
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/.openclaw/workspace/pipes/webhook
ExecStart=/usr/bin/python3 /root/.openclaw/workspace/pipes/webhook/github_webhook_receiver.py
Restart=always
RestartSec=5
Environment="GITHUB_WEBHOOK_SECRET=AOCROS-WEBHOOK-2025"

[Install]
WantedBy=multi-user.target
'''
    
    service_path = '/etc/systemd/system/openclaw-webhook.service'
    with open(service_path, 'w') as f:
        f.write(service_content)
    
    print(f"Systemd service created: {service_path}")
    print("Run: systemctl enable --now openclaw-webhook")


def main():
    """Start webhook receiver"""
    if len(sys.argv) > 1 and sys.argv[1] == 'install':
        create_systemd_service()
        return
    
    server = HTTPServer(('0.0.0.0', WEBHOOK_PORT), WebhookHandler)
    logger.info(f"🚀 Webhook receiver started on port {WEBHOOK_PORT}")
    logger.info(f"📝 Logging to {LOG_PATH}")
    logger.info(f"🔔 Notifications written to {NOTIFICATION_PIPE}")
    logger.info(f"🎯 Monitoring repo: {MILES_REPO}")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("Shutting down...")
        server.shutdown()


if __name__ == '__main__':
    main()
