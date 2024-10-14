from flask import Request
from gemini.generateBook import GenerateBookIdeasWithParams, GenerateBookWithParams
from api.errors import APIError
from api.validation import generate_book_ideas_controller_validation, generate_book_chapter_controller_validation

book_idea_generator = GenerateBookIdeasWithParams()
book_chapter_generator = GenerateBookWithParams()

def generate_book_ideas_controller(request: Request):
    payload = request.get_json()
    generate_book_ideas_controller_validation(payload)

    try:
        prompt = payload["prompt"]
        limit = int(payload["limit"])
        response = book_idea_generator.generateIdeas(prompt, limit)
        return response, 200
    except ValueError as e:
        raise APIError(e, 400)

def generate_book_chapter_controller(request: Request):
    payload = request.get_json()
    generate_book_chapter_controller_validation(payload)

    try:
        title = payload["title"]
        style = payload["style"]
        description = payload["description"]
        genre = payload["genre"]
        noOfChapters = int(payload["noOfChapters"])
        creativity = payload["creativity"]
        logic = payload["logic"]

        response = book_idea_generator.generateChapter(title, style, description, genre, noOfChapters, creativity, logic)
        return response, 200
    except ValueError as e:
        raise APIError(e, 400)