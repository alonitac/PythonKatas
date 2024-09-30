import unittest
from katas.longest_common_prefix import longest_common_prefix


class TestLongestCommonPrefixL3(unittest.TestCase):
    def test_longest_common_prefix(self):
        result = longest_common_prefix('abcd', 'ttty')
        expected = ''
        self.assertEqual(result, expected)

        result = longest_common_prefix('The Linux kernel is an amazing software',
                                       'The Linux kernel is a mostly free and open-source, '
                                       'monolithic, modular, multitasking, Unix-like operating system kernel.')
        expected = 'The Linux kernel is a'
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
