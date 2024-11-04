import json
import time
import re
import os
from jinja2 import Environment, FileSystemLoader
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import base64
from urllib import parse
import requests
from api.errors import APIError
import zipfile


class Utils:

    def __init__(self):
        self.bookSummary = {}
        self.htmlContent = None
        self.pdf_bytes = None
        self.cover_img_url = None

    def geminiResponseToJson(self, text: str) -> dict:
        """
        Converts the gemini response to json.
        """
        jsonStr = text.strip().removeprefix(
            "```json").removesuffix("```")
        jsonStr = re.sub(r'\\[nrtbfv\'"\\]', ' ', jsonStr)
        return dict(json.loads(jsonStr))

    def logger(self, message: str, file: str = "log.txt") -> None:
        """
        Logs the generated book summary.
        """
        with open(file, "a") as f:
            f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}]: {message}\n\n")

    def renderBookHtml(self, book: dict) -> str:
        """
        Converts the generated book summary to pdf.
        """
        try:
            self.bookSummary = book["bookSummary"]
            bookCoverImg = self.generateCoverImage(self.bookSummary)
            try:
                self.cover_img_url = bookCoverImg["data"][0]["asset_url"]
            except IndexError:
                self.cover_img_url = None

            book["bookCoverImg"] = bookCoverImg
        except APIError as e:
            book["bookCoverImg"] = None

        template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        env = Environment(loader=FileSystemLoader(template_dir))
        template = env.get_template('book.html')
        renderedHtml = template.render(book)
        self.htmlContent = renderedHtml
        # with open(os.path.dirname(__file__) + "/" + "rendered.html", 'w') as f:
        #     f.write(renderedHtml)

        return renderedHtml

    def generatePdfFromHtml(self):
        """
        Generates a pdf from the html.
        """
        if (self.htmlContent is None or self.bookSummary.get("title") == None):
            raise APIError(
                "generateHtml must be called first",
                404
            )
        # Set up Chrome options
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')

        driver = webdriver.Chrome(options=chrome_options)

        encoded = parse.quote(self.htmlContent)

        pdf_bytes = b""
        file_name = f"{self.bookSummary['title'].replace(' ', '-')}_{time.time()}.pdf"

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

        self.createZipFile(book_summary=self.bookSummary, pdf_bytes=pdf_bytes,
                           cover_img_url=self.cover_img_url, filename=f"{time.time()}.zip")

        return file_name, pdf_bytes

    def generateCoverImage(self, bookSummary: dict):
        url = "https://api.limewire.com/api/image/generation"

        summary = bookSummary["summary"]
        if (len(summary) > 1800):
            summary = bookSummary["summary"][:1800]

        prompt = f"""{{ "title" : {bookSummary["title"]}, "summary" : {summary} }}"""

        payload = {
            "prompt": f"""generate cover image for book, don't put any text, here is the json of the book summary {prompt}""",
            "negative_prompt": "if prompt is not clear or contains NSFW content generate a fake image, no text in the image",
            "samples": 1,
            "quality": "LOW",
            "guidance_scale": 50,
            "aspect_ratio": "13:19",
            "style": "PHOTOREALISTIC"
        }

        key = "LIMEWIRE_KEY_"
        keyCount = 1
        token = os.getenv(f"{key}{keyCount}")
        while token:
            headers = {
                "Content-Type": "application/json",
                "X-Api-Version": "v1",
                "Accept": "application/json",
                "Authorization": f"Bearer {token}"
            }

            response = requests.post(url, json=payload, headers=headers)
            data = dict(response.json())
            keyCount += 1
            token = os.getenv(f"{key}{keyCount}")

            if data["status"] == 403 and token:
                self.logger(f"{data}")
                print(f"using next token, {keyCount}")
                continue

            if response.status_code == 200 or data["status"] == "COMPLETED":
                return data
            else:
                self.logger(f"{data}")
                raise APIError(data['detail'], data['status'])

    def createZipFile(self, book_summary: dict, pdf_bytes: bytes, cover_img_url: str, filename: str) -> str:
        """
        Creates a zip file of the generated book summary and pdf.
        """

        path = os.path.join(os.getcwd(), "output")
        if not os.path.exists(path):
            os.makedirs(path)

        with zipfile.ZipFile(f"{path}/{filename}", 'w') as zip_file:
            zip_file.writestr(f'{filename}_metadata.json', json.dumps(book_summary))
            zip_file.writestr(f'{filename}_book.pdf', pdf_bytes)

            if cover_img_url:
                response = requests.get(cover_img_url)
                if response.status_code == 200:
                    zip_file.writestr(f'{filename}_cover.jpg', response.content)

        return filename