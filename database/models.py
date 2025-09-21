"""
Database models for Persian Invoicing System
Enhanced with proper decimal handling and Persian date support
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.types import TypeDecorator, DECIMAL
from datetime import datetime
import jdatetime

Base = declarative_base()

class PersianDecimal(TypeDecorator):
    """Custom decimal type that handles Persian numbers and ensures integer storage"""
    impl = Integer
    
    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        # Convert to integer (remove decimal parts for Iranian currency)
        if isinstance(value, (int, float)):
            return int(value)
        # Handle string input
        if isinstance(value, str):
            # Remove commas and convert Persian digits
            value = value.replace(',', '').replace('٬', '')
            persian_digits = '۰۱۲۳۴۵۶۷۸۹'
            arabic_digits = '٠١٢٣٤٥٦٧٨٩'
            english_digits = '0123456789'
            
            for i, persian_digit in enumerate(persian_digits):
                value = value.replace(persian_digit, english_digits[i])
            for i, arabic_digit in enumerate(arabic_digits):
                value = value.replace(arabic_digit, english_digits[i])
            
            try:
                return int(float(value))
            except (ValueError, TypeError):
                return 0
        return int(value) if value else 0
    
    def process_result_value(self, value, dialect):
        return value if value is not None else 0

class User(Base):
    """User authentication model"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    is_active = Column(Boolean, default=True)

class Product(Base):
    """Product inventory model with enhanced validation"""
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    # Removed code field as requested
    purchase_price = Column(PersianDecimal, default=0, nullable=False)
    sale_price = Column(PersianDecimal, default=0, nullable=False)
    stock_quantity = Column(Integer, default=0, nullable=False)
    # Removed unit field as requested - all items are counted as numbers
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    is_active = Column(Boolean, default=True)
    
    # Relationship with invoice items
    invoice_items = relationship("InvoiceItem", back_populates="product")
    
    def __repr__(self):
        return f"<Product(name='{self.name}', sale_price={self.sale_price})>"
    
    @property
    def formatted_sale_price(self):
        """Return formatted price with thousand separators"""
        return f"{self.sale_price:,} تومان"
    
    @property
    def formatted_purchase_price(self):
        """Return formatted purchase price with thousand separators"""
        return f"{self.purchase_price:,} تومان"

class Invoice(Base):
    """Invoice model with Persian date support"""
    __tablename__ = 'invoices'
    
    id = Column(Integer, primary_key=True)
    invoice_number = Column(String(50), unique=True, nullable=False)
    customer_name = Column(String(200), nullable=False)
    customer_phone = Column(String(20))
    customer_address = Column(Text)
    issue_date = Column(DateTime, default=datetime.now)
    total_amount = Column(PersianDecimal, default=0)
    discount_amount = Column(PersianDecimal, default=0)
    final_amount = Column(PersianDecimal, default=0)
    notes = Column(Text)
    background_image_path = Column(String(500))  # New field for custom background
    header_text = Column(Text)  # New field for custom header
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    is_active = Column(Boolean, default=True)
    
    # Relationship with invoice items
    items = relationship("InvoiceItem", back_populates="invoice", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Invoice(number='{self.invoice_number}', customer='{self.customer_name}')>"
    
    @property
    def persian_date(self):
        """Return Persian date string"""
        if self.issue_date:
            jdate = jdatetime.datetime.fromgregorian(datetime=self.issue_date)
            return jdate.strftime('%Y/%m/%d')
        return ""
    
    @property
    def formatted_total(self):
        """Return formatted total with thousand separators"""
        return f"{self.final_amount:,} تومان"
    
    @classmethod
    def generate_invoice_number(cls, session):
        """Generate invoice number based on Persian date"""
        now = datetime.now()
        jdate = jdatetime.datetime.fromgregorian(datetime=now)
        
        # Format: INV-YYYYMMDD-NNNN
        date_part = jdate.strftime('%Y%m%d')
        
        # Find last invoice for today
        prefix = f"INV-{date_part}-"
        last_invoice = session.query(cls).filter(
            cls.invoice_number.like(f"{prefix}%")
        ).order_by(cls.invoice_number.desc()).first()
        
        if last_invoice:
            # Extract sequence number
            last_sequence = int(last_invoice.invoice_number.split('-')[-1])
            new_sequence = last_sequence + 1
        else:
            new_sequence = 1
        
        return f"{prefix}{new_sequence:04d}"

class InvoiceItem(Base):
    """Invoice item model with automatic stock management"""
    __tablename__ = 'invoice_items'
    
    id = Column(Integer, primary_key=True)
    invoice_id = Column(Integer, ForeignKey('invoices.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    unit_price = Column(PersianDecimal, nullable=False)
    total_price = Column(PersianDecimal, nullable=False)
    
    # Relationships
    invoice = relationship("Invoice", back_populates="items")
    product = relationship("Product", back_populates="invoice_items")
    
    def __repr__(self):
        return f"<InvoiceItem(product_id={self.product_id}, quantity={self.quantity})>"
    
    @property
    def formatted_total(self):
        """Return formatted total with thousand separators"""
        return f"{self.total_price:,} تومان"

class Settings(Base):
    """Application settings model"""
    __tablename__ = 'settings'
    
    id = Column(Integer, primary_key=True)
    key = Column(String(100), unique=True, nullable=False)
    value = Column(Text)
    description = Column(String(500))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    @classmethod
    def get_setting(cls, session, key, default=None):
        """Get setting value by key"""
        setting = session.query(cls).filter_by(key=key).first()
        return setting.value if setting else default
    
    @classmethod
    def set_setting(cls, session, key, value, description=None):
        """Set setting value by key"""
        setting = session.query(cls).filter_by(key=key).first()
        if setting:
            setting.value = value
            setting.updated_at = datetime.now()
            if description:
                setting.description = description
        else:
            setting = cls(key=key, value=value, description=description)
            session.add(setting)
        session.commit()
        return setting