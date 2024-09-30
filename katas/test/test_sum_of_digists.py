import unittest
from katas.sum_of_digits import sum_of_digits


class TestSumOfDigitsL2(unittest.TestCase):
    def test_sum_of_digits(self):
        digits_str = '1223432'
        expected_result = 17
        self.assertEqual(sum_of_digits(digits_str), expected_result)

    def test_empty(self):
        digits_str = ''
        expected_result = 0
        self.assertEqual(sum_of_digits(digits_str), expected_result)

    def test_zero(self):
        digits_str = '0000'
        expected_result = 0
        self.assertEqual(sum_of_digits(digits_str), expected_result)


if __name__ == '__main__':
    unittest.main()
