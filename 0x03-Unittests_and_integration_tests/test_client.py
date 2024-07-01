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
from unittest.mock import patch
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

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
            )
        self.assertEqual(client.org, expected)
