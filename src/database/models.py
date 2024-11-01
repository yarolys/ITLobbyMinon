import enum
from datetime import UTC, datetime

from sqlalchemy import BigInteger, Enum, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Mapped, mapped_column

from src.chemas import UserSchema
from src.config import logger

from src.database.connection import Base, async_session_maker


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(BigInteger, nullable=True, primary_key=True)
    full_name: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.now(UTC)
    )

    @classmethod
    async def add_user(cls, user_id, full_name):
        if await cls.get_user(user_id):
            return
        try:
            async with async_session_maker() as session:
                session.add(cls(id=user_id, full_name=full_name))
                await session.commit()
        except IntegrityError as e:
            logger.error(f'Попытались второй раз добавить пользователя: {e}')

    @classmethod
    async def get_user(cls, user_id: int) -> UserSchema:
        async with async_session_maker() as session:
            user = await session.get(cls, user_id)
            return UserSchema(
                id=user.id,
                full_name=user.full_name,
                created_at=user.created_at
            )

    @classmethod
    async def get_all_users(cls):
        async with async_session_maker() as session:
            users = await session.execute(
                select(cls)
            )
            return users.scalars()


class WelcomeMessage(Base):
    __tablename__ = 'welcome_message'
    id: Mapped[int] = mapped_column(nullable=False, primary_key=True)
    message: Mapped[str] = mapped_column(nullable=False)


class Settings(Base):
    __tablename__ = 'settings'
    id: Mapped[int] = mapped_column(nullable=False, primary_key=True)
    dynamic_button_count: Mapped[int] = mapped_column(nullable=False)


class ButtonType(str, enum.Enum):
    static = 'static'
    dynamic = 'dynamic'


class buttons(Base):
    __tablename__ = 'buttons'
    id: Mapped[int] = mapped_column(nullable=False, primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    url: Mapped[str] = mapped_column(nullable=False)
    type: Mapped[ButtonType] = mapped_column(Enum(ButtonType), nullable=False)

