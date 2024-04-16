from words_list import words_list
from mongo_database import mongodb_connection, random_words_collection


if __name__ == "__main__":
    for word in words_list:
        document = {
            "word": word,
        }
        inserted_id = mongodb_connection.insert_document(
            random_words_collection, document
        )
        print(document)
