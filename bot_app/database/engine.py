from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from bot_app.core.config import settings


engine = create_async_engine(settings.database_url, echo=True)
session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session():
    """Asynchronous session generator."""
    async with session_maker() as session:
        yield session
