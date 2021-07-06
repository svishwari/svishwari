"""
purpose of this file is to house all the cdp tests.
"""
import string
from unittest import TestCase, mock
from http import HTTPStatus
import requests_mock
from requests_mock import Mocker
from hypothesis import given, strategies as st

from huxunify.api.config import get_config
from huxunify.api import constants as api_c
from huxunify.test import constants as t_c
from huxunify.app import create_app


class CDPTest(TestCase):
    """
    Test CDP request methods
    """

    def setUp(self) -> None:
        """Setup tests

        Returns:

        """
        self.data_sources_api_endpoint = (
            f"{t_c.BASE_ENDPOINT}{api_c.CDP_DATA_SOURCES_ENDPOINT}"
        )

        # setup the flask test client
        self.test_client = create_app().test_client()

        self.request_mocker = requests_mock.Mocker()
        self.request_mocker.post(t_c.INTROSPECT_CALL, json=t_c.VALID_RESPONSE)
        self.request_mocker.start()

        self.addCleanup(mock.patch.stopall)

    def tearDown(self) -> None:
        """Tear down tests

        Returns:

        """
        self.request_mocker.stop()

    @given(customer_id=st.text(alphabet=string.ascii_letters))
    def test_get_customer(self, customer_id: str):
        """Test get customer profiles

        Args:
            customer_id (str): string for testing get customer.

        Returns:

        """

        # skip empty string from hypothesis
        if not customer_id:
            return

        expected_response = {
            "code": 200,
            "body": {
                api_c.HUX_ID: customer_id,
                api_c.FIRST_NAME: "Bertie",
                api_c.LAST_NAME: "Fox",
                api_c.EMAIL: "fake@fake.com",
                api_c.GENDER: "test_gender",
                api_c.CITY: "test_city",
                api_c.ADDRESS: "test_address",
                api_c.AGE: "test_age",
            },
            "message": "ok",
        }

        self.request_mocker.stop()
        self.request_mocker.get(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/{customer_id}",
            json=expected_response,
        )
        self.request_mocker.start()

        response = self.test_client.get(
            f"{t_c.BASE_ENDPOINT}{api_c.CUSTOMERS_ENDPOINT}/{customer_id}",
            headers=t_c.AUTH_HEADER,
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
