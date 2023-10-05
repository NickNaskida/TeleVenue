import os
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class DevSettings(BaseSettings):
    DEBUG: bool = True
    SECRET_KEY: str = "NOT_A_SECRET"

    BOT_TOKEN: str
    FRONT_BASE_URL: str
    BACK_BASE_URL: str

    SQLALCHEMY_DATABASE_URI: str = 'sqlite+aiosqlite:///' + os.path.join(BASE_DIR, 'db.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False

    # Environment
    model_config = SettingsConfigDict(
        env_file=os.path.join(BASE_DIR, ".env"),
        env_file_encoding='utf-8'
    )


settings = DevSettings()
