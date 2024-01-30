from modules.connection import engine
from sqlalchemy.sql.expression import text
from sqlalchemy import Column, String, Integer, SmallInteger, Numeric, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import DeclarativeBase, Session


# Создаем базовый класс для моделей
class Base(DeclarativeBase):
    pass


class Books(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, autoincrement=True,
                nullable=False, index=True)
    title = Column(String(length=255), nullable=False, unique=False)
    publication = Column(String(length=50), nullable=False, unique=False)
    publication_date = Column(String(length=50), nullable=False, unique=False)
    number_of_copies = Column(Integer, nullable=False, unique=False)
    url_img = Column(String)


class BooksAuthors(Base):
    __tablename__ = "books_authors"

    id = Column(Integer, primary_key=True, autoincrement=True,
                nullable=False, index=True)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    author_id = Column(Integer, ForeignKey('authors.id'), nullable=False)


class Authors(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, autoincrement=True,
                nullable=False, index=True)
    author_name = Column(String(length=70), nullable=False, unique=False)


class BooksGenres(Base):
    __tablename__ = "books_genres"

    id = Column(Integer, primary_key=True, autoincrement=True,
                nullable=False, index=True)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    genre_id = Column(Integer, ForeignKey('genres.id'), nullable=False)


class Genres(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, autoincrement=True,
                nullable=False, index=True)
    title_genre = Column(String(length=70), nullable=False, unique=False)


class Readers(Base):
    __tablename__ = "readers"

    id = Column(Integer, primary_key=True, autoincrement=True,
                nullable=False, index=True)
    reader_name = Column(String(length=70), nullable=False, unique=False)
    year_birth = Column(Integer, nullable=False, unique=False)
    reader_address = Column(String(length=120), nullable=False, unique=False)
    is_deleted = Column(Boolean, nullable=False,
                        default=False, server_default=text('False'))
    date_deleted = Column(DateTime, nullable=True)


# ############################## #
class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True,
                nullable=False, index=True)
    login = Column(String(length=32), nullable=False, unique=True)
    psw = Column(String(length=255), nullable=False)
    access_level = Column(SmallInteger, default=1, server_default=text('1'))


class Customers(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, autoincrement=True,
                nullable=False, index=True)
    name_cust = Column(String(length=32), nullable=False, unique=True)
    is_deleted = Column(Boolean, nullable=False,
                        default=False, server_default=text('False'))

    accounts = relationship("Accounts", back_populates="customer")


class Accounts(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, autoincrement=True,
                index=True, nullable=False)
    cust_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    account_number = Column(String(length=16), nullable=False, unique=True)
    is_deleted = Column(Boolean, nullable=False,
                        default=False, server_default=text('False'))
    date_deleted = Column(DateTime, nullable=True)
    amount = Column(Numeric(precision=10, scale=2),
                    nullable=False, default=10000, server_default=text('10000'))

    customer = relationship("Customers", back_populates="accounts")


Base.metadata.create_all(bind=engine)
