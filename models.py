from pydantic import BaseModel, EmailStr
from typing import Union


class Base(BaseModel):
    pass


class UserModel(Base):
    username: Union[str, EmailStr]
    password: str


class UserInput(Base):
    user_input: str

