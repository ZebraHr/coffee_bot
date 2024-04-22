from aiogram import Bot, types
from aiogram.filters import Filter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot_app.core.config import settings
from bot_app.database.models import User


class IsAdmin(Filter):
    """Filter for admin."""
    def __init__(self) -> None:
        pass

    async def __call__(self, message: types.Message, bot: Bot,
                       session: AsyncSession) -> bool:

        if message.from_user.id == settings.gen_admin_id:
            return True
        result = await session.execute(
            select(User).filter(User.tg_id == message.from_user.id)
        )
        user = result.scalars().one_or_none()
        if user is not None and user.is_admin:
            return True
        else:
            return False
