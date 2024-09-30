import unittest
from katas.reverse_words_concat import reverse_words_concatenation


class TestReverseWordsConcatenationL2(unittest.TestCase):
    def test_reverse_words_concatenation(self):
        words = ['take', 'me', 'home']
        expected_result = 'home me take'
        self.assertEqual(reverse_words_concatenation(words), expected_result)

    def test_empty(self):
        words = []
        expected_result = ''
        self.assertEqual(reverse_words_concatenation(words), expected_result)


if __name__ == '__main__':
    unittest.main()
