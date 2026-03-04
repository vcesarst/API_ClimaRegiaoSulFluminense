# app/core/config.py
from pydantic import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    """Configurações do projeto"""
    OPENWEATHER_API_KEY: str = os.getenv("OPENWEATHER_API_KEY", "")
    
    # Configurações da API
    PROJECT_NAME: str = "API Clima Sul Fluminense"
    VERSION: str = "1.0.0"
    
    # Região de interesse
    LAT_MIN: float = -23.5
    LAT_MAX: float = -22.0
    LON_MIN: float = -45.0
    LON_MAX: float = -43.5
    
    class Config:
        env_file = ".env"

settings = Settings()