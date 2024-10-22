from dotenv.main import load_dotenv
import os
import google.generativeai as genai
from gemini.chatHistory import generateBookWithParamsHistory, generateBookIdeasWithParamsHistory
from gemini.utils import geminiResponseToJson, logger
import time

load_dotenv()

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
config = genai.types.GenerationConfig(
    # Only one candidate for now.
    candidate_count=1,
    temperature=1,
)

MODEL = "gemini-1.5-flash"

class GenerateBookIdeasWithParams:
    """
        Generates a book ideas with the given prompt.\n
    """

    def __init__(self):
        self.modelName = MODEL

        self.model = genai.GenerativeModel(
            self.modelName, generation_config=config)
        self.chat = self.model.start_chat(
            history=generateBookIdeasWithParamsHistory
        )

    def generateIdeas(self, prompt: str, limit: int) -> dict:
        """
            Generates ideas for the given prompt.\n
            prompt -> The prompt to generate ideas for.\n
            limit -> The number of ideas to generate.\n
            Returns dictionary containing the generated ideas.
        """

        if (len(prompt) < 1 or len(prompt) > 600):
            raise ValueError("prompt must be between 1 and 1000 characters")

        if (limit < 1 or limit > 10):
            raise ValueError("limit must be between 1 and 10")

        response = self.chat.send_message(f"""
            {{
                "prompt": {prompt},
                "noOfIdeas": {limit}
            }}
        """)

        return geminiResponseToJson(response.text)


class GenerateBookWithParams:
    """
        Generates a book with the given parameters.\n
        title, \n
        description -> short description about the how the book will be, or we can say the on what the book is based on, \n
        genre -> defines the book genre: can be equal to: comedy, thriller, romance, etc, \n
        style -> defines the writing style can be equal to: persuasive, narrative, expository, or descriptive, \n
        creativity -> out of 10 can be negative, how creative you have to be while generating the content, \n
        logic -> out of 10 can be negative, possibility of it can be true or can happen in real life. \n
    """

    def __init__(self):
        self.title = None
        self.description = None
        self.genre = None
        self.style = None
        self.chapters = None
        self.creativity = None
        self.logic = None

        self.modelName = MODEL

        self.model = genai.GenerativeModel(
            self.modelName, generation_config=config)
        self.chat = self.model.start_chat(
            history=generateBookWithParamsHistory
        )

        self.bookSummary = {}

    def checkParams(self):
        """
        Checks if the parameters are valid.
        """
        if (self.title == None or self.description == None or self.genre == None or self.style == None or self.chapters == None or self.creativity == None or self.logic == None):
            raise ValueError("all parameters must be provided")

        if (len(self.title) > 100):
            raise ValueError("title must be less than 100 characters")

        if (len(self.description) > 500):
            raise ValueError("description must be less than 500 characters")

        if (self.style not in ["persuasive", "narrative", "expository", "descriptive"]):
            raise ValueError(
                "style must be 'persuasive', 'narrative', 'expository', or 'descriptive'")

        if (self.chapters < 1 or self.chapters > 25):
            raise ValueError("chapters must be between 1 and 25")

        if (self.creativity < 0 or self.creativity > 10):
            raise ValueError("creativity must be between 0 and 10")

        if (self.logic < 0 or self.logic > 10):
            raise ValueError("logic must be between 0 and 10")

    def generateBookSummary(self, title: str, description: str, genre: str, style: str, chapters: int, creativity: int, logic: int) -> dict:
        """
        Returns the generated book summary.
        """
        self.title = title
        self.description = description
        self.genre = genre
        self.style = style
        self.chapters = chapters
        self.creativity = creativity
        self.logic = logic

        print(title, style, description, genre, chapters, creativity, logic)
        self.checkParams()


        response = self.chat.send_message(f"""
            {{
                "title": "{self.title}",
                "description": "{self.description}",
                "genre": "{self.genre}",
                "style": {self.style},
                "chapters": {self.chapters},
                "creativity": {self.creativity}/10,
                "logic": {self.logic}/10,
            }}
        """)

        self.bookSummary = geminiResponseToJson(response.text)
        self.bookSummary["genre"] = self.genre.split(",")
        return self.bookSummary

    def generateChapter(self, chapterNo: int, estimatedParagraph: int = 3, paragraphSize: str = "long") -> dict:
        """
        Generates a chapter with the given parameters.\n
        chapterNo -> chapter number that needs to be generated, \n
        estimatedParagraph -> no of paragraphs, \n
        paragraphSize -> brief, long, or very-long. \n
        Returns the generated chapter summary.
        """
        if (chapterNo < 1 or chapterNo > self.chapters):
            raise ValueError(
                f"chapterNo must be between 1 and {self.chapters}")

        if (estimatedParagraph < 1 or estimatedParagraph > 5):
            raise ValueError("estimatedParagraph must be between 1 and 5")

        if (paragraphSize not in ["brief", "long", "very-long"]):
            raise ValueError(
                "paragraphSize must be 'brief', 'long', or 'very-long'")

        try:
            self.checkParams()
        except Exception as e:
            raise Exception("generateBookSummary must be called first")

        retryCount = 0
        lastError = None
        while True:
            try:
                response = self.chat.send_message(f"""
                    {{
                        "generateChapterNo": {chapterNo},
                        "estimatedParagraph": {estimatedParagraph},
                        "paragraphSize": {paragraphSize},
                        "lastError": "got this error while parshing the response: `{lastError}` try again send valid json object"
                    }}
                """)
                res = response.text
                output = geminiResponseToJson(res)
                return output
            except Exception as e:
                error = e.__class__.__name__ + ": " + e.__str__() + " on chapter " + \
                    str(chapterNo)
                logger(error)
                lastError = error
                retryCount += 1
                time.sleep(1)

                if (retryCount == 3):
                    logger("Failed to generate chapter " + str(chapterNo))
                    raise e

    def generateAllChapters(self, estimatedParagraph: int = 3, paragraphSize: str = "long"):
        """
        Generates all the chapters after generating the book summary.\n
        estimatedParagraph -> no of paragraphs, \n
        paragraphSize -> brief, long, or very-long. \n

        Returns the generated book content.
        """

        try:
            self.checkParams()
        except Exception as e:
            raise Exception("generateBookSummary must be called first")

        if (self.bookSummary == None):
            raise Exception("generateBookSummary must be called first")

        bookContent: dict[str, str | list] = {
            "bookSummary": self.bookSummary, "bookContent": [], "author": f"gemini ({self.modelName})"}

        for chapterIndex in range(1, self.chapters + 1):
            chapter = self.generateChapter(
                chapterIndex, estimatedParagraph, paragraphSize)
            bookContent["bookContent"].append(chapter)

            yield chapter

        # return bookContent


# if __name__ == "__main__":
#     gen = GenerateBookIdeasWithParams()
#     res = gen.generateIdeas("comdey of guys school life", 5)
#     print(res)


#     gen = GenerateBookWithParams(
#         title="The last day",
#         description="A thrilling horror story of the last day of the high-school based in japan.",
#         genre="thriller,horror,mystery,high school",
#         style="expository",
#         chapters=2,
#         creativity=10,
#         logic=9,
#     )

#     res = gen.generateBookSummary()
#     print("got the summary")
#     json.dump(res, open("output.json", "w"), indent=4)

    # res = gen.generateChapter(1, 5, "very-long")
    # print("got the chapter")
    # json.dump(res, open("output1.json", "w"), indent=4)

    # chapters = []
    # for [chapterIndex, chapter] in gen.generateAllChapters(5, "very-long"):
    #     print("got the chapter", chapterIndex)
    #     chapters.append(chapter)

    # json.dump(chapters, open("output2.json", "w"), indent=4)
    # print("got all the chapters")
