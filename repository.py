from sqlalchemy import and_

from sqlalchemy.orm import sessionmaker
from connection import engine
from models import Books, Authors, Genres, Readers
from datetime import datetime
# ############## Управление книгами:

Session = sessionmaker(bind=engine)
def create_book(_book_data):
    with Session(autoflush=False, bind=engine) as db:
        book = Books(**_book_data)
        db.add(book)
        db.commit()
        if book:
            return "Книга создана!!!"
        else:
            return False

# Новые данные о книге
new_book_data = {
    'title': 'Примернаяы книга',
    'publication': 'Примерноеы издание',
    'publication_date': datetime(2022, 12, 31),
    'cover_image': 'sample_cover.jpg',
    'book_location': 'A101',
    'description': 'Это примернаяы книга.',
    'price': 19.99,
    'available_copies': 10
}

# Создание новой книги
# print(create_book(new_book_data))

def get_book(_book_id):
    with Session(autoflush=False, bind=engine) as db:
        book_seek = db.query(Books).filter_by(id=_book_id).first()
        if book_seek:
            book_data = {
                'id': book_seek.id,
                'title': book_seek.title,
                'publication': book_seek.publication,
                'publication_date': book_seek.publication_date,
                'cover_image': book_seek.cover_image,
                'book_location': book_seek.book_location,
                'description': book_seek.description,
                'price': book_seek.price,
                'available_copies': book_seek.available_copies
            }
            return book_data
        else:
            return None


def get_book_all():
    with Session(autoflush=False, bind=engine) as db:
        book_seek = db.query(Books).distinct().all()
        if book_seek:
            books_data = []
            for book in book_seek:
                book_data = {
                    'id': book.id,
                    'title': book.title,
                    'publication': book.publication,
                    'publication_date': book.publication_date,
                    'cover_image': book.cover_image,
                    'book_location': book.book_location,
                    'description': book.description,
                    'price': book.price,
                    'available_copies': book.available_copies
                }
                books_data.append(book_data)
            return books_data
        else:
            return None

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
