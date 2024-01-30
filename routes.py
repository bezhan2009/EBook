from flask import jsonify, Blueprint, request
import repository

app = Blueprint('routes', __name__)


@app.route('/', methods=["GET"])
def index():
    return jsonify({"status": "server is up and running..."}), 200
