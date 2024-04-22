from typing import List

from sqlalchemy import Boolean, Integer, String, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import (DeclarativeBase, Mapped, declared_attr,
                            make_transient, mapped_column)

from bot_app.core.config import settings

USER = ('{name} '
        '{last_name}\n'
        '{email}\n'
        '{is_active}'
        '{is_admin}\n')


class Base(DeclarativeBase):
    """Base model."""
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, nullable=False
    )

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


class User(Base):
    """User model."""
    tg_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True
    )
    name: Mapped[str] = mapped_column(
        String(150), nullable=False
    )
    last_name: Mapped[str] = mapped_column(
        String(150), nullable=False
    )
    email: Mapped[str] = mapped_column(
        String(150), nullable=False, unique=True
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True
    )
    is_admin: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )
    is_sent: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )

    def __repr__(self):
        is_admin_text = ', админ' if self.is_admin else ''
        is_active_text = 'активен' if self.is_active else 'неактивен'
        return USER.format(
            name=self.name,
            last_name=self.last_name,
            email=self.email,
            is_active=is_active_text,
            is_admin=is_admin_text,
        )

    @staticmethod
    async def create(session: AsyncSession, data: dict):
        """Creating object."""
        session.add(User(**data))
        result = await session.execute(
            select(User).filter(User.tg_id == settings.gen_admin_id)
        )
        user = result.scalars().one_or_none()
        if user:
            user.is_admin = True
        await session.commit()

    @staticmethod
    async def remove(session: AsyncSession, db_obj):
        """Deleting object."""
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    @staticmethod
    async def get(session: AsyncSession, tg_id: int):
        """Getting object by tg_id."""
        db_obj = await session.execute(select(User).where(User.tg_id == tg_id))
        return db_obj.scalars().one_or_none()

    @staticmethod
    async def get_by_email(session: AsyncSession, email: str):
        """Getting object by email."""
        db_obj = await session.execute(select(User).where(User.email == email))
        return db_obj.scalars().one_or_none()

    @staticmethod
    async def get_all(session: AsyncSession):
        """Getting all objects."""
        users = await session.execute(select(User))
        return users.scalars().all()

    @staticmethod
    async def deactivate_user(session: AsyncSession, email: str):
        """Deactivating object."""
        result = await session.execute(
            select(User).filter(User.email == email)
        )
        user = result.scalars().one_or_none()
        if user is not None:
            user.is_active = False if user.is_active else user.is_active
            await session.commit()
            return True
        return False

    @staticmethod
    async def activate_user(session: AsyncSession, email: str):
        """Activating user."""
        result = await session.execute(
            select(User).filter(User.email == email)
        )
        user = result.scalars().one_or_none()
        if user is not None:
            user.is_active = True if not user.is_active else user.is_active
            await session.commit()
            return True
        return False

    @staticmethod
    async def get_all_activated(session: AsyncSession):
        """Getting all active objects."""
        result = await session.execute(
            select(User).filter(User.is_active == 1)
        )
        return result.scalars().all()

    @staticmethod
    async def get_all_is_sent(session: AsyncSession):
        """Receiving all objects to whom the mailing with couples was sent."""
        result = await session.execute(select(User).filter(User.is_sent == 1))
        return result.scalars().all()

    @staticmethod
    async def first_to_end_db(user, session: AsyncSession):
        """Moving thirst user to last position in table."""
        await User.remove(session, user)
        user.id = None
        session.expunge(user)
        make_transient(user)
        session.add(user)
        await session.commit()

    @staticmethod
    async def set_is_sent_status_true(users: List,
                                      session: AsyncSession):
        """Changing is_sent status to True."""
        if len(users) > 0:
            for user in users:
                user.is_sent = True if not user.is_sent else user.is_sent
            await session.commit()

    @staticmethod
    async def set_is_sent_status_false(users: List,
                                       session: AsyncSession):
        """Changing is_sent status to False."""
        if len(users) > 0:
            for user in users:
                user.is_sent = False if user.is_sent else user.is_sent
            await session.commit()
