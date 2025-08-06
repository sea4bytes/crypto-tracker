#!/bin/bash

# Advanced Binary Packaging Script
# Creates multiple distribution formats

echo "🚀 Advanced Crypto Tracker Binary Packaging"
echo "============================================"

# Check if we have the binary
if [ ! -f "dist/CryptoTracker" ]; then
    echo "❌ Binary not found! Run ./build_binary.sh first"
    exit 1
fi

# Create distribution directory
echo "📁 Creating distribution packages..."
mkdir -p packages

# 1. Create standalone tarball
echo "📦 Creating standalone tarball..."
cd dist
tar -czf ../packages/CryptoTracker-portable-linux-x64.tar.gz CryptoTracker
cd ..

# 2. Create AppImage-like structure (simpler version)
echo "📱 Creating portable app structure..."
mkdir -p packages/CryptoTracker-Portable
cp dist/CryptoTracker packages/CryptoTracker-Portable/
cat > packages/CryptoTracker-Portable/run.sh << 'EOF'
#!/bin/bash
# Crypto Tracker Portable Launcher
cd "$(dirname "$0")"
./CryptoTracker
EOF
chmod +x packages/CryptoTracker-Portable/run.sh

cat > packages/CryptoTracker-Portable/README.txt << 'EOF'
🚀 Crypto Currency Price Tracker - Portable Version

This is a portable version that runs on most Linux distributions without
requiring Python, PyQt5, or any other dependencies to be installed.

HOW TO RUN:
1. Extract this folder to any location
2. Open terminal in this folder
3. Run: ./run.sh
   OR directly: ./CryptoTracker

FEATURES:
- Real-time cryptocurrency price tracking
- Historical price charts
- Exchange fee calculator
- AI-powered trading suggestions
- Premium dark theme with modern UI

REQUIREMENTS:
- Linux x64 system
- Graphics display (X11 or Wayland)
- Internet connection for data

DISTRIBUTION:
- Binary size: ~83MB
- Fully self-contained
- No installation required
- Works offline for UI (data requires internet)

For support and updates, visit the project repository.
EOF

# 3. Create installer script
echo "🔧 Creating installer script..."
cat > packages/install.sh << 'EOF'
#!/bin/bash
# Crypto Tracker Installer

echo "🚀 Installing Crypto Currency Price Tracker..."

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   echo "⚠️  Don't run as root. Installing to user directory."
   exit 1
fi

# Create directories
INSTALL_DIR="$HOME/.local/bin"
DESKTOP_DIR="$HOME/.local/share/applications"

mkdir -p "$INSTALL_DIR"
mkdir -p "$DESKTOP_DIR"

# Copy binary
if [ -f "CryptoTracker" ]; then
    cp CryptoTracker "$INSTALL_DIR/"
    chmod +x "$INSTALL_DIR/CryptoTracker"
    echo "✅ Binary installed to $INSTALL_DIR"
else
    echo "❌ CryptoTracker binary not found!"
    exit 1
fi

# Create desktop entry
cat > "$DESKTOP_DIR/crypto-tracker.desktop" << DESKTOP_EOF
[Desktop Entry]
Name=Crypto Tracker
Comment=Cryptocurrency Price Tracker with AI Analysis
Exec=$INSTALL_DIR/CryptoTracker
Icon=applications-office
Terminal=false
Type=Application
Categories=Office;Finance;
DESKTOP_EOF

echo "✅ Desktop entry created"

# Add to PATH if not already there
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo "📝 Adding $HOME/.local/bin to PATH..."
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
    echo "⚠️  Restart terminal or run: source ~/.bashrc"
fi

echo ""
echo "🎉 Installation complete!"
echo "Run 'CryptoTracker' from terminal or find it in applications menu"
EOF

chmod +x packages/install.sh

# 4. Create the portable package
echo "📦 Creating final portable package..."
cd packages/CryptoTracker-Portable
tar -czf ../CryptoTracker-Portable-Linux.tar.gz .
cd ../..

# Show results
echo ""
echo "✅ Packaging complete!"
echo ""
echo "📋 Available packages:"
echo "  1. packages/CryptoTracker-portable-linux-x64.tar.gz (Binary only)"
echo "  2. packages/CryptoTracker-Portable-Linux.tar.gz (Full portable package)"
echo "  3. packages/CryptoTracker-Portable/ (Folder for direct use)"
echo "  4. packages/install.sh (System installer script)"
echo ""
echo "📏 Package sizes:"
ls -lh packages/*.tar.gz packages/*.sh 2>/dev/null | awk '{print "  " $9 ": " $5}'
echo ""
echo "🚀 Distribution ready!"
