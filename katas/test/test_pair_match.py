import unittest
from katas.pair_match import pair_match


class TestPairMatchL1(unittest.TestCase):

    def test_single_pair(self):
        men = {"John": 20}
        women = {"July": 18}
        self.assertEqual(pair_match(men, women), ("John", "July"))

    def test_multiple_pairs(self):
        men = {"John": 20, "Abraham": 45}
        women = {"July": 18, "Kim": 26}
        self.assertEqual(pair_match(men, women), ("John", "July"))

    def test_tie_age_difference(self):
        men = {"John": 20, "Abraham": 23}
        women = {"July": 18, "Kim": 26, "Linda": 25}
        self.assertIn(pair_match(men, women), [("John", "July"), ("Abraham", "Linda")])


if __name__ == '__main__':
    unittest.main()
