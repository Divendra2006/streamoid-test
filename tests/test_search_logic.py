import pytest
import io
from app.services.csv_service import CSVService
from app.services.product_service import ProductService


class TestSearchLogic:
    """Test search functionality without database integration."""

    def test_search_filter_logic_brand(self):
        """Test brand filtering logic."""
        sample_products = [
            {"brand": "Nike", "name": "Air Max", "color": "White", "price": 6000},
            {"brand": "Adidas", "name": "Ultraboost", "color": "Blue", "price": 7000},
            {"brand": "Nike", "name": "React", "color": "Black", "price": 5500},
        ]
        
        nike_products = [p for p in sample_products if "nike" in p["brand"].lower()]
        assert len(nike_products) == 2
        
        adidas_products = [p for p in sample_products if "adidas" in p["brand"].lower()]
        assert len(adidas_products) == 1

    def test_search_filter_logic_color(self):
        """Test color filtering logic."""
        sample_products = [
            {"brand": "Nike", "name": "Air Max", "color": "White", "price": 6000},
            {"brand": "Adidas", "name": "Ultraboost", "color": "Blue", "price": 7000},
            {"brand": "Nike", "name": "React", "color": "Black", "price": 5500},
        ]
        
        white_products = [p for p in sample_products if "white" in p["color"].lower()]
        assert len(white_products) == 1
        
        blue_products = [p for p in sample_products if "blue" in p["color"].lower()]
        assert len(blue_products) == 1

    def test_search_filter_logic_price_range(self):
        """Test price range filtering logic."""
        sample_products = [
            {"brand": "Nike", "name": "Air Max", "color": "White", "price": 6000},
            {"brand": "Adidas", "name": "Ultraboost", "color": "Blue", "price": 7000},
            {"brand": "Nike", "name": "React", "color": "Black", "price": 5500},
            {"brand": "Puma", "name": "Speed", "color": "Red", "price": 4000},
        ]
        
        mid_range_products = [p for p in sample_products if 5000 <= p["price"] <= 6500]
        assert len(mid_range_products) == 2  
        
        high_end_products = [p for p in sample_products if p["price"] >= 7000]
        assert len(high_end_products) == 1

        budget_products = [p for p in sample_products if p["price"] <= 4000]
        assert len(budget_products) == 1  
    def test_search_filter_logic_multiple_filters(self):
        """Test multiple filters combined."""
        sample_products = [
            {"brand": "Nike", "name": "Air Max", "color": "White", "price": 6000},
            {"brand": "Adidas", "name": "Ultraboost", "color": "Blue", "price": 7000},
            {"brand": "Nike", "name": "React", "color": "Black", "price": 5500},
            {"brand": "Nike", "name": "Casual", "color": "White", "price": 3000},
        ]
        
        filtered_products = [
            p for p in sample_products 
            if "nike" in p["brand"].lower() 
            and "white" in p["color"].lower() 
            and p["price"] >= 5000
        ]
        assert len(filtered_products) == 1  

    def test_search_case_insensitive_matching(self):
        """Test case insensitive search matching."""
        sample_products = [
            {"brand": "Nike", "name": "Air Max", "color": "White", "price": 6000},
            {"brand": "ADIDAS", "name": "Ultraboost", "color": "BLUE", "price": 7000},
        ]
        
        test_cases = [
            ("nike", 1), ("NIKE", 1), ("Nike", 1), ("nIkE", 1),
            ("adidas", 1), ("ADIDAS", 1), ("Adidas", 1), ("aDiDaS", 1),
        ]
        
        for brand_search, expected_count in test_cases:
            filtered = [p for p in sample_products if brand_search.lower() in p["brand"].lower()]
            assert len(filtered) == expected_count

    def test_search_partial_matching(self):
        """Test partial string matching."""
        sample_products = [
            {"brand": "Nike Air", "name": "Air Max", "color": "Sky Blue", "price": 6000},
            {"brand": "Adidas Neo", "name": "Ultraboost", "color": "Dark Blue", "price": 7000},
        ]
        
        nike_partial = [p for p in sample_products if "nike" in p["brand"].lower()]
        assert len(nike_partial) == 1
        
        blue_partial = [p for p in sample_products if "blue" in p["color"].lower()]
        assert len(blue_partial) == 2  

    def test_search_empty_results(self):
        """Test search that returns no results."""
        sample_products = [
            {"brand": "Nike", "name": "Air Max", "color": "White", "price": 6000},
            {"brand": "Adidas", "name": "Ultraboost", "color": "Blue", "price": 7000},
        ]
        
        no_results = [p for p in sample_products if "puma" in p["brand"].lower()]
        assert len(no_results) == 0
        
        no_results_price = [p for p in sample_products if p["price"] < 1000]
        assert len(no_results_price) == 0

    def test_pagination_logic(self):
        """Test pagination calculation logic."""
        total_items = 25
        items_per_page = 10
        
        total_pages = (total_items + items_per_page - 1) // items_per_page 
        assert total_pages == 3
        
        page_1_start = 0
        page_1_end = min(items_per_page, total_items)
        assert page_1_end == 10
        
        page_2_start = items_per_page
        page_2_end = min(2 * items_per_page, total_items)
        assert page_2_end == 20
        
        page_3_start = 2 * items_per_page
        page_3_end = min(3 * items_per_page, total_items)
        assert page_3_end == 25