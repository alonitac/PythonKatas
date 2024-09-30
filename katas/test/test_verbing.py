import unittest
from katas.verbing import verbing


class TestVerbingL1(unittest.TestCase):
    def test_verbing(self):
        self.assertEqual(verbing('walk'), 'walking')
        self.assertEqual(verbing('swimming'), 'swimmingly')
        self.assertEqual(verbing('do'), 'do')


if __name__ == '__main__':
    unittest.main()
