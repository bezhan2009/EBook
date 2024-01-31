from sqlalchemy import and_

from sqlalchemy.orm import Session, sessionmaker
from connection import engine
from models import Books, Authors, Genres, Readers

# ############## Управление книгами:


def create_book(_book_data):
    with Session(autoflush=False, bind=engine) as db:
        book = Books(**_book_data)
        db.add(book)
        db.commit()
        return book


def get_book(_book_id):
    with Session(autoflush=False, bind=engine) as db:
        return db.query(Books).get(_book_id)


def update_book(_book, _updated_data):
    with Session(autoflush=False, bind=engine) as db:
        for key, value in _updated_data.items():
            setattr(_book, key, value)
        db.commit()
        return _book


def delete_book(_book):
    with Session(autoflush=False, bind=engine) as db:
        db.delete(_book)
        db.commit()


def add_author_to_book(_book, _author_id):
    with Session(autoflush=False, bind=engine) as db:
        author = db.query(Authors).get(_author_id)
        if author:
            _book.authors.append(author)
            db.commit()


def remove_author_from_book(_book, _author_id):
    with Session(autoflush=False, bind=engine) as db:
        author = db.query(Authors).get(_author_id)
        if author in _book.authors:
            _book.authors.remove(author)
            db.commit()


def add_genre_to_book(_book, _genre_id):
    with Session(autoflush=False, bind=engine) as db:
        genre = db.query(Genres).get(_genre_id)
        if genre:
            _book.genres.append(genre)
            db.commit()


def remove_genre_from_book(_book, _genre_id):
    with Session(autoflush=False, bind=engine) as db:
        genre = db.query(Genres).get(_genre_id)
        if genre in _book.genres:
            _book.genres.remove(genre)
            db.commit()


# ############## Управление читателями:

def get_reader(reader_id: int):
    with Session(autoflush=False, bind=engine) as db:
        return db.query(Readers).get(reader_id)


def create_reader(reader_data: dict):
    with Session(autoflush=False, bind=engine) as db:
        reader = Readers(**reader_data)
        db.add(reader)
        db.commit()
        db.refresh(reader)
        return reader


def update_reader(reader: Readers, updated_data: dict):
    with Session(autoflush=False, bind=engine) as db:
        for key, value in updated_data.items():
            setattr(reader, key, value)
        db.commit()
        return reader


def delete_reader(reader: Readers):
    with Session(autoflush=False, bind=engine) as db:
        db.delete(reader)
        db.commit()
