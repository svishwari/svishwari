"""
Purpose of this file is to house all data sources tests
"""

import json
from http import HTTPStatus
from unittest import TestCase, mock

import mongomock
import requests_mock
from flask_marshmallow import Schema
from marshmallow import ValidationError
from requests_mock import Mocker

from huxunifylib.database.cdp_data_source_management import create_data_source
from huxunifylib.database.client import DatabaseClient
import huxunifylib.database.constants as db_c
from huxunify.api.config import get_config
from huxunify.api import constants as api_c
from huxunify.api.schema.cdp_data_source import CdpDataSourceSchema
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


def validate_schema(
    schema: Schema, response_json: dict, is_multiple: bool = False
) -> bool:
    """
    Validate if the response confirms with the given schema

    Args:
        schema (Schema): Instance of the Schema to validate against
        response_json (dict): Response json as dict
        is_multiple (bool): If response is a collection of objects

    Returns:
        (bool): True/False
    """

    try:
        schema.load(response_json, many=is_multiple)
        return True
    except ValidationError:
        return False


class CdpDataSourcesTest(TestCase):
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

        # create data sources first
        self.data_sources = []
        for ds_name in [api_c.FACEBOOK_NAME, api_c.SFMC_NAME]:
            self.data_sources.append(
                CdpDataSourceSchema().dump(
                    create_data_source(self.database, ds_name, "")
                )
            )

        self.introspect_call = (
            f"{self.config.OKTA_ISSUER}"
            f"/oauth2/v1/introspect?client_id="
            f"{self.config.OKTA_CLIENT_ID}"
        )

    @requests_mock.Mocker()
    def test_get_data_source_by_id_valid_id(self, request_mocker: Mocker):
        """
        Test get data source by id from DB

        Args:
            request_mocker (Mocker): Request mocker object.

        Returns:

        """

        request_mocker.post(self.introspect_call, json=VALID_RESPONSE)

        valid_response = self.data_sources[0]

        response = self.test_client.get(
            f"{self.data_sources_api_endpoint}/{valid_response[api_c.ID]}",
            headers={
                "Authorization": TEST_AUTH_TOKEN,
                "Content-Type": "application/json",
            },
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertTrue(validate_schema(CdpDataSourceSchema(), response.json))
        self.assertEqual(valid_response, response.json)

    @requests_mock.Mocker()
    def test_get_all_data_sources_success(self, request_mocker: Mocker):
        """
        Test get all data source from DB

        Args:
            request_mocker (Mocker): Request mocker object

        Returns:

        """

        request_mocker.post(self.introspect_call, json=VALID_RESPONSE)
        is_multiple = True

        valid_response = self.data_sources

        response = self.test_client.get(
            self.data_sources_api_endpoint,
            headers={"Authorization": TEST_AUTH_TOKEN},
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertTrue(
            validate_schema(CdpDataSourceSchema(), response.json, is_multiple)
        )
        self.assertEqual(valid_response, response.json)

    @requests_mock.Mocker()
    def test_delete_data_source_by_id_valid_id(self, request_mocker: Mocker):
        """
        Test delete data source by id from DB

        Args:
            request_mocker (Mocker): Request mocker object.

        Returns:

        """

        request_mocker.post(self.introspect_call, json=VALID_RESPONSE)

        ds_id = self.data_sources[0][api_c.ID]

        valid_response = dict(message="SUCCESS")

        response = self.test_client.delete(
            f"{self.data_sources_api_endpoint}/{ds_id}",
            headers={"Authorization": TEST_AUTH_TOKEN},
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(valid_response, response.json)

    @requests_mock.Mocker()
    def test_create_data_source_valid_params(self, request_mocker: Mocker):
        """
        Test creating a new data source with valid params

        Args:
            request_mocker (Mocker): Request mocker object

        Returns:

        """

        request_mocker.post(self.introspect_call, json=VALID_RESPONSE)

        ds_name = "test create data source"
        ds_category = "test category"

        valid_response = {
            api_c.CDP_DATA_SOURCE_NAME: ds_name,
            api_c.CDP_DATA_SOURCE_CATEGORY: ds_category,
            api_c.CDP_DATA_SOURCE_FEED_COUNT: 1,
            api_c.STATUS: db_c.CDP_DATA_SOURCE_STATUS_ACTIVE,
            api_c.CDP_DATA_SOURCE_ADDED: False,
            api_c.CDP_DATA_SOURCE_ENABLED: False,
        }

        response = self.test_client.post(
            self.data_sources_api_endpoint,
            data=json.dumps(
                {
                    db_c.CDP_DATA_SOURCE_FIELD_NAME: ds_name,
                    db_c.CDP_DATA_SOURCE_FIELD_CATEGORY: ds_category,
                }
            ),
            headers={
                "Content-Type": "application/json",
                "Authorization": TEST_AUTH_TOKEN,
            },
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertTrue(validate_schema(CdpDataSourceSchema(), response.json))
        self.assertDictContainsSubset(valid_response, response.json)

    @requests_mock.Mocker()
    def test_get_data_source_by_id_invalid_id(self, request_mocker: Mocker):
        """
        Test get data source with an invalid id

        Args:
            request_mocker (Mocker): Request mocker object.

        Returns:

        """
        request_mocker.post(self.introspect_call, json=VALID_RESPONSE)

        ds_id = "XYZ"
        valid_response = {
            "message": f"Invalid CDP data source ID received {ds_id}."
        }

        response = self.test_client.get(
            f"{self.data_sources_api_endpoint}/{ds_id}",
            headers={
                "Authorization": TEST_AUTH_TOKEN,
                "Content-Type": "application/json",
            },
        )

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual(valid_response, response.json)

    @requests_mock.Mocker()
    def test_delete_data_source_by_id_invalid_id(self, request_mocker: Mocker):
        """
        Test delete data source with an invalid id

        Args:
            request_mocker (Mocker): Request mocker object.

        Returns:

        """
        request_mocker.post(self.introspect_call, json=VALID_RESPONSE)

        ds_id = "ABC123"
        valid_response = {
            "message": f"Invalid CDP data source ID received {ds_id}."
        }

        response = self.test_client.delete(
            f"{self.data_sources_api_endpoint}/{ds_id}",
            headers={"Authorization": TEST_AUTH_TOKEN},
        )

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual(valid_response, response.json)

    @requests_mock.Mocker()
    def test_create_data_source_w_empty_name_string(
        self, request_mocker: Mocker
    ):
        """
        Test creating a data source with name set as empty string

        Args:
            request_mocker (Mocker): Request mocker object.

        Returns:

        """

        request_mocker.post(self.introspect_call, json=VALID_RESPONSE)

        ds_name = ""

        valid_response = {
            "category": ["Missing data for required field."],
            "name": ["Data not provided."],
        }
        response = self.test_client.post(
            self.data_sources_api_endpoint,
            data=json.dumps({db_c.CDP_DATA_SOURCE_FIELD_NAME: ds_name}),
            headers={
                "Content-Type": "application/json",
                "Authorization": TEST_AUTH_TOKEN,
            },
        )

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual(valid_response, response.json)

    @requests_mock.Mocker()
    def test_create_data_source_no_inputs(self, request_mocker: Mocker):
        """
        Test creating a data source without any inputs

        Args:
            request_mocker (Mocker): Request mocker object.

        Returns:

        """

        request_mocker.post(self.introspect_call, json=VALID_RESPONSE)

        valid_response = {
            "category": ["Missing data for required field."],
            "name": ["Missing data for required field."],
        }

        response = self.test_client.post(
            self.data_sources_api_endpoint,
            data=json.dumps({}),
            headers={
                "Content-Type": "application/json",
                "Authorization": TEST_AUTH_TOKEN,
            },
        )

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual(valid_response, response.json)

    @requests_mock.Mocker()
    def test_create_data_source_w_no_values(self, request_mocker: Mocker):
        """
        Test creating a data source with name and category
        set as empty string

        Args:
            request_mocker (Mocker): Request mocker object.

        Returns:

        """

        request_mocker.post(self.introspect_call, json=VALID_RESPONSE)

        ds_name = ""
        ds_category = ""

        valid_response = {
            "category": ["Data not provided."],
            "name": ["Data not provided."],
        }

        response = self.test_client.post(
            self.data_sources_api_endpoint,
            data=json.dumps(
                {
                    db_c.CDP_DATA_SOURCE_FIELD_NAME: ds_name,
                    db_c.CDP_DATA_SOURCE_FIELD_CATEGORY: ds_category,
                }
            ),
            headers={
                "Content-Type": "application/json",
                "Authorization": TEST_AUTH_TOKEN,
            },
        )

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual(valid_response, response.json)
