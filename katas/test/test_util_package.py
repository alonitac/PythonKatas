import unittest
import inspect

class TestUtilPackageL1(unittest.TestCase):

    def test_util_init(self):
        import katas.util as util

        self.assertTrue(hasattr(util, '__file__'))
        util_file_path = util.__file__

        self.assertTrue(hasattr(util, 'HELLO'))
        self.assertTrue(hasattr(util, 'func_a'))
        self.assertTrue(inspect.getsourcefile(util.func_a).endswith('util/a.py'))
        self.assertTrue(hasattr(util, 'func_c'))
        self.assertTrue(inspect.getsourcefile(util.func_c).endswith('util/boo/c.py'))

        self.assertFalse(hasattr(util, 'func_b'))

        with self.assertRaises(AttributeError):
            util.func_b()


if __name__ == '__main__':
    unittest.main()
