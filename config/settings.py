import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class AppConfig:
    """
    App Configuration.
    """

    class _AppConfig(BaseModel):
        bot_token: str
        web_app_tg_secret: str
        web_app_host: str
        web_app_port: int
        web_app_domain: str
        web_app_hook: str
        bratwa_token: str
        debug: bool

    config = _AppConfig(
        bot_token=os.getenv("BOT_TOKEN"),
        web_app_tg_secret =os.getenv("WEB_APP_TG_SECRET"),
        web_app_host=os.getenv("WEB_APP_HOST"),
        web_app_port=int(os.getenv("WEB_APP_PORT", 0)),
        web_app_domain=os.getenv("WEB_APP_DOMAIN"),
        web_app_hook=os.getenv("WEB_APP_WEBHOOK"),
        bratwa_token=os.getenv("BRATWA_TOKEN"),
        debug=os.getenv("DEBUG") in ["1", "True", "true"],
    )

    @classmethod
    def get_config(cls) -> _AppConfig:
        """
        Get the App configuration.
        """

        return cls.config


class RedisConfig:
    """
    App Configuration.
    """

    class _RedisConfig(BaseModel):
        host: str
        port: int
        db: int
        password: Optional[str]

    config = _RedisConfig(
        host=os.getenv("REDIS_HOST"),
        port=int(os.getenv("REDIS_PORT")),
        password=os.getenv("REDIS_PASS"),
        db=1
    )

    @classmethod
    def get_config(cls) -> _RedisConfig:
        """
        Get the Redis configuration.
        """

        return cls.config



class TGServiceConfig:
    """
    Telegram notificaton config
    """

    class _BaseConfig(BaseModel):
        chat_id: int

    config = _BaseConfig(chat_id=int(os.getenv("NOTIFICATION_CHAT_ID")))

    @classmethod
    def get_config(cls) -> _BaseConfig:
        """
        Get TeleNoti config
        """
        return cls.config


# -------------------------
# --- Database Settings ---
# -------------------------

DATABASES = {
    "drivername": "postgresql",
    "username": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
    "host": os.getenv("DB_HOST"),
    "database": os.getenv("DB_NAME"),
    "port": os.getenv("DB_PORT"),
}

# ----------------------
# --- Cors Settings ---
# ----------------------

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS").split(" ")

# ----------------------
# --- Media Settings ---
# ----------------------

BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_DIR = BASE_DIR / "media"

# Ensure the "media" directory exists
MEDIA_DIR.mkdir(parents=True, exist_ok=True)

# int number as MB
MAX_FILE_SIZE = 50

MAX_WORKERS = 40
MAX_USER_TASKS = 1
# int number as currency RUB 
PRICE_PER_CARD = 50

TIMEZONE = "Europe/Moscow"