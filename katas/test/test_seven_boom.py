import unittest
from katas.seven_boom import seven_boom


class TestSevenBoomL1(unittest.TestCase):
    def test_seven_boom(self):
        n = 30
        expected_result = [7, 14, 17, 21, 27, 28]
        self.assertEqual(seven_boom(n), expected_result)

    def test_zero(self):
        n = 0
        expected_result = []
        self.assertEqual(seven_boom(n), expected_result)


if __name__ == '__main__':
    unittest.main()
