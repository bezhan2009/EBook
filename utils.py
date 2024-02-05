import hashlib


def hash_string(input_string):
    # Преобразуем строку в байты перед хешированием
    input_bytes = input_string.encode('utf-8')

    # Создаем объект хеша SHA-256
    sha256_hash = hashlib.sha256()

    # Обновляем объект хеша с байтами строки
    sha256_hash.update(input_bytes)

    # Получаем хеш в виде шестнадцатеричной строки
    hashed_string = sha256_hash.hexdigest()

    return hashed_string