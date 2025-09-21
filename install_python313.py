#!/usr/bin/env python3
"""
Python 3.13 Compatible Installation Script
نصب سازگار با Python 3.13
"""

import subprocess
import sys
import os
from pathlib import Path

def install_requirements():
    """نصب وابستگی‌ها با نسخه‌های سازگار"""
    
    print("🔧 نصب وابستگی‌ها برای Python 3.13...")
    
    # لیست پکیج‌های سازگار با Python 3.13
    packages = [
        "PyQt6>=6.8.0",
        "SQLAlchemy>=2.0.25", 
        "bcrypt>=4.2.0",
        "jdatetime>=5.0.0",
        "Pillow>=10.4.0",
        "reportlab>=4.2.0",
        "fpdf2>=2.8.0",
        "openpyxl>=3.1.5",
        "pandas>=2.2.0",
        "matplotlib>=3.9.0",
        "numpy>=1.26.0"
    ]
    
    # نصب یکی یکی پکیج‌ها
    for package in packages:
        print(f"📦 نصب {package}...")
        try:
            subprocess.run([
                sys.executable, "-m", "pip", "install", package
            ], check=True, capture_output=True)
            print(f"✅ {package} نصب شد")
        except subprocess.CalledProcessError as e:
            print(f"⚠️ خطا در نصب {package}: {e}")
            
            # برای Pillow، سعی کن از wheel از قبل build شده استفاده کنی
            if "Pillow" in package:
                print("🔄 سعی در نصب Pillow از wheel...")
                try:
                    subprocess.run([
                        sys.executable, "-m", "pip", "install", 
                        "--only-binary=all", "Pillow"
                    ], check=True, capture_output=True)
                    print("✅ Pillow از wheel نصب شد")
                except:
                    print("❌ نصب Pillow ناموفق - ادامه بدون آن...")
                    
    print("✅ نصب وابستگی‌ها تکمیل شد!")

def create_directories():
    """ایجاد پوشه‌های مورد نیاز"""
    print("📁 ایجاد پوشه‌ها...")
    
    directories = [
        "assets", "backups", "exports", "logs", 
        "fonts", "database", "services", "views"
    ]
    
    for dir_name in directories:
        Path(dir_name).mkdir(exist_ok=True)
    
    print("✅ پوشه‌ها ایجاد شدند")

def fix_imports():
    """اصلاح مشکلات import"""
    print("🔧 اصلاح مشکلات import...")
    
    # اصلاح main_window.py
    main_window_path = Path("main_window.py")
    if main_window_path.exists():
        content = main_window_path.read_text(encoding='utf-8')
        
        # حذف QActionGroup از import (چون در PyQt6 در QtGui است)
        content = content.replace(
            "QSizePolicy, QToolBar, QActionGroup)",
            "QSizePolicy, QToolBar)"
        )
        
        main_window_path.write_text(content, encoding='utf-8')
        print("✅ main_window.py اصلاح شد")

def test_installation():
    """تست نصب"""
    print("🧪 تست نصب...")
    
    try:
        # تست PyQt6
        import PyQt6.QtWidgets
        print("✅ PyQt6 کار می‌کند")
        
        # تست SQLAlchemy
        import sqlalchemy
        print("✅ SQLAlchemy کار می‌کند")
        
        # تست jdatetime
        import jdatetime
        print("✅ jdatetime کار می‌کند")
        
        print("🎉 تست‌ها موفق بودند!")
        return True
        
    except ImportError as e:
        print(f"❌ خطا در تست: {e}")
        return False

def main():
    """تابع اصلی"""
    print("""
╔══════════════════════════════════════════════════════════╗
║           نصب سازگار با Python 3.13                      ║
║              Persian Invoicing System                    ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    # بررسی نسخه Python
    if sys.version_info < (3, 8):
        print("❌ نسخه Python 3.8+ مورد نیاز است")
        return False
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    
    # مراحل نصب
    steps = [
        ("اصلاح مشکلات import", fix_imports),
        ("ایجاد پوشه‌ها", create_directories), 
        ("نصب وابستگی‌ها", install_requirements),
        ("تست نصب", test_installation)
    ]
    
    for step_name, step_func in steps:
        print(f"\n🔄 {step_name}...")
        try:
            if not step_func():
                print(f"❌ خطا در {step_name}")
                response = input("ادامه؟ (y/n): ")
                if response.lower() not in ['y', 'yes']:
                    return False
        except Exception as e:
            print(f"❌ خطا: {e}")
            response = input("ادامه؟ (y/n): ")
            if response.lower() not in ['y', 'yes']:
                return False
    
    print("""
🎉 نصب تکمیل شد!

نحوه اجرا:
    python main.py

اطلاعات ورود:
    نام کاربری: admin
    رمز عبور: admin123
    """)
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)