# Database models using SQLAlchemy
# File: database/models.py

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Decimal, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_code = Column(String(50), unique=True, nullable=False)
    product_name = Column(String(200), nullable=False)
    purchase_price = Column(Decimal(18, 2), default=0)
    sale_price = Column(Decimal(18, 2), default=0)
    stock_quantity = Column(Integer, default=0)
    unit = Column(String(50), default="عدد")
    
    def __repr__(self):
        return f"<Product(code='{self.product_code}', name='{self.product_name}')>"

class Invoice(Base):
    __tablename__ = 'invoices'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    invoice_number = Column(String(50), unique=True, nullable=False)
    customer_name = Column(String(200), nullable=False)
    issue_date = Column(DateTime, default=datetime.now)
    total_price = Column(Decimal(18, 2), default=0)
    discount = Column(Decimal(18, 2), default=0)
    final_price = Column(Decimal(18, 2), default=0)
    
    # Relationship with invoice items
    items = relationship("InvoiceItem", back_populates="invoice", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Invoice(number='{self.invoice_number}', customer='{self.customer_name}')>"

class InvoiceItem(Base):
    __tablename__ = 'invoice_items'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    invoice_id = Column(Integer, ForeignKey('invoices.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Decimal(18, 2), nullable=False)
    row_total = Column(Decimal(18, 2), nullable=False)
    
    # Relationships
    invoice = relationship("Invoice", back_populates="items")
    product = relationship("Product")
    
    def __repr__(self):
        return f"<InvoiceItem(invoice_id={self.invoice_id}, product_id={self.product_id}, qty={self.quantity})>"

# Database connection and session management
DATABASE_URL = "sqlite:///invoicing.db"
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_database():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

def get_db_session():
    """Get a database session"""
    return SessionLocal()

# File: database/__init__.py
# This file makes the database directory a Python package