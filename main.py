# Simplified Main Application
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
        import sqlalchemy
        print("✅ SQLAlchemy found")
    except ImportError:
        missing_deps.append("SQLAlchemy")
    
    try:
        import dateutil
        print("✅ python-dateutil found")
    except ImportError:
        missing_deps.append("python-dateutil")
    
    if missing_deps:
        print(f"\n❌ Missing dependencies: {', '.join(missing_deps)}")
        print("Please run: pip install PyQt6 SQLAlchemy python-dateutil")
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
            from basic_window import create_basic_window
            
            window = create_basic_window()
            window.show()
            
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

# File: basic_window.py
"""
Basic window for testing and fallback
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
• پایگاه داده: آماده و فعال
• رابط کاربری: حالت پایه
• زبان: فارسی (راست به چپ)
• وضعیت: سالم

برای استفاده از نسخه کامل، فایل main_window.py را اضافه کنید.
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
            
            # Test button
            test_btn = QPushButton("🧪 Test Database Connection")
            test_btn.setStyleSheet("""
                QPushButton {
                    font-size: 16px;
                    font-weight: bold;
                    color: white;
                    background: #3B82F6;
                    padding: 15px 30px;
                    border: none;
                    border-radius: 8px;
                }
                QPushButton:hover {
                    background: #2563EB;
                }
                QPushButton:pressed {
                    background: #1D4ED8;
                }
            """)
            test_btn.clicked.connect(self.test_database)
            
            # Add widgets to layout
            layout.addWidget(title)
            layout.addWidget(status)
            layout.addWidget(info)
            layout.addWidget(test_btn)
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
                from database.models import test_database_connection, get_db_session, Product
                
                if test_database_connection():
                    # Try to count products
                    session = get_db_session()
                    product_count = session.query(Product).count()
                    session.close()
                    
                    QMessageBox.information(
                        self, 
                        "Database Test", 
                        f"✅ Database connection successful!\n\nProducts in database: {product_count}"
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
    
    return BasicWindow()

if __name__ == "__main__":
    sys.exit(main())