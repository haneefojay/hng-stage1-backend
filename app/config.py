from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    database_hostname: Optional[str] = None
    database_port: Optional[str] = None
    database_password: Optional[str] = None
    database_name: Optional[str] = None
    database_username: Optional[str] = None

    class Config:
        env_file = ".env"


settings = Settings()
