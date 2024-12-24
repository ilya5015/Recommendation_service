from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class RunConfig(BaseModel):
    host: str = "localhost"
    port: int = 8000

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP__",
    )
    run: RunConfig = RunConfig()

settings = Settings()
