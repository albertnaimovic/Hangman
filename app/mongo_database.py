from dataclasses import dataclass
from typing import Dict, List, Optional
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.errors import PyMongoError
from pymongo.collection import Collection


@dataclass
class MongoConnect:
    host: str
    port: int
    database_name: str


class MongoDB(MongoConnect):
    def __init__(self, host: str, port: int, database_name: str) -> None:
        super().__init__(host, port, database_name)

    def connect_to_mongodb(self) -> Database:
        client = MongoClient(self.host, self.port)
        database = client[self.database_name]
        return database

    @staticmethod
    def insert_document(collection: Collection, document: Dict) -> str:
        try:
            result = collection.insert_one(document)
            return str(result.inserted_id)
        except PyMongoError as err:
            print(f"An error occured: {err}")

    @staticmethod
    def find_documents(collection: Collection, query: Dict) -> Optional[List[Dict]]:
        try:
            documents = collection.find(query, {"_id": 0})
            return list(documents)
        except PyMongoError as err:
            print(f"An error occured: {err}")


mongodb_connection = MongoDB(host="localhost", port=27017, database_name="hangman")

mongo_db = mongodb_connection.connect_to_mongodb()

random_words_collection = mongo_db["random_words"]
statistics_collection = mongo_db["statistics"]
