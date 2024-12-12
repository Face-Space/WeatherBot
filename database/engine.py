import os

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from database.models import Base


engine = create_async_engine(os.getenv('DB_LITE'), echo=True)
# echo=True означает, что все запросы будут выводится в терминал

session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
# с session_maker беруться сессии, чтобы делать запросы в БД
# class_=AsyncSession - здесь передаём специальный класс, чтобы указать асинхронный класс создания сессий
# expire_on_commit=False - это нужно чтобы возпользоваться сессией повторно после коммита


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

