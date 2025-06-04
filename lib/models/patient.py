from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from . import Base

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    patient_no = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    diagnosis = Column(String, nullable=False)
    doctor = Column(String, nullable=False)

    dosages = relationship("Dosage", back_populates="patient")

