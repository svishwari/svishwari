"""Purpose of this file is to integration test for trust id insights."""
from unittest import TestCase
from http import HTTPStatus
import pytest
import requests


class TestTrustId(TestCase):
    """Test Trust ID."""

    TRUST_ID = "trust_id"
    SIGNAL_NAME = "capability"

    def test_get_trust_id_user_filters(self):
        """Test get trust ID user filters."""

        response = requests.get(
            f"{pytest.API_URL}/{self.TRUST_ID}/user_filters",
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIsInstance(response.json(), list)

    def test_get_trust_id_attributes(self):
        """Test get trust ID attributes data."""

        response = requests.get(
            f"{pytest.API_URL}/{self.TRUST_ID}/attributes",
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIsInstance(response.json(), list)

    def test_get_trust_id_comparison(self):
        """Test get trust ID comparison."""

        response = requests.get(
            f"{pytest.API_URL}/{self.TRUST_ID}/comparison",
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIsInstance(response.json(), list)

    def test_get_trust_id_overview(self):
        """Test get trust ID overview data."""

        response = requests.get(
            f"{pytest.API_URL}/{self.TRUST_ID}/overview",
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIsInstance(response.json(), dict)
