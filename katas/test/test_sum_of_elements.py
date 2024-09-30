import unittest
from katas.sum_of_elements import sum_of_element


class TestSumOfElementsL1(unittest.TestCase):
    def test_sum_of_element(self):
        elements = [1, 2, 3, 4, 5, 6]
        expected_result = 21
        self.assertEqual(sum_of_element(elements), expected_result)

    def test_empty(self):
        elements = []
        expected_result = 0
        self.assertEqual(sum_of_element(elements), expected_result)


if __name__ == '__main__':
    unittest.main()
