import unittest
from katas.valid_git_tree import valid_git_tree


class TestValidGitTreeL3(unittest.TestCase):

    def test_valid_git_tree_no_cycles(self):
        commits_valid = [
            ("commit1", []),
            ("commit2", ["commit1"]),
            ("commit3", ["commit2"]),
            ("commit4", ["commit2"]),
            ("commit5", ["commit3", "commit4"]),
            ("commit6", ["commit5"]),
        ]

        result = valid_git_tree(commits_valid)
        self.assertTrue(result)

    def test_valid_git_tree_with_cycles(self):
        commits_invalid_cycles = [
            ("commit1", ["commit2"]),
            ("commit2", ["commit1"]),
        ]

        result = valid_git_tree(commits_invalid_cycles)
        self.assertFalse(result)

    def test_valid_git_tree_unique_commit_ids(self):
        commits_invalid_duplicate_ids = [
            ("commit1", []),
            ("commit1", ["commit1"]),
        ]

        result = valid_git_tree(commits_invalid_duplicate_ids)
        self.assertFalse(result)

    def test_valid_git_tree_missing_parent_ids(self):
        commits_invalid_missing_parents = [
            ("commit1", []),
            ("commit2", ["commit1"]),
            ("commit3", ["commit4"]),
        ]

        result = valid_git_tree(commits_invalid_missing_parents)
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
