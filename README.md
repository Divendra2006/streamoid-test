# Product Management API

A FastAPI backend service for managing product data with CSV upload, validation, and search functionality.

## Features

- **CSV Upload & Validation**: Upload product CSV files with comprehensive data validation
- **Product Listing**: Paginated product listing with metadata
- **Advanced Search**: Filter products by brand, color, and price range
- **Data Persistence**: SQLite database with automatic table creation
- **Interactive API Docs**: Swagger UI and ReDoc documentation

## Requirements

- Python 3.8+
- FastAPI
- SQLAlchemy
- Pandas

## Setup Instructions

### Local Setup

1. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

4. **Access the API:**
   - API Base URL: http://localhost:8000
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Docker Setup

1. **Build and run with Docker:**
   ```bash
   docker-compose up --build
   ```

## API Endpoints

### 1. Upload CSV File
- **POST** `/upload`
- Upload a CSV file with product data and validate each row

**CSV Format:**
```csv
sku,name,brand,mrp,price,quantity,color,description
ST001,Cotton T-Shirt,StreamThreads,1000,800,50,Blue,Comfortable cotton t-shirt
```

**Validation Rules:**
- Required fields: `sku`, `name`, `brand`, `mrp`, `price`
- `price` ≤ `mrp`
- `quantity` ≥ 0
- `sku` must be unique

### 2. List Products
- **GET** `/products`
- Returns paginated list of all products
- Query parameters: `page` (default: 1), `limit` (default: 10, max: 100)

### 3. Search Products
- **GET** `/products/search`
- Filter products by various criteria
- Query parameters:
  - `brand`: Filter by brand name
  - `color`: Filter by color
  - `minPrice`: Minimum price filter
  - `maxPrice`: Maximum price filter

**Examples:**
```
GET /products/search?brand=StreamThreads
GET /products/search?color=Blue
GET /products/search?minPrice=500&maxPrice=2000
```

## Testing

A sample CSV file `sample_products.csv` is included for testing the upload functionality.

## Database

The application uses SQLite database which will be created automatically when you first run the application.