DB_NAME = "aibooks"
TABLES = {}

TABLES["bookdata"] = (
    "CREATE TABLE `bookmetadata` ("
    "  `id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `title` TEXT NOT NULL,"
    "  `summary` TEXT NOT NULL,"
    "  `genre` TEXT NOT NULL,"
    "  `totalChapters` int(11) NOT NULL,"
    "  `coverImageUrl` TEXT,"
    "  `coverImagePublicId` TEXT,"
    "  `pdfUrl` TEXT NOT NULL,"
    "  `pdfPublicId` TEXT NOT NULL,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")