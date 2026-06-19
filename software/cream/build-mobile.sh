#!/bin/bash
# CREAM Mobile Build Script for Android .apk
# Builds using React Native

set -e

echo "🍦 CREAM Mobile Build Script"
echo "============================"

# Check dependencies
echo "Checking dependencies..."
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js 18+"
    exit 1
fi

if ! command -v java &> /dev/null; then
    echo "❌ Java not found. Please install JDK 17+"
    exit 1
fi

cd mobile

# Install dependencies
echo "Installing npm dependencies..."
npm install

# Install Android dependencies
echo "Installing Android dependencies..."
cd android
./gradlew dependencies
cd ..

# Build Release APK
echo "Building Release APK..."
cd android
./gradlew assembleRelease

echo "✅ Mobile build complete!"
echo "Output: android/app/build/outputs/apk/release/app-release.apk"