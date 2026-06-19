#!/bin/bash
# CREAM Desktop Build Script for Windows .exe
# Builds using Tauri + React

set -e

echo "🍦 CREAM Desktop Build Script"
echo "=============================="

# Check dependencies
echo "Checking dependencies..."
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js 18+"
    exit 1
fi

if ! command -v cargo &> /dev/null; then
    echo "❌ Rust/Cargo not found. Installing..."
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
    source ~/.cargo/env
fi

# Install Tauri CLI if not present
if ! command -v tauri &> /dev/null; then
    echo "Installing Tauri CLI..."
    cargo install tauri-cli
fi

cd desktop

# Install dependencies
echo "Installing npm dependencies..."
npm install

# Build for Windows
echo "Building for Windows..."
npm run tauri build -- --target x86_64-pc-windows-msvc

echo "✅ Desktop build complete!"
echo "Output: src-tauri/target/release/CREAM PIM.exe"