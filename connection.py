from sqlalchemy import create_engine

# db_url = 'postgresql://username:password@host:port/dbname'
db_url = 'postgresql://postgres:postgres@localhost:5436/my_db'

# создание машины соединения
engine = create_engine(db_url, echo=False)
