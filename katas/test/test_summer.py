import unittest
from katas.summer import summer


class TestSummerL1(unittest.TestCase):

    def test_integers(self):
        result = summer([1, 2, 3, 4, 5])
        self.assertEqual(result, 15)

    def test_nested_lists(self):
        result = summer([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10], []])
        self.assertEqual(result, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

    def test_mixed_types(self):
        result = summer([1, 2, 'three', [4, 5]])
        self.assertIsNone(result)

    def test_empty_list(self):
        result = summer([])
        self.assertIsNone(result)

    def test_floats(self):
        result = summer([1.5, 2.5, 3.5])
        self.assertEqual(result, 7.5)

    def test_strings(self):
        result = summer(['hello', ' ', 'world'])
        self.assertEqual(result, 'hello world')

    def test_sets(self):
        result = summer([{1, 2, 3}, {4, 5, 6}, {7, 8, 9}])
        self.assertEqual(result, {1, 2, 3, 4, 5, 6, 7, 8, 9})


if __name__ == '__main__':
    unittest.main()
