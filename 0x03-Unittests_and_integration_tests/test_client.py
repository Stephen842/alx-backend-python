#!/usr/bin/env python3
"""Unit tests for client.GithubOrgClient"""

import unittest
from parameterized import parameterized
from unittest.mock import patch

from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """TestCase for GithubOrgClient"""

    @patch("client.get_json")
    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the expected result"""
        expected_payload = {"login": org_name}
        mock_get_json.return_value = expected_payload

        client = GithubOrgClient(org_name)
        result = client.org

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, expected_payload)
