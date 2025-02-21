from fastapi import APIRouter, status

from app.api.models import UserModel
from app.database import crud

router = APIRouter(prefix='/user', tags=['User'])


@router.get('/get_user/{user_id}', tags=['main'])
async def get_user(user: UserModel):
    return user


@router.delete('/delete/{user_id}', tags=['main'], status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user: UserModel):
    await crud.delete_user(user_model=user)
