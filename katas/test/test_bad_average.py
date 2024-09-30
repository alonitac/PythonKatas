import unittest
from katas.bad_average import bad_average


class TestBadAverageL1(unittest.TestCase):

    def test_bad_average(self):
        # Test case where a=1, b=2, c=3
        result = bad_average(1, 2, 3)
        self.assertEqual(result, 2.0, "Incorrect average calculation")


if __name__ == '__main__':
    unittest.main()
