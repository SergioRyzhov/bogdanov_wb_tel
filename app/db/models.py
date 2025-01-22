from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base

Base: DeclarativeMeta = declarative_base()

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    artikul = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    rating = Column(Float, nullable=True)
    stock = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))