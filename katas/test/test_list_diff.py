import unittest
from katas.list_diff import list_diff


class TestListDiffL1(unittest.TestCase):
    def test_list_diff_empty_list(self):
        elements = []
        expected_result = []
        self.assertEqual(list_diff(elements), expected_result)

    def test_list_diff_normal_list(self):
        elements = [1, 2, 3, 8, 77, 0]
        expected_result = [None, 1, 1, 5, 69, -77]
        self.assertEqual(list_diff(elements), expected_result)


if __name__ == '__main__':
    unittest.main()
