from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    DATABASE_URL: str
    ANTHROPIC_API_KEY: str
    BHASHINI_API_KEY: str = "mock-bhashini-key"
    WHATSAPP_VERIFY_TOKEN: str
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3002"]

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
