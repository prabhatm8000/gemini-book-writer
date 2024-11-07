import json
import os

import cloudinary
import cloudinary.api
import cloudinary.uploader
import dotenv

import zipfile

from pymongo import MongoClient
from Scheme import DB_NAME

dotenv.load_dotenv()

client = MongoClient(os.environ.get("MONGODB_URI"))

cloudinary.config(
    cloud_name=os.environ.get("CLOUDINARY_CLOUD_NAME"),
    api_key=os.environ.get("CLOUDINARY_API_KEY"),
    api_secret=os.environ.get("CLOUDINARY_API_SECRET"),
    secure=True
)

try:
    db = client[DB_NAME]
    print("Connected to Database")

    collections = db.list_collection_names()
    if "bookdata" not in collections:
        db.create_collection("bookdata")

    collection = db["bookdata"]
    print("Got the collection")
except Exception as e:
    print(e)


def addBookDataJsonDocsMany(bookDataJsonDocs: list[dict[str, str]]):
    print("Uploading to DB")
    collection.insert_many(bookDataJsonDocs)
    print("{} book data docs uloaded to DB".format(len(bookDataJsonDocs)))


# region unzipping & parsing & uploading
def unzip(file_name: str, extract_dir=os.path.join(os.getcwd(), "uploadbooks", "temp")) -> list[str]:
    files = []
    with zipfile.ZipFile(file_name, 'r') as zip_ref:
        files = zip_ref.namelist()
        zip_ref.extractall(extract_dir)
    return files


def parseAndUploadFiles(files: list[str]) -> dict[str, str]:
    bookdata = {}
    for file in files:
        upload = {}
        if file.endswith(".json"):
            jsonData: dict = json.load(
                open(os.path.join(os.getcwd(), "uploadbooks", "temp", file)))

            bookdata["title"] = jsonData.get("title", "")
            bookdata["summary"] = jsonData.get("summary", "")
            bookdata["totalChapters"] = jsonData.get("totalChapters", 0)

            bookdata["genre"] = [i.strip() for i in jsonData.get("genre", [])]

        elif file.endswith(".pdf"):
            file_path = os.path.join(os.getcwd(), "uploadbooks", "temp", file)
            upload: dict = cloudinary.uploader.upload(
                file=file_path, folder="aibooks/books", overwrite=False)

            bookdata["pdfUrl"] = upload.get(
                "secure_url", upload.get("url", ""))
            bookdata["pdfPublicId"] = upload.get("public_id", "")

        elif file.endswith(".jpg"):
            file_path = os.path.join(os.getcwd(), "uploadbooks", "temp", file)
            upload: dict = cloudinary.uploader.upload(
                file=file_path, folder="aibooks/covers", overwrite=False)

            bookdata["coverImageUrl"] = upload.get(
                "secure_url", upload.get("url", ""))
            bookdata["coverImagePublicId"] = upload.get("public_id", "")

        deleteFile(os.path.join(os.getcwd(), "uploadbooks", "temp", file))

    return bookdata


def getAllFilesInOutputFolder() -> list[str]:
    files = []
    for root, dirs, filenames in os.walk(os.path.join(os.getcwd(), "output")):
        for filename in filenames:
            files.append(os.path.join(root, filename))
    return files


def deleteFile(path):
    if os.path.exists(path):
        os.remove(path)


def doTheThing():
    zipFiles = getAllFilesInOutputFolder()
    bookDataJsonDocs = []
    try:
        for file in zipFiles:
            extractFiles = unzip(file)
            bookdata = parseAndUploadFiles(extractFiles)
            bookDataJsonDocs.append(bookdata)
            print("Uploaded book zip:", file)
            deleteFile(file)

        addBookDataJsonDocsMany(bookDataJsonDocs)
    except Exception as e:
        with open("bookDataCatch.json", "w") as f:
            json.dump(bookDataJsonDocs, f)

        print(e)


# endregion

doTheThing()
