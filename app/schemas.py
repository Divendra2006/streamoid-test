from pydantic import BaseModel, ConfigDict
from typing import Optional, List

class ProductBase(BaseModel):
    sku: str
    name: str
    brand: str
    color: Optional[str] = None
    size: Optional[str] = None
    mrp: float
    price: float
    quantity: int = 0

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int

class PaginationInfo(BaseModel):
    current_page: int
    total_pages: int
    total_products: int
    products_per_page: int

class PaginatedProductResponse(BaseModel):
    products: List[ProductResponse]
    pagination: PaginationInfo