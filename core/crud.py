from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from models import UserModel
from .schemas import UserSchemas


# Функция получения пользователя по id
async def get_user(session: AsyncSession, user_id: int) -> UserSchemas | None:
    return await session.get(UserSchemas, user_id)


# Функция добавления юзера в БД
async def create_user(session: AsyncSession, user_input: UserModel) -> UserSchemas:
    user = UserSchemas(**user_input.model_dump())
    session.add(user)
    await session.commit()
    return user


# Функция удаления юзера
async def delete_user(
        session: AsyncSession,
        user: UserSchemas,
) -> None:
    await session.delete(user)
    await session.commit()