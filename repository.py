from sqlalchemy import and_

from sqlalchemy.orm import Session, sessionmaker
from connection import engine
from models import Books, Authors, Genres, BorrowedBooks, Readers, Orders

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

def create_reader(_reader_data):
    with Session(autoflush=False, bind=engine) as db:
        reader = Readers(**_reader_data)
        db.add(reader)
        db.commit()
        return reader, 200


def update_reader(_reader_data):
    with Session(autoflush=False, bind=engine) as db:
        reader_id = _reader_data.get("id")
        reader = db.query(Readers).get(reader_id)
        if not reader:
            return None, 404
        for key, value in _reader_data.items():
            setattr(reader, key, value)
        db.commit()
        return reader, 200


def get_all_readers():
    with Session(autoflush=False, bind=engine) as db:
        readers = db.query(Readers).all()
        return readers, 200


def get_single_reader(_reader_id):
    with Session(autoflush=False, bind=engine) as db:
        reader = db.query(Readers).get(_reader_id)
        if not reader:
            return None, 404
        return reader, 200


def get_reader_activity(_reader_id):
    with Session(autoflush=False, bind=engine) as db:
        reader = db.query(Readers).get(_reader_id)
        if not reader:
            return None, 404
        borrowed_books = (
            db.query(BorrowedBooks)
            .join(Books)
            .filter(BorrowedBooks.reader_id == _reader_id)
            .all()
        )
        activity = []
        for borrowed_book in borrowed_books:
            book = borrowed_book.book
            activity.append({
                "book": book,
                "date_borrowed": borrowed_book.date_borrowed,
                "date_returned": borrowed_book.date_returned,
                "is_returned": borrowed_book.is_returned
            })
        return activity, 200


# ############## Управление заказами:


def create_order(_order_data):
    with Session(autoflush=False, bind=engine) as db:
        _book_ids = _order_data.get("book_ids")
        _books = db.query(Books).filter(Books.id.in_(_book_ids)).all()

        _order = Orders(books=_books, status="pending")
        db.add(_order)
        db.commit()

        return _order, 200


def update_order(_order_id, _status):
    with Session(autoflush=False, bind=engine) as db:
        _order = db.query(Orders).get(_order_id)
        if not _order:
            return None, 404

        _order.status = _status
        db.commit()

        return _order, 200


def get_order_details(_order_id):
    with Session(autoflush=False, bind=engine) as db:
        _order = db.query(Orders).get(_order_id)
        if not _order:
            return None, 404

        _books = _order.books
        _book_details = []
        for _book in _books:
            _book_details.append({
                "id": _book.id,
                "title": _book.title,
                "author": _book.author
            })

        _order_details = {
            "id": _order.id,
            "status": _order.status,
            "books": _book_details,
            "created_at": _order.created_at,
            "updated_at": _order.updated_at
        }

        return _order_details, 200
