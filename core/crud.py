from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from models import UserModel
from .schemas import UserSchemas

# Функция добавления юзера в БД
async def create_user(session: AsyncSession, user_input: UserModel) -> UserSchemas:
    user = UserSchemas(**user_input.model_dump())
    session.add(user)
    await session.commit()
    return user