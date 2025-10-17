import pytest
import tempfile
import os


@pytest.fixture
def sample_product_data():
    return {
        "sku": "TEST001",
        "name": "Test Product",
        "brand": "TestBrand",
        "color": "Blue",
        "size": "M",
        "mrp": 1000.0,
        "price": 800.0,
        "quantity": 10
    }


@pytest.fixture
def sample_csv_valid():
    return """sku,name,brand,color,size,mrp,price,quantity
TEST001,Test Product 1,TestBrand,Blue,M,1000,800,10
TEST002,Test Product 2,TestBrand,Red,L,2000,1500,20
TEST003,Test Product 3,AnotherBrand,Green,XL,1500,1200,15"""


@pytest.fixture
def sample_csv_invalid():
    return """sku,name,brand,color,size,mrp,price,quantity
TEST001,Test Product 1,TestBrand,Blue,M,1000,800,10
INVALID001,,TestBrand,Blue,M,1000,800,10
INVALID002,Test Product,TestBrand,Red,L,1000,1200,10
INVALID003,Test Product,TestBrand,Blue,M,1000,800,-5"""


@pytest.fixture
def sample_csv_file(sample_csv_valid):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write(sample_csv_valid)
        f.flush()
        yield f.name
    os.unlink(f.name)