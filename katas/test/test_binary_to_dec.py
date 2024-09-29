import unittest
from python_katas.binary_to_dec import binary_to_dec


class TestBinaryToDecL1(unittest.TestCase):
    def test_binary_to_dec_valid_input(self):
        result = binary_to_dec("001011101111011000")
        self.assertEqual(result, 48088)

    def test_binary_to_dec_invalid_input(self):
        with self.assertRaises(ArithmeticError):
            binary_to_dec("0010154431101111012000")


if __name__ == '__main__':
    unittest.main()
