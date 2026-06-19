#!/bin/bash
# Deploy N'og nog v3 to cloud servers

# Config
V3_DIR="/root/.openclaw/workspace/nognog/v3"
WEB_DIR="/var/www/nog"

# Check if running on server
if [[ "$HOSTNAME" == "myl0nr0s" ]] || [[ "$HOSTNAME" == "vps" ]]; then
    echo "Running on server..."
else
    echo "This script must run on the target server"
    echo "Or use: ssh root@myl0nr0s.cloud 'bash -s' < deploy_v3.sh"
    exit 1
fi

# Deploy
mkdir -p $WEB_DIR
cd $WEB_DIR

# Backup current
tar czf backup_$(date +%Y%m%d_%H%M%S).tar.gz . 2>/dev/null || true

# Copy v3 files
cp -r $V3_DIR/* $WEB_DIR/

# Set permissions
chown -R www-data:www-data $WEB_DIR
chmod -R 755 $WEB_DIR

echo "✅ N'og nog v3 deployed to $WEB_DIR"
echo "URL: http://myl0nr0s.cloud/nog"
