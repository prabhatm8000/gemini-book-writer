from flask import (
    Blueprint,
    request,
    jsonify
)

from app import apiControllers as controllers
from app.errors import APIError

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/')
def test():
    res = {
        "status": "success",
    }
    return res


@api.route('/generate-book-ideas')
def generate_book_ideas():
    try:
        [res, status] = controllers.generate_book_ideas_controller(request)
        return jsonify(res), status

    except APIError as e:
        return jsonify({"message": e.message}), e.status
