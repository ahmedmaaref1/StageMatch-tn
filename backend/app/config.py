import os 
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "StageMatch TN"
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://stagematch:stagematch123@localhost:5432/stagematch_db"
    )
    class Config:
        env_file = ".env"
settings = Settings()