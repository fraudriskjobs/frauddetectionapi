from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TransactionBase(BaseModel):
    ip_address: str
    email: str
    transaction_amount: float
    location: str
    phone_number: str

class TransactionCreate(TransactionBase):
    pass

class FraudAssessment(TransactionBase):
    id: int
    risk_score: int
    risk_level: str
    created_at: datetime
    
    class Config:
        orm_mode = True