import unittest
from katas.best_student import best_student


class TestBestStudentL1(unittest.TestCase):

    def test_single_student(self):
        self.assertEqual(best_student({"John": 78}), "John")

    def test_multiple_students(self):
        self.assertEqual(best_student({
            "Dan": 78,
            "Jessica": 88,
            "John": 99,
            "Daniel": 65,
            "Lindsy": 95
        }), "John")

    def test_two_highest_grade(self):
        self.assertIn(best_student({
            "Dan": 78,
            "Jessica": 88,
            "John": 99,
            "Daniel": 65,
            "Lindsy": 99
        }), ["John", "Lindsy"])


if __name__ == '__main__':
    unittest.main()
