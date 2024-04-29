from game_backend import Hangman
import unittest
import mock


class TestHangman(unittest.TestCase):
    @mock.patch("pymongo.collection.Collection.find")
    def setUp(self, mock_find):
        mock_find.return_value = [{"word": "testas"}]
        self.hangman_test = Hangman()

    def test_random_word(self):
        self.assertEqual("testas", self.hangman_test.secret_word)

    def test_update_word(self):
        self.hangman_test.update_word(letter="t")
        self.assertEqual("t__t__", self.hangman_test.user_word)
        self.hangman_test.update_word(letter="s")
        self.assertEqual("t_st_s", self.hangman_test.user_word)

    def test_get_game_result_win(self):
        self.hangman_test.user_word = "testas"
        self.assertEqual(
            self.hangman_test.get_game_result(), "You've won !!! Secret word: testas"
        )

    def test_get_game_result_loss(self):
        self.hangman_test.all_attempts = 0
        self.assertEqual(
            self.hangman_test.get_game_result(), "You've lost !!! Secret word: testas"
        )

    def test_take_turn(self):
        self.hangman_test.take_turn("t")
        self.assertEqual(self.hangman_test.display_word(), "t__t__")

    def test_try_full_word(self):
        self.assertEqual(
            self.hangman_test.try_full_word("testas"),
            "You've won !!! Secret word: testas",
        )
        self.assertEqual(
            self.hangman_test.try_full_word("bbbb"),
            "You've lost !!! Secret word: testas",
        )


if __name__ == "__main__":
    unittest.main()
