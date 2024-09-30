import unittest
from katas.is_valid_email import is_valid_email


class TestIsValidEmailL1(unittest.TestCase):
    def test_valid_email(self):
        result = is_valid_email('john.johnson@gmail.com')
        self.assertTrue(result)

    def test_invalid_email_missing_at(self):
        result = is_valid_email('john.johnsongmail.com')
        self.assertFalse(result)

    def test_invalid_email_invalid_characters(self):
        result = is_valid_email('john^johnson@gmail.com')
        self.assertFalse(result)

    def test_invalid_email_invalid_domain(self):
        result = is_valid_email('john.johnson@invalid-domainee43212343212.com')
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
