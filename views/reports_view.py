# Advanced Reports View with Charts and Export
# File: views/reports_view.py

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                            QLabel, QFrame, QPushButton, QDateEdit, QTableWidget,
                            QTableWidgetItem, QHeaderView, QMessageBox, QComboBox,
                            QSpinBox, QSplitter, QScrollArea, QTextEdit,
                            QProgressBar, QFileDialog, QTabWidget, QGroupBox)
from PyQt6.QtCore import Qt, QDate, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QPainter, QPen, QBrush, QColor
from database.models import get_db_session, Product, Invoice, InvoiceItem
from services.report_service import ReportService
from datetime import datetime, date, timedelta
from decimal import Decimal
import csv
import json

# Simple chart widget (since we don't want external dependencies)
class SimpleBarChart(QWidget):
    """Simple bar chart widget"""
    
    def __init__(self, data=None, title="Chart"):
        super().__init__()
        self.data = data or []
        self.title = title
        self.setMinimumHeight(300)
        self.setStyleSheet("background: #374151; border-radius: 8px;")
    
    def set_data(self, data, title="Chart"):
        """Set chart data"""
        self.data = data
        self.title = title
        self.update()
    
    def paintEvent(self, event):
        """Paint the chart"""
        if not self.data:
            return
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Background
        painter.fillRect(self.rect(), QColor("#374151"))
        
        # Chart area
        margin = 50
        chart_rect = self.rect().adjusted(margin, margin, -margin, -margin)
        
        # Title
        painter.setPen(QColor("#F9FAFB"))
        painter.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title_rect = self.rect().adjusted(0, 10, 0, -self.rect().height() + 40)
        painter.drawText(title_rect, Qt.AlignmentFlag.AlignCenter, self.title)
        
        if not self.data:
            return
        
        # Calculate max value
        max_value = max(item['value'] for item in self.data)
        if max_value == 0:
            return
        
        # Draw bars
        bar_width = chart_rect.width() // len(self.data) - 10
        colors = ["#3B82F6", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6", "#F97316"]
        
        for i, item in enumerate(self.data):
            color = QColor(colors[i % len(colors)])
            brush = QBrush(color)
            painter.setBrush(brush)
            painter.setPen(QPen(color))
            
            bar_height = int((item['value'] / max_value) * chart_rect.height() * 0.8)
            x = chart_rect.left() + i * (bar_width + 10)
            y = chart_rect.bottom() - bar_height
            
            # Draw bar
            painter.drawRect(x, y, bar_width, bar_height)
            
            # Draw label
            painter.setPen(QColor("#F9FAFB"))
            painter.setFont(QFont("Arial", 10))
            label_rect = self.rect().adjusted(x, chart_rect.bottom() + 5, 
                                           x + bar_width - chart_rect.width(), 
                                           chart_rect.bottom() + 25)
            painter.drawText(x, chart_rect.bottom() + 20, item['label'][:10] + "...")
            
            # Draw value
            painter.drawText(x, y - 5, f"{item['value']:,.0f}")

class ReportWorker(QThread):
    """Background worker for generating reports"""
    
    progress_updated = pyqtSignal(int)
    report_ready = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, report_type, start_date, end_date):
        super().__init__()
        self.report_type = report_type
        self.start_date = start_date
        self.end_date = end_date
    
    def run(self):
        """Generate report in background"""
        try:
            self.progress_updated.emit(10)
            
            if self.report_type == "sales":
                report_data = ReportService.generate_sales_report(
                    self.start_date, self.end_date
                )
            elif self.report_type == "products":
                report_data = ReportService.generate_product_report()
            else:
                report_data = {}
            
            self.progress_updated.emit(100)
            self.report_ready.emit(report_data)
            
        except Exception as e:
            self.error_occurred.emit(str(e))

class SalesReportTab(QWidget):
    """Sales report tab"""
    
    def __init__(self):
        super().__init__()
        self.report_data = {}
        self.setup_ui()
    
    def setup_ui(self):
        """Setup sales report UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Date range selection
        date_frame = QFrame()
        date_frame.setStyleSheet("""
            QFrame {
                background: #374151;
                border: 1px solid #6B7280;
                border-radius: 12px;
                padding: 20px;
            }
        """)
        
        date_layout = QHBoxLayout(date_frame)
        
        start_label = QLabel("از تاریخ:")
        start_label.setStyleSheet("font-weight: bold; background: transparent;")
        self.start_date = QDateEdit()
        self.start_date.setDate(QDate.currentDate().addDays(-30))
        self.start_date.setCalendarPopup(True)
        
        end_label = QLabel("تا تاریخ:")
        end_label.setStyleSheet("font-weight: bold; background: transparent;")
        self.end_date = QDateEdit()
        self.end_date.setDate(QDate.currentDate())
        self.end_date.setCalendarPopup(True)
        
        generate_button = QPushButton("📊 تولید گزارش")
        generate_button.setFixedHeight(40)
        generate_button.setStyleSheet("""
            QPushButton {
                background: #10B981;
                color: white;
                font-weight: bold;
                border-radius: 8px;
                padding: 0px 20px;
            }
            QPushButton:hover {
                background: #059669;
            }
        """)
        generate_button.clicked.connect(self.generate_report)
        
        export_button = QPushButton("📁 خروجی CSV")
        export_button.setFixedHeight(40)
        export_button.clicked.connect(self.export_to_csv)
        
        date_layout.addWidget(start_label)
        date_layout.addWidget(self.start_date)
        date_layout.addWidget(end_label)
        date_layout.addWidget(self.end_date)
        date_layout.addStretch()
        date_layout.addWidget(generate_button)
        date_layout.addWidget(export_button)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        
        # Splitter for chart and table
        splitter = QSplitter(Qt.Orientation.Vertical)
        
        # Summary cards and chart
        summary_frame = QFrame()
        summary_frame.setStyleSheet("""
            QFrame {
                background: #374151;
                border: 1px solid #6B7280;
                border-radius: 12px;
            }
        """)
        
        summary_layout = QVBoxLayout(summary_frame)
        summary_layout.setContentsMargins(20, 20, 20, 20)
        
        # Summary statistics
        stats_layout = QHBoxLayout()
        
        self.total_sales_label = self.create_stat_card("💰 مجموع فروش", "0 ریال", "#10B981")
        self.total_invoices_label = self.create_stat_card("🧾 تعداد فاکتور", "0", "#3B82F6")
        self.average_sale_label = self.create_stat_card("📊 میانگین فروش", "0 ریال", "#F59E0B")
        self.total_discount_label = self.create_stat_card("🏷️ کل تخفیف", "0 ریال", "#EF4444")
        
        stats_layout.addWidget(self.total_sales_label)
        stats_layout.addWidget(self.total_invoices_label)
        stats_layout.addWidget(self.average_sale_label)
        stats_layout.addWidget(self.total_discount_label)
        
        # Chart
        self.sales_chart = SimpleBarChart(title="نمودار فروش روزانه")
        
        summary_layout.addLayout(stats_layout)
        summary_layout.addWidget(self.sales_chart, 1)
        
        # Detailed table
        table_frame = QFrame()
        table_frame.setStyleSheet("""
            QFrame {
                background: #374151;
                border: 1px solid #6B7280;
                border-radius: 12px;
            }
        """)
        
        table_layout = QVBoxLayout(table_frame)
        table_layout.setContentsMargins(0, 0, 0, 0)
        
        table_header = QLabel("📋 جزئیات فاکتورها")
        table_header.setStyleSheet("""
            background: #4B5563;
            color: #F9FAFB;
            font-size: 16px;
            font-weight: bold;
            padding: 15px 20px;
            border-radius: 12px 12px 0px 0px;
        """)
        
        self.sales_table = QTableWidget()
        self.setup_sales_table()
        
        table_layout.addWidget(table_header)
        table_layout.addWidget(self.sales_table, 1)
        
        splitter.addWidget(summary_frame)
        splitter.addWidget(table_frame)
        splitter.setSizes([400, 300])
        
        layout.addWidget(date_frame)
        layout.addWidget(self.progress_bar)
        layout.addWidget(splitter, 1)
    
    def create_stat_card(self, title, value, color):
        """Create a statistics card"""
        card = QFrame()
        card.setFixedHeight(100)
        card.setStyleSheet(f"""
            QFrame {{
                background: #4B5563;
                border: 2px solid {color};
                border-radius: 8px;
                margin: 5px;
            }}
        """)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(15, 10, 15, 10)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            color: #D1D5DB;
            font-size: 12px;
            font-weight: bold;
            background: transparent;
        """)
        
        value_label = QLabel(value)
        value_label.setStyleSheet(f"""
            color: {color};
            font-size: 18px;
            font-weight: bold;
            background: transparent;
        """)
        value_label.setObjectName("stat_value")
        
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        
        return card
    
    def setup_sales_table(self):
        """Setup sales table"""
        self.sales_table.setColumnCount(5)
        self.sales_table.setHorizontalHeaderLabels([
            "شماره فاکتور", "نام مشتری", "تاریخ", "مجموع", "مبلغ نهایی"
        ])
        
        # Set table properties
        self.sales_table.setAlternatingRowColors(True)
        self.sales_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.sales_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.sales_table.verticalHeader().setVisible(False)
        
        # Set column widths
        header = self.sales_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        
        self.sales_table.setStyleSheet("""
            QTableWidget {
                background: transparent;
                border: none;
                gridline-color: #6B7280;
                font-size: 14px;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #6B7280;
            }
            QTableWidget::item:selected {
                background: #3B82F6;
                color: white;
            }
            QHeaderView::section {
                background: #4B5563;
                color: #F9FAFB;
                padding: 10px;
                border: none;
                border-bottom: 2px solid #6B7280;
                font-weight: bold;
                font-size: 14px;
            }
        """)
    
    def generate_report(self):
        """Generate sales report"""
        start = self.start_date.date().toPython()
        end = self.end_date.date().toPython()
        
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        # Create worker thread
        self.worker = ReportWorker("sales", start, end)
        self.worker.progress_updated.connect(self.progress_bar.setValue)
        self.worker.report_ready.connect(self.display_sales_report)
        self.worker.error_occurred.connect(self.handle_error)
        self.worker.start()
    
    def display_sales_report(self, report_data):
        """Display the generated report"""
        self.report_data = report_data
        self.progress_bar.setVisible(False)
        
        # Update summary cards
        total_sales = report_data.get('total_sales', 0)
        total_invoices = report_data.get('total_invoices', 0)
        average_sale = report_data.get('average_sale', 0)
        total_discount = report_data.get('total_discount', 0)
        
        # Find value labels and update them
        cards = [self.total_sales_label, self.total_invoices_label, 
                self.average_sale_label, self.total_discount_label]
        values = [
            f"{total_sales:,.0f} ریال",
            f"{total_invoices}",
            f"{average_sale:,.0f} ریال",
            f"{total_discount:,.0f} ریال"
        ]
        
        for card, value in zip(cards, values):
            value_label = card.findChild(QLabel, "stat_value")
            if value_label:
                value_label.setText(value)
        
        # Update chart - group by date
        chart_data = self.prepare_chart_data(report_data.get('invoices', []))
        self.sales_chart.set_data(chart_data, "نمودار فروش روزانه")
        
        # Update table
        self.populate_sales_table(report_data.get('invoices', []))
    
    def prepare_chart_data(self, invoices):
        """Prepare data for chart"""
        daily_sales = {}
        
        for invoice in invoices:
            date_str = invoice.issue_date.strftime("%m/%d")
            if date_str not in daily_sales:
                daily_sales[date_str] = 0
            daily_sales[date_str] += float(invoice.final_price)
        
        # Convert to chart format
        chart_data = []
        for date_str, amount in sorted(daily_sales.items()):
            chart_data.append({
                'label': date_str,
                'value': amount
            })
        
        return chart_data[:7]  # Show last 7 days
    
    def populate_sales_table(self, invoices):
        """Populate sales table"""
        self.sales_table.setRowCount(len(invoices))
        
        for row, invoice in enumerate(invoices):
            self.sales_table.setItem(row, 0, QTableWidgetItem(invoice.invoice_number))
            self.sales_table.setItem(row, 1, QTableWidgetItem(invoice.customer_name))
            self.sales_table.setItem(row, 2, QTableWidgetItem(invoice.issue_date.strftime("%Y/%m/%d")))
            self.sales_table.setItem(row, 3, QTableWidgetItem(f"{invoice.total_price:,.0f} ریال"))
            self.sales_table.setItem(row, 4, QTableWidgetItem(f"{invoice.final_price:,.0f} ریال"))
    
    def export_to_csv(self):
        """Export report to CSV"""
        if not self.report_data:
            QMessageBox.warning(self, "خطا", "ابتدا گزارش را تولید کنید.")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, "ذخیره گزارش", "sales_report.csv", "CSV Files (*.csv)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
                    writer = csv.writer(csvfile)
                    
                    # Header
                    writer.writerow(["شماره فاکتور", "نام مشتری", "تاریخ", "مجموع", "تخفیف", "مبلغ نهایی"])
                    
                    # Data
                    for invoice in self.report_data.get('invoices', []):
                        writer.writerow([
                            invoice.invoice_number,
                            invoice.customer_name,
                            invoice.issue_date.strftime("%Y/%m/%d"),
                            float(invoice.total_price),
                            float(invoice.discount),
                            float(invoice.final_price)
                        ])
                
                QMessageBox.information(self, "موفقیت", f"گزارش در {file_path} ذخیره شد.")
                
            except Exception as e:
                QMessageBox.critical(self, "خطا", f"خطا در ذخیره فایل: {str(e)}")
    
    def handle_error(self, error_msg):
        """Handle worker error"""
        self.progress_bar.setVisible(False)
        QMessageBox.critical(self, "خطا", f"خطا در تولید گزارش: {error_msg}")

class ProductReportTab(QWidget):
    """Product inventory report tab"""
    
    def __init__(self):
        super().__init__()
        self.report_data = {}
        self.setup_ui()
        self.generate_report()
    
    def setup_ui(self):
        """Setup product report UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Control buttons
        controls_frame = QFrame()
        controls_frame.setStyleSheet("""
            QFrame {
                background: #374151;
                border: 1px solid #6B7280;
                border-radius: 12px;
                padding: 15px;
            }
        """)
        
        controls_layout = QHBoxLayout(controls_frame)
        
        refresh_button = QPushButton("🔄 بروزرسانی")
        refresh_button.clicked.connect(self.generate_report)
        
        export_button = QPushButton("📁 خروجی CSV")
        export_button.clicked.connect(self.export_to_csv)
        
        controls_layout.addStretch()
        controls_layout.addWidget(refresh_button)
        controls_layout.addWidget(export_button)
        
        # Summary cards
        summary_frame = QFrame()
        summary_frame.setStyleSheet("""
            QFrame {
                background: #374151;
                border: 1px solid #6B7280;
                border-radius: 12px;
                padding: 20px;
            }
        """)
        
        summary_layout = QHBoxLayout(summary_frame)
        
        self.total_products_card = self.create_stat_card("📦 کل محصولات", "0", "#3B82F6")
        self.out_of_stock_card = self.create_stat_card("❌ ناموجود", "0", "#EF4444")
        self.low_stock_card = self.create_stat_card("⚠️ موجودی کم", "0", "#F59E0B")
        self.inventory_value_card = self.create_stat_card("💰 ارزش کل", "0 ریال", "#10B981")
        
        summary_layout.addWidget(self.total_products_card)
        summary_layout.addWidget(self.out_of_stock_card)
        summary_layout.addWidget(self.low_stock_card)
        summary_layout.addWidget(self.inventory_value_card)
        
        # Products table
        table_frame = QFrame()
        table_frame.setStyleSheet("""
            QFrame {
                background: #374151;
                border: 1px solid #6B7280;
                border-radius: 12px;
            }
        """)
        
        table_layout = QVBoxLayout(table_frame)
        table_layout.setContentsMargins(0, 0, 0, 0)
        
        table_header = QLabel("📋 جزئیات محصولات")
        table_header.setStyleSheet("""
            background: #4B5563;
            color: #F9FAFB;
            font-size: 16px;
            font-weight: bold;
            padding: 15px 20px;
            border-radius: 12px 12px 0px 0px;
        """)
        
        self.products_table = QTableWidget()
        self.setup_products_table()
        
        table_layout.addWidget(table_header)
        table_layout.addWidget(self.products_table, 1)
        
        layout.addWidget(controls_frame)
        layout.addWidget(summary_frame)
        layout.addWidget(table_frame, 1)
    
    def create_stat_card(self, title, value, color):
        """Create a statistics card"""
        card = QFrame()
        card.setFixedHeight(100)
        card.setStyleSheet(f"""
            QFrame {{
                background: #4B5563;
                border: 2px solid {color};
                border-radius: 8px;
                margin: 5px;
            }}
        """)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(15, 10, 15, 10)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            color: #D1D5DB;
            font-size: 12px;
            font-weight: bold;
            background: transparent;
        """)
        
        value_label = QLabel(value)
        value_label.setStyleSheet(f"""
            color: {color};
            font-size: 18px;
            font-weight: bold;
            background: transparent;
        """)
        value_label.setObjectName("stat_value")
        
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        
        return card
    
    def setup_products_table(self):
        """Setup products table"""
        self.products_table.setColumnCount(6)
        self.products_table.setHorizontalHeaderLabels([
            "کد کالا", "نام کالا", "موجودی", "واحد", "قیمت خرید", "ارزش کل"
        ])
        
        # Set table properties
        self.products_table.setAlternatingRowColors(True)
        self.products_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.products_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.products_table.verticalHeader().setVisible(False)
        
        # Set column widths
        header = self.products_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        
        self.products_table.setStyleSheet("""
            QTableWidget {
                background: transparent;
                border: none;
                gridline-color: #6B7280;
                font-size: 14px;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #6B7280;
            }
            QTableWidget::item:selected {
                background: #3B82F6;
                color: white;
            }
            QHeaderView::section {
                background: #4B5563;
                color: #F9FAFB;
                padding: 10px;
                border: none;
                border-bottom: 2px solid #6B7280;
                font-weight: bold;
                font-size: 14px;
            }
        """)
    
    def generate_report(self):
        """Generate product report"""
        try:
            self.report_data = ReportService.generate_product_report()
            self.display_product_report()
        except Exception as e:
            QMessageBox.critical(self, "خطا", f"خطا در تولید گزارش: {str(e)}")
    
    def display_product_report(self):
        """Display product report"""
        # Update summary cards
        total_products = self.report_data.get('total_products', 0)
        out_of_stock = self.report_data.get('out_of_stock', 0)
        low_stock = self.report_data.get('low_stock', 0)
        inventory_value = self.report_data.get('total_inventory_value', 0)
        
        cards = [self.total_products_card, self.out_of_stock_card, 
                self.low_stock_card, self.inventory_value_card]
        values = [
            f"{total_products}",
            f"{out_of_stock}",
            f"{low_stock}",
            f"{inventory_value:,.0f} ریال"
        ]
        
        for card, value in zip(cards, values):
            value_label = card.findChild(QLabel, "stat_value")
            if value_label:
                value_label.setText(value)
        
        # Update table
        self.populate_products_table(self.report_data.get('products', []))
    
    def populate_products_table(self, products):
        """Populate products table"""
        self.products_table.setRowCount(len(products))
        
        for row, product in enumerate(products):
            # Color code based on stock level
            stock_color = "#F9FAFB"  # Default
            if product.stock_quantity == 0:
                stock_color = "#EF4444"  # Red for out of stock
            elif product.stock_quantity <= 5:
                stock_color = "#F59E0B"  # Orange for low stock
            
            self.products_table.setItem(row, 0, QTableWidgetItem(product.product_code))
            self.products_table.setItem(row, 1, QTableWidgetItem(product.product_name))
            
            stock_item = QTableWidgetItem(str(product.stock_quantity))
            stock_item.setForeground(QColor(stock_color))
            self.products_table.setItem(row, 2, stock_item)
            
            self.products_table.setItem(row, 3, QTableWidgetItem(product.unit))
            self.products_table.setItem(row, 4, QTableWidgetItem(f"{product.purchase_price:,.0f} ریال"))
            
            total_value = product.stock_quantity * product.purchase_price
            self.products_table.setItem(row, 5, QTableWidgetItem(f"{total_value:,.0f} ریال"))
    
    def export_to_csv(self):
        """Export report to CSV"""
        if not self.report_data:
            QMessageBox.warning(self, "خطا", "ابتدا گزارش را تولید کنید.")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, "ذخیره گزارش", "product_report.csv", "CSV Files (*.csv)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
                    writer = csv.writer(csvfile)
                    
                    # Header
                    writer.writerow(["کد کالا", "نام کالا", "موجودی", "واحد", "قیمت خرید", "قیمت فروش", "ارزش کل"])
                    
                    # Data
                    for product in self.report_data.get('products', []):
                        total_value = product.stock_quantity * product.purchase_price
                        writer.writerow([
                            product.product_code,
                            product.product_name,
                            product.stock_quantity,
                            product.unit,
                            float(product.purchase_price),
                            float(product.sale_price),
                            float(total_value)
                        ])
                
                QMessageBox.information(self, "موفقیت", f"گزارش در {file_path} ذخیره شد.")
                
            except Exception as e:
                QMessageBox.critical(self, "خطا", f"خطا در ذخیره فایل: {str(e)}")

class ReportsView(QWidget):
    """Main reports view with multiple report types"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        """Setup reports view UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(0)
        
        # Tab widget for different report types
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget {
                background: transparent;
                border: none;
            }
            QTabWidget::pane {
                border: 1px solid #374151;
                background: #1F2937;
                border-radius: 12px;
                margin-top: 5px;
            }
            QTabBar::tab {
                background: #374151;
                color: #F9FAFB;
                padding: 12px 20px;
                margin: 2px;
                border-radius: 12px 12px 0px 0px;
                font-size: 15px;
                font-weight: bold;
                min-width: 150px;
            }
            QTabBar::tab:selected {
                background: #3B82F6;
                color: white;
            }
            QTabBar::tab:hover {
                background: #4B5563;
            }
        """)
        
        # Add report tabs
        self.sales_report = SalesReportTab()
        self.product_report = ProductReportTab()
        
        self.tab_widget.addTab(self.sales_report, "📊 گزارش فروش")
        self.tab_widget.addTab(self.product_report, "📦 گزارش موجودی")
        
        layout.addWidget(self.tab_widget)