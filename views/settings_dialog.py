# Settings and Configuration Dialog
# File: views/settings_dialog.py

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QGridLayout,
                            QLabel, QFrame, QPushButton, QLineEdit, QTabWidget,
                            QMessageBox, QComboBox, QSpinBox, QCheckBox,
                            QTextEdit, QFileDialog, QGroupBox, QFormLayout)
from PyQt6.QtCore import Qt, QSettings, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap
import json
import os
from pathlib import Path

class CompanyInfoTab(QWidget):
    """Company information settings tab"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.load_settings()
    
    def setup_ui(self):
        """Setup company info UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Company Info Group
        company_group = QGroupBox("اطلاعات شرکت")
        company_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 16px;
                border: 2px solid #6B7280;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top right;
                padding: 0 10px;
                background: #374151;
                color: #F9FAFB;
            }
        """)
        
        company_layout = QFormLayout(company_group)
        company_layout.setSpacing(15)
        
        self.company_name = QLineEdit()
        self.company_name.setPlaceholderText("نام شرکت یا کسب‌وکار")
        
        self.company_description = QLineEdit()
        self.company_description.setPlaceholderText("توضیح کوتاه درباره شرکت")
        
        self.company_address = QTextEdit()
        self.company_address.setPlaceholderText("آدرس کامل شرکت")
        self.company_address.setMaximumHeight(80)
        
        self.company_phone = QLineEdit()
        self.company_phone.setPlaceholderText("شماره تلفن")
        
        self.company_email = QLineEdit()
        self.company_email.setPlaceholderText("آدرس ایمیل")
        
        self.company_website = QLineEdit()
        self.company_website.setPlaceholderText("آدرس وب‌سایت")
        
        self.economic_code = QLineEdit()
        self.economic_code.setPlaceholderText("کد اقتصادی")
        
        self.registration_number = QLineEdit()
        self.registration_number.setPlaceholderText("شماره ثبت")
        
        company_layout.addRow("نام شرکت:", self.company_name)
        company_layout.addRow("توضیحات:", self.company_description)
        company_layout.addRow("آدرس:", self.company_address)
        company_layout.addRow("تلفن:", self.company_phone)
        company_layout.addRow("ایمیل:", self.company_email)
        company_layout.addRow("وب‌سایت:", self.company_website)
        company_layout.addRow("کد اقتصادی:", self.economic_code)
        company_layout.addRow("شماره ثبت:", self.registration_number)
        
        layout.addWidget(company_group)
        layout.addStretch()
    
    def load_settings(self):
        """Load company settings"""
        settings = QSettings()
        self.company_name.setText(settings.value("company/name", "شرکت نمونه تجارت پارس"))
        self.company_description.setText(settings.value("company/description", "متخصص در ارائه بهترین محصولات و خدمات"))
        self.company_address.setText(settings.value("company/address", "تهران، خیابان ولیعصر، پلاک ۱۲۳"))
        self.company_phone.setText(settings.value("company/phone", "۰۲۱-۱۲۳۴۵۶۷۸"))
        self.company_email.setText(settings.value("company/email", "info@company.com"))
        self.company_website.setText(settings.value("company/website", "www.company.com"))
        self.economic_code.setText(settings.value("company/economic_code", "۱۲۳۴۵۶۷۸۹۰"))
        self.registration_number.setText(settings.value("company/registration", "۱۲۳۴۵۶"))
    
    def save_settings(self):
        """Save company settings"""
        settings = QSettings()
        settings.setValue("company/name", self.company_name.text())
        settings.setValue("company/description", self.company_description.text())
        settings.setValue("company/address", self.company_address.toPlainText())
        settings.setValue("company/phone", self.company_phone.text())
        settings.setValue("company/email", self.company_email.text())
        settings.setValue("company/website", self.company_website.text())
        settings.setValue("company/economic_code", self.economic_code.text())
        settings.setValue("company/registration", self.registration_number.text())

class AppearanceTab(QWidget):
    """Application appearance settings tab"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.load_settings()
    
    def setup_ui(self):
        """Setup appearance UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Theme Group
        theme_group = QGroupBox("تنظیمات ظاهری")
        theme_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 16px;
                border: 2px solid #6B7280;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top right;
                padding: 0 10px;
                background: #374151;
                color: #F9FAFB;
            }
        """)
        
        theme_layout = QFormLayout(theme_group)
        theme_layout.setSpacing(15)
        
        # Theme selection
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["تیره (پیش‌فرض)", "روشن", "آبی", "سبز"])
        
        # Font size
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(10, 20)
        self.font_size_spin.setValue(14)
        self.font_size_spin.setSuffix(" پیکسل")
        
        # Auto refresh
        self.auto_refresh = QCheckBox("بروزرسانی خودکار داشبورد")
        self.auto_refresh.setChecked(True)
        
        # Refresh interval
        self.refresh_interval = QSpinBox()
        self.refresh_interval.setRange(1, 60)
        self.refresh_interval.setValue(5)
        self.refresh_interval.setSuffix(" دقیقه")
        
        # Show tooltips
        self.show_tooltips = QCheckBox("نمایش راهنمای ابزارها")
        self.show_tooltips.setChecked(True)
        
        # Animations
        self.enable_animations = QCheckBox("فعال‌سازی انیمیشن‌ها")
        self.enable_animations.setChecked(True)
        
        theme_layout.addRow("قالب رنگی:", self.theme_combo)
        theme_layout.addRow("اندازه فونت:", self.font_size_spin)
        theme_layout.addRow("", self.auto_refresh)
        theme_layout.addRow("فاصله بروزرسانی:", self.refresh_interval)
        theme_layout.addRow("", self.show_tooltips)
        theme_layout.addRow("", self.enable_animations)
        
        layout.addWidget(theme_group)
        layout.addStretch()
    
    def load_settings(self):
        """Load appearance settings"""
        settings = QSettings()
        theme_index = settings.value("appearance/theme", 0, type=int)
        self.theme_combo.setCurrentIndex(theme_index)
        
        font_size = settings.value("appearance/font_size", 14, type=int)
        self.font_size_spin.setValue(font_size)
        
        auto_refresh = settings.value("appearance/auto_refresh", True, type=bool)
        self.auto_refresh.setChecked(auto_refresh)
        
        refresh_interval = settings.value("appearance/refresh_interval", 5, type=int)
        self.refresh_interval.setValue(refresh_interval)
        
        show_tooltips = settings.value("appearance/show_tooltips", True, type=bool)
        self.show_tooltips.setChecked(show_tooltips)
        
        enable_animations = settings.value("appearance/enable_animations", True, type=bool)
        self.enable_animations.setChecked(enable_animations)
    
    def save_settings(self):
        """Save appearance settings"""
        settings = QSettings()
        settings.setValue("appearance/theme", self.theme_combo.currentIndex())
        settings.setValue("appearance/font_size", self.font_size_spin.value())
        settings.setValue("appearance/auto_refresh", self.auto_refresh.isChecked())
        settings.setValue("appearance/refresh_interval", self.refresh_interval.value())
        settings.setValue("appearance/show_tooltips", self.show_tooltips.isChecked())
        settings.setValue("appearance/enable_animations", self.enable_animations.isChecked())

class DatabaseTab(QWidget):
    """Database settings and backup tab"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.load_settings()
    
    def setup_ui(self):
        """Setup database UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Database Group
        db_group = QGroupBox("تنظیمات پایگاه داده")
        db_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 16px;
                border: 2px solid #6B7280;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top right;
                padding: 0 10px;
                background: #374151;
                color: #F9FAFB;
            }
        """)
        
        db_layout = QVBoxLayout(db_group)
        db_layout.setSpacing(15)
        
        # Database location
        location_layout = QHBoxLayout()
        location_label = QLabel("مسیر پایگاه داده:")
        self.db_location = QLineEdit()
        self.db_location.setReadOnly(True)
        browse_button = QPushButton("انتخاب مسیر")
        browse_button.clicked.connect(self.browse_database_location)
        
        location_layout.addWidget(self.db_location)
        location_layout.addWidget(browse_button)
        
        # Auto backup
        self.auto_backup = QCheckBox("پشتیبان‌گیری خودکار")
        self.auto_backup.setChecked(True)
        
        # Backup interval
        backup_interval_layout = QHBoxLayout()
        backup_interval_label = QLabel("فاصله پشتیبان‌گیری:")
        self.backup_interval = QSpinBox()
        self.backup_interval.setRange(1, 30)
        self.backup_interval.setValue(7)
        self.backup_interval.setSuffix(" روز")
        
        backup_interval_layout.addWidget(backup_interval_label)
        backup_interval_layout.addWidget(self.backup_interval)
        backup_interval_layout.addStretch()
        
        # Backup buttons
        backup_buttons_layout = QHBoxLayout()
        
        backup_now_button = QPushButton("🔄 پشتیبان‌گیری همین حالا")
        backup_now_button.setStyleSheet("""
            QPushButton {
                background: #10B981;
                color: white;
                font-weight: bold;
                border-radius: 8px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background: #059669;
            }
        """)
        backup_now_button.clicked.connect(self.backup_database)
        
        restore_button = QPushButton("📁 بازیابی پشتیبان")
        restore_button.setStyleSheet("""
            QPushButton {
                background: #3B82F6;
                color: white;
                font-weight: bold;
                border-radius: 8px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background: #2563EB;
            }
        """)
        restore_button.clicked.connect(self.restore_database)
        
        backup_buttons_layout.addWidget(backup_now_button)
        backup_buttons_layout.addWidget(restore_button)
        backup_buttons_layout.addStretch()
        
        db_layout.addWidget(location_label)
        db_layout.addLayout(location_layout)
        db_layout.addWidget(self.auto_backup)
        db_layout.addLayout(backup_interval_layout)
        db_layout.addLayout(backup_buttons_layout)
        
        layout.addWidget(db_group)
        layout.addStretch()
    
    def load_settings(self):
        """Load database settings"""
        settings = QSettings()
        db_location = settings.value("database/location", "invoicing.db")
        self.db_location.setText(db_location)
        
        auto_backup = settings.value("database/auto_backup", True, type=bool)
        self.auto_backup.setChecked(auto_backup)
        
        backup_interval = settings.value("database/backup_interval", 7, type=int)
        self.backup_interval.setValue(backup_interval)
    
    def save_settings(self):
        """Save database settings"""
        settings = QSettings()
        settings.setValue("database/location", self.db_location.text())
        settings.setValue("database/auto_backup", self.auto_backup.isChecked())
        settings.setValue("database/backup_interval", self.backup_interval.value())
    
    def browse_database_location(self):
        """Browse for database location"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "انتخاب مسیر پایگاه داده", "invoicing.db", "Database Files (*.db)"
        )
        if file_path:
            self.db_location.setText(file_path)
    
    def backup_database(self):
        """Create database backup"""
        try:
            import shutil
            from datetime import datetime
            
            source = self.db_location.text()
            if not os.path.exists(source):
                QMessageBox.warning(self, "خطا", "فایل پایگاه داده یافت نشد.")
                return
            
            backup_dir = "backups"
            os.makedirs(backup_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"invoicing_backup_{timestamp}.db"
            backup_path = os.path.join(backup_dir, backup_name)
            
            shutil.copy2(source, backup_path)
            
            QMessageBox.information(
                self, "موفقیت", 
                f"پشتیبان‌گیری با موفقیت انجام شد.\nمسیر: {backup_path}"
            )
            
        except Exception as e:
            QMessageBox.critical(self, "خطا", f"خطا در پشتیبان‌گیری: {str(e)}")
    
    def restore_database(self):
        """Restore database from backup"""
        try:
            backup_file, _ = QFileDialog.getOpenFileName(
                self, "انتخاب فایل پشتیبان", "backups", "Database Files (*.db)"
            )
            
            if not backup_file:
                return
            
            reply = QMessageBox.question(
                self, "تأیید بازیابی",
                "آیا از بازیابی پایگاه داده اطمینان دارید؟\nاطلاعات فعلی حذف خواهد شد.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                import shutil
                shutil.copy2(backup_file, self.db_location.text())
                
                QMessageBox.information(
                    self, "موفقیت", 
                    "پایگاه داده با موفقیت بازیابی شد.\nلطفاً برنامه را مجدداً راه‌اندازی کنید."
                )
                
        except Exception as e:
            QMessageBox.critical(self, "خطا", f"خطا در بازیابی: {str(e)}")

class SettingsDialog(QDialog):
    """Main settings dialog"""
    
    settings_changed = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("تنظیمات")
        self.setFixedSize(600, 500)
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.setup_ui()
        self.apply_styles()
    
    def setup_ui(self):
        """Setup settings dialog UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Tab widget
        self.tab_widget = QTabWidget()
        
        # Add tabs
        self.company_tab = CompanyInfoTab()
        self.appearance_tab = AppearanceTab()
        self.database_tab = DatabaseTab()
        
        self.tab_widget.addTab(self.company_tab, "🏢 اطلاعات شرکت")
        self.tab_widget.addTab(self.appearance_tab, "🎨 ظاهر")
        self.tab_widget.addTab(self.database_tab, "💾 پایگاه داده")
        
        # Buttons
        buttons_frame = QFrame()
        buttons_layout = QHBoxLayout(buttons_frame)
        buttons_layout.setContentsMargins(20, 15, 20, 15)
        
        save_button = QPushButton("💾 ذخیره")
        save_button.setFixedHeight(40)
        save_button.clicked.connect(self.save_all_settings)
        
        cancel_button = QPushButton("❌ انصراف")
        cancel_button.setFixedHeight(40)
        cancel_button.clicked.connect(self.reject)
        
        reset_button = QPushButton("🔄 بازنشانی")
        reset_button.setFixedHeight(40)
        reset_button.clicked.connect(self.reset_settings)
        
        buttons_layout.addWidget(reset_button)
        buttons_layout.addStretch()
        buttons_layout.addWidget(cancel_button)
        buttons_layout.addWidget(save_button)
        
        layout.addWidget(self.tab_widget, 1)
        layout.addWidget(buttons_frame)
    
    def apply_styles(self):
        """Apply styles to the dialog"""
        self.setStyleSheet("""
            QDialog {
                background: #1F2937;
                color: #F9FAFB;
            }
            
            QTabWidget {
                background: transparent;
                border: none;
            }
            
            QTabWidget::pane {
                border: 1px solid #374151;
                background: #1F2937;
                border-radius: 8px;
                margin-top: 5px;
            }
            
            QTabBar::tab {
                background: #374151;
                color: #F9FAFB;
                padding: 12px 20px;
                margin: 2px;
                border-radius: 8px 8px 0px 0px;
                font-size: 14px;
                font-weight: bold;
                min-width: 120px;
            }
            
            QTabBar::tab:selected {
                background: #3B82F6;
                color: white;
            }
            
            QTabBar::tab:hover {
                background: #4B5563;
            }
            
            QPushButton {
                background: #3B82F6;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
            }
            
            QPushButton:hover {
                background: #2563EB;
            }
            
            QLineEdit, QTextEdit, QSpinBox, QComboBox {
                background: #374151;
                border: 2px solid #6B7280;
                border-radius: 6px;
                padding: 8px;
                color: #F9FAFB;
                font-size: 14px;
            }
            
            QLineEdit:focus, QTextEdit:focus, QSpinBox:focus, QComboBox:focus {
                border-color: #3B82F6;
            }
            
            QCheckBox {
                color: #F9FAFB;
                font-size: 14px;
                spacing: 8px;
            }
            
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border-radius: 3px;
                border: 2px solid #6B7280;
                background: #374151;
            }
            
            QCheckBox::indicator:checked {
                background: #3B82F6;
                border-color: #3B82F6;
            }
            
            QLabel {
                color: #F9FAFB;
                font-size: 14px;
            }
        """)
    
    def save_all_settings(self):
        """Save all settings"""
        try:
            self.company_tab.save_settings()
            self.appearance_tab.save_settings()
            self.database_tab.save_settings()
            
            QMessageBox.information(self, "موفقیت", "تنظیمات با موفقیت ذخیره شد.")
            self.settings_changed.emit()
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(self, "خطا", f"خطا در ذخیره تنظیمات: {str(e)}")
    
    def reset_settings(self):
        """Reset all settings to default"""
        reply = QMessageBox.question(
            self, "تأیید بازنشانی",
            "آیا از بازنشانی همه تنظیمات اطمینان دارید؟",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            settings = QSettings()
            settings.clear()
            
            # Reload default values
            self.company_tab.load_settings()
            self.appearance_tab.load_settings()
            self.database_tab.load_settings()
            
            QMessageBox.information(self, "موفقیت", "تنظیمات به حالت پیش‌فرض بازنشانی شد.")