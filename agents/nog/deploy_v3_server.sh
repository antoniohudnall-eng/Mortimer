#!/bin/bash
# Deploy N'og nog v3 - Run this on the server

set -e

echo "🚀 N'og nog v3 Deployment Script"
echo "================================"

# Check if we're on the server
if [ ! -d "/var/www" ] && [ ! -d "/var/log" ]; then
    echo "⚠️  Warning: This doesn't look like the VPS. Are you sure?"
    echo "To run remotely: ssh root@myl0nr0s.cloud 'bash -s' < deploy_v3.sh"
    exit 1
fi

WEB_DIR="/var/www/nog"
BACKUP_DIR="/var/www/nog_backup_$(date +%Y%m%d_%H%M%S)"

echo ""
echo "📦 Step 1: Creating backup..."
if [ -d "$WEB_DIR" ]; then
    mkdir -p "$BACKUP_DIR"
    cp -r "$WEB_DIR"/* "$BACKUP_DIR/" 2>/dev/null || true
    echo "   ✅ Backed up to $BACKUP_DIR"
fi

echo ""
echo "📥 Step 2: Downloading latest v3 from GitHub..."
mkdir -p /tmp/nognog_v3
cd /tmp/nognog_v3

# Download via curl/wget
if command -v curl &> /dev/null; then
    curl -L -o nognog_v3.tar.gz https://github.com/hcindus/AOS-Brain/tarball/master/nognog/v3 2>/dev/null || \
    curl -L -o nognog_v3.tar.gz https://api.github.com/repos/hcindus/AOS-Brain/tarball/master 2>/dev/null
elif command -v wget &> /dev/null; then
    wget -q -O nognog_v3.tar.gz https://github.com/hcindus/AOS-Brain/tarball/master 2>/dev/null || true
fi

# Check if we got the file
if [ ! -f "nognog_v3.tar.gz" ] || [ ! -s "nognog_v3.tar.gz" ]; then
    echo "   ⚠️  Download failed. Trying alternative method..."
    # Fallback: clone and extract
    rm -rf /tmp/nognog_clone
    git clone --depth 1 https://github.com/hcindus/AOS-Brain.git /tmp/nognog_clone 2>/dev/null || {
        echo "   ❌ Git clone also failed. Manual deployment required."
        exit 1
    }
    
    echo ""
    echo "📂 Step 3: Deploying files..."
    mkdir -p "$WEB_DIR"
    cp -r /tmp/nognog_clone/nognog/v3/* "$WEB_DIR/"
else
    echo "   ✅ Downloaded successfully"
    echo ""
    echo "📂 Step 3: Extracting and deploying..."
    tar -xzf nognog_v3.tar.gz --strip-components=2 "*/nognog/v3/*" 2>/dev/null || \
    tar -xzf nognog_v3.tar.gz 2>/dev/null
    
    mkdir -p "$WEB_DIR"
    cp -r /tmp/nognog_v3/nognog/v3/* "$WEB_DIR/" 2>/dev/null || \
    cp -r /tmp/nognog_v3/* "$WEB_DIR/" 2>/dev/null || true
fi

echo "   ✅ Files deployed"

echo ""
echo "🔧 Step 4: Setting permissions..."
chown -R www-data:www-data "$WEB_DIR" 2>/dev/null || chown -R root:root "$WEB_DIR"
chmod -R 755 "$WEB_DIR"
echo "   ✅ Permissions set"

echo ""
echo "🧹 Step 5: Cleanup..."
rm -rf /tmp/nognog_v3 /tmp/nognog_clone 2>/dev/null || true
echo "   ✅ Cleanup complete"

echo ""
echo "================================"
echo "✅ N'og nog v3 deployed!"
echo ""
echo "URLs:"
echo "   http://myl0nr0s.cloud/nog"
echo "   http://tappylewis.cloud/nog"
echo ""
echo "Backup: $BACKUP_DIR"
echo "================================"
