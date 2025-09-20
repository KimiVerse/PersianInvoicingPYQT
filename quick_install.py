"""
Quick installation script for Persian Invoicing System
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    
    requirements = [
        "PyQt6>=6.6.0",
        "SQLAlchemy>=2.0.0", 
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
    directories = ["logs", "backups", "exports"]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created directory: {directory}/")
    
    return True

def main():
    """Main installation function"""
    print("🚀 Persian Invoicing System - Quick Install")
    print("=" * 50)
    
    # Install requirements
    if not install_requirements():
        print("❌ Installation failed!")
        return False
    
    # Create directories
    if not create_directories():
        print("❌ Directory creation failed!")
        return False
    
    # Test the setup
    print("\n🧪 Testing setup...")
    try:
        from test_setup import main as test_main
        if test_main():
            print("\n🎉 Installation completed successfully!")
            print("🚀 Run 'python main.py' to start the application")
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