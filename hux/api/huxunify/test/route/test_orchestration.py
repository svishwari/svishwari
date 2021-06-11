"""
Purpose of this file is to house all the orchestration api tests
"""
from http import HTTPStatus
from unittest import TestCase, mock

import mongomock
import requests_mock
from requests_mock import Mocker

import huxunifylib.database.constants as db_c
from huxunifylib.database import data_management
from huxunifylib.database.client import DatabaseClient
from huxunify.app import create_app
from huxunify.api import constants as api_c
from huxunify.api.config import get_config


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


class OrchestrationRouteTest(TestCase):
    """Orchestration Route tests"""

    def setUp(self) -> None:
        """Setup tests
        Returns:
            None
        """
        self.config = get_config("TEST")
        self.audience_api_endpoint = "/api/v1{}".format(
            api_c.AUDIENCE_ENDPOINT
        )

        # init mongo patch initially
        mongo_patch = mongomock.patch(servers=(("localhost", 27017),))
        mongo_patch.start()

        # setup the mock DB client
        self.database = DatabaseClient(
            "localhost", 27017, None, None
        ).connect()

        get_db_client_mock = mock.patch(
            "huxunify.api.route.orchestration.get_db_client"
        ).start()
        get_db_client_mock.return_value = self.database
        self.addCleanup(mock.patch.stopall)

        # setup the flask test client
        self.test_client = create_app().test_client()

        self.database.drop_database(db_c.DATA_MANAGEMENT_DATABASE)
        # create data sources first

        self.introspect_call = "{}/oauth2/v1/introspect?client_id={}".format(
            self.config.OKTA_ISSUER, self.config.OKTA_CLIENT_ID
        )

    @requests_mock.Mocker()
    def test_get_audience_rules(self, request_mocker: Mocker):
        """Test the get audience rules route

        Args:
            request_mocker (Mocker): Request mocker object.

        Expects a dict of all necessary audience rules

        """

        request_mocker.post(self.introspect_call, json=VALID_RESPONSE)

        data_management.set_constant(
            self.database,
            db_c.AUDIENCE_FILTER_CONSTANTS,
            {
                "text_operators": {
                    "contains": "Contains",
                    "does_not_contain": "Does not contain",
                    "does_not_equal": "Does not equal",
                    "equals": "Equals",
                }
            }
        )

        response = self.test_client.get(
            f"{self.audience_api_endpoint}/rules",
            headers={"Authorization": TEST_AUTH_TOKEN},
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertTrue("rule_attributes" in response.json)
        self.assertTrue("text_operators" in response.json)
