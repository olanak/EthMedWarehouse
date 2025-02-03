from sqlalchemy import Column, Integer, String, Float, JSON, ForeignKey, Date
from sqlalchemy.orm import relationship
from api.database import Base

class DimProduct(Base):
    __tablename__ = "dim_product"
    product_id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, unique=True, index=True)
    category = Column(String)
    brand = Column(String)
    detected_label = Column(String)

class FactMedical(Base):
    __tablename__ = "fact_medical"
    fact_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("dim_product.product_id"))
    price = Column(Float)
    quantity = Column(Integer)
    scraped_at = Column(Date)

    product = relationship("DimProduct")