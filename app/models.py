from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(100), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    brand = Column(String(100), nullable=False, index=True)
    color = Column(String(50), index=True)
    size = Column(String(20))
    mrp = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, default=0)
    
    def __repr__(self):
        return f"<Product(sku='{self.sku}', name='{self.name}', brand='{self.brand}')>"