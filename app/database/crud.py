from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.endpoints.models import UserModel
from app.database.schemas import UserSchemas


# Функция получения пользователя по id
async def get_user(session: AsyncSession, user_id: int) -> UserSchemas | None:
    return await session.get(UserSchemas, user_id)


# Проверяет, существует ли пользователь в базе данных по имени пользователя и паролю
async def user_exists_by_name(session: AsyncSession, username: str, password: str) -> bool:
    stmt = select(UserSchemas).where(UserSchemas.username == username, UserSchemas.password == password)
    result = await session.execute(stmt)
    return result.scalars().first() is not None


# # Проверяет, существует ли пароль пользователя в базе данных по имени пользователя
# async def user_exists_by_password(session: AsyncSession, password: str) -> bool:
#     stmt = select(UserSchemas).where(UserSchemas.password == password)
#     result = await session.execute(stmt)
#     return result.scalars().first() is not None


# Функция добавления пользователя в БД
async def create_user(session: AsyncSession, user_input: UserModel) -> UserSchemas:
    user = UserSchemas(**user_input.model_dump())
    session.add(user)
    await session.commit()
    return user


# Функция удаления пользователя
async def delete_user(
        session: AsyncSession,
        user: UserSchemas,
) -> None:
    await session.delete(user)
    await session.commit()