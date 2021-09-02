"""
Purpose of this file is to house audience related tests
"""

from http import HTTPStatus
from unittest import TestCase, mock

import mongomock
import requests_mock
from huxunifylib.connectors.connector_cdp import ConnectorCDP

from huxunifylib.database.client import DatabaseClient
import huxunifylib.database.constants as db_c
from huxunifylib.database.orchestration_management import create_audience

import huxunify.test.constants as t_c
from huxunify.api import constants as api_c
from huxunify.app import create_app


class AudienceDownloadsTest(TestCase):
    """
    Test audience download
    """

    def setUp(self) -> None:
        """
        Setup tests

        Returns:

        """

        self.audiences_endpoint = (
            f"{t_c.BASE_ENDPOINT}{api_c.AUDIENCE_ENDPOINT}"
        )

        # init mongo patch initially
        mongo_patch = mongomock.patch(servers=(("localhost", 27017),))
        mongo_patch.start()

        # setup the mock DB client
        self.database = DatabaseClient(
            "localhost", 27017, None, None
        ).connect()

        mock.patch(
            "huxunify.api.route.utils.get_db_client",
            return_value=self.database,
        ).start()

        mock.patch(
            "huxunify.api.route.decorators.get_db_client",
            return_value=self.database,
        ).start()

        # mock get_db_client() in cdp_data_source
        mock.patch(
            "huxunify.api.route.audiences.get_db_client",
            return_value=self.database,
        ).start()

        # mock request for introspect call
        request_mocker = requests_mock.Mocker()
        request_mocker.post(t_c.INTROSPECT_CALL, json=t_c.VALID_RESPONSE)
        request_mocker.get(t_c.USER_INFO_CALL, json=t_c.VALID_USER_RESPONSE)
        request_mocker.get(
            t_c.CDM_HEALTHCHECK_CALL, json=t_c.CDM_HEALTHCHECK_RESPONSE
        )
        request_mocker.post(
            f"{t_c.CUSTOMER_PROFILE_API}/customer-profiles/audience",
            json=t_c.CUSTOMER_PROFILE_AUDIENCES_RESPONSE,
        )
        request_mocker.start()

        # stop all mocks in cleanup
        self.addCleanup(mock.patch.stopall)

        # setup the flask test client
        self.test_client = create_app().test_client()

        self.database.drop_database(db_c.DATA_MANAGEMENT_DATABASE)

        self.user_name = "Joe Smithers"

        # create audience first
        audience = {
            db_c.AUDIENCE_NAME: "Test Audience",
            "audience_filters": [
                {
                    api_c.AUDIENCE_SECTION_AGGREGATOR: "ALL",
                    api_c.AUDIENCE_SECTION_FILTERS: [
                        {
                            api_c.AUDIENCE_FILTER_FIELD: "filter_field",
                            api_c.AUDIENCE_FILTER_TYPE: "type",
                            api_c.AUDIENCE_FILTER_VALUE: "value",
                        }
                    ],
                }
            ],
            api_c.USER_NAME: self.user_name,
            api_c.DESTINATION_IDS: [],
        }
        self.audience = create_audience(self.database, **audience)

    def test_download_google_ads(self) -> None:
        """
        Test to check download google_ads customers hashed data

        Returns:

        """
        # mock read_batches() in ConnectorCDP class to a return a test generator
        mock.patch.object(
            ConnectorCDP,
            "read_batches",
            return_value=t_c.dataframe_generator(
                api_c.GOOGLE_ADS,
                list(api_c.DOWNLOAD_TYPES[api_c.GOOGLE_ADS].keys()),
            ),
        ).start()

        response = self.test_client.get(
            f"{t_c.BASE_ENDPOINT}{api_c.AUDIENCE_ENDPOINT}/"
            f"{self.audience[db_c.ID]}/{api_c.GOOGLE_ADS}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(response.content_type, "application/csv")

    def test_download_amazon_ads(self) -> None:
        """
        Test to check download amazon_ads customers hashed data

        Returns:

        """
        # mock read_batches() in ConnectorCDP class to a return a test generator
        mock.patch.object(
            ConnectorCDP,
            "read_batches",
            return_value=t_c.dataframe_generator(
                api_c.AMAZON_ADS,
                list(api_c.DOWNLOAD_TYPES[api_c.AMAZON_ADS].keys()),
            ),
        ).start()

        response = self.test_client.get(
            f"{t_c.BASE_ENDPOINT}{api_c.AUDIENCE_ENDPOINT}/"
            f"{self.audience[db_c.ID]}/{api_c.AMAZON_ADS}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(response.content_type, "application/csv")
