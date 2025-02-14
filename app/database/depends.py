from typing import Annotated
from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.dbhelper import database
from app.database.schemas import UserSchemas
from app.database.crud import get_user

# Вернет пользователя по id
async def user_by_id(
    user_id: Annotated[int, Path],
    session: AsyncSession = Depends(database.session_depend)
) -> UserSchemas:
    user = await get_user(session=session, user_id=user_id)
    if user is not None:
        return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Product {user_id} not found"
    )