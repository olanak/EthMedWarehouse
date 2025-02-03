from sqlalchemy.orm import Session
from api.models import DimProduct, FactMedical
from api.schemas import ProductCreate, FactMedicalCreate

# Product CRUD
def get_product(db: Session, product_id: int):
    return db.query(DimProduct).filter(DimProduct.product_id == product_id).first()

def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(DimProduct).offset(skip).limit(limit).all()

def create_product(db: Session, product: ProductCreate):
    db_product = DimProduct(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# FactMedical CRUD
def create_fact_medical(db: Session, fact: FactMedicalCreate):
    db_fact = FactMedical(**fact.dict())
    db.add(db_fact)
    db.commit()
    db.refresh(db_fact)
    return db_fact