from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from api.database import get_db
from api.schemas import Product, ProductCreate, FactMedical, FactMedicalCreate
from api.crud import get_products, create_product, create_fact_medical

app = FastAPI()

# Products Endpoints
@app.post("/products/", response_model=Product)
def create_new_product(product: ProductCreate, db: Session = Depends(get_db)):
    return create_product(db=db, product=product)

@app.get("/products/", response_model=List[Product])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = get_products(db, skip=skip, limit=limit)
    return products

# FactMedical Endpoints
@app.post("/facts/", response_model=FactMedical)
def create_fact(fact: FactMedicalCreate, db: Session = Depends(get_db)):
    return create_fact_medical(db=db, fact=fact)

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Ethiopian Medical Data API"}