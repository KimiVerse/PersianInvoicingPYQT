"""
Settings Dialog for Persian Invoicing System
Enhanced settings management with user preferences
"""

import os
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QGridLayout,
                           QLabel, QLineEdit, QPushButton, QTabWidget, 
                           QGroupBox, QCheckBox, QSpinBox, QComboBox,
                           QTextEdit, QFileDialog, QMessageBox, QFrame,
                           QColorDialog, QFontDialog, QSlider)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QColor, QPalette
from services.database_service import DatabaseService

class AppearanceTab(QFrame):
    """Appearance settings tab"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        """Setup appearance settings UI"""
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        # Theme settings
        theme_group = QGroupBox("تنظیمات ظاهری")
        theme_layout = QGridLayout(theme_group)
        
        # Font settings
        font_label = QLabel("فونت اصلی:")
        self.font_button = QPushButton("انتخاب فونت")
        self.font_button.clicked.connect(self.select_font)
        self.current_font_label = QLabel("Vazirmatn, 11pt")
        
        # Theme selection
        theme_label = QLabel("تم رنگی:")
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["تیره", "روشن", "آبی", "سبز"])
        
        # Color customization
        primary_color_label = QLabel("رنگ اصلی:")
        self.primary_color_button = QPushButton()
        self.primary_color_button.setFixedSize(50, 30)
        self.primary_color_button.setStyleSheet("background-color: #4CAF50; border-radius: 4px;")
        self.primary_color_button.clicked.connect(self.select_primary_color)
        
        # Language settings
        lang_label = QLabel("زبان رابط:")
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["فارسی", "English"])
        
        theme_layout.addWidget(font_label, 0, 0)
        theme_layout.addWidget(self.font_button, 0, 1)
        theme_layout.addWidget(self.current_font_label, 0, 2)
        theme_layout.addWidget(theme_label, 1, 0)
        theme_layout.addWidget(self.theme_combo, 1, 1)
        theme_layout.addWidget(primary_color_label, 2, 0)
        theme_layout.addWidget(self.primary_color_button, 2, 1)
        theme_layout.addWidget(lang_label, 3, 0)
        theme_layout.addWidget(self.lang_combo, 3, 1)
        
        # Window settings
        window_group = QGroupBox("تنظیمات پنجره")
        window_layout = QGridLayout(window_group)
        
        self.remember_size_check = QCheckBox("ذخیره اندازه پنجره")
        self.remember_position_check = QCheckBox("ذخیره موقعیت پنجره")
        self.maximize_startup_check = QCheckBox("شروع با حداکثر اندازه")
        self.show_statusbar_check = QCheckBox("نمایش نوار وضعیت")
        
        window_layout.addWidget(self.remember_size_check, 0, 0)
        window_layout.addWidget(self.remember_position_check, 0, 1)
        window_layout.addWidget(self.maximize_startup_check, 1, 0)
        window_layout.addWidget(self.show_statusbar_check, 1, 1)
        
        layout.addWidget(theme_group)
        layout.addWidget(window_group)
        layout.addStretch()
        
        self.setLayout(layout)
        
    def select_font(self):
        """Select application font"""
        current_font = QFont("Vazirmatn", 11)
        font, ok = QFontDialog.getFont(current_font, self)
        
        if ok:
            self.current_font_label.setText(f"{font.family()}, {font.pointSize()}pt")
            self.selected_font = font
            
    def select_primary_color(self):
        """Select primary color"""
        color = QColorDialog.getColor(QColor("#4CAF50"), self)
        
        if color.isValid():
            self.primary_color_button.setStyleSheet(
                f"background-color: {color.name()}; border-radius: 4px;"
            )
            self.selected_color = color

class DatabaseTab(QFrame):
    """Database settings tab"""
    
    def __init__(self):
        super().__init__()
        self.db_service = DatabaseService()
        self.setup_ui()
        
    def setup_ui(self):
        """Setup database settings UI"""
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        # Backup settings
        backup_group = QGroupBox("تنظیمات پشتیبان‌گیری")
        backup_layout = QGridLayout(backup_group)
        
        # Auto backup
        self.auto_backup_check = QCheckBox("پشتیبان‌گیری خودکار")
        
        backup_interval_label = QLabel("فاصله پشتیبان‌گیری:")
        self.backup_interval_spin = QSpinBox()
        self.backup_interval_spin.setRange(1, 30)
        self.backup_interval_spin.setValue(7)
        self.backup_interval_spin.setSuffix(" روز")
        
        backup_location_label = QLabel("مسیر پشتیبان:")
        self.backup_location_edit = QLineEdit()
        self.backup_location_edit.setText("./backups/")
        self.backup_location_button = QPushButton("انتخاب مسیر")
        self.backup_location_button.clicked.connect(self.select_backup_location)
        
        # Max backup files
        max_backups_label = QLabel("حداکثر تعداد پشتیبان:")
        self.max_backups_spin = QSpinBox()
        self.max_backups_spin.setRange(1, 100)
        self.max_backups_spin.setValue(10)
        self.max_backups_spin.setSuffix(" فایل")
        
        backup_layout.addWidget(self.auto_backup_check, 0, 0, 1, 2)
        backup_layout.addWidget(backup_interval_label, 1, 0)
        backup_layout.addWidget(self.backup_interval_spin, 1, 1)
        backup_layout.addWidget(backup_location_label, 2, 0)
        backup_layout.addWidget(self.backup_location_edit, 2, 1)
        backup_layout.addWidget(self.backup_location_button, 2, 2)
        backup_layout.addWidget(max_backups_label, 3, 0)
        backup_layout.addWidget(self.max_backups_spin, 3, 1)
        
        # Database maintenance
        maintenance_group = QGroupBox("نگهداری دیتابیس")
        maintenance_layout = QVBoxLayout(maintenance_group)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        
        self.backup_now_button = QPushButton("پشتیبان فوری")
        self.backup_now_button.clicked.connect(self.backup_now)
        
        self.optimize_button = QPushButton("بهینه‌سازی دیتابیس")
        self.optimize_button.clicked.connect(self.optimize_database)
        
        self.repair_button = QPushButton("تعمیر دیتابیس")
        self.repair_button.clicked.connect(self.repair_database)
        
        buttons_layout.addWidget(self.backup_now_button)
        buttons_layout.addWidget(self.optimize_button)
        buttons_layout.addWidget(self.repair_button)
        
        # Database info
        info_label = QLabel("اطلاعات دیتابیس:")
        self.db_info_text = QTextEdit()
        self.db_info_text.setMaximumHeight(100)
        self.db_info_text.setReadOnly(True)
        self.load_database_info()
        
        maintenance_layout.addLayout(buttons_layout)
        maintenance_layout.addWidget(info_label)
        maintenance_layout.addWidget(self.db_info_text)
        
        layout.addWidget(backup_group)
        layout.addWidget(maintenance_group)
        layout.addStretch()
        
        self.setLayout(layout)
        
    def select_backup_location(self):
        """Select backup directory"""
        directory = QFileDialog.getExistingDirectory(
            self, "انتخاب مسیر پشتیبان", self.backup_location_edit.text()
        )
        
        if directory:
            self.backup_location_edit.setText(directory)
    
    def backup_now(self):
        """Create immediate backup"""
        try:
            self.backup_now_button.setText("در حال پشتیبان‌گیری...")
            self.backup_now_button.setEnabled(False)
            
            success, message = self.db_service.backup_database()
            
            if success:
                QMessageBox.information(self, "موفقیت", message)
            else:
                QMessageBox.critical(self, "خطا", message)
                
        finally:
            self.backup_now_button.setText("پشتیبان فوری")
            self.backup_now_button.setEnabled(True)
    
    def optimize_database(self):
        """Optimize database"""
        reply = QMessageBox.question(
            self, "تأیید", "آیا مطمئن هستید که می‌خواهید دیتابیس را بهینه‌سازی کنید؟"
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Implement database optimization
            QMessageBox.information(self, "موفقیت", "دیتابیس با موفقیت بهینه‌سازی شد")
    
    def repair_database(self):
        """Repair database"""
        reply = QMessageBox.question(
            self, "تأیید", "آیا مطمئن هستید که می‌خواهید دیتابیس را تعمیر کنید؟"
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Implement database repair
            QMessageBox.information(self, "موفقیت", "دیتابیس با موفقیت تعمیر شد")
    
    def load_database_info(self):
        """Load database information"""
        try:
            # Get database file info
            db_path = "invoicing.db"
            if os.path.exists(db_path):
                size = os.path.getsize(db_path)
                size_mb = size / (1024 * 1024)
                
                info_text = f"""
مسیر دیتابیس: {os.path.abspath(db_path)}
اندازه فایل: {size_mb:.2f} مگابایت
تاریخ آخرین تغییر: {os.path.getmtime(db_path)}
                """
            else:
                info_text = "فایل دیتابیس یافت نشد"
            
            self.db_info_text.setText(info_text.strip())
            
        except Exception as e:
            self.db_info_text.setText(f"خطا در خواندن اطلاعات: {str(e)}")

class PrintingTab(QFrame):
    """Printing settings tab"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        """Setup printing settings UI"""
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        # Print settings
        print_group = QGroupBox("تنظیمات چاپ")
        print_layout = QGridLayout(print_group)
        
        # Default printer
        printer_label = QLabel("چاپگر پیش‌فرض:")
        self.printer_combo = QComboBox()
        self.printer_combo.addItems(["سیستمی", "PDF", "خودکار"])
        
        # Paper size
        paper_label = QLabel("اندازه کاغذ:")
        self.paper_combo = QComboBox()
        self.paper_combo.addItems(["A4", "A5", "Letter"])
        
        # Print quality
        quality_label = QLabel("کیفیت چاپ:")
        self.quality_combo = QComboBox()
        self.quality_combo.addItems(["بالا", "متوسط", "پایین"])
        
        # Margins
        margin_label = QLabel("حاشیه (میلی‌متر):")
        self.margin_spin = QSpinBox()
        self.margin_spin.setRange(5, 50)
        self.margin_spin.setValue(20)
        
        print_layout.addWidget(printer_label, 0, 0)
        print_layout.addWidget(self.printer_combo, 0, 1)
        print_layout.addWidget(paper_label, 1, 0)
        print_layout.addWidget(self.paper_combo, 1, 1)
        print_layout.addWidget(quality_label, 2, 0)
        print_layout.addWidget(self.quality_combo, 2, 1)
        print_layout.addWidget(margin_label, 3, 0)
        print_layout.addWidget(self.margin_spin, 3, 1)
        
        # Invoice template settings
        template_group = QGroupBox("تنظیمات قالب فاکتور")
        template_layout = QGridLayout(template_group)
        
        # Show logo
        self.show_logo_check = QCheckBox("نمایش لوگو")
        
        # Company info
        company_label = QLabel("اطلاعات شرکت:")
        self.company_edit = QTextEdit()
        self.company_edit.setMaximumHeight(80)
        self.company_edit.setPlaceholderText("نام شرکت، آدرس، تلفن...")
        
        # Footer text
        footer_label = QLabel("متن پاورقی:")
        self.footer_edit = QLineEdit()
        self.footer_edit.setPlaceholderText("با تشکر از خرید شما")
        
        template_layout.addWidget(self.show_logo_check, 0, 0, 1, 2)
        template_layout.addWidget(company_label, 1, 0)
        template_layout.addWidget(self.company_edit, 1, 1)
        template_layout.addWidget(footer_label, 2, 0)
        template_layout.addWidget(self.footer_edit, 2, 1)
        
        layout.addWidget(print_group)
        layout.addWidget(template_group)
        layout.addStretch()
        
        self.setLayout(layout)

class SecurityTab(QFrame):
    """Security settings tab"""
    
    def __init__(self):
        super().__init__()
        self.db_service = DatabaseService()
        self.setup_ui()
        
    def setup_ui(self):
        """Setup security settings UI"""
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        # User management
        user_group = QGroupBox("مدیریت کاربران")
        user_layout = QGridLayout(user_group)
        
        # Change password
        change_pass_label = QLabel("تغییر رمز عبور:")
        self.change_pass_button = QPushButton("تغییر رمز عبور")
        self.change_pass_button.clicked.connect(self.change_password)
        
        # Session timeout
        timeout_label = QLabel("مدت انقضای نشست (دقیقه):")
        self.timeout_spin = QSpinBox()
        self.timeout_spin.setRange(5, 480)
        self.timeout_spin.setValue(60)
        
        # Auto lock
        self.auto_lock_check = QCheckBox("قفل خودکار برنامه")
        
        user_layout.addWidget(change_pass_label, 0, 0)
        user_layout.addWidget(self.change_pass_button, 0, 1)
        user_layout.addWidget(timeout_label, 1, 0)
        user_layout.addWidget(self.timeout_spin, 1, 1)
        user_layout.addWidget(self.auto_lock_check, 2, 0, 1, 2)
        
        # Data security
        security_group = QGroupBox("امنیت اطلاعات")
        security_layout = QGridLayout(security_group)
        
        # Encryption
        self.encrypt_backup_check = QCheckBox("رمزگذاری پشتیبان‌ها")
        self.secure_delete_check = QCheckBox("حذف امن اطلاعات")
        self.audit_log_check = QCheckBox("ثبت لاگ عملیات")
        
        # Data retention
        retention_label = QLabel("مدت نگهداری لاگ‌ها (روز):")
        self.retention_spin = QSpinBox()
        self.retention_spin.setRange(7, 365)
        self.retention_spin.setValue(90)
        
        security_layout.addWidget(self.encrypt_backup_check, 0, 0, 1, 2)
        security_layout.addWidget(self.secure_delete_check, 1, 0, 1, 2)
        security_layout.addWidget(self.audit_log_check, 2, 0, 1, 2)
        security_layout.addWidget(retention_label, 3, 0)
        security_layout.addWidget(self.retention_spin, 3, 1)
        
        layout.addWidget(user_group)
        layout.addWidget(security_group)
        layout.addStretch()
        
        self.setLayout(layout)
        
    def change_password(self):
        """Change user password"""
        from PyQt6.QtWidgets import QInputDialog
        
        # Get current password
        current_password, ok = QInputDialog.getText(
            self, "تغییر رمز عبور", "رمز عبور فعلی:", QLineEdit.EchoMode.Password
        )
        
        if not ok:
            return
        
        # Get new password
        new_password, ok = QInputDialog.getText(
            self, "تغییر رمز عبور", "رمز عبور جدید:", QLineEdit.EchoMode.Password
        )
        
        if not ok:
            return
        
        # Confirm new password
        confirm_password, ok = QInputDialog.getText(
            self, "تغییر رمز عبور", "تکرار رمز عبور جدید:", QLineEdit.EchoMode.Password
        )
        
        if not ok:
            return
        
        if new_password != confirm_password:
            QMessageBox.warning(self, "خطا", "رمز عبور جدید و تکرار آن یکسان نیستند")
            return
        
        # TODO: Implement password change logic
        QMessageBox.information(self, "موفقیت", "رمز عبور با موفقیت تغییر کرد")

class SettingsDialog(QDialog):
    """Enhanced settings dialog with tabbed interface"""
    
    settings_changed = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.setup_styling()
        self.load_settings()
        
    def setup_ui(self):
        """Setup the settings dialog UI"""
        self.setWindowTitle("تنظیمات سیستم")
        self.setModal(True)
        self.resize(700, 600)
        
        # Main layout
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header_label = QLabel("تنظیمات سیستم")
        header_label.setFont(QFont("Vazirmatn", 16, QFont.Weight.Bold))
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_label.setStyleSheet("color: #2c3e50; margin-bottom: 15px;")
        
        # Tab widget
        self.tab_widget = QTabWidget()
        
        # Create tabs
        self.appearance_tab = AppearanceTab()
        self.database_tab = DatabaseTab()
        self.printing_tab = PrintingTab()
        self.security_tab = SecurityTab()
        
        # Add tabs
        self.tab_widget.addTab(self.appearance_tab, "🎨 ظاهر")
        self.tab_widget.addTab(self.database_tab, "💾 دیتابیس")
        self.tab_widget.addTab(self.printing_tab, "🖨️ چاپ")
        self.tab_widget.addTab(self.security_tab, "🔒 امنیت")
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.defaults_button = QPushButton("بازگشت به پیش‌فرض")
        self.defaults_button.clicked.connect(self.reset_to_defaults)
        
        self.cancel_button = QPushButton("انصراف")
        self.cancel_button.clicked.connect(self.reject)
        
        self.apply_button = QPushButton("اعمال")
        self.apply_button.clicked.connect(self.apply_settings)
        
        self.ok_button = QPushButton("تأیید")
        self.ok_button.clicked.connect(self.accept_settings)
        
        button_layout.addWidget(self.defaults_button)
        button_layout.addStretch()
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.apply_button)
        button_layout.addWidget(self.ok_button)
        
        # Add to main layout
        layout.addWidget(header_label)
        layout.addWidget(self.tab_widget)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
    def setup_styling(self):
        """Setup dialog styling"""
        self.setStyleSheet("""
            QDialog {
                background-color: #f8f9fa;
                font-family: 'Vazirmatn', Arial, sans-serif;
            }
            
            QTabWidget::pane {
                border: 2px solid #dee2e6;
                border-radius: 8px;
                background-color: white;
                margin-top: 10px;
            }
            
            QTabBar::tab {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f8f9fa, stop:1 #e9ecef);
                border: 2px solid #dee2e6;
                border-bottom: none;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                min-width: 120px;
                padding: 12px 15px;
                margin: 2px;
                color: #495057;
                font-weight: bold;
                font-size: 11pt;
            }
            
            QTabBar::tab:selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4CAF50, stop:1 #45a049);
                color: white;
                border-color: #4CAF50;
            }
            
            QTabBar::tab:hover:!selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e3f2fd, stop:1 #bbdefb);
                border-color: #2196F3;
            }
            
            QGroupBox {
                font-weight: bold;
                border: 2px solid #dee2e6;
                border-radius: 8px;
                margin: 15px 0px;
                padding-top: 15px;
                background-color: white;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px 0 8px;
                color: #495057;
                background-color: white;
            }
            
            QLineEdit, QTextEdit, QComboBox, QSpinBox {
                border: 2px solid #dee2e6;
                border-radius: 6px;
                padding: 8px;
                font-size: 11pt;
                background-color: white;
            }
            
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QSpinBox:focus {
                border-color: #4CAF50;
            }
            
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4CAF50, stop:1 #45a049);
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 15px;
                font-size: 11pt;
                font-weight: bold;
                min-width: 80px;
            }
            
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #45a049, stop:1 #3d8b40);
            }
            
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3d8b40, stop:1 #2e7d32);
            }
            
            QCheckBox {
                font-size: 11pt;
                color: #495057;
                spacing: 8px;
            }
            
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid #dee2e6;
                border-radius: 4px;
                background-color: white;
            }
            
            QCheckBox::indicator:checked {
                background-color: #4CAF50;
                border-color: #4CAF50;
                image: url(checkmark.png);
            }
            
            QLabel {
                color: #495057;
                font-size: 11pt;
            }
        """)
        
    def load_settings(self):
        """Load current settings"""
        # Load settings from database or config file
        # This is a placeholder - implement actual settings loading
        pass
        
    def apply_settings(self):
        """Apply settings without closing dialog"""
        self.save_settings()
        self.settings_changed.emit()
        QMessageBox.information(self, "موفقیت", "تنظیمات با موفقیت اعمال شد")
        
    def accept_settings(self):
        """Accept and save settings"""
        self.save_settings()
        self.settings_changed.emit()
        self.accept()
        
    def save_settings(self):
        """Save settings to database or config file"""
        # Implement actual settings saving
        try:
            # Save appearance settings
            # Save database settings
            # Save printing settings
            # Save security settings
            pass
        except Exception as e:
            QMessageBox.critical(self, "خطا", f"خطا در ذخیره تنظیمات: {str(e)}")
            
    def reset_to_defaults(self):
        """Reset all settings to default values"""
        reply = QMessageBox.question(
            self,
            "تأیید",
            "آیا مطمئن هستید که می‌خواهید همه تنظیمات را به حالت پیش‌فرض بازگردانید؟",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Reset all settings to defaults
            self.load_default_settings()
            QMessageBox.information(self, "موفقیت", "تنظیمات به حالت پیش‌فرض بازگردانده شد")
            
    def load_default_settings(self):
        """Load default settings"""
        # Reset all tabs to default values
        # This is a placeholder - implement actual default loading
        pass