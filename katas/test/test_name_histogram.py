import unittest
from katas.name_histogram import name_histogram


class TestNameHistogramL2(unittest.TestCase):

    def test_empty_list(self):
        result = name_histogram([])
        self.assertEqual(result, {})

    def test_single_name(self):
        result = name_histogram(["Alice"])
        self.assertEqual(result, {"Alice": 1})

    def test_multiple_names(self):
        names = ["Alice", "Bob", "Charlie", "David", "Alice", "Eva", "Bob", "Alice", "David", "Charlie", "Alice", "Eva", "Alice", "Bob", "Charlie", "Alice", "David", "Eva", "Bob", "Charlie", "David", "Alice", "Eva", "Bob", "Alice", "Charlie", "David", "Eva", "Alice", "Bob", "Charlie", "David", "Alice", "Eva", "Bob", "Alice", "Charlie", "David", "Eva", "Alice", "Bob", "Charlie", "David", "Eva", "Alice", "Bob", "Charlie", "David", "Eva", "Alice", "Bob", "Charlie"]
        result = name_histogram(names)
        expected_result = {"Alice": 14, "Bob": 10, "Charlie": 10, "David": 9, "Eva": 9}
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
