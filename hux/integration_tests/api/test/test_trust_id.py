"""Purpose of this file is to integration test for trust id insights."""
from unittest import TestCase
from http import HTTPStatus
import pytest
import requests


class TestTrustId(TestCase):
    """Test Trust ID."""

    TRUST_ID = "trust_id"
    SIGNAL_NAME = "capability"

    def test_get_trust_id_overview(self):
        """Test get trust ID overview data."""

        response = requests.get(
            f"{pytest.API_URL}/{self.TRUST_ID}/overview",
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIsInstance(response.json(), dict)

    def test_get_trust_id_signal(self):
        """Test get trust ID signal data."""

        response = requests.get(
            f"{pytest.API_URL}/{self.TRUST_ID}/signal/{self.SIGNAL_NAME}",
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIsInstance(response.json(), dict)
