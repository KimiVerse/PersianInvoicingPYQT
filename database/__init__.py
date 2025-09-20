# File: database/__init__.py
"""
Database package for Persian Invoicing System
Using direct SQLite instead of SQLAlchemy for Python 3.13 compatibility
"""

from .models import (
    Product, 
    Invoice, 
    InvoiceItem, 
    DatabaseManager, 
    db_manager, 
    create_database, 
    test_database_connection, 
    get_db_session
)

__all__ = [
    'Product',
    'Invoice', 
    'InvoiceItem',
    'DatabaseManager',
    'db_manager',
    'create_database',
    'test_database_connection',
    'get_db_session'
]

# File: updated_basic_window.py
"""
Updated basic window for testing (No SQLAlchemy)
"""

def create_basic_window():
    """Create a basic window for testing"""
    from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                                QLabel, QPushButton, QMessageBox)
    from PyQt6.QtCore import Qt
    
    class BasicWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Persian Invoicing System - Basic Mode")
            self.setGeometry(100, 100, 800, 600)
            self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
            
            # Create central widget
            central_widget = QWidget()
            self.setCentralWidget(central_widget)
            
            # Create layout
            layout = QVBoxLayout(central_widget)
            layout.setSpacing(20)
            layout.setContentsMargins(50, 50, 50, 50)
            
            # Title
            title = QLabel("🎉 Persian Invoicing System")
            title.setStyleSheet("""
                QLabel {
                    font-size: 24px;
                    font-weight: bold;
                    color: #2563EB;
                    padding: 20px;
                    background: #F3F4F6;
                    border-radius: 10px;
                    border: 2px solid #2563EB;
                }
            """)
            title.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            # Status
            status = QLabel("✅ Application is running successfully!")
            status.setStyleSheet("""
                QLabel {
                    font-size: 16px;
                    color: #059669;
                    padding: 15px;
                    background: #ECFDF5;
                    border-radius: 8px;
                    border: 1px solid #10B981;
                }
            """)
            status.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            # Info
            info = QLabel("""
اطلاعات سیستم:
• پایگاه داده: SQLite مستقیم (بدون SQLAlchemy)
• رابط کاربری: حالت پایه  
• زبان: فارسی (راست به چپ)
• سازگاری: Python 3.13
• وضعیت: سالم

برای استفاده از نسخه کامل، فایل main_window.py موجود است.
            """)
            info.setStyleSheet("""
                QLabel {
                    font-size: 14px;
                    color: #374151;
                    padding: 20px;
                    background: white;
                    border-radius: 8px;
                    border: 1px solid #D1D5DB;
                    line-height: 1.6;
                }
            """)
            
            # Test buttons layout
            buttons_layout = QVBoxLayout()
            
            # Test database button
            test_db_btn = QPushButton("🧪 Test Database Connection")
            test_db_btn.setStyleSheet("""
                QPushButton {
                    font-size: 16px;
                    font-weight: bold;
                    color: white;
                    background: #3B82F6;
                    padding: 15px 30px;
                    border: none;
                    border-radius: 8px;
                    margin: 5px;
                }
                QPushButton:hover {
                    background: #2563EB;
                }
                QPushButton:pressed {
                    background: #1D4ED8;
                }
            """)
            test_db_btn.clicked.connect(self.test_database)
            
            # Test products button
            test_products_btn = QPushButton("📦 Test Products Operations")
            test_products_btn.setStyleSheet("""
                QPushButton {
                    font-size: 16px;
                    font-weight: bold;
                    color: white;
                    background: #10B981;
                    padding: 15px 30px;
                    border: none;
                    border-radius: 8px;
                    margin: 5px;
                }
                QPushButton:hover {
                    background: #059669;
                }
            """)
            test_products_btn.clicked.connect(self.test_products)
            
            # Open full app button
            open_app_btn = QPushButton("🚀 Open Full Application")
            open_app_btn.setStyleSheet("""
                QPushButton {
                    font-size: 18px;
                    font-weight: bold;
                    color: white;
                    background: #7C3AED;
                    padding: 20px 40px;
                    border: none;
                    border-radius: 10px;
                    margin: 10px;
                }
                QPushButton:hover {
                    background: #5B21B6;
                }
            """)
            open_app_btn.clicked.connect(self.open_full_app)
            
            buttons_layout.addWidget(test_db_btn)
            buttons_layout.addWidget(test_products_btn)
            buttons_layout.addWidget(open_app_btn)
            
            # Add widgets to layout
            layout.addWidget(title)
            layout.addWidget(status)
            layout.addWidget(info)
            layout.addLayout(buttons_layout)
            layout.addStretch()
            
            # Set window style
            self.setStyleSheet("""
                QMainWindow {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #F9FAFB, stop:1 #F3F4F6);
                }
            """)
        
        def test_database(self):
            """Test database connection"""
            try:
                from database.models import test_database_connection, db_manager, Product
                
                if test_database_connection():
                    # Try to count products
                    product_count = db_manager.count_products()
                    
                    QMessageBox.information(
                        self, 
                        "Database Test", 
                        f"✅ Database connection successful!\n\n"
                        f"Products in database: {product_count}\n"
                        f"Database type: Direct SQLite\n"
                        f"Python 3.13 compatible: Yes"
                    )
                else:
                    QMessageBox.warning(
                        self, 
                        "Database Test", 
                        "❌ Database connection failed!"
                    )
            except Exception as e:
                QMessageBox.critical(
                    self, 
                    "Database Test", 
                    f"❌ Database test error:\n{str(e)}"
                )
        
        def test_products(self):
            """Test product operations"""
            try:
                from database.models import db_manager, Product
                from decimal import Decimal
                import random
                
                # Create a test product
                test_code = f"TEST{random.randint(100, 999)}"
                test_product = Product(
                    product_code=test_code,
                    product_name="محصول تستی",
                    purchase_price=Decimal("10000"),
                    sale_price=Decimal("15000"),
                    stock_quantity=50,
                    unit="عدد"
                )
                
                # Add product
                if db_manager.add_product(test_product):
                    # Get products
                    products = db_manager.get_products()
                    
                    # Find our test product
                    found = any(p.product_code == test_code for p in products)
                    
                    if found:
                        QMessageBox.information(
                            self,
                            "Products Test",
                            f"✅ Product operations test successful!\n\n"
                            f"✅ Created test product: {test_code}\n"
                            f"✅ Product found in database\n"
                            f"✅ Total products: {len(products)}\n\n"
                            f"Test product will be automatically cleaned up."
                        )
                        
                        # Clean up - delete test product
                        test_product_from_db = next(p for p in products if p.product_code == test_code)
                        db_manager.delete_product(test_product_from_db.id)
                    else:
                        QMessageBox.warning(self, "Products Test", "❌ Could not find test product")
                else:
                    QMessageBox.warning(self, "Products Test", "❌ Could not create test product")
                    
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Products Test", 
                    f"❌ Product test error:\n{str(e)}"
                )
        
        def open_full_app(self):
            """Open the full application"""
            try:
                # Close this basic window
                self.close()
                
                # Try to import and open main window
                from main_window import MainWindow
                
                self.main_window = MainWindow()
                self.main_window.show()
                
            except ImportError:
                QMessageBox.warning(
                    self,
                    "Full App",
                    "❌ main_window.py not found!\n\n"
                    "The basic interface will continue running.\n"
                    "Make sure main_window.py is in the same directory."
                )
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Full App Error",
                    f"❌ Error opening full application:\n{str(e)}"
                )
    
    return BasicWindow()

# File: create_sample_data.py
"""
Script to create sample data for testing
"""

def create_sample_data():
    """Create sample products and invoices for testing"""
    try:
        from database.models import db_manager, Product, Invoice, InvoiceItem
        from decimal import Decimal
        from datetime import datetime
        import random
        
        print("Creating sample data...")
        
        # Sample products
        sample_products = [
            Product(
                product_code="LAP001",
                product_name="لپ‌تاپ ایسوس VivoBook",
                purchase_price=Decimal("15000000"),
                sale_price=Decimal("18000000"),
                stock_quantity=15,
                unit="عدد"
            ),
            Product(
                product_code="MSE001", 
                product_name="ماوس بی‌سیم لاجیتک",
                purchase_price=Decimal("150000"),
                sale_price=Decimal("200000"),
                stock_quantity=50,
                unit="عدد"
            ),
            Product(
                product_code="KBD001",
                product_name="کیبورد مکانیکی گیمینگ",
                purchase_price=Decimal("800000"),
                sale_price=Decimal("1200000"),
                stock_quantity=25,
                unit="عدد"
            ),
            Product(
                product_code="HDD001",
                product_name="هارد اکسترنال ۱ ترابایت",
                purchase_price=Decimal("2000000"),
                sale_price=Decimal("2500000"),
                stock_quantity=30,
                unit="عدد"
            ),
            Product(
                product_code="CBL001",
                product_name="کابل USB Type-C",
                purchase_price=Decimal("50000"),
                sale_price=Decimal("80000"),
                stock_quantity=100,
                unit="عدد"
            )
        ]
        
        # Add products
        added_products = []
        for product in sample_products:
            if db_manager.add_product(product):
                added_products.append(product)
                print(f"✅ Added product: {product.product_name}")
            else:
                print(f"⚠️ Product {product.product_code} might already exist")
        
        # Create sample invoices
        customers = ["علی احمدی", "فاطمه محمدی", "رضا کریمی", "مریم رضایی", "حسن علوی"]
        
        for i in range(3):
            customer = random.choice(customers)
            invoice_number = f"INV-{datetime.now().strftime('%Y%m%d')}-{1000 + i}"
            
            # Select random products for invoice
            selected_products = random.sample(added_products, random.randint(1, 3))
            
            invoice_items = []
            total = Decimal('0')
            
            for product in selected_products:
                quantity = random.randint(1, 3)
                unit_price = product.sale_price
                row_total = quantity * unit_price
                total += row_total
                
                invoice_items.append(InvoiceItem(
                    product_id=product.id,
                    quantity=quantity,
                    unit_price=unit_price,
                    row_total=row_total
                ))
            
            discount = Decimal('0') if random.random() > 0.3 else total * Decimal('0.05')  # 5% discount sometimes
            final_price = total - discount
            
            invoice = Invoice(
                invoice_number=invoice_number,
                customer_name=customer,
                issue_date=datetime.now(),
                total_price=total,
                discount=discount,
                final_price=final_price,
                items=invoice_items
            )
            
            if db_manager.add_invoice(invoice):
                print(f"✅ Added invoice: {invoice_number} for {customer}")
            else:
                print(f"❌ Failed to add invoice: {invoice_number}")
        
        print("\n🎉 Sample data created successfully!")
        print(f"📦 Products added: {len(added_products)}")
        print(f"🧾 Invoices created: 3")
        print("\nYou can now test the full application with real data!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating sample data: {e}")
        return False

if __name__ == "__main__":
    from database.models import create_database
    
    print("🚀 Creating Persian Invoicing Sample Data")
    print("=" * 45)
    
    # Create database first
    if create_database():
        create_sample_data()
    else:
        print("❌ Could not create database!")
    
    input("\nPress Enter to exit...")

# File: run_tests.py
"""
Run all tests and setup verification
"""

def main():
    """Run comprehensive tests"""
    print("🔬 Running Comprehensive Tests")
    print("=" * 40)
    
    try:
        import test_setup
        success = test_setup.main()
        
        if success:
            print("\n" + "=" * 40)
            print("🎉 All tests passed!")
            print("\n🚀 Ready to run:")
            print("   python main.py              # Full application")
            print("   python create_sample_data.py # Add test data")
            print("   python quick_install.py     # Re-run installer")
            
        return success
        
    except Exception as e:
        print(f"❌ Test runner failed: {e}")
        return False

if __name__ == "__main__":
    main()
    input("\nPress Enter to exit...")