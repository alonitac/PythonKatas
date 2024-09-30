import unittest
from katas.mypackage.mymodule import *


class TestCustomImportAllL1(unittest.TestCase):
    def test_imported_functions(self):

        self.assertTrue(callable(foo))
        self.assertTrue(callable(boo))
        with self.assertRaises(NameError):
            print(secret)


if __name__ == '__main__':
    unittest.main()
