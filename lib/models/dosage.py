from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from . import Base

class Dosage(Base):
    __tablename__ = "dosages"

    id = Column(Integer, primary_key=True, index=True)
    medication_id = Column(Integer, ForeignKey("medications.id"), nullable=False)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    amount = Column(Integer, nullable=False)
    unit = Column(String, nullable=False)
    frequency = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    medication = relationship("Medication", back_populates="dosages")
    patient = relationship("Patient", back_populates="dosages")
