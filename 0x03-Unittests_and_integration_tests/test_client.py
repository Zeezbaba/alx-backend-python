#!/usr/bin/env python3
"""In a new test_client.py file, declare the TestGithubOrgClient
(unittest.TestCase) class and implement the test_org method.
This method should test that GithubOrgClient.org returns the
correct value.Use @patch as a decorator to make sure get_json
is called once with the expected argument but make sure it is
not executed.Use @parameterized.expand as a decorator to
parametrize the test with a couple of org examples to pass to
GithubOrgClient, in this order:
    google
    abc
"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """testing"""
    @parameterized.expand([
        ("google", {"login": "google", "id": 1}),
        ("abc", {"login": "abc", "id": 2}),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, expected, mock_get_json):
        """test GithubOrgClient"""
        mock_get_json.return_value = expected
        client = GithubOrgClient(org_name)

        self.assertEqual(client.org, expected)
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}",
            )
        # self.assertEqual(client.org, expected)

    def test_public_repos_url(self):
        """Testing"""
        with patch.object(GithubOrgClient, 'org',
                          new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {
                "repos_url": "https://api.github.com/orgs/google/repos",
                }
            # client = GithubOrgClient("google")
            self.assertEqual(
                GithubOrgClient("google")._public_repos_url,
                "https://api.github.com/orgs/google/repos",
                )

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test GithubOrgClient.public_repos method"""
        mock_payload = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
            {"name": "repo3", "license": {"key": "mit"}},
        ]
        mock_get_json.return_value = mock_payload
        with patch.object(GithubOrgClient, '_public_repos_url',
                          new_callable=PropertyMock) as \
                mock_public_repos_url:
            mock_public_repos_url.return_value = \
                    "https://api.github.com/orgs/google/repos"
            client = GithubOrgClient("google")
            repos = client.public_repos()

            expected_repos = ["repo1", "repo2", "repo3"]
            self.assertEqual(repos, expected_repos)
            mock_public_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with(
                    "https://api.github.com/orgs/google/repos",
                    )


if __name__ == "__main__":
    unittest.main()
