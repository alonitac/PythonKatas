import unittest
from katas.ceaser_cipher import caesar_cipher


class TestCaesarCipherL2(unittest.TestCase):
    def test_caesar_cipher(self):
        str_to_encrypt = 'Fly Me To The Moon'
        expected_result = 'Iob Ph Wr Wkh Prrq'
        self.assertEqual(caesar_cipher(str_to_encrypt), expected_result)

    def test_empty(self):
        str_to_encrypt = ''
        expected_result = ''
        self.assertEqual(caesar_cipher(str_to_encrypt), expected_result)


if __name__ == '__main__':
    unittest.main()
