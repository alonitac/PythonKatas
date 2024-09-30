import unittest
from katas.merge_dicts_v2 import merge_dicts_v2


class TestMergeDictsV2L2(unittest.TestCase):

    def test_empty_dicts(self):
        self.assertEqual(merge_dicts_v2(), {})

    def test_single_dict(self):
        self.assertEqual(merge_dicts_v2({'a': 1}), {'a': 1})

    def test_merge_dicts(self):
        dict1 = {'a': 1, 'b': 99}
        dict2 = {'b': 2, 'c': 6}
        dict3 = {'d': 42}
        self.assertEqual(merge_dicts_v2(dict1, dict2, dict3), {'a': 1, 'b': 2, 'c': 6, 'd': 42})

    def test_dict2_empty(self):
        dict1 = {'a': 1, 'b': 99}
        dict2 = {}
        self.assertEqual(merge_dicts_v2(dict1, dict2), {'a': 1, 'b': 99})

    def test_dict1_empty(self):
        dict1 = {}
        dict2 = {'b': 2, 'c': 6}
        self.assertEqual(merge_dicts_v2(dict1, dict2), {'b': 2, 'c': 6})


if __name__ == '__main__':
    unittest.main()
