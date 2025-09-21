"""
Main Window for Persian Invoicing System
Enhanced with modern UI and improved navigation
"""

import os
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                           QTabWidget, QMenuBar, QStatusBar, QLabel, 
                           QPushButton, QFrame, QMessageBox, QApplication,
                           QSizePolicy, QToolBar)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont, QIcon, QAction, QPixmap
from views.dashboard_view import DashboardView
from views.invoice_view import InvoiceView
from views.products_view import ProductsView
from views.reports_view import ReportsView
from views.settings_dialog import SettingsDialog
from services.database_service import DatabaseService
import jdatetime
from datetime import datetime

class ModernTabWidget(QTabWidget):
    """Custom tab widget with modern styling"""
    
    def __init__(self):
        super().__init__()
        self.setTabPosition(QTabWidget.TabPosition.West)
        self.setMovable(False)
        self.setTabsClosable(False)
        
        # Custom styling for tabs
        self.setStyleSheet("""
            QTabWidget::pane {
                border: 2px solid #dee2e6;
                border-radius: 8px;
                background-color: white;
                margin-left: 10px;
            }
            
            QTabWidget::tab-bar {
                alignment: left;
            }
            
            QTabBar::tab {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f8f9fa, stop:1 #e9ecef);
                border: 2px solid #dee2e6;
                border-bottom: none;
                border-top-left-radius: 8px;
                border-bottom-left-radius: 8px;
                min-width: 120px;
                min-height: 60px;
                padding: 10px;
                margin: 2px 0px;
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
        """)

class StatusBarWidget(QStatusBar):
    """Enhanced status bar with system information"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.setup_timer()
        
    def setup_ui(self):
        """Setup status bar UI"""
        # System info
        self.system_label = QLabel("سیستم مدیریت فاکتور فروش")
        self.system_label.setFont(QFont("Vazirmatn", 9))
        
        # Date and time
        self.datetime_label = QLabel()
        self.datetime_label.setFont(QFont("Vazirmatn", 9))
        
        # Connection status
        self.db_status_label = QLabel("💾 دیتابیس: متصل")
        self.db_status_label.setFont(QFont("Vazirmatn", 9))
        self.db_status_label.setStyleSheet("color: #27ae60;")
        
        # Add widgets
        self.addWidget(self.system_label)
        self.addPermanentWidget(self.db_status_label)
        self.addPermanentWidget(self.datetime_label)
        
        # Styling
        self.setStyleSheet("""
            QStatusBar {
                background-color: #f8f9fa;
                border-top: 1px solid #dee2e6;
                padding: 5px;
            }
            QStatusBar::item {
                border: none;
            }
        """)
        
    def setup_timer(self):
        """Setup timer for updating date/time"""
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_datetime)
        self.timer.start(1000)  # Update every second
        self.update_datetime()
        
    def update_datetime(self):
        """Update date and time display"""
        now = datetime.now()
        jdate = jdatetime.datetime.fromgregorian(datetime=now)
        
        persian_date = jdate.strftime('%Y/%m/%d')
        time_str = now.strftime('%H:%M:%S')
        
        self.datetime_label.setText(f"📅 {persian_date} | 🕐 {time_str}")

class MainWindow(QMainWindow):
    """Enhanced main window with modern design"""
    
    def __init__(self):
        super().__init__()
        self.db_service = DatabaseService()
        self.setup_ui()
        self.setup_styling()
        self.setup_connections()
        
    def setup_ui(self):
        """Setup the main user interface"""
        self.setWindowTitle("سیستم مدیریت فاکتور فروش - نسخه پیشرفته")
        self.setGeometry(100, 100, 1400, 900)
        
        # Set window icon if available
        if os.path.exists("assets/icon.png"):
            self.setWindowIcon(QIcon("assets/icon.png"))
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Header section
        header_widget = self.create_header()
        main_layout.addWidget(header_widget)
        
        # Create tab widget
        self.tab_widget = ModernTabWidget()
        
        # Create views
        self.dashboard_view = DashboardView()
        self.invoice_view = InvoiceView()
        self.products_view = ProductsView()
        self.reports_view = ReportsView()
        
        # Add tabs with icons
        self.tab_widget.addTab(self.dashboard_view, "📊 داشبورد")
        self.tab_widget.addTab(self.invoice_view, "🧾 صدور فاکتور")
        self.tab_widget.addTab(self.products_view, "📦 مدیریت کالاها")
        self.tab_widget.addTab(self.reports_view, "📈 گزارشات")
        
        main_layout.addWidget(self.tab_widget)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create status bar
        self.status_bar = StatusBarWidget()
        self.setStatusBar(self.status_bar)
        
        # Set initial tab
        self.tab_widget.setCurrentIndex(0)
        
    def create_header(self):
        """Create application header"""
        header_frame = QFrame()
        header_frame.setFrameStyle(QFrame.Shape.Box)
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(20, 15, 20, 15)
        
        # Logo/Title section
        title_layout = QVBoxLayout()
        
        app_title = QLabel("سیستم مدیریت فاکتور فروش")
        app_title.setFont(QFont("Vazirmatn", 16, QFont.Weight.Bold))
        app_title.setStyleSheet("color: #2c3e50;")
        
        app_subtitle = QLabel("نسخه پیشرفته با قابلیت‌های کامل مدیریت")
        app_subtitle.setFont(QFont("Vazirmatn", 10))
        app_subtitle.setStyleSheet("color: #7f8c8d;")
        
        title_layout.addWidget(app_title)
        title_layout.addWidget(app_subtitle)
        
        # Quick action buttons
        actions_layout = QHBoxLayout()
        
        self.quick_invoice_btn = QPushButton("🧾 فاکتور سریع")
        self.quick_product_btn = QPushButton("📦 کالای جدید")
        self.settings_btn = QPushButton("⚙️ تنظیمات")
        self.help_btn = QPushButton("❓ راهنما")
        
        for btn in [self.quick_invoice_btn, self.quick_product_btn, self.settings_btn, self.help_btn]:
            btn.setFont(QFont("Vazirmatn", 10, QFont.Weight.Bold))
            btn.setMinimumHeight(35)
            btn.setMaximumWidth(120)
            actions_layout.addWidget(btn)
        
        # Add to header layout
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        header_layout.addLayout(actions_layout)
        
        # Header styling
        header_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                border: none;
                border-radius: 12px;
                margin-bottom: 10px;
            }
            QLabel {
                color: white;
            }
            QPushButton {
                background: rgba(255, 255, 255, 0.2);
                color: white;
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 6px;
                padding: 8px 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.3);
                border-color: white;
            }
            QPushButton:pressed {
                background: rgba(255, 255, 255, 0.1);
            }
        """)
        
        return header_frame
        
    def create_menu_bar(self):
        """Create application menu bar"""
        menubar = self.menuBar()
        menubar.setFont(QFont("Vazirmatn", 10))
        
        # File menu
        file_menu = menubar.addMenu('فایل')
        
        new_invoice_action = QAction('🧾 فاکتور جدید', self)
        new_invoice_action.setShortcut('Ctrl+N')
        new_invoice_action.triggered.connect(lambda: self.tab_widget.setCurrentIndex(1))
        file_menu.addAction(new_invoice_action)
        
        new_product_action = QAction('📦 کالای جدید', self)
        new_product_action.setShortcut('Ctrl+P')
        new_product_action.triggered.connect(lambda: self.tab_widget.setCurrentIndex(2))
        file_menu.addAction(new_product_action)
        
        file_menu.addSeparator()
        
        backup_action = QAction('💾 پشتیبان‌گیری', self)
        backup_action.triggered.connect(self.create_backup)
        file_menu.addAction(backup_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction('❌ خروج', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # View menu
        view_menu = menubar.addMenu('نمایش')
        
        dashboard_action = QAction('📊 داشبورد', self)
        dashboard_action.triggered.connect(lambda: self.tab_widget.setCurrentIndex(0))
        view_menu.addAction(dashboard_action)
        
        reports_action = QAction('📈 گزارشات', self)
        reports_action.triggered.connect(lambda: self.tab_widget.setCurrentIndex(3))
        view_menu.addAction(reports_action)
        
        # Tools menu
        tools_menu = menubar.addMenu('ابزارها')
        
        settings_action = QAction('⚙️ تنظیمات', self)
        settings_action.triggered.connect(self.show_settings)
        tools_menu.addAction(settings_action)
        
        refresh_action = QAction('🔄 به‌روزرسانی', self)
        refresh_action.setShortcut('F5')
        refresh_action.triggered.connect(self.refresh_all_views)
        tools_menu.addAction(refresh_action)
        
        # Help menu
        help_menu = menubar.addMenu('راهنما')
        
        about_action = QAction('ℹ️ درباره نرم‌افزار', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
        help_action = QAction('❓ راهنمای استفاده', self)
        help_action.triggered.connect(self.show_help)
        help_menu.addAction(help_action)
        
        # Menu styling
        menubar.setStyleSheet("""
            QMenuBar {
                background-color: #f8f9fa;
                border-bottom: 1px solid #dee2e6;
                padding: 5px;
            }
            QMenuBar::item {
                background: transparent;
                padding: 8px 12px;
                border-radius: 4px;
                margin: 2px;
            }
            QMenuBar::item:selected {
                background-color: #e3f2fd;
                color: #1976d2;
            }
            QMenu {
                background-color: white;
                border: 1px solid #dee2e6;
                border-radius: 6px;
                padding: 5px;
            }
            QMenu::item {
                padding: 8px 20px;
                border-radius: 4px;
            }
            QMenu::item:selected {
                background-color: #e3f2fd;
                color: #1976d2;
            }
        """)
        
    def setup_styling(self):
        """Setup global window styling"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8f9fa;
                font-family: 'Vazirmatn', Arial, sans-serif;
            }
        """)
        
    def setup_connections(self):
        """Setup signal connections between components"""
        # Connect quick action buttons
        self.quick_invoice_btn.clicked.connect(lambda: self.tab_widget.setCurrentIndex(1))
        self.quick_product_btn.clicked.connect(lambda: self.tab_widget.setCurrentIndex(2))
        self.settings_btn.clicked.connect(self.show_settings)
        self.help_btn.clicked.connect(self.show_help)
        
        # Connect dashboard quick actions
        dashboard_buttons = self.dashboard_view.get_quick_action_buttons()
        dashboard_buttons['new_invoice'].clicked.connect(lambda: self.tab_widget.setCurrentIndex(1))
        dashboard_buttons['new_product'].clicked.connect(lambda: self.tab_widget.setCurrentIndex(2))
        dashboard_buttons['reports'].clicked.connect(lambda: self.tab_widget.setCurrentIndex(3))
        
        # Connect view refresh signals
        self.dashboard_view.refresh_requested.connect(self.refresh_dashboard_dependents)
        self.invoice_view.invoice_created.connect(self.on_invoice_created)
        
    def refresh_all_views(self):
        """Refresh all views"""
        try:
            self.dashboard_view.load_dashboard_data()
            self.products_view.load_products()
            self.status_bar.system_label.setText("📊 همه بخش‌ها به‌روزرسانی شدند")
            
            # Reset status message after 3 seconds
            QTimer.singleShot(3000, lambda: 
                self.status_bar.system_label.setText("سیستم مدیریت فاکتور فروش")
            )
        except Exception as e:
            QMessageBox.critical(self, "خطا", f"خطا در به‌روزرسانی: {str(e)}")
    
    def refresh_dashboard_dependents(self):
        """Refresh views that depend on dashboard data"""
        self.products_view.load_products()
    
    def on_invoice_created(self, message):
        """Handle invoice creation"""
        self.dashboard_view.load_dashboard_data()
        self.products_view.load_products()
        self.status_bar.system_label.setText(f"✅ {message}")
        
        # Reset status message after 5 seconds
        QTimer.singleShot(5000, lambda: 
            self.status_bar.system_label.setText("سیستم مدیریت فاکتور فروش")
        )
    
    def create_backup(self):
        """Create database backup"""
        try:
            success, message = self.db_service.backup_database()
            if success:
                QMessageBox.information(self, "موفقیت", message)
                self.status_bar.system_label.setText("💾 پشتیبان با موفقیت ایجاد شد")
            else:
                QMessageBox.critical(self, "خطا", message)
                self.status_bar.system_label.setText("❌ خطا در ایجاد پشتیبان")
        except Exception as e:
            QMessageBox.critical(self, "خطا", f"خطا در ایجاد پشتیبان: {str(e)}")
    
    def show_settings(self):
        """Show settings dialog"""
        try:
            settings_dialog = SettingsDialog(self)
            settings_dialog.exec()
        except Exception as e:
            QMessageBox.critical(self, "خطا", f"خطا در باز کردن تنظیمات: {str(e)}")
    
    def show_about(self):
        """Show about dialog"""
        about_text = """
        <h2>سیستم مدیریت فاکتور فروش</h2>
        <p><b>نسخه:</b> 2.0</p>
        <p><b>سازنده:</b> KimiVerse</p>
        <p><b>توضیحات:</b> نرم‌افزار پیشرفته مدیریت فاکتور فروش با قابلیت‌های:</p>
        <ul>
        <li>صدور فاکتور با امکان انتخاب پس‌زمینه</li>
        <li>مدیریت کالاها با کنترل موجودی</li>
        <li>گزارش‌گیری پیشرفته</li>
        <li>خروجی PDF و تصویر</li>
        <li>پشتیبانی کامل از تاریخ شمسی</li>
        <li>رابط کاربری مدرن و فارسی</li>
        </ul>
        <p><b>تاریخ ساخت:</b> ۱۴۰۳</p>
        """
        
        QMessageBox.about(self, "درباره نرم‌افزار", about_text)
    
    def show_help(self):
        """Show help dialog"""
        help_text = """
        <h3>راهنمای سریع استفاده</h3>
        
        <h4>📊 داشبورد:</h4>
        <p>• مشاهده آمار کلی سیستم</p>
        <p>• کنترل آخرین فاکتورها</p>
        <p>• مدیریت کالاهای کم‌موجود</p>
        
        <h4>🧾 صدور فاکتور:</h4>
        <p>• وارد کردن اطلاعات مشتری</p>
        <p>• انتخاب کالاها و تعداد</p>
        <p>• اعمال تخفیف</p>
        <p>• خروجی PDF یا تصویر</p>
        
        <h4>📦 مدیریت کالاها:</h4>
        <p>• افزودن کالای جدید</p>
        <p>• ویرایش اطلاعات کالا</p>
        <p>• کنترل موجودی</p>
        
        <h4>📈 گزارشات:</h4>
        <p>• گزارش فروش روزانه/ماهانه</p>
        <p>• گزارش موجودی کالاها</p>
        <p>• آمار مشتریان</p>
        
        <p><b>کلیدهای میانبر:</b></p>
        <p>Ctrl+N: فاکتور جدید</p>
        <p>Ctrl+P: کالای جدید</p>
        <p>F5: به‌روزرسانی</p>
        <p>Ctrl+Q: خروج</p>
        """
        
        help_dialog = QMessageBox(self)
        help_dialog.setWindowTitle("راهنمای استفاده")
        help_dialog.setText(help_text)
        help_dialog.setTextFormat(Qt.TextFormat.RichText)
        help_dialog.exec()
    
    def closeEvent(self, event):
        """Handle window close event"""
        reply = QMessageBox.question(
            self,
            'تأیید خروج',
            'آیا مطمئن هستید که می‌خواهید از برنامه خارج شوید؟',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Save any pending data
            try:
                self.db_service.close()
            except:
                pass
            event.accept()
        else:
            event.ignore()