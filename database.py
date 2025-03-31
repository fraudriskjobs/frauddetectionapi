# In your database.py or main.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Use Render's environment variable
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")  # Render auto-injects this

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
        
