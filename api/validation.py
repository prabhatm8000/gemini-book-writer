from api.errors import APIError

def generate_book_ideas_controller_validation(payload) -> dict:
    if (payload is None):
        raise APIError("Invalid JSON", 400)
    
    if ("prompt" not in payload):
        raise APIError("Missing prompt", 400)

    if ("limit" not in payload):
        raise APIError("Missing limit", 400)

def generate_book_chapter_controller_validation(payload) -> dict:
    if (payload is None):
        raise APIError("Invalid JSON", 400)
    
    if ("title" not in payload):
        raise APIError("Missing title", 400)
    
    if ("description" not in payload):
        raise APIError("Missing description", 400)

    if ("style" not in payload):
        raise APIError("Missing style", 400)

    if ("genre" not in payload):
        raise APIError("Missing genre", 400)

    if ("noOfChapters" not in payload):
        raise APIError("Missing noOfChapters", 400)

    if ("creativity" not in payload):
        raise APIError("Missing creativity", 400)

    if ("logic" not in payload):
        raise APIError("Missing logic", 400)