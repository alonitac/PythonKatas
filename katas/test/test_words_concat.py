import unittest
from katas.words_concat import words_concatenation


class TestWordsConcatenationL1(unittest.TestCase):
    def test_words_concatenation(self):
        words = ['take', 'me', 'home']
        expected_result = 'take me home'
        self.assertEqual(words_concatenation(words), expected_result)

    def test_empty(self):
        words = []
        expected_result = ''
        self.assertEqual(words_concatenation(words), expected_result)


if __name__ == '__main__':
    unittest.main()
