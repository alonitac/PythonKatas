import unittest
from katas.merge_sorted_lists import merge_sorted_lists


class TestMergeSortedListsL1(unittest.TestCase):
    def test_merge_sorted_lists(self):
        lst1 = [1, 4, 9, 77, 13343]
        lst2 = [-7, 0, 7, 23]
        expected_result = [-7, 0, 1, 4, 7, 9, 23, 77, 13343]
        self.assertEqual(merge_sorted_lists(lst1, lst2), expected_result)

    def test_empty(self):
        lst1 = []
        lst2 = [-7, 0, 7, 23]
        expected_result = [-7, 0, 7, 23]
        self.assertEqual(merge_sorted_lists(lst1, lst2), expected_result)


if __name__ == '__main__':
    unittest.main()
