import unittest
from unittest.mock import patch, MagicMock
from requests import HTTPError
from katas.custom_exceptions import get_public_repositories


class TestGetPublicRepositoriesL2(unittest.TestCase):
    def test_get_public_repositories_success(self):
        repositories = get_public_repositories('pallets')
        self.assertIn('flask', repositories)
        self.assertIn('jinja', repositories)
        self.assertIn('click', repositories)

    def test_get_public_repositories_user_not_found(self):
        from katas.custom_exceptions import UserNotFoundException

        with self.assertRaises(UserNotFoundException):
            get_public_repositories('1111111111111111111111111111111111111111111')

    @patch('requests.get')
    def test_get_public_repositories_rate_limit_exceeded(self, mock_get):
        from katas.custom_exceptions import RateLimitExceededException

        mock_response = MagicMock()
        mock_response.status_code = 403
        mock_get.return_value = mock_response

        with self.assertRaises(RateLimitExceededException):
            get_public_repositories('testuser')

    @patch('requests.get')
    def test_get_public_repositories_generic_exception(self, mock_get):
        from katas.custom_exceptions import GitHubApiException

        mock_get.side_effect = HTTPError("API is not available", response=MagicMock(status_code=500))

        with self.assertRaises(GitHubApiException):
            get_public_repositories('testuser')


if __name__ == '__main__':
    unittest.main()
