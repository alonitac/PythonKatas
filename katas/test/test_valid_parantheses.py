import unittest
from katas.valid_parentheses import valid_parentheses


class TestValidParenthesesL3(unittest.TestCase):

    def test_valid_parentheses(self):
        self.assertTrue(valid_parentheses('[[{()}](){}]'))

    def test_invalid_parentheses(self):
        self.assertFalse(valid_parentheses('[{]}'))

    def test_mixed_parentheses(self):
        self.assertFalse(valid_parentheses('[[{()}](){}'))

    def test_empty_string(self):
        self.assertTrue(valid_parentheses(''))


if __name__ == '__main__':
    unittest.main()
