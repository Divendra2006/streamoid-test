from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.services.product_service import ProductService
from app.schemas import ProductResponse, PaginatedProductResponse

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("", response_model=PaginatedProductResponse)
async def list_products(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Number of products per page"),
    db: Session = Depends(get_db)
):
    return ProductService.get_products_paginated(db, page, limit)


@router.get("/search", response_model=List[ProductResponse])
async def search_products(
    brand: Optional[str] = Query(None, description="Filter by brand"),
    color: Optional[str] = Query(None, description="Filter by color"),
    minPrice: Optional[float] = Query(None, ge=0, description="Minimum price filter"),
    maxPrice: Optional[float] = Query(None, ge=0, description="Maximum price filter"),
    db: Session = Depends(get_db)
):
    return ProductService.search_products(db, brand, color, minPrice, maxPrice)


@router.delete("/clear")
async def clear_all_products(db: Session = Depends(get_db)):
    """Clear all products from database."""
    return ProductService.clear_all_products(db)