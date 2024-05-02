from typing import List
from mongo_database import mongodb_connection, random_words_collection


def random_words_generator(words_list: List[str]) -> None:
    for word in words_list:
        document = {
            "word": word,
        }
        inserted_id = mongodb_connection.insert_document(
            random_words_collection, document
        )
