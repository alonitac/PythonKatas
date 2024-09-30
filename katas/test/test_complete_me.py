import unittest
from katas.complete_me import manipulate_data


class TestManipulateDataL1(unittest.TestCase):

    def test_manipulate_data_normal_sentence(self):
        result = manipulate_data('We shall fight on the beaches')
        self.assertEqual(result, ('WE', 'BEACHES THE ON FIGHT SHALL WE'))


if __name__ == '__main__':
    unittest.main()
