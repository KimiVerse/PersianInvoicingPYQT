"""
Persian Invoicing System - Main Application
Enhanced with login system and improved UI
"""

import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                           QMessageBox, QFrame, QSizePolicy)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap, QPalette, QColor, QIcon
from main_window import MainWindow
from services.database_service import DatabaseService
import hashlib

class LoginDialog(QWidget):
    """Enhanced login dialog with Persian support"""
    
    login_successful = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.db_service = DatabaseService()
        self.is_first_run = self.check_first_run()
        self.setup_ui()
        self.setup_styling()
        
    def check_first_run(self):
        """Check if this is the first run (no users exist)"""
        # This is a simplified check - you might want to implement a more robust method
        return not os.path.exists('invoicing.db') or os.path.getsize('invoicing.db') < 1024
        
    def setup_ui(self):
        """Setup the user interface"""
        self.setWindowTitle("ورود به سیستم مدیریت فاکتور فروش")
        self.setFixedSize(400, 500)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(40, 40, 40, 40)
        
        # Header section
        header_frame = QFrame()
        header_layout = QVBoxLayout(header_frame)
        
        # Logo/Title
        title_label = QLabel("سیستم مدیریت فاکتور فروش")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont("Vazirmatn", 18, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #ffffff; margin-bottom: 10px;")
        
        subtitle_label = QLabel("نسخه پیشرفته با قابلیت مدیریت کامل")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setFont(QFont("Vazirmatn", 10))
        subtitle_label.setStyleSheet("color: #cccccc; margin-bottom: 20px;")
        
        header_layout.addWidget(title_label)
        header_layout.addWidget(subtitle_label)
        
        # Form section
        form_frame = QFrame()
        form_layout = QVBoxLayout(form_frame)
        form_layout.setSpacing(15)
        
        # Mode label
        if self.is_first_run:
            mode_label = QLabel("🔐 تنظیم اولیه - ایجاد حساب کاربری")
            mode_label.setStyleSheet("color: #4CAF50; font-weight: bold; margin-bottom: 10px;")
        else:
            mode_label = QLabel("🔑 ورود به سیستم")
            mode_label.setStyleSheet("color: #2196F3; font-weight: bold; margin-bottom: 10px;")
        
        mode_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        form_layout.addWidget(mode_label)
        
        # Username field
        username_label = QLabel("نام کاربری:")
        username_label.setFont(QFont("Vazirmatn", 10))
        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText("نام کاربری خود را وارد کنید")
        self.username_edit.setFont(QFont("Vazirmatn", 11))
        
        # Password field
        password_label = QLabel("رمز عبور:")
        password_label.setFont(QFont("Vazirmatn", 10))
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_edit.setPlaceholderText("رمز عبور خود را وارد کنید")
        self.password_edit.setFont(QFont("Vazirmatn", 11))
        
        # Confirm password (only for first run)
        self.confirm_password_label = QLabel("تکرار رمز عبور:")
        self.confirm_password_label.setFont(QFont("Vazirmatn", 10))
        self.confirm_password_edit = QLineEdit()
        self.confirm_password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_password_edit.setPlaceholderText("رمز عبور را مجدداً وارد کنید")
        self.confirm_password_edit.setFont(QFont("Vazirmatn", 11))
        
        # Add fields to form
        form_layout.addWidget(username_label)
        form_layout.addWidget(self.username_edit)
        form_layout.addWidget(password_label)
        form_layout.addWidget(self.password_edit)
        
        if self.is_first_run:
            form_layout.addWidget(self.confirm_password_label)
            form_layout.addWidget(self.confirm_password_edit)
        else:
            self.confirm_password_label.hide()
            self.confirm_password_edit.hide()
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.login_button = QPushButton("ورود" if not self.is_first_run else "ایجاد حساب")
        self.login_button.setFont(QFont("Vazirmatn", 11, QFont.Weight.Bold))
        self.login_button.clicked.connect(self.handle_login)
        
        self.exit_button = QPushButton("خروج")
        self.exit_button.setFont(QFont("Vazirmatn", 11))
        self.exit_button.clicked.connect(self.close)
        
        button_layout.addWidget(self.exit_button)
        button_layout.addWidget(self.login_button)
        
        # Add sections to main layout
        main_layout.addWidget(header_frame)
        main_layout.addStretch()
        main_layout.addWidget(form_frame)
        main_layout.addStretch()
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)
        
        # Connect Enter key to login
        self.password_edit.returnPressed.connect(self.handle_login)
        if self.is_first_run:
            self.confirm_password_edit.returnPressed.connect(self.handle_login)
        
    def setup_styling(self):
        """Setup modern dark theme styling"""
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1e3c72, stop:1 #2a5298);
                color: #ffffff;
                font-family: 'Vazirmatn', Arial, sans-serif;
            }
            
            QLineEdit {
                background-color: rgba(255, 255, 255, 0.1);
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 8px;
                padding: 12px 15px;
                color: #ffffff;
                font-size: 11pt;
                margin: 5px 0px;
            }
            
            QLineEdit:focus {
                border-color: #4CAF50;
                background-color: rgba(255, 255, 255, 0.15);
            }
            
            QLineEdit::placeholder {
                color: rgba(255, 255, 255, 0.6);
            }
            
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4CAF50, stop:1 #45a049);
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                color: white;
                font-weight: bold;
                font-size: 11pt;
                min-width: 100px;
            }
            
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #45a049, stop:1 #3d8b40);
            }
            
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3d8b40, stop:1 #2e7d32);
            }
            
            QPushButton#exit_button {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #f44336, stop:1 #d32f2f);
            }
            
            QPushButton#exit_button:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #d32f2f, stop:1 #c62828);
            }
            
            QLabel {
                color: #ffffff;
                margin: 5px 0px;
            }
            
            QFrame {
                background: transparent;
            }
        """)
        
        # Set object names for specific styling
        self.exit_button.setObjectName("exit_button")
        
    def handle_login(self):
        """Handle login/registration process"""
        username = self.username_edit.text().strip()
        password = self.password_edit.text()
        
        # Validation
        if not username or not password:
            self.show_message("خطا", "لطفاً نام کاربری و رمز عبور را وارد کنید", QMessageBox.Icon.Warning)
            return
        
        if len(username) < 3:
            self.show_message("خطا", "نام کاربری باید حداقل ۳ کاراکتر باشد", QMessageBox.Icon.Warning)
            return
            
        if len(password) < 4:
            self.show_message("خطا", "رمز عبور باید حداقل ۴ کاراکتر باشد", QMessageBox.Icon.Warning)
            return
        
        if self.is_first_run:
            # Registration mode
            confirm_password = self.confirm_password_edit.text()
            
            if password != confirm_password:
                self.show_message("خطا", "رمز عبور و تکرار آن یکسان نیستند", QMessageBox.Icon.Warning)
                return
            
            success, message = self.db_service.create_user(username, password)
            if success:
                self.show_message("موفقیت", "حساب کاربری با موفقیت ایجاد شد", QMessageBox.Icon.Information)
                self.is_first_run = False
                self.update_ui_for_login_mode()
            else:
                self.show_message("خطا", message, QMessageBox.Icon.Critical)
        else:
            # Login mode
            if self.db_service.authenticate_user(username, password):
                self.login_successful.emit()
                self.close()
            else:
                self.show_message("خطا", "نام کاربری یا رمز عبور اشتباه است", QMessageBox.Icon.Critical)
                self.password_edit.clear()
                self.password_edit.setFocus()
    
    def update_ui_for_login_mode(self):
        """Update UI from registration to login mode"""
        self.confirm_password_label.hide()
        self.confirm_password_edit.hide()
        self.login_button.setText("ورود")
        
        # Update mode label
        mode_label = self.findChild(QLabel)
        if mode_label:
            mode_label.setText("🔑 ورود به سیستم")
            mode_label.setStyleSheet("color: #2196F3; font-weight: bold; margin-bottom: 10px;")
        
        # Clear fields
        self.username_edit.clear()
        self.password_edit.clear()
        self.username_edit.setFocus()
    
    def show_message(self, title, message, icon=QMessageBox.Icon.Information):
        """Show message box with Persian styling"""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(icon)
        
        # Apply dark theme to message box
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #2b2b2b;
                color: #ffffff;
                font-family: 'Vazirmatn';
            }
            QMessageBox QPushButton {
                background-color: #4CAF50;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                color: white;
                font-weight: bold;
                min-width: 60px;
            }
            QMessageBox QPushButton:hover {
                background-color: #45a049;
            }
        """)
        
        msg_box.exec()
    
    def closeEvent(self, event):
        """Handle close event"""
        if not self.is_first_run:
            event.accept()
        else:
            reply = QMessageBox.question(
                self, 
                'تأیید خروج',
                'آیا مطمئن هستید که می‌خواهید خروج کنید؟\nحساب کاربری ایجاد نشده است.',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                event.accept()
            else:
                event.ignore()

class InvoiceApplication(QApplication):
    """Main application class"""
    
    def __init__(self, argv):
        super().__init__(argv)
        self.setup_application()
        self.login_dialog = None
        self.main_window = None
        
    def setup_application(self):
        """Setup application properties"""
        self.setApplicationName("Persian Invoicing System")
        self.setApplicationVersion("2.0")
        self.setOrganizationName("KimiVerse")
        
        # Set application icon if available
        if os.path.exists("assets/icon.png"):
            self.setWindowIcon(QIcon("assets/icon.png"))
        
        # Apply global stylesheet
        self.setStyleSheet("""
            * {
                font-family: 'Vazirmatn', Arial, sans-serif;
            }
        """)
    
    def start(self):
        """Start the application with login"""
        self.login_dialog = LoginDialog()
        self.login_dialog.login_successful.connect(self.show_main_window)
        self.login_dialog.show()
        
        # Center the login dialog
        self.center_widget(self.login_dialog)
        
    def show_main_window(self):
        """Show main window after successful login"""
        try:
            self.main_window = MainWindow()
            self.main_window.show()
            
            # Center the main window
            self.center_widget(self.main_window)
            
        except Exception as e:
            QMessageBox.critical(
                None,
                "خطا",
                f"خطا در بارگذاری برنامه اصلی:\n{str(e)}"
            )
            self.quit()
    
    def center_widget(self, widget):
        """Center widget on screen"""
        screen = self.primaryScreen().geometry()
        widget_rect = widget.frameGeometry()
        center_point = screen.center()
        widget_rect.moveCenter(center_point)
        widget.move(widget_rect.topLeft())

def main():
    """Main function"""
    # Ensure required directories exist
    os.makedirs('logs', exist_ok=True)
    os.makedirs('exports', exist_ok=True)
    os.makedirs('backups', exist_ok=True)
    os.makedirs('assets', exist_ok=True)
    
    # Create and start application
    app = InvoiceApplication(sys.argv)
    app.start()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()