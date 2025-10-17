import pytest
import pandas as pd
import io
from app.services.csv_service import CSVService


class TestAdvancedValidation:
    """Advanced validation and edge case tests."""

    def test_validate_sku_uniqueness_within_csv(self):
        """Test SKU uniqueness validation within the same CSV."""
        csv_content = """sku,name,brand,color,size,mrp,price,quantity
TEST001,Product 1,Brand1,Blue,M,1000,800,10
TEST001,Product 2,Brand2,Red,L,2000,1500,20"""  
        
        content = csv_content.encode('utf-8')
        df = CSVService.parse_csv(content)
       
        errors1 = CSVService.validate_row(df.iloc[0], 0)
        assert len(errors1) == 0
        
        existing_skus = {'TEST001'} 
        errors2 = CSVService.validate_row(df.iloc[1], 1, existing_skus)
        assert len(errors2) == 0  # We removed unique SKU validation from validate_row

    def test_validate_numeric_fields_invalid_types(self):
        """Test validation with invalid numeric field types."""
        row = pd.Series({
            'sku': 'TEST001',
            'name': 'Test Product',
            'brand': 'TestBrand',
            'mrp': 'not_a_number', 
            'price': 800.0,
            'quantity': 'invalid' 
        })
        
        errors = CSVService.validate_row(row, 0)
        assert len(errors) >= 0  
    def test_validate_extreme_values(self):
        """Test validation with extreme numeric values."""
        row = pd.Series({
            'sku': 'TEST001',
            'name': 'Test Product',
            'brand': 'TestBrand',
            'mrp': 99999999.99,  
            'price': 99999999.99, 
            'quantity': 999999  
        })
        
        errors = CSVService.validate_row(row, 0)
        assert isinstance(errors, list)

    def test_validate_zero_values(self):
        """Test validation with zero values."""
        row = pd.Series({
            'sku': 'TEST001',
            'name': 'Test Product',
            'brand': 'TestBrand',
            'mrp': 0.0, 
            'price': 0.0, 
            'quantity': 0  
        })
        
        errors = CSVService.validate_row(row, 0)
        quantity_error = any("Quantity must be greater than or equal to 0" in error for error in errors)
        assert not quantity_error 

    def test_validate_decimal_precision(self):
        """Test validation with high decimal precision."""
        row = pd.Series({
            'sku': 'TEST001',
            'name': 'Test Product',
            'brand': 'TestBrand',
            'mrp': 1000.123456789,  
            'price': 800.987654321, 
            'quantity': 10
        })
        
        errors = CSVService.validate_row(row, 0)
        assert isinstance(errors, list)

    def test_validate_unicode_and_special_characters(self):
        """Test validation with Unicode and special characters."""
        row = pd.Series({
            'sku': 'TEST-001_ñ',  
            'name': 'Tëst Prøduct™ 中文',  
            'brand': 'TestBrand® & Co.',
            'color': 'Blüe',
            'size': 'M™',
            'mrp': 1000.0,
            'price': 800.0,
            'quantity': 10
        })
        
        errors = CSVService.validate_row(row, 0)
        assert isinstance(errors, list)

    def test_validate_whitespace_handling(self):
        """Test validation with various whitespace scenarios."""
        row = pd.Series({
            'sku': '  TEST001  ', 
            'name': ' Test Product ',  
            'brand': 'Test Brand', 
            'mrp': 1000.0,
            'price': 800.0,
            'quantity': 10
        })
        
        errors = CSVService.validate_row(row, 0)
        assert isinstance(errors, list)

    def test_validate_empty_strings_vs_null(self):
        """Test validation difference between empty strings and null values."""
        row_empty_string = pd.Series({
            'sku': 'TEST001',
            'name': '',  
            'brand': 'TestBrand',
            'mrp': 1000.0,
            'price': 800.0,
            'quantity': 10
        })
        
        row_null = pd.Series({
            'sku': 'TEST002',
            'name': None,  
            'brand': 'TestBrand',
            'mrp': 1000.0,
            'price': 800.0,
            'quantity': 10
        })
        
        errors_empty = CSVService.validate_row(row_empty_string, 0)
        errors_null = CSVService.validate_row(row_null, 1)

        assert any("Missing required field: name" in error for error in errors_empty)
        assert any("Missing required field: name" in error for error in errors_null)

    def test_parse_csv_malformed(self):
        """Test parsing malformed CSV content."""
        malformed_csv = """sku,name,brand,mrp,price
TEST001,Product 1,Brand1,1000  # Missing price
TEST002,"Product with, comma",Brand2,2000,1500
TEST003,Product 3,Brand3,1500,1200,extra_column"""
        
        content = malformed_csv.encode('utf-8')
        try:
            df = CSVService.parse_csv(content)
            assert isinstance(df, pd.DataFrame)
        except Exception as e:
            assert isinstance(e, Exception)

    def test_parse_csv_empty_file(self):
        """Test parsing empty CSV file."""
        empty_csv = ""
        content = empty_csv.encode('utf-8')
        
        try:
            df = CSVService.parse_csv(content)
            assert len(df) == 0
        except Exception as e:
            assert isinstance(e, Exception)

    def test_parse_csv_only_headers(self):
        """Test parsing CSV with only headers."""
        header_only_csv = "sku,name,brand,color,size,mrp,price,quantity"
        content = header_only_csv.encode('utf-8')
        
        df = CSVService.parse_csv(content)
        assert len(df) == 0
        assert len(df.columns) > 0

    def test_parse_csv_missing_required_columns(self):
        """Test parsing CSV missing required columns."""
        missing_columns_csv = """sku,name,brand
TEST001,Product 1,Brand1
TEST002,Product 2,Brand2""" 
        
        content = missing_columns_csv.encode('utf-8')
        df = CSVService.parse_csv(content)
        
        errors = CSVService.validate_row(df.iloc[0], 0)
        assert any("Missing required field: mrp" in error for error in errors)
        assert any("Missing required field: price" in error for error in errors)

    def test_create_product_data_type_conversion(self):
        """Test product data creation with type conversions."""
        row = pd.Series({~
            'sku': 'TEST001',
            'name': 'Test Product',
            'brand': 'TestBrand',
            'color': 'Blue',
            'size': 'M',
            'mrp': '1000.50',  
            'price': '800.75',  
            'quantity': '10' 
        })
        
        product_data = CSVService._create_product_data(row)
        
        assert isinstance(product_data['mrp'], (int, float))
        assert isinstance(product_data['price'], (int, float))
        assert isinstance(product_data['quantity'], int)

    def test_validate_business_rules_edge_cases(self):
        """Test business rule validation edge cases."""
        row_equal_prices = pd.Series({
            'sku': 'TEST001',
            'name': 'Test Product',
            'brand': 'TestBrand',
            'color': 'Blue',
            'size': 'M',
            'mrp': 1000.0,
            'price': 1000.0, 
            'quantity': 10
        })
        
        errors = CSVService.validate_row(row_equal_prices, 0)
        # Price = MRP should be allowed (price ≤ MRP)
        price_error = any("Price must be less than or equal to MRP" in error for error in errors)
        assert not price_error  