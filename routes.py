from flask import jsonify, Blueprint, request
import repository
from connection import Session
from models import Readers, Books, Loans

app = Blueprint('routes', __name__)


@app.route('/', methods=["GET"])
def index():
    return jsonify({"status": "server is up and running..."}), 200


# ############## Управление книгами:
@app.route("/books", methods=["POST"])
def create_new_book():
    book_data = request.json
    book = repository.create_book(book_data)
    return jsonify(book), 200


@app.route("/books/<book_id>", methods=["GET"])
def get_single_book(book_id):
    book = repository.get_book(book_id)
    if not book:
        return jsonify(error="Book not found"), 404
    return jsonify(book), 200


@app.route("/books/<book_id>", methods=["PUT"])
def update_existing_book(book_id):
    book = repository.get_book(book_id)
    if not book:
        return jsonify(error="Book not found"), 404
    updated_data = request.json
    updated_book = repository.update_book(book, updated_data)
    return jsonify(updated_book), 200


@app.route("/books/<book_id>", methods=["DELETE"])
def delete_existing_book(book_id):
    book = repository.get_book(book_id)
    if not book:
        return jsonify(error="Book not found"), 404
    repository.delete_book(book)
    return jsonify(message="Book deleted"), 200


@app.route("/books/<book_id>/authors/<author_id>", methods=["POST"])
def add_author_to_existing_book(book_id, author_id):
    book = repository.get_book(book_id)
    if not book:
        return jsonify(error="Book not found"), 404
    repository.add_author_to_book(book, author_id)
    return jsonify(message="Author added to book"), 200


@app.route("/books/<book_id>/authors/<author_id>", methods=["DELETE"])
def remove_author_from_existing_book(book_id, author_id):
    book = repository.get_book(book_id)
    if not book:
        return jsonify(error="Book not found"), 404
    repository.remove_author_from_book(book, author_id)
    return jsonify(message="Author removed from book"), 200


@app.route("/books/<book_id>/genres/<genre_id>", methods=["POST"])
def add_genre_to_existing_book(book_id, genre_id):
    book = repository.get_book(book_id)
    if not book:
        return jsonify(error="Book not found"), 404
    repository.add_genre_to_book(book, genre_id)
    return jsonify(message="Genre added to book"), 200


@app.route("/books/<book_id>/genres/<genre_id>", methods=["DELETE"])
def remove_genre_from_existing_book(book_id, genre_id):
    book = repository.get_book(book_id)
    if not book:
        return jsonify(error="Book not found"), 404
    repository.remove_genre_from_book(book, genre_id)
    return jsonify(message="Genre removed from book"), 200

# ############## Управление читателями:


@app.route("/readers", methods=["POST"])
def create_reader_route():
    '''Создание данных о читателях'''
    reader_data = request.json
    reader, status_code = repository.create_reader(reader_data)
    if reader is None:
        return jsonify(error="Reader not found"), status_code
    return jsonify(reader), status_code


@app.route("/readers", methods=["PUT"])
def update_reader_route():
    '''Редактирование данных о читателях'''
    reader_data = request.json
    reader, status_code = repository.update_reader(reader_data)
    if reader is None:
        return jsonify(error="Reader not found"), status_code
    return jsonify(reader), status_code


@app.route("/readers", methods=["GET"])
def get_all_readers_route():
    '''Просмотр списка читателей'''
    readers, status_code = repository.get_all_readers()
    return jsonify(readers), status_code


@app.route("/readers/<reader_id>", methods=["GET"])
def get_single_reader_route(reader_id):
    '''Просмотр информации о конкретном читателе'''
    reader, status_code = repository.get_single_reader(reader_id)
    if reader is None:
        return jsonify(error="Reader not found"), status_code
    return jsonify(reader), status_code


@app.route("/readers/<reader_id>/activity", methods=["GET"])
def get_reader_activity_route(reader_id):
    '''Просмотр активности читателя'''
    activity, status_code = repository.get_reader_activity(reader_id)
    if activity is None:
        return jsonify(error="Reader not found"), status_code
    return jsonify(activity), status_code


# ############## Управление заказами:

@app.route("/orders", methods=["POST"])
def create_order_route():
    '''Регистрация новых заказов на книги'''
    order_data = request.json
    order, status_code = repository.create_order(order_data)
    if order is None:
        return jsonify(error="Order not found"), status_code
    return jsonify(order), status_code


@app.route("/orders/<int:order_id>", methods=["PUT"])
def update_order_route(order_id):
    '''Отметка заказов как выполненных или отклоненных'''
    status = request.json.get("status")
    order, status_code = repository.update_order(order_id, status)
    if order is None:
        return jsonify(error="Order not found"), status_code
    return jsonify(order), status_code


@app.route("/orders/<int:order_id>", methods=["GET"])
def get_order_details_route(order_id):
    '''Отображение деталей заказа, включая книги, статус и сроки'''
    order_details, status_code = repository.get_order_details(order_id)
    if order_details is None:
        return jsonify(error="Order not found"), status_code
    return jsonify(order_details), status_code
