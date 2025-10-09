# backend/app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Google Gemini Settings
    GOOGLE_API_KEY: str

    # Azure AI Services Settings
    AZURE_AI_ENDPOINT: str
    AZURE_AI_KEY: str

    # Database Settings
    DATABASE_URL: str

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()