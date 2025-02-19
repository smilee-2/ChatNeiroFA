from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


#Базовый класс
class BaseSchemas(DeclarativeBase):
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True)


# Класс для создания таблицы пользователей
class UserSchemas(BaseSchemas):
    __tablename__ = "Users"

    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)