"""
Database service for common operations
"""

from database.models import get_db_session, Product, Invoice, InvoiceItem
from sqlalchemy import func, and_
from datetime import datetime, date
from typing import List, Optional

class DatabaseService:
    """Service class for database operations"""
    
    @staticmethod
    def get_today_invoices() -> List[Invoice]:
        """Get all invoices for today"""
        session = get_db_session()
        today = date.today()
        invoices = session.query(Invoice).filter(
            func.date(Invoice.issue_date) == today
        ).all()
        session.close()
        return invoices
    
    @staticmethod
    def get_recent_invoices(limit: int = 10) -> List[Invoice]:
        """Get recent invoices"""
        session = get_db_session()
        invoices = session.query(Invoice).order_by(
            Invoice.issue_date.desc()
        ).limit(limit).all()
        session.close()
        return invoices
    
    @staticmethod
    def get_products_with_stock() -> List[Product]:
        """Get products that have stock"""
        session = get_db_session()
        products = session.query(Product).filter(
            Product.stock_quantity > 0
        ).order_by(Product.product_name).all()
        session.close()
        return products
    
    @staticmethod
    def search_products(search_term: str) -> List[Product]:
        """Search products by name or code"""
        session = get_db_session()
        products = session.query(Product).filter(
            (Product.product_name.contains(search_term)) |
            (Product.product_code.contains(search_term))
        ).order_by(Product.product_name).all()
        session.close()
        return products
    
    @staticmethod
    def check_product_code_exists(code: str, exclude_id: Optional[int] = None) -> bool:
        """Check if product code already exists"""
        session = get_db_session()
        query = session.query(Product).filter(Product.product_code == code)
        if exclude_id:
            query = query.filter(Product.id != exclude_id)
        exists = query.first() is not None
        session.close()
        return exists