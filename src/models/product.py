from sqlalchemy import Column, Integer, String, Float
from ..database import Base

class ProductTable(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)