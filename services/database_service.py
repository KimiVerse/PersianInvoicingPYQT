"""
Database Service for Persian Invoicing System
Enhanced with proper error handling and validation
"""

import os
import shutil
from datetime import datetime
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from database.models import Base, Product, Invoice, InvoiceItem, User, Settings
import bcrypt
import logging

class DatabaseService:
    """Enhanced database service with improved error handling"""
    
    def __init__(self, db_path="invoicing.db"):
        self.db_path = db_path
        self.engine = create_engine(f'sqlite:///{db_path}', echo=False)
        self.SessionLocal = scoped_session(sessionmaker(bind=self.engine))
        self.setup_logging()
        self.create_tables()
        self.create_default_user()
    
    def setup_logging(self):
        """Setup logging for database operations"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/database.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def create_tables(self):
        """Create all database tables"""
        try:
            os.makedirs('logs', exist_ok=True)
            os.makedirs('backups', exist_ok=True)
            Base.metadata.create_all(self.engine)
            self.logger.info("Database tables created successfully")
        except Exception as e:
            self.logger.error(f"Error creating tables: {e}")
            raise
    
    def create_default_user(self):
        """Create default admin user if no users exist"""
        session = self.SessionLocal()
        try:
            if not session.query(User).first():
                # Default credentials
                default_username = "admin"
                default_password = "admin123"
                
                password_hash = bcrypt.hashpw(
                    default_password.encode('utf-8'), 
                    bcrypt.gensalt()
                ).decode('utf-8')
                
                user = User(
                    username=default_username,
                    password_hash=password_hash
                )
                session.add(user)
                session.commit()
                self.logger.info("Default admin user created")
        except Exception as e:
            session.rollback()
            self.logger.error(f"Error creating default user: {e}")
        finally:
            session.close()
    
    def authenticate_user(self, username, password):
        """Authenticate user with username and password"""
        session = self.SessionLocal()
        try:
            user = session.query(User).filter_by(
                username=username, 
                is_active=True
            ).first()
            
            if user and bcrypt.checkpw(
                password.encode('utf-8'), 
                user.password_hash.encode('utf-8')
            ):
                return True
            return False
        except Exception as e:
            self.logger.error(f"Authentication error: {e}")
            return False
        finally:
            session.close()
    
    def create_user(self, username, password):
        """Create new user"""
        session = self.SessionLocal()
        try:
            # Check if user already exists
            existing_user = session.query(User).filter_by(username=username).first()
            if existing_user:
                return False, "کاربر با این نام کاربری قبلاً ثبت شده است"
            
            password_hash = bcrypt.hashpw(
                password.encode('utf-8'), 
                bcrypt.gensalt()
            ).decode('utf-8')
            
            user = User(username=username, password_hash=password_hash)
            session.add(user)
            session.commit()
            return True, "کاربر با موفقیت ایجاد شد"
        except Exception as e:
            session.rollback()
            self.logger.error(f"Error creating user: {e}")
            return False, f"خطا در ایجاد کاربر: {str(e)}"
        finally:
            session.close()
    
    def add_product(self, name, purchase_price=0, sale_price=0, stock_quantity=0, description=""):
        """Add new product with improved validation"""
        session = self.SessionLocal()
        try:
            # Validate input
            if not name or name.strip() == "":
                return False, "نام کالا الزامی است"
            
            # Check for duplicate names
            existing_product = session.query(Product).filter_by(
                name=name.strip(), 
                is_active=True
            ).first()
            
            if existing_product:
                return False, "کالایی با این نام قبلاً ثبت شده است"
            
            # Ensure prices are integers
            purchase_price = int(float(purchase_price)) if purchase_price else 0
            sale_price = int(float(sale_price)) if sale_price else 0
            stock_quantity = int(stock_quantity) if stock_quantity else 0
            
            product = Product(
                name=name.strip(),
                purchase_price=purchase_price,
                sale_price=sale_price,
                stock_quantity=stock_quantity,
                description=description.strip()
            )
            
            session.add(product)
            session.commit()
            self.logger.info(f"Product added: {name}")
            return True, "کالا با موفقیت اضافه شد"
            
        except Exception as e:
            session.rollback()
            self.logger.error(f"Error adding product: {e}")
            return False, f"خطا در افزودن کالا: {str(e)}"
        finally:
            session.close()
    
    def update_product(self, product_id, name, purchase_price, sale_price, stock_quantity, description=""):
        """Update existing product"""
        session = self.SessionLocal()
        try:
            product = session.query(Product).filter_by(id=product_id, is_active=True).first()
            if not product:
                return False, "کالا یافت نشد"
            
            # Check for duplicate names (excluding current product)
            existing_product = session.query(Product).filter(
                and_(Product.name == name.strip(), 
                     Product.id != product_id,
                     Product.is_active == True)
            ).first()
            
            if existing_product:
                return False, "کالایی با این نام قبلاً ثبت شده است"
            
            # Update fields
            product.name = name.strip()
            product.purchase_price = int(float(purchase_price)) if purchase_price else 0
            product.sale_price = int(float(sale_price)) if sale_price else 0
            product.stock_quantity = int(stock_quantity) if stock_quantity else 0
            product.description = description.strip()
            product.updated_at = datetime.now()
            
            session.commit()
            self.logger.info(f"Product updated: {name}")
            return True, "کالا با موفقیت به‌روزرسانی شد"
            
        except Exception as e:
            session.rollback()
            self.logger.error(f"Error updating product: {e}")
            return False, f"خطا در به‌روزرسانی کالا: {str(e)}"
        finally:
            session.close()
    
    def delete_product(self, product_id):
        """Soft delete product"""
        session = self.SessionLocal()
        try:
            product = session.query(Product).filter_by(id=product_id).first()
            if not product:
                return False, "کالا یافت نشد"
            
            # Check if product is used in any active invoice
            used_in_invoice = session.query(InvoiceItem).join(Invoice).filter(
                and_(InvoiceItem.product_id == product_id,
                     Invoice.is_active == True)
            ).first()
            
            if used_in_invoice:
                return False, "این کالا در فاکتورهای فعال استفاده شده و قابل حذف نیست"
            
            product.is_active = False
            product.updated_at = datetime.now()
            session.commit()
            self.logger.info(f"Product deleted: {product.name}")
            return True, "کالا با موفقیت حذف شد"
            
        except Exception as e:
            session.rollback()
            self.logger.error(f"Error deleting product: {e}")
            return False, f"خطا در حذف کالا: {str(e)}"
        finally:
            session.close()
    
    def get_products(self, search_term="", active_only=True):
        """Get products with search functionality"""
        session = self.SessionLocal()
        try:
            query = session.query(Product)
            
            if active_only:
                query = query.filter(Product.is_active == True)
            
            if search_term:
                search_term = f"%{search_term}%"
                query = query.filter(Product.name.like(search_term))
            
            products = query.order_by(Product.name).all()
            return products
            
        except Exception as e:
            self.logger.error(f"Error getting products: {e}")
            return []
        finally:
            session.close()
    
    def create_invoice(self, customer_name, customer_phone="", customer_address="", 
                      items=None, discount_amount=0, notes="", background_image_path="", header_text=""):
        """Create new invoice with automatic stock management"""
        if items is None:
            items = []
        
        session = self.SessionLocal()
        try:
            # Generate invoice number
            invoice_number = Invoice.generate_invoice_number(session)
            
            # Calculate totals
            total_amount = 0
            invoice_items = []
            
            for item in items:
                product_id = item['product_id']
                quantity = int(item['quantity'])
                
                # Get product and check stock
                product = session.query(Product).filter_by(
                    id=product_id, 
                    is_active=True
                ).first()
                
                if not product:
                    return False, f"کالا با شناسه {product_id} یافت نشد"
                
                if product.stock_quantity < quantity:
                    return False, f"موجودی کالا {product.name} کافی نیست. موجودی فعلی: {product.stock_quantity}"
                
                unit_price = product.sale_price
                total_price = unit_price * quantity
                total_amount += total_price
                
                invoice_items.append({
                    'product_id': product_id,
                    'quantity': quantity,
                    'unit_price': unit_price,
                    'total_price': total_price
                })
            
            # Apply discount
            discount_amount = int(float(discount_amount)) if discount_amount else 0
            final_amount = total_amount - discount_amount
            
            # Create invoice
            invoice = Invoice(
                invoice_number=invoice_number,
                customer_name=customer_name.strip(),
                customer_phone=customer_phone.strip(),
                customer_address=customer_address.strip(),
                total_amount=total_amount,
                discount_amount=discount_amount,
                final_amount=final_amount,
                notes=notes.strip(),
                background_image_path=background_image_path,
                header_text=header_text.strip()
            )
            
            session.add(invoice)
            session.flush()  # Get invoice ID
            
            # Add invoice items and update stock
            for item_data in invoice_items:
                invoice_item = InvoiceItem(
                    invoice_id=invoice.id,
                    **item_data
                )
                session.add(invoice_item)
                
                # Update product stock
                product = session.query(Product).filter_by(id=item_data['product_id']).first()
                product.stock_quantity -= item_data['quantity']
                product.updated_at = datetime.now()
            
            session.commit()
            self.logger.info(f"Invoice created: {invoice_number}")
            return True, f"فاکتور {invoice_number} با موفقیت ایجاد شد"
            
        except Exception as e:
            session.rollback()
            self.logger.error(f"Error creating invoice: {e}")
            return False, f"خطا در ایجاد فاکتور: {str(e)}"
        finally:
            session.close()
    
    def get_invoices(self, search_term="", active_only=True):
        """Get invoices with search functionality"""
        session = self.SessionLocal()
        try:
            query = session.query(Invoice)
            
            if active_only:
                query = query.filter(Invoice.is_active == True)
            
            if search_term:
                search_term = f"%{search_term}%"
                query = query.filter(
                    Invoice.invoice_number.like(search_term) |
                    Invoice.customer_name.like(search_term)
                )
            
            invoices = query.order_by(Invoice.created_at.desc()).all()
            return invoices
            
        except Exception as e:
            self.logger.error(f"Error getting invoices: {e}")
            return []
        finally:
            session.close()
    
    def get_dashboard_stats(self):
        """Get dashboard statistics"""
        session = self.SessionLocal()
        try:
            # Today's stats
            today = datetime.now().date()
            
            today_invoices = session.query(Invoice).filter(
                and_(Invoice.issue_date >= today,
                     Invoice.is_active == True)
            ).count()
            
            today_sales = session.query(Invoice).filter(
                and_(Invoice.issue_date >= today,
                     Invoice.is_active == True)
            ).with_entities(Invoice.final_amount).all()
            
            today_revenue = sum(invoice.final_amount for invoice in today_sales if invoice.final_amount)
            
            # Total stats
            total_products = session.query(Product).filter(Product.is_active == True).count()
            total_invoices = session.query(Invoice).filter(Invoice.is_active == True).count()
            
            # Low stock products
            low_stock_products = session.query(Product).filter(
                and_(Product.stock_quantity <= 5,
                     Product.is_active == True)
            ).count()
            
            return {
                'today_invoices': today_invoices,
                'today_revenue': today_revenue,
                'total_products': total_products,
                'total_invoices': total_invoices,
                'low_stock_products': low_stock_products
            }
            
        except Exception as e:
            self.logger.error(f"Error getting dashboard stats: {e}")
            return {
                'today_invoices': 0,
                'today_revenue': 0,
                'total_products': 0,
                'total_invoices': 0,
                'low_stock_products': 0
            }
        finally:
            session.close()
    
    def backup_database(self):
        """Create database backup"""
        try:
            backup_filename = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
            backup_path = os.path.join('backups', backup_filename)
            shutil.copy2(self.db_path, backup_path)
            self.logger.info(f"Database backup created: {backup_path}")
            return True, f"پشتیبان در مسیر {backup_path} ایجاد شد"
        except Exception as e:
            self.logger.error(f"Error creating backup: {e}")
            return False, f"خطا در ایجاد پشتیبان: {str(e)}"
    
    def close(self):
        """Close database connection"""
        try:
            self.SessionLocal.remove()
            self.engine.dispose()
        except Exception as e:
            self.logger.error(f"Error closing database: {e}")