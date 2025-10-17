import pandas as pd
import io
from typing import List, Dict, Any, Tuple
from sqlalchemy.orm import Session
from app.models import Product


class CSVService:
    REQUIRED_FIELDS = ['sku', 'name', 'brand', 'mrp', 'price']
    @staticmethod
    def parse_csv(file_content: bytes) -> pd.DataFrame:
        try:
            return pd.read_csv(io.StringIO(file_content.decode('utf-8')))
        except Exception as e:
            raise ValueError(f"Invalid CSV format: {str(e)}")
    
    @classmethod
    def validate_row(cls, row: pd.Series, index: int, existing_skus: set = None) -> List[str]:
        errors = []
        
        for field in cls.REQUIRED_FIELDS:
            if field not in row or pd.isna(row[field]) or str(row[field]).strip() == '':
                errors.append(f"Missing required field: {field}")
        
        if 'price' in row and 'mrp' in row and pd.notna(row['price']) and pd.notna(row['mrp']):
            try:
                price = float(row['price'])
                mrp = float(row['mrp'])
                if price > mrp:
                    errors.append("Price must be less than or equal to MRP")
            except (ValueError, TypeError):
                pass
     
        if 'quantity' in row and pd.notna(row['quantity']):
            try:
                quantity = float(row['quantity'])
                if quantity < 0:
                    errors.append("Quantity must be greater than or equal to 0")
            except (ValueError, TypeError):
                pass
        
        return errors
    
    @classmethod
    def process_csv(cls, df: pd.DataFrame, db: Session) -> Dict[str, Any]:
        valid_products = []
        validation_errors = []
        
        for index, row in df.iterrows():
            row_errors = cls.validate_row(row, index)
            
            if row_errors:
                validation_errors.append({"row": index + 1, "errors": row_errors})
            else:
                product_data = cls._create_product_data(row)
                valid_products.append(product_data)
        
        stored_count = cls._store_products(valid_products, db, validation_errors)
        skipped_duplicates = len(valid_products) - stored_count
        
        return {
            "message": "Successfully processed CSV file",
            "total_rows": len(df),
            "valid_products_stored": stored_count,
            "validation_errors_count": len(validation_errors),
            "skipped_duplicates": skipped_duplicates,
            "errors": validation_errors
        }
    
    @staticmethod
    def _create_product_data(row: pd.Series) -> Dict[str, Any]:
        quantity = row.get('quantity', 0)
        try:
            quantity = int(quantity) if pd.notna(quantity) else 0
        except (ValueError, TypeError):
            quantity = 0
        
        return {
            'sku': str(row['sku']).strip(),
            'name': str(row['name']).strip(),
            'brand': str(row['brand']).strip(),
            'color': str(row.get('color', '')).strip() if pd.notna(row.get('color')) else None,
            'size': str(row.get('size', '')).strip() if pd.notna(row.get('size')) else None,
            'mrp': float(row['mrp']),
            'price': float(row['price']),
            'quantity': quantity
        }
    
    @staticmethod
    def _store_products(valid_products: List[Dict[str, Any]], db: Session, errors: List[Dict]) -> int:
        stored_count = 0
        skipped_duplicates = 0
        
        for product_data in valid_products:
            existing_product = db.query(Product).filter(Product.sku == product_data['sku']).first()
            if existing_product:
                # Skip duplicates but don't count as validation errors
                skipped_duplicates += 1
                continue
            
            product = Product(**product_data)
            db.add(product)
            stored_count += 1
        
        db.commit()
        return stored_count