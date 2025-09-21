"""
Reports View for Persian Invoicing System
Enhanced reporting with charts and export functionality
"""

import os
from datetime import datetime, timedelta
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                           QLabel, QPushButton, QTableWidget, QTableWidgetItem,
                           QHeaderView, QGroupBox, QDateEdit, QComboBox,
                           QTextEdit, QSplitter, QFrame, QMessageBox,
                           QFileDialog, QProgressBar)
from PyQt6.QtCore import Qt, QDate, pyqtSignal, QThread
from PyQt6.QtGui import QFont
from services.database_service import DatabaseService
import jdatetime

class ReportGeneratorThread(QThread):
    """Thread for generating reports without blocking UI"""
    
    report_ready = pyqtSignal(dict)
    progress_updated = pyqtSignal(int)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, db_service, report_type, start_date, end_date):
        super().__init__()
        self.db_service = db_service
        self.report_type = report_type
        self.start_date = start_date
        self.end_date = end_date
    
    def run(self):
        """Generate report in background"""
        try:
            self.progress_updated.emit(10)
            
            if self.report_type == "sales":
                report_data = self.generate_sales_report()
            elif self.report_type == "products":
                report_data = self.generate_products_report()
            elif self.report_type == "customers":
                report_data = self.generate_customers_report()
            else:
                report_data = {}
            
            self.progress_updated.emit(100)
            self.report_ready.emit(report_data)
            
        except Exception as e:
            self.error_occurred.emit(str(e))
    
    def generate_sales_report(self):
        """Generate sales report"""
        invoices = self.db_service.get_invoices()
        
        # Filter by date range
        filtered_invoices = []
        for invoice in invoices:
            if self.start_date <= invoice.issue_date.date() <= self.end_date:
                filtered_invoices.append(invoice)
        
        self.progress_updated.emit(50)
        
        # Calculate statistics
        total_invoices = len(filtered_invoices)
        total_revenue = sum(inv.final_amount for inv in filtered_invoices)
        total_discount = sum(inv.discount_amount for inv in filtered_invoices)
        
        # Group by date
        daily_sales = {}
        for invoice in filtered_invoices:
            date_key = invoice.issue_date.date()
            if date_key not in daily_sales:
                daily_sales[date_key] = {'count': 0, 'revenue': 0}
            daily_sales[date_key]['count'] += 1
            daily_sales[date_key]['revenue'] += invoice.final_amount
        
        self.progress_updated.emit(80)
        
        return {
            'type': 'sales',
            'summary': {
                'total_invoices': total_invoices,
                'total_revenue': total_revenue,
                'total_discount': total_discount,
                'average_invoice': total_revenue // total_invoices if total_invoices > 0 else 0
            },
            'daily_data': daily_sales,
            'invoices': filtered_invoices
        }
    
    def generate_products_report(self):
        """Generate products report"""
        products = self.db_service.get_products()
        
        self.progress_updated.emit(50)
        
        # Calculate statistics
        total_products = len(products)
        total_stock_value = sum(p.stock_quantity * p.sale_price for p in products)
        low_stock_products = [p for p in products if p.stock_quantity <= 5]
        zero_stock_products = [p for p in products if p.stock_quantity == 0]
        
        self.progress_updated.emit(80)
        
        return {
            'type': 'products',
            'summary': {
                'total_products': total_products,
                'total_stock_value': total_stock_value,
                'low_stock_count': len(low_stock_products),
                'zero_stock_count': len(zero_stock_products)
            },
            'products': products,
            'low_stock_products': low_stock_products,
            'zero_stock_products': zero_stock_products
        }
    
    def generate_customers_report(self):
        """Generate customers report"""
        invoices = self.db_service.get_invoices()
        
        # Filter by date range
        filtered_invoices = []
        for invoice in invoices:
            if self.start_date <= invoice.issue_date.date() <= self.end_date:
                filtered_invoices.append(invoice)
        
        self.progress_updated.emit(50)
        
        # Group by customer
        customers_data = {}
        for invoice in filtered_invoices:
            customer = invoice.customer_name
            if customer not in customers_data:
                customers_data[customer] = {
                    'invoice_count': 0,
                    'total_amount': 0,
                    'phone': invoice.customer_phone,
                    'last_purchase': invoice.issue_date
                }
            
            customers_data[customer]['invoice_count'] += 1
            customers_data[customer]['total_amount'] += invoice.final_amount
            
            if invoice.issue_date > customers_data[customer]['last_purchase']:
                customers_data[customer]['last_purchase'] = invoice.issue_date
        
        self.progress_updated.emit(80)
        
        return {
            'type': 'customers',
            'summary': {
                'total_customers': len(customers_data),
                'total_invoices': len(filtered_invoices),
                'total_revenue': sum(inv.final_amount for inv in filtered_invoices)
            },
            'customers_data': customers_data
        }

class ReportsView(QWidget):
    """Enhanced reports view with comprehensive reporting"""
    
    def __init__(self):
        super().__init__()
        self.db_service = DatabaseService()
        self.report_thread = None
        self.current_report_data = None
        self.setup_ui()
        self.setup_styling()
        
    def setup_ui(self):
        """Setup the reports user interface"""
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header_label = QLabel("گزارشات و آمار")
        header_label.setFont(QFont("Vazirmatn", 16, QFont.Weight.Bold))
        header_label.setStyleSheet("color: #2c3e50; margin-bottom: 15px;")
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Controls section
        controls_group = QGroupBox("تنظیمات گزارش")
        controls_layout = QGridLayout(controls_group)
        
        # Report type
        type_label = QLabel("نوع گزارش:")
        self.report_type_combo = QComboBox()
        self.report_type_combo.addItems([
            "گزارش فروش",
            "گزارش کالاها", 
            "گزارش مشتریان"
        ])
        self.report_type_combo.setFont(QFont("Vazirmatn", 11))
        
        # Date range
        start_date_label = QLabel("از تاریخ:")
        self.start_date_edit = QDateEdit()
        self.start_date_edit.setDate(QDate.currentDate().addDays(-30))
        self.start_date_edit.setCalendarPopup(True)
        self.start_date_edit.setFont(QFont("Vazirmatn", 11))
        
        end_date_label = QLabel("تا تاریخ:")
        self.end_date_edit = QDateEdit()
        self.end_date_edit.setDate(QDate.currentDate())
        self.end_date_edit.setCalendarPopup(True)
        self.end_date_edit.setFont(QFont("Vazirmatn", 11))
        
        # Buttons
        self.generate_button = QPushButton("تولید گزارش")
        self.generate_button.setFont(QFont("Vazirmatn", 11, QFont.Weight.Bold))
        self.generate_button.clicked.connect(self.generate_report)
        
        self.export_button = QPushButton("خروجی اکسل")
        self.export_button.setFont(QFont("Vazirmatn", 11, QFont.Weight.Bold))
        self.export_button.clicked.connect(self.export_report)
        self.export_button.setEnabled(False)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        
        # Add to controls layout
        controls_layout.addWidget(type_label, 0, 0)
        controls_layout.addWidget(self.report_type_combo, 0, 1)
        controls_layout.addWidget(start_date_label, 0, 2)
        controls_layout.addWidget(self.start_date_edit, 0, 3)
        controls_layout.addWidget(end_date_label, 0, 4)
        controls_layout.addWidget(self.end_date_edit, 0, 5)
        controls_layout.addWidget(self.generate_button, 1, 0, 1, 2)
        controls_layout.addWidget(self.export_button, 1, 2, 1, 2)
        controls_layout.addWidget(self.progress_bar, 1, 4, 1, 2)
        
        # Results section
        results_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Summary panel
        summary_group = QGroupBox("خلاصه آمار")
        summary_layout = QVBoxLayout(summary_group)
        
        self.summary_text = QTextEdit()
        self.summary_text.setMaximumHeight(200)
        self.summary_text.setFont(QFont("Vazirmatn", 11))
        self.summary_text.setReadOnly(True)
        summary_layout.addWidget(self.summary_text)
        
        # Data table
        table_group = QGroupBox("جزئیات گزارش")
        table_layout = QVBoxLayout(table_group)
        
        self.report_table = QTableWidget()
        self.report_table.setAlternatingRowColors(True)
        self.report_table.setFont(QFont("Vazirmatn", 10))
        table_layout.addWidget(self.report_table)
        
        # Add to splitter
        results_splitter.addWidget(summary_group)
        results_splitter.addWidget(table_group)
        results_splitter.setStretchFactor(0, 1)
        results_splitter.setStretchFactor(1, 2)
        
        # Add to main layout
        main_layout.addWidget(header_label)
        main_layout.addWidget(controls_group)
        main_layout.addWidget(results_splitter)
        
        self.setLayout(main_layout)
        
    def setup_styling(self):
        """Setup modern styling"""
        self.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
                font-family: 'Vazirmatn', Arial, sans-serif;
            }
            
            QGroupBox {
                font-weight: bold;
                border: 2px solid #dee2e6;
                border-radius: 12px;
                margin: 10px 0px;
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
            
            QComboBox, QDateEdit {
                border: 2px solid #dee2e6;
                border-radius: 6px;
                padding: 8px;
                font-size: 11pt;
                background-color: white;
                min-height: 20px;
            }
            
            QComboBox:focus, QDateEdit:focus {
                border-color: #4CAF50;
            }
            
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            
            QComboBox::down-arrow {
                image: url(down-arrow.png);
                width: 12px;
                height: 12px;
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
                min-width: 100px;
            }
            
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #45a049, stop:1 #3d8b40);
            }
            
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3d8b40, stop:1 #2e7d32);
            }
            
            QPushButton:disabled {
                background: #cccccc;
                color: #666666;
            }
            
            QTableWidget {
                border: 1px solid #dee2e6;
                border-radius: 8px;
                background-color: white;
                gridline-color: #f1f3f4;
                font-size: 10pt;
            }
            
            QTableWidget::item {
                padding: 10px 8px;
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
            
            QTextEdit {
                border: 1px solid #dee2e6;
                border-radius: 6px;
                background-color: white;
                padding: 10px;
            }
            
            QProgressBar {
                border: 2px solid #dee2e6;
                border-radius: 5px;
                background-color: #f8f9fa;
                text-align: center;
            }
            
            QProgressBar::chunk {
                background-color: #4CAF50;
                border-radius: 3px;
            }
        """)
    
    def generate_report(self):
        """Generate selected report"""
        if self.report_thread and self.report_thread.isRunning():
            return
        
        # Get parameters
        report_type_map = {
            "گزارش فروش": "sales",
            "گزارش کالاها": "products",
            "گزارش مشتریان": "customers"
        }
        
        report_type = report_type_map[self.report_type_combo.currentText()]
        start_date = self.start_date_edit.date().toPython()
        end_date = self.end_date_edit.date().toPython()
        
        # Validate date range
        if start_date > end_date:
            QMessageBox.warning(self, "خطا", "تاریخ شروع نمی‌تواند از تاریخ پایان بزرگتر باشد")
            return
        
        # Show progress
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.generate_button.setEnabled(False)
        
        # Start background thread
        self.report_thread = ReportGeneratorThread(
            self.db_service, report_type, start_date, end_date
        )
        self.report_thread.report_ready.connect(self.on_report_ready)
        self.report_thread.progress_updated.connect(self.progress_bar.setValue)
        self.report_thread.error_occurred.connect(self.on_report_error)
        self.report_thread.start()
    
    def on_report_ready(self, report_data):
        """Handle completed report"""
        self.current_report_data = report_data
        self.display_report(report_data)
        
        # Hide progress and enable buttons
        self.progress_bar.setVisible(False)
        self.generate_button.setEnabled(True)
        self.export_button.setEnabled(True)
    
    def on_report_error(self, error_message):
        """Handle report generation error"""
        QMessageBox.critical(self, "خطا", f"خطا در تولید گزارش: {error_message}")
        
        # Hide progress and enable buttons
        self.progress_bar.setVisible(False)
        self.generate_button.setEnabled(True)
        self.export_button.setEnabled(False)
    
    def display_report(self, report_data):
        """Display report data in UI"""
        report_type = report_data['type']
        
        if report_type == 'sales':
            self.display_sales_report(report_data)
        elif report_type == 'products':
            self.display_products_report(report_data)
        elif report_type == 'customers':
            self.display_customers_report(report_data)
    
    def display_sales_report(self, report_data):
        """Display sales report"""
        summary = report_data['summary']
        
        # Update summary
        summary_text = f"""
📊 خلاصه گزارش فروش

🧾 تعداد کل فاکتورها: {summary['total_invoices']:,}
💰 مجموع درآمد: {summary['total_revenue']:,} تومان
🎯 مجموع تخفیفات: {summary['total_discount']:,} تومان
📈 میانگین فاکتور: {summary['average_invoice']:,} تومان

📅 بازه زمانی: {self.start_date_edit.date().toString('yyyy/MM/dd')} تا {self.end_date_edit.date().toString('yyyy/MM/dd')}
        """
        self.summary_text.setText(summary_text.strip())
        
        # Update table
        invoices = report_data['invoices']
        self.report_table.setColumnCount(5)
        self.report_table.setHorizontalHeaderLabels([
            "شماره فاکتور", "نام مشتری", "تاریخ", "مبلغ نهایی", "تخفیف"
        ])
        self.report_table.setRowCount(len(invoices))
        
        for row, invoice in enumerate(invoices):
            # Convert to Persian date
            jdate = jdatetime.datetime.fromgregorian(datetime=invoice.issue_date)
            persian_date = jdate.strftime('%Y/%m/%d')
            
            items = [
                invoice.invoice_number,
                invoice.customer_name,
                persian_date,
                f"{invoice.final_amount:,} تومان",
                f"{invoice.discount_amount:,} تومان"
            ]
            
            for col, item in enumerate(items):
                table_item = QTableWidgetItem(str(item))
                table_item.setFlags(table_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.report_table.setItem(row, col, table_item)
        
        # Resize columns
        header = self.report_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
    
    def display_products_report(self, report_data):
        """Display products report"""
        summary = report_data['summary']
        
        # Update summary
        summary_text = f"""
📦 خلاصه گزارش کالاها

📋 تعداد کل کالاها: {summary['total_products']:,}
💎 ارزش کل موجودی: {summary['total_stock_value']:,} تومان
⚠️ کالاهای کم‌موجود: {summary['low_stock_count']:,}
❌ کالاهای ناموجود: {summary['zero_stock_count']:,}
        """
        self.summary_text.setText(summary_text.strip())
        
        # Update table
        products = report_data['products']
        self.report_table.setColumnCount(5)
        self.report_table.setHorizontalHeaderLabels([
            "نام کالا", "قیمت خرید", "قیمت فروش", "موجودی", "ارزش موجودی"
        ])
        self.report_table.setRowCount(len(products))
        
        for row, product in enumerate(products):
            stock_value = product.stock_quantity * product.sale_price
            
            items = [
                product.name,
                f"{product.purchase_price:,} تومان",
                f"{product.sale_price:,} تومان",
                f"{product.stock_quantity:,}",
                f"{stock_value:,} تومان"
            ]
            
            for col, item in enumerate(items):
                table_item = QTableWidgetItem(str(item))
                table_item.setFlags(table_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                
                # Color code low stock
                if col == 3 and product.stock_quantity <= 5:
                    if product.stock_quantity == 0:
                        table_item.setBackground(QFont().defaultFamily())  # Red
                    else:
                        table_item.setBackground(QFont().defaultFamily())  # Orange
                
                self.report_table.setItem(row, col, table_item)
        
        # Resize columns
        header = self.report_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
    
    def display_customers_report(self, report_data):
        """Display customers report"""
        summary = report_data['summary']
        
        # Update summary
        summary_text = f"""
👥 خلاصه گزارش مشتریان

👤 تعداد کل مشتریان: {summary['total_customers']:,}
🧾 تعداد کل فاکتورها: {summary['total_invoices']:,}
💰 مجموع درآمد: {summary['total_revenue']:,} تومان

📅 بازه زمانی: {self.start_date_edit.date().toString('yyyy/MM/dd')} تا {self.end_date_edit.date().toString('yyyy/MM/dd')}
        """
        self.summary_text.setText(summary_text.strip())
        
        # Update table
        customers_data = report_data['customers_data']
        self.report_table.setColumnCount(5)
        self.report_table.setHorizontalHeaderLabels([
            "نام مشتری", "تعداد فاکتور", "مجموع خرید", "شماره تماس", "آخرین خرید"
        ])
        self.report_table.setRowCount(len(customers_data))
        
        for row, (customer_name, data) in enumerate(customers_data.items()):
            # Convert to Persian date
            jdate = jdatetime.datetime.fromgregorian(datetime=data['last_purchase'])
            persian_date = jdate.strftime('%Y/%m/%d')
            
            items = [
                customer_name,
                str(data['invoice_count']),
                f"{data['total_amount']:,} تومان",
                data['phone'] or "ندارد",
                persian_date
            ]
            
            for col, item in enumerate(items):
                table_item = QTableWidgetItem(str(item))
                table_item.setFlags(table_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.report_table.setItem(row, col, table_item)
        
        # Resize columns
        header = self.report_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
    
    def export_report(self):
        """Export report to Excel"""
        if not self.current_report_data:
            QMessageBox.warning(self, "خطا", "لطفاً ابتدا گزارشی تولید کنید")
            return
        
        # Get save path
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "ذخیره گزارش",
            f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            "Excel Files (*.xlsx)"
        )
        
        if not file_path:
            return
        
        try:
            self.save_excel_report(file_path)
            QMessageBox.information(self, "موفقیت", f"گزارش در مسیر زیر ذخیره شد:\\n{file_path}")
        except Exception as e:
            QMessageBox.critical(self, "خطا", f"خطا در ذخیره فایل: {str(e)}")
    
    def save_excel_report(self, file_path):
        """Save report to Excel file"""
        try:
            import pandas as pd
            
            # Create Excel writer
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                report_type = self.current_report_data['type']
                
                if report_type == 'sales':
                    self.save_sales_excel(writer)
                elif report_type == 'products':
                    self.save_products_excel(writer)
                elif report_type == 'customers':
                    self.save_customers_excel(writer)
                    
        except ImportError:
            # Fallback to simple CSV if pandas not available
            self.save_csv_report(file_path.replace('.xlsx', '.csv'))
    
    def save_sales_excel(self, writer):
        """Save sales report to Excel"""
        import pandas as pd
        
        invoices = self.current_report_data['invoices']
        
        # Prepare data
        data = []
        for invoice in invoices:
            jdate = jdatetime.datetime.fromgregorian(datetime=invoice.issue_date)
            data.append({
                'شماره فاکتور': invoice.invoice_number,
                'نام مشتری': invoice.customer_name,
                'تاریخ': jdate.strftime('%Y/%m/%d'),
                'مبلغ نهایی': invoice.final_amount,
                'تخفیف': invoice.discount_amount
            })
        
        df = pd.DataFrame(data)
        df.to_excel(writer, sheet_name='گزارش فروش', index=False)
    
    def save_products_excel(self, writer):
        """Save products report to Excel"""
        import pandas as pd
        
        products = self.current_report_data['products']
        
        # Prepare data
        data = []
        for product in products:
            data.append({
                'نام کالا': product.name,
                'قیمت خرید': product.purchase_price,
                'قیمت فروش': product.sale_price,
                'موجودی': product.stock_quantity,
                'ارزش موجودی': product.stock_quantity * product.sale_price
            })
        
        df = pd.DataFrame(data)
        df.to_excel(writer, sheet_name='گزارش کالاها', index=False)
    
    def save_customers_excel(self, writer):
        """Save customers report to Excel"""
        import pandas as pd
        
        customers_data = self.current_report_data['customers_data']
        
        # Prepare data
        data = []
        for customer_name, customer_data in customers_data.items():
            jdate = jdatetime.datetime.fromgregorian(datetime=customer_data['last_purchase'])
            data.append({
                'نام مشتری': customer_name,
                'تعداد فاکتور': customer_data['invoice_count'],
                'مجموع خرید': customer_data['total_amount'],
                'شماره تماس': customer_data['phone'] or '',
                'آخرین خرید': jdate.strftime('%Y/%m/%d')
            })
        
        df = pd.DataFrame(data)
        df.to_excel(writer, sheet_name='گزارش مشتریان', index=False)
    
    def save_csv_report(self, file_path):
        """Save report as CSV (fallback)"""
        # Simple CSV export without pandas
        import csv
        
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            if self.current_report_data['type'] == 'sales':
                writer = csv.writer(csvfile)
                writer.writerow(['شماره فاکتور', 'نام مشتری', 'تاریخ', 'مبلغ نهایی', 'تخفیف'])
                
                for invoice in self.current_report_data['invoices']:
                    jdate = jdatetime.datetime.fromgregorian(datetime=invoice.issue_date)
                    writer.writerow([
                        invoice.invoice_number,
                        invoice.customer_name,
                        jdate.strftime('%Y/%m/%d'),
                        invoice.final_amount,
                        invoice.discount_amount
                    ])