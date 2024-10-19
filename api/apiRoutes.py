from flask import (
    Blueprint,
    request,
    Response,
    jsonify
)

import json

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


def chapter_stream():
    try:
        for chapter in controller.generate_full_book_controller():
            yield chapter
    except APIError as e:
        yield json.dumps({"error": True, "status": e.status, "message": e.message}).encode('utf-8')


@api.route('/generate-full-book')
def generate_full_book():
    return Response(chapter_stream(), content_type='application/json',
                    direct_passthrough=True)


@api.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    try:
        [res, status] = controller.generate_pdf_controller(request)
        return res, status
    except APIError as e:
        return jsonify({"message": e.message}), e.status
