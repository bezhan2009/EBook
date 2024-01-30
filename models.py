from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import DeclarativeBase, Session


# создаем базовый класс для моделей
class Base(DeclarativeBase):
    pass

