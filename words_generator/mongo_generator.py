from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from typing import Dict
from words_list import words_list


def connect_to_mongodb(host: str, port: int, db_name: str) -> Database:
    client = MongoClient(host, port)
    database = client[db_name]
    return database


def insert_document(collection: Collection, document: Dict) -> str:
    result = collection.insert_one(document)
    return str(result.inserted_id)


if __name__ == "__main__":
    mongodb_host = "localhost"
    mongodb_port = 27017
    database_name = "hangman"
    collection_name = "random_words"

    db = connect_to_mongodb(mongodb_host, mongodb_port, database_name)

    collection = db[collection_name]

    for word in words_list:
        document = {
            "word": word,
        }
        inserted_id = insert_document(collection, document)
        print(document)
