from flask import jsonify, Blueprint, request, make_response
import repository
from connection import engine
from models import Readers, Books
from sqlalchemy.orm import sessionmaker

app = Blueprint('routes', __name__)

Session = sessionmaker(autoflush=False, bind=engine)


# Поднятие сервера
@app.route('/', methods=["GET"])
def index():
    return jsonify({"status": "server is up and running..."}), 200


# ======================================= РАБОТАЕТ ==================================

# === УПРАВЛЕНИЕ КНИГАМИ ===

# Создание новой книги
@app.route("/books", methods=["POST"])
def create_new_book():
    book_data = request.json
    book = repository.create_book(book_data)
    return jsonify(book), 200


# Получение всего списка книг
@app.route("/bookies", methods=["GET"])
def get_single_book_all():
    books = repository.get_book_all()
    if not books:
        return jsonify(error="Books not found"), 404
    else:
        return jsonify(books), 200


# Поиск книги по id
@app.route("/books/<book_id>", methods=["GET"])
def get_single_book(book_id):
    book = repository.get_book(book_id)
    if not book:
        return jsonify(error="Book not found"), 404
    else:
        return jsonify(book), 200


# Изменение книги
@app.route("/books/<book_id>", methods=["PUT"])
def update_existing_book(book_id):
    book = repository.get_book(book_id)
    if not book:
        return jsonify(error="Book not found"), 404
    updated_data = request.get_json()
    updated_book = repository.update_book(book, book_id, updated_data)
    return jsonify(updated_book), 200


# Удаление книги
@app.route("/books/<book_id>", methods=["DELETE"])
def delete_existing_book(book_id):
    get_info_about_is_deleted = repository.delete_book(book_id)
    if get_info_about_is_deleted:
        return jsonify(message="Book deleted"), 200
    else:
        return jsonify(error="The book was not deleted because the id is not in the database"), 404


# Добавить автора для книги
@app.route("/books/<int:book_id>/authors/<int:author_id>", methods=["POST"])
def add_author_to_existing_book(book_id, author_id):
    book = repository.get_book_found(book_id)
    if not book:
        return jsonify(error="Книга не найдена"), 404
    author = repository.get_author_found(author_id)
    if not author:
        return jsonify(error="Автор не найден"), 404
    repository.add_author_to_book(book_id, author_id)
    return jsonify(message="Автор добавлен к книге"), 200


# Удалить автора для книги
@app.route("/books/<book_id>/authors/<author_id>", methods=["DELETE"])
def delete_author_from_book(book_id, author_id):
    print(book_id, author_id)
    result = repository.remove_author_from_book(book_id, author_id)
    if result:
        return jsonify(message="Author removed from book"), 200
    else:
        return jsonify(error="Author not found for the given book"), 404


# === УПРАВЛЕНИЕ АВТОРАМИ ===

# Создать автора
@app.route("/authors", methods=["POST"])
def create_new_author():
    new_author_data = request.get_json()
    new_author = repository.create_author(new_author_data)
    return jsonify(new_author), 201


# Получение списка всех авторов
@app.route("/authors", methods=["GET"])
def get_all_authors():
    all_authors = repository.get_all_authors()
    return jsonify(all_authors), 200


# Поиск автора по id
@app.route("/authors/<int:author_id>", methods=["GET"])
def get_single_author(author_id):
    author = repository.get_author(author_id)
    if not author:
        return jsonify(error="Автор не найден"), 404
    else:
        return jsonify(author), 200


# Изменение автора
@app.route("/authors/<int:author_id>", methods=["PUT"])
def update_existing_author(author_id):
    updated_data = request.get_json()
    updated_author = repository.update_author(author_id, updated_data)
    if not updated_author:
        return jsonify(error="Автор не найден"), 404
    return jsonify(updated_author), 200


# Удаление автора
@app.route("/authors/<int:author_id>", methods=["DELETE"])
def delete_author_by_id(author_id):
    success = repository.delete_author(author_id)
    if success:
        return jsonify({'message': 'Автор успешно удален'}), 200
    else:
        return jsonify({'message': 'Автор не найден'}), 404


# === УПРАВЛЕНИЕ ЖАНРАМИ ===

# Создать новый жанр
@app.route("/genres", methods=["POST"])
def create_new_genre():
    new_genre_data = request.get_json()
    new_genre = repository.create_genre(new_genre_data)
    return jsonify(new_genre), 201


# Добавить жанр книги
@app.route("/books/<book_id>/genres/<genre_id>", methods=["POST"])
def add_genre_to_existing_book(book_id, genre_id):
    book = repository.get_book_found(book_id)
    if not book:
        return jsonify(error="Book not found"), 404
    genre = repository.get_genre_found(genre_id)
    if not genre:
        return jsonify(error="Genre not found"), 404
    repository.add_genre_to_book(book_id, genre_id)
    return jsonify(message="Genre added to book"), 200


# Удалить жанр книги
@app.route("/books/<book_id>/genres/<genre_id>", methods=["DELETE"])
def delete_genre_from_book(book_id, genre_id):
    print(book_id, genre_id)
    result = repository.remove_genre_from_book(book_id, genre_id)
    if result:
        return jsonify(message="Genre removed from book"), 200
    else:
        return jsonify(error="Genre not found for the given book"), 404


# === УПРАВЛЕНИЕ ЧИТАТЕЛЯМИ ===

# Создать читателя
@app.route("/readers", methods=["POST"])
def create_new_reader():
    reader_data = request.json
    reader = repository.create_reader(reader_data)
    if reader:
        return jsonify(reader), 200
    else:
        return jsonify(error="Failed to create reader"), 500


# Удалить читателя по id
@app.route("/readers/<int:reader_id>", methods=["DELETE"])
def delete_reader(reader_id):
    result = repository.delete_reader_by_id(reader_id)
    if "error" in result:
        return jsonify(result), 404
    else:
        return jsonify(result), 200


# Поиск читателя по id
@app.route("/readers/<int:reader_id>", methods=["GET"])
def get_single_reader_info(reader_id):
    reader = repository.get_single_reader(reader_id)
    if not reader:
        return jsonify(error="Читатель не найден"), 404
    return jsonify({
        "id": reader.id,
        "reader_name": reader.reader_name,
        "year_birth": reader.year_birth,
        "reader_address": reader.reader_address,
        "email": reader.email
    }), 200


# Показать всех читателей
@app.route("/readers", methods=["GET"])
def get_all_readers():
    '''Просмотр списка читателей'''
    with Session(autoflush=False, bind=engine) as db:
        readers = db.query(Readers).all()
        serialized_readers = []
        for reader in readers:
            serialized_reader = {
                'id': reader.id,
                'reader_name': reader.reader_name,
                'year_birth': reader.year_birth,
                'reader_address': reader.reader_address,
                'email': reader.email
            }
            serialized_readers.append(serialized_reader)
        return make_response(jsonify(serialized_readers), 200)


# Поиск активностей конкретного читателя
@app.route("/readers/<reader_id>/activity", methods=["GET"])
def get_reader_activity_route(reader_id):
    activity, status_code = repository.get_reader_activity(reader_id)
    if activity is None:
        return jsonify(error="Reader not found"), status_code
    return jsonify(activity), status_code


# === УПРАВЛЕНИЕ ЗАКАЗАМИ ===

# Регистрация нового заказа на книги
@app.route('/orders', methods=['POST'])
def create_order_route():
    book_ids = request.json.get('book_ids')
    # print(book_ids)
    # print('*' * 1120)
    repository.create_order(book_ids)
    return 'Order created', 201


# Обновление статуса заказа
@app.route('/orders/<int:order_id>/status', methods=['PUT'])
def update_order_status_route(order_id):
    status = request.json.get('status')
    if status not in ['Completed', 'Rejected']:
        return 'Invalid status', 400

    if repository.update_order_status(order_id, status):
        return 'Order status updated', 200
    return 'Order not found', 404

