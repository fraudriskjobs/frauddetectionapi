from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import uvicorn

from models import FraudAssessment
from schemas import TransactionCreate, FraudAssessment as FraudAssessmentSchema
from database import get_db, Base, engine
from utils.model_utils import load_model
from utils.data_processing import calculate_risk_score
from config import settings

# Initialize FastAPI
app = FastAPI(title="Fraud Detection API")

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load ML model
model, email_codes, location_codes = load_model()

# Create database tables
Base.metadata.create_all(bind=engine)

@app.post("/fraud-check", response_model=FraudAssessmentSchema)
async def check_fraud(
    transaction: TransactionCreate,
    db: Session = Depends(get_db)
):
    risk_score, risk_level = calculate_risk_score(
        transaction, model, email_codes, location_codes
    )
    
    db_assessment = FraudAssessment(
        **transaction.dict(),
        risk_score=risk_score,
        risk_level=risk_level
    )
    
    db.add(db_assessment)
    db.commit()
    db.refresh(db_assessment)
    
    return db_assessment

@app.get("/assessments/", response_model=List[FraudAssessmentSchema])
async def get_assessments(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return db.query(FraudAssessment).offset(skip).limit(limit).all()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=int(settings.API_PORT),
        reload=True
    )