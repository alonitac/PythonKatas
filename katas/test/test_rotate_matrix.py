import unittest
from katas.rotate_matrix import rotate_matrix


class TestRotateMatrixL3(unittest.TestCase):

    def test_rotate_matrix_2x5(self):
        input_matrix = [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]]
        rotated_matrix = rotate_matrix(input_matrix)
        expected_rotated_matrix = [[6, 1], [7, 2], [8, 3], [9, 4], [10, 5]]
        self.assertEqual(rotated_matrix, expected_rotated_matrix)

    def test_rotate_matrix_empty(self):
        input_matrix = []
        rotated_matrix = rotate_matrix(input_matrix)
        self.assertEqual(rotated_matrix, [])

    def test_rotate_matrix_single_row(self):
        input_matrix = [[1, 2, 3, 4, 5]]
        rotated_matrix = rotate_matrix(input_matrix)
        expected_rotated_matrix = [[1], [2], [3], [4], [5]]
        self.assertEqual(rotated_matrix, expected_rotated_matrix)


if __name__ == '__main__':
    unittest.main()
