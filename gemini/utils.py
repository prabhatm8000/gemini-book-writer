import json
import time
import re
import os
from jinja2 import Environment, FileSystemLoader
import asyncio
from pyppeteer import launch


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
    # with open(os.path.dirname(__file__) + "/" + "rendered.html", 'w') as f:
    #     f.write(renderedHtml)

    return renderedHtml


async def generatePdfFromHtml(html_content):
    """
    Generates a pdf from the html.
    """
    browser = await launch(headless=False, executablePath=os.environ.get("Chromium_exe_path"))
    page = await browser.newPage()
    await page.setContent(html_content)

    pdf_bytes = await page.pdf({
        'format': 'letter',
        'margin': {
            'top': '0.6in',
            'right': '0.6in',
            'bottom': '0.6in',
            'left': '0.6in'
        }
    })

    await browser.close()
    return pdf_bytes
