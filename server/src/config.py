import os
import secrets
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class BaseSettings:
    DEBUG = True
    SECRET_KEY = secrets.token_urlsafe(32)

    BOT_TOKEN = "6564109746:AAELai-cCPlj8_Rr7b_6ADpUE8KtOxkSnxA"
    FRONT_BASE_URL = "https://dd94-188-121-217-243.ngrok-free.app"
    BACK_BASE_URL = "https://4f3f-188-121-217-243.ngrok-free.app"

    SQLALCHEMY_DATABASE_URI = 'sqlite+aiosqlite:///' + os.path.join(BASE_DIR, 'db.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    BACKEND_CORS_ORIGINS = [FRONT_BASE_URL]  # Cors origins. Change this to frontend url in production


settings = BaseSettings()
