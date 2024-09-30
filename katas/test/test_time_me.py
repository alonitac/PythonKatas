import time
import unittest
from katas.time_me import time_me


class TestTimeMeL3(unittest.TestCase):

    def test_time_me_with_sleep(self):
        def sleep_function():
            time.sleep(0.5)

        average_time = time_me(sleep_function)
        self.assertAlmostEqual(average_time, 500, delta=10)

    def test_time_me_with_fast_function(self):
        def fast_function():
            pass

        average_time = time_me(fast_function)
        self.assertAlmostEqual(average_time, 0, delta=1)


if __name__ == '__main__':
    unittest.main()
