import json
import time

from flask import Request

from api.errors import APIError
from api.validation import (generate_book_ideas_controller_validation,
                            generate_book_summary_controller_validation,
                            generate_html_controller_validation)
from gemini.generateBook import (MODEL, GenerateBookIdeasWithParams,
                                 GenerateBookWithParams)
from gemini.utils import Utils

book_idea_generator = GenerateBookIdeasWithParams()
book_chapter_generator = GenerateBookWithParams()
utils = Utils()


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


def generate_book_summary_controller(request: Request):
    payload = request.get_json()
    generate_book_summary_controller_validation(payload)

    try:
        title = payload["title"]
        style = payload["style"]
        description = payload["description"]
        genre = payload["genre"]
        noOfChapters = int(payload["noOfChapters"])
        creativity = int(payload["creativity"])
        logic = int(payload["logic"])

        response = book_chapter_generator.generateBookSummary(
            title=title, description=description, genre=genre, style=style, chapters=noOfChapters, creativity=creativity, logic=logic)
        return response, 200
    except ValueError as e:
        raise APIError(e, 400)


def generate_full_book_controller():
    try:
        for chapter in book_chapter_generator.generateAllChapters(5, "very-long"):
            jsonString = f"{json.dumps(chapter)}\n".encode(
                'utf-8')  # convert to bytes
            yield jsonString

    except Exception as e:
        raise APIError(
            "generateBookSummary must be called first, if you got this error even after calling generateBookSummary, then please refresh the page and try again", 400)


def generate_html_controller(request: Request):
    payload = request.get_json()
    generate_html_controller_validation(payload)

    try:
        book_summary = payload["bookSummary"]
        bookContent = payload["bookContent"]

        htmlContent = utils.renderBookHtml({"bookSummary": book_summary,
                                            "bookContent": bookContent, "author": MODEL})

        return htmlContent, 200

    except Exception as e:
        raise APIError(e, 500)


def generate_pdf_controller(request: Request):
    payload = request.get_json()
    generate_html_controller_validation(payload)

    try:
        book_summary = payload["bookSummary"]
        bookContent = payload["bookContent"]

        file_name = f"{book_summary['title'].replace(' ', '-')}_{time.time()}.pdf"
        htmlContent = utils.renderBookHtml({"bookSummary": book_summary,
                                            "bookContent": bookContent, "author": MODEL})
        pdfContent = utils.generatePdfFromHtml(htmlContent)

        return file_name, pdfContent, 200

    except Exception as e:
        raise APIError(e, 500)
