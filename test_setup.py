# File: test_setup.py
"""
Test script to verify the setup is working correctly
"""

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
        import sqlalchemy
        print(f"✅ SQLAlchemy {sqlalchemy.__version__} imported successfully")
    except ImportError as e:
        print(f"❌ SQLAlchemy import failed: {e}")
        return False
    
    try:
        import dateutil
        print("✅ python-dateutil imported successfully")
    except ImportError as e:
        print(f"❌ python-dateutil import failed: {e}")
        return False
    
    return True

def test_database():
    """Test database creation and basic operations"""
    print("\nTesting database...")
    
    try:
        from database.models import create_database, get_db_session, Product, test_database_connection
        
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
        session = get_db_session()
        test_product = Product(
            product_code="TEST001",
            product_name="Test Product",
            sale_price=1000,
            stock_quantity=10
        )
        
        session.add(test_product)
        session.commit()
        
        # Test querying the product
        found_product = session.query(Product).filter(Product.product_code == "TEST001").first()
        if found_product:
            print("✅ Database operations test passed")
            # Clean up
            session.delete(found_product)
            session.commit()
        else:
            print("❌ Database operations test failed")
            return False
        
        session.close()
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

def main():
    """Run all tests"""
    print("🚀 Persian Invoicing System - Setup Test")
    print("=" * 50)
    
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
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All tests passed! Your setup is ready.")
        print("🚀 You can now run: python main.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        print("💡 Try running: pip install -r requirements.txt")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
