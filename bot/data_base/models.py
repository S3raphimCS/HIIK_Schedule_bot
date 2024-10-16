from datetime import datetime

from sqlalchemy import (BigInteger, Boolean, Date, ForeignKey, Integer, String,
                        Text, func)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


# Модель для таблицы пользователей
class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    direction: Mapped[str] = mapped_column(String, nullable=True)
    agreement: Mapped[bool] = mapped_column(Boolean, nullable=True)


# Модель для таблицы заметок
class Change(Base):
    __tablename__ = 'changes'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[datetime] = mapped_column(String, server_default=func.now())
    direction: Mapped[str] = mapped_column(String, nullable=False)
    link: Mapped[str] = mapped_column(String, nullable=False)
