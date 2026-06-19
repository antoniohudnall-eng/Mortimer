#!/bin/bash
# build.sh — Build NetProbe DroidScript app
# Usage: ./build.sh

set -e

echo "🔧 Building NetProbe DroidScript Application..."
echo ""

# Check if we're in the right directory
if [ ! -f "NetProbe/Main.js" ]; then
    echo "❌ Error: Must run from /projects/netprobe-droidscript/"
    exit 1
fi

# Create distribution directory
mkdir -p dist

# Copy all files to dist
cp -r NetProbe dist/
cp README.md dist/

# Create zip file
ZIP_NAME="NetProbe-${VERSION:-1.0.0-OMEGA}.zip"
echo "📦 Creating $ZIP_NAME..."
cd dist
zip -r "../$ZIP_NAME" NetProbe/ README.md
cd ..

echo ""
echo "✅ Build complete!"
echo ""
echo "📱 Installation:"
echo "  1. Install DroidScript (Play Store)"
echo "  2. Copy $ZIP_NAME to Android device"
echo "  3. Extract to /sdcard/DroidScript/NetProbe/"
echo "  4. Launch NetProbe in DroidScript app"
echo ""
echo "🎉 NetProbe ready for deployment!"
