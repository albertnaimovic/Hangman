from typing import Optional
from mongo_db import collection
from random import choice


class Hangman:
    def __init__(self) -> None:
        self.secret_word = self.get_secret_word()
        self.wrong_attempts = 6
        self.all_attempts = 10
        self.user_word = "_" * len(self.secret_word)
        self.used_letters = []

    def get_secret_word(self) -> str:
        response = collection.find({}, {"_id": 0})
        words_list = [x["word"] for x in response]
        return choice(words_list)

    def display_word(self) -> str:
        return self.user_word

    def update_word(self, letter: str) -> None:
        indices = [i for i, x in enumerate(self.secret_word) if x == letter]
        for i in indices:
            self.user_word = self.user_word[:i] + letter + self.user_word[i + 1 :]

    def get_game_result(self) -> Optional[str]:
        if self.secret_word == self.user_word:
            return "You've won !!!"
        elif self.all_attempts == 0 or self.wrong_attempts == 0:
            return "You've lost !!!"
        return

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
