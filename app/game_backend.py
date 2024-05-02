from typing import Optional
from mongo_database import random_words_collection
from random import choice
from pymongo.errors import PyMongoError
import logging
import logging.config


logging.config.fileConfig("logging.conf")
logger = logging.getLogger("Log")


class Hangman:
    def __init__(self) -> None:
        self.secret_word = self.get_secret_word()
        self.wrong_attempts = 6
        self.all_attempts = 10
        self.user_word = "_" * len(self.secret_word)
        self.used_letters = [""]

    def to_json(self) -> dict:
        return {
            "secret_word": self.secret_word,
            "wrong_attempts": self.wrong_attempts,
            "all_attempts": self.all_attempts,
            "user_word": self.user_word,
            "used_letters": self.used_letters,
        }

    @classmethod
    def from_json(cls, json_data: dict) -> "Hangman":
        hangman_instance = cls()
        hangman_instance.secret_word = json_data["secret_word"]
        hangman_instance.wrong_attempts = json_data["wrong_attempts"]
        hangman_instance.all_attempts = json_data["all_attempts"]
        hangman_instance.user_word = json_data["user_word"]
        hangman_instance.used_letters = json_data["used_letters"]
        return hangman_instance

    def get_secret_word(self) -> str:
        try:
            response = random_words_collection.find({}, {"_id": 0})
        except PyMongoError as err:
            logging.error(f"An error occured: {err}")
        words_list = [x["word"] for x in response]
        return choice(words_list)

    def display_word(self) -> str:
        return self.user_word

    def update_word(self, letter: str) -> None:
        indices = [i for i, x in enumerate(self.secret_word) if x == letter]
        for i in indices:
            self.user_word = self.user_word[:i] + letter + self.user_word[i + 1 :]

    def get_game_result(self) -> str:
        if self.secret_word == self.user_word:
            return f"You've won !!! Secret word: {self.secret_word}"
        elif self.all_attempts == 0 or self.wrong_attempts == 0:
            return f"You've lost !!! Secret word: {self.secret_word}"

    def take_turn(self, letter: str) -> Optional[str]:
        if letter not in self.secret_word and letter not in self.used_letters:
            self.wrong_attempts -= 1
        else:
            self.update_word(letter)
        if letter not in self.used_letters:
            self.all_attempts -= 1

        if (
            self.secret_word == self.user_word
            or self.all_attempts == 0
            or self.wrong_attempts == 0
        ):
            return self.get_game_result()
        self.used_letters.append(letter)
        return

    def try_full_word(self, full_word: str) -> str:
        self.user_word = full_word
        self.all_attempts = 0
        return self.get_game_result()
