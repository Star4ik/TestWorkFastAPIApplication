from pydantic_settings import BaseSettings
from urllib.parse import quote_plus
from pydantic import Field

class Settings(BaseSettings):
    DB_USER: str = Field(..., env="DB_USER")
    DB_PASSWORD: str = Field(..., env="DB_PASSWORD")
    DB_NAME: str = Field(..., env="DB_NAME")
    DB_HOST: str = Field(..., env="DB_HOST")
    DB_PORT: int = Field(..., env="DB_PORT")
    redis_url: str = Field(..., env="REDIS_URL")
    DATABASE_URL: str = Field(..., env="DATABASE_URL")

    model_config = {"env_file": "/app/.env"}

    @property
    def async_database_url(self) -> str:
        pw = quote_plus(self.DB_PASSWORD)
        return f"postgresql+asyncpg://{self.DB_USER}:{pw}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def sync_database_url(self) -> str:
        pw = quote_plus(self.DB_PASSWORD)
        return f"postgresql+psycopg2://{self.DB_USER}:{pw}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()