from typing import Annotated
from datetime import timedelta, datetime, timezone

import jwt
from jwt import InvalidTokenError
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status, Depends

from app.api.models import TokenData
from app.config.config import setting
from app.database import crud

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Получить хеш пароля
def get_password_hash(password):
    return pwd_context.hash(password)


# Проверить пароль
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# Создать токен
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, setting.SECRET_KEY, algorithm=setting.ALGORITHM)
    return encoded_jwt


# Проверить пользователя
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = jwt.decode(token, setting.SECRET_KEY, algorithms=[setting.ALGORITHM])
        username = payload.get('sub')
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError as e:
        print('token bad(', e)
        raise credentials_exception
    user = crud.get_user_by_name(username=token_data.username, )
    if user is None:
        raise credentials_exception
    return user
