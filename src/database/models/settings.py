from sqlalchemy import update
from sqlalchemy.orm import Mapped, mapped_column

from src.schemas import SettingsSchema
from src.database.connection import Base, async_session_maker


class Settings(Base):
    __tablename__ = 'settings'
    id: Mapped[int] = mapped_column(nullable=False, primary_key=True)
    dynamic_button_count: Mapped[int] = mapped_column(nullable=False)
    welcome_message: Mapped[str] = mapped_column(nullable=False)

    @classmethod
    async def get_settings(cls) -> SettingsSchema:
        async with async_session_maker() as session:
            settings = await session.get(cls, 1)

            return SettingsSchema(
                id=settings.id,
                dynamic_button_count=settings.dynamic_button_count,
                welcome_message=settings.welcome_message
            )

    @classmethod
    async def set_settings(
            cls, dynamic_button_count: int = None,
            dynamic_welcome_message: str = None
    ):
        async with async_session_maker() as session:
            if await session.get(cls, 1):
                if not (dynamic_button_count or dynamic_welcome_message):
                    return
                query = update(cls).where(cls.id == 1)
                if dynamic_button_count:
                    query = query.values(dynamic_button_count=dynamic_button_count)
                if dynamic_welcome_message:
                    query = query.values(
                        dynamic_welcome_message=dynamic_welcome_message)
                await session.execute(
                    query
                )
