

from fastapi import APIRouter, Depends, status

from app.api.models import UserModel
from app.database import crud
from app.database.depends import user_by_id


router = APIRouter(prefix='/user', tags=['User'])


@router.get('/get_user/{user_id}', tags=['main'])
async def get_user(user: UserModel = Depends(user_by_id)):
    return user



@router.delete('/delete/{user_id}', tags=['main'], status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user: UserModel = Depends(user_by_id)):
    await crud.delete_user(user=user)