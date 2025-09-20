"""
Report generation service
"""

from database.models import get_db_session, Invoice, Product, InvoiceItem
from sqlalchemy import func, and_
from datetime import datetime, date
from typing import Dict, Any

class ReportService:
    """Service for generating various reports"""
    
    @staticmethod
    def generate_sales_report(start_date: date, end_date: date) -> Dict[str, Any]:
        """Generate sales report for date range"""
        session = get_db_session()
        
        invoices = session.query(Invoice).filter(
            and_(
                func.date(Invoice.issue_date) >= start_date,
                func.date(Invoice.issue_date) <= end_date
            )
        ).all()
        
        total_sales = sum(invoice.final_price for invoice in invoices)
        total_invoices = len(invoices)
        average_sale = total_sales / total_invoices if total_invoices > 0 else 0
        total_discount = sum(invoice.discount for invoice in invoices)
        
        session.close()
        
        return {
            'start_date': start_date,
            'end_date': end_date,
            'total_sales': total_sales,
            'total_invoices': total_invoices,
            'average_sale': average_sale,
            'total_discount': total_discount,
            'invoices': invoices
        }
    
    @staticmethod
    def generate_product_report() -> Dict[str, Any]:
        """Generate product inventory report"""
        session = get_db_session()
        
        products = session.query(Product).all()
        total_products = len(products)
        out_of_stock = len([p for p in products if p.stock_quantity == 0])
        low_stock = len([p for p in products if 0 < p.stock_quantity <= 5])
        
        total_inventory_value = sum(
            product.stock_quantity * product.purchase_price 
            for product in products
        )
        
        session.close()
        
        return {
            'total_products': total_products,
            'out_of_stock': out_of_stock,
            'low_stock': low_stock,
            'total_inventory_value': total_inventory_value,
            'products': products
        }
