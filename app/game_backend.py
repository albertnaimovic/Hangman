secret_word = "zodis"


def hangman(
    secret_word: str,
    current_word: str,
    letter: str,
    wrong_attempts: int,
    all_attempts: int,
) -> tuple:
    if letter not in secret_word:
        wrong_attempts -= 1
    else:
        indices = [i for i, x in enumerate(secret_word) if x == letter]
        for i in indices:
            current_word = current_word[:i] + letter + current_word[i + 1 :]

    all_attempts -= 1
    return current_word, wrong_attempts, all_attempts


# def hangman(
#     secret_word: str, current_word: str, letter: str, attempts_left: int
# ) -> tuple:
#     if letter not in secret_word:
#         attempts_left -= 1
#     else:
#         indices = [i for i, x in enumerate(secret_word) if x == letter]
#         for i in indices:
#             current_word = current_word[:i] + letter + current_word[i + 1 :]
#     return current_word, attempts_left
