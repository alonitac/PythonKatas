import unittest
from katas.matrix_avg import matrix_avg


class TestMatrixAvgTestCaseL2(unittest.TestCase):
    def test_matrix_avg(self):
        result = matrix_avg([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        expected = 5
        self.assertEqual(result, expected)

        result = matrix_avg([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
        expected = 0
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
