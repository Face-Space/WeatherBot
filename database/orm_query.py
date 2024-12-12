from aiogram import types
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User


async def orm_add_user(message: types.Message, session: AsyncSession):
    session.add(User(
        user_id=message.from_user.id,
        state="yes"
    ))
    await session.commit()


async def orm_get_user(session: AsyncSession, user_id: int):
    query = select(User).where(User.user_id == user_id)
    result = await session.execute(query)
    return result.scalar()


async def orm_delete_user(session: AsyncSession, user_id: int):
    query = delete(User).where(User.user_id == user_id)
    await session.execute(query)
    await session.commit()
