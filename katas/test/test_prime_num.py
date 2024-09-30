import unittest
from katas.prime_num import prime_number


class TestPrimeNumberL1(unittest.TestCase):
    def test_prime_number_true(self):
        num = 5
        expected_result = True
        self.assertEqual(prime_number(num), expected_result)

    def test_prime_number_false(self):
        num = 22
        expected_result = False
        self.assertEqual(prime_number(num), expected_result)


if __name__ == '__main__':
    unittest.main()
