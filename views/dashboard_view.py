"""
Dashboard View for Persian Invoicing System
Enhanced with refresh functionality and improved statistics
"""

from datetime import datetime, timedelta
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                           QLabel, QPushButton, QFrame, QTableWidget, 
                           QTableWidgetItem, QHeaderView, QGroupBox,
                           QProgressBar, QSizePolicy)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap, QIcon
from services.database_service import DatabaseService
import jdatetime

class StatCard(QFrame):
    """Custom stat card widget"""
    
    def __init__(self, title, value, subtitle="", color="#4CAF50", icon=""):
        super().__init__()
        self.setup_ui(title, value, subtitle, color, icon)
        
    def setup_ui(self, title, value, subtitle, color, icon):
        """Setup stat card UI"""
        self.setFrameStyle(QFrame.Shape.Box)
        layout = QVBoxLayout()
        layout.setSpacing(8)
        layout.setContentsMargins(20, 15, 20, 15)
        
        # Icon and title row
        header_layout = QHBoxLayout()
        
        if icon:
            icon_label = QLabel(icon)
            icon_label.setFont(QFont("Vazirmatn", 20))
            icon_label.setStyleSheet(f"color: {color};")
            header_layout.addWidget(icon_label)
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Vazirmatn", 11, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #666;")
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        # Value
        self.value_label = QLabel(str(value))
        self.value_label.setFont(QFont("Vazirmatn", 24, QFont.Weight.Bold))
        self.value_label.setStyleSheet(f"color: {color};")
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Subtitle
        if subtitle:
            subtitle_label = QLabel(subtitle)
            subtitle_label.setFont(QFont("Vazirmatn", 9))
            subtitle_label.setStyleSheet("color: #999;")
            subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(subtitle_label)
        
        layout.addLayout(header_layout)
        layout.addWidget(self.value_label)
        
        self.setLayout(layout)
        
        # Apply styling
        self.setStyleSheet(f"""
            StatCard {{
                background-color: white;
                border: 2px solid #f0f0f0;
                border-radius: 12px;
                margin: 5px;
            }}
            StatCard:hover {{
                border-color: {color};
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            }}
        """)
        
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setMinimumHeight(120)
        
    def update_value(self, value):
        """Update the stat value"""
        self.value_label.setText(str(value))

class DashboardView(QWidget):
    """Enhanced dashboard with comprehensive statistics and refresh functionality"""
    
    refresh_requested = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.db_service = DatabaseService()
        self.setup_ui()
        self.setup_auto_refresh()
        self.load_dashboard_data()
        
    def setup_ui(self):
        """Setup the dashboard user interface"""
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Header section
        header_layout = QHBoxLayout()
        
        # Welcome message
        welcome_label = QLabel("داشبورد مدیریت")
        welcome_label.setFont(QFont("Vazirmatn", 18, QFont.Weight.Bold))
        welcome_label.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        
        # Refresh button
        self.refresh_button = QPushButton("🔄 به‌روزرسانی")
        self.refresh_button.setFont(QFont("Vazirmatn", 11, QFont.Weight.Bold))
        self.refresh_button.clicked.connect(self.refresh_dashboard)
        self.refresh_button.setMinimumHeight(40)
        
        # Last update label
        self.last_update_label = QLabel()
        self.last_update_label.setFont(QFont("Vazirmatn", 9))
        self.last_update_label.setStyleSheet("color: #666;")
        
        header_layout.addWidget(welcome_label)
        header_layout.addStretch()
        header_layout.addWidget(self.last_update_label)
        header_layout.addWidget(self.refresh_button)
        
        # Statistics cards
        stats_layout = QGridLayout()
        stats_layout.setSpacing(15)
        
        # Create stat cards
        self.today_invoices_card = StatCard(
            "فاکتورهای امروز", "0", "", "#3498db", "📋"
        )
        
        self.today_revenue_card = StatCard(
            "درآمد امروز", "0 تومان", "", "#27ae60", "💰"
        )
        
        self.total_products_card = StatCard(
            "تعداد کالاها", "0", "", "#e74c3c", "📦"
        )
        
        self.total_invoices_card = StatCard(
            "کل فاکتورها", "0", "", "#9b59b6", "📊"
        )
        
        self.low_stock_card = StatCard(
            "کالاهای کم‌موجود", "0", "موجودی کمتر از 5", "#f39c12", "⚠️"
        )
        
        self.monthly_revenue_card = StatCard(
            "درآمد ماه جاری", "0 تومان", "", "#1abc9c", "📈"
        )
        
        # Add cards to grid
        stats_layout.addWidget(self.today_invoices_card, 0, 0)
        stats_layout.addWidget(self.today_revenue_card, 0, 1)
        stats_layout.addWidget(self.total_products_card, 0, 2)
        stats_layout.addWidget(self.total_invoices_card, 1, 0)
        stats_layout.addWidget(self.low_stock_card, 1, 1)
        stats_layout.addWidget(self.monthly_revenue_card, 1, 2)
        
        # Recent invoices section
        recent_group = QGroupBox("آخرین فاکتورها")
        recent_group.setFont(QFont("Vazirmatn", 12, QFont.Weight.Bold))
        recent_layout = QVBoxLayout(recent_group)
        
        # Recent invoices table
        self.recent_table = QTableWidget()
        self.recent_table.setColumnCount(5)
        self.recent_table.setHorizontalHeaderLabels([
            "شماره فاکتور", "نام مشتری", "تاریخ", "مبلغ", "وضعیت"
        ])
        
        # Configure table
        header = self.recent_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        
        self.recent_table.setMaximumHeight(200)
        self.recent_table.setAlternatingRowColors(True)
        
        recent_layout.addWidget(self.recent_table)
        
        # Low stock products section
        stock_group = QGroupBox("کالاهای کم‌موجود")
        stock_group.setFont(QFont("Vazirmatn", 12, QFont.Weight.Bold))
        stock_layout = QVBoxLayout(stock_group)
        
        self.stock_table = QTableWidget()
        self.stock_table.setColumnCount(3)
        self.stock_table.setHorizontalHeaderLabels([
            "نام کالا", "موجودی فعلی", "قیمت فروش"
        ])
        
        # Configure stock table
        stock_header = self.stock_table.horizontalHeader()
        stock_header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        stock_header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        stock_header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        
        self.stock_table.setMaximumHeight(150)
        self.stock_table.setAlternatingRowColors(True)
        
        stock_layout.addWidget(self.stock_table)
        
        # Quick actions section
        actions_group = QGroupBox("عملیات سریع")
        actions_group.setFont(QFont("Vazirmatn", 12, QFont.Weight.Bold))
        actions_layout = QHBoxLayout(actions_group)
        
        self.new_invoice_btn = QPushButton("📋 فاکتور جدید")
        self.new_product_btn = QPushButton("📦 کالای جدید")
        self.backup_btn = QPushButton("💾 پشتیبان‌گیری")
        self.reports_btn = QPushButton("📊 گزارشات")
        
        for btn in [self.new_invoice_btn, self.new_product_btn, self.backup_btn, self.reports_btn]:
            btn.setFont(QFont("Vazirmatn", 11, QFont.Weight.Bold))
            btn.setMinimumHeight(45)
            actions_layout.addWidget(btn)
        
        # Connect quick action buttons
        self.backup_btn.clicked.connect(self.create_backup)
        
        # Add all sections to main layout
        main_layout.addLayout(header_layout)
        main_layout.addLayout(stats_layout)
        main_layout.addWidget(recent_group)
        main_layout.addWidget(stock_group)
        main_layout.addWidget(actions_group)
        main_layout.addStretch()
        
        self.setLayout(main_layout)
        self.setup_styling()
        
    def setup_styling(self):
        """Setup modern dashboard styling"""
        self.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
                font-family: 'Vazirmatn', Arial, sans-serif;
            }
            
            QGroupBox {
                font-weight: bold;
                border: 2px solid #dee2e6;
                border-radius: 12px;
                margin: 15px 0px;
                padding-top: 15px;
                background-color: white;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px 0 8px;
                color: #495057;
                background-color: white;
            }
            
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4CAF50, stop:1 #45a049);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 20px;
                font-size: 11pt;
                font-weight: bold;
                min-width: 120px;
            }
            
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #45a049, stop:1 #3d8b40);
                transform: translateY(-2px);
            }
            
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3d8b40, stop:1 #2e7d32);
            }
            
            QPushButton#refresh_button {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2196F3, stop:1 #1976D2);
            }
            
            QPushButton#refresh_button:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1976D2, stop:1 #1565C0);
            }
            
            QTableWidget {
                border: 1px solid #dee2e6;
                border-radius: 8px;
                background-color: white;
                gridline-color: #f8f9fa;
                font-size: 10pt;
            }
            
            QTableWidget::item {
                padding: 12px 8px;
                border: none;
            }
            
            QTableWidget::item:selected {
                background-color: #e3f2fd;
                color: #1976d2;
            }
            
            QTableWidget::item:alternate {
                background-color: #f8f9fa;
            }
            
            QHeaderView::section {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f8f9fa, stop:1 #e9ecef);
                padding: 12px 8px;
                border: 1px solid #dee2e6;
                font-weight: bold;
                color: #495057;
            }
            
            QLabel {
                color: #495057;
            }
        """)
        
        # Set object names for specific styling
        self.refresh_button.setObjectName("refresh_button")
        
    def setup_auto_refresh(self):
        """Setup automatic refresh timer"""
        self.auto_refresh_timer = QTimer()
        self.auto_refresh_timer.timeout.connect(self.load_dashboard_data)
        self.auto_refresh_timer.start(300000)  # Refresh every 5 minutes
        
    def load_dashboard_data(self):
        """Load and display dashboard data"""
        try:
            # Get dashboard statistics
            stats = self.db_service.get_dashboard_stats()
            
            # Update stat cards
            self.today_invoices_card.update_value(stats['today_invoices'])
            self.today_revenue_card.update_value(f"{stats['today_revenue']:,} تومان")
            self.total_products_card.update_value(stats['total_products'])
            self.total_invoices_card.update_value(stats['total_invoices'])
            self.low_stock_card.update_value(stats['low_stock_products'])
            
            # Calculate monthly revenue
            monthly_revenue = self.get_monthly_revenue()
            self.monthly_revenue_card.update_value(f"{monthly_revenue:,} تومان")
            
            # Load recent invoices
            self.load_recent_invoices()
            
            # Load low stock products
            self.load_low_stock_products()
            
            # Update last refresh time
            current_time = datetime.now()
            jdate = jdatetime.datetime.fromgregorian(datetime=current_time)
            self.last_update_label.setText(
                f"آخرین به‌روزرسانی: {jdate.strftime('%H:%M:%S')}"
            )
            
        except Exception as e:
            print(f"Error loading dashboard data: {e}")
    
    def get_monthly_revenue(self):
        """Calculate monthly revenue"""
        try:
            # Get invoices for current month
            now = datetime.now()
            month_start = datetime(now.year, now.month, 1)
            
            invoices = self.db_service.get_invoices()
            monthly_total = 0
            
            for invoice in invoices:
                if invoice.issue_date >= month_start:
                    monthly_total += invoice.final_amount
            
            return monthly_total
        except:
            return 0
    
    def load_recent_invoices(self):
        """Load recent invoices into table"""
        try:
            invoices = self.db_service.get_invoices()
            recent_invoices = invoices[:5]  # Get last 5 invoices
            
            self.recent_table.setRowCount(len(recent_invoices))
            
            for row, invoice in enumerate(recent_invoices):
                # Invoice number
                num_item = QTableWidgetItem(invoice.invoice_number)
                num_item.setFlags(num_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.recent_table.setItem(row, 0, num_item)
                
                # Customer name
                customer_item = QTableWidgetItem(invoice.customer_name)
                customer_item.setFlags(customer_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.recent_table.setItem(row, 1, customer_item)
                
                # Date
                date_item = QTableWidgetItem(invoice.persian_date)
                date_item.setFlags(date_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.recent_table.setItem(row, 2, date_item)
                
                # Amount
                amount_item = QTableWidgetItem(f"{invoice.final_amount:,} تومان")
                amount_item.setFlags(amount_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.recent_table.setItem(row, 3, amount_item)
                
                # Status
                status_item = QTableWidgetItem("✅ تکمیل شده")
                status_item.setFlags(status_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.recent_table.setItem(row, 4, status_item)
                
        except Exception as e:
            print(f"Error loading recent invoices: {e}")
    
    def load_low_stock_products(self):
        """Load low stock products into table"""
        try:
            products = self.db_service.get_products()
            low_stock_products = [p for p in products if p.stock_quantity <= 5]
            
            self.stock_table.setRowCount(len(low_stock_products))
            
            for row, product in enumerate(low_stock_products):
                # Product name
                name_item = QTableWidgetItem(product.name)
                name_item.setFlags(name_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.stock_table.setItem(row, 0, name_item)
                
                # Stock quantity with warning color
                stock_item = QTableWidgetItem(str(product.stock_quantity))
                stock_item.setFlags(stock_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                if product.stock_quantity == 0:
                    stock_item.setBackground(QPixmap(1, 1))  # Red background for zero stock
                elif product.stock_quantity <= 2:
                    stock_item.setBackground(QPixmap(1, 1))  # Orange background for very low
                self.stock_table.setItem(row, 1, stock_item)
                
                # Sale price
                price_item = QTableWidgetItem(f"{product.sale_price:,} تومان")
                price_item.setFlags(price_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.stock_table.setItem(row, 2, price_item)
                
        except Exception as e:
            print(f"Error loading low stock products: {e}")
    
    def refresh_dashboard(self):
        """Manual refresh dashboard data"""
        self.refresh_button.setText("🔄 در حال به‌روزرسانی...")
        self.refresh_button.setEnabled(False)
        
        # Load fresh data
        self.load_dashboard_data()
        
        # Emit refresh signal
        self.refresh_requested.emit()
        
        # Reset button
        QTimer.singleShot(1000, lambda: (
            self.refresh_button.setText("🔄 به‌روزرسانی"),
            self.refresh_button.setEnabled(True)
        ))
    
    def create_backup(self):
        """Create database backup"""
        try:
            self.backup_btn.setText("💾 در حال پشتیبان‌گیری...")
            self.backup_btn.setEnabled(False)
            
            success, message = self.db_service.backup_database()
            
            # Show result in status
            if success:
                self.backup_btn.setText("✅ پشتیبان ایجاد شد")
            else:
                self.backup_btn.setText("❌ خطا در پشتیبان‌گیری")
            
            # Reset button after 3 seconds
            QTimer.singleShot(3000, lambda: (
                self.backup_btn.setText("💾 پشتیبان‌گیری"),
                self.backup_btn.setEnabled(True)
            ))
            
        except Exception as e:
            print(f"Error creating backup: {e}")
            self.backup_btn.setText("❌ خطا در پشتیبان‌گیری")
            QTimer.singleShot(3000, lambda: (
                self.backup_btn.setText("💾 پشتیبان‌گیری"),
                self.backup_btn.setEnabled(True)
            ))
    
    def get_quick_action_buttons(self):
        """Return quick action buttons for connecting to main window"""
        return {
            'new_invoice': self.new_invoice_btn,
            'new_product': self.new_product_btn,
            'reports': self.reports_btn
        }