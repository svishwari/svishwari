"""
Purpose of this file is to house all data sources tests
"""

import json
from http import HTTPStatus
from unittest import TestCase, mock

import mongomock
import requests_mock
from bson import ObjectId

from huxunifylib.database.cdp_data_source_management import create_data_source
from huxunifylib.database.client import DatabaseClient
import huxunifylib.database.constants as db_c
import huxunify.test.constants as t_c
from huxunify.api import constants as api_c
from huxunify.api.schema.cdp_data_source import (
    CdpDataSourceSchema,
    DataSourceDataFeedsGetSchema,
    CdpDataSourceDataFeedSchema,
)
from huxunify.app import create_app


class CdpDataSourcesTest(TestCase):
    """
    Test CDP Data Sources CRUD APIs
    """

    def setUp(self) -> None:
        """
        Setup tests

        Returns:

        """

        self.data_sources_api_endpoint = (
            f"{t_c.BASE_ENDPOINT}{api_c.CDP_DATA_SOURCES_ENDPOINT}"
        )

        # init mongo patch initially
        mongo_patch = mongomock.patch(servers=(("localhost", 27017),))
        mongo_patch.start()

        # setup the mock DB client
        self.database = DatabaseClient(
            "localhost", 27017, None, None
        ).connect()

        # mock get_db_client() in cdp_data_source
        mock.patch(
            "huxunify.api.route.cdp_data_source.get_db_client",
            return_value=self.database,
        ).start()

        # mock request for introspect call
        self.request_mocker = requests_mock.Mocker()
        self.request_mocker.post(t_c.INTROSPECT_CALL, json=t_c.VALID_RESPONSE)
        self.request_mocker.start()

        # stop all mocks in cleanup
        self.addCleanup(mock.patch.stopall)

        # setup the flask test client
        self.test_client = create_app().test_client()

        self.database.drop_database(db_c.DATA_MANAGEMENT_DATABASE)

        # create data sources first
        self.data_sources = []
        for ds_name in [
            db_c.DELIVERY_PLATFORM_FACEBOOK,
            db_c.DELIVERY_PLATFORM_SFMC,
        ]:
            self.data_sources.append(
                CdpDataSourceSchema().dump(
                    create_data_source(self.database, ds_name, "")
                )
            )

    def test_get_data_source_by_id_valid_id(self):
        """
        Test get data source by id from DB

        Args:

        Returns:

        """

        valid_response = self.data_sources[0]

        response = self.test_client.get(
            f"{self.data_sources_api_endpoint}/{valid_response[api_c.ID]}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertTrue(
            t_c.validate_schema(CdpDataSourceSchema(), response.json)
        )
        self.assertEqual(valid_response, response.json)

    def test_get_all_data_sources_success(self):
        """
        Test get all data source from DB

        Args:

        Returns:

        """

        valid_response = self.data_sources

        response = self.test_client.get(
            self.data_sources_api_endpoint,
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertTrue(
            t_c.validate_schema(
                CdpDataSourceSchema(), response.json, is_multiple=True
            )
        )
        self.assertEqual(valid_response, response.json)

    def test_delete_data_source_by_id_valid_id(self):
        """
        Test delete data source by id from DB

        Args:

        Returns:

        """

        ds_id = self.data_sources[0][api_c.ID]

        valid_response = dict(message="SUCCESS")

        response = self.test_client.delete(
            f"{self.data_sources_api_endpoint}/{ds_id}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(valid_response, response.json)

    def test_create_data_source_valid_params(self):
        """
        Test creating a new data source with valid params

        Args:

        Returns:

        """

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
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertTrue(
            t_c.validate_schema(CdpDataSourceSchema(), response.json)
        )
        self.assertDictContainsSubset(valid_response, response.json)

    def test_get_data_source_by_id_invalid_id(self):
        """
        Test get data source with an invalid id

        Args:

        Returns:

        """

        ds_id = "XYZ"
        valid_response = {
            "message": f"Invalid CDP data source ID received {ds_id}."
        }

        response = self.test_client.get(
            f"{self.data_sources_api_endpoint}/{ds_id}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual(valid_response, response.json)

    def test_delete_data_source_by_id_invalid_id(self):
        """
        Test delete data source with an invalid id

        Args:

        Returns:

        """

        ds_id = "ABC123"
        valid_response = {
            "message": f"Invalid CDP data source ID received {ds_id}."
        }

        response = self.test_client.delete(
            f"{self.data_sources_api_endpoint}/{ds_id}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual(valid_response, response.json)

    def test_delete_data_source_by_id_non_existent_id(self) -> None:
        """
        Test delete data source with an non-existent id

        Args:

        Returns:
            None
        """

        non_existent_data_source_id = str(ObjectId())

        response = self.test_client.delete(
            f"{self.data_sources_api_endpoint}/{non_existent_data_source_id}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(
            HTTPStatus.INTERNAL_SERVER_ERROR, response.status_code
        )
        self.assertEqual({"message": api_c.OPERATION_FAILED}, response.json)

    def test_create_data_source_w_empty_name_string(self):
        """
        Test creating a data source with name set as empty string

        Args:

        Returns:

        """

        ds_name = ""

        valid_response = {
            "category": ["Missing data for required field."],
            "name": ["Data not provided."],
        }
        response = self.test_client.post(
            self.data_sources_api_endpoint,
            data=json.dumps({db_c.CDP_DATA_SOURCE_FIELD_NAME: ds_name}),
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual(valid_response, response.json)

    def test_create_data_source_no_inputs(self):
        """
        Test creating a data source without any inputs

        Args:

        Returns:

        """

        valid_response = {
            "category": ["Missing data for required field."],
            "name": ["Missing data for required field."],
        }

        response = self.test_client.post(
            self.data_sources_api_endpoint,
            data=json.dumps({}),
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual(valid_response, response.json)

    def test_create_data_source_w_no_values(self):
        """
        Test creating a data source with name and category
        set as empty string

        Args:

        Returns:

        """

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
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual(valid_response, response.json)

    def test_patch_data_source_valid_params(self) -> None:
        """
        Test patching/updating an existing data source with valid params

        Args:

        Returns:
            None
        """

        valid_data_source = self.data_sources[0]

        response = self.test_client.patch(
            self.data_sources_api_endpoint,
            data=json.dumps(
                {
                    api_c.CDP_DATA_SOURCE_IDS: [valid_data_source[api_c.ID]],
                    api_c.BODY: {
                        api_c.IS_ADDED: valid_data_source[api_c.IS_ADDED],
                        api_c.STATUS: valid_data_source[api_c.STATUS],
                    },
                }
            ),
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        for record in response.json:
            self.assertTrue(t_c.validate_schema(CdpDataSourceSchema(), record))

    def test_patch_data_source_invalid_params(self) -> None:
        """
        Test patching/updating an existing data source with invalid params

        Args:

        Returns:
            None
        """

        valid_data_source = self.data_sources[0]

        response = self.test_client.patch(
            self.data_sources_api_endpoint,
            data=json.dumps(
                {
                    api_c.CDP_DATA_SOURCE_IDS: [valid_data_source[api_c.ID]],
                }
            ),
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)

    def test_get_data_source_data_feed(self) -> None:
        """
        Test get data source data feeds endpoint

        Returns:

        """
        data_source_type = t_c.DATASOURCE_DATA_FEEDS_RESPONSE[api_c.BODY][0][
            api_c.DATAFEED_DATA_SOURCE_NAME
        ]
        data_source_name = t_c.DATASOURCE_DATA_FEEDS_RESPONSE[api_c.BODY][0][
            api_c.DATAFEED_DATA_SOURCE_TYPE
        ]
        # create a data source of type test_data_source
        create_data_source(
            self.database,
            name=data_source_name,
            category="",
            source_type=data_source_type,
        )

        self.request_mocker.stop()
        self.request_mocker.get(
            f"{t_c.TEST_CONFIG.CDP_CONNECTION_SERVICE}"
            f"/{api_c.CDM_CONNECTIONS_ENDPOINT}/{data_source_type}/"
            f"{api_c.DATA_FEEDS}",
            json=t_c.DATASOURCE_DATA_FEEDS_RESPONSE,
        )
        self.request_mocker.start()

        response = self.test_client.get(
            f"{t_c.BASE_ENDPOINT}{api_c.CDP_DATA_SOURCES_ENDPOINT}/"
            f"{data_source_type}/{api_c.DATAFEEDS}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIn(api_c.NAME, response.json)
        self.assertIn(api_c.TYPE, response.json)
        self.assertIn(api_c.DATAFEEDS, response.json)

        self.assertFalse(
            DataSourceDataFeedsGetSchema().validate(response.json)
        )
        self.assertFalse(
            CdpDataSourceDataFeedSchema().validate(
                response.json.get(api_c.DATAFEEDS), many=True
            )
        )
