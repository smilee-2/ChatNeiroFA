from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent


class Setting(BaseSettings):

    database_url: str = f"sqlite+aiosqlite:///{BASE_DIR}/DB/database.db"
    database_echo: bool = False


setting = Setting()
