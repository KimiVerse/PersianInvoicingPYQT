"""
Print Service for Persian Invoicing System
Enhanced with PDF and image export capabilities
"""

import os
from datetime import datetime
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QRect, Qt
from PyQt6.QtGui import (QPainter, QFont, QPixmap, QColor, QPen, 
                        QBrush, QFontMetrics, QImage)
from PyQt6.QtPrintSupport import QPrinter
import jdatetime

class PrintService:
    """Enhanced print service with multiple export formats"""
    
    def __init__(self):
        self.setup_fonts()
        self.setup_styles()
        
    def setup_fonts(self):
        """Setup fonts for different text elements"""
        self.title_font = QFont("Vazirmatn", 16, QFont.Weight.Bold)
        self.header_font = QFont("Vazirmatn", 14, QFont.Weight.Bold)
        self.normal_font = QFont("Vazirmatn", 11)
        self.small_font = QFont("Vazirmatn", 9)
        self.table_font = QFont("Vazirmatn", 10)
        
    def setup_styles(self):
        """Setup color and style constants"""
        self.primary_color = QColor(41, 128, 185)  # Blue
        self.secondary_color = QColor(46, 125, 50)  # Green
        self.text_color = QColor(33, 33, 33)  # Dark gray
        self.light_gray = QColor(245, 245, 245)
        self.border_color = QColor(200, 200, 200)
        
    def print_invoice(self, invoice_data, printer):
        """Print invoice to printer"""
        painter = QPainter()
        painter.begin(printer)
        
        try:
            self.draw_invoice(painter, invoice_data, printer.pageRect())
        finally:
            painter.end()
    
    def export_to_pdf(self, invoice_data, file_path):
        """Export invoice to PDF"""
        try:
            printer = QPrinter(QPrinter.Mode.HighResolution)
            printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
            printer.setOutputFileName(file_path)
            printer.setPageSize(QPrinter.PageSize.A4)
            printer.setPageMargins(20, 20, 20, 20, QPrinter.Unit.Millimeter)
            
            painter = QPainter()
            painter.begin(printer)
            
            try:
                self.draw_invoice(painter, invoice_data, printer.pageRect())
                return True
            finally:
                painter.end()
                
        except Exception as e:
            print(f"Error exporting to PDF: {e}")
            return False
    
    def export_to_image(self, invoice_data, file_path):
        """Export invoice to image (PNG/JPG)"""
        try:
            # Create high-resolution image
            width, height = 2480, 3508  # A4 at 300 DPI
            image = QImage(width, height, QImage.Format.Format_RGB32)
            image.fill(Qt.GlobalColor.white)
            
            painter = QPainter()
            painter.begin(image)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            
            try:
                rect = QRect(0, 0, width, height)
                self.draw_invoice(painter, invoice_data, rect)
                
                # Save image
                return image.save(file_path)
            finally:
                painter.end()
                
        except Exception as e:
            print(f"Error exporting to image: {e}")
            return False
    
    def draw_invoice(self, painter, invoice_data, page_rect):
        """Draw complete invoice on painter"""
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Calculate margins and content area
        margin = min(page_rect.width(), page_rect.height()) * 0.05  # 5% margin
        content_rect = QRect(
            int(page_rect.x() + margin),
            int(page_rect.y() + margin),
            int(page_rect.width() - 2 * margin),
            int(page_rect.height() - 2 * margin)
        )
        
        current_y = content_rect.y()
        
        # Draw background if specified
        if invoice_data.get('background_image_path') and os.path.exists(invoice_data['background_image_path']):
            current_y = self.draw_background(painter, invoice_data['background_image_path'], content_rect, current_y)
        
        # Draw header
        current_y = self.draw_header(painter, invoice_data, content_rect, current_y)
        
        # Draw invoice info
        current_y = self.draw_invoice_info(painter, invoice_data, content_rect, current_y)
        
        # Draw customer info
        current_y = self.draw_customer_info(painter, invoice_data, content_rect, current_y)
        
        # Draw items table
        current_y = self.draw_items_table(painter, invoice_data, content_rect, current_y)
        
        # Draw totals
        current_y = self.draw_totals(painter, invoice_data, content_rect, current_y)
        
        # Draw footer
        self.draw_footer(painter, invoice_data, content_rect, current_y)
        
    def draw_background(self, painter, image_path, content_rect, current_y):
        """Draw background image"""
        try:
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                # Scale image to fit content area while maintaining aspect ratio
                scaled_pixmap = pixmap.scaled(
                    content_rect.size(),
                    Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                    Qt.TransformationMode.SmoothTransformation
                )
                
                # Draw with reduced opacity
                painter.setOpacity(0.1)
                painter.drawPixmap(content_rect, scaled_pixmap)
                painter.setOpacity(1.0)
        except Exception as e:
            print(f"Error drawing background: {e}")
        
        return current_y
    
    def draw_header(self, painter, invoice_data, content_rect, current_y):
        """Draw invoice header"""
        # Main title
        painter.setPen(QPen(self.primary_color))
        painter.setFont(self.title_font)
        
        title_text = "فاکتور فروش"
        title_metrics = QFontMetrics(self.title_font)
        title_width = title_metrics.horizontalAdvance(title_text)
        title_x = content_rect.x() + (content_rect.width() - title_width) // 2
        
        painter.drawText(title_x, current_y + title_metrics.height(), title_text)
        current_y += title_metrics.height() + 20
        
        # Custom header text if provided
        if invoice_data.get('header_text'):
            painter.setPen(QPen(self.text_color))
            painter.setFont(self.normal_font)
            
            header_lines = invoice_data['header_text'].split('\\n')
            metrics = QFontMetrics(self.normal_font)
            
            for line in header_lines:
                line_width = metrics.horizontalAdvance(line)
                line_x = content_rect.x() + (content_rect.width() - line_width) // 2
                painter.drawText(line_x, current_y + metrics.height(), line)
                current_y += metrics.height() + 5
            
            current_y += 15
        
        # Separator line
        painter.setPen(QPen(self.border_color, 2))
        painter.drawLine(content_rect.x(), current_y, content_rect.x() + content_rect.width(), current_y)
        current_y += 30
        
        return current_y
    
    def draw_invoice_info(self, painter, invoice_data, content_rect, current_y):
        """Draw invoice information (number and date)"""
        painter.setPen(QPen(self.text_color))
        painter.setFont(self.normal_font)
        metrics = QFontMetrics(self.normal_font)
        
        # Invoice number
        invoice_num_text = f"شماره فاکتور: {invoice_data.get('invoice_number', 'N/A')}"
        painter.drawText(content_rect.x(), current_y + metrics.height(), invoice_num_text)
        
        # Persian date
        if 'issue_date' in invoice_data:
            jdate = jdatetime.datetime.fromgregorian(datetime=invoice_data['issue_date'])
            date_text = f"تاریخ: {jdate.strftime('%Y/%m/%d')}"
            date_width = metrics.horizontalAdvance(date_text)
            date_x = content_rect.x() + content_rect.width() - date_width
            painter.drawText(date_x, current_y + metrics.height(), date_text)
        
        current_y += metrics.height() + 30
        return current_y
    
    def draw_customer_info(self, painter, invoice_data, content_rect, current_y):
        """Draw customer information"""
        painter.setPen(QPen(self.text_color))
        painter.setFont(self.header_font)
        metrics = QFontMetrics(self.header_font)
        
        # Customer section title
        painter.drawText(content_rect.x(), current_y + metrics.height(), "مشخصات مشتری:")
        current_y += metrics.height() + 15
        
        # Customer details
        painter.setFont(self.normal_font)
        metrics = QFontMetrics(self.normal_font)
        
        customer_info = [
            f"نام: {invoice_data.get('customer_name', '')}",
            f"تلفن: {invoice_data.get('customer_phone', '')}",
            f"آدرس: {invoice_data.get('customer_address', '')}"
        ]
        
        for info in customer_info:
            if info.split(': ')[1]:  # Only draw if value exists
                painter.drawText(content_rect.x() + 20, current_y + metrics.height(), info)
                current_y += metrics.height() + 8
        
        current_y += 20
        return current_y
    
    def draw_items_table(self, painter, invoice_data, content_rect, current_y):
        """Draw items table"""
        items = invoice_data.get('items', [])
        if not items:
            return current_y
        
        # Table configuration
        table_width = content_rect.width()
        col_widths = [
            int(table_width * 0.4),   # Product name
            int(table_width * 0.15),  # Quantity
            int(table_width * 0.225), # Unit price
            int(table_width * 0.225)  # Total price
        ]
        
        # Table headers
        headers = ["نام کالا", "تعداد", "قیمت واحد (تومان)", "قیمت کل (تومان)"]
        
        # Draw table header
        painter.setPen(QPen(self.text_color))
        painter.setFont(self.table_font)
        painter.setBrush(QBrush(self.light_gray))
        
        header_height = 40
        header_rect = QRect(content_rect.x(), current_y, table_width, header_height)
        painter.drawRect(header_rect)
        
        # Draw header text
        painter.setBrush(QBrush())  # Clear brush
        col_x = content_rect.x()
        metrics = QFontMetrics(self.table_font)
        text_y = current_y + (header_height + metrics.height()) // 2
        
        for i, header in enumerate(headers):
            header_width = metrics.horizontalAdvance(header)
            header_x = col_x + (col_widths[i] - header_width) // 2
            painter.drawText(header_x, text_y, header)
            
            # Draw column separator
            if i < len(headers) - 1:
                col_x += col_widths[i]
                painter.drawLine(col_x, current_y, col_x, current_y + header_height)
        
        current_y += header_height
        
        # Draw table rows
        row_height = 35
        for row_index, item in enumerate(items):
            # Alternate row colors
            if row_index % 2 == 1:
                painter.setBrush(QBrush(QColor(250, 250, 250)))
                row_rect = QRect(content_rect.x(), current_y, table_width, row_height)
                painter.drawRect(row_rect)
                painter.setBrush(QBrush())  # Clear brush
            
            # Draw row data
            col_x = content_rect.x()
            text_y = current_y + (row_height + metrics.height()) // 2
            
            row_data = [
                item.get('product_name', ''),
                str(item.get('quantity', 0)),
                f"{item.get('unit_price', 0):,}",
                f"{item.get('total_price', 0):,}"
            ]
            
            for i, data in enumerate(row_data):
                if i == 0:  # Product name - left aligned
                    text_x = col_x + 10
                else:  # Numbers - center aligned
                    data_width = metrics.horizontalAdvance(data)
                    text_x = col_x + (col_widths[i] - data_width) // 2
                
                painter.drawText(text_x, text_y, data)
                
                # Draw column separator
                if i < len(row_data) - 1:
                    col_x += col_widths[i]
                    painter.drawLine(col_x, current_y, col_x, current_y + row_height)
            
            # Draw row separator
            painter.drawLine(content_rect.x(), current_y + row_height, 
                           content_rect.x() + table_width, current_y + row_height)
            
            current_y += row_height
        
        current_y += 20
        return current_y
    
    def draw_totals(self, painter, invoice_data, content_rect, current_y):
        """Draw totals section"""
        items = invoice_data.get('items', [])
        subtotal = sum(item.get('total_price', 0) for item in items)
        discount = invoice_data.get('discount_amount', 0)
        final_total = subtotal - discount
        
        # Totals box
        totals_width = content_rect.width() // 3
        totals_x = content_rect.x() + content_rect.width() - totals_width
        
        painter.setPen(QPen(self.border_color))
        painter.setFont(self.normal_font)
        metrics = QFontMetrics(self.normal_font)
        
        # Calculate box height
        box_height = metrics.height() * 4 + 40  # 3 lines + padding
        
        # Draw totals box
        totals_rect = QRect(totals_x, current_y, totals_width, box_height)
        painter.drawRect(totals_rect)
        
        # Draw totals text
        painter.setPen(QPen(self.text_color))
        line_height = metrics.height() + 8
        text_y = current_y + 20
        
        totals_data = [
            ("جمع کل:", f"{subtotal:,} تومان"),
            ("تخفیف:", f"{discount:,} تومان"),
            ("مبلغ نهایی:", f"{final_total:,} تومان")
        ]
        
        for i, (label, value) in enumerate(totals_data):
            # Draw label
            painter.drawText(totals_x + 10, text_y + metrics.height(), label)
            
            # Draw value (right aligned)
            value_width = metrics.horizontalAdvance(value)
            value_x = totals_x + totals_width - value_width - 10
            
            # Highlight final total
            if i == 2:  # Final total
                painter.setPen(QPen(self.secondary_color))
                painter.setFont(QFont("Vazirmatn", 12, QFont.Weight.Bold))
                metrics = QFontMetrics(painter.font())
                value_width = metrics.horizontalAdvance(value)
                value_x = totals_x + totals_width - value_width - 10
            
            painter.drawText(value_x, text_y + metrics.height(), value)
            
            # Reset font for next line
            if i == 2:
                painter.setPen(QPen(self.text_color))
                painter.setFont(self.normal_font)
                metrics = QFontMetrics(self.normal_font)
            
            text_y += line_height
        
        return current_y + box_height + 30
    
    def draw_footer(self, painter, invoice_data, content_rect, current_y):
        """Draw footer with notes and signature"""
        painter.setPen(QPen(self.text_color))
        painter.setFont(self.normal_font)
        metrics = QFontMetrics(self.normal_font)
        
        # Notes section
        notes = invoice_data.get('notes', '')
        if notes:
            painter.setFont(self.header_font)
            header_metrics = QFontMetrics(self.header_font)
            painter.drawText(content_rect.x(), current_y + header_metrics.height(), "یادداشت:")
            current_y += header_metrics.height() + 10
            
            painter.setFont(self.normal_font)
            
            # Split notes into lines if needed
            note_lines = notes.split('\\n')
            for line in note_lines:
                painter.drawText(content_rect.x() + 20, current_y + metrics.height(), line)
                current_y += metrics.height() + 5
            
            current_y += 20
        
        # Signature line
        signature_y = content_rect.y() + content_rect.height() - 60
        if current_y < signature_y:
            current_y = signature_y
        
        # Company signature
        painter.drawText(content_rect.x(), current_y, "مهر و امضای فروشنده:")
        
        # Signature line
        line_y = current_y + 30
        line_start_x = content_rect.x() + 150
        line_end_x = content_rect.x() + content_rect.width() // 2
        painter.drawLine(line_start_x, line_y, line_end_x, line_y)
        
        # Customer signature
        customer_sig_x = content_rect.x() + content_rect.width() - 200
        painter.drawText(customer_sig_x, current_y, "امضای خریدار:")
        
        # Customer signature line
        cust_line_start_x = customer_sig_x + 100
        cust_line_end_x = content_rect.x() + content_rect.width()
        painter.drawLine(cust_line_start_x, line_y, cust_line_end_x, line_y)
    
    def format_persian_number(self, number):
        """Convert number to Persian digits"""
        persian_digits = '۰۱۲۳۴۵۶۷۸۹'
        english_digits = '0123456789'
        
        number_str = str(number)
        for i, english_digit in enumerate(english_digits):
            number_str = number_str.replace(english_digit, persian_digits[i])
        
        return number_str