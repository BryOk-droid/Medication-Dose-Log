from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from . import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    medications = relationship("Medication", back_populates="category")

class Medication(Base):
    __tablename__ = "medications"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    total_stock = Column(Integer, nullable=False)
    threshold = Column(Integer, nullable=False)
    category = relationship("Category", back_populates="medications")
    dosages = relationship("Dosage", back_populates="medication", cascade="all, delete-orphan")
