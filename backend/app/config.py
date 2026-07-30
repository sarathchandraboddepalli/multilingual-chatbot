from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://chatbot:changeme@db:5432/multilingual_chatbot"
    ANTHROPIC_API_KEY: str = "your-anthropic-api-key"
    BHASHINI_API_KEY: str = "mock-bhashini-key"
    WHATSAPP_VERIFY_TOKEN: str = "verify-token-change-me"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
