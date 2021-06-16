"""
Purpose of this file is to house all the customers api tests
"""

import unittest
from http import HTTPStatus

import mongomock
import requests_mock
from requests_mock import Mocker

from huxunifylib.database.client import DatabaseClient
import huxunifylib.database.constants as db_c
from huxunify.api.config import get_config
from huxunify.api import constants as api_c
from huxunify.app import create_app


BASE_ENDPOINT = "/api/v1"
TEST_AUTH_TOKEN = "Bearer 12345678"
VALID_RESPONSE = {
    "active": True,
    "scope": "openid email profile",
    "username": "davesmith",
    "exp": 1234,
    "iat": 12345,
    "sub": "davesmith@fake",
    "aud": "sample_aud",
    "iss": "sample_iss",
    "jti": "sample_jti",
    "token_type": "Bearer",
    "client_id": "1234",
    "uid": "1234567",
}


class TestCustomersOverview(unittest.TestCase):
    """
    Purpose of this class is to test Customers overview
    """

    def setUp(self):  # pylint: disable=arguments-differ
        """
        Sets up Test Client

        Returns:
        """
        self.config = get_config("TEST")
        self.customers = f"{BASE_ENDPOINT}{api_c.CUSTOMERS_ENDPOINT}"
        self.idr = f"{BASE_ENDPOINT}{api_c.IDR_ENDPOINT}"
        self.headers = {
            "Authorization": TEST_AUTH_TOKEN,
            "Content-Type": "application/json",
        }

        # init mongo patch initially
        mongo_patch = mongomock.patch(servers=(("localhost", 27017),))
        mongo_patch.start()

        # setup the mock DB client
        self.database = DatabaseClient(
            "localhost", 27017, None, None
        ).connect()

        # setup the flask test client
        self.test_client = create_app().test_client()
        self.database.drop_database(db_c.DATA_MANAGEMENT_DATABASE)
        self.introspect_call = (
            f"{self.config.OKTA_ISSUER}"
            f"/oauth2/v1/introspect?client_id="
            f"{self.config.OKTA_CLIENT_ID}"
        )

    @requests_mock.Mocker()
    def test_get_customers(self, request_mocker: Mocker):
        """
        Test get customers

        Args:
            request_mocker (Mocker): Request mocker object.

        Returns:

        """

        request_mocker.post(self.introspect_call, json=VALID_RESPONSE)
        response = self.test_client.get(
            self.customers,
            headers=self.headers,
        )
        self.assertEqual(HTTPStatus.OK, response.status_code)

    @requests_mock.Mocker()
    def test_get_customer_overview(self, request_mocker: Mocker):
        """
        Test get customers overview

        Args:
            request_mocker (Mocker): Request mocker object.

        Returns:

        """

        request_mocker.post(self.introspect_call, json=VALID_RESPONSE)
        response = self.test_client.get(
            f"{self.customers}/{api_c.OVERVIEW}",
            headers=self.headers,
        )
        self.assertEqual(HTTPStatus.OK, response.status_code)

    @requests_mock.Mocker()
    def test_get_idr_overview(self, request_mocker: Mocker):
        """
        Test get customers idr overview

        Args:
            request_mocker (Mocker): Request mocker object.

        Returns:

        """

        request_mocker.post(self.introspect_call, json=VALID_RESPONSE)
        response = self.test_client.get(
            f"{self.idr}/{api_c.OVERVIEW}",
            headers=self.headers,
        )
        self.assertEqual(HTTPStatus.OK, response.status_code)

    @requests_mock.Mocker()
    def test_get_customer_by_id(self, request_mocker: Mocker):
        """
        Test get customer by id

        Args:
            request_mocker (Mocker): Request mocker object.

        Returns:

        """

        request_mocker.post(self.introspect_call, json=VALID_RESPONSE)
        customer_id = "1531-2039-22"
        response = self.test_client.get(
            f"{self.customers}/{customer_id}",
            headers=self.headers,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)

    @requests_mock.Mocker()
    def test_post_customeroverview_by_attributes(
        self, request_mocker: Mocker
    ) -> None:
        """
        Test get customer over by attributes

        Args:
            request_mocker (Mocker): Request mocker object.

        Returns:
            None
        """

        request_mocker.post(self.introspect_call, json=VALID_RESPONSE)

        filter_attributes = {
            "filters": {
                "section_aggregator": "ALL",
                "section_filters": [
                    {"field": "country", "type": "equals", "value": "us"}
                ],
            }
        }

        response = self.test_client.post(
            f"{self.customers}/{api_c.OVERVIEW}",
            data=filter_attributes,
            headers=self.headers,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
