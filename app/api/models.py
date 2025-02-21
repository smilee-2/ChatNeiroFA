from pydantic import BaseModel, EmailStr


# Базовый класс
class Base(BaseModel):
    pass


# Класс для валидации пользователей
class UserModel(Base):
    username: str | EmailStr
    password: str
    disabled: bool | None = None


# Класс для валидации запроса gpt
class UserInput(Base):
    user_input: str


# Класс для валидации токена
class Token(BaseModel):
    access_token: str
    token_type: str


#
class TokenData(BaseModel):
    username: str | None = None
