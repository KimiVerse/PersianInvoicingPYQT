# Direct SQLite Database Models (No SQLAlchemy)
# File: database/models.py

import sqlite3
import os
from datetime import datetime
from decimal import Decimal
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

# Database path
DATABASE_PATH = "invoicing.db"

@dataclass
class Product:
    """Product data class"""
    id: Optional[int] = None
    product_code: str = ""
    product_name: str = ""
    purchase_price: Decimal = Decimal('0')
    sale_price: Decimal = Decimal('0')
    stock_quantity: int = 0
    unit: str = "عدد"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'product_code': self.product_code,
            'product_name': self.product_name,
            'purchase_price': float(self.purchase_price),
            'sale_price': float(self.sale_price),
            'stock_quantity': self.stock_quantity,
            'unit': self.unit
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Product':
        return cls(
            id=data.get('id'),
            product_code=data.get('product_code', ''),
            product_name=data.get('product_name', ''),
            purchase_price=Decimal(str(data.get('purchase_price', 0))),
            sale_price=Decimal(str(data.get('sale_price', 0))),
            stock_quantity=data.get('stock_quantity', 0),
            unit=data.get('unit', 'عدد')
        )

@dataclass
class Invoice:
    """Invoice data class"""
    id: Optional[int] = None
    invoice_number: str = ""
    customer_name: str = ""
    issue_date: datetime = None
    total_price: Decimal = Decimal('0')
    discount: Decimal = Decimal('0')
    final_price: Decimal = Decimal('0')
    items: List['InvoiceItem'] = None
    
    def __post_init__(self):
        if self.issue_date is None:
            self.issue_date = datetime.now()
        if self.items is None:
            self.items = []
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'invoice_number': self.invoice_number,
            'customer_name': self.customer_name,
            'issue_date': self.issue_date.isoformat() if self.issue_date else None,
            'total_price': float(self.total_price),
            'discount': float(self.discount),
            'final_price': float(self.final_price)
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Invoice':
        issue_date = None
        if data.get('issue_date'):
            try:
                issue_date = datetime.fromisoformat(data['issue_date'])
            except:
                issue_date = datetime.now()
        
        return cls(
            id=data.get('id'),
            invoice_number=data.get('invoice_number', ''),
            customer_name=data.get('customer_name', ''),
            issue_date=issue_date,
            total_price=Decimal(str(data.get('total_price', 0))),
            discount=Decimal(str(data.get('discount', 0))),
            final_price=Decimal(str(data.get('final_price', 0)))
        )

@dataclass
class InvoiceItem:
    """Invoice item data class"""
    id: Optional[int] = None
    invoice_id: Optional[int] = None
    product_id: Optional[int] = None
    quantity: int = 0
    unit_price: Decimal = Decimal('0')
    row_total: Decimal = Decimal('0')
    product: Optional[Product] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'invoice_id': self.invoice_id,
            'product_id': self.product_id,
            'quantity': self.quantity,
            'unit_price': float(self.unit_price),
            'row_total': float(self.row_total)
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'InvoiceItem':
        return cls(
            id=data.get('id'),
            invoice_id=data.get('invoice_id'),
            product_id=data.get('product_id'),
            quantity=data.get('quantity', 0),
            unit_price=Decimal(str(data.get('unit_price', 0))),
            row_total=Decimal(str(data.get('row_total', 0)))
        )

class DatabaseManager:
    """Direct SQLite database manager"""
    
    def __init__(self, db_path: str = DATABASE_PATH):
        self.db_path = db_path
    
    def get_connection(self) -> sqlite3.Connection:
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable dict-like access
        return conn
    
    def create_tables(self) -> bool:
        """Create all database tables"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Products table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    product_code TEXT UNIQUE NOT NULL,
                    product_name TEXT NOT NULL,
                    purchase_price REAL DEFAULT 0,
                    sale_price REAL DEFAULT 0,
                    stock_quantity INTEGER DEFAULT 0,
                    unit TEXT DEFAULT 'عدد'
                )
            """)
            
            # Invoices table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS invoices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    invoice_number TEXT UNIQUE NOT NULL,
                    customer_name TEXT NOT NULL,
                    issue_date TEXT NOT NULL,
                    total_price REAL DEFAULT 0,
                    discount REAL DEFAULT 0,
                    final_price REAL DEFAULT 0
                )
            """)
            
            # Invoice items table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS invoice_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    invoice_id INTEGER NOT NULL,
                    product_id INTEGER NOT NULL,
                    quantity INTEGER NOT NULL,
                    unit_price REAL NOT NULL,
                    row_total REAL NOT NULL,
                    FOREIGN KEY (invoice_id) REFERENCES invoices (id),
                    FOREIGN KEY (product_id) REFERENCES products (id)
                )
            """)
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Error creating tables: {e}")
            return False
    
    # Product methods
    def add_product(self, product: Product) -> bool:
        """Add a new product"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO products (product_code, product_name, purchase_price, sale_price, stock_quantity, unit)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                product.product_code,
                product.product_name,
                float(product.purchase_price),
                float(product.sale_price),
                product.stock_quantity,
                product.unit
            ))
            
            product.id = cursor.lastrowid
            conn.commit()
            conn.close()
            return True
            
        except sqlite3.IntegrityError:
            print(f"Product code {product.product_code} already exists")
            return False
        except Exception as e:
            print(f"Error adding product: {e}")
            return False
    
    def update_product(self, product: Product) -> bool:
        """Update an existing product"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE products 
                SET product_code = ?, product_name = ?, purchase_price = ?, 
                    sale_price = ?, stock_quantity = ?, unit = ?
                WHERE id = ?
            """, (
                product.product_code,
                product.product_name,
                float(product.purchase_price),
                float(product.sale_price),
                product.stock_quantity,
                product.unit,
                product.id
            ))
            
            conn.commit()
            conn.close()
            return cursor.rowcount > 0
            
        except Exception as e:
            print(f"Error updating product: {e}")
            return False
    
    def delete_product(self, product_id: int) -> bool:
        """Delete a product"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
            
            conn.commit()
            conn.close()
            return cursor.rowcount > 0
            
        except Exception as e:
            print(f"Error deleting product: {e}")
            return False
    
    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        """Get product by ID"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
            row = cursor.fetchone()
            
            conn.close()
            
            if row:
                return Product.from_dict(dict(row))
            return None
            
        except Exception as e:
            print(f"Error getting product: {e}")
            return None
    
    def get_products(self, search_term: str = None) -> List[Product]:
        """Get all products or search by term"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            if search_term:
                cursor.execute("""
                    SELECT * FROM products 
                    WHERE product_name LIKE ? OR product_code LIKE ?
                    ORDER BY product_name
                """, (f"%{search_term}%", f"%{search_term}%"))
            else:
                cursor.execute("SELECT * FROM products ORDER BY product_name")
            
            rows = cursor.fetchall()
            conn.close()
            
            return [Product.from_dict(dict(row)) for row in rows]
            
        except Exception as e:
            print(f"Error getting products: {e}")
            return []
    
    def get_products_with_stock(self) -> List[Product]:
        """Get products that have stock"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM products 
                WHERE stock_quantity > 0
                ORDER BY product_name
            """)
            
            rows = cursor.fetchall()
            conn.close()
            
            return [Product.from_dict(dict(row)) for row in rows]
            
        except Exception as e:
            print(f"Error getting products with stock: {e}")
            return []
    
    # Invoice methods
    def add_invoice(self, invoice: Invoice) -> bool:
        """Add a new invoice with items"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Insert invoice
            cursor.execute("""
                INSERT INTO invoices (invoice_number, customer_name, issue_date, total_price, discount, final_price)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                invoice.invoice_number,
                invoice.customer_name,
                invoice.issue_date.isoformat(),
                float(invoice.total_price),
                float(invoice.discount),
                float(invoice.final_price)
            ))
            
            invoice_id = cursor.lastrowid
            invoice.id = invoice_id
            
            # Insert invoice items
            for item in invoice.items:
                cursor.execute("""
                    INSERT INTO invoice_items (invoice_id, product_id, quantity, unit_price, row_total)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    invoice_id,
                    item.product_id,
                    item.quantity,
                    float(item.unit_price),
                    float(item.row_total)
                ))
                
                # Update product stock
                cursor.execute("""
                    UPDATE products 
                    SET stock_quantity = stock_quantity - ?
                    WHERE id = ?
                """, (item.quantity, item.product_id))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Error adding invoice: {e}")
            return False
    
    def get_invoices(self, limit: int = None, date_filter: str = None) -> List[Invoice]:
        """Get invoices with optional limit and date filter"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            query = "SELECT * FROM invoices"
            params = []
            
            if date_filter:
                query += " WHERE DATE(issue_date) = ?"
                params.append(date_filter)
            
            query += " ORDER BY issue_date DESC"
            
            if limit:
                query += " LIMIT ?"
                params.append(limit)
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            conn.close()
            
            return [Invoice.from_dict(dict(row)) for row in rows]
            
        except Exception as e:
            print(f"Error getting invoices: {e}")
            return []
    
    def get_today_invoices(self) -> List[Invoice]:
        """Get today's invoices"""
        today = datetime.now().date().isoformat()
        return self.get_invoices(date_filter=today)
    
    def get_recent_invoices(self, limit: int = 10) -> List[Invoice]:
        """Get recent invoices"""
        return self.get_invoices(limit=limit)
    
    def count_products(self) -> int:
        """Count total products"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM products")
            count = cursor.fetchone()[0]
            
            conn.close()
            return count
            
        except Exception as e:
            print(f"Error counting products: {e}")
            return 0

# Global database manager instance
db_manager = DatabaseManager()

# Convenience functions for compatibility
def create_database() -> bool:
    """Create database tables"""
    try:
        result = db_manager.create_tables()
        if result:
            print("✅ Database tables created successfully!")
        else:
            print("❌ Failed to create database tables")
        return result
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        return False

def test_database_connection() -> bool:
    """Test database connection"""
    try:
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        conn.close()
        print("✅ Database connection test: SUCCESS")
        return True
    except Exception as e:
        print(f"❌ Database connection test: FAILED - {e}")
        return False

def get_db_session():
    """Get database manager (for compatibility)"""
    return db_manager

# For backward compatibility with main_window.py
class MockSession:
    """Mock session for compatibility with existing code"""
    def __init__(self, db_manager):
        self.db = db_manager
    
    def query(self, model_class):
        return MockQuery(model_class, self.db)
    
    def add(self, obj):
        # Handle in commit
        if not hasattr(self, '_pending_objects'):
            self._pending_objects = []
        self._pending_objects.append(obj)
    
    def commit(self):
        if hasattr(self, '_pending_objects'):
            for obj in self._pending_objects:
                if isinstance(obj, Product):
                    self.db.add_product(obj)
                elif isinstance(obj, Invoice):
                    self.db.add_invoice(obj)
            self._pending_objects = []
    
    def close(self):
        pass

class MockQuery:
    """Mock query for compatibility"""
    def __init__(self, model_class, db_manager):
        self.model_class = model_class
        self.db = db_manager
        self._filters = []
        self._order_by = None
        self._limit_val = None
    
    def filter(self, condition):
        self._filters.append(condition)
        return self
    
    def order_by(self, field):
        self._order_by = field
        return self
    
    def limit(self, count):
        self._limit_val = count
        return self
    
    def all(self):
        if self.model_class == Product:
            return self.db.get_products()
        elif self.model_class == Invoice:
            return self.db.get_invoices(limit=self._limit_val)
        return []
    
    def first(self):
        results = self.all()
        return results[0] if results else None
    
    def count(self):
        if self.model_class == Product:
            return self.db.count_products()
        return 0

# Override get_db_session to return mock session
def get_db_session():
    return MockSession(db_manager)