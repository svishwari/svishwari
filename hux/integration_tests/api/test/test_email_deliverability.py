"""Purpose of this file is to integration test for email deliverability."""
from unittest import TestCase
from http import HTTPStatus
import pytest
import requests


class TestEmailDeliverability(TestCase):
    """Test Email Deliverability."""

    EMAIL_DELIVERABILITY = "email_deliverability"
    COLLECTION = "deliverability_metrics"

    def test_get_email_deliverability_overview(self):
        """Test get email deliverability overview data."""

        response = requests.get(
            f"{pytest.API_URL}/{self.EMAIL_DELIVERABILITY}/overview",
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIsInstance(response.json(), dict)

    def test_get_email_deliverability_domains(self):
        """Test get email deliverability domains data."""

        response = requests.get(
            f"{pytest.API_URL}/{self.EMAIL_DELIVERABILITY}/domains",
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIsInstance(response.json(), dict)
