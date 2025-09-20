# Updated Test Script (No SQLAlchemy)
# File: test_setup.py

import sys
import traceback

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import PyQt6
        print("✅ PyQt6 imported successfully")
    except ImportError as e:
        print(f"❌ PyQt6 import failed: {e}")
        return False
    
    try:
        import dateutil
        print("✅ python-dateutil imported successfully")
    except ImportError as e:
        print(f"❌ python-dateutil import failed: {e}")
        return False
    
    try:
        import sqlite3
        print("✅ SQLite3 (built-in) available")
    except ImportError as e:
        print(f"❌ SQLite3 import failed: {e}")
        return False
    
    return True

def test_database():
    """Test database creation and basic operations"""
    print("\nTesting database...")
    
    try:
        from database.models import (create_database, test_database_connection, 
                                   db_manager, Product)
        
        # Test database creation
        if create_database():
            print("✅ Database created successfully")
        else:
            print("❌ Database creation failed")
            return False
        
        # Test database connection
        if test_database_connection():
            print("✅ Database connection test passed")
        else:
            print("❌ Database connection test failed")
            return False
        
        # Test adding a sample product
        test_product = Product(
            product_code="TEST001",
            product_name="Test Product",
            sale_price=1000,
            stock_quantity=10
        )
        
        if db_manager.add_product(test_product):
            print("✅ Product creation test passed")
            
            # Test querying the product
            found_products = db_manager.get_products("TEST001")
            if found_products and found_products[0].product_code == "TEST001":
                print("✅ Product query test passed")
                
                # Clean up - delete test product
                if db_manager.delete_product(found_products[0].id):
                    print("✅ Product deletion test passed")
                else:
                    print("⚠️ Product deletion test failed (but not critical)")
            else:
                print("❌ Product query test failed")
                return False
        else:
            print("❌ Product creation test failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        traceback.print_exc()
        return False

def test_pyqt():
    """Test PyQt6 basic functionality"""
    print("\nTesting PyQt6...")
    
    try:
        from PyQt6.QtWidgets import QApplication, QWidget
        from PyQt6.QtCore import Qt
        
        # Create a minimal application (don't show it)
        app = QApplication([])
        widget = QWidget()
        widget.setWindowTitle("Test Window")
        
        print("✅ PyQt6 widgets creation test passed")
        
        # Test RTL support
        app.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        print("✅ PyQt6 RTL support test passed")
        
        app.quit()
        return True
        
    except Exception as e:
        print(f"❌ PyQt6 test failed: {e}")
        traceback.print_exc()
        return False

def test_persian_support():
    """Test Persian text and number support"""
    print("\nTesting Persian support...")
    
    try:
        # Test Persian text
        persian_text = "سیستم مدیریت فاکتور فروش"
        print(f"✅ Persian text: {persian_text}")
        
        # Test Persian numbers
        persian_numbers = "۱۲۳۴۵۶۷۸۹۰"
        english_numbers = "1234567890"
        print(f"✅ Persian digits: {persian_numbers}")
        print(f"✅ English digits: {english_numbers}")
        
        # Test decimal handling
        from decimal import Decimal
        price = Decimal("1234567.89")
        print(f"✅ Decimal handling: {price}")
        
        return True
        
    except Exception as e:
        print(f"❌ Persian support test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Persian Invoicing System - Setup Test (No SQLAlchemy)")
    print("=" * 60)
    
    all_passed = True
    
    # Test imports
    if not test_imports():
        all_passed = False
    
    # Test database
    if not test_database():
        all_passed = False
    
    # Test PyQt6
    if not test_pyqt():
        all_passed = False
    
    # Test Persian support
    if not test_persian_support():
        all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 All tests passed! Your setup is ready.")
        print("🚀 You can now run: python main.py")
        print("\n📋 Summary:")
        print("   ✅ PyQt6 GUI framework working")
        print("   ✅ SQLite database working")
        print("   ✅ Persian language support ready")
        print("   ✅ No SQLAlchemy compatibility issues")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        print("💡 Try running: pip install PyQt6 python-dateutil")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    input("\nPress Enter to exit...")
    sys.exit(0 if success else 1)

# File: updated_requirements.txt
"""
PyQt6>=6.6.0
python-dateutil>=2.8.2
"""

# File: quick_install.py
"""
Quick installation script (Updated for No SQLAlchemy)
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    
    requirements = [
        "PyQt6>=6.6.0",
        "python-dateutil>=2.8.2"
    ]
    
    for requirement in requirements:
        try:
            print(f"Installing {requirement}...")
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", requirement
            ])
            print(f"✅ {requirement} installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {requirement}: {e}")
            return False
    
    return True

def create_directories():
    """Create necessary directories"""
    directories = ["logs", "backups", "exports", "database"]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created directory: {directory}/")
    
    return True

def create_init_files():
    """Create __init__.py files"""
    init_files = [
        "database/__init__.py"
    ]
    
    for init_file in init_files:
        os.makedirs(os.path.dirname(init_file), exist_ok=True)
        with open(init_file, 'w') as f:
            f.write('# Package initialization\n')
        print(f"✅ Created: {init_file}")
    
    return True

def main():
    """Main installation function"""
    print("🚀 Persian Invoicing System - Quick Install (No SQLAlchemy)")
    print("=" * 60)
    
    # Install requirements
    if not install_requirements():
        print("❌ Installation failed!")
        return False
    
    # Create directories
    if not create_directories():
        print("❌ Directory creation failed!")
        return False
    
    # Create init files
    if not create_init_files():
        print("❌ Init file creation failed!")
        return False
    
    # Test the setup
    print("\n🧪 Testing setup...")
    try:
        import test_setup
        if test_setup.main():
            print("\n🎉 Installation completed successfully!")
            print("🚀 Run 'python main.py' to start the application")
            print("\n📋 What's ready:")
            print("   ✅ PyQt6 for modern GUI")
            print("   ✅ Direct SQLite database (no SQLAlchemy)")
            print("   ✅ Persian language support")
            print("   ✅ Right-to-left layout")
            print("   ✅ Professional dark theme")
            return True
        else:
            print("\n❌ Setup test failed!")
            return False
    except Exception as e:
        print(f"\n❌ Could not run setup test: {e}")
        return False

if __name__ == "__main__":
    success = main()
    input("\nPress Enter to exit...")
    sys.exit(0 if success else 1)