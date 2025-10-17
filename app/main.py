from fastapi import FastAPI
from app.database import engine
from app.models import Base
from app.routers import upload, products

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Product Management API",
    description="A FastAPI service for managing product data with CSV upload, validation, and search functionality",
    version="1.0.0"
)

app.include_router(upload.router)
app.include_router(products.router)

@app.get("/")
async def root():
    return {"message": "Product Management API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)