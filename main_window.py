# Main Application Window
# File: main_window.py

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                            QTabWidget, QLabel, QFrame, QPushButton, QTableWidget,
                            QTableWidgetItem, QLineEdit, QSpinBox, QDoubleSpinBox,
                            QComboBox, QDateEdit, QMessageBox, QHeaderView,
                            QFormLayout, QTextEdit, QSplitter)
from PyQt6.QtCore import Qt, QDate, QTimer
from PyQt6.QtGui import QFont
from database.models import get_db_session, Product, Invoice, InvoiceItem
from datetime import datetime, date
from decimal import Decimal
import random

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("سیستم مدیریت فاکتور فروش")
        self.setGeometry(100, 100, 1400, 850)
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        
        # Apply modern theme
        self.apply_theme()
        
        # Setup UI
        self.setup_ui()
        
        # Show maximized
        self.showMaximized()
    
    def apply_theme(self):
        """Apply modern Persian theme"""
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1F2937, stop:1 #111827);
                color: #F9FAFB;
            }
            
            QWidget {
                font-family: 'Segoe UI', 'Tahoma', sans-serif;
                font-size: 14px;
                color: #F9FAFB;
                background: transparent;
            }
            
            QPushButton {
                background: #3B82F6;
                color: white;
                border: none;
                padding: 10px 16px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
            }
            
            QPushButton:hover {
                background: #2563EB;
            }
            
            QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox, QDateEdit {
                background: #374151;
                border: 2px solid #6B7280;
                border-radius: 8px;
                padding: 8px 12px;
                color: #F9FAFB;
                font-size: 14px;
            }
            
            QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus, QDateEdit:focus {
                border-color: #3B82F6;
                background: #4B5563;
            }
            
            QTableWidget {
                background: #374151;
                alternate-background-color: #4B5563;
                border: 1px solid #6B7280;
                border-radius: 12px;
                gridline-color: #6B7280;
                color: #F9FAFB;
                font-size: 14px;
            }
            
            QTableWidget::item {
                padding: 8px;
                border: none;
            }
            
            QTableWidget::item:selected {
                background: #3B82F6;
                color: white;
            }
            
            QHeaderView::section {
                background: #4B5563;
                color: #F9FAFB;
                padding: 10px;
                border: 1px solid #6B7280;
                font-weight: bold;
                font-size: 14px;
            }
            
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
            
            QFrame {
                background: #374151;
                border: 1px solid #6B7280;
                border-radius: 12px;
            }
            
            QLabel {
                color: #F9FAFB;
                background: transparent;
            }
        """)
    
    def setup_ui(self):
        """Setup the main user interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header
        header = self.create_header()
        layout.addWidget(header)
        
        # Tab widget
        self.tab_widget = QTabWidget()
        
        # Create tabs
        self.dashboard_tab = self.create_dashboard_tab()
        self.products_tab = self.create_products_tab()
        self.invoice_tab = self.create_invoice_tab()
        
        self.tab_widget.addTab(self.dashboard_tab, "📈 داشبورد")
        self.tab_widget.addTab(self.products_tab, "📦 مدیریت کالاها")
        self.tab_widget.addTab(self.invoice_tab, "🧾 صدور فاکتور")
        
        layout.addWidget(self.tab_widget, 1)
        
        # Load initial data
        self.load_dashboard_data()
        self.load_products_data()
    
    def create_header(self):
        """Create application header"""
        header_frame = QFrame()
        header_frame.setFixedHeight(80)
        header_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #3B82F6, stop:1 #10B981);
                border-radius: 0px;
                border: none;
            }
        """)
        
        layout = QHBoxLayout(header_frame)
        layout.setContentsMargins(25, 20, 25, 20)
        
        # Title
        title_layout = QVBoxLayout()
        title_label = QLabel("سیستم مدیریت فاکتور فروش")
        title_label.setStyleSheet("""
            color: white;
            font-size: 24px;
            font-weight: bold;
            background: transparent;
        """)
        
        subtitle_label = QLabel("نسخه پیشرفته با قابلیت مدیریت کامل")
        subtitle_label.setStyleSheet("""
            color: #E5E7EB;
            font-size: 14px;
            background: transparent;
        """)
        
        title_layout.addWidget(title_label)
        title_layout.addWidget(subtitle_label)
        
        layout.addLayout(title_layout)
        layout.addStretch()
        
        return header_frame
    
    def create_dashboard_tab(self):
        """Create dashboard tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Stats cards
        stats_layout = QHBoxLayout()
        
        self.today_invoices_card = self.create_stat_card("تعداد فاکتورهای امروز", "0", "#3B82F6")
        self.today_sales_card = self.create_stat_card("فروش کل امروز", "0 ریال", "#10B981")
        self.total_products_card = self.create_stat_card("تعداد کل کالاها", "0", "#F59E0B")
        
        stats_layout.addWidget(self.today_invoices_card)
        stats_layout.addWidget(self.today_sales_card)
        stats_layout.addWidget(self.total_products_card)
        
        # Recent invoices table
        recent_frame = QFrame()
        recent_layout = QVBoxLayout(recent_frame)
        recent_layout.setContentsMargins(20, 20, 20, 20)
        
        recent_title = QLabel("📋 فاکتورهای اخیر")
        recent_title.setStyleSheet("font-size: 18px; font-weight: bold; background: transparent;")
        
        self.recent_table = QTableWidget()
        self.recent_table.setColumnCount(4)
        self.recent_table.setHorizontalHeaderLabels(["شماره فاکتور", "نام مشتری", "تاریخ", "مبلغ نهایی"])
        
        recent_layout.addWidget(recent_title)
        recent_layout.addWidget(self.recent_table)
        
        layout.addLayout(stats_layout)
        layout.addWidget(recent_frame, 1)
        
        return widget
    
    def create_stat_card(self, title, value, color):
        """Create a statistics card"""
        card = QFrame()
        card.setFixedHeight(120)
        card.setStyleSheet(f"""
            QFrame {{
                background: #374151;
                border: 2px solid {color};
                border-radius: 15px;
                margin: 8px;
            }}
        """)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(10)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            color: #D1D5DB;
            font-size: 14px;
            font-weight: bold;
            background: transparent;
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        value_label = QLabel(value)
        value_label.setStyleSheet(f"""
            color: {color};
            font-size: 24px;
            font-weight: bold;
            background: transparent;
        """)
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        value_label.setObjectName("stat_value")
        
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        
        return card
    
    def create_products_tab(self):
        """Create products management tab"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Products list
        list_frame = QFrame()
        list_layout = QVBoxLayout(list_frame)
        list_layout.setContentsMargins(20, 20, 20, 20)
        
        list_title = QLabel("📦 لیست کالاها")
        list_title.setStyleSheet("font-size: 18px; font-weight: bold; background: transparent;")
        
        # Search
        search_layout = QHBoxLayout()
        self.product_search = QLineEdit()
        self.product_search.setPlaceholderText("جستجو...")
        search_btn = QPushButton("🔍 جستجو")
        search_btn.clicked.connect(self.search_products)
        
        search_layout.addWidget(self.product_search)
        search_layout.addWidget(search_btn)
        
        # Products table
        self.products_table = QTableWidget()
        self.products_table.setColumnCount(5)
        self.products_table.setHorizontalHeaderLabels(["کد کالا", "نام کالا", "قیمت فروش", "موجودی", "واحد"])
        self.products_table.selectionModel().selectionChanged.connect(self.on_product_selected)
        
        list_layout.addWidget(list_title)
        list_layout.addLayout(search_layout)
        list_layout.addWidget(self.products_table)
        
        # Product form
        form_frame = QFrame()
        form_layout = QVBoxLayout(form_frame)
        form_layout.setContentsMargins(20, 20, 20, 20)
        
        form_title = QLabel("✏️ افزودن / ویرایش کالا")
        form_title.setStyleSheet("font-size: 16px; font-weight: bold; background: transparent;")
        
        # Form fields
        form_fields = QFormLayout()
        
        self.product_code_edit = QLineEdit()
        self.product_name_edit = QLineEdit()
        self.purchase_price_spin = QDoubleSpinBox()
        self.purchase_price_spin.setRange(0, 999999999)
        self.sale_price_spin = QDoubleSpinBox()
        self.sale_price_spin.setRange(0, 999999999)
        self.stock_quantity_spin = QSpinBox()
        self.stock_quantity_spin.setRange(0, 999999)
        self.unit_combo = QComboBox()
        self.unit_combo.addItems(["عدد", "کیلوگرم", "بسته", "متر", "لیتر"])
        
        form_fields.addRow("کد کالا:", self.product_code_edit)
        form_fields.addRow("نام کالا:", self.product_name_edit)
        form_fields.addRow("قیمت خرید:", self.purchase_price_spin)
        form_fields.addRow("قیمت فروش:", self.sale_price_spin)
        form_fields.addRow("موجودی:", self.stock_quantity_spin)
        form_fields.addRow("واحد:", self.unit_combo)
        
        # Buttons
        buttons_layout = QVBoxLayout()
        
        add_btn = QPushButton("➕ ثبت کالای جدید")
        add_btn.setStyleSheet("background: #10B981;")
        add_btn.clicked.connect(self.add_product)
        
        update_btn = QPushButton("✏️ ویرایش کالا")
        update_btn.clicked.connect(self.update_product)
        
        delete_btn = QPushButton("🗑️ حذف کالا")
        delete_btn.setStyleSheet("background: #EF4444;")
        delete_btn.clicked.connect(self.delete_product)
        
        buttons_layout.addWidget(add_btn)
        buttons_layout.addWidget(update_btn)
        buttons_layout.addWidget(delete_btn)
        buttons_layout.addStretch()
        
        form_layout.addWidget(form_title)
        form_layout.addLayout(form_fields)
        form_layout.addLayout(buttons_layout)
        
        # Add to main layout
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(list_frame)
        splitter.addWidget(form_frame)
        splitter.setSizes([700, 400])
        
        layout.addWidget(splitter)
        
        return widget
    
    def create_invoice_tab(self):
        """Create invoice creation tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Customer info
        customer_frame = QFrame()
        customer_layout = QHBoxLayout(customer_frame)
        customer_layout.setContentsMargins(20, 20, 20, 20)
        
        customer_layout.addWidget(QLabel("نام مشتری:"))
        self.customer_name_edit = QLineEdit()
        customer_layout.addWidget(self.customer_name_edit)
        
        customer_layout.addWidget(QLabel("شماره فاکتور:"))
        self.invoice_number_edit = QLineEdit()
        self.invoice_number_edit.setReadOnly(True)
        self.generate_invoice_number()
        customer_layout.addWidget(self.invoice_number_edit)
        
        customer_layout.addWidget(QLabel("تاریخ:"))
        self.invoice_date_edit = QDateEdit()
        self.invoice_date_edit.setDate(QDate.currentDate())
        customer_layout.addWidget(self.invoice_date_edit)
        
        # Add item section
        add_item_frame = QFrame()
        add_item_layout = QHBoxLayout(add_item_frame)
        add_item_layout.setContentsMargins(20, 20, 20, 20)
        
        add_item_layout.addWidget(QLabel("کالا:"))
        self.invoice_product_combo = QComboBox()
        add_item_layout.addWidget(self.invoice_product_combo)
        
        add_item_layout.addWidget(QLabel("تعداد:"))
        self.invoice_quantity_spin = QSpinBox()
        self.invoice_quantity_spin.setRange(1, 999999)
        add_item_layout.addWidget(self.invoice_quantity_spin)
        
        add_item_btn = QPushButton("➕ افزودن ردیف")
        add_item_btn.setStyleSheet("background: #10B981;")
        add_item_btn.clicked.connect(self.add_invoice_item)
        add_item_layout.addWidget(add_item_btn)
        
        # Invoice items table
        self.invoice_items_table = QTableWidget()
        self.invoice_items_table.setColumnCount(5)
        self.invoice_items_table.setHorizontalHeaderLabels(["کالا", "تعداد", "قیمت واحد", "مبلغ کل", "حذف"])
        
        # Totals section
        totals_frame = QFrame()
        totals_layout = QHBoxLayout(totals_frame)
        totals_layout.setContentsMargins(20, 20, 20, 20)
        
        totals_layout.addWidget(QLabel("تخفیف:"))
        self.discount_spin = QDoubleSpinBox()
        self.discount_spin.setRange(0, 999999999)
        self.discount_spin.valueChanged.connect(self.calculate_totals)
        totals_layout.addWidget(self.discount_spin)
        
        self.total_label = QLabel("مجموع: 0 ریال")
        self.total_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #10B981;")
        totals_layout.addWidget(self.total_label)
        
        save_invoice_btn = QPushButton("💾 ثبت و چاپ فاکتور")
        save_invoice_btn.setStyleSheet("background: #3B82F6; font-size: 16px; padding: 15px;")
        save_invoice_btn.clicked.connect(self.save_invoice)
        totals_layout.addWidget(save_invoice_btn)
        
        layout.addWidget(customer_frame)
        layout.addWidget(add_item_frame)
        layout.addWidget(self.invoice_items_table, 1)
        layout.addWidget(totals_frame)
        
        # Initialize invoice items list
        self.current_invoice_items = []
        
        return widget
    
    # Dashboard methods
    def load_dashboard_data(self):
        """Load dashboard statistics"""
        try:
            session = get_db_session()
            
            # Today's statistics
            today = date.today()
            today_invoices = session.query(Invoice).filter(
                Invoice.issue_date >= datetime.combine(today, datetime.min.time())
            ).all()
            
            today_count = len(today_invoices)
            today_total = sum(float(invoice.final_price) for invoice in today_invoices)
            
            # Total products
            total_products = session.query(Product).count()
            
            # Update stat cards
            self.update_stat_card(self.today_invoices_card, str(today_count))
            self.update_stat_card(self.today_sales_card, f"{today_total:,.0f} ریال")
            self.update_stat_card(self.total_products_card, str(total_products))
            
            # Recent invoices
            recent_invoices = session.query(Invoice).order_by(
                Invoice.issue_date.desc()
            ).limit(10).all()
            
            self.populate_recent_invoices(recent_invoices)
            
            session.close()
            
        except Exception as e:
            QMessageBox.critical(self, "خطا", f"خطا در بارگذاری اطلاعات داشبورد: {str(e)}")
    
    def update_stat_card(self, card, value):
        """Update stat card value"""
        value_label = card.findChild(QLabel, "stat_value")
        if value_label:
            value_label.setText(value)
    
    def populate_recent_invoices(self, invoices):
        """Populate recent invoices table"""
        self.recent_table.setRowCount(len(invoices))
        
        for row, invoice in enumerate(invoices):
            self.recent_table.setItem(row, 0, QTableWidgetItem(invoice.invoice_number))
            self.recent_table.setItem(row, 1, QTableWidgetItem(invoice.customer_name))
            self.recent_table.setItem(row, 2, QTableWidgetItem(invoice.issue_date.strftime("%Y/%m/%d")))
            self.recent_table.setItem(row, 3, QTableWidgetItem(f"{invoice.final_price:,.0f} ریال"))
    
    # Products methods
    def load_products_data(self):
        """Load products data"""
        try:
            session = get_db_session()
            products = session.query(Product).order_by(Product.product_name).all()
            
            self.populate_products_table(products)
            self.populate_invoice_products_combo(products)
            
            session.close()
            
        except Exception as e:
            QMessageBox.critical(self, "خطا", f"خطا در بارگذاری کالاها: {str(e)}")
    
    def populate_products_table(self, products):
        """Populate products table"""
        self.products_table.setRowCount(len(products))
        
        for row, product in enumerate(products):
            self.products_table.setItem(row, 0, QTableWidgetItem(product.product_code))
            self.products_table.setItem(row, 1, QTableWidgetItem(product.product_name))
            self.products_table.setItem(row, 2, QTableWidgetItem(f"{product.sale_price:,.0f}"))
            self.products_table.setItem(row, 3, QTableWidgetItem(str(product.stock_quantity)))
            self.products_table.setItem(row, 4, QTableWidgetItem(product.unit))
            
            # Store product object in first column
            self.products_table.item(row, 0).setData(Qt.ItemDataRole.UserRole, product)
    
    def populate_invoice_products_combo(self, products):
        """Populate invoice products combo"""
        self.invoice_product_combo.clear()
        self.invoice_product_combo.addItem("انتخاب کنید...", None)
        
        for product in products:
            if product.stock_quantity > 0:
                display_text = f"{product.product_name} ({product.product_code})"
                self.invoice_product_combo.addItem(display_text, product)
    
    def search_products(self):
        """Search products"""
        search_text = self.product_search.text().strip()
        
        try:
            session = get_db_session()
            
            if search_text:
                products = session.query(Product).filter(
                    (Product.product_name.contains(search_text)) |
                    (Product.product_code.contains(search_text))
                ).order_by(Product.product_name).all()
            else:
                products = session.query(Product).order_by(Product.product_name).all()
            
            self.populate_products_table(products)
            session.close()
            
        except Exception as e:
            QMessageBox.critical(self, "خطا", f"خطا در جستجو: {str(e)}")
    
    def on_product_selected(self):
        """Handle product selection"""
        selected_rows = self.products_table.selectionModel().selectedRows()
        if selected_rows:
            row = selected_rows[0].row()
            product = self.products_table.item(row, 0).data(Qt.ItemDataRole.UserRole)
            
            if product:
                self.product_code_edit.setText(product.product_code)
                self.product_name_edit.setText(product.product_name)
                self.purchase_price_spin.setValue(float(product.purchase_price))
                self.sale_price_spin.setValue(float(product.sale_price))
                self.stock_quantity_spin.setValue(product.stock_quantity)
                self.unit_combo.setCurrentText(product.unit)
    
    def add_product(self):
        """Add new product"""
        if not self.product_code_edit.text() or not self.product_name_edit.text():
            QMessageBox.warning(self, "خطا", "لطفاً کد کالا و نام کالا را وارد کنید.")
            return
        
        try:
            session = get_db_session()
            
            # Check for duplicate code
            existing = session.query(Product).filter(
                Product.product_code == self.product_code_edit.text()
            ).first()
            
            if existing:
                QMessageBox.warning(self, "خطا", "کد کالای وارد شده قبلاً استفاده شده است.")
                session.close()
                return
            
            product = Product(
                product_code=self.product_code_edit.text(),
                product_name=self.product_name_edit.text(),
                purchase_price=Decimal(str(self.purchase_price_spin.value())),
                sale_price=Decimal(str(self.sale_price_spin.value())),
                stock_quantity=self.stock_quantity_spin.value(),
                unit=self.unit_combo.currentText()
            )
            
            session.add(product)
            session.commit()
            session.close()
            
            QMessageBox.information(self, "موفقیت", "کالا با موفقیت اضافه شد.")
            self.clear_product_form()
            self.load_products_data()
            
        except Exception as e:
            QMessageBox.critical(self, "خطا", f"خطا در افزودن کالا: {str(e)}")
    
    def update_product(self):
        """Update selected product"""
        selected_rows = self.products_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "خطا", "لطفاً یک کالا برای ویرایش انتخاب کنید.")
            return
        
        try:
            row = selected_rows[0].row()
            product = self.products_table.item(row, 0).data(Qt.ItemDataRole.UserRole)
            
            session = get_db_session()
            db_product = session.query(Product).filter(Product.id == product.id).first()
            
            if db_product:
                db_product.product_code = self.product_code_edit.text()
                db_product.product_name = self.product_name_edit.text()
                db_product.purchase_price = Decimal(str(self.purchase_price_spin.value()))
                db_product.sale_price = Decimal(str(self.sale_price_spin.value()))
                db_product.stock_quantity = self.stock_quantity_spin.value()
                db_product.unit = self.unit_combo.currentText()
                
                session.commit()
                session.close()
                
                QMessageBox.information(self, "موفقیت", "کالا با موفقیت ویرایش شد.")
                self.clear_product_form()
                self.load_products_data()
            
        except Exception as e:
            QMessageBox.critical(self, "خطا", f"خطا در ویرایش کالا: {str(e)}")
    
    def delete_product(self):
        """Delete selected product"""
        selected_rows = self.products_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "خطا", "لطفاً یک کالا برای حذف انتخاب کنید.")
            return
        
        reply = QMessageBox.question(
            self, "تأیید حذف",
            "آیا از حذف این کالا اطمینان دارید؟",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                row = selected_rows[0].row()
                product = self.products_table.item(row, 0).data(Qt.ItemDataRole.UserRole)
                
                session = get_db_session()
                db_product = session.query(Product).filter(Product.id == product.id).first()
                
                if db_product:
                    session.delete(db_product)
                    session.commit()
                    session.close()
                    
                    QMessageBox.information(self, "موفقیت", "کالا با موفقیت حذف شد.")
                    self.clear_product_form()
                    self.load_products_data()
                
            except Exception as e:
                QMessageBox.critical(self, "خطا", f"خطا در حذف کالا: {str(e)}")
    
    def clear_product_form(self):
        """Clear product form"""
        self.product_code_edit.clear()
        self.product_name_edit.clear()
        self.purchase_price_spin.setValue(0)
        self.sale_price_spin.setValue(0)
        self.stock_quantity_spin.setValue(0)
        self.unit_combo.setCurrentIndex(0)
    
    # Invoice methods
    def generate_invoice_number(self):
        """Generate new invoice number"""
        timestamp = datetime.now().strftime("%Y%m%d")
        random_num = random.randint(1000, 9999)
        invoice_number = f"INV-{timestamp}-{random_num}"
        self.invoice_number_edit.setText(invoice_number)
    
    def add_invoice_item(self):
        """Add item to current invoice"""
        if self.invoice_product_combo.currentIndex() == 0:
            QMessageBox.warning(self, "خطا", "لطفاً یک کالا انتخاب کنید.")
            return
        
        product = self.invoice_product_combo.currentData()
        quantity = self.invoice_quantity_spin.value()
        
        if quantity > product.stock_quantity:
            QMessageBox.warning(self, "خطا", f"موجودی کافی نیست. موجودی فعلی: {product.stock_quantity}")
            return
        
        # Check if product already exists in items
        for item in self.current_invoice_items:
            if item['product'].id == product.id:
                item['quantity'] += quantity
                item['row_total'] = item['quantity'] * item['unit_price']
                break
        else:
            # Add new item
            item = {
                'product': product,
                'quantity': quantity,
                'unit_price': float(product.sale_price),
                'row_total': quantity * float(product.sale_price)
            }
            self.current_invoice_items.append(item)
        
        self.refresh_invoice_items_table()
        self.calculate_totals()
        
        # Reset form
        self.invoice_product_combo.setCurrentIndex(0)
        self.invoice_quantity_spin.setValue(1)
    
    def refresh_invoice_items_table(self):
        """Refresh invoice items table"""
        self.invoice_items_table.setRowCount(len(self.current_invoice_items))
        
        for row, item in enumerate(self.current_invoice_items):
            self.invoice_items_table.setItem(row, 0, QTableWidgetItem(item['product'].product_name))
            self.invoice_items_table.setItem(row, 1, QTableWidgetItem(str(item['quantity'])))
            self.invoice_items_table.setItem(row, 2, QTableWidgetItem(f"{item['unit_price']:,.0f}"))
            self.invoice_items_table.setItem(row, 3, QTableWidgetItem(f"{item['row_total']:,.0f}"))
            
            # Delete button
            delete_btn = QPushButton("🗑️")
            delete_btn.setStyleSheet("background: #EF4444; max-width: 30px;")
            delete_btn.clicked.connect(lambda checked, r=row: self.remove_invoice_item(r))
            self.invoice_items_table.setCellWidget(row, 4, delete_btn)
    
    def remove_invoice_item(self, row):
        """Remove item from invoice"""
        if 0 <= row < len(self.current_invoice_items):
            self.current_invoice_items.pop(row)
            self.refresh_invoice_items_table()
            self.calculate_totals()
    
    def calculate_totals(self):
        """Calculate invoice totals"""
        subtotal = sum(item['row_total'] for item in self.current_invoice_items)
        discount = self.discount_spin.value()
        final_total = subtotal - discount
        
        self.total_label.setText(f"مجموع: {final_total:,.0f} ریال")
    
    def save_invoice(self):
        """Save current invoice"""
        if not self.customer_name_edit.text().strip():
            QMessageBox.warning(self, "خطا", "لطفاً نام مشتری را وارد کنید.")
            return
        
        if not self.current_invoice_items:
            QMessageBox.warning(self, "خطا", "لطفاً حداقل یک کالا به فاکتور اضافه کنید.")
            return
        
        try:
            session = get_db_session()
            
            # Calculate totals
            subtotal = sum(item['row_total'] for item in self.current_invoice_items)
            discount = Decimal(str(self.discount_spin.value()))
            final_total = subtotal - discount
            
            # Create invoice
            invoice = Invoice(
                invoice_number=self.invoice_number_edit.text(),
                customer_name=self.customer_name_edit.text().strip(),
                issue_date=self.invoice_date_edit.date().toPython(),
                total_price=Decimal(str(subtotal)),
                discount=discount,
                final_price=Decimal(str(final_total))
            )
            
            session.add(invoice)
            session.flush()  # Get the invoice ID
            
            # Add invoice items and update stock
            for item_data in self.current_invoice_items:
                invoice_item = InvoiceItem(
                    invoice_id=invoice.id,
                    product_id=item_data['product'].id,
                    quantity=item_data['quantity'],
                    unit_price=Decimal(str(item_data['unit_price'])),
                    row_total=Decimal(str(item_data['row_total']))
                )
                session.add(invoice_item)
                
                # Update product stock
                product = session.query(Product).filter(Product.id == item_data['product'].id).first()
                if product:
                    product.stock_quantity -= item_data['quantity']
            
            session.commit()
            session.close()
            
            QMessageBox.information(self, "موفقیت", f"فاکتور شماره {invoice.invoice_number} با موفقیت ثبت شد.")
            
            # Clear form
            self.clear_invoice_form()
            self.load_products_data()
            self.load_dashboard_data()
            
        except Exception as e:
            QMessageBox.critical(self, "خطا", f"خطا در ثبت فاکتور: {str(e)}")
    
    def clear_invoice_form(self):
        """Clear invoice form"""
        self.customer_name_edit.clear()
        self.current_invoice_items.clear()
        self.discount_spin.setValue(0)
        self.invoice_date_edit.setDate(QDate.currentDate())
        self.generate_invoice_number()
        self.refresh_invoice_items_table()
        self.calculate_totals()