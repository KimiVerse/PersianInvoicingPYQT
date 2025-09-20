# Dashboard View - Main statistics and recent invoices
# File: views/dashboard_view.py

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                            QLabel, QFrame, QPushButton, QTableWidget, 
                            QTableWidgetItem, QHeaderView, QSpacerItem,
                            QSizePolicy)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont
from database.models import get_db_session, Invoice, Product
from datetime import datetime, date
from sqlalchemy import func, and_

class StatCard(QFrame):
    """Modern statistics card widget"""
    
    def __init__(self, title, value, icon, color="#3B82F6"):
        super().__init__()
        self.setFixedHeight(150)
        self.setup_ui(title, value, icon, color)
    
    def setup_ui(self, title, value, icon, color):
        self.setStyleSheet(f"""
            QFrame {{
                background: #374151;
                border: 2px solid {color};
                border-radius: 15px;
                margin: 8px;
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)
        
        # Icon container
        icon_container = QFrame()
        icon_container.setFixedSize(50, 50)
        icon_container.setStyleSheet(f"""
            QFrame {{
                background: {color};
                border-radius: 12px;
                border: none;
            }}
        """)
        
        icon_layout = QVBoxLayout(icon_container)
        icon_layout.setContentsMargins(0, 0, 0, 0)
        icon_label = QLabel(icon)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet("font-size: 24px; background: transparent; color: white;")
        icon_layout.addWidget(icon_label)
        
        # Title label
        self.title_label = QLabel(title)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("""
            color: #D1D5DB;
            font-size: 14px;
            font-weight: bold;
            background: transparent;
        """)
        
        # Value label
        self.value_label = QLabel(str(value))
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.value_label.setStyleSheet(f"""
            color: {color};
            font-size: 36px;
            font-weight: bold;
            background: transparent;
        """)
        
        # Center the icon
        icon_layout_h = QHBoxLayout()
        icon_layout_h.addStretch()
        icon_layout_h.addWidget(icon_container)
        icon_layout_h.addStretch()
        
        layout.addLayout(icon_layout_h)
        layout.addWidget(self.title_label)
        layout.addWidget(self.value_label)
        layout.addStretch()
    
    def update_value(self, new_value):
        """Update the displayed value"""
        self.value_label.setText(str(new_value))

class DashboardView(QWidget):
    """Main dashboard showing statistics and recent invoices"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.setup_timer()
        self.load_dashboard_data()
    
    def setup_ui(self):
        """Setup the dashboard user interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(25)
        
        # Statistics cards
        stats_container = QWidget()
        stats_layout = QGridLayout(stats_container)
        stats_layout.setContentsMargins(0, 0, 0, 0)
        stats_layout.setSpacing(0)
        
        # Create stat cards
        self.today_invoices_card = StatCard("تعداد فاکتورهای امروز", "0", "📊", "#3B82F6")
        self.today_sales_card = StatCard("فروش کل امروز", "0 ریال", "💰", "#10B981")
        self.total_products_card = StatCard("تعداد کل کالاها", "0", "📦", "#F59E0B")
        
        stats_layout.addWidget(self.today_invoices_card, 0, 0)
        stats_layout.addWidget(self.today_sales_card, 0, 1)
        stats_layout.addWidget(self.total_products_card, 0, 2)
        
        layout.addWidget(stats_container)
        
        # Recent invoices section
        recent_invoices_frame = QFrame()
        recent_invoices_frame.setStyleSheet("""
            QFrame {
                background: #374151;
                border: 1px solid #6B7280;
                border-radius: 15px;
            }
        """)
        
        recent_layout = QVBoxLayout(recent_invoices_frame)
        recent_layout.setContentsMargins(0, 0, 0, 0)
        recent_layout.setSpacing(0)
        
        # Header
        header_frame = QFrame()
        header_frame.setFixedHeight(60)
        header_frame.setStyleSheet("""
            QFrame {
                background: #4B5563;
                border-radius: 15px 15px 0px 0px;
                border-bottom: 1px solid #6B7280;
            }
        """)
        
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(20, 0, 20, 0)
        
        header_title = QLabel("📋 فاکتورهای اخیر")
        header_title.setStyleSheet("""
            color: #F9FAFB;
            font-size: 18px;
            font-weight: bold;
            background: transparent;
        """)
        
        self.refresh_button = QPushButton("🔄 بروزرسانی")
        self.refresh_button.setStyleSheet("""
            QPushButton {
                background: #10B981;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 8px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #059669;
            }
        """)
        self.refresh_button.clicked.connect(self.load_dashboard_data)
        
        header_layout.addWidget(header_title)
        header_layout.addStretch()
        header_layout.addWidget(self.refresh_button)
        
        # Table
        self.recent_table = QTableWidget()
        self.setup_recent_table()
        
        recent_layout.addWidget(header_frame)
        recent_layout.addWidget(self.recent_table, 1)
        
        layout.addWidget(recent_invoices_frame, 1)
    
    def setup_recent_table(self):
        """Setup the recent invoices table"""
        self.recent_table.setColumnCount(4)
        self.recent_table.setHorizontalHeaderLabels([
            "شماره فاکتور", "نام مشتری", "تاریخ", "مبلغ نهایی"
        ])
        
        # Set table properties
        self.recent_table.setAlternatingRowColors(True)
        self.recent_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.recent_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.recent_table.verticalHeader().setVisible(False)
        
        # Set column widths
        header = self.recent_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        
        # Set row height
        self.recent_table.verticalHeader().setDefaultSectionSize(40)
        
        self.recent_table.setStyleSheet("""
            QTableWidget {
                background: transparent;
                border: none;
                border-radius: 0px;
                gridline-color: #6B7280;
                font-size: 14px;
            }
            QTableWidget::item {
                padding: 10px;
                border-bottom: 1px solid #6B7280;
            }
            QTableWidget::item:selected {
                background: #3B82F6;
                color: white;
            }
            QHeaderView::section {
                background: #4B5563;
                color: #F9FAFB;
                padding: 12px;
                border: none;
                border-bottom: 2px solid #6B7280;
                font-weight: bold;
                font-size: 14px;
            }
        """)
    
    def setup_timer(self):
        """Setup auto-refresh timer"""
        self.timer = QTimer()
        self.timer.timeout.connect(self.load_dashboard_data)
        self.timer.start(300000)  # Refresh every 5 minutes
    
    def load_dashboard_data(self):
        """Load dashboard statistics and recent invoices"""
        try:
            session = get_db_session()
            
            # Get today's date
            today = date.today()
            
            # Today's invoices count and total sales
            today_invoices = session.query(Invoice).filter(
                func.date(Invoice.issue_date) == today
            ).all()
            
            today_count = len(today_invoices)
            today_total = sum(invoice.final_price for invoice in today_invoices)
            
            # Total products count
            total_products = session.query(Product).count()
            
            # Update stat cards
            self.today_invoices_card.update_value(today_count)
            self.today_sales_card.update_value(f"{today_total:,.0f} ریال")
            self.total_products_card.update_value(total_products)
            
            # Recent invoices (last 10)
            recent_invoices = session.query(Invoice).order_by(
                Invoice.issue_date.desc()
            ).limit(10).all()
            
            self.populate_recent_table(recent_invoices)
            
            session.close()
            
        except Exception as e:
            print(f"Error loading dashboard data: {e}")
    
    def populate_recent_table(self, invoices):
        """Populate the recent invoices table"""
        self.recent_table.setRowCount(len(invoices))
        
        for row, invoice in enumerate(invoices):
            # Invoice number
            self.recent_table.setItem(row, 0, QTableWidgetItem(invoice.invoice_number))
            
            # Customer name
            self.recent_table.setItem(row, 1, QTableWidgetItem(invoice.customer_name))
            
            # Issue date
            date_str = invoice.issue_date.strftime("%Y/%m/%d")
            self.recent_table.setItem(row, 2, QTableWidgetItem(date_str))
            
            # Final price
            price_str = f"{invoice.final_price:,.0f} ریال"
            self.recent_table.setItem(row, 3, QTableWidgetItem(price_str))

# File: views/__init__.py
# This file makes the views directory a Python package