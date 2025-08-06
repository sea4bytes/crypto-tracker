# Changelog

All notable changes to the Crypto Currency Price Tracker will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- Future features will be listed here

### Changed
- Future changes will be listed here

### Fixed
- Future bug fixes will be listed here

## [1.0.0] - 2025-08-06

### Added
- ✨ **Premium UI/UX Design**: Modern interface with gradients and professional styling
- 📊 **Real-time Price Tracking**: Support for 17 popular cryptocurrencies including:
  - Bitcoin (BTC), Ethereum (ETH), Binance Coin (BNB), Cardano (ADA)
  - Solana (SOL), XRP, Dogecoin (DOGE), Monero (XMR), Tether (USDT)
  - Polygon (MATIC), Litecoin (LTC), Chainlink (LINK), Avalanche (AVAX)
  - TRON (TRX), Shiba Inu (SHIB), Uniswap (UNI), Toncoin (TON)
- 📈 **Market Overview Tab**: Live price table with 24h changes, market cap, and volume
- 📉 **Price History Tab**: Interactive charts with multiple timeframes (7d, 30d, 90d, 1y)
- 💱 **Exchange Fees Tab**: Real-time exchange rates from ChangeNOW.io
- 💰 **Custom Amount Calculator**: Enter specific amounts for exact exchange calculations
- 🎯 **AI Trading Suggestions Tab**: Smart buy/sell/hold recommendations
- ⚡ **Auto-refresh**: Automatic price updates every 60 seconds
- 🌙 **Enhanced Dark Theme**: Professional dark interface with gradients
- 🌐 **Proxy Support**: HTTP and SOCKS proxy configuration
- 🚀 **Portable Binary**: 83MB self-contained Linux executable
- 📦 **Multiple Distribution Formats**: Tarball, portable package, installer script

### Technical Features
- **CoinGecko API Integration**: Free cryptocurrency price data
- **ChangeNOW.io API Integration**: Real-time exchange rates and fees
- **PyQt5 Framework**: Modern desktop GUI with custom styling
- **Matplotlib Charts**: Interactive price history visualization
- **Threading**: Non-blocking API calls for responsive UI
- **Error Handling**: Robust network error handling and user feedback
- **Virtual Environment**: Clean dependency management

### AI Analysis Engine
- **Technical Indicators**: Price momentum and volume analysis
- **Market Analysis**: Oversold/overbought condition detection
- **Risk Assessment**: Confidence levels from 5% to 95%
- **Smart Logic**: Special handling for major cryptocurrencies and stablecoins
- **Color-coded Recommendations**: Visual buy/sell/hold indicators

### Build System
- **PyInstaller Integration**: Automated binary building
- **Static Linking**: Maximum compatibility across Linux distributions
- **Package Generation**: Multiple distribution formats
- **GitHub Actions**: Automated release pipeline

### Fixed
- 🔧 **XMR Availability**: Monero now appears in all tabs (Price History, Exchange Fees)
- 🔧 **Amount Input Field**: Exchange tab input field now fully functional
- 🔧 **Binary Dependencies**: PIL/matplotlib errors resolved in portable binary
- 🔧 **Market Analysis**: Fixed data type handling in AI analysis engine
- 🔧 **API Error Handling**: Improved network timeout and error recovery

### Known Issues
- Qt warnings for unsupported CSS properties (cosmetic, doesn't affect functionality)
- Wayland compatibility warnings (application works correctly)

### Requirements
- **For Binary**: Linux x64, graphics display, internet connection
- **For Source**: Python 3.7+, PyQt5, matplotlib, numpy==1.26.4, requests

### Distribution
- **Binary Size**: ~83MB (fully self-contained)
- **Supported Platforms**: Linux x64 distributions
- **Installation**: No dependencies required for binary version
- **License**: MIT License with GPL v3 compatibility for PyQt5

---

## Release Notes Format

### Version Categories
- **Major Release** (x.0.0): Significant new features, major UI changes
- **Minor Release** (x.y.0): New features, improvements, non-breaking changes  
- **Patch Release** (x.y.z): Bug fixes, security updates, minor improvements

### Change Categories
- **Added**: New features and capabilities
- **Changed**: Changes to existing functionality
- **Deprecated**: Features that will be removed in future versions
- **Removed**: Features removed in this version
- **Fixed**: Bug fixes and corrections
- **Security**: Security-related improvements and fixes
