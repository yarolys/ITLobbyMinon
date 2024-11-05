import os

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('SQLALCHEMY_URL')
engine = create_async_engine(DATABASE_URL)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)  # noqa
metadata = MetaData()


class Base(DeclarativeBase):
    """Базовый класс, от которого наследуются все модели SQLAlchemy."""
    pass
