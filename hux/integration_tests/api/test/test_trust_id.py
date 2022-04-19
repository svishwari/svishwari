"""Purpose of this file is to integration test for trust id insights."""
from time import time
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
        self.assertGreaterEqual(len(response.json()), 1)

    def test_get_trust_id_attributes(self):
        """Test get trust ID attributes data."""

        response = requests.get(
            f"{pytest.API_URL}/{self.TRUST_ID}/attributes",
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIsInstance(response.json(), list)
        self.assertGreaterEqual(len(response.json()), 1)

    def test_get_trust_id_comparison(self):
        """Test get trust ID comparison."""

        response = requests.get(
            f"{pytest.API_URL}/{self.TRUST_ID}/comparison",
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIsInstance(response.json(), list)
        self.assertGreaterEqual(len(response.json()), 1)

    def test_get_trust_id_overview(self):
        """Test get trust ID overview data."""

        response = requests.get(
            f"{pytest.API_URL}/{self.TRUST_ID}/overview",
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIsInstance(response.json(), dict)

    def test_add_and_remove_trust_id_segment(self):
        """Test adding and removing trust ID segment for a user."""

        segment_name = (
            f"E2E test_trust_id Integration Test-{int(time() * 1000)}"
        )

        # request to add trust ID segment to a user
        add_response = requests.post(
            f"{pytest.API_URL}/{self.TRUST_ID}/segment",
            json={
                "segment_name": segment_name,
                "segment_filters": [
                    {
                        "type": "age",
                        "description": "Age",
                        "values": ["18-20 years", "21-24 years"],
                    }
                ],
            },
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.CREATED, add_response.status_code)
        self.assertIsInstance(add_response.json(), list)

        # request to remove trust ID segment to a user
        remove_response = requests.delete(
            f"{pytest.API_URL}/{self.TRUST_ID}/segment?segment_name={segment_name}",
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.OK, remove_response.status_code)
        self.assertIsInstance(remove_response.json(), list)
