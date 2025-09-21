#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تست راه‌اندازی سیستم فاکتور فارسی - نسخه تصحیح شده
"""

import sys
import traceback
import os

def test_imports():
    """تست import های اساسی"""
    print("تست import ها...")
    
    try:
        import PyQt6
        print("✅ PyQt6")
    except ImportError:
        print("❌ PyQt6 نصب نیست")
        return False
    
    try:
        import sqlalchemy
        print("✅ SQLAlchemy")
    except ImportError:
        print("❌ SQLAlchemy نصب نیست")
        return False
    
    return True

def test_database():
    """تست دیتابیس"""
    print("تست دیتابیس...")
    
    try:
        from services.database_service import DatabaseService
        
        # تست ایجاد دیتابیس
        test_db = "test_temp.db"
        if os.path.exists(test_db):
            os.remove(test_db)
        
        db_service = DatabaseService(db_path=test_db)
        print("✅ دیتابیس")
        
        # تنظیف
        db_service.close()
        if os.path.exists(test_db):
            os.remove(test_db)
        
        return True
        
    except Exception as e:
        print(f"❌ دیتابیس: {e}")
        return False

def test_pyqt():
    """تست PyQt6"""
    print("تست PyQt6...")
    
    try:
        from PyQt6.QtWidgets import QApplication
        app = QApplication([])
        print("✅ PyQt6 GUI")
        app.quit()
        return True
    except Exception as e:
        print(f"❌ PyQt6: {e}")
        return False

def main():
    """تست اصلی"""
    print("🚀 تست سیستم فاکتور فارسی")
    print("=" * 40)
    
    tests = [test_imports, test_database, test_pyqt]
    results = [test() for test in tests]
    
    print("\n" + "=" * 40)
    if all(results):
        print("🎉 همه تست‌ها موفق!")
        print("🚀 python main.py را اجرا کنید")
    else:
        print("❌ برخی تست‌ها ناموفق")
        print("pip install -r requirements.txt")
    
    return all(results)

if __name__ == "__main__":
    success = main()
    input("Enter برای خروج...")
    sys.exit(0 if success else 1)
