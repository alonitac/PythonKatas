import unittest
from katas.longest_common_substring import longest_common_substring


class TestLongestCommonSubstringL3(unittest.TestCase):

    def test_empty_strings(self):
        self.assertEqual(longest_common_substring('', ''), '')

    def test_no_common_substring(self):
        str1 = 'abcdefg'
        str2 = 'hijklmn'
        self.assertEqual(longest_common_substring(str1, str2), '')

    def test_partial_common_substring(self):
        str1 = 'abcdefg'
        str2 = 'bgtcdefffrrfssd'
        self.assertEqual(longest_common_substring(str1, str2), 'cdef')

    def test_complete_common_substring(self):
        str1 = 'Introduced in 1991, the Linux kernel is an amazing software'
        str2 = 'The Linux kernel is a mostly free and open-source, monolithic, modular, multitasking, Unix-like operating system kernel.'
        self.assertEqual(longest_common_substring(str1, str2), 'he Linux kernel is a')


if __name__ == '__main__':
    unittest.main()
