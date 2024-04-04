from pymongo import MongoClient
from pymongo.database import Database


def connect_to_mongodb(host: str, port: int, db_name: str) -> Database:
    client = MongoClient(host, port)
    database = client[db_name]
    return database


mongodb_host = "localhost"
mongodb_port = 27017
database_name = "hangman"
collection_name = "random_words"

db = connect_to_mongodb(mongodb_host, mongodb_port, database_name)
collection = db[collection_name]

