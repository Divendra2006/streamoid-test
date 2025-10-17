import pytest
import pandas as pd
import io
from app.services.csv_service import CSVService


class TestCSVServiceUnit:
    """Unit tests for CSV service that don't require database."""

    def test_parse_csv_valid(self):
        """Test parsing valid CSV content."""
        csv_content = """sku,name,brand,color,size,mrp,price,quantity
TEST001,Test Product 1,TestBrand,Blue,M,1000,800,10
TEST002,Test Product 2,TestBrand,Red,L,2000,1500,20"""
        
        content = csv_content.encode('utf-8')
        df = CSVService.parse_csv(content)
        
        assert len(df) == 2
        assert list(df.columns) == ['sku', 'name', 'brand', 'color', 'size', 'mrp', 'price', 'quantity']
        assert df.iloc[0]['sku'] == 'TEST001'
        assert df.iloc[0]['name'] == 'Test Product 1'

    def test_validate_row_valid(self):
        """Test validation of valid product row."""
        row = pd.Series({
            'sku': 'TEST001',
            'name': 'Test Product',
            'brand': 'TestBrand',
            'color': 'Blue',
            'size': 'M',
            'mrp': 1000.0,
            'price': 800.0,
            'quantity': 10
        })
        
        errors = CSVService.validate_row(row, 0)
        assert errors == []

    def test_validate_row_missing_required_fields(self):
        """Test validation with missing required fields."""
        row = pd.Series({
            'sku': 'TEST001',
            'name': '',  
            'brand': 'TestBrand',
            'mrp': 1000.0,
            'quantity': 10
        })
        
        errors = CSVService.validate_row(row, 0)
        assert len(errors) == 2  # name, price
        assert "Missing required field: name" in errors
        assert "Missing required field: price" in errors

    def test_validate_row_price_greater_than_mrp(self):
        """Test validation when price > MRP."""
        row = pd.Series({
            'sku': 'TEST001',
            'name': 'Test Product',
            'brand': 'TestBrand',
            'color': 'Blue',
            'size': 'M',
            'mrp': 1000.0,
            'price': 1200.0, 
            'quantity': 10
        })
        
        errors = CSVService.validate_row(row, 0)
        assert "Price must be less than or equal to MRP" in errors

    def test_validate_row_negative_quantity(self):
        """Test validation with negative quantity."""
        row = pd.Series({
            'sku': 'TEST001',
            'name': 'Test Product',
            'brand': 'TestBrand',
            'color': 'Blue',
            'size': 'M',
            'mrp': 1000.0,
            'price': 800.0,
            'quantity': -5  # Negative quantity
        })
        
        errors = CSVService.validate_row(row, 0)
        assert "Quantity must be greater than or equal to 0" in errors

    def test_create_product_data(self):
        """Test creation of product data dictionary."""
        row = pd.Series({
            'sku': 'TEST001',
            'name': 'Test Product',
            'brand': 'TestBrand',
            'color': 'Blue',
            'size': 'M',
            'mrp': 1000.0,
            'price': 800.0,
            'quantity': 10
        })
        
        product_data = CSVService._create_product_data(row)
        
        assert product_data['sku'] == 'TEST001'
        assert product_data['name'] == 'Test Product'
        assert product_data['brand'] == 'TestBrand'
        assert product_data['color'] == 'Blue'
        assert product_data['size'] == 'M'
        assert product_data['mrp'] == 1000.0
        assert product_data['price'] == 800.0
        assert product_data['quantity'] == 10

    def test_create_product_data_with_missing_optional_fields(self):
        """Test creation of product data with missing optional fields."""
        row = pd.Series({
            'sku': 'TEST001',
            'name': 'Test Product',
            'brand': 'TestBrand',
            'color': 'Blue',
            'size': 'M',
            'mrp': 1000.0,
            'price': 800.0
        })
        
        product_data = CSVService._create_product_data(row)
        
        assert product_data['quantity'] == 0
        assert product_data['color'] == 'Blue'
        assert product_data['size'] == 'M'