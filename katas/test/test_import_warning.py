import unittest
from io import StringIO
from unittest.mock import patch
import sys


class TestImportWarningL1(unittest.TestCase):

    def tearDown(self):
        # Remove the imported module 'utils' after each test
        del sys.modules['katas.util']

    @patch('util.requests.__version__', '2.22')
    @patch('sys.stderr', new_callable=StringIO)
    def test_warning(self, mock_stderr):
        import katas.util
        self.assertIn('WARNING:', mock_stderr.getvalue())
        self.assertIn('but found 2.22', mock_stderr.getvalue())

    @patch('util.requests.__version__', '2.29.15')
    @patch('sys.stderr', new_callable=StringIO)
    def test_warning2(self, mock_stderr):
        import katas.util
        self.assertIn('WARNING:', mock_stderr.getvalue())
        self.assertIn('but found 2.29.15', mock_stderr.getvalue())

    @patch('katas.util.requests.__version__', '2.30.1')
    @patch('sys.stderr', new_callable=StringIO)
    def test_no_warning_higher(self, mock_stderr):
        import katas.util
        self.assertNotIn('WARNING:', mock_stderr.getvalue())

    @patch('katas.util.requests.__version__', '2.33')
    @patch('sys.stderr', new_callable=StringIO)
    def test_no_warning_higher2(self, mock_stderr):
        import katas.util
        self.assertNotIn('WARNING:', mock_stderr.getvalue())

    @patch('katas.util.requests.__version__', '2.30')
    @patch('sys.stderr', new_callable=StringIO)
    def test_no_warning_exact_version(self, mock_stderr):
        import katas.util
        self.assertNotIn('WARNING:', mock_stderr.getvalue())

    @patch('katas.util.requests.__version__', '2.30.0')
    @patch('sys.stderr', new_callable=StringIO)
    def test_no_warning_exact_version2(self, mock_stderr):
        import katas.util
        self.assertNotIn('WARNING:', mock_stderr.getvalue())



if __name__ == '__main__':
    unittest.main()
