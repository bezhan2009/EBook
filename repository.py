from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from connection import engine
from models import Books, Authors, Genres, Readers, BorrowedBooks
from datetime import datetime


Session = sessionmaker(bind=engine)


# Добавить автора для книги
def add_author_to_book(_book, _author_id):
    with Session(autoflush=False, bind=engine) as db:
        author = db.query(Authors).get(_author_id)
        if author:
            _book.authors.append(author)
            db.commit()


# Удалить автора для книги
def remove_author_from_book(_book, _author_id):
    with Session(autoflush=False, bind=engine) as db:
        author = db.query(Authors).get(_author_id)
        if author in _book.authors:
            _book.authors.remove(author)
            db.commit()


# Добавить жанр книги
def add_genre_to_book(_book, _genre_id):
    with Session(autoflush=False, bind=engine) as db:
        genre = db.query(Genres).get(_genre_id)
        if genre:
            _book.genres.append(genre)
            db.commit()


# Удалить жанр книги
def remove_genre_from_book(_book, _genre_id):
    with Session(autoflush=False, bind=engine) as db:
        genre = db.query(Genres).get(_genre_id)
        if genre in _book.genres:
            _book.genres.remove(genre)
            db.commit()


# Создать читателя
def create_reader(reader_data: dict):
    with Session(autoflush=False, bind=engine) as db:
        reader = Readers(**reader_data)
        db.add(reader)
        db.commit()
        db.refresh(reader)
        return reader


# Измененить читателя
def update_reader(reader: Readers, updated_data: dict):
    with Session(autoflush=False, bind=engine) as db:
        for key, value in updated_data.items():
            setattr(reader, key, value)
        db.commit()
        return reader


# Удалить читателя
def delete_reader(reader: Readers):
    with Session(autoflush=False, bind=engine) as db:
        db.delete(reader)
        db.commit()


# ======================================= РАБОТАЕТ ==================================

# === УПРАВЛЕНИЕ КНИГАМИ ===

# Создание новой книги
def create_book(_book_data):
    with Session(autoflush=False, bind=engine) as db:
        book = Books(**_book_data)
        db.add(book)
        db.commit()
        if book:
            return "Книга создана!!!"
        else:
            return False


# Получение всего списка книг
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


# Поиск книги по id
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


# Изменение книги
def update_book(_book, book_id, _updated_data):
    with Session(autoflush=False, bind=engine) as db:
        db.query(Books).filter(Books.id == book_id).update(_updated_data)
        db.commit()
        updated_book = db.query(Books).get(book_id)
        serialized_book = {
            'id': updated_book.id,
            'title': updated_book.title,
            'publication': updated_book.publication,
            'publication_date': updated_book.publication_date.isoformat(),
            'cover_image': updated_book.cover_image,
            'book_location': updated_book.book_location,
            'description': updated_book.description,
            'price': updated_book.price,
            'available_copies': updated_book.available_copies
        }
        return serialized_book


# Удаление книги
def delete_book(_book_id):
    with Session(autoflush=False, bind=engine) as db:
        book_to_delete = db.query(Books).filter_by(id=_book_id).first()
        if book_to_delete:
            db.delete(book_to_delete)
            db.commit()
            return True
        else:
            return False


# === УПРАВЛЕНИЕ АВТОРАМИ ===

# Создать автора
def create_author(author_data):
    existing_author = get_author_by_name(author_data['author_name'])
    if existing_author:
        return {'message': 'Автор с таким именем уже есть'}
    new_author = Authors(author_name=author_data['author_name'],
                         description=author_data.get('description'))
    with Session(autoflush=False, bind=engine) as db:
        try:
            db.add(new_author)
            db.commit()
            db.refresh(new_author)
            return {
                'id': new_author.id,
                'author_name': new_author.author_name,
                'description': new_author.description
            }
        except IntegrityError:
            db.rollback()
            return {'message': 'Не удалось создать автора из-за нарушения ограничений базы данных'}


# Получение автора по имени
# (эта функция без роута, т.к. она нужна только
# для проверки именни автора для функции create_author)
def get_author_by_name(author_name):
    with Session(autoflush=False, bind=engine) as db:
        return db.query(Authors).filter(Authors.author_name == author_name).first()


# Поиск автора по id
def get_author(author_id):
    with Session(autoflush=False, bind=engine) as db:
        author = db.query(Authors).filter(Authors.id == author_id).first()
        if author:
            return {
                'id': author.id,
                'author_name': author.author_name,
                'description': author.description
            }
        else:
            return None


# Получение списка всех авторов
def get_all_authors():
    with Session(autoflush=False, bind=engine) as db:
        authors = db.query(Authors).all()
        author_list = []
        for author in authors:
            author_info = {
                'id': author.id,
                'author_name': author.author_name,
                'description': author.description
            }
            author_list.append(author_info)
        return author_list


# Изменение автора
def update_author(author_id, updated_data):
    with Session(autoflush=False, bind=engine) as db:
        db.query(Authors).filter(Authors.id == author_id).update(updated_data)
        db.commit()
        updated_author = db.query(Authors).get(author_id)
        serialized_author = {
            'id': updated_author.id,
            'author_name': updated_author.author_name,
            'description': updated_author.description,
        }
        return serialized_author


# Удаление автора
def delete_author(author_id):
    with Session(autoflush=False, bind=engine) as db:
        author = db.query(Authors).filter(Authors.id == author_id).first()
        if author:
            db.delete(author)
            db.commit()
            return True
        else:
            return False


# === УПРАВЛЕНИЕ ЖАНРАМИ ===

# Создать автора
def create_genre(genre_data):
    existing_genre = get_genre_by_title(genre_data['title_genre'])
    if existing_genre:
        return {'message': 'Автор с таким именем уже есть'}
    new_genre = Genres(title_genre=genre_data['title_genre'])
    with Session(autoflush=False, bind=engine) as db:
        try:
            db.add(new_genre)
            db.commit()
            db.refresh(new_genre)
            return {
                'id': new_genre.id,
                'title_genre': new_genre.title_genre
            }
        except IntegrityError:
            db.rollback()
            return {'message': 'Не удалось создать жанр из-за нарушения ограничений базы данных'}


# Получение жанра по названию
# (эта функция без роута, т.к. она нужна только
# для проверки именни автора для функции create_genre)
def get_genre_by_title(title_genre):
    with Session(autoflush=False, bind=engine) as db:
        return db.query(Genres).filter(Genres.title_genre == title_genre).first()


# === УПРАВЛЕНИЕ ЧИТАТЕЛЯМИ ===

# Поиск активностей конкретного читателя
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


# Показать читателей
def get_reader(reader_id: int):
    with Session(autoflush=False, bind=engine) as db:
        return db.query(Readers).get(reader_id)
