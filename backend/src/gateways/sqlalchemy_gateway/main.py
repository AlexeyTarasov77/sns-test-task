from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from core.config import app_config
from contextlib import asynccontextmanager

engine = create_async_engine(str(app_config.pg_dsn), echo=True)

session_factory = async_sessionmaker(engine, expire_on_commit=False)


@asynccontextmanager
async def get_session():
    async with session_factory() as session:
        async with session:
            yield session
            await session.commit()
