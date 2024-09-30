import unittest
from katas.monotonic_array import monotonic_array


class TestMonotonicArrayL1(unittest.TestCase):
    def test_monotonic_array_increasing(self):
        lst = [1, 2, 3, 6, 8, 9]
        expected_result = True
        self.assertEqual(monotonic_array(lst), expected_result)

    def test_monotonic_array_decreasing(self):
        lst = [9, 8, 6, 3, 2, 1]
        expected_result = True
        self.assertEqual(monotonic_array(lst), expected_result)

    def test_monotonic_array_not_monotonic(self):
        lst = [1, 2, 3, 6, 8, 9, 0]
        expected_result = False
        self.assertEqual(monotonic_array(lst), expected_result)


if __name__ == '__main__':
    unittest.main()
