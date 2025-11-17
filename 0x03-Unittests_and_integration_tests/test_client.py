#!/usr/bin/env python3
"""Unit tests for client.GithubOrgClient"""

import unittest
from parameterized import parameterized
from unittest.mock import patch

from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """TestCase for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the expected result"""
        expected = {"login": org_name}
        mock_get_json.return_value = expected

        client = GithubOrgClient(org_name)
        result = client.org

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, expected)

    # Task 5
    def test_public_repos_url(self):
        """Test that _public_repos_url returns correct URL from org"""
        # Mock payload for org property
        mock_payload = {
            "repos_url": "https://api.github.com/orgs/google/repos"
        }

        client = GithubOrgClient("google")

        # Patch the org property of this client instance
        with patch.object(
            GithubOrgClient,
            "org",
            new_callable=property,
            return_value=mock_payload
        ):
            result = client._public_repos_url
            self.assertEqual(result, mock_payload["repos_url"])

    # Task 6: More patching
    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns correct list of repo names"""
        fake_url = "https://api.github.com/orgs/google/repos"
        payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"}
        ]
        mock_get_json.return_value = payload

        client = GithubOrgClient("google")

        with patch.object(
            GithubOrgClient,
            "_public_repos_url",
            new_callable=property,
            return_value=fake_url
        ) as mock_url:
            result = client.public_repos()

            self.assertEqual(result, ["repo1", "repo2", "repo3"])
            mock_get_json.assert_called_once_with(fake_url)
            mock_url.assert_called_once()
            