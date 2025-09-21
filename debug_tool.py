#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ابزار دیباگ پروژه Persian Invoicing System
این ابزار مشکلات اصلی پروژه را شناسایی و حل میکند
"""

import os
import sys
import traceback
import subprocess
from pathlib import Path

class PersianDebugger:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.fixes = []
        self.project_dir = Path.cwd()
        
    def log_error(self, message):
        self.errors.append(f"❌ {message}")
        print(f"❌ {message}")
        
    def log_warning(self, message):
        self.warnings.append(f"⚠️ {message}")
        print(f"⚠️ {message}")
        
    def log_success(self, message):
        print(f"✅ {message}")
        
    def log_fix(self, message):
        self.fixes.append(f"🔧 {message}")
        print(f"🔧 {message}")

    def check_python_version(self):
        """بررسی نسخه پایتون"""
        print("\n🐍 بررسی نسخه پایتون...")
        if sys.version_info < (3, 8):
            self.log_error(f"نسخه پایتون شما {sys.version} است. حداقل نسخه 3.8 نیاز است.")
            return False
        else:
            self.log_success(f"نسخه پایتون {sys.version.split()[0]} مناسب است")
            return True

    def check_required_files(self):
        """بررسی وجود فایل‌های ضروری"""
        print("\n📁 بررسی فایل‌های ضروری...")
        
        required_files = [
            'main.py',
            'main_window.py',
            'requirements.txt',
            'database/models.py',
            'services/database_service.py'
        ]
        
        missing_files = []
        for file_path in required_files:
            if not (self.project_dir / file_path).exists():
                missing_files.append(file_path)
                self.log_error(f"فایل مفقود: {file_path}")
            else:
                self.log_success(f"فایل موجود: {file_path}")
        
        if missing_files:
            self.log_fix("فایل‌های مفقود را از گیتهاب دانلود کنید")
            return False
        
        return True

    def check_dependencies(self):
        """بررسی وابستگی‌های پروژه"""
        print("\n📦 بررسی وابستگی‌ها...")
        
        try:
            import PyQt6
            self.log_success("PyQt6 نصب شده است")
        except ImportError:
            self.log_error("PyQt6 نصب نیست")
            self.log_fix("pip install PyQt6")
            return False
            
        try:
            import sqlalchemy
            self.log_success("SQLAlchemy نصب شده است")
        except ImportError:
            self.log_error("SQLAlchemy نصب نیست")
            self.log_fix("pip install SQLAlchemy")
            return False
            
        try:
            import bcrypt
            self.log_success("bcrypt نصب شده است")
        except ImportError:
            self.log_warning("bcrypt نصب نیست - برای رمزگذاری لازم است")
            self.log_fix("pip install bcrypt")
            
        try:
            import jdatetime
            self.log_success("jdatetime نصب شده است")
        except ImportError:
            self.log_warning("jdatetime نصب نیست - برای تاریخ شمسی لازم است")
            self.log_fix("pip install jdatetime")
            
        return True

    def check_database_imports(self):
        """بررسی import های دیتابیس"""
        print("\n🗃️ بررسی import های دیتابیس...")
        
        try:
            # تست import کردن مدل‌های SQLAlchemy
            from database.models import Base, Product, Invoice, User
            self.log_success("مدل‌های SQLAlchemy با موفقیت import شدند")
            return True
        except ImportError as e:
            self.log_error(f"خطا در import مدل‌های دیتابیس: {e}")
            return False
        except Exception as e:
            self.log_error(f"خطای ناشناخته در مدل‌های دیتابیس: {e}")
            return False

    def check_services_imports(self):
        """بررسی import های سرویس‌ها"""
        print("\n🔧 بررسی import های سرویس‌ها...")
        
        try:
            from services.database_service import DatabaseService
            self.log_success("DatabaseService با موفقیت import شد")
            return True
        except ImportError as e:
            self.log_error(f"خطا در import DatabaseService: {e}")
            return False
        except Exception as e:
            self.log_error(f"خطای ناشناخته در DatabaseService: {e}")
            return False

    def check_views_imports(self):
        """بررسی import های view ها"""
        print("\n🖼️ بررسی import های view ها...")
        
        views_to_check = [
            'views.dashboard_view',
            'views.invoice_view', 
            'views.products_view',
            'views.reports_view'
        ]
        
        for view_module in views_to_check:
            try:
                __import__(view_module)
                self.log_success(f"{view_module} با موفقیت import شد")
            except ImportError as e:
                self.log_error(f"خطا در import {view_module}: {e}")
                return False
            except Exception as e:
                self.log_warning(f"خطای احتمالی در {view_module}: {e}")
        
        return True

    def test_database_creation(self):
        """تست ایجاد دیتابیس"""
        print("\n🗄️ تست ایجاد دیتابیس...")
        
        try:
            from services.database_service import DatabaseService
            
            # حذف دیتابیس قدیمی برای تست
            test_db = "test_debug.db"
            if os.path.exists(test_db):
                os.remove(test_db)
            
            # ایجاد سرویس دیتابیس
            db_service = DatabaseService(db_path=test_db)
            self.log_success("دیتابیس تست با موفقیت ایجاد شد")
            
            # تنظیف
            db_service.close()
            if os.path.exists(test_db):
                os.remove(test_db)
                
            return True
            
        except Exception as e:
            self.log_error(f"خطا در ایجاد دیتابیس: {e}")
            self.log_error(f"جزئیات خطا: {traceback.format_exc()}")
            return False

    def check_font_file(self):
        """بررسی وجود فونت فارسی"""
        print("\n🔤 بررسی فونت فارسی...")
        
        font_path = self.project_dir / "fonts" / "Vazirmatn-Regular.ttf"
        if font_path.exists():
            self.log_success("فونت Vazirmatn موجود است")
            return True
        else:
            self.log_warning("فونت Vazirmatn موجود نیست")
            self.log_fix("فونت را از گیتهاب دانلود کنید یا از quick_install.py استفاده کنید")
            return False

    def check_directories(self):
        """بررسی و ایجاد دایرکتوری‌های لازم"""
        print("\n📂 بررسی دایرکتوری‌ها...")
        
        required_dirs = ['logs', 'backups', 'exports', 'assets']
        
        for dir_name in required_dirs:
            dir_path = self.project_dir / dir_name
            if not dir_path.exists():
                try:
                    dir_path.mkdir(exist_ok=True)
                    self.log_fix(f"دایرکتوری {dir_name} ایجاد شد")
                except Exception as e:
                    self.log_error(f"خطا در ایجاد دایرکتوری {dir_name}: {e}")
            else:
                self.log_success(f"دایرکتوری {dir_name} موجود است")

    def test_main_window_import(self):
        """تست import کردن پنجره اصلی"""
        print("\n🪟 تست import پنجره اصلی...")
        
        try:
            from main_window import MainWindow
            self.log_success("MainWindow با موفقیت import شد")
            return True
        except ImportError as e:
            self.log_error(f"خطا در import MainWindow: {e}")
            return False
        except Exception as e:
            self.log_error(f"خطای ناشناخته در MainWindow: {e}")
            return False

    def fix_test_setup_conflict(self):
        """حل تداخل test_setup.py"""
        print("\n🔄 حل تداخل test_setup.py...")
        
        test_setup_path = self.project_dir / "test_setup.py"
        if test_setup_path.exists():
            # خواندن محتوای فایل
            with open(test_setup_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # بررسی وجود import های مشکل‌ساز
            if "from database.models import (create_database, test_database_connection" in content:
                self.log_warning("test_setup.py از رویکرد غیر SQLAlchemy استفاده میکند")
                
                # ایجاد نسخه جدید سازگار با SQLAlchemy
                new_test_content = self.create_compatible_test_setup()
                
                # پشتیبان از فایل قدیمی
                backup_path = test_setup_path.with_suffix('.py.backup')
                os.rename(test_setup_path, backup_path)
                
                # نوشتن فایل جدید
                with open(test_setup_path, 'w', encoding='utf-8') as f:
                    f.write(new_test_content)
                
                self.log_fix("test_setup.py به نسخه سازگار با SQLAlchemy تبدیل شد")
                self.log_fix(f"فایل قدیمی در {backup_path} پشتیبان شد")
                
                return True
        
        return False

    def create_compatible_test_setup(self):
        """ایجاد محتوای سازگار برای test_setup.py"""
        return '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تست راه‌اندازی سیستم فاکتور فارسی - نسخه سازگار با SQLAlchemy
"""

import sys
import traceback
import os

def test_imports():
    """تست import های اساسی"""
    print("🔍 تست import ها...")
    
    try:
        import PyQt6
        print("✅ PyQt6 نصب شده")
    except ImportError as e:
        print(f"❌ PyQt6 نصب نیست: {e}")
        return False
    
    try:
        import sqlalchemy
        print("✅ SQLAlchemy نصب شده")
    except ImportError as e:
        print(f"❌ SQLAlchemy نصب نیست: {e}")
        return False
    
    try:
        import jdatetime
        print("✅ jdatetime نصب شده")
    except ImportError as e:
        print(f"⚠️ jdatetime نصب نیست: {e}")
    
    return True

def test_database():
    """تست دیتابیس SQLAlchemy"""
    print("\\n🗃️ تست دیتابیس...")
    
    try:
        from services.database_service import DatabaseService
        
        # ایجاد دیتابیس تست
        test_db = "test_debug.db"
        if os.path.exists(test_db):
            os.remove(test_db)
        
        db_service = DatabaseService(db_path=test_db)
        print("✅ دیتابیس ایجاد شد")
        
        # تنظیف
        db_service.close()
        if os.path.exists(test_db):
            os.remove(test_db)
        
        return True
        
    except Exception as e:
        print(f"❌ خطا در تست دیتابیس: {e}")
        return False

def test_pyqt():
    """تست PyQt6"""
    print("\\n🖼️ تست PyQt6...")
    
    try:
        from PyQt6.QtWidgets import QApplication, QWidget
        from PyQt6.QtCore import Qt
        
        app = QApplication([])
        widget = QWidget()
        widget.setWindowTitle("تست فارسی")
        
        print("✅ PyQt6 کار میکند")
        app.quit()
        return True
        
    except Exception as e:
        print(f"❌ خطا در PyQt6: {e}")
        return False

def main():
    """تست اصلی"""
    print("🚀 تست راه‌اندازی سیستم فاکتور فارسی")
    print("=" * 50)
    
    all_passed = True
    
    if not test_imports():
        all_passed = False
    
    if not test_database():
        all_passed = False
    
    if not test_pyqt():
        all_passed = False
    
    print("\\n" + "=" * 50)
    if all_passed:
        print("🎉 تمام تست‌ها موفق بود!")
        print("🚀 میتوانید python main.py را اجرا کنید")
    else:
        print("❌ برخی تست‌ها شکست خوردند")
        print("💡 pip install -r requirements.txt را اجرا کنید")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    input("\\nEnter برای خروج...")
    sys.exit(0 if success else 1)
'''

    def generate_full_report(self):
        """تولید گزارش کامل مشکلات"""
        print("\n" + "="*60)
        print("📋 گزارش کامل دیباگ")
        print("="*60)
        
        if self.errors:
            print("\n❌ خطاهای یافت شده:")
            for error in self.errors:
                print(f"  {error}")
        
        if self.warnings:
            print("\n⚠️ هشدارها:")
            for warning in self.warnings:
                print(f"  {warning}")
        
        if self.fixes:
            print("\n🔧 راه‌حل‌های پیشنهادی:")
            for fix in self.fixes:
                print(f"  {fix}")
        
        print("\n📞 اگر مشکل برطرف نشد:")
        print("  - GitHub Issues: https://github.com/KimiVerse/PersianInvoicingPYQT/issues")
        print("  - ایمیل: support@kimivi.com")

    def run_full_debug(self):
        """اجرای کامل فرآیند دیباگ"""
        print("🔍 شروع دیباگ کامل پروژه فارسی...")
        print("="*60)
        
        # تست‌های اساسی
        self.check_python_version()
        self.check_required_files()
        self.check_directories()
        self.check_font_file()
        
        # تست وابستگی‌ها
        self.check_dependencies()
        
        # تست import ها
        self.check_database_imports()
        self.check_services_imports()
        self.check_views_imports()
        self.test_main_window_import()
        
        # تست عملکرد
        self.test_database_creation()
        
        # حل مشکلات شناخته شده
        self.fix_test_setup_conflict()
        
        # گزارش نهایی
        self.generate_full_report()
        
        return len(self.errors) == 0

def main():
    debugger = PersianDebugger()
    success = debugger.run_full_debug()
    
    if success:
        print("\n🎉 پروژه آماده اجراست!")
        print("🚀 python main.py را اجرا کنید")
    else:
        print("\n❌ لطفاً مشکلات را حل کنید")
    
    return success

if __name__ == "__main__":
    main()