"""
purpose of this file is to house all the cdp tests.
"""
import string
from unittest import TestCase
from http import HTTPStatus
import requests_mock
from requests_mock import Mocker
from hypothesis import given, strategies as st

from huxunify.api.config import get_config
from huxunify.api import constants as api_c
from huxunify.test import constants as sh
from huxunify.app import create_app


class CDPTest(TestCase):
    """
    Test CDP request methods
    """

    def setUp(self) -> None:
        """Setup tests

        Returns:

        """
        self.config = get_config("TEST")
        self.data_sources_api_endpoint = (
            f"{sh.BASE_ENDPOINT}{api_c.CDP_DATA_SOURCES_ENDPOINT}"
        )

        # setup the flask test client
        self.test_client = create_app().test_client()

        self.introspect_call = (
            f"{self.config.OKTA_ISSUER}"
            f"/oauth2/v1/introspect?client_id="
            f"{self.config.OKTA_CLIENT_ID}"
        )

    @requests_mock.Mocker()
    @given(customer_id=st.text(alphabet=string.ascii_letters))
    def test_get_customer(self, request_mocker: Mocker, customer_id: str):
        """Test get customer profiles

        Args:
            request_mocker (Mocker): Request mock object.
            customer_id (str): string for testing get customer.

        Returns:

        """

        # skip empty string from hypothesis
        if not customer_id:
            return

        request_mocker.post(self.introspect_call, json=sh.VALID_RESPONSE)
        response = self.test_client.get(
            f"{sh.BASE_ENDPOINT}{api_c.CUSTOMERS_ENDPOINT}/{customer_id}",
            headers=sh.AUTH_HEADER,
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        data = response.json
        self.assertTrue(data[api_c.FIRST_NAME])
        self.assertTrue(data[api_c.LAST_NAME])
        self.assertEqual(data[api_c.EMAIL], api_c.REDACTED)
        self.assertEqual(data[api_c.GENDER], api_c.REDACTED)
        self.assertEqual(data[api_c.CITY], api_c.REDACTED)
        self.assertEqual(data[api_c.ADDRESS], api_c.REDACTED)
        self.assertEqual(data[api_c.AGE], api_c.REDACTED)
