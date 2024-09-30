import unittest
from unittest.mock import patch
from katas.unittesting import TestIsAllowedFileExtension


def bad_is_allowed_file_extension(filename):
    return True  # Always return True, which is incorrect


class TestTestIsAllowedFileExtensionL3(unittest.TestCase):

    def test_unittest(self):
        suite = unittest.TestLoader().loadTestsFromTestCase(TestIsAllowedFileExtension)
        results = unittest.TextTestRunner().run(suite)
        self.assertEqual(results.failures, [])

    @patch('katas.unittesting.is_allowed_file_extension', side_effect=bad_is_allowed_file_extension)
    def test_run_tests_with_bad_implementation(self, mock_is_allowed_file_extension):
        suite = unittest.TestLoader().loadTestsFromTestCase(TestIsAllowedFileExtension)
        results = unittest.TextTestRunner().run(suite)
        self.assertNotEqual(results.failures, [])


if __name__ == '__main__':
    unittest.main()
