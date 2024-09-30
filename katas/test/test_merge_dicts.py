import unittest
from katas.merge_dicts import merge_dicts


class TestMergeDictsL1(unittest.TestCase):

    def test_empty_dicts(self):
        dict1 = {}
        dict2 = {}
        self.assertEqual(merge_dicts(dict1, dict2), {})

    def test_merge_dicts(self):
        dict1 = {'a': 1, 'b': 99}
        dict2 = {'b': 2, 'c': 6}
        self.assertEqual(merge_dicts(dict1, dict2), {'a': 1, 'b': 2, 'c': 6})

    def test_dict2_empty(self):
        dict1 = {'a': 1, 'b': 99}
        dict2 = {}
        self.assertEqual(merge_dicts(dict1, dict2), {'a': 1, 'b': 99})

    def test_dict1_empty(self):
        dict1 = {}
        dict2 = {'b': 2, 'c': 6}
        self.assertEqual(merge_dicts(dict1, dict2), {'b': 2, 'c': 6})


if __name__ == '__main__':
    unittest.main()
