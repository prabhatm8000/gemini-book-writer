from flask import Request
from app.errors import APIError


def generate_book_ideas_controller(request: Request):
    if (request.method != "POST"):
        raise APIError("Not found", 404)

    return {
        "status": "success",
    }
