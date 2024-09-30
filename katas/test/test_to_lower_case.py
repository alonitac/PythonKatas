import unittest
from katas.to_lower_case import to_lower_case


class TestToLowerCaseL1(unittest.TestCase):

    def test_to_lower_case(self):
        # Test case where the sentence is in uppercase
        result = to_lower_case("HELLO WORLD")
        self.assertEqual(result, "hello world", "Incorrect conversion to lowercase")

    def test_to_lower_case_empty_string(self):
        # Test case with an empty string
        result = to_lower_case("")
        self.assertEqual(result, "", "Incorrect conversion for an empty string")


if __name__ == '__main__':
    unittest.main()
