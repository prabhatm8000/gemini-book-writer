from flask import Request
from gemini.generateBook import GenerateBookIdeasWithParams
from api.errors import APIError
from api.validation import generate_book_ideas_controller_validation

book_idea_generator = GenerateBookIdeasWithParams()

def generate_book_ideas_controller(request: Request):
    if (request.method != "POST"):
        raise APIError("Not found", 404)
    
    payload = request.get_json()
    generate_book_ideas_controller_validation(payload)

    prompt = payload["prompt"]
    limit = payload["limit"]

    try:
        response = book_idea_generator.generateIdeas(prompt, limit)
        return {
            "ideas": response
        }
    except ValueError as e:
        raise APIError(e, 400)

