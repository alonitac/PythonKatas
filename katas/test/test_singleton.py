import unittest
from katas.singleton import Singleton


class TestSingletonL3(unittest.TestCase):

    def test_singleton_instance(self):
        s1 = Singleton.get_instance()
        s2 = Singleton.get_instance()
        self.assertIsInstance(s1, Singleton)
        self.assertIsInstance(s2, Singleton)
        self.assertIs(s1, s2)

    def test_constructor_error(self):
        with self.assertRaises(RuntimeError):
            s = Singleton()


if __name__ == '__main__':
    unittest.main()
