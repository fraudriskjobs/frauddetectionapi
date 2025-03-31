from pydantic import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    POSTGRES_PORT: str
    POSTGRES_DB: str
    
    class Config:
        env_file = ".env"

settings = Settings()