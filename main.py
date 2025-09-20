# Enhanced Main Window with Menu Bar and About Dialog
# File: main_enhanced.py

import sys
import os
from pathlib import Path
from PyQt6.QtWidgets import (QApplication, QMainWindow, QTabWidget, 
                            QVBoxLayout, QHBoxLayout, QWidget, QLabel,
                            QFrame, QPushButton, QMessageBox, QMenuBar,
                            QDialog, QTextEdit, QScrollArea, QSplashScreen)
from PyQt6.QtCore import Qt, QDir, QSettings, QTimer, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QIcon, QPalette, QColor, QAction, QPixmap, QPainter

# Import our modules
from database.models import create_database
from views.dashboard_view import DashboardView
from views.products_view import ProductsView
from views.invoice_view import InvoiceView
from views.reports_view import ReportsView
from views.settings_dialog import SettingsDialog

class AboutDialog(QDialog):
    """About dialog showing application information"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("درباره برنامه")
        self.setFixedSize(500, 400)
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.setup_ui()
        self.apply_styles()
    
    def setup_ui(self):
        """Setup about dialog UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # App icon and title
        header_layout = QHBoxLayout()
        
        # Icon placeholder
        icon_label = QLabel("📊")
        icon_label.setStyleSheet("""
            font-size: 48px;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #3B82F6, stop:1 #10B981);
            border-radius: 25px;
            padding: 15px;
            color: white;
        """)
        icon_label.setFixedSize(80, 80)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Title and version
        title_layout = QVBoxLayout()
        title_label = QLabel("سیستم مدیریت فاکتور فروش")
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #F9FAFB;
            background: transparent;
        """)
        
        version_label = QLabel("نسخه ۱.۰.۰")
        version_label.setStyleSheet("""
            font-size: 14px;
            color: #9CA3AF;
            background: transparent;
        """)
        
        title_layout.addWidget(title_label)
        title_layout.addWidget(version_label)
        title_layout.addStretch()
        
        header_layout.addWidget(icon_label)
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        
        # Description
        description = QTextEdit()
        description.setReadOnly(True)
        description.setFixedHeight(180)
        description.setHtml("""
        <div style="color: #F9FAFB; font-size: 14px; line-height: 1.6;">
            <p><strong>سیستم مدیریت فاکتور فروش</strong> نرم‌افزاری مدرن و کارآمد برای مدیریت فروش و صدور فاکتور است.</p>
            
            <p><strong>ویژگی‌های کلیدی:</strong></p>
            <ul>
                <li>📊 داشبورد پیشرفته با آمار لحظه‌ای</li>
                <li>📦 مدیریت کامل محصولات و موجودی</li>
                <li>🧾 صدور و چاپ فاکتورهای حرفه‌ای</li>
                <li>📈 گزارش‌گیری تفصیلی و نمودارها</li>
                <li>💾 پشتیبان‌گیری خودکار از اطلاعات</li>
                <li>🎨 واسط کاربری مدرن و زیبا</li>
            </ul>
            
            <p><strong>توسعه‌دهنده:</strong> تیم توسعه نرم‌افزار پارس<br>
            <strong>تکنولوژی:</strong> Python & PyQt6<br>
            <strong>مجوز:</strong> MIT License</p>
        </div>
        """)
        description.setStyleSheet("""
            QTextEdit {
                background: #374151;
                border: 1px solid #6B7280;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        
        close_button = QPushButton("بستن")
        close_button.setFixedHeight(35)
        close_button.clicked.connect(self.accept)
        
        website_button = QPushButton("🌐 وب‌سایت")
        website_button.setFixedHeight(35)
        website_button.clicked.connect(self.open_website)
        
        buttons_layout.addWidget(website_button)
        buttons_layout.addStretch()
        buttons_layout.addWidget(close_button)
        
        layout.addLayout(header_layout)
        layout.addWidget(description)
        layout.addLayout(buttons_layout)
    
    def apply_styles(self):
        """Apply styles to the dialog"""
        self.setStyleSheet("""
            QDialog {
                background: #1F2937;
                color: #F9FAFB;
            }
            QPushButton {
                background: #3B82F6;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #2563EB;
            }
        """)
    
    def open_website(self):
        """Open website URL"""
        from PyQt6.QtGui import QDesktopServices
        from PyQt6.QtCore import QUrl
        QDesktopServices.openUrl(QUrl("https://github.com/persian-invoice"))

class SplashScreen(QSplashScreen):
    """Custom splash screen for application startup"""
    
    def __init__(self):
        # Create a simple splash image
        pixmap = QPixmap(400, 300)
        pixmap.fill(QColor("#1F2937"))
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Background gradient
        from PyQt6.QtGui import QLinearGradient
        gradient = QLinearGradient(0, 0, 400, 300)
        gradient.setColorAt(0, QColor("#3B82F6"))
        gradient.setColorAt(1, QColor("#10B981"))
        painter.fillRect(pixmap.rect(), gradient)
        
        # App icon
        painter.setPen(QColor("white"))
        painter.setFont(QFont("Arial", 48, QFont.Weight.Bold))
        painter.drawText(pixmap.rect().adjusted(0, -50, 0, 0), Qt.AlignmentFlag.AlignCenter, "📊")
        
        # App title
        painter.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        painter.drawText(pixmap.rect().adjusted(0, 50, 0, 0), Qt.AlignmentFlag.AlignCenter, "سیستم مدیریت فاکتور فروش")
        
        # Loading text
        painter.setFont(QFont("Arial", 12))
        painter.drawText(pixmap.rect().adjusted(0, 100, 0, 0), Qt.AlignmentFlag.AlignCenter, "در حال بارگذاری...")
        
        painter.end()
        
        super().__init__(pixmap)
        self.setWindowFlags(Qt.WindowType.SplashScreen | Qt.WindowType.FramelessWindowHint)

class DatabaseInitWorker(QThread):
    """Worker thread for database initialization"""
    
    progress_updated = pyqtSignal(str)
    finished = pyqtSignal()
    error_occurred = pyqtSignal(str)
    
    def run(self):
        """Initialize database in background"""
        try:
            self.progress_updated.emit("ایجاد پایگاه داده...")
            create_database()
            
            # Simulate some loading time for demo
            import time
            time.sleep(1)
            
            self.progress_updated.emit("بارگذاری تنظیمات...")
            time.sleep(0.5)
            
            self.progress_updated.emit("آماده‌سازی واسط کاربری...")
            time.sleep(0.5)
            
            self.finished.emit()
            
        except Exception as e:
            self.error_occurred.emit(str(e))

class EnhancedMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = QSettings()
        self.setWindowTitle("سیستم مدیریت فاکتور فروش")
        self.setGeometry(100, 100, 1400, 850)
        
        # Set RTL layout direction
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        
        # Apply modern theme
        self.apply_modern_theme()
        
        # Setup UI
        self.setup_menu_bar()
        self.setup_ui()
        
        # Load settings
        self.load_window_settings()
        
        # Show maximized
        self.showMaximized()
    
    def setup_menu_bar(self):
        """Setup application menu bar"""
        menubar = self.menuBar()
        menubar.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        menubar.setStyleSheet("""
            QMenuBar {
                background: #374151;
                color: #F9FAFB;
                border-bottom: 1px solid #6B7280;
                padding: 5px;
            }
            QMenuBar::item {
                background: transparent;
                padding: 8px 12px;
                border-radius: 4px;
            }
            QMenuBar::item:selected {
                background: #4B5563;
            }
            QMenu {
                background: #374151;
                color: #F9FAFB;
                border: 1px solid #6B7280;
                border-radius: 6px;
                padding: 5px;
            }
            QMenu::item {
                padding: 8px 20px;
                border-radius: 4px;
            }
            QMenu::item:selected {
                background: #3B82F6;
            }
            QMenu::separator {
                height: 1px;
                background: #6B7280;
                margin: 5px 0px;
            }
        """)
        
        # File menu
        file_menu = menubar.addMenu("📁 فایل")
        
        new_invoice_action = QAction("🧾 فاکتور جدید", self)
        new_invoice_action.setShortcut("Ctrl+N")
        new_invoice_action.triggered.connect(lambda: self.tab_widget.setCurrentIndex(2))
        file_menu.addAction(new_invoice_action)
        
        file_menu.addSeparator()
        
        backup_action = QAction("💾 پشتیبان‌گیری", self)
        backup_action.triggered.connect(self.backup_database)
        file_menu.addAction(backup_action)
        
        restore_action = QAction("📁 بازیابی", self)
        restore_action.triggered.connect(self.restore_database)
        file_menu.addAction(restore_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("❌ خروج", self)
        exit_action.setShortcut("Alt+F4")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Tools menu
        tools_menu = menubar.addMenu("🔧 ابزارها")
        
        settings_action = QAction("⚙️ تنظیمات", self)
        settings_action.setShortcut("Ctrl+,")
        settings_action.triggered.connect(self.open_settings)
        tools_menu.addAction(settings_action)
        
        refresh_action = QAction("🔄 بروزرسانی", self)
        refresh_action.setShortcut("F5")
        refresh_action.triggered.connect(self.refresh_data)
        tools_menu.addAction(refresh_action)
        
        # Reports menu
        reports_menu = menubar.addMenu("📊 گزارش‌ها")
        
        sales_report_action = QAction("💰 گزارش فروش", self)
        sales_report_action.triggered.connect(lambda: self.tab_widget.setCurrentIndex(3))
        reports_menu.addAction(sales_report_action)
        
        # Help menu
        help_menu = menubar.addMenu("❓ راهنما")
        
        user_guide_action = QAction("📖 راهنمای کاربر", self)
        user_guide_action.triggered.connect(self.show_user_guide)
        help_menu.addAction(user_guide_action)
        
        help_menu.addSeparator()
        
        about_action = QAction("ℹ️ درباره برنامه", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def setup_ui(self):
        """Setup the main user interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Create header
        header = self.create_header()
        layout.addWidget(header)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget {
                background: transparent;
                border: none;
            }
            QTabWidget::pane {
                border: 1px solid #374151;
                background: #1F2937;
                border-radius: 12px;
                margin-top: 5px;
            }
            QTabBar::tab {
                background: #374151;
                color: #F9FAFB;
                padding: 12px 20px;
                margin: 2px;
                border-radius: 12px 12px 0px 0px;
                font-size: 15px;
                font-weight: bold;
                min-width: 150px;
            }
            QTabBar::tab:selected {
                background: #3B82F6;
                color: white;
            }
            QTabBar::tab:hover {
                background: #4B5563;
            }
        """)
        
        # Add tabs
        self.dashboard_view = DashboardView()
        self.products_view = ProductsView()
        self.invoice_view = InvoiceView()
        self.reports_view = ReportsView()
        
        self.tab_widget.addTab(self.dashboard_view, "📈 داشبورد")
        self.tab_widget.addTab(self.products_view, "📦 مدیریت کالاها")
        self.tab_widget.addTab(self.invoice_view, "🧾 صدور فاکتور")
        self.tab_widget.addTab(self.reports_view, "📊 گزارش‌ها")
        
        layout.addWidget(self.tab_widget, 1)
        
        # Setup auto-refresh timer
        self.setup_auto_refresh()
    
    def create_header(self):
        """Create the modern header section"""
        header_frame = QFrame()
        header_frame.setFixedHeight(80)
        header_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #3B82F6, stop:1 #10B981);
                border-radius: 0px;
                margin: 0px;
                padding: 0px;
            }
        """)
        
        layout = QHBoxLayout(header_frame)
        layout.setContentsMargins(25, 20, 25, 20)
        
        # Icon container
        icon_container = QFrame()
        icon_container.setFixedSize(50, 50)
        icon_container.setStyleSheet("""
            QFrame {
                background: #374151;
                border-radius: 15px;
                border: none;
            }
        """)
        
        icon_layout = QVBoxLayout(icon_container)
        icon_layout.setContentsMargins(0, 0, 0, 0)
        icon_label = QLabel("📊")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet("font-size: 28px; background: transparent;")
        icon_layout.addWidget(icon_label)
        
        # Text container
        text_container = QWidget()
        text_layout = QVBoxLayout(text_container)
        text_layout.setContentsMargins(20, 0, 0, 0)
        text_layout.setSpacing(2)
        
        # Get company name from settings
        company_name = self.settings.value("company/name", "سیستم مدیریت فاکتور فروش")
        company_desc = self.settings.value("company/description", "نسخه پیشرفته با قابلیت چاپ و گزارش‌گیری")
        
        title_label = QLabel(company_name)
        title_label.setStyleSheet("""
            color: white;
            font-size: 24px;
            font-weight: bold;
            background: transparent;
        """)
        
        subtitle_label = QLabel(company_desc)
        subtitle_label.setStyleSheet("""
            color: #D1D5DB;
            font-size: 14px;
            background: transparent;
        """)
        
        text_layout.addWidget(title_label)
        text_layout.addWidget(subtitle_label)
        text_layout.addStretch()
        
        # Quick action buttons
        actions_layout = QHBoxLayout()
        
        new_invoice_btn = QPushButton("🧾 فاکتور جدید")
        new_invoice_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255, 255, 255, 0.2);
                color: white;
                border: 2px solid white;
                border-radius: 8px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.3);
            }
        """)
        new_invoice_btn.clicked.connect(lambda: self.tab_widget.setCurrentIndex(2))
        
        settings_btn = QPushButton("⚙️")
        settings_btn.setFixedSize(40, 40)
        settings_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255, 255, 255, 0.2);
                color: white;
                border: 2px solid white;
                border-radius: 20px;
                font-size: 16px;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.3);
            }
        """)
        settings_btn.clicked.connect(self.open_settings)
        
        actions_layout.addWidget(new_invoice_btn)
        actions_layout.addWidget(settings_btn)
        
        layout.addWidget(icon_container)
        layout.addWidget(text_container)
        layout.addStretch()
        layout.addLayout(actions_layout)
        
        return header_frame
    
    def setup_auto_refresh(self):
        """Setup auto-refresh timer for dashboard"""
        if self.settings.value("appearance/auto_refresh", True, type=bool):
            interval = self.settings.value("appearance/refresh_interval", 5, type=int)
            self.refresh_timer = QTimer()
            self.refresh_timer.timeout.connect(self.refresh_data)
            self.refresh_timer.start(interval * 60 * 1000)  # Convert to milliseconds
    
    def refresh_data(self):
        """Refresh all data"""
        try:
            # Refresh dashboard
            if hasattr(self.dashboard_view, 'load_dashboard_data'):
                self.dashboard_view.load_dashboard_data()
            
            # Refresh products if visible
            if self.tab_widget.currentIndex() == 1 and hasattr(self.products_view, 'load_products'):
                self.products_view.load_products()
            
            # Refresh reports if visible
            if self.tab_widget.currentIndex() == 3:
                # Trigger refresh for active report tab
                pass
                
        except Exception as e:
            QMessageBox.warning(self, "خطا", f"خطا در بروزرسانی داده‌ها: {str(e)}")
    
    def open_settings(self):
        """Open settings dialog"""
        settings_dialog = SettingsDialog(self)
        settings_dialog.settings_changed.connect(self.apply_settings_changes)
        settings_dialog.exec()
    
    def apply_settings_changes(self):
        """Apply changes from settings"""
        # Reload header with new company info
        self.setup_ui()
        
        # Update auto-refresh timer
        if hasattr(self, 'refresh_timer'):
            self.refresh_timer.stop()
        self.setup_auto_refresh()
        
        QMessageBox.information(self, "اعمال تنظیمات", "تغییرات اعمال شد. برخی تغییرات پس از راه‌اندازی مجدد اعمال می‌شوند.")
    
    def backup_database(self):
        """Backup database"""
        try:
            import shutil
            from datetime import datetime
            
            source = "invoicing.db"
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
        from PyQt6.QtWidgets import QFileDialog
        
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
                shutil.copy2(backup_file, "invoicing.db")
                
                QMessageBox.information(
                    self, "موفقیت", 
                    "پایگاه داده با موفقیت بازیابی شد.\nلطفاً برنامه را مجدداً راه‌اندازی کنید."
                )
                
        except Exception as e:
            QMessageBox.critical(self, "خطا", f"خطا در بازیابی: {str(e)}")
    
    def show_user_guide(self):
        """Show user guide"""
        guide_dialog = QDialog(self)
        guide_dialog.setWindowTitle("راهنمای کاربر")
        guide_dialog.setFixedSize(600, 500)
        guide_dialog.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        
        layout = QVBoxLayout(guide_dialog)
        
        guide_text = QTextEdit()
        guide_text.setReadOnly(True)
        guide_text.setHtml("""
        <div style="color: #F9FAFB; font-size: 14px; line-height: 1.6;">
            <h2>راهنمای استفاده از سیستم مدیریت فاکتور</h2>
            
            <h3>🏠 داشبورد</h3>
            <p>در صفحه داشبورد می‌توانید آمار کلی فروش امروز، تعداد فاکتورها و محصولات را مشاهده کنید.</p>
            
            <h3>📦 مدیریت کالاها</h3>
            <p>برای افزودن کالای جدید:</p>
            <ul>
                <li>کد کالا و نام کالا را وارد کنید</li>
                <li>قیمت خرید و فروش را مشخص کنید</li>
                <li>موجودی اولیه و واحد را انتخاب کنید</li>
                <li>روی "ثبت کالای جدید" کلیک کنید</li>
            </ul>
            
            <h3>🧾 صدور فاکتور</h3>
            <p>برای صدور فاکتور جدید:</p>
            <ul>
                <li>نام مشتری را وارد کنید</li>
                <li>کالاهای مورد نظر را انتخاب کنید</li>
                <li>تعداد هر کالا را مشخص کنید</li>
                <li>در صورت نیاز تخفیف اعمال کنید</li>
                <li>روی "ثبت و چاپ فاکتور" کلیک کنید</li>
            </ul>
            
            <h3>📊 گزارش‌ها</h3>
            <p>بخش گزارش‌ها شامل:</p>
            <ul>
                <li>گزارش فروش با نمودار و جداول تفصیلی</li>
                <li>گزارش موجودی محصولات</li>
                <li>امکان خروجی CSV از گزارش‌ها</li>
            </ul>
            
            <h3>⚙️ تنظیمات</h3>
            <p>در بخش تنظیمات می‌توانید:</p>
            <ul>
                <li>اطلاعات شرکت را ویرایش کنید</li>
                <li>ظاهر برنامه را تغییر دهید</li>
                <li>پشتیبان‌گیری خودکار تنظیم کنید</li>
            </ul>
        </div>
        """)
        
        close_button = QPushButton("بستن")
        close_button.clicked.connect(guide_dialog.accept)
        
        layout.addWidget(guide_text)
        layout.addWidget(close_button)
        
        guide_dialog.setStyleSheet("""
            QDialog {
                background: #1F2937;
                color: #F9FAFB;
            }
            QTextEdit {
                background: #374151;
                border: 1px solid #6B7280;
                border-radius: 8px;
                padding: 15px;
            }
            QPushButton {
                background: #3B82F6;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
            }
        """)
        
        guide_dialog.exec()
    
    def show_about(self):
        """Show about dialog"""
        about_dialog = AboutDialog(self)
        about_dialog.exec()
    
    def load_window_settings(self):
        """Load window settings"""
        geometry = self.settings.value("window/geometry")
        if geometry:
            self.restoreGeometry(geometry)
        
        state = self.settings.value("window/state")
        if state:
            self.restoreState(state)
    
    def save_window_settings(self):
        """Save window settings"""
        self.settings.setValue("window/geometry", self.saveGeometry())
        self.settings.setValue("window/state", self.saveState())
    
    def closeEvent(self, event):
        """Handle application close event"""
        self.save_window_settings()
        event.accept()
    
    def apply_modern_theme(self):
        """Apply modern dark theme to the application"""
        palette = QPalette()
        
        # Define colors
        bg_color = QColor("#1F2937")
        secondary_bg = QColor("#374151")
        text_color = QColor("#F9FAFB")
        accent_color = QColor("#3B82F6")
        
        # Set palette colors
        palette.setColor(QPalette.ColorRole.Window, bg_color)
        palette.setColor(QPalette.ColorRole.WindowText, text_color)
        palette.setColor(QPalette.ColorRole.Base, secondary_bg)
        palette.setColor(QPalette.ColorRole.AlternateBase, bg_color)
        palette.setColor(QPalette.ColorRole.ToolTipBase, secondary_bg)
        palette.setColor(QPalette.ColorRole.ToolTipText, text_color)
        palette.setColor(QPalette.ColorRole.Text, text_color)
        palette.setColor(QPalette.ColorRole.Button, secondary_bg)
        palette.setColor(QPalette.ColorRole.ButtonText, text_color)
        palette.setColor(QPalette.ColorRole.BrightText, accent_color)
        palette.setColor(QPalette.ColorRole.Link, accent_color)
        palette.setColor(QPalette.ColorRole.Highlight, accent_color)
        palette.setColor(QPalette.ColorRole.HighlightedText, text_color)
        
        self.setPalette(palette)
        
        # Apply global stylesheet (same as before)
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1F2937, stop:1 #111827);
            }
            
            QWidget {
                font-family: 'Segoe UI', 'Tahoma', sans-serif;
                font-size: 14px;
                color: #F9FAFB;
                background: transparent;
            }
            
            QPushButton {
                background: #3B82F6;
                color: white;
                border: none;
                padding: 10px 16px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
            }
            
            QPushButton:hover {
                background: #4B5563;
            }
            
            QPushButton:pressed {
                background: #374151;
            }
            
            QLineEdit, QTextEdit, QSpinBox, QDoubleSpinBox {
                background: #374151;
                border: 2px solid #6B7280;
                border-radius: 8px;
                padding: 8px 12px;
                color: #F9FAFB;
                font-size: 14px;
            }
            
            QLineEdit:focus, QTextEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus {
                border-color: #3B82F6;
                background: #4B5563;
            }
            
            QComboBox {
                background: #374151;
                border: 2px solid #6B7280;
                border-radius: 8px;
                padding: 8px 12px;
                color: #F9FAFB;
                font-size: 14px;
                min-height: 20px;
            }
            
            QComboBox:focus {
                border-color: #3B82F6;
                background: #4B5563;
            }
            
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #F9FAFB;
                margin-right: 10px;
            }
            
            QComboBox QAbstractItemView {
                background: #374151;
                border: 1px solid #6B7280;
                border-radius: 8px;
                color: #F9FAFB;
                selection-background-color: #3B82F6;
                outline: none;
            }
            
            QTableWidget, QTableView {
                background: #374151;
                alternate-background-color: #4B5563;
                border: 1px solid #6B7280;
                border-radius: 12px;
                gridline-color: #6B7280;
                color: #F9FAFB;
                font-size: 14px;
            }
            
            QTableWidget::item, QTableView::item {
                padding: 8px;
                border: none;
            }
            
            QTableWidget::item:selected, QTableView::item:selected {
                background: #3B82F6;
                color: white;
            }
            
            QHeaderView::section {
                background: #4B5563;
                color: #F9FAFB;
                padding: 10px;
                border: 1px solid #6B7280;
                font-weight: bold;
                font-size: 14px;
            }
            
            QLabel {
                color: #F9FAFB;
                background: transparent;
            }
            
            QFrame {
                border-radius: 12px;
            }
            
            QScrollBar:vertical {
                background: #374151;
                width: 12px;
                border-radius: 6px;
                margin: 0;
            }
            
            QScrollBar::handle:vertical {
                background: #6B7280;
                border-radius: 6px;
                min-height: 20px;
            }
            
            QScrollBar::handle:vertical:hover {
                background: #9CA3AF;
            }
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0;
            }
            
            QDateEdit {
                background: #374151;
                border: 2px solid #6B7280;
                border-radius: 8px;
                padding: 8px 12px;
                color: #F9FAFB;
                font-size: 14px;
            }
            
            QDateEdit:focus {
                border-color: #3B82F6;
                background: #4B5563;
            }
        """)

def main():
    # Enable high DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Persian Invoicing System")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Persian Software")
    app.setOrganizationDomain("persian-software.com")
    
    # Set RTL layout direction globally
    app.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
    
    # Show splash screen
    splash = SplashScreen()
    splash.show()
    
    # Initialize database in background
    def update_splash(message):
        splash.showMessage(message, Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignCenter, Qt.GlobalColor.white)
    
    def show_main_window():
        splash.close()
        window = EnhancedMainWindow()
        window.show()
    
    def handle_error(error):
        splash.close()
        QMessageBox.critical(None, "خطا", f"خطا در راه‌اندازی برنامه: {error}")
        sys.exit(1)
    
    # Initialize database
    db_worker = DatabaseInitWorker()
    db_worker.progress_updated.connect(update_splash)
    db_worker.finished.connect(show_main_window)
    db_worker.error_occurred.connect(handle_error)
    db_worker.start()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()