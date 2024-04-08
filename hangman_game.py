# secret_word = "vienas"


# def hangman(secret_word: str) -> str:
#     wrong_attempts = 6
#     all_attempts = 10
#     my_word = "_" * len(secret_word)
#     print(my_word)
#     while secret_word != my_word and all_attempts != 0:
#         letter = input("Enter letter: ")
#         if letter not in secret_word:
#             wrong_attempts -= 1
#             print(f"Wrong! {wrong_attempts} incorrect guesses remaining")
#             if wrong_attempts == 0:
#                 return "You've lost !!!"
#         else:
#             indices = [i for i, x in enumerate(secret_word) if x == letter]
#             for i in indices:
#                 my_word = my_word[:i] + letter + my_word[i + 1 :]
#         print(my_word)
#         all_attempts -= 1
#         print(f"{all_attempts} attempts left.")
#     if secret_word == my_word:
#         return "You've won !!!"
#     elif all_attempts == 0:
#         return "You've lost !!!"


# print(hangman(secret_word))


class Hangman:
    def __init__(self, secret_word: str) -> None:
        self._secret_word = secret_word
        self.my_word = "_" * len(secret_word)
        self.wrong_attempts = 6
        self.all_attempts = 10