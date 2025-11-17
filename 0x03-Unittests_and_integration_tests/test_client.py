#!/usr/bin/env python3
"""Unit tests for client.GithubOrgClient"""

import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock

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
        # Arrange: mock return value
        expected_payload = {"login": org_name}
        mock_get_json.return_value = expected_payload

        # Act
        client = GithubOrgClient(org_name)
        result = client.org

        # Assert
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, expected_payload)
