import unittest
from katas.strong_pass import strong_pass


class TestStrongPassL1(unittest.TestCase):
    def test_strong_pass_true(self):
        password = '##$FgC7^^5a'
        expected_result = True
        self.assertEqual(strong_pass(password), expected_result)

    def test_short(self):
        password = '12'
        expected_result = False
        self.assertEqual(strong_pass(password), expected_result)

    def test_no_digit(self):
        password = 'SDg$%^*JJHMSADSER#$R'
        expected_result = False
        self.assertEqual(strong_pass(password), expected_result)

    def test_no_lower(self):
        password = 'SF$%^*J45HMSADSER#$R'
        expected_result = False
        self.assertEqual(strong_pass(password), expected_result)

    def test_no_upper(self):
        password = '234234dfcsfgre5^%&%^&ef'
        expected_result = False
        self.assertEqual(strong_pass(password), expected_result)

    def test_no_special(self):
        password = '43545reFSDFSDFerrtdsdfeR4'
        expected_result = False
        self.assertEqual(strong_pass(password), expected_result)


if __name__ == '__main__':
    unittest.main()
