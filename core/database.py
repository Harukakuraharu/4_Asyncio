from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from core.settings import config
from models.models import Base

async_engine = create_async_engine(config.async_dsn)
async_session = async_sessionmaker(async_engine, expire_on_commit=False)


async def initial_db():
    """Fuction for connect DB"""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
