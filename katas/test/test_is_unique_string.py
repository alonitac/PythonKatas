import unittest
from katas.is_unique_str import is_unique_string


class TestIsUniqueStringL2(unittest.TestCase):
    def test_is_unique_string(self):
        self.assertTrue(is_unique_string('abcd'))
        self.assertFalse(is_unique_string('aaabcd'))
        self.assertTrue(is_unique_string(''))
        self.assertTrue(is_unique_string('12345tgbnh'))
        self.assertFalse(is_unique_string('aasdssdsederd'))


if __name__ == '__main__':
    unittest.main()
