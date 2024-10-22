import json
import time
import re
import os
from jinja2 import Environment, FileSystemLoader
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import base64
from urllib import parse


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


def generatePdfFromHtml(html_content):
    """
    Generates a pdf from the html.
    """
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')

    driver = webdriver.Chrome(options=chrome_options)

    encoded = parse.quote(html_content)

    pdf_bytes = b""
    try:
        driver.get(f"""data:text/html,{encoded}""")
        time.sleep(1)

        # Enable Chrome DevTools Protocol
        pdf = driver.execute_cdp_cmd("Page.printToPDF", {
            "margin": {
                "top": "2in",
                "bottom": "2in",
                "left": "2in",
                "right": "2in"
            },
            "pageSize": {
                "width": "8.5in",
                "height": "11in",
                "paperWidth": "8.5in",
                "paperHeight": "11in"
            }
        })

        pdf_bytes = base64.b64decode(pdf['data'])

    finally:
        driver.quit()
        # if os.path.exists(pdf_file_path):
        # os.remove(pdf_file_path)

    return pdf_bytes
