import os
from pathlib import Path

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()
BASE_DIR = Path(__file__).parent.parent.parent


class Setting(BaseSettings):
    database_url: str = f"sqlite+aiosqlite:///{BASE_DIR}/database/database.db"
    database_echo: bool = False

    SECRET_KEY: str = os.getenv('SECRET_KEY')
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


setting = Setting()
engine = create_async_engine(url=setting.database_url, echo=setting.database_echo)
session_maker = async_sessionmaker(engine, expire_on_commit=False)