import unittest
from katas.palindrome import palindrome_num


class TestPalindromeNumL1(unittest.TestCase):
    def test_palindrome_num_true(self):
        num = 12221
        expected_result = True
        self.assertEqual(palindrome_num(num), expected_result)

    def test_palindrome_num_false(self):
        num = 577
        expected_result = False
        self.assertEqual(palindrome_num(num), expected_result)

    def test_palindrome_single_digit(self):
        num = 0
        expected_result = True
        self.assertEqual(palindrome_num(num), expected_result)


if __name__ == '__main__':
    unittest.main()
