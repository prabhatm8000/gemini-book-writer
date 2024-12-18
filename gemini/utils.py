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
from PIL import Image
from io import BytesIO


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
        jsonStr = re.sub(r'\\[nrtbfv\'"\\]', '', jsonStr)
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
            if self.generateCoverImageLimewire(self.bookSummary):
                book["bookCoverImg"] = "http://localhost:5000/static/images/cover.jpg"
            else:
                book["bookCoverImg"] = "https://res.cloudinary.com/dtapvbbzb/image/upload/v1730986074/aibooks/covers/ilkmj3sgqqx6ker4u6kz.jpg"
        except APIError as e:
            book["bookCoverImg"] = "https://res.cloudinary.com/dtapvbbzb/image/upload/v1730986074/aibooks/covers/ilkmj3sgqqx6ker4u6kz.jpg"

        self.cover_img_url = book["bookCoverImg"]

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

        self.createZipFile(pdf_bytes=pdf_bytes, filename=f"{time.time()}.zip")
        return file_name, pdf_bytes

    def generateCoverImageLimewire(self, bookSummary: dict) -> bool:
        url = "https://api.limewire.com/api/image/generation"

        summary = bookSummary["summary"]
        if (len(summary) > 1800):
            summary = bookSummary["summary"][:1800]

        prompt = f"""{{ "title" : {bookSummary["title"]}, "summary" : {summary} }}"""

        payload = {
            "prompt": f"""generate cover image for book, there is the json of the book summary {prompt}""",
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
                imgUrl = data["data"][0]["asset_url"]
                imgBuffer = self.getImageFromUrlAndCompress(imgUrl)
                with open(os.path.join(os.getcwd(), "static", "images", "cover.jpg"), "wb") as f:
                    f.write(imgBuffer)
                return True
            else:
                self.logger(f"{data}")
                return False

        return False

    def createZipFile(self, pdf_bytes: bytes, filename: str) -> str:
        """
        Creates a zip file of the generated book summary and pdf.
        """

        path = os.path.join(os.getcwd(), "output")
        if not os.path.exists(path):
            os.makedirs(path)

        with zipfile.ZipFile(f"{path}/{filename}", 'w') as zip_file:
            zip_file.writestr(f'{filename}_metadata.json',
                              json.dumps(self.bookSummary))
            zip_file.writestr(f'{filename}_book.pdf', pdf_bytes)

            if self.cover_img_url.find("cover.jpg") > -1:
                with open(os.path.join(os.getcwd(), "static", "images", "cover.jpg"), "rb") as f:
                    imgBytes = f.read()
                    zip_file.writestr(f'{filename}_cover.jpg', imgBytes)

        return filename

    def getImageFromUrlAndCompress(self, img_url: str, reduction: float = 0.5) -> str:
        try:
            response = requests.get(img_url)
            if response.status_code != 200:
                raise APIError("Failed to download image",
                               response.status_code)

            image = Image.open(BytesIO(response.content))
            width, height = image.size
            new_width = int(width * (1 - reduction))
            new_height = int(height * (1 - reduction))
            resized_image = image.resize((new_width, new_height))

            buffered = BytesIO()
            resized_image.save(buffered, format="JPEG")
            img_bytes = buffered.getvalue()
            return img_bytes
        except Exception as e:
            raise APIError("shit happened in getImageFromUrlAndCompress", 500)
