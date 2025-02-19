from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Получить хеш пароля
def get_password_hash(password):
    return pwd_context.hash(password)

# Проверить пароль
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


print(get_password_hash('123'))