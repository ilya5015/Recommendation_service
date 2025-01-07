from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

import os
from dotenv import load_dotenv

load_dotenv()

database_url = os.getenv('DATABASE_URL')
redis_host = os.getenv('REDIS_HOST')
redis_port = os.getenv('REDIS_PORT')

class RunConfig(BaseModel):
    host: str = "localhost"
    port: int = 8000

class DatabaseConfig(BaseModel):
    redis_host: str = redis_host
    redis_port: int = redis_port
    database_url: str = database_url

class Settings(BaseSettings):
    db: DatabaseConfig = DatabaseConfig()
    run: RunConfig = RunConfig()

settings = Settings()
