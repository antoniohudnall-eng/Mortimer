#!/bin/bash
# Deploy dashboard to web server
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Copy to workspace public
mkdir -p /root/.openclaw/workspace/public
cp "$SCRIPT_DIR/dashboard.html" /root/.openclaw/workspace/public/dashboard.html
echo "✅ Dashboard copied to workspace/public"

# Copy to nginx if available
if [ -d "/var/www/html" ]; then
    cp "$SCRIPT_DIR/dashboard.html" /var/www/html/dashboard.html
    echo "✅ Dashboard deployed to /var/www/html/dashboard.html"
fi

# Start Python HTTP server if not running
if ! pgrep -f "python3 -m http.server 8080" > /dev/null; then
    cd /root/.openclaw/workspace/public
    nohup python3 -m http.server 8080 > /tmp/public_server.log 2>&1 &
    echo "✅ HTTP server started on port 8080"
fi

echo ""
echo "🚀 Dashboard accessible at:"
echo "  http://$(hostname -I | awk '{print $1}'):8080/dashboard.html"
echo "  http://localhost:8080/dashboard.html"
