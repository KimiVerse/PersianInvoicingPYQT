# Invoice Creation View
# File: views/invoice_view.py

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                            QLabel, QFrame, QPushButton, QLineEdit, QTableWidget,
                            QTableWidgetItem, QHeaderView, QMessageBox, QComboBox,
                            QDoubleSpinBox, QSpinBox, QDateEdit, QSplitter,
                            QScrollArea, QTextEdit)
from PyQt6.QtCore import Qt, QDate, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap, QPainter, QPrinter, QTextDocument
from database.models import get_db_session, Product, Invoice, InvoiceItem
from datetime import datetime, date
from decimal import Decimal
import random

class InvoiceHeaderWidget(QFrame):
    """Modern invoice header with company info"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the invoice header"""
        self.setFixedHeight(120)
        self.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #3B82F6, stop:1 #10B981);
                border-radius: 12px;
                border: none;
            }
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(25, 20, 25, 20)
        
        # Company info
        company_layout = QVBoxLayout()
        
        company_name = QLabel("شرکت نمونه تجارت پارس")
        company_name.setStyleSheet("""
            color: white;
            font-size: 24px;
            font-weight: bold;
            background: transparent;
        """)
        
        company_desc = QLabel("متخصص در ارائه بهترین محصولات و خدمات")
        company_desc.setStyleSheet("""
            color: #E5E7EB;
            font-size: 12px;
            background: transparent;
        """)
        
        company_layout.addWidget(company_name)
        company_layout.addWidget(company_desc)
        company_layout.addStretch()
        
        # Logo placeholder
        logo_frame = QFrame()
        logo_frame.setFixedSize(80, 80)
        logo_frame.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.2);
                border-radius: 40px;
                border: 2px solid white;
            }
        """)
        
        logo_layout = QVBoxLayout(logo_frame)
        logo_layout.setContentsMargins(0, 0, 0, 0)
        logo_label = QLabel("🏢")
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_label.setStyleSheet("font-size: 32px; background: transparent; color: white;")
        logo_layout.addWidget(logo_label)
        
        layout.addLayout(company_layout)
        layout.addStretch()
        layout.addWidget(logo_frame)

class InvoiceView(QWidget):
    """Invoice creation and management view"""
    
    def __init__(self):
        super().__init__()
        self.current_invoice_items = []
        self.available_products = []
        self.setup_ui()
        self.load_products()
        self.generate_invoice_number()
    
    def setup_ui(self):
        """Setup the invoice view UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Invoice header
        self.header_widget = InvoiceHeaderWidget()
        layout.addWidget(self.header_widget)
        
        # Customer information section
        customer_frame = self.create_customer_section()
        layout.addWidget(customer_frame)
        
        # Items section
        items_frame = self.create_items_section()
        layout.addWidget(items_frame, 1)
        
        # Footer section
        footer_frame = self.create_footer_section()
        layout.addWidget(footer_frame)
    
    def create_customer_section(self):
        """Create customer information section"""
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background: #374151;
                border: 1px solid #6B7280;
                border-radius: 12px;
            }
        """)
        
        layout = QGridLayout(frame)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)
        
        # Customer name
        customer_label = QLabel("👤 نام مشتری:")
        customer_label.setStyleSheet("font-weight: bold; font-size: 14px; background: transparent;")
        self.customer_edit = QLineEdit()
        self.customer_edit.setPlaceholderText("نام مشتری را وارد کنید")
        
        # Invoice number
        invoice_label = QLabel("🧾 شماره فاکتور:")
        invoice_label.setStyleSheet("font-weight: bold; font-size: 14px; background: transparent;")
        self.invoice_number_edit = QLineEdit()
        self.invoice_number_edit.setReadOnly(True)
        self.invoice_number_edit.setStyleSheet("""
            QLineEdit {
                background: #4B5563;
                color: #D1D5DB;
            }
        """)
        
        # Date
        date_label = QLabel("📅 تاریخ:")
        date_label.setStyleSheet("font-weight: bold; font-size: 14px; background: transparent;")
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        
        layout.addWidget(customer_label, 0, 0)
        layout.addWidget(self.customer_edit, 1, 0)
        layout.addWidget(invoice_label, 0, 1)
        layout.addWidget(self.invoice_number_edit, 1, 1)
        layout.addWidget(date_label, 0, 2)
        layout.addWidget(self.date_edit, 1, 2)
        
        return frame
    
    def create_items_section(self):
        """Create invoice items section"""
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background: #374151;
                border: 1px solid #6B7280;
                border-radius: 12px;
            }
        """)
        
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Add item header
        add_header = QFrame()
        add_header.setFixedHeight(80)
        add_header.setStyleSheet("""
            QFrame {
                background: #4B5563;
                border-radius: 12px 12px 0px 0px;
                border-bottom: 1px solid #6B7280;
            }
        """)
        
        add_layout = QHBoxLayout(add_header)
        add_layout.setContentsMargins(25, 15, 25, 15)
        add_layout.setSpacing(15)
        
        # Product selection
        product_label = QLabel("🛍️ انتخاب کالا:")
        product_label.setStyleSheet("font-weight: bold; font-size: 14px; background: transparent;")
        product_container = QVBoxLayout()
        product_container.addWidget(product_label)
        
        self.product_combo = QComboBox()
        self.product_combo.setMinimumWidth(300)
        product_container.addWidget(self.product_combo)
        
        # Quantity
        qty_label = QLabel("🔢 تعداد:")
        qty_label.setStyleSheet("font-weight: bold; font-size: 14px; background: transparent;")
        qty_container = QVBoxLayout()
        qty_container.addWidget(qty_label)
        
        self.quantity_spin = QSpinBox()
        self.quantity_spin.setRange(1, 999999)
        self.quantity_spin.setValue(1)
        qty_container.addWidget(self.quantity_spin)
        
        # Add button
        add_button = QPushButton("➕ افزودن ردیف")
        add_button.setFixedHeight(45)
        add_button.setStyleSheet("""
            QPushButton {
                background: #10B981;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border-radius: 8px;
                padding: 0px 20px;
            }
            QPushButton:hover {
                background: #059669;
            }
        """)
        add_button.clicked.connect(self.add_invoice_item)
        
        add_layout.addLayout(product_container)
        add_layout.addLayout(qty_container)
        add_layout.addStretch()
        add_layout.addWidget(add_button)
        
        # Items table
        self.items_table = QTableWidget()
        self.setup_items_table()
        
        layout.addWidget(add_header)
        layout.addWidget(self.items_table, 1)
        
        return frame
    
    def setup_items_table(self):
        """Setup the invoice items table"""
        self.items_table.setColumnCount(5)
        self.items_table.setHorizontalHeaderLabels([
            "کالا", "تعداد", "قیمت واحد", "مبلغ کل", "عملیات"
        ])
        
        # Set table properties
        self.items_table.setAlternatingRowColors(True)
        self.items_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.items_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.items_table.verticalHeader().setVisible(False)
        
        # Set column widths
        header = self.items_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        header.resizeSection(4, 100)
        
        # Set row height
        self.items_table.verticalHeader().setDefaultSectionSize(50)
        
        self.items_table.setStyleSheet("""
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
    
    def create_footer_section(self):
        """Create invoice footer with totals and save button"""
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background: #374151;
                border: 1px solid #6B7280;
                border-radius: 12px;
            }
        """)
        
        layout = QGridLayout(frame)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)
        
        # Subtotal
        subtotal_label = QLabel("💰 جمع کل:")
        subtotal_label.setStyleSheet("font-weight: bold; font-size: 14px; background: transparent;")
        self.subtotal_display = QFrame()
        self.subtotal_display.setStyleSheet("""
            QFrame {
                background: #4B5563;
                border: 2px solid #10B981;
                border-radius: 8px;
                padding: 8px 12px;
            }
        """)
        
        subtotal_layout = QVBoxLayout(self.subtotal_display)
        subtotal_layout.setContentsMargins(0, 0, 0, 0)
        self.subtotal_value = QLabel("0 ریال")
        self.subtotal_value.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #10B981;
            background: transparent;
        """)
        subtotal_layout.addWidget(self.subtotal_value)
        
        # Discount
        discount_label = QLabel("🏷️ تخفیف:")
        discount_label.setStyleSheet("font-weight: bold; font-size: 14px; background: transparent;")
        self.discount_spin = QDoubleSpinBox()
        self.discount_spin.setRange(0, 999999999)
        self.discount_spin.setDecimals(0)
        self.discount_spin.setSuffix(" ریال")
        self.discount_spin.valueChanged.connect(self.calculate_totals)
        
        # Final total
        final_label = QLabel("✅ مبلغ نهایی:")
        final_label.setStyleSheet("font-weight: bold; font-size: 14px; background: transparent;")
        self.final_display = QFrame()
        self.final_display.setStyleSheet("""
            QFrame {
                background: #4B5563;
                border: 2px solid #F59E0B;
                border-radius: 8px;
                padding: 8px 12px;
            }
        """)
        
        final_layout = QVBoxLayout(self.final_display)
        final_layout.setContentsMargins(0, 0, 0, 0)
        self.final_value = QLabel("0 ریال")
        self.final_value.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #F59E0B;
            background: transparent;
        """)
        final_layout.addWidget(self.final_value)
        
        # Save button
        save_button = QPushButton("💾 ثبت و چاپ فاکتور")
        save_button.setFixedHeight(50)
        save_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #3B82F6, stop:1 #10B981);
                color: white;
                font-size: 16px;
                font-weight: bold;
                border-radius: 10px;
                padding: 0px 25px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #2563EB, stop:1 #059669);
            }
        """)
        save_button.clicked.connect(self.save_invoice)
        
        # Layout arrangement
        layout.addWidget(subtotal_label, 0, 0)
        layout.addWidget(self.subtotal_display, 1, 0)
        layout.addWidget(discount_label, 0, 1)
        layout.addWidget(self.discount_spin, 1, 1)
        layout.addWidget(final_label, 0, 2)
        layout.addWidget(self.final_display, 1, 2)
        layout.addWidget(save_button, 0, 3, 2, 1)
        
        return frame
    
    def load_products(self):
        """Load products for selection"""
        try:
            session = get_db_session()
            products = session.query(Product).filter(
                Product.stock_quantity > 0
            ).order_by(Product.product_name).all()
            
            self.available_products = products
            
            self.product_combo.clear()
            self.product_combo.addItem("انتخاب کنید...", None)
            
            for product in products:
                display_text = f"{product.product_name} ({product.product_code}) - {product.sale_price:,.0f} ریال"
                self.product_combo.addItem(display_text, product)
            
            session.close()
            
        except Exception as e:
            QMessageBox.critical(self, "خطا", f"خطا در بارگذاری کالاها: {str(e)}")
    
    def generate_invoice_number(self):
        """Generate a unique invoice number"""
        timestamp = datetime.now().strftime("%Y%m%d")
        random_num = random.randint(1000, 9999)
        invoice_number = f"INV-{timestamp}-{random_num}"
        self.invoice_number_edit.setText(invoice_number)
    
    def add_invoice_item(self):
        """Add selected product to invoice items"""
        if self.product_combo.currentIndex() == 0:
            QMessageBox.warning(self, "خطا", "لطفاً یک کالا انتخاب کنید.")
            return
        
        selected_product = self.product_combo.currentData()
        if not selected_product:
            return
        
        quantity = self.quantity_spin.value()
        
        if quantity > selected_product.stock_quantity:
            QMessageBox.warning(
                self, "خطا", 
                f"موجودی کافی نیست. موجودی فعلی: {selected_product.stock_quantity}"
            )
            return
        
        # Check if product already exists in items
        for item in self.current_invoice_items:
            if item['product'].id == selected_product.id:
                item['quantity'] += quantity
                item['row_total'] = item['quantity'] * item['unit_price']
                break
        else:
            # Add new item
            item = {
                'product': selected_product,
                'quantity': quantity,
                'unit_price': selected_product.sale_price,
                'row_total': quantity * selected_product.sale_price
            }
            self.current_invoice_items.append(item)
        
        self.refresh_items_table()
        self.calculate_totals()
        
        # Reset form
        self.product_combo.setCurrentIndex(0)
        self.quantity_spin.setValue(1)
    
    def remove_invoice_item(self, index):
        """Remove item from invoice"""
        if 0 <= index < len(self.current_invoice_items):
            self.current_invoice_items.pop(index)
            self.refresh_items_table()
            self.calculate_totals()
    
    def refresh_items_table(self):
        """Refresh the invoice items table"""
        self.items_table.setRowCount(len(self.current_invoice_items))
        
        for row, item in enumerate(self.current_invoice_items):
            # Product name
            self.items_table.setItem(row, 0, QTableWidgetItem(item['product'].product_name))
            
            # Quantity
            self.items_table.setItem(row, 1, QTableWidgetItem(str(item['quantity'])))
            
            # Unit price
            price_str = f"{item['unit_price']:,.0f} ریال"
            self.items_table.setItem(row, 2, QTableWidgetItem(price_str))
            
            # Row total
            total_str = f"{item['row_total']:,.0f} ریال"
            self.items_table.setItem(row, 3, QTableWidgetItem(total_str))
            
            # Delete button
            delete_button = QPushButton("🗑️ حذف")
            delete_button.setStyleSheet("""
                QPushButton {
                    background: #EF4444;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 6px 12px;
                    font-size: 12px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background: #DC2626;
                }
            """)
            delete_button.clicked.connect(lambda checked, i=row: self.remove_invoice_item(i))
            self.items_table.setCellWidget(row, 4, delete_button)
    
    def calculate_totals(self):
        """Calculate invoice totals"""
        subtotal = sum(item['row_total'] for item in self.current_invoice_items)
        discount = Decimal(str(self.discount_spin.value()))
        final_total = subtotal - discount
        
        self.subtotal_value.setText(f"{subtotal:,.0f} ریال")
        self.final_value.setText(f"{final_total:,.0f} ریال")
    
    def save_invoice(self):
        """Save the invoice to database"""
        if not self.customer_edit.text().strip():
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
                customer_name=self.customer_edit.text().strip(),
                issue_date=self.date_edit.date().toPython(),
                total_price=subtotal,
                discount=discount,
                final_price=final_total
            )
            
            session.add(invoice)
            session.flush()  # Get the invoice ID
            
            # Add invoice items and update stock
            for item_data in self.current_invoice_items:
                # Create invoice item
                invoice_item = InvoiceItem(
                    invoice_id=invoice.id,
                    product_id=item_data['product'].id,
                    quantity=item_data['quantity'],
                    unit_price=item_data['unit_price'],
                    row_total=item_data['row_total']
                )
                session.add(invoice_item)
                
                # Update product stock
                product = session.query(Product).filter(
                    Product.id == item_data['product'].id
                ).first()
                if product:
                    product.stock_quantity -= item_data['quantity']
            
            session.commit()
            session.close()
            
            QMessageBox.information(
                self, "موفقیت", 
                f"فاکتور شماره {invoice.invoice_number} با موفقیت ثبت شد."
            )
            
            # Ask about printing
            reply = QMessageBox.question(
                self, "چاپ فاکتور",
                "آیا می‌خواهید فاکتور را چاپ کنید؟",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.Yes
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                self.print_invoice(invoice)
            
            # Clear form
            self.clear_form()
            self.load_products()  # Refresh products list
            
        except Exception as e:
            QMessageBox.critical(self, "خطا", f"خطا در ثبت فاکتور: {str(e)}")
    
    def print_invoice(self, invoice):
        """Print the invoice"""
        try:
            # Create a simple print dialog
            printer = QPrinter()
            printer.setPageSize(QPrinter.PageSize.A4)
            
            # Create HTML content for printing
            html_content = self.generate_print_html(invoice)
            
            # Create QTextDocument and print
            document = QTextDocument()
            document.setHtml(html_content)
            document.print(printer)
            
            QMessageBox.information(self, "چاپ", "فاکتور آماده چاپ شد.")
            
        except Exception as e:
            QMessageBox.warning(self, "خطا در چاپ", f"خطا در چاپ فاکتور: {str(e)}")
    
    def generate_print_html(self, invoice):
        """Generate HTML content for printing"""
        items_html = ""
        for i, item in enumerate(self.current_invoice_items, 1):
            items_html += f"""
            <tr>
                <td style="text-align: center; padding: 8px; border: 1px solid #ccc;">{i}</td>
                <td style="padding: 8px; border: 1px solid #ccc;">{item['product'].product_name}</td>
                <td style="text-align: center; padding: 8px; border: 1px solid #ccc;">{item['quantity']}</td>
                <td style="text-align: center; padding: 8px; border: 1px solid #ccc;">{item['unit_price']:,.0f}</td>
                <td style="text-align: center; padding: 8px; border: 1px solid #ccc;">{item['row_total']:,.0f}</td>
            </tr>
            """
        
        html = f"""
        <!DOCTYPE html>
        <html dir="rtl">
        <head>
            <meta charset="utf-8">
            <style>
                body {{ font-family: 'Tahoma', sans-serif; direction: rtl; }}
                .header {{ text-align: center; margin-bottom: 30px; }}
                .invoice-info {{ margin: 20px 0; }}
                table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                th {{ background: #f0f0f0; padding: 10px; border: 1px solid #ccc; }}
                .totals {{ margin-top: 20px; text-align: right; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>شرکت نمونه تجارت پارس</h1>
                <p>صورتحساب فروش</p>
            </div>
            
            <div class="invoice-info">
                <p><strong>شماره فاکتور:</strong> {invoice.invoice_number}</p>
                <p><strong>نام مشتری:</strong> {invoice.customer_name}</p>
                <p><strong>تاریخ صدور:</strong> {invoice.issue_date.strftime('%Y/%m/%d')}</p>
            </div>
            
            <table>
                <thead>
                    <tr>
                        <th>ردیف</th>
                        <th>شرح کالا</th>
                        <th>تعداد</th>
                        <th>قیمت واحد (ریال)</th>
                        <th>مبلغ کل (ریال)</th>
                    </tr>
                </thead>
                <tbody>
                    {items_html}
                </tbody>
            </table>
            
            <div class="totals">
                <p><strong>جمع کل: {invoice.total_price:,.0f} ریال</strong></p>
                <p><strong>تخفیف: {invoice.discount:,.0f} ریال</strong></p>
                <p><strong>مبلغ نهایی: {invoice.final_price:,.0f} ریال</strong></p>
            </div>
            
            <div style="margin-top: 50px; text-align: center;">
                <p>با تشکر از خرید شما</p>
            </div>
        </body>
        </html>
        """
        return html
    
    def clear_form(self):
        """Clear the invoice form"""
        self.customer_edit.clear()
        self.current_invoice_items.clear()
        self.discount_spin.setValue(0)
        self.date_edit.setDate(QDate.currentDate())
        self.generate_invoice_number()
        self.refresh_items_table()
        self.calculate_totals()