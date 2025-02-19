from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.endpoints.models import UserModel
from app.database.schemas import UserSchemas
from app.config.config import session_maker

# Функция получения пользователя по id
async def get_user(user_id: int) -> UserSchemas | None:
    async with session_maker.begin() as session:
        return await session.get(UserSchemas, user_id)


# Проверяет, существует ли пользователь в базе данных по имени пользователя и паролю
async def get_user_by_name(username: str) -> UserSchemas:
    async with session_maker.begin() as session:
        stmt = select(UserSchemas).where(UserSchemas.username == username)
        result = await session.execute(stmt)
        return result.scalars().first()


# Функция добавления пользователя в БД
async def create_user(user_input: UserModel) -> UserSchemas:
    async with session_maker.begin() as session:
        user = UserSchemas(**user_input.model_dump())
        session.add(user)
        await session.commit()
        return user


# Функция удаления пользователя
async def delete_user(user: UserSchemas) -> None:
    async with session_maker.begin() as session:
        await session.delete(user)
        await session.commit()