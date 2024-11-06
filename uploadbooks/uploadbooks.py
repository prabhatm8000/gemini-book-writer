import json
import os

import cloudinary
import cloudinary.api
import cloudinary.uploader
import dotenv
import mysql.connector
from mysql.connector import errorcode
from Scheme import DB_NAME, TABLES
import zipfile

dotenv.load_dotenv()
# region database&table creation
config = {
    "user": os.getenv("AIVEN_MYSQL_USER"),
    "password": os.getenv("AIVEN_MYSQL_PASSWORD"),
    "host": os.getenv("AIVEN_MYSQL_HOST"),
    "port": os.getenv("AIVEN_MYSQL_PORT"),
    "database": os.getenv("AIVEN_MYSQL_DB_NAME")
}

mydb = None
try:
    mydb = mysql.connector.connect(
        **config
    )
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        raise (err)

cursor = mydb.cursor()

try:
    cursor.execute(
        f"CREATE DATABASE {DB_NAME} DEFAULT CHARACTER SET 'utf8'")
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_DB_CREATE_EXISTS:
        print("Database {} already exists.".format(DB_NAME))
    else:
        print("Failed creating database: {}".format(err))
        exit(1)


try:
    cursor.execute(f"USE {DB_NAME}")
except mysql.connector.Error as err:
    print("Database {} does not exists.".format(DB_NAME))
    print(err)
    exit(1)

try:
    for table_name in TABLES:
        table_description = TABLES[table_name]
        cursor.execute(table_description)
        print("Creating table {}: ".format(table_name), end='')
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
        print("table {} already exists.".format(table_name))
    else:
        print(err.msg)

mydb.commit()

def addBookData(bookdata: dict[str, str]):
    try:
        cursor.execute(
            "INSERT INTO bookmetadata (title, summary, genre, totalChapters, coverImageUrl, coverImagePublicId, pdfUrl, pdfPublicId) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (
                bookdata["title"],
                bookdata["summary"],
                bookdata["genre"],
                bookdata["totalChapters"],
                bookdata["coverImageUrl"],
                bookdata["coverImagePublicId"],
                bookdata["pdfUrl"],
                bookdata["pdfPublicId"],
            )
        )
        mydb.commit()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_DUP_ENTRY:
            print("Book already exists.")
        else:
            print(err)
# endregion

# region unzipping & parsing
def unzip(file_name: str, extract_dir=os.path.join(os.getcwd(), "uploadbooks", "temp")) -> list[str]:
    files = []
    with zipfile.ZipFile(file_name, 'r') as zip_ref:
        files = zip_ref.namelist()
        zip_ref.extractall(extract_dir)
    return files

def parseAndUploadFiles(files: list[str]) -> dict[str, str]:
    bookdata = {}
    for file in files:
        if file.endswith(".json"):
            jsonData: dict = json.load(
                open(os.path.join(os.getcwd(), "uploadbooks", "temp", file)))
            
            bookdata["genre"] = jsonData.get("genre", "")
            bookdata["title"] = jsonData.get("title", "")
            bookdata["summary"] = jsonData.get("summary", "")
            bookdata["totalChapters"] = jsonData.get("totalChapters", 0)

        elif file.endswith(".pdf"):
            file_path = os.path.join(os.getcwd(), "uploadbooks", "temp", file)
            upload: dict = cloudinary.uploader.upload(
                file=file_path, folder="aibooks/books", overwrite=False)
            
            bookdata["pdfUrl"] = upload.get("secure_url", upload.get("url", ""))
            bookdata["pdfPublicId"] = upload.get("public_id", "")

        elif file.endswith(".jpg"):
            file_path = os.path.join(os.getcwd(), "uploadbooks", "temp", file)
            upload: dict = cloudinary.uploader.upload(
                file=file_path, folder="aibooks/covers", overwrite=False)
            
            bookdata["coverImageUrl"] = upload.get("secure_url", upload.get("url", ""))
            bookdata["coverImagePublicId"] = upload.get("public_id", "")

    return bookdata

def getAllFilesInOutputFolder() -> list[str]:
    files = []
    for root, dirs, filenames in os.walk(os.path.join(os.getcwd(), "output")):
        for filename in filenames:
            files.append(os.path.join(root, filename))
    return files

def deleteZipFile(path):
    os.remove(path)

def doTheThing():
    zipFiles = getAllFilesInOutputFolder()
    for file in zipFiles:
        extractFiles = unzip(file)
        bookdata = parseAndUploadFiles(extractFiles)
        addBookData(bookdata)
        print("Uploaded book zip:", file)
        deleteZipFile(file)

# endregion

doTheThing()
mydb.close()