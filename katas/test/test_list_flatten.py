import unittest
from katas.list_flatten import list_flatten


class TestListFlattenL3(unittest.TestCase):
    def test_list_flatten(self):
        result = list_flatten([1, 2, [3, 4, [4, 5], 7], 8])
        expected = [1, 2, 3, 4, 4, 5, 7, 8]
        self.assertEqual(result, expected)

    def test_empty(self):
        result = list_flatten([[[]], []])
        expected = []
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
