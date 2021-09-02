"""purpose of this file is to house all the cdp connections tests."""
from unittest import TestCase, mock
import requests_mock

from huxunify.api import constants as api_c
from huxunify.test import constants as t_c
from huxunify.api.data_connectors.cdp_connection import (
    get_idr_data_feeds,
    get_idr_data_feed_details,
    get_connections_data_feeds,
)
from huxunify.app import create_app


class CDPConnectionsTest(TestCase):
    """
    Test CDP request methods
    """

    def setUp(self) -> None:
        """Setup tests

        Returns:

        """
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

    def test_get_idr_data_feeds(self) -> None:
        """
        Test fetch IDR data feeds

        Args:

        Returns:

        """

        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_CONNECTION_SERVICE}"
            f"/{api_c.CDM_IDENTITY_ENDPOINT}/{api_c.DATAFEEDS}",
            json=t_c.IDR_DATAFEEDS_RESPONSE,
        )
        self.request_mocker.start()

        data_feeds = get_idr_data_feeds(
            token="", start_date="2021-08-02", end_date="2021-08-26"
        )

        for data_feed in data_feeds:
            self.assertIn(api_c.DATAFEED_DATA_SOURCE_TYPE, data_feed)
            self.assertIn(api_c.DATAFEED_DATA_SOURCE_NAME, data_feed)
            self.assertIn(api_c.DATAFEED_RECORDS_PROCESSED_COUNT, data_feed)
            self.assertIn(api_c.DATAFEED_NEW_IDS_COUNT, data_feed)

    def test_get_idr_data_feed_details(self):
        """
        Test fetch IDR data feed details

        Args:

        Returns:

        """
        datafeed_id = 1
        self.request_mocker.stop()
        self.request_mocker.get(
            f"{t_c.TEST_CONFIG.CDP_CONNECTION_SERVICE}"
            f"/{api_c.CDM_IDENTITY_ENDPOINT}/{api_c.DATAFEEDS}/"
            f"{datafeed_id}",
            json=t_c.IDR_DATAFEED_DETAILS_RESPONSE,
        )
        self.request_mocker.start()

        data_feed = get_idr_data_feed_details(
            token="", datafeed_id=datafeed_id
        )

        self.assertIn(api_c.PINNING, data_feed)
        self.assertIn(api_c.STITCHED, data_feed)

    def test_get_connections_data_feeds(self) -> None:
        """
        Test fetch data source data feeds

        Args:

        Returns:

        """
        data_source_type = "test_data_source"

        self.request_mocker.stop()
        self.request_mocker.get(
            f"{t_c.TEST_CONFIG.CDP_CONNECTION_SERVICE}"
            f"/{api_c.CDM_CONNECTIONS_ENDPOINT}/{data_source_type}/"
            f"{api_c.DATA_FEEDS}",
            json=t_c.DATASOURCE_DATA_FEEDS_RESPONSE,
        )
        self.request_mocker.start()

        data_feeds = get_connections_data_feeds(
            token="", data_source_type=data_source_type
        )

        for data_feed in data_feeds:
            self.assertIn(api_c.DATAFEED_DATA_SOURCE_TYPE, data_feed)
            self.assertIn(api_c.DATAFEED_DATA_SOURCE_NAME, data_feed)
            self.assertIn(api_c.NAME, data_feed)
            self.assertIn(api_c.RECORDS_PROCESSED, data_feed)
            self.assertIn(api_c.RECORDS_RECEIVED, data_feed)
            self.assertIn(api_c.RECORDS_PROCESSED_PERCENTAGE, data_feed)
            self.assertIn(api_c.THIRTY_DAYS_AVG, data_feed)
