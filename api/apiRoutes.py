from flask import (
    Blueprint,
    request,
    jsonify
)

from api import controller
from api.errors import APIError

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/')
def test():
    res = {
        "status": "success",
    }
    return res


@api.route('/generate-book-ideas', methods=['POST'])
def generate_book_ideas():
    try:
        [res, status] = controller.generate_book_ideas_controller(request)
        return jsonify(res), status

    except APIError as e:
        return jsonify({"message": e.message}), e.status

@api.route('/generate-book-summary', methods=['POST'])
def generate_book_summary():
    try:
        [res, status] = controller.generate_book_summary_controller(request)
        return jsonify(res), status

    except APIError as e:
        return jsonify({"message": e.message}), e.status
