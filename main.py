# Fixed Main Application (No SQLAlchemy)
# File: main.py

import sys
import os
import traceback
from pathlib import Path

def check_dependencies():
    """Check if all required dependencies are available"""
    missing_deps = []
    
    try:
        import PyQt6
        print("✅ PyQt6 found")
    except ImportError:
        missing_deps.append("PyQt6")
    
    try:
        import dateutil
        print("✅ python-dateutil found")
    except ImportError:
        missing_deps.append("python-dateutil")
    
    try:
        import sqlite3
        print("✅ SQLite3 (built-in) available")
    except ImportError:
        missing_deps.append("sqlite3")
    
    if missing_deps:
        print(f"\n❌ Missing dependencies: {', '.join(missing_deps)}")
        print("Please run: pip install PyQt6 python-dateutil")
        return False
    
    return True

def create_required_directories():
    """Create necessary directories"""
    directories = ["logs", "backups", "exports"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)

def main():
    """Main application entry point"""
    print("🚀 Persian Invoicing System")
    print("=" * 40)
    
    # Check dependencies first
    if not check_dependencies():
        input("Press Enter to exit...")
        return 1
    
    # Create directories
    create_required_directories()
    
    try:
        # Import PyQt6 components
        from PyQt6.QtWidgets import QApplication, QMessageBox
        from PyQt6.QtCore import Qt
        
        # Create application
        app = QApplication(sys.argv)
        app.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        
        # Try to import and initialize database
        print("🔄 Initializing database...")
        try:
            from database.models import create_database, test_database_connection
            
            if not create_database():
                raise Exception("Failed to create database")
            
            if not test_database_connection():
                raise Exception("Database connection test failed")
            
            print("✅ Database initialized successfully")
            
        except Exception as e:
            error_msg = f"Database initialization failed: {str(e)}"
            print(f"❌ {error_msg}")
            QMessageBox.critical(None, "Database Error", error_msg)
            return 1
        
        # Try to import and create main window
        print("🔄 Loading main application...")
        try:
            from main_window import MainWindow
            
            # Create and show main window
            window = MainWindow()
            window.show()
            
            print("✅ Application started successfully!")
            print("📱 Main window is now open")
            
            # Start the application event loop
            return app.exec()
            
        except ImportError:
            # Fallback to basic window if main_window.py doesn't exist
            print("⚠️  main_window.py not found, creating basic interface...")
            from updated_basic_window import create_basic_window
            
            window = create_basic_window()
            window.show()
            
            print("✅ Basic interface started successfully!")
            print("📱 Basic window is now open")
            
            return app.exec()
            
    except Exception as e:
        error_msg = f"Application failed to start: {str(e)}"
        print(f"❌ {error_msg}")
        print("\nFull error details:")
        traceback.print_exc()
        
        try:
            from PyQt6.QtWidgets import QApplication, QMessageBox
            if QApplication.instance() is None:
                app = QApplication([])
            QMessageBox.critical(None, "Application Error", error_msg)
        except:
            pass
        
        input("\nPress Enter to exit...")
        return 1

if __name__ == "__main__":
    sys.exit(main())

# Also create basic_window.py (in case updated_basic_window.py import fails)
# File: basic_window.py

def create_basic_window():
    """Create a basic window for testing"""
    from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                                QLabel, QPushButton, QMessageBox)
    from PyQt6.QtCore import Qt
    
    class BasicWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Persian Invoicing System - Working!")
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
            title = QLabel("🎉 سیستم مدیریت فاکتور فروش")
            title.setStyleSheet("""
                QLabel {
                    font-size: 28px;
                    font-weight: bold;
                    color: #2563EB;
                    padding: 25px;
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #EBF4FF, stop:1 #DBEAFE);
                    border-radius: 15px;
                    border: 3px solid #3B82F6;
                }
            """)
            title.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            # Success status
            status = QLabel("✅ برنامه با موفقیت اجرا شد!")
            status.setStyleSheet("""
                QLabel {
                    font-size: 18px;
                    color: #059669;
                    padding: 20px;
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #ECFDF5, stop:1 #D1FAE5);
                    border-radius: 10px;
                    border: 2px solid #10B981;
                    font-weight: bold;
                }
            """)
            status.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            # Features info
            features = QLabel("""
🎯 ویژگی‌های سیستم:

📊 داشبورد با آمار لحظه‌ای
📦 مدیریت کامل محصولات  
🧾 صدور فاکتور حرفه‌ای
💾 پایگاه داده SQLite مستقل
🌙 ظاهر مدرن تیره
🔄 سازگاری کامل با Python 3.13

همه چیز آماده است! 🚀
            """)
            features.setStyleSheet("""
                QLabel {
                    font-size: 16px;
                    color: #374151;
                    padding: 25px;
                    background: white;
                    border-radius: 10px;
                    border: 1px solid #D1D5DB;
                    line-height: 1.8;
                }
            """)
            
            # Test database button
            test_btn = QPushButton("🧪 تست پایگاه داده")
            test_btn.setStyleSheet("""
                QPushButton {
                    font-size: 18px;
                    font-weight: bold;
                    color: white;
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #3B82F6, stop:1 #1D4ED8);
                    padding: 18px 35px;
                    border: none;
                    border-radius: 10px;
                    margin: 10px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #2563EB, stop:1 #1E40AF);
                }
                QPushButton:pressed {
                    background: #1D4ED8;
                }
            """)
            test_btn.clicked.connect(self.test_database)
            
            # Open full app button (if available)
            full_app_btn = QPushButton("🚀 باز کردن برنامه کامل")
            full_app_btn.setStyleSheet("""
                QPushButton {
                    font-size: 20px;
                    font-weight: bold;
                    color: white;
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #10B981, stop:1 #047857);
                    padding: 20px 40px;
                    border: none;
                    border-radius: 12px;
                    margin: 15px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #059669, stop:1 #065F46);
                }
            """)
            full_app_btn.clicked.connect(self.open_full_app)
            
            # Add widgets to layout
            layout.addWidget(title)
            layout.addWidget(status)
            layout.addWidget(features)
            layout.addWidget(test_btn)
            layout.addWidget(full_app_btn)
            layout.addStretch()
            
            # Set window style
            self.setStyleSheet("""
                QMainWindow {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #F8FAFC, stop:1 #F1F5F9);
                }
            """)
        
        def test_database(self):
            """Test database operations"""
            try:
                from database.models import test_database_connection, db_manager, Product
                from decimal import Decimal
                import random
                
                if test_database_connection():
                    # Test adding a sample product
                    test_code = f"TEST{random.randint(100, 999)}"
                    test_product = Product(
                        product_code=test_code,
                        product_name="محصول تستی",
                        purchase_price=Decimal("10000"),
                        sale_price=Decimal("15000"),
                        stock_quantity=10,
                        unit="عدد"
                    )
                    
                    if db_manager.add_product(test_product):
                        product_count = db_manager.count_products()
                        
                        # Clean up
                        products = db_manager.get_products()
                        test_product_from_db = next(p for p in products if p.product_code == test_code)
                        db_manager.delete_product(test_product_from_db.id)
                        
                        QMessageBox.information(
                            self, 
                            "تست پایگاه داده", 
                            f"✅ تست پایگاه داده موفق!\n\n"
                            f"📊 عملیات انجام شده:\n"
                            f"   • ایجاد محصول تستی: {test_code}\n"
                            f"   • خواندن از پایگاه داده\n"
                            f"   • حذف محصول تستی\n\n"
                            f"📦 تعداد محصولات: {product_count}\n"
                            f"💾 نوع پایگاه داده: SQLite مستقیم\n"
                            f"🐍 سازگاری Python 3.13: بله"
                        )
                    else:
                        QMessageBox.warning(self, "تست پایگاه داده", "❌ خطا در ایجاد محصول تستی")
                else:
                    QMessageBox.warning(self, "تست پایگاه داده", "❌ اتصال به پایگاه داده ناموفق!")
                    
            except Exception as e:
                QMessageBox.critical(
                    self, 
                    "خطای تست", 
                    f"❌ خطا در تست پایگاه داده:\n{str(e)}"
                )
        
        def open_full_app(self):
            """Try to open the full application"""
            try:
                # Close this window
                self.close()
                
                # Try to import and open main window
                from main_window import MainWindow
                
                self.main_window = MainWindow()
                self.main_window.show()
                
                QMessageBox.information(
                    None,
                    "برنامه کامل", 
                    "✅ برنامه کامل با موفقیت باز شد!"
                )
                
            except ImportError:
                QMessageBox.warning(
                    self,
                    "برنامه کامل",
                    "⚠️ فایل main_window.py یافت نشد!\n\n"
                    "برای استفاده از رابط کامل، مطمئن شوید که\n"
                    "فایل main_window.py در همین پوشه موجود است."
                )
                # Reopen this window
                self.show()
                
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "خطای برنامه",
                    f"❌ خطا در باز کردن برنامه کامل:\n{str(e)}"
                )
                # Reopen this window
                self.show()
    
    return BasicWindow()