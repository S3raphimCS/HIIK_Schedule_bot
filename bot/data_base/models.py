from sqlalchemy import BigInteger, Integer, Text, ForeignKey, String, Boolean, Date, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .database import Base
from datetime import datetime


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
