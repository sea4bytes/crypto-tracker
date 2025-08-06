import sys
import requests
import threading
import os
import datetime
import json
import time
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, 
    QPushButton, QListWidget, QMessageBox, QComboBox, QSizePolicy, QSpacerItem,
    QTableWidget, QTableWidgetItem, QTabWidget, QGridLayout
)
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QColor, QPalette
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
plt.style.use('dark_background')


class CryptoPriceWidget(QWidget):
    update_status_signal = pyqtSignal(str)
    update_price_signal = pyqtSignal(float)
    update_table_signal = pyqtSignal(dict)
    update_chart_signal = pyqtSignal(list, list, str, str)
    update_exchange_signal = pyqtSignal(str, str, dict)
    update_suggestions_signal = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.session = requests.Session()
        self.setup_data()
        self.setup_ui()
        self.setup_connections()
        self.load_initial_settings()
        self.populate_combo()
        
        # Auto-refresh every 60 seconds
        self.auto_refresh_timer = QTimer()
        self.auto_refresh_timer.timeout.connect(self.refresh_all_prices)
        self.auto_refresh_timer.start(60000)  # 60 seconds

    def setup_ui(self):
        self.setWindowTitle('Crypto Currency Price Tracker')
        self.setGeometry(100, 100, 1200, 800)
        self.setMinimumSize(900, 600)

        # Set dark theme
        self.apply_dark_theme()

        # Main layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Title
        title = QLabel('🚀 Crypto Currency Price Tracker')
        title.setFont(QFont('Arial', 28, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet('''
            color: #ffffff; 
            margin: 20px;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #00ff99, stop:0.5 #00cc77, stop:1 #00aa55);
            border: 3px solid #ffffff;
            border-radius: 15px;
            padding: 20px;
        ''')
        self.layout.addWidget(title)

        # Configuration section
        self.setup_config_ui()

        # Tab widget for different views
        self.tab_widget = QTabWidget()
        self.layout.addWidget(self.tab_widget)
        
        # Overview tab
        self.overview_tab = QWidget()
        self.tab_widget.addTab(self.overview_tab, "📊 Market Overview")
        self.setup_overview_tab()
        
        # Chart tab
        self.chart_tab = QWidget()
        self.tab_widget.addTab(self.chart_tab, "📈 Price History")
        self.setup_chart_tab()
        
        # Exchange tab
        self.exchange_tab = QWidget()
        self.tab_widget.addTab(self.exchange_tab, "💱 Exchange Fees")
        self.setup_exchange_tab()
        
        # Suggestions tab
        self.suggestions_tab = QWidget()
        self.tab_widget.addTab(self.suggestions_tab, "🎯 Trade Suggestions")
        self.setup_suggestions_tab()

        # Status
        self.status_label = QLabel('Initializing...')
        self.status_label.setFont(QFont('Arial', 12))
        self.status_label.setStyleSheet('color: #ffb347; padding: 5px;')
        self.layout.addWidget(self.status_label)

    def apply_dark_theme(self):
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(18, 18, 18))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(22, 22, 22))
        dark_palette.setColor(QPalette.AlternateBase, QColor(40, 44, 52))
        dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(40, 44, 52))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Highlight, QColor(0, 255, 153))
        dark_palette.setColor(QPalette.HighlightedText, Qt.black)
        self.setPalette(dark_palette)

        # Enhanced modern dark theme with gradients and improved styling
        self.setStyleSheet('''
            QWidget { 
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #121212, stop:1 #1a1a1a);
                color: #ffffff; 
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            
            QTabWidget::pane { 
                border: 2px solid #00ff99; 
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1e1e1e, stop:1 #2a2a2a);
                border-radius: 8px;
                margin-top: 10px;
            }
            
            QTabBar::tab { 
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #3a3a3a, stop:1 #2a2a2a);
                color: #ffffff; 
                padding: 12px 20px; 
                margin-right: 3px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                border: 1px solid #444;
                font-weight: bold;
                min-width: 120px;
            }
            
            QTabBar::tab:selected { 
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #00ff99, stop:1 #00cc77);
                color: #000000;
                border: 2px solid #00ff99;
                margin-top: -2px;
            }
            
            QTabBar::tab:hover:!selected { 
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #4a4a4a, stop:1 #3a3a3a);
                border: 1px solid #00ff99;
            }
            
            QTableWidget { 
                gridline-color: #333; 
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1e1e1e, stop:1 #2a2a2a);
                border: 1px solid #444;
                border-radius: 6px;
                selection-background-color: #00ff99;
                selection-color: #000000;
            }
            
            QTableWidget::item { 
                padding: 12px; 
                border-bottom: 1px solid #333;
                border-right: 1px solid #333;
            }
            
            QTableWidget::item:selected { 
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00ff99, stop:1 #00cc77);
                color: #000000;
                font-weight: bold;
            }
            
            QHeaderView::section { 
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #404040, stop:1 #2a2a2a);
                color: #00ff99; 
                padding: 12px; 
                border: 1px solid #555;
                font-weight: bold;
                font-size: 12px;
            }
            
            QPushButton { 
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #404040, stop:1 #2a2a2a);
                color: #ffffff; 
                border: 2px solid #00ff99; 
                padding: 10px 20px; 
                border-radius: 8px;
                font-weight: bold;
                font-size: 13px;
            }
            
            QPushButton:hover { 
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #00ff99, stop:1 #00cc77);
                color: #000000;
                border: 2px solid #ffffff;
            }
            
            QPushButton:pressed { 
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #00cc77, stop:1 #00aa55);
                color: #000000;
                padding: 11px 19px;
            }
            
            QLineEdit { 
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #2a2a2a, stop:1 #1e1e1e);
                border: 2px solid #444; 
                padding: 10px; 
                border-radius: 8px;
                color: #ffffff;
                font-size: 13px;
            }
            
            QLineEdit:focus {
                border: 2px solid #00ff99;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1e1e1e, stop:1 #2a2a2a);
            }
            
            QComboBox { 
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #2a2a2a, stop:1 #1e1e1e);
                border: 2px solid #444; 
                padding: 10px; 
                border-radius: 8px;
                color: #ffffff;
                font-size: 13px;
                min-width: 150px;
            }
            
            QComboBox:focus {
                border: 2px solid #00ff99;
            }
            
            QComboBox::drop-down { 
                border: none; 
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00ff99, stop:1 #00cc77);
                border-top-right-radius: 6px;
                border-bottom-right-radius: 6px;
                width: 30px;
            }
            
            QComboBox::down-arrow { 
                image: none; 
                border: none;
                width: 0;
                height: 0;
                border-left: 6px solid transparent;
                border-right: 6px solid transparent;
                border-top: 8px solid #000000;
                margin: 4px;
            }
            
            QComboBox QAbstractItemView {
                background: #2a2a2a;
                border: 2px solid #00ff99;
                selection-background-color: #00ff99;
                selection-color: #000000;
                border-radius: 4px;
            }
            
            QLabel {
                color: #ffffff;
                font-size: 13px;
            }
            
            /* Scrollbar styling */
            QScrollBar:vertical {
                background: #1e1e1e;
                width: 12px;
                border-radius: 6px;
            }
            
            QScrollBar::handle:vertical {
                background: #00ff99;
                border-radius: 6px;
                min-height: 20px;
            }
            
            QScrollBar::handle:vertical:hover {
                background: #00cc77;
            }
        ''')

    def setup_config_ui(self):
        config_widget = QWidget()
        config_layout = QVBoxLayout()
        config_widget.setLayout(config_layout)
        
        # Proxy configuration
        proxy_layout = QHBoxLayout()
        proxy_label = QLabel('Proxy:')
        proxy_label.setFixedWidth(60)
        self.proxy_input = QLineEdit()
        self.proxy_input.setPlaceholderText('http://host:port or socks5h://host:port')
        self.proxy_button = QPushButton('Set Proxy')
        self.proxy_button.setFixedWidth(100)
        
        proxy_layout.addWidget(proxy_label)
        proxy_layout.addWidget(self.proxy_input)
        proxy_layout.addWidget(self.proxy_button)
        
        config_layout.addLayout(proxy_layout)
        self.layout.addWidget(config_widget)

    def setup_overview_tab(self):
        layout = QVBoxLayout()
        self.overview_tab.setLayout(layout)
        
        # Refresh button
        refresh_layout = QHBoxLayout()
        self.refresh_button = QPushButton('Refresh All Prices')
        self.refresh_button.setFixedWidth(200)
        refresh_layout.addWidget(self.refresh_button)
        refresh_layout.addStretch()
        layout.addLayout(refresh_layout)
        
        # Price table
        self.price_table = QTableWidget()
        self.price_table.setColumnCount(7)
        self.price_table.setHorizontalHeaderLabels([
            'Symbol', 'Name', 'Price (USD)', '24h Change (%)', 
            'Market Cap', '24h Volume', 'Last Updated'
        ])
        
        # Make table responsive
        header = self.price_table.horizontalHeader()
        header.setStretchLastSection(True)
        for i in range(6):
            header.setSectionResizeMode(i, header.Stretch if i < 2 else header.ResizeToContents)
        
        layout.addWidget(self.price_table)

    def setup_chart_tab(self):
        layout = QVBoxLayout()
        self.chart_tab.setLayout(layout)
        
        # Controls
        controls_layout = QHBoxLayout()
        
        coin_label = QLabel('Select Cryptocurrency:')
        controls_layout.addWidget(coin_label)
        
        self.combo = QComboBox()
        self.combo.setMinimumWidth(200)
        controls_layout.addWidget(self.combo)
        
        self.period_combo = QComboBox()
        self.period_combo.addItems(['7 days', '30 days', '90 days', '1 year'])
        self.period_combo.setCurrentText('30 days')
        controls_layout.addWidget(self.period_combo)
        
        controls_layout.addStretch()
        
        self.price_label = QLabel('Current Price: $0.00')
        self.price_label.setFont(QFont('Arial', 16, QFont.Bold))
        self.price_label.setStyleSheet('color: #00ff99;')
        controls_layout.addWidget(self.price_label)
        
        layout.addLayout(controls_layout)
        
        # Chart
        self.figure = Figure(figsize=(12, 6), facecolor='#1e1e1e')
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_facecolor('#2d2d2d')
        layout.addWidget(self.canvas)

    def setup_exchange_tab(self):
        layout = QVBoxLayout()
        self.exchange_tab.setLayout(layout)
        
        # Title
        exchange_title = QLabel('Exchange Fees (ChangeNOW.io)')
        exchange_title.setFont(QFont('Arial', 18, QFont.Bold))
        exchange_title.setAlignment(Qt.AlignCenter)
        exchange_title.setStyleSheet('color: #00ff99; margin: 10px;')
        layout.addWidget(exchange_title)
        
        # Exchange controls
        controls_layout = QVBoxLayout()
        
        # First row: From and To currency selection
        currency_layout = QHBoxLayout()
        
        # From currency
        from_label = QLabel('From:')
        currency_layout.addWidget(from_label)
        
        self.from_combo = QComboBox()
        self.from_combo.setMinimumWidth(150)
        currency_layout.addWidget(self.from_combo)
        
        # Arrow
        arrow_label = QLabel('→')
        arrow_label.setFont(QFont('Arial', 20, QFont.Bold))
        arrow_label.setStyleSheet('color: #00ff99;')
        currency_layout.addWidget(arrow_label)
        
        # To currency
        to_label = QLabel('To:')
        currency_layout.addWidget(to_label)
        
        self.to_combo = QComboBox()
        self.to_combo.setMinimumWidth(150)
        currency_layout.addWidget(self.to_combo)
        
        currency_layout.addStretch()
        controls_layout.addLayout(currency_layout)
        
        # Second row: Amount input and button
        amount_layout = QHBoxLayout()
        
        # Amount input
        amount_label = QLabel('💰 Amount:')
        amount_label.setStyleSheet('color: #00ff99; font-weight: bold; font-size: 14px;')
        amount_layout.addWidget(amount_label)
        
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText('Enter amount (e.g., 0.5, 1.0)')
        self.amount_input.setFixedWidth(200)
        self.amount_input.setStyleSheet('''
            QLineEdit {
                padding: 12px; 
                font-size: 14px;
                font-weight: bold;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #2a2a2a, stop:1 #1e1e1e);
                border: 2px solid #00ff99;
                border-radius: 8px;
                color: #ffffff;
            }
            QLineEdit:focus {
                border: 3px solid #00ff99;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1e1e1e, stop:1 #2a2a2a);
            }
        ''')
        # Ensure the input is editable and accepts focus
        self.amount_input.setReadOnly(False)
        self.amount_input.setEnabled(True)
        self.amount_input.setFocusPolicy(Qt.StrongFocus)
        amount_layout.addWidget(self.amount_input)
        
        # Get fee button
        self.get_fee_button = QPushButton('Get Exchange Fee')
        self.get_fee_button.setFixedWidth(150)
        amount_layout.addWidget(self.get_fee_button)
        
        amount_layout.addStretch()
        controls_layout.addLayout(amount_layout)
        
        layout.addLayout(controls_layout)
        
        # Exchange results
        self.exchange_results = QLabel('Select currencies and click "Get Exchange Fee" to see rates')
        self.exchange_results.setFont(QFont('Arial', 14))
        self.exchange_results.setStyleSheet('color: #ffffff; padding: 20px; background-color: #2d2d2d; border: 1px solid #555; border-radius: 5px;')
        self.exchange_results.setWordWrap(True)
        self.exchange_results.setMinimumHeight(100)
        layout.addWidget(self.exchange_results)
        
        # Exchange fee table
        self.exchange_table = QTableWidget()
        self.exchange_table.setColumnCount(4)
        self.exchange_table.setHorizontalHeaderLabels([
            'From → To', 'Min Amount', 'Exchange Fee', 'Network Fee'
        ])
        
        # Make exchange table responsive
        ex_header = self.exchange_table.horizontalHeader()
        ex_header.setStretchLastSection(True)
        for i in range(4):
            ex_header.setSectionResizeMode(i, ex_header.Stretch)
        
        layout.addWidget(self.exchange_table)

    def setup_suggestions_tab(self):
        layout = QVBoxLayout()
        self.suggestions_tab.setLayout(layout)
        
        # Title
        suggestions_title = QLabel('🎯 AI-Powered Trading Suggestions')
        suggestions_title.setFont(QFont('Arial', 20, QFont.Bold))
        suggestions_title.setAlignment(Qt.AlignCenter)
        suggestions_title.setStyleSheet('''
            color: #00ff99; 
            margin: 15px; 
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1e1e1e, stop:1 #2a2a2a);
            border: 2px solid #00ff99;
            border-radius: 10px;
            padding: 15px;
        ''')
        layout.addWidget(suggestions_title)
        
        # Analysis controls
        controls_layout = QHBoxLayout()
        
        # Analyze button
        self.analyze_button = QPushButton('🔍 Analyze Market')
        self.analyze_button.setFixedWidth(200)
        self.analyze_button.setStyleSheet('''
            QPushButton {
                font-size: 14px;
                font-weight: bold;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00ff99, stop:1 #00cc77);
                color: #000000;
                border: 2px solid #ffffff;
                padding: 12px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #ffffff, stop:1 #e6e6e6);
                color: #000000;
            }
        ''')
        controls_layout.addWidget(self.analyze_button)
        
        # Auto-refresh for suggestions
        auto_refresh_label = QLabel('⚡ Auto-updates with market data')
        auto_refresh_label.setStyleSheet('color: #ffb347; font-weight: bold; margin-left: 20px;')
        controls_layout.addWidget(auto_refresh_label)
        
        controls_layout.addStretch()
        layout.addLayout(controls_layout)
        
        # Suggestions results
        self.suggestions_results = QLabel('Click "Analyze Market" to get AI-powered trading suggestions based on technical indicators')
        self.suggestions_results.setFont(QFont('Arial', 14))
        self.suggestions_results.setStyleSheet('''
            color: #ffffff; 
            padding: 25px; 
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1e1e1e, stop:1 #2a2a2a);
            border: 2px solid #444; 
            border-radius: 10px;
            margin: 10px;
        ''')
        self.suggestions_results.setWordWrap(True)
        self.suggestions_results.setMinimumHeight(150)
        layout.addWidget(self.suggestions_results)
        
        # Suggestions table
        self.suggestions_table = QTableWidget()
        self.suggestions_table.setColumnCount(6)
        self.suggestions_table.setHorizontalHeaderLabels([
            'Cryptocurrency', 'Action', 'Confidence', 'Price Target', 'Current Price', 'Reasoning'
        ])
        
        # Enhanced table styling
        self.suggestions_table.setStyleSheet('''
            QTableWidget {
                gridline-color: #00ff99;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1e1e1e, stop:1 #2a2a2a);
                border: 2px solid #00ff99;
                border-radius: 8px;
                font-size: 13px;
            }
            QTableWidget::item {
                padding: 15px;
                border-bottom: 1px solid #00ff99;
                border-right: 1px solid #444;
            }
            QHeaderView::section {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #00ff99, stop:1 #00cc77);
                color: #000000;
                padding: 15px;
                font-weight: bold;
                font-size: 13px;
                border: 1px solid #ffffff;
            }
        ''')
        
        # Make suggestions table responsive
        sug_header = self.suggestions_table.horizontalHeader()
        sug_header.setStretchLastSection(True)
        for i in range(6):
            sug_header.setSectionResizeMode(i, sug_header.Stretch)
        
        layout.addWidget(self.suggestions_table)

    def setup_data(self):
        # Famous cryptocurrencies with their CoinGecko IDs
        self.coins = [
            ('bitcoin', 'BTC', 'Bitcoin'),
            ('ethereum', 'ETH', 'Ethereum'),
            ('binancecoin', 'BNB', 'BNB'),
            ('cardano', 'ADA', 'Cardano'),
            ('solana', 'SOL', 'Solana'),
            ('xrp', 'XRP', 'XRP'),
            ('dogecoin', 'DOGE', 'Dogecoin'),
            ('monero', 'XMR', 'Monero'),
            ('tether', 'USDT', 'Tether'),
            ('polygon', 'MATIC', 'Polygon'),
            ('litecoin', 'LTC', 'Litecoin'),
            ('chainlink', 'LINK', 'Chainlink'),
            ('avalanche-2', 'AVAX', 'Avalanche'),
            ('tron', 'TRX', 'TRON'),
            ('shiba-inu', 'SHIB', 'Shiba Inu'),
            ('uniswap', 'UNI', 'Uniswap'),
            ('the-open-network', 'TON', 'Toncoin'),
        ]
        
        self.coin_ids = ','.join([c[0] for c in self.coins])
        self.proxy = None
        self.current_prices = {}
        
        # ChangeNOW currency mapping (CoinGecko ID to ChangeNOW ticker)
        self.changenow_mapping = {
            'bitcoin': 'btc',
            'ethereum': 'eth',
            'binancecoin': 'bnb',
            'cardano': 'ada',
            'solana': 'sol',
            'xrp': 'xrp',
            'dogecoin': 'doge',
            'monero': 'xmr',
            'tether': 'usdt',
            'polygon': 'matic',
            'litecoin': 'ltc',
            'chainlink': 'link',
            'avalanche-2': 'avax',
            'tron': 'trx',
            'shiba-inu': 'shib',
            'uniswap': 'uni',
            'the-open-network': 'ton',
        }

    def setup_connections(self):
        self.update_price_signal.connect(self.update_current_price)
        self.update_status_signal.connect(self.update_status)
        self.update_table_signal.connect(self.update_price_table)
        self.update_chart_signal.connect(self.update_chart)
        self.update_exchange_signal.connect(self.update_exchange_info)
        self.update_suggestions_signal.connect(self.update_suggestions_display)
        self.refresh_button.clicked.connect(self.refresh_all_prices)
        self.proxy_button.clicked.connect(self.set_proxy)
        self.combo.currentTextChanged.connect(self.on_coin_changed)
        self.period_combo.currentTextChanged.connect(self.on_period_changed)
        self.get_fee_button.clicked.connect(self.get_exchange_fee)
        self.analyze_button.clicked.connect(self.analyze_market)

    def load_initial_settings(self):
        # Use environment proxy if set
        env_proxy = os.environ.get('HTTP_PROXY') or os.environ.get('http_proxy')
        if env_proxy:
            self.proxy = env_proxy
            self.session.proxies = {'http': env_proxy, 'https': env_proxy}
            self.proxy_input.setText(env_proxy)

    def populate_combo(self):
        self.combo.clear()
        self.from_combo.clear()
        self.to_combo.clear()
        
        for coin_id, symbol, name in self.coins:
            # Chart combo
            self.combo.addItem(f"{symbol} - {name}", coin_id)
            # Exchange combos
            self.from_combo.addItem(f"{symbol} - {name}", coin_id)
            self.to_combo.addItem(f"{symbol} - {name}", coin_id)
        
        if self.coins:
            self.combo.setCurrentIndex(0)
            self.from_combo.setCurrentIndex(0)  # BTC
            self.to_combo.setCurrentIndex(1)    # ETH
            # Load initial chart after a short delay to ensure combo is populated
            QTimer.singleShot(1000, self.load_initial_chart)
        
        # Initial data load
        self.refresh_all_prices()
    
    def load_initial_chart(self):
        """Load initial chart for the first cryptocurrency"""
        coin_id = self.combo.currentData()
        print(f"Loading initial chart for: {coin_id}")  # Debug
        if coin_id:
            self.fetch_price_history(coin_id)

    def set_proxy(self):
        proxy_url = self.proxy_input.text().strip()
        if proxy_url:
            if proxy_url.startswith(('socks5h://', 'socks5://', 'socks4://')):
                try:
                    import socks
                    self.session.proxies = {'http': proxy_url, 'https': proxy_url}
                    self.update_status_signal.emit(f'SOCKS proxy set: {proxy_url}')
                except ImportError:
                    self.update_status_signal.emit('requests[socks] required for SOCKS proxy. Install with: pip install requests[socks]')
                    return
            else:
                self.session.proxies = {'http': proxy_url, 'https': proxy_url}
                self.update_status_signal.emit(f'HTTP proxy set: {proxy_url}')
        else:
            self.session.proxies = {}
            self.update_status_signal.emit('Proxy cleared.')

    def refresh_all_prices(self):
        """Fetch current prices and market data for all cryptocurrencies"""
        self.update_status_signal.emit('Fetching latest prices...')
        
        def fetch_data():
            try:
                # Fetch detailed market data
                url = f'https://api.coingecko.com/api/v3/coins/markets'
                params = {
                    'vs_currency': 'usd',
                    'ids': self.coin_ids,
                    'order': 'market_cap_desc',
                    'per_page': 100,
                    'page': 1,
                    'sparkline': False,
                    'price_change_percentage': '24h'
                }
                
                response = self.session.get(url, params=params, timeout=15)
                
                if response.status_code == 200:
                    data = response.json()
                    market_data = {}
                    
                    for coin in data:
                        coin_id = coin['id']
                        market_data[coin_id] = {
                            'symbol': coin['symbol'].upper(),
                            'name': coin['name'],
                            'current_price': coin['current_price'] or 0,
                            'price_change_24h': coin['price_change_percentage_24h'] or 0,
                            'market_cap': coin['market_cap'] or 0,
                            'total_volume': coin['total_volume'] or 0,
                            'last_updated': coin['last_updated']
                        }
                        self.current_prices[coin_id] = coin['current_price'] or 0
                    
                    self.update_table_signal.emit(market_data)
                    self.update_status_signal.emit('Prices updated successfully')
                    
                    # Update current coin's price
                    current_coin_id = self.combo.currentData()
                    if current_coin_id and current_coin_id in self.current_prices:
                        self.update_price_signal.emit(self.current_prices[current_coin_id])
                    
                else:
                    self.update_status_signal.emit(f'Error: HTTP {response.status_code}')
                    
            except requests.RequestException as e:
                self.update_status_signal.emit(f'Network error: {str(e)}')
            except Exception as e:
                self.update_status_signal.emit(f'Error fetching data: {str(e)}')
        
        threading.Thread(target=fetch_data, daemon=True).start()

    def update_price_table(self, market_data):
        """Update the price table with market data"""
        self.price_table.setRowCount(len(market_data))
        
        row = 0
        for coin_id, data in market_data.items():
            # Symbol
            self.price_table.setItem(row, 0, QTableWidgetItem(data['symbol']))
            
            # Name
            self.price_table.setItem(row, 1, QTableWidgetItem(data['name']))
            
            # Price
            price_item = QTableWidgetItem(f"${data['current_price']:,.4f}")
            self.price_table.setItem(row, 2, price_item)
            
            # 24h Change
            change = data['price_change_24h']
            change_item = QTableWidgetItem(f"{change:+.2f}%")
            if change > 0:
                change_item.setBackground(QColor(0, 255, 0, 50))
            elif change < 0:
                change_item.setBackground(QColor(255, 0, 0, 50))
            self.price_table.setItem(row, 3, change_item)
            
            # Market Cap
            market_cap = data['market_cap']
            if market_cap > 1e9:
                market_cap_str = f"${market_cap/1e9:.2f}B"
            elif market_cap > 1e6:
                market_cap_str = f"${market_cap/1e6:.2f}M"
            else:
                market_cap_str = f"${market_cap:,.0f}"
            self.price_table.setItem(row, 4, QTableWidgetItem(market_cap_str))
            
            # Volume
            volume = data['total_volume']
            if volume > 1e9:
                volume_str = f"${volume/1e9:.2f}B"
            elif volume > 1e6:
                volume_str = f"${volume/1e6:.2f}M"
            else:
                volume_str = f"${volume:,.0f}"
            self.price_table.setItem(row, 5, QTableWidgetItem(volume_str))
            
            # Last Updated
            try:
                last_updated = datetime.datetime.fromisoformat(data['last_updated'].replace('Z', '+00:00'))
                time_str = last_updated.strftime('%H:%M:%S')
            except:
                time_str = 'Unknown'
            self.price_table.setItem(row, 6, QTableWidgetItem(time_str))
            
            row += 1

    def update_current_price(self, price):
        """Update the current price display"""
        self.price_label.setText(f'Current Price: ${price:,.4f}')

    def on_coin_changed(self):
        """Handle coin selection change"""
        coin_id = self.combo.currentData()
        print(f"Coin changed to: {coin_id}")  # Debug
        if coin_id:
            self.fetch_price_history(coin_id)
            if coin_id in self.current_prices:
                self.update_price_signal.emit(self.current_prices[coin_id])

    def on_period_changed(self):
        """Handle period selection change"""
        coin_id = self.combo.currentData()
        period = self.period_combo.currentText()
        print(f"Period changed to: {period} for coin: {coin_id}")  # Debug
        if coin_id:
            self.fetch_price_history(coin_id)

    def fetch_price_history(self, coin_id):
        """Fetch and display price history for selected coin"""
        period = self.period_combo.currentText()
        
        # Map period to days
        days_map = {
            '7 days': 7,
            '30 days': 30,
            '90 days': 90,
            '1 year': 365
        }
        days = days_map.get(period, 30)
        
        self.update_status_signal.emit(f'Loading {period} price history...')
        
        def fetch_history():
            try:
                url = f'https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart'
                params = {
                    'vs_currency': 'usd',
                    'days': days,
                    'interval': 'daily' if days > 7 else 'hourly'
                }
                
                print(f"Fetching data from: {url}")  # Debug
                print(f"Params: {params}")  # Debug
                
                response = self.session.get(url, params=params, timeout=15)
                
                print(f"Response status: {response.status_code}")  # Debug
                
                if response.status_code == 200:
                    data = response.json()
                    prices = data.get('prices', [])
                    
                    print(f"Received {len(prices)} price points")  # Debug
                    
                    if prices:
                        # Extract dates and prices
                        dates = [datetime.datetime.fromtimestamp(p[0]/1000) for p in prices]
                        price_values = [p[1] for p in prices]
                        
                        # Use signal-slot mechanism instead of QTimer
                        self.update_chart_signal.emit(dates, price_values, coin_id, period)
                        
                        self.update_status_signal.emit('Price history loaded successfully')
                    else:
                        self.update_status_signal.emit('No price data available')
                else:
                    error_msg = f'Error loading history: HTTP {response.status_code}'
                    if response.status_code == 429:
                        error_msg += ' (Rate limited - please wait)'
                    print(f"Error response: {response.text[:200]}")  # Debug
                    self.update_status_signal.emit(error_msg)
                    
            except Exception as e:
                print(f"Exception in fetch_history: {str(e)}")  # Debug
                self.update_status_signal.emit(f'Error loading price history: {str(e)}')
        
        threading.Thread(target=fetch_history, daemon=True).start()

    def update_chart(self, dates, prices, coin_id, period):
        """Update the price chart"""
        try:
            print(f"Updating chart for {coin_id} with {len(dates)} data points")  # Debug
            
            self.ax.clear()
            self.ax.set_facecolor('#2d2d2d')
            
            # Plot price line
            self.ax.plot(dates, prices, color='#00ff99', linewidth=2)
            
            # Customize chart
            coin_name = next((name for cid, symbol, name in self.coins if cid == coin_id), coin_id)
            self.ax.set_title(f'{coin_name} Price History ({period})', color='white', fontsize=16, pad=20)
            self.ax.set_xlabel('Date', color='white')
            self.ax.set_ylabel('Price (USD)', color='white')
            
            # Style axes
            self.ax.tick_params(axis='both', colors='white')
            self.ax.grid(True, alpha=0.3, color='white')
            
            # Format x-axis dates
            try:
                import matplotlib.dates as mdates
                if len(dates) > 30:  # More than 30 data points
                    self.ax.xaxis.set_major_locator(mdates.WeekdayLocator())
                    self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
                else:
                    self.ax.xaxis.set_major_locator(mdates.DayLocator(interval=max(1, len(dates)//10)))
                    self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
                
                # Rotate x-axis labels
                for label in self.ax.get_xticklabels():
                    label.set_rotation(45)
                    label.set_horizontalalignment('right')
            except Exception as date_error:
                print(f"Date formatting error: {date_error}")
            
            # Format y-axis for currency
            try:
                if max(prices) > 1000:
                    self.ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
                elif max(prices) > 1:
                    self.ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:.2f}'))
                else:
                    self.ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:.4f}'))
            except Exception as format_error:
                print(f"Y-axis formatting error: {format_error}")
            
            self.figure.tight_layout()
            self.canvas.draw()
            
            print("Chart updated successfully")  # Debug
            
        except Exception as e:
            print(f"Error updating chart: {str(e)}")  # Debug
            self.update_status_signal.emit(f'Error updating chart: {str(e)}')

    def update_status(self, msg):
        """Update status label"""
        self.status_label.setText(msg)

    def get_exchange_fee(self):
        """Get exchange fee from ChangeNOW.io"""
        from_coin_id = self.from_combo.currentData()
        to_coin_id = self.to_combo.currentData()
        
        if not from_coin_id or not to_coin_id:
            self.update_status_signal.emit('Please select both currencies')
            return
            
        if from_coin_id == to_coin_id:
            self.update_status_signal.emit('Please select different currencies')
            return
        
        from_ticker = self.changenow_mapping.get(from_coin_id)
        to_ticker = self.changenow_mapping.get(to_coin_id)
        
        if not from_ticker or not to_ticker:
            self.update_status_signal.emit('Currency not supported by ChangeNOW')
            return
        
        # Get custom amount from input field
        custom_amount = None
        amount_text = self.amount_input.text().strip()
        if amount_text:
            try:
                custom_amount = float(amount_text)
                if custom_amount <= 0:
                    self.update_status_signal.emit('Amount must be greater than 0')
                    return
            except ValueError:
                self.update_status_signal.emit('Please enter a valid amount')
                return
        
        self.update_status_signal.emit(f'Getting exchange rate for {from_ticker.upper()} → {to_ticker.upper()}...')
        
        def fetch_exchange_data():
            try:
                # Get minimum exchange amount
                min_url = f'https://api.changenow.io/v1/min-amount/{from_ticker}_{to_ticker}'
                print(f"Fetching min amount from: {min_url}")
                
                min_response = self.session.get(min_url, timeout=10)
                
                if min_response.status_code == 200:
                    min_data = min_response.json()
                    min_amount = min_data.get('minAmount', 0)
                    print(f"Min amount: {min_amount}")
                    
                    # Use custom amount or minimum amount
                    exchange_amount = custom_amount if custom_amount else max(min_amount, 1)
                    
                    # Check if custom amount is below minimum
                    if custom_amount and custom_amount < min_amount:
                        self.update_status_signal.emit(f'Amount is below minimum ({min_amount} {from_ticker.upper()})')
                        return
                    
                    # Get exchange estimate
                    estimate_url = f'https://api.changenow.io/v1/exchange-amount/{exchange_amount}/{from_ticker}_{to_ticker}'
                    print(f"Fetching estimate from: {estimate_url}")
                    
                    estimate_response = self.session.get(estimate_url, timeout=10)
                    
                    if estimate_response.status_code == 200:
                        estimate_data = estimate_response.json()
                        estimated_amount = estimate_data.get('estimatedAmount', 0)
                        print(f"Estimated amount: {estimated_amount}")
                        
                        # Get exchange info (fees)
                        info_url = f'https://api.changenow.io/v1/exchange-range/{from_ticker}_{to_ticker}'
                        info_response = self.session.get(info_url, timeout=10)
                        
                        exchange_info = {
                            'from_ticker': from_ticker.upper(),
                            'to_ticker': to_ticker.upper(),
                            'min_amount': min_amount,
                            'estimated_amount': estimated_amount,
                            'exchange_amount': exchange_amount,
                            'exchange_rate': estimated_amount / exchange_amount if exchange_amount > 0 else 0,
                            'network_fee': 'Variable',
                            'service_fee': 'Included in rate',
                            'custom_amount': custom_amount is not None
                        }
                        
                        if info_response.status_code == 200:
                            info_data = info_response.json()
                            print(f"Exchange range info: {info_data}")
                        
                        # Emit signal to update UI
                        self.update_exchange_signal.emit(from_ticker, to_ticker, exchange_info)
                        self.update_status_signal.emit('Exchange rates loaded successfully')
                        
                    else:
                        print(f"Estimate error: {estimate_response.status_code} - {estimate_response.text}")
                        self.update_status_signal.emit(f'Error getting exchange estimate: {estimate_response.status_code}')
                else:
                    print(f"Min amount error: {min_response.status_code} - {min_response.text}")
                    self.update_status_signal.emit(f'Error getting minimum amount: {min_response.status_code}')
                    
            except Exception as e:
                print(f"Exception in fetch_exchange_data: {str(e)}")
                self.update_status_signal.emit(f'Error fetching exchange data: {str(e)}')
        
        threading.Thread(target=fetch_exchange_data, daemon=True).start()

    def update_exchange_info(self, from_ticker, to_ticker, exchange_info):
        """Update exchange information display"""
        try:
            # Update results text
            if exchange_info.get('custom_amount', False):
                results_text = f"""
Exchange Rate: {from_ticker} → {to_ticker}

• Custom Amount: {exchange_info['exchange_amount']:.8f} {from_ticker}
• Minimum Amount: {exchange_info['min_amount']:.8f} {from_ticker}
• Exchange Rate: 1 {from_ticker} ≈ {exchange_info['exchange_rate']:.8f} {to_ticker}
• Service Fee: {exchange_info['service_fee']}
• Network Fee: {exchange_info['network_fee']}

You will receive: {exchange_info['estimated_amount']:.8f} {to_ticker}
(for {exchange_info['exchange_amount']:.8f} {from_ticker})

Note: Rates are approximate and may change. Always verify on ChangeNOW.io before exchange.
            """.strip()
            else:
                results_text = f"""
Exchange Rate: {from_ticker} → {to_ticker}

• Minimum Amount: {exchange_info['min_amount']:.8f} {from_ticker}
• Exchange Rate: 1 {from_ticker} ≈ {exchange_info['exchange_rate']:.8f} {to_ticker}
• Service Fee: {exchange_info['service_fee']}
• Network Fee: {exchange_info['network_fee']}

Estimated Amount: {exchange_info['estimated_amount']:.8f} {to_ticker}
(for {exchange_info['exchange_amount']:.8f} {from_ticker})

Note: Rates are approximate and may change. Always verify on ChangeNOW.io before exchange.
            """.strip()
            
            self.exchange_results.setText(results_text)
            
            # Update table
            self.exchange_table.setRowCount(1)
            
            # Conversion pair
            pair_item = QTableWidgetItem(f"{from_ticker} → {to_ticker}")
            self.exchange_table.setItem(0, 0, pair_item)
            
            # Min amount
            min_item = QTableWidgetItem(f"{exchange_info['min_amount']:.8f} {from_ticker}")
            self.exchange_table.setItem(0, 1, min_item)
            
            # Exchange fee (rate info)
            rate_item = QTableWidgetItem(f"1:{exchange_info['exchange_rate']:.6f}")
            self.exchange_table.setItem(0, 2, rate_item)
            
            # Network fee
            network_item = QTableWidgetItem(exchange_info['network_fee'])
            self.exchange_table.setItem(0, 3, network_item)
            
        except Exception as e:
            print(f"Error updating exchange info: {str(e)}")
            self.update_status_signal.emit(f'Error updating exchange display: {str(e)}')

    def analyze_market(self):
        """Analyze market data and generate trading suggestions"""
        self.update_status_signal.emit('🔍 Analyzing market trends and generating suggestions...')
        
        def fetch_market_analysis():
            try:
                suggestions = []
                
                # Analyze each coin
                for coin_id, symbol, name in self.coins:
                    if coin_id in self.current_prices:
                        price_data = self.current_prices[coin_id]
                        
                        # Handle both dict and direct value cases
                        if isinstance(price_data, dict):
                            current_price = price_data.get('usd', 0)
                            price_change_24h = price_data.get('usd_24h_change', 0)
                            market_cap = price_data.get('usd_market_cap', 0)
                            volume = price_data.get('usd_24h_vol', 0)
                        else:
                            # If price_data is just a number, use it as current_price
                            current_price = price_data if isinstance(price_data, (int, float)) else 0
                            price_change_24h = 0
                            market_cap = 0
                            volume = 0
                        
                        # Skip if no valid price data
                        if current_price <= 0:
                            continue
                        
                        # Simple technical analysis
                        suggestion = self.analyze_coin_data(
                            name, symbol, current_price, price_change_24h, 
                            market_cap, volume
                        )
                        if suggestion:
                            suggestions.append(suggestion)
                
                # Sort by confidence
                suggestions.sort(key=lambda x: x['confidence'], reverse=True)
                
                # Emit signal to update UI
                self.update_suggestions_signal.emit(suggestions[:10])  # Top 10 suggestions
                self.update_status_signal.emit('✅ Market analysis complete!')
                
            except Exception as e:
                print(f"Exception in market analysis: {str(e)}")
                self.update_status_signal.emit(f'❌ Error analyzing market: {str(e)}')
        
        threading.Thread(target=fetch_market_analysis, daemon=True).start()

    def analyze_coin_data(self, name, symbol, price, change_24h, market_cap, volume):
        """Analyze individual coin data and return suggestion"""
        try:
            # Technical indicators analysis
            confidence = 50  # Base confidence
            action = "HOLD"
            reasoning = []
            target_price = price
            
            # Price momentum analysis
            if change_24h > 15:
                action = "SELL"
                confidence += 20
                reasoning.append(f"Strong upward momentum (+{change_24h:.1f}%)")
                target_price = price * 0.95  # Take profit
                
            elif change_24h > 5:
                if volume > market_cap * 0.1:  # High volume
                    action = "BUY"
                    confidence += 15
                    reasoning.append(f"Good momentum with high volume")
                    target_price = price * 1.1
                else:
                    action = "HOLD"
                    reasoning.append(f"Moderate gain (+{change_24h:.1f}%)")
                    
            elif change_24h < -15:
                action = "BUY"
                confidence += 25
                reasoning.append(f"Oversold condition ({change_24h:.1f}%)")
                target_price = price * 1.2  # Recovery target
                
            elif change_24h < -5:
                action = "BUY"
                confidence += 10
                reasoning.append(f"Dip buying opportunity ({change_24h:.1f}%)")
                target_price = price * 1.15
                
            else:
                reasoning.append(f"Sideways movement ({change_24h:.1f}%)")
            
            # Volume analysis
            if market_cap > 0:
                volume_ratio = volume / market_cap if market_cap > 0 else 0
                if volume_ratio > 0.2:
                    confidence += 10
                    reasoning.append("High trading volume")
                elif volume_ratio < 0.05:
                    confidence -= 5
                    reasoning.append("Low trading volume")
            
            # Market cap considerations
            if market_cap > 50_000_000_000:  # Large cap
                reasoning.append("Large-cap stability")
                confidence += 5
            elif market_cap < 1_000_000_000:  # Small cap
                reasoning.append("Small-cap volatility")
                confidence -= 5
            
            # Special crypto considerations
            if symbol in ['BTC', 'ETH']:
                confidence += 10
                reasoning.append("Major cryptocurrency")
            elif symbol in ['USDT', 'USDC']:
                action = "HOLD"
                confidence = 90
                reasoning = ["Stablecoin - hold for stability"]
                target_price = price
            
            confidence = min(95, max(5, confidence))  # Clamp between 5-95%
            
            return {
                'name': name,
                'symbol': symbol,
                'action': action,
                'confidence': confidence,
                'current_price': price,
                'target_price': target_price,
                'reasoning': ' | '.join(reasoning)
            }
            
        except Exception as e:
            print(f"Error analyzing {name}: {str(e)}")
            return None

    def update_suggestions_display(self, suggestions):
        """Update the suggestions display with analysis results"""
        try:
            # Update results text
            if suggestions:
                summary_text = f"""
🎯 AI MARKET ANALYSIS COMPLETE 🎯

📊 Analyzed {len(self.coins)} cryptocurrencies
🔍 Generated {len(suggestions)} actionable suggestions
⭐ Top recommendations ready below

💡 STRATEGY OVERVIEW:
• BUY signals: Look for oversold conditions and dip opportunities
• SELL signals: Take profits on strong momentum moves  
• HOLD signals: Wait for better entry/exit points

⚠️ DISCLAIMER: This is automated analysis based on price data and technical indicators. 
Always do your own research and consider market risks before trading.

📈 Last updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                """.strip()
            else:
                summary_text = "No suggestions available. Try refreshing market data first."
            
            self.suggestions_results.setText(summary_text)
            
            # Update table
            self.suggestions_table.setRowCount(len(suggestions))
            
            for row, suggestion in enumerate(suggestions):
                # Cryptocurrency name
                name_item = QTableWidgetItem(f"{suggestion['symbol']}")
                name_item.setFont(QFont('Arial', 12, QFont.Bold))
                self.suggestions_table.setItem(row, 0, name_item)
                
                # Action with color coding
                action_item = QTableWidgetItem(suggestion['action'])
                action_item.setFont(QFont('Arial', 12, QFont.Bold))
                if suggestion['action'] == 'BUY':
                    action_item.setBackground(QColor(0, 255, 0, 100))  # Green
                    action_item.setForeground(QColor(0, 200, 0))
                elif suggestion['action'] == 'SELL':
                    action_item.setBackground(QColor(255, 0, 0, 100))  # Red
                    action_item.setForeground(QColor(255, 100, 100))
                else:  # HOLD
                    action_item.setBackground(QColor(255, 255, 0, 100))  # Yellow
                    action_item.setForeground(QColor(255, 215, 0))
                self.suggestions_table.setItem(row, 1, action_item)
                
                # Confidence
                confidence_item = QTableWidgetItem(f"{suggestion['confidence']:.0f}%")
                confidence_item.setFont(QFont('Arial', 11, QFont.Bold))
                if suggestion['confidence'] >= 80:
                    confidence_item.setForeground(QColor(0, 255, 153))
                elif suggestion['confidence'] >= 60:
                    confidence_item.setForeground(QColor(255, 215, 0))
                else:
                    confidence_item.setForeground(QColor(255, 165, 0))
                self.suggestions_table.setItem(row, 2, confidence_item)
                
                # Price target
                target_item = QTableWidgetItem(f"${suggestion['target_price']:.4f}")
                target_item.setFont(QFont('Arial', 11))
                self.suggestions_table.setItem(row, 3, target_item)
                
                # Current price
                current_item = QTableWidgetItem(f"${suggestion['current_price']:.4f}")
                current_item.setFont(QFont('Arial', 11))
                self.suggestions_table.setItem(row, 4, current_item)
                
                # Reasoning
                reasoning_item = QTableWidgetItem(suggestion['reasoning'])
                reasoning_item.setFont(QFont('Arial', 10))
                self.suggestions_table.setItem(row, 5, reasoning_item)
                
        except Exception as e:
            print(f"Error updating suggestions display: {str(e)}")
            self.update_status_signal.emit(f'Error updating suggestions: {str(e)}')
        
    def closeEvent(self, event):
        """Clean up on close"""
        if hasattr(self, 'auto_refresh_timer'):
            self.auto_refresh_timer.stop()
        if hasattr(self, 'session'):
            self.session.close()
        event.accept()


def main():
    app = QApplication(sys.argv)
    widget = CryptoPriceWidget()
    widget.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()