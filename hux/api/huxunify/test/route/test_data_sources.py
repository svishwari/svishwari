import json
from unittest import TestCase

import mongomock
import requests_mock
from huxunifylib.database.cdp_data_source_management import create_data_source
from requests_mock import Mocker

import huxunifylib.database.constants as c
from huxunify.api.config import get_config
from huxunifylib.database.client import DatabaseClient
from huxunify.api import constants as api_c
from huxunify.app import create_app as huxunify_app


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


class DataSourcesTest(TestCase):
    """
    Test Data Sources CRUD APIs
    """

    @mongomock.patch(servers=(("localhost", 27017),))
    def setUp(self) -> None:
        """Setup tests

        Returns:

        """
        self.test_client = huxunify_app().test_client()
        self.data_sources_api_endpoint = f"/api/v1{api_c.CDP_DATA_SOURCES_ENDPOINT}"

        self.config = get_config()
        self.introspect_call = (
            f"{self.config.OKTA_ISSUER}"
            f"/oauth2/v1/introspect?client_id="
            f"{self.config.OKTA_CLIENT_ID}"
        )

        # TODO: Draft for review
        # setup the mock DB client
        self.database = DatabaseClient(
            "localhost", 27017, None, None
        ).connect()

        self.database.drop_database(c.DATA_MANAGEMENT_DATABASE)

        data_sources_list = [
            {
                "name": "TestDataSource1",
                "category": "Web Events"
            },
            {
                "name": "TestDataSource2",
                "category": "Web Events"
            }
        ]

        self.data_sources = []
        for ds in data_sources_list:
            data_source = create_data_source(
                self.database,
                ds["name"],
                ds["category"]
            )
            data_source["_id"] = str(data_source["_id"])
            self.data_sources.append(data_source)

    def tearDown(self) -> None:
        """
        To be executed after the end of each test
        """

        self.database.drop_database(c.DATA_MANAGEMENT_DATABASE)

    @requests_mock.Mocker()
    def test_get_data_source_by_id_valid_request(self, request_mocker: Mocker):
        """Test get data source by id from DB

        Args:

        Returns:

        """
        valid_response = self.data_sources[0]

        request_mocker.post(self.introspect_call, json=VALID_RESPONSE)

        response = self.test_client.get(
            f'{self.data_sources_api_endpoint}/{valid_response["_id"]}',
            headers={"Authorization": "Bearer 12345678"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, valid_response)

    @requests_mock.Mocker()
    def test_get_all_data_sources_valid_request(self, request_mocker: Mocker):
        """Test get all data source from DB

        Args:

        Returns:

        """
        valid_response = self.data_sources

        request_mocker.post(self.introspect_call, json=VALID_RESPONSE)

        response = self.test_client.get(
            self.data_sources_api_endpoint,
            headers={"Authorization": "Bearer 12345678"}
        )

        status_code = response.status_code
        response_data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(status_code, 200)
        self.assertEqual(response_data, valid_response)

    @requests_mock.Mocker()
    def test_delete_data_source_by_id_valid_request(self, request_mocker: Mocker):
        """Test delete data source by id from DB

        Args:

        Returns:

        """
        valid_response = self.data_sources[0]

        request_mocker.post(self.introspect_call, json=VALID_RESPONSE)

        response = self.test_client.delete(
            "self.data_sources_api_endpoint/{}".format(valid_response["_id"]),
            headers={
                "Authorization": "Bearer 12345678"
            }
        )

        status_code = response.status_code
        response_data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(status_code, 200)
        self.assertEqual(response_data[c.CDP_DATA_SOURCE_ID], valid_response["_id"])

    @requests_mock.Mocker()
    def test_create_data_source(self, request_mocker: Mocker):

        ds_name = "test_create"
        ds_category = "Web Events"

        valid_response = {
            c.CDP_DATA_SOURCE_FIELD_NAME: ds_name,
            c.CDP_DATA_SOURCE_FIELD_CATEGORY: ds_category,
            c.CDP_DATA_SOURCE_FIELD_STATUS: c.CDP_DATA_SOURCE_STATUS_ACTIVE,
            c.CDP_DATA_SOURCE_FIELD_FEED_COUNT: 1,
            c.ADDED: False,
            c.ENABLED: False
        }

        request_mocker.post(self.introspect_call, json=VALID_RESPONSE)

        response = self.test_client.post(
            self.data_sources_api_endpoint,
            data=json.dumps({
                c.CDP_DATA_SOURCE_FIELD_NAME: ds_name,
                c.CDP_DATA_SOURCE_FIELD_CATEGORY: ds_category
            }),
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer 12345678"
            }
        )

        status_code = response.status_code
        response_data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(status_code, 200)
        self.assertEqual(response_data[c.CDP_DATA_SOURCE_FIELD_NAME], ds_name)
        self.assertEqual(response_data[c.CDP_DATA_SOURCE_FIELD_CATEGORY], ds_category)
