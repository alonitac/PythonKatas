import unittest
from katas.start_end_v2 import start_end_v2


class TestStartEndV2L2(unittest.TestCase):

    def test_valid_input(self):
        result = start_end_v2('Elvis has left the building', 3, 4)
        self.assertEqual(result, 'Elvding')

    def test_negative_n_and_m(self):
        result = start_end_v2('Testing negative n and m', -2, -4)
        self.assertIsNone(result)

    def test_non_integer_n_and_m(self):
        result = start_end_v2('Non-integer n and m', 'abc', 'def')
        self.assertIsNone(result)

    def test_large_n_and_m(self):
        result = start_end_v2('Non-integer n and m', 554, 67)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
