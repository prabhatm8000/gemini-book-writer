import json
import time
import re
import os
from jinja2 import Environment, FileSystemLoader

def geminiResponseToJson(text: str) -> dict:
    """
    Converts the gemini response to json.
    """
    jsonStr = text.strip().removeprefix(
        "```json").removesuffix("```")
    jsonStr = re.sub(r'\\[nrtbfv\'"\\]', ' ', jsonStr)
    return dict(json.loads(jsonStr))


def logger(message: str, file: str = "log.txt") -> None:
    """
    Logs the generated book summary.
    """
    with open(file, "a") as f:
        f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}]: {message}\n\n")


def renderBookHtml(book: dict) -> str:
    """
    Converts the generated book summary to pdf.
    """
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template('book.html')
    renderedHtml = template.render(book)
    with open(os.path.dirname(__file__) + "/" + "rendered.html", 'w') as f:
        f.write(renderedHtml)