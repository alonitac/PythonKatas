import os
import unittest
from katas.do_n_times import do_n_time


class TestDoNTimesL2(unittest.TestCase):
    def test_do_n_time(self):
        os.environ['C'] = '0'

        def foo():
            os.environ['C'] = str(int(os.environ['C']) + 1)
            print('foo was executed')

        do_n_time(foo, 4)
        self.assertEqual(os.environ['C'], '4')


if __name__ == '__main__':
    unittest.main()
