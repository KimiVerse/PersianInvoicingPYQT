"""
Products View for Persian Invoicing System
Enhanced with improved validation and UI
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                           QLabel, QLineEdit, QPushButton, QTableWidget, 
                           QTableWidgetItem, QHeaderView, QMessageBox, 
                           QFrame, QGroupBox, QTextEdit, QSpinBox,
                           QSplitter, QSizePolicy, QAbstractItemView)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QDoubleValidator, QIntValidator
from services.database_service import DatabaseService

class ProductFormWidget(QFrame):
    """Enhanced product form widget"""
    
    product_saved = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.db_service = DatabaseService()
        self.current_product_id = None
        self.setup_ui()
        self.setup_validation()
        
    def setup_ui(self):
        """Setup the product form UI"""
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Form title
        title_label = QLabel("افزودن / ویرایش کالا")
        title_label.setFont(QFont("Vazirmatn", 14, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #2c3e50; margin-bottom: 15px;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Form fields
        form_layout = QGridLayout()
        form_layout.setSpacing(15)
        
        # Product name
        name_label = QLabel("نام کالا:")
        name_label.setFont(QFont("Vazirmatn", 11, QFont.Weight.Bold))
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("نام کالا را وارد کنید")
        self.name_edit.setFont(QFont("Vazirmatn", 11))
        
        # Purchase price
        purchase_label = QLabel("قیمت خرید (تومان):")
        purchase_label.setFont(QFont("Vazirmatn", 11, QFont.Weight.Bold))
        self.purchase_edit = QLineEdit()
        self.purchase_edit.setPlaceholderText("0")
        self.purchase_edit.setFont(QFont("Vazirmatn", 11))
        self.purchase_edit.textChanged.connect(self.format_price_input)
        
        # Sale price
        sale_label = QLabel("قیمت فروش (تومان):")
        sale_label.setFont(QFont("Vazirmatn", 11, QFont.Weight.Bold))
        self.sale_edit = QLineEdit()
        self.sale_edit.setPlaceholderText("0")
        self.sale_edit.setFont(QFont("Vazirmatn", 11))
        self.sale_edit.textChanged.connect(self.format_price_input)
        
        # Stock quantity
        stock_label = QLabel("موجودی:")
        stock_label.setFont(QFont("Vazirmatn", 11, QFont.Weight.Bold))
        self.stock_spin = QSpinBox()
        self.stock_spin.setMinimum(0)
        self.stock_spin.setMaximum(1000000)
        self.stock_spin.setValue(0)
        self.stock_spin.setFont(QFont("Vazirmatn", 11))
        self.stock_spin.setSuffix(" عدد")
        
        # Description
        desc_label = QLabel("توضیحات:")
        desc_label.setFont(QFont("Vazirmatn", 11, QFont.Weight.Bold))
        self.desc_edit = QTextEdit()
        self.desc_edit.setPlaceholderText("توضیحات کالا (اختیاری)")
        self.desc_edit.setFont(QFont("Vazirmatn", 11))
        self.desc_edit.setMaximumHeight(80)
        
        # Add fields to form
        form_layout.addWidget(name_label, 0, 0)
        form_layout.addWidget(self.name_edit, 0, 1)
        form_layout.addWidget(purchase_label, 1, 0)
        form_layout.addWidget(self.purchase_edit, 1, 1)
        form_layout.addWidget(sale_label, 2, 0)
        form_layout.addWidget(self.sale_edit, 2, 1)
        form_layout.addWidget(stock_label, 3, 0)
        form_layout.addWidget(self.stock_spin, 3, 1)
        form_layout.addWidget(desc_label, 4, 0)
        form_layout.addWidget(self.desc_edit, 4, 1)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.clear_button = QPushButton("پاک کردن فرم")
        self.clear_button.setFont(QFont("Vazirmatn", 11, QFont.Weight.Bold))
        self.clear_button.clicked.connect(self.clear_form)
        
        self.save_button = QPushButton("ذخیره کالا")
        self.save_button.setFont(QFont("Vazirmatn", 11, QFont.Weight.Bold))
        self.save_button.clicked.connect(self.save_product)
        
        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.save_button)
        
        # Add to main layout
        layout.addWidget(title_label)
        layout.addLayout(form_layout)
        layout.addStretch()
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
    def setup_validation(self):
        """Setup input validation"""
        # Set validators for numeric fields
        self.purchase_edit.textChanged.connect(self.validate_form)
        self.sale_edit.textChanged.connect(self.validate_form)
        self.name_edit.textChanged.connect(self.validate_form)
        
    def format_price_input(self):
        """Format price input with thousand separators"""
        sender = self.sender()
        text = sender.text().replace(',', '').replace('٬', '')
        
        if text and text.isdigit():
            # Format with thousand separators
            formatted = f"{int(text):,}"
            
            # Prevent infinite loop
            if sender.text() != formatted:
                cursor_pos = sender.cursorPosition()
                sender.setText(formatted)
                # Adjust cursor position
                new_pos = min(cursor_pos + (len(formatted) - len(text)), len(formatted))
                sender.setCursorPosition(new_pos)
    
    def validate_form(self):
        """Validate form inputs"""
        is_valid = True
        
        # Check product name
        if not self.name_edit.text().strip():
            is_valid = False
        
        # Check prices (they can be 0)
        try:
            purchase_text = self.purchase_edit.text().replace(',', '').replace('٬', '')
            if purchase_text and not purchase_text.isdigit():
                is_valid = False
        except:
            is_valid = False
            
        try:
            sale_text = self.sale_edit.text().replace(',', '').replace('٬', '')
            if sale_text and not sale_text.isdigit():
                is_valid = False
        except:
            is_valid = False
        
        # Enable/disable save button
        self.save_button.setEnabled(is_valid)
        
        return is_valid
    
    def clear_form(self):
        """Clear all form fields"""
        self.name_edit.clear()
        self.purchase_edit.clear()
        self.sale_edit.clear()
        self.stock_spin.setValue(0)
        self.desc_edit.clear()
        self.current_product_id = None
        
        # Update form title
        title_label = self.findChild(QLabel)
        if title_label:
            title_label.setText("افزودن / ویرایش کالا")
            
        self.save_button.setText("ذخیره کالا")
    
    def save_product(self):
        """Save product to database"""
        if not self.validate_form():
            QMessageBox.warning(self, "خطا", "لطفاً تمام فیلدهای الزامی را پر کنید")
            return
        
        # Get form data
        name = self.name_edit.text().strip()
        
        # Parse prices (remove commas)
        try:
            purchase_text = self.purchase_edit.text().replace(',', '').replace('٬', '')
            purchase_price = int(purchase_text) if purchase_text else 0
        except:
            purchase_price = 0
            
        try:
            sale_text = self.sale_edit.text().replace(',', '').replace('٬', '')
            sale_price = int(sale_text) if sale_text else 0
        except:
            sale_price = 0
        
        stock_quantity = self.stock_spin.value()
        description = self.desc_edit.toPlainText().strip()
        
        # Save to database
        if self.current_product_id:
            # Update existing product
            success, message = self.db_service.update_product(
                self.current_product_id, name, purchase_price, 
                sale_price, stock_quantity, description
            )
        else:
            # Add new product
            success, message = self.db_service.add_product(
                name, purchase_price, sale_price, stock_quantity, description
            )
        
        if success:
            QMessageBox.information(self, "موفقیت", message)
            self.clear_form()
            self.product_saved.emit()
        else:
            QMessageBox.critical(self, "خطا", message)
    
    def load_product(self, product):
        """Load product data into form for editing"""
        self.current_product_id = product.id
        self.name_edit.setText(product.name)
        self.purchase_edit.setText(f"{product.purchase_price:,}")
        self.sale_edit.setText(f"{product.sale_price:,}")
        self.stock_spin.setValue(product.stock_quantity)
        self.desc_edit.setPlainText(product.description or "")
        
        # Update form title
        title_label = self.findChild(QLabel)
        if title_label:
            title_label.setText(f"ویرایش کالا: {product.name}")
            
        self.save_button.setText("به‌روزرسانی کالا")

class ProductsView(QWidget):
    """Enhanced products management view"""
    
    def __init__(self):
        super().__init__()
        self.db_service = DatabaseService()
        self.current_products = []
        self.setup_ui()
        self.setup_styling()
        self.load_products()
        
    def setup_ui(self):
        """Setup the user interface"""
        main_layout = QHBoxLayout()
        main_layout.setSpacing(20)
        
        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left panel - Product form
        self.form_widget = ProductFormWidget()
        self.form_widget.product_saved.connect(self.load_products)
        
        # Right panel - Products list
        right_panel = self.create_products_list()
        
        splitter.addWidget(self.form_widget)
        splitter.addWidget(right_panel)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)
        
        main_layout.addWidget(splitter)
        self.setLayout(main_layout)
        
    def create_products_list(self):
        """Create products list panel"""
        panel_widget = QWidget()
        layout = QVBoxLayout(panel_widget)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header_layout = QHBoxLayout()
        
        title_label = QLabel("لیست کالاها")
        title_label.setFont(QFont("Vazirmatn", 14, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #2c3e50;")
        
        # Search box
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("جستجو در کالاها...")
        self.search_edit.setFont(QFont("Vazirmatn", 11))
        self.search_edit.textChanged.connect(self.filter_products)
        self.search_edit.setMaximumWidth(300)
        
        # Refresh button
        self.refresh_button = QPushButton("🔄 به‌روزرسانی")
        self.refresh_button.setFont(QFont("Vazirmatn", 10, QFont.Weight.Bold))
        self.refresh_button.clicked.connect(self.load_products)
        self.refresh_button.setMaximumWidth(120)
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.search_edit)
        header_layout.addWidget(self.refresh_button)
        
        # Products table
        self.products_table = QTableWidget()
        self.products_table.setColumnCount(6)
        self.products_table.setHorizontalHeaderLabels([
            "نام کالا", "قیمت خرید", "قیمت فروش", "موجودی", "توضیحات", "عملیات"
        ])
        
        # Configure table
        header = self.products_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)
        
        self.products_table.setColumnWidth(1, 120)
        self.products_table.setColumnWidth(2, 120)
        self.products_table.setColumnWidth(3, 80)
        self.products_table.setColumnWidth(4, 150)
        self.products_table.setColumnWidth(5, 150)
        
        # Table settings
        self.products_table.setAlternatingRowColors(True)
        self.products_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.products_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        
        # Statistics
        stats_group = QGroupBox("آمار کالاها")
        stats_group.setFont(QFont("Vazirmatn", 11, QFont.Weight.Bold))
        stats_layout = QGridLayout(stats_group)
        
        self.total_products_label = QLabel("تعداد کل: 0")
        self.total_value_label = QLabel("ارزش کل موجودی: 0 تومان")
        self.low_stock_label = QLabel("کالاهای کم‌موجود: 0")
        
        for label in [self.total_products_label, self.total_value_label, self.low_stock_label]:
            label.setFont(QFont("Vazirmatn", 10))
            label.setStyleSheet("color: #495057; padding: 5px;")
        
        stats_layout.addWidget(self.total_products_label, 0, 0)
        stats_layout.addWidget(self.total_value_label, 0, 1)
        stats_layout.addWidget(self.low_stock_label, 0, 2)
        
        # Add to layout
        layout.addLayout(header_layout)
        layout.addWidget(self.products_table)
        layout.addWidget(stats_group)
        
        return panel_widget
        
    def setup_styling(self):
        """Setup modern styling"""
        self.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
                font-family: 'Vazirmatn', Arial, sans-serif;
            }
            
            ProductFormWidget {
                background-color: white;
                border: 2px solid #dee2e6;
                border-radius: 12px;
                margin: 5px;
            }
            
            QGroupBox {
                font-weight: bold;
                border: 2px solid #dee2e6;
                border-radius: 8px;
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
            
            QLineEdit, QTextEdit, QSpinBox {
                border: 2px solid #dee2e6;
                border-radius: 8px;
                padding: 10px;
                font-size: 11pt;
                background-color: white;
                color: #495057;
            }
            
            QLineEdit:focus, QTextEdit:focus, QSpinBox:focus {
                border-color: #4CAF50;
                outline: none;
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
            
            QPushButton[class="secondary"] {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2196F3, stop:1 #1976D2);
            }
            
            QPushButton[class="secondary"]:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1976D2, stop:1 #1565C0);
            }
            
            QPushButton[class="danger"] {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f44336, stop:1 #d32f2f);
            }
            
            QPushButton[class="danger"]:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #d32f2f, stop:1 #c62828);
            }
            
            QTableWidget {
                border: 1px solid #dee2e6;
                border-radius: 8px;
                background-color: white;
                gridline-color: #f1f3f4;
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
        
        # Set button classes
        self.form_widget.clear_button.setProperty("class", "secondary")
        self.refresh_button.setProperty("class", "secondary")
    
    def load_products(self):
        """Load products into table"""
        try:
            self.current_products = self.db_service.get_products()
            self.update_products_table(self.current_products)
            self.update_statistics()
        except Exception as e:
            QMessageBox.critical(self, "خطا", f"خطا در بارگذاری کالاها: {str(e)}")
    
    def update_products_table(self, products):
        """Update products table with given products"""
        self.products_table.setRowCount(len(products))
        
        for row, product in enumerate(products):
            # Product name
            name_item = QTableWidgetItem(product.name)
            name_item.setFlags(name_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.products_table.setItem(row, 0, name_item)
            
            # Purchase price
            purchase_item = QTableWidgetItem(f"{product.purchase_price:,} تومان")
            purchase_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft)
            purchase_item.setFlags(purchase_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.products_table.setItem(row, 1, purchase_item)
            
            # Sale price
            sale_item = QTableWidgetItem(f"{product.sale_price:,} تومان")
            sale_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft)
            sale_item.setFlags(sale_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.products_table.setItem(row, 2, sale_item)
            
            # Stock quantity with color coding
            stock_item = QTableWidgetItem(f"{product.stock_quantity} عدد")
            stock_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            stock_item.setFlags(stock_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            
            # Color code based on stock level
            if product.stock_quantity == 0:
                stock_item.setBackground(QFont().defaultFamily())  # Red background
            elif product.stock_quantity <= 5:
                stock_item.setBackground(QFont().defaultFamily())  # Yellow background
            
            self.products_table.setItem(row, 3, stock_item)
            
            # Description (truncated)
            desc_text = product.description[:50] + "..." if product.description and len(product.description) > 50 else product.description or ""
            desc_item = QTableWidgetItem(desc_text)
            desc_item.setFlags(desc_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.products_table.setItem(row, 4, desc_item)
            
            # Action buttons
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(5, 5, 5, 5)
            actions_layout.setSpacing(5)
            
            edit_button = QPushButton("ویرایش")
            edit_button.setProperty("class", "secondary")
            edit_button.setMaximumWidth(60)
            edit_button.clicked.connect(lambda checked, p=product: self.edit_product(p))
            
            delete_button = QPushButton("حذف")
            delete_button.setProperty("class", "danger")
            delete_button.setMaximumWidth(50)
            delete_button.clicked.connect(lambda checked, p=product: self.delete_product(p))
            
            actions_layout.addWidget(edit_button)
            actions_layout.addWidget(delete_button)
            
            self.products_table.setCellWidget(row, 5, actions_widget)
    
    def update_statistics(self):
        """Update products statistics"""
        try:
            total_products = len(self.current_products)
            total_value = sum(p.stock_quantity * p.sale_price for p in self.current_products)
            low_stock_count = len([p for p in self.current_products if p.stock_quantity <= 5])
            
            self.total_products_label.setText(f"تعداد کل: {total_products}")
            self.total_value_label.setText(f"ارزش کل موجودی: {total_value:,} تومان")
            self.low_stock_label.setText(f"کالاهای کم‌موجود: {low_stock_count}")
            
        except Exception as e:
            print(f"Error updating statistics: {e}")
    
    def filter_products(self):
        """Filter products based on search term"""
        search_term = self.search_edit.text().strip().lower()
        
        if not search_term:
            filtered_products = self.current_products
        else:
            filtered_products = [
                p for p in self.current_products 
                if search_term in p.name.lower() or 
                (p.description and search_term in p.description.lower())
            ]
        
        self.update_products_table(filtered_products)
    
    def edit_product(self, product):
        """Load product for editing"""
        self.form_widget.load_product(product)
    
    def delete_product(self, product):
        """Delete product with confirmation"""
        reply = QMessageBox.question(
            self,
            'تأیید حذف',
            f'آیا مطمئن هستید که می‌خواهید کالا "{product.name}" را حذف کنید؟\\n\\nاین عمل قابل بازگشت نیست.',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            success, message = self.db_service.delete_product(product.id)
            
            if success:
                QMessageBox.information(self, "موفقیت", message)
                self.load_products()
            else:
                QMessageBox.critical(self, "خطا", message)