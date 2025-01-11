from os import getenv
from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent


class Setting(BaseSettings):

    database_url: str = f"sqlite+aiosqlite:///{BASE_DIR}/database/database.db"
    database_echo: bool = True


setting = Setting()
