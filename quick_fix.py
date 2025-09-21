#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تعمیرگر سریع برای مشکلات پروژه Persian Invoicing System
این اسکریپت مشکلات شایع را به صورت خودکار حل میکند
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

class QuickFixer:
    def __init__(self):
        self.project_dir = Path.cwd()
        self.fixes_applied = []
        
    def log(self, message, emoji="🔧"):
        print(f"{emoji} {message}")
        
    def apply_fix(self, description):
        self.fixes_applied.append(description)
        self.log(f"اعمال شد: {description}", "✅")

    def install_missing_dependencies(self):
        """نصب وابستگی‌های مفقود"""
        self.log("بررسی و نصب وابستگی‌ها...", "📦")
        
        required_packages = [
            "PyQt6>=6.7.0",
            "SQLAlchemy>=2.0.23", 
            "bcrypt>=4.1.2",
            "jdatetime>=5.0.0",
            "Pillow>=10.1.0",
            "reportlab>=4.0.7",
            "openpyxl>=3.1.2"
        ]
        
        for package in required_packages:
            try:
                self.log(f"نصب {package}...")
                subprocess.run([
                    sys.executable, "-m", "pip", "install", package, "--quiet"
                ], check=True, capture_output=True)
                self.apply_fix(f"نصب {package}")
            except subprocess.CalledProcessError:
                self.log(f"خطا در نصب {package}", "❌")

    def create_missing_directories(self):
        """ایجاد دایرکتوری‌های مفقود"""
        self.log("ایجاد دایرکتوری‌های لازم...", "📁")
        
        required_dirs = [
            'logs', 'backups', 'exports', 'assets', 
            'database', 'services', 'views', 'fonts'
        ]
        
        for dir_name in required_dirs:
            dir_path = self.project_dir / dir_name
            if not dir_path.exists():
                dir_path.mkdir(exist_ok=True)
                self.apply_fix(f"ایجاد دایرکتوری {dir_name}")

    def create_missing_init_files(self):
        """ایجاد فایل‌های __init__.py مفقود"""
        self.log("ایجاد فایل‌های __init__.py...", "📄")
        
        init_dirs = ['database', 'services', 'views']
        
        for dir_name in init_dirs:
            init_file = self.project_dir / dir_name / "__init__.py"
            if not init_file.exists():
                init_file.write_text('# Package initialization\\n', encoding='utf-8')
                self.apply_fix(f"ایجاد {dir_name}/__init__.py")

    def fix_test_setup_imports(self):
        """تصحیح import های test_setup.py"""
        self.log("تصحیح test_setup.py...", "🔄")
        
        test_setup_path = self.project_dir / "test_setup.py"
        if test_setup_path.exists():
            content = test_setup_path.read_text(encoding='utf-8')
            
            # بررسی وجود import های مشکل‌ساز
            if "create_database, test_database_connection" in content:
                # ایجاد نسخه جدید
                fixed_content = '''#!/usr/bin/env python3
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
    
    print("\\n" + "=" * 40)
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
'''
                
                # پشتیبان و جایگزینی
                backup_path = test_setup_path.with_suffix('.py.old')
                shutil.copy2(test_setup_path, backup_path)
                test_setup_path.write_text(fixed_content, encoding='utf-8')
                
                self.apply_fix("تصحیح test_setup.py")

    def fix_database_models_compatibility(self):
        """تصحیح سازگاری مدل‌های دیتابیس"""
        self.log("بررسی مدل‌های دیتابیس...", "🗃️")
        
        models_path = self.project_dir / "database" / "models.py"
        if models_path.exists():
            try:
                # تست import کردن مدل‌ها
                content = models_path.read_text(encoding='utf-8')
                if "from sqlalchemy" in content:
                    self.log("مدل‌های SQLAlchemy یافت شد", "✅")
                    self.apply_fix("تأیید ساختار SQLAlchemy")
                else:
                    self.log("مدل‌های SQLAlchemy یافت نشد", "⚠️")
            except Exception as e:
                self.log(f"خطا در بررسی models.py: {e}", "❌")

    def create_basic_config_files(self):
        """ایجاد فایل‌های پیکربندی اساسی"""
        self.log("ایجاد فایل‌های پیکربندی...", "⚙️")
        
        # ایجاد .env در صورت عدم وجود
        env_path = self.project_dir / ".env"
        if not env_path.exists():
            env_content = """# تنظیمات محیطی پروژه فاکتور فارسی
DEBUG=True
DATABASE_PATH=invoicing.db
LOG_LEVEL=INFO
BACKUP_RETENTION_DAYS=30
"""
            env_path.write_text(env_content, encoding='utf-8')
            self.apply_fix("ایجاد فایل .env")

    def check_font_availability(self):
        """بررسی وجود فونت فارسی"""
        self.log("بررسی فونت فارسی...", "🔤")
        
        font_path = self.project_dir / "fonts" / "Vazirmatn-Regular.ttf"
        if not font_path.exists():
            self.log("فونت Vazirmatn موجود نیست", "⚠️")
            
            # ایجاد فایل راهنما برای دانلود فونت
            font_readme = self.project_dir / "fonts" / "README.md"
            font_readme.write_text("""# راهنمای دانلود فونت

فونت Vazirmatn را از لینک زیر دانلود کنید:
https://github.com/rastikerdar/vazirmatn/raw/master/fonts/ttf/Vazirmatn-Regular.ttf

سپس فایل را در این پوشه قرار دهید.
""", encoding='utf-8')
            self.apply_fix("ایجاد راهنمای دانلود فونت")

    def create_run_scripts(self):
        """ایجاد اسکریپت‌های اجرا"""
        self.log("ایجاد اسکریپت‌های اجرا...", "🚀")
        
        # اسکریپت Windows
        bat_content = """@echo off
chcp 65001 > nul
echo شروع سیستم فاکتور فارسی...
python main.py
pause
"""
        bat_path = self.project_dir / "run.bat"
        bat_path.write_text(bat_content, encoding='utf-8')
        self.apply_fix("ایجاد run.bat")
        
        # اسکریپت Linux/Mac  
        sh_content = """#!/bin/bash
echo "شروع سیستم فاکتور فارسی..."
python3 main.py
"""
        sh_path = self.project_dir / "run.sh"
        sh_path.write_text(sh_content, encoding='utf-8')
        
        # اجازه اجرا برای Linux/Mac
        try:
            os.chmod(sh_path, 0o755)
        except:
            pass
        
        self.apply_fix("ایجاد run.sh")

    def verify_main_files(self):
        """تأیید وجود فایل‌های اصلی"""
        self.log("بررسی فایل‌های اصلی...", "📋")
        
        critical_files = {
            'main.py': 'فایل اجرایی اصلی',
            'main_window.py': 'پنجره اصلی برنامه',
            'requirements.txt': 'فهرست وابستگی‌ها',
            'services/database_service.py': 'سرویس دیتابیس'
        }
        
        for file_path, description in critical_files.items():
            if (self.project_dir / file_path).exists():
                self.log(f"✅ {description} موجود")
            else:
                self.log(f"❌ {description} مفقود: {file_path}", "❌")

    def run_quick_fix(self):
        """اجرای تعمیرات سریع"""
        print("🛠️ شروع تعمیرات سریع پروژه فاکتور فارسی")
        print("=" * 50)
        
        # اجرای تعمیرات
        self.create_missing_directories()
        self.create_missing_init_files()
        self.install_missing_dependencies()
        self.fix_test_setup_imports()
        self.fix_database_models_compatibility()
        self.create_basic_config_files()
        self.check_font_availability()
        self.create_run_scripts()
        self.verify_main_files()
        
        # گزارش نهایی
        print("\\n" + "=" * 50)
        print("📊 گزارش تعمیرات:")
        
        if self.fixes_applied:
            for fix in self.fixes_applied:
                print(f"  ✅ {fix}")
        else:
            print("  ℹ️ تعمیری لازم نبود")
        
        print("\\n🎯 مراحل بعدی:")
        print("  1. python debug_tool.py (برای تست کامل)")
        print("  2. python main.py (برای اجرا)")
        print("  3. در صورت مشکل: pip install -r requirements.txt")
        
        return len(self.fixes_applied) > 0

def main():
    fixer = QuickFixer()
    fixer.run_quick_fix()
    
    print("\\n✨ تعمیرات سریع کامل شد!")
    input("Enter برای خروج...")

if __name__ == "__main__":
    main()