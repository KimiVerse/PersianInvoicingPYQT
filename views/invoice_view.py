"""
Invoice View for Persian Invoicing System
Enhanced with background selection, PDF/PNG export, and improved UI
"""

import os
from datetime import datetime
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                           QLabel, QLineEdit, QPushButton, QTableWidget, 
                           QTableWidgetItem, QComboBox, QTextEdit, QSpinBox,
                           QHeaderView, QMessageBox, QFrame, QFileDialog,
                           QSplitter, QGroupBox, QCheckBox)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap, QPainter, QPrintPreviewDialog, QPrinter
from PyQt6.QtPrintSupport import QPrintDialog
import jdatetime
from services.database_service import DatabaseService
from services.print_service import PrintService

class InvoiceView(QWidget):
    """Enhanced invoice creation and management view"""
    
    invoice_created = pyqtSignal(str)  # Signal emitted when invoice is created
    
    def __init__(self):
        super().__init__()
        self.db_service = DatabaseService()
        self.print_service = PrintService()
        self.current_products = []
        self.invoice_items = []
        self.background_image_path = ""
        self.setup_ui()
        self.load_products()
        self.setup_styling()
        
    def setup_ui(self):
        """Setup the user interface"""
        main_layout = QHBoxLayout()
        main_layout.setSpacing(15)
        
        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left panel - Invoice form
        left_panel = self.create_invoice_form()
        
        # Right panel - Items table and totals
        right_panel = self.create_items_panel()
        
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)
        
        main_layout.addWidget(splitter)
        self.setLayout(main_layout)
        
    def create_invoice_form(self):
        """Create invoice form panel"""
        form_widget = QWidget()
        layout = QVBoxLayout(form_widget)
        layout.setSpacing(20)
        
        # Header section
        header_group = QGroupBox("تنظیمات فاکتور")
        header_layout = QGridLayout(header_group)
        
        # Background selection
        bg_label = QLabel("تصویر پس‌زمینه:")
        self.bg_button = QPushButton("انتخاب تصویر")
        self.bg_button.clicked.connect(self.select_background_image)
        self.bg_label_path = QLabel("تصویر انتخاب نشده")
        self.bg_label_path.setStyleSheet("color: #666; font-style: italic;")
        
        # Header text
        header_text_label = QLabel("متن سربرگ:")
        self.header_text_edit = QTextEdit()
        self.header_text_edit.setMaximumHeight(80)
        self.header_text_edit.setPlaceholderText("متن سربرگ فاکتور (اختیاری)")
        
        header_layout.addWidget(bg_label, 0, 0)
        header_layout.addWidget(self.bg_button, 0, 1)
        header_layout.addWidget(self.bg_label_path, 0, 2)
        header_layout.addWidget(header_text_label, 1, 0)
        header_layout.addWidget(self.header_text_edit, 1, 1, 1, 2)
        
        # Customer information
        customer_group = QGroupBox("اطلاعات مشتری")
        customer_layout = QGridLayout(customer_group)
        
        # Customer fields
        customer_name_label = QLabel("نام مشتری:")
        self.customer_name_edit = QLineEdit()
        self.customer_name_edit.setPlaceholderText("نام و نام خانوادگی مشتری")
        
        customer_phone_label = QLabel("شماره تماس:")
        self.customer_phone_edit = QLineEdit()
        self.customer_phone_edit.setPlaceholderText("شماره تماس مشتری")
        
        customer_address_label = QLabel("آدرس:")
        self.customer_address_edit = QTextEdit()
        self.customer_address_edit.setMaximumHeight(80)
        self.customer_address_edit.setPlaceholderText("آدرس مشتری")
        
        customer_layout.addWidget(customer_name_label, 0, 0)
        customer_layout.addWidget(self.customer_name_edit, 0, 1)
        customer_layout.addWidget(customer_phone_label, 1, 0)
        customer_layout.addWidget(self.customer_phone_edit, 1, 1)
        customer_layout.addWidget(customer_address_label, 2, 0)
        customer_layout.addWidget(self.customer_address_edit, 2, 1)
        
        # Product selection
        product_group = QGroupBox("افزودن کالا")
        product_layout = QGridLayout(product_group)
        
        product_label = QLabel("انتخاب کالا:")
        self.product_combo = QComboBox()
        self.product_combo.setMinimumHeight(35)
        
        quantity_label = QLabel("تعداد:")
        self.quantity_spin = QSpinBox()
        self.quantity_spin.setMinimum(1)
        self.quantity_spin.setMaximum(10000)
        self.quantity_spin.setValue(1)
        self.quantity_spin.setMinimumHeight(35)
        
        self.add_item_button = QPushButton("افزودن کالا")
        self.add_item_button.clicked.connect(self.add_item_to_invoice)
        self.add_item_button.setMinimumHeight(35)
        
        product_layout.addWidget(product_label, 0, 0)
        product_layout.addWidget(self.product_combo, 0, 1, 1, 2)
        product_layout.addWidget(quantity_label, 1, 0)
        product_layout.addWidget(self.quantity_spin, 1, 1)
        product_layout.addWidget(self.add_item_button, 1, 2)
        
        # Notes and discount
        details_group = QGroupBox("جزئیات اضافی")
        details_layout = QGridLayout(details_group)
        
        discount_label = QLabel("تخفیف (تومان):")
        self.discount_edit = QLineEdit()
        self.discount_edit.setPlaceholderText("0")
        self.discount_edit.textChanged.connect(self.update_totals)
        
        notes_label = QLabel("یادداشت:")
        self.notes_edit = QTextEdit()
        self.notes_edit.setMaximumHeight(80)
        self.notes_edit.setPlaceholderText("یادداشت‌های اضافی")
        
        details_layout.addWidget(discount_label, 0, 0)
        details_layout.addWidget(self.discount_edit, 0, 1)
        details_layout.addWidget(notes_label, 1, 0)
        details_layout.addWidget(self.notes_edit, 1, 1)
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        self.clear_button = QPushButton("پاک کردن فرم")
        self.clear_button.clicked.connect(self.clear_form)
        
        self.preview_button = QPushButton("پیش‌نمایش فاکتور")
        self.preview_button.clicked.connect(self.preview_invoice)
        
        self.save_button = QPushButton("ثبت فاکتور")
        self.save_button.clicked.connect(self.save_invoice)
        
        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.preview_button)
        button_layout.addWidget(self.save_button)
        
        # Add all groups to layout
        layout.addWidget(header_group)
        layout.addWidget(customer_group)
        layout.addWidget(product_group)
        layout.addWidget(details_group)
        layout.addStretch()
        layout.addLayout(button_layout)
        
        return form_widget
        
    def create_items_panel(self):
        """Create items table and totals panel"""
        panel_widget = QWidget()
        layout = QVBoxLayout(panel_widget)
        
        # Items table
        items_group = QGroupBox("کالاهای فاکتور")
        items_layout = QVBoxLayout(items_group)
        
        self.items_table = QTableWidget()
        self.items_table.setColumnCount(5)
        self.items_table.setHorizontalHeaderLabels([
            "نام کالا", "تعداد", "قیمت واحد", "قیمت کل", "عملیات"
        ])
        
        # Configure table
        header = self.items_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        
        self.items_table.setColumnWidth(1, 80)
        self.items_table.setColumnWidth(2, 120)
        self.items_table.setColumnWidth(3, 120)
        self.items_table.setColumnWidth(4, 80)
        
        items_layout.addWidget(self.items_table)
        
        # Totals section
        totals_group = QGroupBox("محاسبات")
        totals_layout = QGridLayout(totals_group)
        
        # Total labels
        subtotal_label = QLabel("جمع کل:")
        self.subtotal_value = QLabel("0 تومان")
        self.subtotal_value.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        discount_label = QLabel("تخفیف:")
        self.discount_value = QLabel("0 تومان")
        self.discount_value.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        final_label = QLabel("مبلغ نهایی:")
        self.final_value = QLabel("0 تومان")
        self.final_value.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.final_value.setStyleSheet("font-weight: bold; font-size: 14pt; color: #2E7D32;")
        
        totals_layout.addWidget(subtotal_label, 0, 0)
        totals_layout.addWidget(self.subtotal_value, 0, 1)
        totals_layout.addWidget(discount_label, 1, 0)
        totals_layout.addWidget(self.discount_value, 1, 1)
        totals_layout.addWidget(final_label, 2, 0)
        totals_layout.addWidget(self.final_value, 2, 1)
        
        # Export buttons
        export_group = QGroupBox("خروجی فاکتور")
        export_layout = QHBoxLayout(export_group)
        
        self.export_pdf_button = QPushButton("خروجی PDF")
        self.export_pdf_button.clicked.connect(self.export_to_pdf)
        
        self.export_image_button = QPushButton("خروجی تصویر")
        self.export_image_button.clicked.connect(self.export_to_image)
        
        self.print_button = QPushButton("چاپ فاکتور")
        self.print_button.clicked.connect(self.print_invoice)
        
        export_layout.addWidget(self.export_pdf_button)
        export_layout.addWidget(self.export_image_button)
        export_layout.addWidget(self.print_button)
        
        # Add to main layout
        layout.addWidget(items_group, 2)
        layout.addWidget(totals_group)
        layout.addWidget(export_group)
        
        return panel_widget
        
    def setup_styling(self):
        """Setup modern styling"""
        self.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #ddd;
                border-radius: 8px;
                margin: 10px 0px;
                padding-top: 10px;
                background-color: #f9f9f9;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #333;
                background-color: #f9f9f9;
            }
            
            QLineEdit, QTextEdit, QComboBox, QSpinBox {
                border: 2px solid #ddd;
                border-radius: 6px;
                padding: 8px;
                font-size: 11pt;
                background-color: white;
            }
            
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QSpinBox:focus {
                border-color: #4CAF50;
            }
            
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 15px;
                font-size: 11pt;
                font-weight: bold;
                min-width: 100px;
            }
            
            QPushButton:hover {
                background-color: #45a049;
            }
            
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            
            QPushButton[class="secondary"] {
                background-color: #2196F3;
            }
            
            QPushButton[class="secondary"]:hover {
                background-color: #1976D2;
            }
            
            QPushButton[class="danger"] {
                background-color: #f44336;
            }
            
            QPushButton[class="danger"]:hover {
                background-color: #d32f2f;
            }
            
            QTableWidget {
                border: 1px solid #ddd;
                border-radius: 6px;
                background-color: white;
                gridline-color: #f0f0f0;
                font-size: 10pt;
            }
            
            QTableWidget::item {
                padding: 8px;
                border: none;
            }
            
            QTableWidget::item:selected {
                background-color: #E3F2FD;
                color: #1976D2;
            }
            
            QHeaderView::section {
                background-color: #f5f5f5;
                padding: 8px;
                border: 1px solid #ddd;
                font-weight: bold;
            }
            
            QLabel {
                color: #333;
                font-size: 11pt;
            }
        """)
        
        # Set button classes
        self.clear_button.setProperty("class", "secondary")
        self.preview_button.setProperty("class", "secondary")
        self.export_pdf_button.setProperty("class", "secondary")
        self.export_image_button.setProperty("class", "secondary")
        self.print_button.setProperty("class", "secondary")
        
    def select_background_image(self):
        """Select background image for invoice"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "انتخاب تصویر پس‌زمینه",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        
        if file_path:
            self.background_image_path = file_path
            filename = os.path.basename(file_path)
            self.bg_label_path.setText(f"تصویر انتخاب شده: {filename}")
            self.bg_label_path.setStyleSheet("color: #4CAF50; font-weight: bold;")
        
    def load_products(self):
        """Load products into combo box"""
        self.current_products = self.db_service.get_products()
        self.product_combo.clear()
        
        for product in self.current_products:
            display_text = f"{product.name} - {product.formatted_sale_price}"
            self.product_combo.addItem(display_text, product.id)
        
    def add_item_to_invoice(self):
        """Add selected item to invoice"""
        if not self.current_products:
            QMessageBox.warning(self, "خطا", "هیچ کالایی در سیستم ثبت نشده است")
            return
            
        product_id = self.product_combo.currentData()
        quantity = self.quantity_spin.value()
        
        if not product_id:
            QMessageBox.warning(self, "خطا", "لطفاً کالایی را انتخاب کنید")
            return
        
        # Find selected product
        selected_product = None
        for product in self.current_products:
            if product.id == product_id:
                selected_product = product
                break
        
        if not selected_product:
            QMessageBox.warning(self, "خطا", "کالای انتخاب شده یافت نشد")
            return
        
        # Check stock
        if selected_product.stock_quantity < quantity:
            QMessageBox.warning(
                self, 
                "خطا", 
                f"موجودی کالا کافی نیست\\nموجودی فعلی: {selected_product.stock_quantity}"
            )
            return
        
        # Check if item already exists
        for i, item in enumerate(self.invoice_items):
            if item['product_id'] == product_id:
                # Update existing item
                new_quantity = item['quantity'] + quantity
                if selected_product.stock_quantity < new_quantity:
                    QMessageBox.warning(
                        self, 
                        "خطا", 
                        f"موجودی کالا کافی نیست\\nموجودی فعلی: {selected_product.stock_quantity}\\nتعداد فعلی در فاکتور: {item['quantity']}"
                    )
                    return
                
                self.invoice_items[i]['quantity'] = new_quantity
                self.invoice_items[i]['total_price'] = new_quantity * selected_product.sale_price
                self.update_items_table()
                self.update_totals()
                return
        
        # Add new item
        item = {
            'product_id': product_id,
            'product_name': selected_product.name,
            'quantity': quantity,
            'unit_price': selected_product.sale_price,
            'total_price': quantity * selected_product.sale_price
        }
        
        self.invoice_items.append(item)
        self.update_items_table()
        self.update_totals()
        
        # Reset quantity
        self.quantity_spin.setValue(1)
        
    def update_items_table(self):
        """Update items table display"""
        self.items_table.setRowCount(len(self.invoice_items))
        
        for row, item in enumerate(self.invoice_items):
            # Product name
            name_item = QTableWidgetItem(item['product_name'])
            name_item.setFlags(name_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.items_table.setItem(row, 0, name_item)
            
            # Quantity
            quantity_item = QTableWidgetItem(str(item['quantity']))
            quantity_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            quantity_item.setFlags(quantity_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.items_table.setItem(row, 1, quantity_item)
            
            # Unit price
            unit_price_item = QTableWidgetItem(f"{item['unit_price']:,} تومان")
            unit_price_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft)
            unit_price_item.setFlags(unit_price_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.items_table.setItem(row, 2, unit_price_item)
            
            # Total price
            total_price_item = QTableWidgetItem(f"{item['total_price']:,} تومان")
            total_price_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft)
            total_price_item.setFlags(total_price_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.items_table.setItem(row, 3, total_price_item)
            
            # Delete button
            delete_button = QPushButton("حذف")
            delete_button.setProperty("class", "danger")
            delete_button.clicked.connect(lambda checked, r=row: self.remove_item(r))
            self.items_table.setCellWidget(row, 4, delete_button)
    
    def remove_item(self, row):
        """Remove item from invoice"""
        if 0 <= row < len(self.invoice_items):
            self.invoice_items.pop(row)
            self.update_items_table()
            self.update_totals()
    
    def update_totals(self):
        """Update total calculations"""
        subtotal = sum(item['total_price'] for item in self.invoice_items)
        
        # Get discount
        try:
            discount_text = self.discount_edit.text().replace(',', '').replace('٬', '')
            discount = int(float(discount_text)) if discount_text else 0
        except (ValueError, TypeError):
            discount = 0
        
        final_total = max(0, subtotal - discount)
        
        # Update labels
        self.subtotal_value.setText(f"{subtotal:,} تومان")
        self.discount_value.setText(f"{discount:,} تومان")
        self.final_value.setText(f"{final_total:,} تومان")
    
    def clear_form(self):
        """Clear all form fields"""
        self.customer_name_edit.clear()
        self.customer_phone_edit.clear()
        self.customer_address_edit.clear()
        self.discount_edit.clear()
        self.notes_edit.clear()
        self.header_text_edit.clear()
        self.background_image_path = ""
        self.bg_label_path.setText("تصویر انتخاب نشده")
        self.bg_label_path.setStyleSheet("color: #666; font-style: italic;")
        self.invoice_items.clear()
        self.update_items_table()
        self.update_totals()
        self.quantity_spin.setValue(1)
    
    def save_invoice(self):
        """Save invoice to database"""
        # Validation
        if not self.customer_name_edit.text().strip():
            QMessageBox.warning(self, "خطا", "نام مشتری الزامی است")
            return
        
        if not self.invoice_items:
            QMessageBox.warning(self, "خطا", "لطفاً حداقل یک کالا به فاکتور اضافه کنید")
            return
        
        # Prepare data
        customer_name = self.customer_name_edit.text().strip()
        customer_phone = self.customer_phone_edit.text().strip()
        customer_address = self.customer_address_edit.toPlainText().strip()
        notes = self.notes_edit.toPlainText().strip()
        header_text = self.header_text_edit.toPlainText().strip()
        
        try:
            discount_text = self.discount_edit.text().replace(',', '').replace('٬', '')
            discount_amount = int(float(discount_text)) if discount_text else 0
        except (ValueError, TypeError):
            discount_amount = 0
        
        # Save invoice
        success, message = self.db_service.create_invoice(
            customer_name=customer_name,
            customer_phone=customer_phone,
            customer_address=customer_address,
            items=self.invoice_items,
            discount_amount=discount_amount,
            notes=notes,
            background_image_path=self.background_image_path,
            header_text=header_text
        )
        
        if success:
            QMessageBox.information(self, "موفقیت", message)
            self.invoice_created.emit(message)
            self.clear_form()
            self.load_products()  # Refresh products to update stock
        else:
            QMessageBox.critical(self, "خطا", message)
    
    def preview_invoice(self):
        """Preview invoice before saving"""
        if not self.customer_name_edit.text().strip():
            QMessageBox.warning(self, "خطا", "نام مشتری الزامی است")
            return
        
        if not self.invoice_items:
            QMessageBox.warning(self, "خطا", "لطفاً حداقل یک کالا به فاکتور اضافه کنید")
            return
        
        # Create temporary invoice data for preview
        invoice_data = {
            'invoice_number': 'پیش‌نمایش',
            'customer_name': self.customer_name_edit.text().strip(),
            'customer_phone': self.customer_phone_edit.text().strip(),
            'customer_address': self.customer_address_edit.toPlainText().strip(),
            'items': self.invoice_items,
            'discount_amount': int(float(self.discount_edit.text().replace(',', ''))) if self.discount_edit.text() else 0,
            'notes': self.notes_edit.toPlainText().strip(),
            'header_text': self.header_text_edit.toPlainText().strip(),
            'background_image_path': self.background_image_path,
            'issue_date': datetime.now()
        }
        
        # Show print preview
        self.show_print_preview(invoice_data)
    
    def export_to_pdf(self):
        """Export invoice to PDF"""
        if not self.invoice_items:
            QMessageBox.warning(self, "خطا", "هیچ فاکتوری برای خروجی وجود ندارد")
            return
            
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "ذخیره فاکتور به صورت PDF",
            f"invoice_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            "PDF Files (*.pdf)"
        )
        
        if file_path:
            try:
                # Create invoice data
                invoice_data = self.get_current_invoice_data()
                
                # Generate PDF
                success = self.print_service.export_to_pdf(invoice_data, file_path)
                
                if success:
                    QMessageBox.information(self, "موفقیت", f"فاکتور در مسیر زیر ذخیره شد:\\n{file_path}")
                else:
                    QMessageBox.critical(self, "خطا", "خطا در ایجاد فایل PDF")
            except Exception as e:
                QMessageBox.critical(self, "خطا", f"خطا در ایجاد PDF: {str(e)}")
    
    def export_to_image(self):
        """Export invoice to image (PNG/JPG)"""
        if not self.invoice_items:
            QMessageBox.warning(self, "خطا", "هیچ فاکتوری برای خروجی وجود ندارد")
            return
            
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "ذخیره فاکتور به صورت تصویر",
            f"invoice_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
            "Image Files (*.png *.jpg *.jpeg)"
        )
        
        if file_path:
            try:
                # Create invoice data
                invoice_data = self.get_current_invoice_data()
                
                # Generate image
                success = self.print_service.export_to_image(invoice_data, file_path)
                
                if success:
                    QMessageBox.information(self, "موفقیت", f"فاکتور در مسیر زیر ذخیره شد:\\n{file_path}")
                else:
                    QMessageBox.critical(self, "خطا", "خطا در ایجاد فایل تصویر")
            except Exception as e:
                QMessageBox.critical(self, "خطا", f"خطا در ایجاد تصویر: {str(e)}")
    
    def print_invoice(self):
        """Print invoice"""
        if not self.invoice_items:
            QMessageBox.warning(self, "خطا", "هیچ فاکتوری برای چاپ وجود ندارد")
            return
            
        try:
            invoice_data = self.get_current_invoice_data()
            self.show_print_preview(invoice_data)
        except Exception as e:
            QMessageBox.critical(self, "خطا", f"خطا در چاپ: {str(e)}")
    
    def get_current_invoice_data(self):
        """Get current invoice data for export/print"""
        try:
            discount_text = self.discount_edit.text().replace(',', '').replace('٬', '')
            discount_amount = int(float(discount_text)) if discount_text else 0
        except (ValueError, TypeError):
            discount_amount = 0
            
        return {
            'invoice_number': f"پیش‌نمایش-{datetime.now().strftime('%H%M%S')}",
            'customer_name': self.customer_name_edit.text().strip(),
            'customer_phone': self.customer_phone_edit.text().strip(),
            'customer_address': self.customer_address_edit.toPlainText().strip(),
            'items': self.invoice_items,
            'discount_amount': discount_amount,
            'notes': self.notes_edit.toPlainText().strip(),
            'header_text': self.header_text_edit.toPlainText().strip(),
            'background_image_path': self.background_image_path,
            'issue_date': datetime.now()
        }
    
    def show_print_preview(self, invoice_data):
        """Show print preview dialog"""
        printer = QPrinter(QPrinter.Mode.HighResolution)
        printer.setPageSize(QPrinter.PageSize.A4)
        
        preview_dialog = QPrintPreviewDialog(printer, self)
        preview_dialog.paintRequested.connect(
            lambda printer: self.print_service.print_invoice(invoice_data, printer)
        )
        preview_dialog.exec()