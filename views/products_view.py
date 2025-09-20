# Products Management View
# File: views/products_view.py

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                            QLabel, QFrame, QPushButton, QLineEdit, QTableWidget,
                            QTableWidgetItem, QHeaderView, QMessageBox, QComboBox,
                            QDoubleSpinBox, QSpinBox, QSplitter, QScrollArea)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QIntValidator, QDoubleValidator
from database.models import get_db_session, Product
from sqlalchemy.exc import IntegrityError
from decimal import Decimal

class ProductForm(QFrame):
    """Product add/edit form widget"""
    
    product_saved = pyqtSignal()  # Signal emitted when a product is saved
    
    def __init__(self):
        super().__init__()
        self.current_product = None
        self.setup_ui()
        self.clear_form()
    
    def setup_ui(self):
        """Setup the product form UI"""
        self.setStyleSheet("""
            QFrame {
                background: #374151;
                border: 1px solid #6B7280;
                border-radius: 15px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
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
        
        header_title = QLabel("✏️ افزودن / ویرایش کالا")
        header_title.setStyleSheet("""
            color: #F9FAFB;
            font-size: 16px;
            font-weight: bold;
            background: transparent;
        """)
        header_layout.addWidget(header_title)
        
        # Form content in scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setStyleSheet("QScrollArea { background: transparent; border: none; }")
        
        form_widget = QWidget()
        form_layout = QVBoxLayout(form_widget)
        form_layout.setContentsMargins(20, 20, 20, 20)
        form_layout.setSpacing(15)
        
        # Product Code
        code_label = QLabel("کد کالا:")
        code_label.setStyleSheet("font-weight: bold; background: transparent;")
        self.code_edit = QLineEdit()
        self.code_edit.setPlaceholderText("کد یکتا کالا را وارد کنید")
        
        # Product Name
        name_label = QLabel("نام کالا:")
        name_label.setStyleSheet("font-weight: bold; background: transparent;")
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("نام کالا را وارد کنید")
        
        # Purchase Price
        purchase_label = QLabel("قیمت خرید:")
        purchase_label.setStyleSheet("font-weight: bold; background: transparent;")
        self.purchase_spin = QDoubleSpinBox()
        self.purchase_spin.setRange(0, 999999999)
        self.purchase_spin.setDecimals(0)
        self.purchase_spin.setSuffix(" ریال")
        
        # Sale Price
        sale_label = QLabel("قیمت فروش:")
        sale_label.setStyleSheet("font-weight: bold; background: transparent;")
        self.sale_spin = QDoubleSpinBox()
        self.sale_spin.setRange(0, 999999999)
        self.sale_spin.setDecimals(0)
        self.sale_spin.setSuffix(" ریال")
        
        # Stock Quantity
        stock_label = QLabel("موجودی:")
        stock_label.setStyleSheet("font-weight: bold; background: transparent;")
        self.stock_spin = QSpinBox()
        self.stock_spin.setRange(0, 999999)
        
        # Unit
        unit_label = QLabel("واحد:")
        unit_label.setStyleSheet("font-weight: bold; background: transparent;")
        self.unit_combo = QComboBox()
        self.unit_combo.addItems(["عدد", "کیلوگرم", "بسته", "متر", "لیتر", "کیلو", "گرم"])
        self.unit_combo.setEditable(True)
        
        # Add form fields
        form_layout.addWidget(code_label)
        form_layout.addWidget(self.code_edit)
        form_layout.addWidget(name_label)
        form_layout.addWidget(self.name_edit)
        form_layout.addWidget(purchase_label)
        form_layout.addWidget(self.purchase_spin)
        form_layout.addWidget(sale_label)
        form_layout.addWidget(self.sale_spin)
        form_layout.addWidget(stock_label)
        form_layout.addWidget(self.stock_spin)
        form_layout.addWidget(unit_label)
        form_layout.addWidget(self.unit_combo)
        
        form_layout.addStretch()
        
        # Buttons
        buttons_layout = QVBoxLayout()
        buttons_layout.setSpacing(8)
        
        self.add_button = QPushButton("➕ ثبت کالای جدید")
        self.add_button.setFixedHeight(45)
        self.add_button.setStyleSheet("""
            QPushButton {
                background: #10B981;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border-radius: 8px;
            }
            QPushButton:hover {
                background: #059669;
            }
        """)
        self.add_button.clicked.connect(self.add_product)
        
        self.update_button = QPushButton("✏️ ویرایش کالا")
        self.update_button.setFixedHeight(45)
        self.update_button.setStyleSheet("""
            QPushButton {
                background: #3B82F6;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border-radius: 8px;
            }
            QPushButton:hover {
                background: #2563EB;
            }
        """)
        self.update_button.clicked.connect(self.update_product)
        
        self.delete_button = QPushButton("🗑️ حذف کالا")
        self.delete_button.setFixedHeight(45)
        self.delete_button.setStyleSheet("""
            QPushButton {
                background: #EF4444;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border-radius: 8px;
            }
            QPushButton:hover {
                background: #DC2626;
            }
        """)
        self.delete_button.clicked.connect(self.delete_product)
        
        self.clear_button = QPushButton("🔄 پاک کردن فرم")
        self.clear_button.setFixedHeight(45)
        self.clear_button.setStyleSheet("""
            QPushButton {
                background: #6B7280;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border-radius: 8px;
            }
            QPushButton:hover {
                background: #4B5563;
            }
        """)
        self.clear_button.clicked.connect(self.clear_form)
        
        buttons_layout.addWidget(self.add_button)
        buttons_layout.addWidget(self.update_button)
        buttons_layout.addWidget(self.delete_button)
        buttons_layout.addWidget(self.clear_button)
        
        form_layout.addLayout(buttons_layout)
        
        scroll_area.setWidget(form_widget)
        
        layout.addWidget(header_frame)
        layout.addWidget(scroll_area, 1)
    
    def load_product(self, product):
        """Load product data into form"""
        self.current_product = product
        if product:
            self.code_edit.setText(product.product_code)
            self.name_edit.setText(product.product_name)
            self.purchase_spin.setValue(float(product.purchase_price))
            self.sale_spin.setValue(float(product.sale_price))
            self.stock_spin.setValue(product.stock_quantity)
            self.unit_combo.setCurrentText(product.unit)
            
            # Enable update/delete buttons
            self.update_button.setEnabled(True)
            self.delete_button.setEnabled(True)
        else:
            self.clear_form()
    
    def clear_form(self):
        """Clear all form fields"""
        self.current_product = None
        self.code_edit.clear()
        self.name_edit.clear()
        self.purchase_spin.setValue(0)
        self.sale_spin.setValue(0)
        self.stock_spin.setValue(0)
        self.unit_combo.setCurrentIndex(0)
        
        # Disable update/delete buttons
        self.update_button.setEnabled(False)
        self.delete_button.setEnabled(False)
    
    def add_product(self):
        """Add a new product"""
        if not self.validate_form():
            return
        
        try:
            session = get_db_session()
            
            product = Product(
                product_code=self.code_edit.text().strip(),
                product_name=self.name_edit.text().strip(),
                purchase_price=Decimal(str(self.purchase_spin.value())),
                sale_price=Decimal(str(self.sale_spin.value())),
                stock_quantity=self.stock_spin.value(),
                unit=self.unit_combo.currentText()
            )
            
            session.add(product)
            session.commit()
            session.close()
            
            QMessageBox.information(self, "موفقیت", "کالا با موفقیت اضافه شد.")
            self.clear_form()
            self.product_saved.emit()
            
        except IntegrityError:
            QMessageBox.warning(self, "خطا", "کد کالای وارد شده قبلاً استفاده شده است.")
        except Exception as e:
            QMessageBox.critical(self, "خطا", f"خطا در افزودن کالا: {str(e)}")
    
    def update_product(self):
        """Update the current product"""
        if not self.current_product or not self.validate_form():
            return
        
        try:
            session = get_db_session()
            
            product = session.query(Product).filter(
                Product.id == self.current_product.id
            ).first()
            
            if product:
                product.product_code = self.code_edit.text().strip()
                product.product_name = self.name_edit.text().strip()
                product.purchase_price = Decimal(str(self.purchase_spin.value()))
                product.sale_price = Decimal(str(self.sale_spin.value()))
                product.stock_quantity = self.stock_spin.value()
                product.unit = self.unit_combo.currentText()
                
                session.commit()
                session.close()
                
                QMessageBox.information(self, "موفقیت", "کالا با موفقیت ویرایش شد.")
                self.clear_form()
                self.product_saved.emit()
            
        except IntegrityError:
            QMessageBox.warning(self, "خطا", "کد کالای وارد شده قبلاً استفاده شده است.")
        except Exception as e:
            QMessageBox.critical(self, "خطا", f"خطا در ویرایش کالا: {str(e)}")
    
    def delete_product(self):
        """Delete the current product"""
        if not self.current_product:
            return
        
        reply = QMessageBox.question(
            self, "تأیید حذف",
            "آیا از حذف این کالا اطمینان دارید؟",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                session = get_db_session()
                
                product = session.query(Product).filter(
                    Product.id == self.current_product.id
                ).first()
                
                if product:
                    session.delete(product)
                    session.commit()
                    session.close()
                    
                    QMessageBox.information(self, "موفقیت", "کالا با موفقیت حذف شد.")
                    self.clear_form()
                    self.product_saved.emit()
                
            except Exception as e:
                QMessageBox.critical(self, "خطا", f"خطا در حذف کالا: {str(e)}")
    
    def validate_form(self):
        """Validate form data"""
        if not self.code_edit.text().strip():
            QMessageBox.warning(self, "خطا", "لطفاً کد کالا را وارد کنید.")
            return False
        
        if not self.name_edit.text().strip():
            QMessageBox.warning(self, "خطا", "لطفاً نام کالا را وارد کنید.")
            return False
        
        return True

class ProductsView(QWidget):
    """Products management view"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.load_products()
    
    def setup_ui(self):
        """Setup the products view UI"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(25)
        
        # Create splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Products list (left side)
        products_frame = QFrame()
        products_frame.setStyleSheet("""
            QFrame {
                background: #374151;
                border: 1px solid #6B7280;
                border-radius: 15px;
            }
        """)
        
        products_layout = QVBoxLayout(products_frame)
        products_layout.setContentsMargins(0, 0, 0, 0)
        products_layout.setSpacing(0)
        
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
        
        header_title = QLabel("📦 لیست کالاها و موجودی")
        header_title.setStyleSheet("""
            color: #F9FAFB;
            font-size: 18px;
            font-weight: bold;
            background: transparent;
        """)
        header_layout.addWidget(header_title)
        
        # Search section
        search_frame = QFrame()
        search_frame.setStyleSheet("QFrame { background: transparent; border: none; }")
        search_layout = QHBoxLayout(search_frame)
        search_layout.setContentsMargins(20, 15, 20, 15)
        
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("جستجو بر اساس نام یا کد کالا...")
        self.search_edit.textChanged.connect(self.search_products)
        
        search_button = QPushButton("🔍 جستجو")
        search_button.setFixedWidth(100)
        search_button.clicked.connect(self.load_products)
        
        search_layout.addWidget(self.search_edit)
        search_layout.addWidget(search_button)
        
        # Products table
        self.products_table = QTableWidget()
        self.setup_products_table()
        
        products_layout.addWidget(header_frame)
        products_layout.addWidget(search_frame)
        products_layout.addWidget(self.products_table, 1)
        
        # Product form (right side)
        self.product_form = ProductForm()
        self.product_form.product_saved.connect(self.load_products)
        
        # Add to splitter
        splitter.addWidget(products_frame)
        splitter.addWidget(self.product_form)
        splitter.setSizes([700, 400])  # Set initial sizes
        
        layout.addWidget(splitter)
    
    def setup_products_table(self):
        """Setup the products table"""
        self.products_table.setColumnCount(5)
        self.products_table.setHorizontalHeaderLabels([
            "کد کالا", "نام کالا", "قیمت فروش", "موجودی", "واحد"
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
        
        # Set row height
        self.products_table.verticalHeader().setDefaultSectionSize(45)
        
        # Connect selection change
        self.products_table.selectionModel().selectionChanged.connect(self.on_product_selected)
        
        self.products_table.setStyleSheet("""
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
    
    def load_products(self):
        """Load products from database"""
        try:
            session = get_db_session()
            
            query = session.query(Product)
            
            # Apply search filter if exists
            search_text = self.search_edit.text().strip()
            if search_text:
                query = query.filter(
                    (Product.product_name.contains(search_text)) |
                    (Product.product_code.contains(search_text))
                )
            
            products = query.order_by(Product.product_name).all()
            
            self.populate_products_table(products)
            session.close()
            
        except Exception as e:
            QMessageBox.critical(self, "خطا", f"خطا در بارگذاری کالاها: {str(e)}")
    
    def populate_products_table(self, products):
        """Populate the products table"""
        self.products_table.setRowCount(len(products))
        
        for row, product in enumerate(products):
            # Store product object in the first column item
            code_item = QTableWidgetItem(product.product_code)
            code_item.setData(Qt.ItemDataRole.UserRole, product)
            self.products_table.setItem(row, 0, code_item)
            
            # Product name
            self.products_table.setItem(row, 1, QTableWidgetItem(product.product_name))
            
            # Sale price
            price_str = f"{product.sale_price:,.0f} ریال"
            self.products_table.setItem(row, 2, QTableWidgetItem(price_str))
            
            # Stock quantity
            self.products_table.setItem(row, 3, QTableWidgetItem(str(product.stock_quantity)))
            
            # Unit
            self.products_table.setItem(row, 4, QTableWidgetItem(product.unit))
    
    def search_products(self):
        """Search products as user types"""
        # Add a small delay to avoid too many database calls
        if hasattr(self, '_search_timer'):
            self._search_timer.stop()
        
        from PyQt6.QtCore import QTimer
        self._search_timer = QTimer()
        self._search_timer.timeout.connect(self.load_products)
        self._search_timer.setSingleShot(True)
        self._search_timer.start(300)  # 300ms delay
    
    def on_product_selected(self):
        """Handle product selection in table"""
        selected_rows = self.products_table.selectionModel().selectedRows()
        if selected_rows:
            row = selected_rows[0].row()
            product = self.products_table.item(row, 0).data(Qt.ItemDataRole.UserRole)
            self.product_form.load_product(product)
        else:
            self.product_form.clear_form()