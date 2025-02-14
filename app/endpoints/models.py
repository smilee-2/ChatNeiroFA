from pydantic import BaseModel, EmailStr

#Базовый класс
class Base(BaseModel):
    pass

# Класс для валидации пользователей
class UserModel(Base):
    username: str | EmailStr
    password: str

# Класс для валидации запроса gpt
class UserInput(Base):
    user_input: str

