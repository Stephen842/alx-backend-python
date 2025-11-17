#!/usr/bin/env python3
"""Unit tests for client.GithubOrgClient"""

import unittest
from parameterized import parameterized_class
from parameterized import parameterized
from unittest.mock import patch

from client import GithubOrgClient
from .fixtures import org_payload, repos_payload, expected_repos, apache2_repos


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

    def test_public_repos_url(self):
        """Test that _public_repos_url returns correct URL from org"""
        mock_payload = {
            "repos_url": (
                "https://api.github.com/orgs/google/repos"
            )
        }

        client = GithubOrgClient("google")

        with patch.object(
            GithubOrgClient,
            "org",
            new_callable=property,
            return_value=mock_payload
        ):
            result = client._public_repos_url
            self.assertEqual(result, mock_payload["repos_url"])

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

        # Patch _public_repos_url as a normal attribute, not a property
        with patch.object(GithubOrgClient, "_public_repos_url", fake_url):
            result = client.public_repos()

            self.assertEqual(result, ["repo1", "repo2", "repo3"])
            mock_get_json.assert_called_once_with(fake_url)

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test GithubOrgClient.has_license returns correct boolean"""
        client = GithubOrgClient("google")
        result = client.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos"""

    @classmethod
    def setUpClass(cls):
        """Set up patcher for requests.get before all tests"""
        cls.get_patcher = patch("client.requests.get")
        cls.mock_get = cls.get_patcher.start()

        # Use side_effect to return correct payloads based on call order
        cls.mock_get.return_value.json.side_effect = [
            cls.org_payload,
            cls.repos_payload
        ]

    @classmethod
    def tearDownClass(cls):
        """Stop patching requests.get after all tests"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns expected repo names"""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos filtered by license 'apache-2.0'"""
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos(license_key="apache-2.0"),
            self.apache2_repos
        )
