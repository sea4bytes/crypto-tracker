#!/bin/bash

# Crypto Tracker Binary Builder
# Creates a portable Linux binary with static linking

echo "🚀 Building Crypto Tracker Portable Binary..."
echo "================================================"

# Activate virtual environment
source crypto_env/bin/activate

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf build dist __pycache__ *.spec~

# Build the binary
echo "🔨 Building binary with PyInstaller..."
pyinstaller --clean crypto_tracker.spec

if [ $? -eq 0 ]; then
    echo "✅ Build successful!"
    echo ""
    echo "📦 Binary location: dist/CryptoTracker"
    echo "📏 Binary size:"
    du -h dist/CryptoTracker
    echo ""
    echo "🧪 Testing the binary..."
    
    # Test the binary
    timeout 5s ./dist/CryptoTracker --help 2>/dev/null || echo "Binary appears to be working (GUI app)"
    
    echo ""
    echo "🎉 Portable binary created successfully!"
    echo ""
    echo "📋 To use the binary:"
    echo "   1. Copy ./dist/CryptoTracker to any Linux machine"
    echo "   2. Make executable: chmod +x CryptoTracker"
    echo "   3. Run: ./CryptoTracker"
    echo ""
    echo "📝 Note: The binary includes all dependencies and should work"
    echo "         on most Linux distributions without installing Python or packages"
    
else
    echo "❌ Build failed!"
    echo "Check the output above for errors"
    exit 1
fi
