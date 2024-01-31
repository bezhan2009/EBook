from connection import engine
from sqlalchemy import Column, String, Integer, SmallInteger, Numeric, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Session, relationship
from sqlalchemy.sql.expression import text


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
    # number_of_copies = Column(Integer, nullable=False, unique=False)
    cover_image = Column(String)
    # floor, row, rack, shelf
    book_location = Column(String(length=8), nullable=False)
    other_attribute = Column(String(length=120))
    price = Column(Float, nullable=False)


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
    email = Column(String(length=80), nullable=False, unique=False)


class BorrowedBooks(Base):
    __tablename__ = "borrowed_books"

    id = Column(Integer, primary_key=True, autoincrement=True,
                nullable=False, index=True)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    reader_id = Column(Integer, ForeignKey('readers.id'), nullable=False)
    date_borrowed = Column(DateTime, nullable=False)
    date_return = Column(DateTime, nullable=True)
    date_returned = Column(DateTime, nullable=True)
    is_returned = Column(Boolean, nullable=False,
                         default=False, server_default=text('False'))
    # Library, Home
    location = Column(String(7), nullable=False)


class Orders(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    order_date = Column(DateTime, nullable=False)
    status = Column(String, nullable=False)
    order_items = relationship("OrderItems")


class OrderItems(Base):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    new_book_id = Column(Integer, ForeignKey('books.id'), nullable=True)
    new_book_title = Column(String, nullable=False)
    new_book_author = Column(String, nullable=False)
    new_book_price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)


# ########################################################################### #
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
