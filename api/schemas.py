from pydantic import BaseModel
from typing import Optional

# Schemas for DimProduct
class ProductBase(BaseModel):
    product_name: str
    category: Optional[str] = None
    brand: Optional[str] = None
    detected_label: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    product_id: int

    class Config:
        orm_mode = True

# Schemas for FactMedical
class FactMedicalBase(BaseModel):
    product_id: int
    price: float
    quantity: int

class FactMedicalCreate(FactMedicalBase):
    pass

class FactMedical(FactMedicalBase):
    fact_id: int
    scraped_at: str

    class Config:
        orm_mode = True