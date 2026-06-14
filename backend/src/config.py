from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://appuser:apppassword@db:5432/appdb"
    app_env: str = "development"

    class Config:
        env_file = ".env"


settings = Settings()
