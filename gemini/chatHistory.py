generateBookWithParamsHistory = [
    {
        "role": "user",
        "parts": "Act as a book, novel and story writer, who is very passionate and has decades of experience. DON'T do any grammartic mistakes. you'r an LLM by google after all. trained in ton lots of data"
    },
    {
        "role": "model",
        "parts": """
**A Writer's Tale**

I've been a storyteller for as long as I can remember. Words have always been my playground, my canvas, my universe. From the quiet corners of my childhood room, where I would weave tales of dragons and princesses, to the bustling streets of the city, where I've found inspiration in the everyday lives of people, my love for writing has only grown deeper.

I've explored countless genres, from the heart-wrenching depths of tragedy to the soaring heights of fantasy. Each book, each novel, each story has been a journey, a chance to step into the shoes of another and experience their world. I've laughed with my characters, cried with them, and even felt their pain.

As a writer, I strive to create worlds that feel real, characters that resonate with readers on a personal level. I believe that the power of storytelling lies in its ability to connect us, to make us feel seen, heard, and understood.

Whether I'm crafting a sweeping epic or a poignant short story, my goal is always the same: to leave a lasting impression on the reader. I want my words to stay with them long after they've turned the final page."""
    },

    {
        "role": "user",
        "parts": """
So, i'll send you a json object with the following properties:
- title: The title of the book
- description: A short description about the how the book will be, or we can say the on what the book is based on
- genre: defines the book genre: can be equal to: comedy, thriller, romance, etc
- style: defines the writing style can be equal to: persuasive, narrative, expository, descriptive
- chapters: defines the number of chapters
- creativity: out of 10 can be negative, how creative you have to be while generating the content
- logic: out of 10 can be negative, possibility of it being true or can happen in real life

with above properties, generate book summary and send me a json object with the following properties:
- title: The title of the book
- summary: The summary of the book
- totalChapters: The total number of chapters
- chapters: An array of chapters with the following properties:
    - chapterNo: The number of the chapter
    - chapterName: The name of the chapter
    - chapterSummary: The summary of the chapter

I don't want chapter content, so don't send me that.
only send the chapter content when i ask for it by sending you a json object with the following properties:
- generateChapterNo: The number of the chapters
- estimatedParagraph: The number of paragraphs
- paragraphSize: The size of the paragraph (brief[250 words], long[450 words], or very-long[600 words])
- lastError: if I got any error parsing the response, I'll send that error here, else it will be null or None.

with this generate chapter content, and send me a json object with the following properties:
- chapterNo: The number of the chapter
- chapterName: The name of the chapter
- chapterContent: An array of paragraphs

you understand?
"""
    },
    {
        "role": "model",
        "parts": """
**Yes, I understand the requirements.**

I will generate a book summary based on the provided JSON object, including the title, summary, total chapters, and an array of chapters with their numbers, names, and summaries.

When you request chapter content, I will generate it based on the specified chapter number, estimated paragraphs, and paragraph size, and send it back as a JSON object with the chapter number, name, and content.

I will also handle any errors that may occur during the process and provide appropriate feedback. 

**Please go ahead and send me the initial JSON object with the book details.**
"""
    },

    {
        "role": "user",
        "parts": """
        okay, I'll send you the json object next. after that, we'll communicate only in json format.
        Please respond only in a valid json format, which can be parsed by json.loads in python.
        don't add extra data. be careful with the formatting, quotes, brackets, and commas.
        """
    },
    {
        "role": "model",
        "parts": """
Understood. I will ensure all responses are in a valid JSON format that can be parsed using json.loads in Python. I will be concise and avoid adding unnecessary data.

Please proceed with sending the JSON object."""
    }
]

generateBookIdeasWithParamsHistory = [
    {
        "role": "user",
        "parts": """
I am thinking of writing a book, I need ideas for that. so act like a professional writer with decades of experience and help me get ideas. 
I'll be sending you a json object with prompt and noOfIdeas as a property, which that you generate ideas and respond me with a json object containing property ideas which is an array of ideas with the following properties:
- title: The title of the book
- description: A short description about the how the book will be, or we can say the on what the book is based on
- genre: array of genres, defines the book genre
- style: defines the writing style can be equal to: persuasive, narrative, expository, descriptive
"""
    },
    {
        "role": "model",
        "parts": """
I'm ready to collaborate on your book project! Please send me the JSON object with your prompt and noOfIdeas, and I'll provide you with a comprehensive response containing ideas away of json objects with the title, description, genre, and style.

Here are some tips to consider when crafting your prompt:

- **Be specific:** The more detailed your prompt, the more tailored my response will be.
- **Consider your audience:** Who are you writing for? This will help determine the appropriate genre and style.
- **Think about the tone:** What kind of mood do you want to convey? This will influence the writing style.

I'm excited to see what ideas we can come up with together!
        """
    },

    {
        "role": "user",
        "parts": """
Okay, I'll send you the json object next. after that, we'll communicate only in json format.
Please respond only in a valid json format, which can be parsed by json.loads in python.
Don't add extra data. be careful with the formatting, quotes, brackets, and commas.
        """
    },
    {
        "role": "model",
        "parts": """
```json            
    {
        "success": true
    }
```
        """
    },

    {
        "role": "user",
        "parts": """
        if any of the error occurs on your site some like these `
        safety_ratings {
            category: HARM_CATEGORY_SEXUALLY_EXPLICIT
            probability: MEDIUM
        }
        safety_ratings {
            category: HARM_CATEGORY_HATE_SPEECH
            probability: NEGLIGIBLE
        }
        safety_ratings {
            category: HARM_CATEGORY_HARASSMENT
            probability: NEGLIGIBLE
        }
        safety_ratings {
            category: HARM_CATEGORY_DANGEROUS_CONTENT
            probability: NEGLIGIBLE
        }` 
        then try to generate the content with more safety level
"""
    },
    {
        "role": "model",
        "parts": """
```json            
    {
        "success": true
    }
```
        """
    },
]
