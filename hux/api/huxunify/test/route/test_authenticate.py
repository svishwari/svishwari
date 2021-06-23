"""
Purpose of this file is to house all authentication tests
"""
from unittest import TestCase, mock

import mongomock
import requests_mock
from requests_mock import Mocker

import huxunifylib.database.constants as db_c
from huxunifylib.database.client import DatabaseClient

from huxunify.api import constants as api_c
from huxunify.api.config import get_config
from huxunify.app import create_app
from huxunify.test.shared import BASE_ENDPOINT, VALID_RESPONSE


class AuthenticateTest(TestCase):
    """
    Test CDP Data Sources CRUD APIs
    """

    def setUp(self) -> None:
        """
        Setup tests

        Returns:

        """
        self.config = get_config("TEST")
        self.data_sources_api_endpoint = (
            f"{BASE_ENDPOINT}{api_c.CDP_DATA_SOURCES_ENDPOINT}"
        )

        # init mongo patch initially
        mongo_patch = mongomock.patch(servers=(("localhost", 27017),))
        mongo_patch.start()

        # setup the mock DB client
        self.database = DatabaseClient(
            "localhost", 27017, None, None
        ).connect()

        # mock get_db_client()
        get_db_client_mock = mock.patch(
            "huxunify.api.route.cdp_data_source.get_db_client"
        ).start()
        get_db_client_mock.return_value = self.database
        self.addCleanup(mock.patch.stopall)

        # setup the flask test client
        self.test_client = create_app().test_client()

        self.database.drop_database(db_c.DATA_MANAGEMENT_DATABASE)

        self.introspect_call = (
            f"{self.config.OKTA_ISSUER}"
            f"/oauth2/v1/introspect?client_id="
            f"{self.config.OKTA_CLIENT_ID}"
        )

    @requests_mock.Mocker()
    def test_authenticate(self, request_mocker: Mocker):
        """ Tests validation of the provided JWT access token

        Args:
            request_mocker (Mocker): Request mocker object.

        Returns:

        """

        # mock the introspect token call
        request_mocker.post(self.introspect_call, json=VALID_RESPONSE)

        response = self.test_client.get(

        )