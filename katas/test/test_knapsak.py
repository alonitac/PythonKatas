import unittest
from katas.knapsack import knapsack


class TestKnapsackL4(unittest.TestCase):

    def test_empty_items(self):
        result = knapsack({})
        self.assertEqual(result, set())

    def test_single_item_within_limit(self):
        items = {'book': (3, 2)}
        result = knapsack(items, knapsack_limit=5)
        self.assertEqual(result, {'book'})

    def test_single_item_exceeds_limit(self):
        items = {'table': (6, 1)}
        result = knapsack(items, knapsack_limit=5)
        self.assertEqual(result, set())

    def test_multiple_items(self):
        items = {
            'book': (3, 2),
            'television': (4, 3),
            'table': (6, 1),
            'scooter': (5, 4)
        }
        result = knapsack(items, knapsack_limit=8)
        self.assertEqual(result, {'scooter', 'book'})


if __name__ == '__main__':
    unittest.main()
