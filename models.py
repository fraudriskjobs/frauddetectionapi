from sqlalchemy import Column, Integer, String, Float, DateTime, func
from database import Base

class FraudAssessment(Base):
    __tablename__ = "fraud_assessments"
    
    id = Column(Integer, primary_key=True, index=True)
    ip_address = Column(String(45), index=True)
    email = Column(String(255), index=True)
    transaction_amount = Column(Float)
    location = Column(String(100))
    phone_number = Column(String(50))
    risk_score = Column(Integer)
    risk_level = Column(String(20))
    created_at = Column(DateTime(timezone=True), server_default=func.now())