from flask import Flask, jsonify
from sqlalchemy.orm import Session, sessionmaker
from routes import app as routes_app
from models import Base
from connection import engine
from flask_jwt_extended import JWTManager
# создаем таблицы
Base.metadata.create_all(bind=engine)

app = Flask(__name__)
app.register_blueprint(routes_app)
app.config['JWT_SECRET_KEY'] = 'your_secret_key_here'
jwt = JWTManager(app)
if __name__ == '__main__':
    app.run(debug=False, port=7000)
