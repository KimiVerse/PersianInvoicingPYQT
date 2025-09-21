#!/usr/bin/env python3
"""
Quick Installation Script for Persian Invoicing System
Automated setup and dependency installation
"""

import os
import sys
import subprocess
import platform
import urllib.request
import zipfile
from pathlib import Path

class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

class PersianInvoiceInstaller:
    """Automated installer for Persian Invoicing System"""
    
    def __init__(self):
        self.system = platform.system()
        self.python_version = sys.version_info
        self.project_dir = Path(__file__).parent.absolute()
        self.venv_dir = self.project_dir / "venv"
        
    def print_header(self):
        """Print installation header"""
        header = f"""
{Colors.CYAN}{'='*60}{Colors.END}
{Colors.BOLD}{Colors.PURPLE}    سیستم مدیریت فاکتور فروش - نصب خودکار{Colors.END}
{Colors.CYAN}{'='*60}{Colors.END}

{Colors.BLUE}نسخه:{Colors.END} 2.0
{Colors.BLUE}سازنده:{Colors.END} KimiVerse
{Colors.BLUE}سیستم عامل:{Colors.END} {self.system}
{Colors.BLUE}نسخه پایتون:{Colors.END} {self.python_version.major}.{self.python_version.minor}.{self.python_version.micro}

{Colors.CYAN}{'='*60}{Colors.END}
        """
        print(header)
    
    def check_python_version(self):
        """Check if Python version is compatible"""
        print(f"{Colors.YELLOW}🔍 بررسی نسخه پایتون...{Colors.END}")
        
        if self.python_version < (3, 8):
            print(f"{Colors.RED}❌ خطا: نسخه پایتون 3.8 یا بالاتر مورد نیاز است{Colors.END}")
            print(f"{Colors.RED}   نسخه فعلی: {self.python_version.major}.{self.python_version.minor}.{self.python_version.micro}{Colors.END}")
            return False
        
        print(f"{Colors.GREEN}✅ نسخه پایتون مناسب است{Colors.END}")
        return True
    
    def check_pip(self):
        """Check if pip is available"""
        print(f"{Colors.YELLOW}🔍 بررسی pip...{Colors.END}")
        
        try:
            subprocess.run([sys.executable, "-m", "pip", "--version"], 
                         check=True, capture_output=True)
            print(f"{Colors.GREEN}✅ pip موجود است{Colors.END}")
            return True
        except subprocess.CalledProcessError:
            print(f"{Colors.RED}❌ pip یافت نشد{Colors.END}")
            return False
    
    def create_virtual_environment(self):
        """Create Python virtual environment"""
        print(f"{Colors.YELLOW}🏗️ ایجاد محیط مجازی...{Colors.END}")
        
        if self.venv_dir.exists():
            print(f"{Colors.BLUE}📁 محیط مجازی از قبل موجود است{Colors.END}")
            return True
        
        try:
            subprocess.run([sys.executable, "-m", "venv", str(self.venv_dir)], 
                         check=True)
            print(f"{Colors.GREEN}✅ محیط مجازی ایجاد شد{Colors.END}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"{Colors.RED}❌ خطا در ایجاد محیط مجازی: {e}{Colors.END}")
            return False
    
    def get_pip_executable(self):
        """Get pip executable path for virtual environment"""
        if self.system == "Windows":
            return self.venv_dir / "Scripts" / "pip.exe"
        else:
            return self.venv_dir / "bin" / "pip"
    
    def get_python_executable(self):
        """Get Python executable path for virtual environment"""
        if self.system == "Windows":
            return self.venv_dir / "Scripts" / "python.exe"
        else:
            return self.venv_dir / "bin" / "python"
    
    def upgrade_pip(self):
        """Upgrade pip to latest version"""
        print(f"{Colors.YELLOW}⬆️ به‌روزرسانی pip...{Colors.END}")
        
        pip_exe = self.get_pip_executable()
        
        try:
            subprocess.run([str(pip_exe), "install", "--upgrade", "pip"], 
                         check=True)
            print(f"{Colors.GREEN}✅ pip به‌روزرسانی شد{Colors.END}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"{Colors.YELLOW}⚠️ خطا در به‌روزرسانی pip: {e}{Colors.END}")
            return False
    
    def install_dependencies(self):
        """Install project dependencies"""
        print(f"{Colors.YELLOW}📦 نصب وابستگی‌ها...{Colors.END}")
        
        requirements_file = self.project_dir / "requirements.txt"
        pip_exe = self.get_pip_executable()
        
        if not requirements_file.exists():
            print(f"{Colors.RED}❌ فایل requirements.txt یافت نشد{Colors.END}")
            return False
        
        try:
            print(f"{Colors.BLUE}📋 در حال خواندن فایل requirements.txt...{Colors.END}")
            
            # Install dependencies with progress
            result = subprocess.run([
                str(pip_exe), "install", "-r", str(requirements_file),
                "--progress-bar", "on"
            ], check=True, capture_output=False)
            
            print(f"{Colors.GREEN}✅ تمام وابستگی‌ها نصب شدند{Colors.END}")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"{Colors.RED}❌ خطا در نصب وابستگی‌ها: {e}{Colors.END}")
            return False
    
    def download_font(self):
        """Download Vazirmatn font if not exists"""
        print(f"{Colors.YELLOW}🔤 بررسی فونت فارسی...{Colors.END}")
        
        fonts_dir = self.project_dir / "fonts"
        font_file = fonts_dir / "Vazirmatn-Regular.ttf"
        
        fonts_dir.mkdir(exist_ok=True)
        
        if font_file.exists():
            print(f"{Colors.GREEN}✅ فونت فارسی موجود است{Colors.END}")
            return True
        
        print(f"{Colors.YELLOW}⬇️ دانلود فونت فارسی...{Colors.END}")
        
        font_url = "https://github.com/rastikerdar/vazirmatn/raw/master/fonts/ttf/Vazirmatn-Regular.ttf"
        
        try:
            urllib.request.urlretrieve(font_url, str(font_file))
            print(f"{Colors.GREEN}✅ فونت فارسی دانلود شد{Colors.END}")
            return True
        except Exception as e:
            print(f"{Colors.YELLOW}⚠️ خطا در دانلود فونت: {e}{Colors.END}")
            print(f"{Colors.BLUE}💡 فونت را به صورت دستی در پوشه fonts قرار دهید{Colors.END}")
            return False
    
    def create_directories(self):
        """Create necessary directories"""
        print(f"{Colors.YELLOW}📁 ایجاد پوشه‌های مورد نیاز...{Colors.END}")
        
        directories = [
            "assets", "backups", "exports", "logs", 
            "fonts", "database", "services", "views"
        ]
        
        for dir_name in directories:
            dir_path = self.project_dir / dir_name
            dir_path.mkdir(exist_ok=True)
        
        print(f"{Colors.GREEN}✅ پوشه‌ها ایجاد شدند{Colors.END}")
        return True
    
    def create_database(self):
        """Initialize database"""
        print(f"{Colors.YELLOW}🗄️ ایجاد دیتابیس...{Colors.END}")
        
        python_exe = self.get_python_executable()
        
        # Create a simple database initialization script
        init_script = '''
import sys
sys.path.insert(0, ".")
from services.database_service import DatabaseService

try:
    db = DatabaseService()
    print("Database initialized successfully")
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
'''
        
        try:
            result = subprocess.run([
                str(python_exe), "-c", init_script
            ], check=True, capture_output=True, text=True, cwd=str(self.project_dir))
            
            print(f"{Colors.GREEN}✅ دیتابیس ایجاد شد{Colors.END}")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"{Colors.YELLOW}⚠️ خطا در ایجاد دیتابیس: {e.stderr}{Colors.END}")
            return False
    
    def create_run_script(self):
        """Create run script for easy execution"""
        print(f"{Colors.YELLOW}📝 ایجاد اسکریپت اجرا...{Colors.END}")
        
        if self.system == "Windows":
            script_name = "run.bat"
            script_content = f'''@echo off
cd /d "{self.project_dir}"
"{self.get_python_executable()}" main.py
pause
'''
        else:
            script_name = "run.sh"
            script_content = f'''#!/bin/bash
cd "{self.project_dir}"
"{self.get_python_executable()}" main.py
'''
        
        script_path = self.project_dir / script_name
        
        try:
            with open(script_path, 'w', encoding='utf-8') as f:
                f.write(script_content)
            
            if self.system != "Windows":
                script_path.chmod(0o755)
            
            print(f"{Colors.GREEN}✅ اسکریپت اجرا ایجاد شد: {script_name}{Colors.END}")
            return True
            
        except Exception as e:
            print(f"{Colors.YELLOW}⚠️ خطا در ایجاد اسکریپت: {e}{Colors.END}")
            return False
    
    def create_desktop_shortcut(self):
        """Create desktop shortcut (Windows only)"""
        if self.system != "Windows":
            return True
        
        print(f"{Colors.YELLOW}🖥️ ایجاد میانبر دسکتاپ...{Colors.END}")
        
        try:
            import winshell
            from win32com.client import Dispatch
            
            desktop = winshell.desktop()
            shortcut_path = os.path.join(desktop, "Persian Invoice System.lnk")
            
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.Targetpath = str(self.get_python_executable())
            shortcut.Arguments = "main.py"
            shortcut.WorkingDirectory = str(self.project_dir)
            shortcut.IconLocation = str(self.project_dir / "assets" / "icon.ico")
            shortcut.save()
            
            print(f"{Colors.GREEN}✅ میانبر دسکتاپ ایجاد شد{Colors.END}")
            return True
            
        except ImportError:
            print(f"{Colors.BLUE}💡 برای ایجاد میانبر، پکیج pywin32 نصب کنید{Colors.END}")
            return False
        except Exception as e:
            print(f"{Colors.YELLOW}⚠️ خطا در ایجاد میانبر: {e}{Colors.END}")
            return False
    
    def test_installation(self):
        """Test if installation works"""
        print(f"{Colors.YELLOW}🧪 تست نصب...{Colors.END}")
        
        python_exe = self.get_python_executable()
        
        test_script = '''
import sys
sys.path.insert(0, ".")

try:
    from PyQt6.QtWidgets import QApplication
    from services.database_service import DatabaseService
    
    # Test Qt
    app = QApplication([])
    
    # Test database
    db = DatabaseService()
    
    print("Installation test passed!")
    
except Exception as e:
    print(f"Installation test failed: {e}")
    sys.exit(1)
'''
        
        try:
            result = subprocess.run([
                str(python_exe), "-c", test_script
            ], check=True, capture_output=True, text=True, cwd=str(self.project_dir))
            
            print(f"{Colors.GREEN}✅ تست نصب موفق بود{Colors.END}")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"{Colors.RED}❌ تست نصب ناموفق: {e.stderr}{Colors.END}")
            return False
    
    def print_completion_message(self):
        """Print installation completion message"""
        python_exe = self.get_python_executable()
        
        message = f"""
{Colors.GREEN}{'='*60}{Colors.END}
{Colors.BOLD}{Colors.GREEN}🎉 نصب با موفقیت تکمیل شد! 🎉{Colors.END}
{Colors.GREEN}{'='*60}{Colors.END}

{Colors.BOLD}نحوه اجرا:{Colors.END}

{Colors.BLUE}1. اجرای مستقیم:{Colors.END}
   cd "{self.project_dir}"
   "{python_exe}" main.py

{Colors.BLUE}2. استفاده از اسکریپت اجرا:{Colors.END}
   {"run.bat" if self.system == "Windows" else "./run.sh"}

{Colors.BOLD}اطلاعات ورود پیش‌فرض:{Colors.END}
   نام کاربری: admin
   رمز عبور: admin123

{Colors.BOLD}ویژگی‌های سیستم:{Colors.END}
   ✅ صدور فاکتور با پس‌زمینه دلخواه
   ✅ مدیریت کالاها با کنترل موجودی
   ✅ خروجی PDF و تصویر
   ✅ گزارش‌گیری پیشرفته
   ✅ تاریخ شمسی
   ✅ رابط کاربری فارسی

{Colors.PURPLE}برای راهنمایی بیشتر، فایل README.md را مطالعه کنید.{Colors.END}

{Colors.GREEN}{'='*60}{Colors.END}
        """
        print(message)
    
    def run_installation(self):
        """Run complete installation process"""
        self.print_header()
        
        steps = [
            ("بررسی نسخه پایتون", self.check_python_version),
            ("بررسی pip", self.check_pip),
            ("ایجاد محیط مجازی", self.create_virtual_environment),
            ("به‌روزرسانی pip", self.upgrade_pip),
            ("نصب وابستگی‌ها", self.install_dependencies),
            ("دانلود فونت فارسی", self.download_font),
            ("ایجاد پوشه‌ها", self.create_directories),
            ("ایجاد دیتابیس", self.create_database),
            ("ایجاد اسکریپت اجرا", self.create_run_script),
            ("ایجاد میانبر دسکتاپ", self.create_desktop_shortcut),
            ("تست نصب", self.test_installation)
        ]
        
        failed_steps = []
        
        for step_name, step_function in steps:
            print(f"\n{Colors.CYAN}🔄 {step_name}...{Colors.END}")
            
            if not step_function():
                failed_steps.append(step_name)
                print(f"{Colors.RED}❌ خطا در {step_name}{Colors.END}")
                
                # Ask user if they want to continue
                try:
                    response = input(f"{Colors.YELLOW}آیا می‌خواهید ادامه دهید؟ (y/n): {Colors.END}")
                    if response.lower() not in ['y', 'yes', 'بله']:
                        print(f"{Colors.RED}نصب متوقف شد.{Colors.END}")
                        return False
                except KeyboardInterrupt:
                    print(f"\n{Colors.RED}نصب لغو شد.{Colors.END}")
                    return False
        
        if failed_steps:
            print(f"\n{Colors.YELLOW}⚠️ مراحل ناموفق: {', '.join(failed_steps)}{Colors.END}")
            print(f"{Colors.BLUE}💡 ممکن است برنامه به درستی کار نکند.{Colors.END}")
        
        self.print_completion_message()
        return True

def main():
    """Main installation function"""
    try:
        installer = PersianInvoiceInstaller()
        success = installer.run_installation()
        
        if success:
            print(f"\n{Colors.GREEN}✨ نصب کامل شد! ✨{Colors.END}")
            return 0
        else:
            print(f"\n{Colors.RED}💥 نصب ناموفق بود! 💥{Colors.END}")
            return 1
            
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}⚠️ نصب توسط کاربر لغو شد.{Colors.END}")
        return 1
    except Exception as e:
        print(f"\n{Colors.RED}❌ خطای غیرمنتظره: {e}{Colors.END}")
        return 1

if __name__ == "__main__":
    sys.exit(main())