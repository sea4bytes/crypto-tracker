# 🚀 Crypto Currency Price Tracker

![Release](https://img.shields.io/github/v/release/sea4bytes/crypto-tracker?style=for-the-badge&logo=github)
![Downloads](https://img.shields.io/github/downloads/sea4bytes/crypto-tracker/total?style=for-the-badge&logo=github)
![License](https://img.shields.io/github/license/sea4bytes/crypto-tracker?style=for-the-badge)
![Python](https://img.shields.io/badge/python-3.7+-blue?style=for-the-badge&logo=python)
![PyQt5](https://img.shields.io/badge/PyQt5-GUI-green?style=for-the-badge&logo=qt)

A **stunning modern PyQt5-based application** with premium UI/UX design for tracking cryptocurrency prices, viewing historical price charts, checking exchange fees, and getting AI-powered trading suggestions.

## ✨ Features

- **🎨 Premium UI/UX Design**: Gorgeous modern interface with gradients, animations, and professional styling
- **📊 Real-time Price Tracking**: View current prices of 17 popular cryptocurrencies
- **📈 Market Overview**: Beautiful price changes with color-coding, market cap, and trading volume
- **📉 Historical Charts**: Interactive price history for 7 days, 30 days, 90 days, or 1 year
- **💱 Exchange Fees**: Real-time exchange rates and fees from ChangeNOW.io
- **💰 Custom Amount Calculator**: Enter specific amounts to see exact exchange calculations
- **🎯 AI Trading Suggestions**: Smart analysis with buy/sell/hold recommendations
- **⚡ Auto-refresh**: Prices update automatically every 60 seconds
- **🌙 Enhanced Dark Theme**: Premium dark interface with gradients and modern styling
- **🌐 Proxy Support**: HTTP and SOCKS proxy support for network restrictions

## Supported Cryptocurrencies

- Bitcoin (BTC)
- Ethereum (ETH)
- Binance Coin (BNB)
- Cardano (ADA)
- Solana (SOL)
- XRP (XRP)
- Dogecoin (DOGE)
- **Monero (XMR)** ✨ *New*
- **Tether (USDT)** ✨ *New*
- Polygon (MATIC)
- Litecoin (LTC)
- Chainlink (LINK)
- Avalanche (AVAX)
- TRON (TRX)
- Shiba Inu (SHIB)
- Uniswap (UNI)
- Toncoin (TON)

## 🎮 Application Tabs

### 1. 📊 Market Overview
- **Premium price table** with all supported cryptocurrencies
- **Color-coded changes**: Green gains, red losses with beautiful gradients
- **Market data**: Market capitalization and trading volume
- **Live timestamps**: Real-time update indicators
- **Enhanced refresh**: Stylish manual refresh button

### 2. 📈 Price History  
- **Interactive charts** with professional styling
- **Multiple timeframes**: 7 days, 30 days, 90 days, 1 year
- **Beautiful chart design**: Dark theme with gradient backgrounds
- **Smart updates**: Automatic refresh when switching currencies or periods
- **All cryptocurrencies available** in dropdown menu

### 3. 💱 Exchange Fees ✨ *Enhanced*
- **Real-time rates** from ChangeNOW.io with premium UI
- **💰 Custom amount calculator** - enter specific amounts for exact calculations  
- **Fixed input field** - now fully functional and responsive
- **Minimum amounts** with smart validation
- **Fee information** with detailed breakdowns
- **All cryptocurrency pairs** supported
- **Intuitive design** with gradient buttons and improved styling

### 4. 🎯 Trade Suggestions ✨ *NEW*
- **AI-powered analysis** based on technical indicators
- **Smart recommendations**: Buy, Sell, or Hold with confidence levels
- **Price targets** with reasoning explanations
- **Market momentum** analysis with volume indicators
- **Risk assessment** for each cryptocurrency
- **Beautiful table display** with color-coded actions
- **Real-time updates** that sync with market data

## Installation & Usage

### 🚀 Method 1: Portable Binary (Recommended)
**No Python installation required!**

Download the portable binary:
```bash
# Download and extract (replace with actual download URL)
wget -O CryptoTracker-Portable-Linux.tar.gz [download_url]
tar -xzf CryptoTracker-Portable-Linux.tar.gz
cd CryptoTracker-Portable

# Run directly
./CryptoTracker
# OR
./run.sh
```

**Binary Features:**
- ✅ **83MB** fully self-contained executable  
- ✅ **No dependencies** - works on most Linux distributions
- ✅ **No Python required** - includes everything needed
- ✅ **Portable** - copy and run anywhere
- ✅ **Static linking** - maximum compatibility

### 🛠 Method 2: From Source

1. Install Python 3.7 or higher
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

**Run the application:**
```bash
python crypto_gui.py
```

Or use the startup script:
```bash
./start_crypto_tracker.sh
```

**Note**: If you get "python not found" error, use `python3` instead:
```bash
python3 crypto_gui.py
```

Or activate the virtual environment:
```bash
source crypto_env/bin/activate
python crypto_gui.py
```

### 📦 Method 3: System Installation
```bash
# Extract the portable package
tar -xzf CryptoTracker-Portable-Linux.tar.gz
cd CryptoTracker-Portable

# Run installer
./install.sh

# Then run from anywhere
CryptoTracker
```

### Exchange Fee Feature Usage:

1. **Go to Exchange Fees Tab**: Click on the "💱 Exchange Fees" tab
2. **Select Source Currency**: Choose the cryptocurrency you want to exchange from
3. **Select Target Currency**: Choose the cryptocurrency you want to exchange to  
4. **💰 Enter Custom Amount** ✨ *Fixed*: Enter a specific amount in the enhanced "Amount" field
5. **Get Exchange Rate**: Click the stylish "Get Exchange Fee" button
6. **View Results**: See minimum amounts, exchange rates, fees, and exact calculations in beautiful styling

### 🎯 Trading Suggestions Feature Usage ✨ *NEW*:

1. **Go to Trade Suggestions Tab**: Click on the "🎯 Trade Suggestions" tab
2. **Analyze Market**: Click "🔍 Analyze Market" for AI-powered analysis
3. **Review Suggestions**: See buy/sell/hold recommendations with confidence levels
4. **Check Reasoning**: Read detailed explanations for each suggestion
5. **View Price Targets**: See projected price targets based on technical analysis
6. **Color-coded Actions**: Green for BUY, Red for SELL, Yellow for HOLD

### 💡 AI Analysis Features:
- **Technical Indicators**: Price momentum, volume analysis, market cap considerations
- **Smart Logic**: Identifies oversold/overbought conditions and trend reversals  
- **Risk Assessment**: Confidence levels from 5% to 95% based on multiple factors
- **Major Crypto Recognition**: Special handling for BTC, ETH, and stablecoins
- **Real-time Updates**: Analysis syncs with latest market data

### Custom Amount Feature:
- **Leave empty**: See rates for the minimum exchange amount
- **Enter amount**: Get exact calculations for your specific amount  
- **Below minimum**: App will warn if your amount is below the minimum required
- **Real-time calculation**: Instantly see how much you'll receive for your exact amount
- **Enhanced UI**: Beautiful input field with focus effects and validation

### Example Exchange Fee Information:
- **Minimum Amount**: The smallest amount you can exchange
- **Exchange Rate**: How much you'll receive for 1 unit of source currency
- **Service Fee**: ChangeNOW's service fee (usually included in the rate)
- **Network Fee**: Blockchain network fees (variable)

## 🔧 Technical Details

- **🎨 Premium UI Framework**: Enhanced PyQt5 with custom gradients and modern styling
- **📡 CoinGecko API**: Real-time cryptocurrency prices and historical data
- **💱 ChangeNOW.io API**: Live exchange rates and fees
- **🤖 AI Analysis Engine**: Custom technical analysis algorithms
- **📊 Interactive Charts**: Matplotlib with dark theme integration
- **🌐 HTTP Client**: Requests library with threading for responsive UI
- **🔄 Auto-refresh**: Smart background updates every 60 seconds
- **💾 Virtual Environment**: Clean dependency management
- **🎭 Responsive Design**: Adaptive layouts for different screen sizes

## 🏗️ Building From Source

### Prerequisites
- Python 3.7+
- Virtual environment (recommended)

### Build Portable Binary
```bash
# Setup environment
python3 -m venv crypto_env
source crypto_env/bin/activate
pip install -r requirements.txt
pip install pyinstaller

# Build binary
./build_binary.sh

# Create distribution packages
./package_releases.sh
```

### Build Results
- **dist/CryptoTracker**: Single executable binary (~83MB)
- **packages/**: Various distribution formats
- **Fully static**: No external dependencies required

## 🚨 Known Issues & Fixes

### ✅ XMR Issue Fixed
- **Problem**: XMR (Monero) not appearing in History and Exchange tabs  
- **Solution**: Fixed in latest version - all 17 cryptocurrencies now appear in all tabs
- **Verification**: Check dropdown menus in Price History and Exchange Fees tabs

### ✅ Amount Input Fixed  
- **Problem**: Exchange tab amount field not accepting input
- **Solution**: Enhanced input field with proper focus and validation
- **Test**: Go to Exchange Fees → Enter amount like "0.5" → Should accept input

### ✅ Binary Dependencies Fixed
- **Problem**: PIL/matplotlib errors in portable binary
- **Solution**: Included all required modules in PyInstaller build
- **Result**: Binary now works on systems without Python/PIL installed

## API Sources

- **Price Data**: CoinGecko API (free, no API key required)
- **Exchange Data**: ChangeNOW.io API (free, no API key required)

## 📋 Changelog

See [CHANGELOG.md](CHANGELOG.md) for detailed version history and release notes.

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:
- Bug reports and feature requests
- Development setup and coding standards  
- Pull request process
- Code of conduct

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**Third-party License Notice**: This application uses PyQt5 which is licensed under GPL v3. The combination maintains GPL v3 compatibility.

## Environment Variables

You can set proxy using environment variables:
- `HTTP_PROXY` or `http_proxy`: Set HTTP proxy URL

## Requirements

- Python 3.7+
- PyQt5
- matplotlib
- numpy==1.26.4 (specific version for compatibility)
- requests

## Troubleshooting

- If you encounter network issues, try setting up a proxy
- For SOCKS proxy support, install: `pip install requests[socks]`
- If the application doesn't start, ensure all dependencies are installed
- Exchange rates are provided by ChangeNOW.io and may vary
- Always verify rates on the actual exchange platform before trading
