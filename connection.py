from security import dbname_app, user_app, password_app, host_app, port_app
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# db_url = 'postgresql://username:password@host:port/dbname'
db_url = f'postgresql://{user_app}:{password_app}@{
    host_app}:{port_app}/{dbname_app}'

# создание машины соединения
engine = create_engine(db_url, echo=False)

# Создаем класс последующих сессий, на основе которого будут создаваться разовые экземпляры для разовых подключений.
Session = sessionmaker(bind=engine)
