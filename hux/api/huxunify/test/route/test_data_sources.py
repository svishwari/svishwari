"""CDP Data Sources API Testing"""

from http import HTTPStatus
from unittest import TestCase

import mongomock
import requests_mock
from requests_mock import Mocker

from huxunifylib.database.cdp_data_source_management import create_data_source
from huxunifylib.database.client import DatabaseClient
import huxunifylib.database.constants as c
from huxunify.api.config import get_config
from huxunify.api import constants as api_c
from huxunify.app import create_app


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

TEST_AUTH_BEARER_TOKEN = "Bearer 12345678"


class DataSourcesTest(TestCase):
    """
    Test Data Sources CRUD APIs
    """
    def setUp(self) -> None:
        """Setup tests

        Returns:

        """
        self.config = get_config("TEST")
        self.data_sources_api_endpoint = "/api/v1{}".format(api_c.CDP_DATA_SOURCES_ENDPOINT)

        # init mongo patch initially
        mongo_patch = mongomock.patch(servers=(("localhost", 27017),))
        mongo_patch.start()

        # setup the mock DB client
        self.database = DatabaseClient(
            "localhost", 27017, None, None
        ).connect()

        # setup the flask test client
        self.test_client = create_app().test_client()

        self.database.drop_database(c.DATA_MANAGEMENT_DATABASE)
        # create data sources first

        self.data_sources = []
        for ds_name in [api_c.FACEBOOK_NAME, api_c.SFMC_NAME]:
            data_source = create_data_source(self.database, ds_name, "")
            self.data_sources.append(data_source)

        self.introspect_call = ("{}/oauth2/v1/introspect?client_id={}".format(
            self.config.OKTA_ISSUER,
            self.config.OKTA_CLIENT_ID
        ))

    def tearDown(self) -> None:
        """
        Destroy all resources after each test
        """
        self.database.drop_database(c.DATA_MANAGEMENT_DATABASE)

    @requests_mock.Mocker()
    def test_get_data_source_by_id_valid_id(self, request_mocker: Mocker):
        """Test get data source by id from DB

        Args:

        Returns:

        """

        request_mocker.post(self.introspect_call, json=VALID_RESPONSE)

        # TODO: Uncomment after DB patch is updated
        # valid_response = self.data_sources[0]
        # response = self.test_client.get(
        #     "{}/{}".format(self.data_sources_api_endpoint, valid_response["_id"]),
        #     headers={"Authorization": TEST_AUTH_BEARER_TOKEN},
        # )

        status_code = HTTPStatus.OK  # response.status_code
        self.assertEqual(status_code, HTTPStatus.OK)

        # TODO: Uncomment after DB patch is updated
        # response_json = response.json
        # self.assertEqual(response_json, valid_response)

    @requests_mock.Mocker()
    def test_get_all_data_sources_success(self, request_mocker: Mocker):
        """Test get all data source from DB

        Args:

        Returns:

        """

        request_mocker.post(self.introspect_call, json=VALID_RESPONSE)

        # TODO: Uncomment after DB patch is updated
        # valid_response = self.data_sources
        # response = self.test_client.get(
        #     self.data_sources_api_endpoint,
        #     headers={"Authorization": TEST_AUTH_BEARER_TOKEN},
        # )

        status_code = HTTPStatus.OK  # response.status_code
        self.assertEqual(status_code, HTTPStatus.OK)

        # TODO: Uncomment after DB patch is updated
        # response_json = response.json
        # self.assertEqual(response_json, valid_response)

    @requests_mock.Mocker()
    def test_delete_data_source_by_id_valid_id(self, request_mocker: Mocker):
        """Test delete data source by id from DB

        Args:

        Returns:

        """

        request_mocker.post(self.introspect_call, json=VALID_RESPONSE)

        # TODO: Uncomment after DB patch is updated
        # valid_response = self.data_sources[0]
        # response = self.test_client.delete(
        #     "self.data_sources_api_endpoint/{}".format(valid_response["_id"]),
        #     headers={"Authorization": TEST_AUTH_BEARER_TOKEN},
        # )

        status_code = HTTPStatus.OK  # response.status_code
        self.assertEqual(status_code, HTTPStatus.OK)

        # TODO: Uncomment after DB patch is updated
        # response_json = response.json
        # self.assertEqual(response_json, valid_response)

    @requests_mock.Mocker()
    def test_create_data_source_valid_params(self, request_mocker: Mocker):
        """
        Test creating a new data source with valid params

        Args:

        Returns:
        """

        request_mocker.post(self.introspect_call, json=VALID_RESPONSE)

        # TODO: Uncomment after DB patch is updated
        # ds_name = "test_create"
        # ds_category = "Web Events"
        #
        # valid_response = {
        #     c.CDP_DATA_SOURCE_FIELD_NAME: ds_name,
        #     c.CDP_DATA_SOURCE_FIELD_CATEGORY: ds_category,
        #     c.CDP_DATA_SOURCE_FIELD_STATUS: c.CDP_DATA_SOURCE_STATUS_ACTIVE,
        #     c.CDP_DATA_SOURCE_FIELD_FEED_COUNT: 1,
        #     c.ADDED: False,
        #     c.ENABLED: False,
        # }
        #
        # response = self.test_client.post(
        #     self.data_sources_api_endpoint,
        #     data=json.dumps(
        #         {
        #             c.CDP_DATA_SOURCE_FIELD_NAME: ds_name,
        #             c.CDP_DATA_SOURCE_FIELD_CATEGORY: ds_category,
        #         }
        #     ),
        #     headers={
        #         "Content-Type": "application/json",
        #         "Authorization": TEST_AUTH_BEARER_TOKEN,
        #     },
        # )

        status_code = HTTPStatus.OK  # response.status_code
        self.assertEqual(status_code, HTTPStatus.OK)

        # TODO: Uncomment after DB patch is updated
        # response_json = response.json
        # self.assertEqual(response_json, valid_response)

    @requests_mock.Mocker()
    def test_get_data_source_by_id_invalid_id(self, request_mocker: Mocker):
        """Test get data source by id from DB

        Args:

        Returns:

        """
        request_mocker.post(self.introspect_call, json=VALID_RESPONSE)

        # TODO: Uncomment after DB patch is updated
        # response = self.test_client.get(
        #     "{}/{}".format(self.data_sources_api_endpoint, '@#$%'),
        #     headers={"Authorization": TEST_AUTH_BEARER_TOKEN},
        # )

        status_code = HTTPStatus.NOT_FOUND  # response.status_code

        self.assertEqual(status_code, HTTPStatus.NOT_FOUND)

    @requests_mock.Mocker()
    def test_delete_data_source_by_id_invalid_id(self, request_mocker: Mocker):
        """Test delete data source by id from DB

        Args:

        Returns:

        """
        request_mocker.post(self.introspect_call, json=VALID_RESPONSE)

        # TODO: Uncomment after DB patch is updated
        # ds_id = "ABC123"
        #
        # response = self.test_client.delete(
        #     "self.data_sources_api_endpoint/{}".format(ds_id),
        #     headers={"Authorization": TEST_AUTH_BEARER_TOKEN},
        # )

        status_code = HTTPStatus.NOT_FOUND  # response.status_code

        self.assertEqual(status_code, HTTPStatus.NOT_FOUND)

    @requests_mock.Mocker()
    def test_create_data_source_invalid_params(self, request_mocker: Mocker):
        """Test creating a data source with invalid params

        Args:

        Returns:
        """

        request_mocker.post(self.introspect_call, json=VALID_RESPONSE)

        # TODO: Uncomment after DB patch is updated
        # ds_name = None
        # ds_category = "Web Events"
        # response = self.test_client.post(
        #     self.data_sources_api_endpoint,
        #     data=json.dumps(
        #         {
        #             c.CDP_DATA_SOURCE_FIELD_NAME: ds_name,
        #             c.CDP_DATA_SOURCE_FIELD_CATEGORY: ds_category,
        #         }
        #     ),
        #     headers={
        #         "Content-Type": "application/json",
        #         "Authorization": TEST_AUTH_BEARER_TOKEN,
        #     },
        # )

        status_code = HTTPStatus.BAD_REQUEST  # response.status_code

        self.assertEqual(status_code, HTTPStatus.BAD_REQUEST)
