from typing import Annotated

from fastapi import Path, HTTPException, status

from app.config.config import session_maker
from app.database.schemas import UserSchemas
from app.database import crud

# Вернет пользователя по id
async def user_by_id(user_id: Annotated[int, Path]) -> UserSchemas:
    async with session_maker.begin() as session:
        user = await crud.get_user(user_id=user_id)
        if user is not None:
            return user
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User {user_id} not found"
        )