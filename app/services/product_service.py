from typing import List, Optional
from sqlalchemy.orm import Session
from app.models import Product
from app.schemas import ProductResponse, PaginatedProductResponse, PaginationInfo

class ProductService:
    @staticmethod
    def get_products_paginated(
        db: Session, 
        page: int = 1, 
        limit: int = 10
    ) -> PaginatedProductResponse:
        offset = (page - 1) * limit
        
        products = db.query(Product).offset(offset).limit(limit).all()
        total_count = db.query(Product).count()
        
        total_pages = (total_count + limit - 1) // limit
        
        return PaginatedProductResponse(
            products=products,
            pagination=PaginationInfo(
                current_page=page,
                total_pages=total_pages,
                total_products=total_count,
                products_per_page=limit
            )
        )
    
    @staticmethod
    def search_products(
        db: Session,
        brand: Optional[str] = None,
        color: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None
    ) -> List[Product]:
        query = db.query(Product)
        
        if brand:
            query = query.filter(Product.brand.ilike(f"%{brand}%"))
        if color:
            query = query.filter(Product.color.ilike(f"%{color}%"))
        if min_price is not None:
            query = query.filter(Product.price >= min_price)
        if max_price is not None:
            query = query.filter(Product.price <= max_price)
        return query.all()
    
    @staticmethod
    def get_product_by_sku(db: Session, sku: str) -> Optional[Product]:
        return db.query(Product).filter(Product.sku == sku).first()
    
    @staticmethod
    def clear_all_products(db: Session) -> dict:
        deleted_count = db.query(Product).count()
        db.query(Product).delete()
        db.commit()
        return {"message": f"Deleted {deleted_count} products from database"}