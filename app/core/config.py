from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class RunConfig(BaseModel):
    host: str = "localhost"
    port: int = 8000

class DatabaseConfig(BaseModel):
    redis_host: str = "localhost"  # или "localhost"
    redis_port: int = 6379

class Settings(BaseSettings):
    db: DatabaseConfig = DatabaseConfig()
    run: RunConfig = RunConfig()

settings = Settings()
