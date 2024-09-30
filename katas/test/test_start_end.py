import unittest
from katas.start_end import start_end


class TestStartEndL1(unittest.TestCase):

    def test_start_end(self):
        result = start_end("abcdefgh", 2, 2)
        self.assertEqual(result, "abgh")

    def test_start_end_n_zero(self):
        result = start_end("abcdefgh", 0, 2)
        self.assertEqual(result, "gh")

    def test_start_end_m_zero(self):
        result = start_end("abcdefgh", 3, 0)
        self.assertEqual(result, "abc")

    def test_start_end_n_m_zero(self):
        result = start_end("abcdefgh", 0, 0)
        self.assertEqual(result, "")


if __name__ == '__main__':
    unittest.main()
