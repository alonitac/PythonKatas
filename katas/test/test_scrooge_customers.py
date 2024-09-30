import unittest
from katas.scrooge_customers import scrooge_customers


class TestScroogeCustomersL2(unittest.TestCase):

    def test_empty_orders(self):
        customers = {
            "c1": {"name": "Alice", "email": "alice@example.com"},
            "c2": {"name": "Bob", "email": "bob@example.com", "orders": []},
            "c3": {"name": "Charlie", "email": "charlie@example.com", "orders": []},
            "c4": {"name": "David", "email": "david@example.com", "orders": []}
        }
        result = scrooge_customers(customers)
        self.assertEqual(result, ["c1", "c2", "c3", "c4"])

    def test_no_orders_key(self):
        customers = {
            "c1": {"name": "Alice", "email": "alice@example.com"},
            "c2": {"name": "Bob", "email": "bob@example.com"},
            "c3": {"name": "Charlie", "email": "charlie@example.com"},
            "c4": {"name": "David", "email": "david@example.com"}
        }
        result = scrooge_customers(customers)
        self.assertEqual(result, ["c1", "c2", "c3", "c4"])

    def test_mixed_orders(self):
        customers = {
            "c1": {"name": "Alice", "email": "alice@example.com"},
            "c2": {"name": "Bob", "email": "bob@example.com", "orders": []},
            "c3": {"name": "Charlie", "email": "charlie@example.com", "orders": [{"order_id": 103, "product": "Widget C"}]},
            "c4": {"name": "David", "email": "david@example.com", "orders": []}
        }
        result = scrooge_customers(customers)
        self.assertEqual(result, ["c1", "c2", "c4"])


if __name__ == '__main__':
    unittest.main()
