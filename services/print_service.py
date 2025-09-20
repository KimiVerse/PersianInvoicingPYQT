"""
Enhanced printing service
"""

from PyQt6.QtPrintSupport import QPrintDialog, QPrinter
from PyQt6.QtGui import QTextDocument, QPageLayout, QPageSize
from PyQt6.QtWidgets import QWidget, QMessageBox
from PyQt6.QtCore import QMarginsF
import os
from typing import Optional

class PrintService:
    """Service for printing invoices and reports"""
    
    @staticmethod
    def print_document(html_content: str, title: str = "Document", parent: Optional[QWidget] = None):
        """Print HTML content"""
        try:
            printer = QPrinter(QPrinter.PrinterMode.HighResolution)
            printer.setPageSize(QPageSize(QPageSize.PageSizeId.A4))
            printer.setPageOrientation(QPageLayout.Orientation.Portrait)
            
            # Set margins
            page_layout = QPageLayout(
                QPageSize(QPageSize.PageSizeId.A4),
                QPageLayout.Orientation.Portrait,
                QMarginsF(20, 20, 20, 20)
            )
            printer.setPageLayout(page_layout)
            
            # Show print dialog
            print_dialog = QPrintDialog(printer, parent)
            print_dialog.setWindowTitle(f"چاپ {title}")
            
            if print_dialog.exec() == QPrintDialog.DialogCode.Accepted:
                # Create document and print
                document = QTextDocument()
                document.setHtml(html_content)
                document.print(printer)
                
                if parent:
                    QMessageBox.information(parent, "چاپ", f"{title} با موفقیت چاپ شد.")
                return True
            
        except Exception as e:
            if parent:
                QMessageBox.critical(parent, "خطا در چاپ", f"خطا در چاپ {title}: {str(e)}")
            return False
        
        return False
    
    @staticmethod
    def save_as_pdf(html_content: str, filename: str, title: str = "Document", parent: Optional[QWidget] = None):
        """Save HTML content as PDF"""
        try:
            printer = QPrinter(QPrinter.PrinterMode.HighResolution)
            printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
            printer.setOutputFileName(filename)
            printer.setPageSize(QPageSize(QPageSize.PageSizeId.A4))
            
            document = QTextDocument()
            document.setHtml(html_content)
            document.print(printer)
            
            if parent:
                QMessageBox.information(parent, "ذخیره PDF", f"{title} به صورت PDF ذخیره شد.")
            return True
            
        except Exception as e:
            if parent:
                QMessageBox.critical(parent, "خطا در ذخیره", f"خطا در ذخیره {title}: {str(e)}")
            return False