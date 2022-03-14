"""Purpose of this file is to house all the cdp connections tests."""
from http import HTTPStatus
from unittest import TestCase, mock
import string

import requests_mock
from hypothesis import given, strategies as st, settings
from requests_mock import Mocker

from huxunify.api import constants as api_c
from huxunify.api.config import get_config
from huxunify.api.exceptions.integration_api_exceptions import (
    FailedAPIDependencyError,
)
from huxunify.api.data_connectors.cdp_connection import (
    get_idr_data_feeds,
    get_idr_data_feed_details,
    get_data_source_data_feeds,
    get_idr_matching_trends,
    get_data_sources,
    check_cdp_connections_api_connection,
    get_identity_overview,
)
from huxunify.test import constants as t_c
from huxunify.app import create_app


class CDPConnectionsTest(TestCase):
    """Test CDP request methods."""

    def setUp(self) -> None:
        """Setup tests."""

        # setup the flask test client
        self.test_client = create_app().test_client()

        self.config = get_config(api_c.TEST_MODE)
        self.request_mocker = requests_mock.Mocker()
        self.request_mocker.post(
            t_c.INTROSPECT_CALL, json=t_c.VALID_INTROSPECTION_RESPONSE
        )
        self.request_mocker.start()

        self.addCleanup(mock.patch.stopall)

    def tearDown(self) -> None:
        """Tear down tests."""

        self.request_mocker.stop()

    @requests_mock.Mocker()
    def test_check_cdp_connections_api_connection_success(
        self, request_mocker: Mocker
    ) -> None:
        """Test cdp connections health check function success.

        Args:
            request_mocker (Mocker): request_mocker object
        """
        request_mocker.get(
            f"{self.config.CDP_CONNECTION_SERVICE}/healthcheck",
            json={
                "code": 200,
                "status": "success",
                "message": "Health Check Performed",
            },
        )
        status, message = check_cdp_connections_api_connection()
        self.assertTrue(status)
        self.assertEqual("CDP connections available.", message)

    @requests_mock.Mocker()
    def test_check_cdp_connections_api_connection_failure(
        self, request_mocker: Mocker
    ) -> None:
        """Test cdp connections health check function failure.

        Args:
            request_mocker (Mocker): request_mocker object
        """
        request_mocker.get(
            f"{self.config.CDP_CONNECTION_SERVICE}/healthcheck",
            status_code=HTTPStatus.BAD_REQUEST,
        )
        status, message = check_cdp_connections_api_connection()
        self.assertFalse(status)
        self.assertEqual(
            f"CDP connections not available. Received {HTTPStatus.BAD_REQUEST}",
            message,
        )

    def test_get_idr_data_feeds(self) -> None:
        """Test fetch IDR data feeds."""

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
        """Test fetch IDR data feed details."""

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

    def test_get_data_sources(self) -> None:
        """Test fetch data sources."""

        self.request_mocker.stop()
        self.request_mocker.get(
            f"{t_c.TEST_CONFIG.CDP_CONNECTION_SERVICE}"
            f"/{api_c.CDM_CONNECTIONS_ENDPOINT}/{api_c.DATASOURCES}",
            json=t_c.DATASOURCES_RESPONSE,
        )
        self.request_mocker.start()

        data_sources = get_data_sources(token="")

        self.assertCountEqual(
            data_sources, t_c.DATASOURCES_RESPONSE[api_c.BODY]
        )
        self.assertEqual(data_sources, t_c.DATASOURCES_RESPONSE[api_c.BODY])

        for idx, data_source in enumerate(data_sources):
            self.assertIn(api_c.NAME, data_source)
            self.assertIn(api_c.LABEL, data_source)
            self.assertIn(api_c.STATUS, data_source)
            self.assertEqual(
                data_source, t_c.DATASOURCES_RESPONSE[api_c.BODY][idx]
            )

    def test_get_data_source_data_feeds(self) -> None:
        """Test fetch data source data feeds."""

        data_source_type = "test_data_source"

        self.request_mocker.stop()
        self.request_mocker.get(
            f"{t_c.TEST_CONFIG.CDP_CONNECTION_SERVICE}"
            f"/{api_c.CDM_CONNECTIONS_ENDPOINT}/{data_source_type}/"
            f"{api_c.DATA_FEEDS}",
            json=t_c.DATASOURCE_DATA_FEEDS_RESPONSE,
        )
        self.request_mocker.start()

        data_feeds = get_data_source_data_feeds(
            token="", data_source_type=data_source_type
        )

        for data_feed in data_feeds:
            self.assertIn(api_c.DATAFEED_DATA_SOURCE_TYPE, data_feed)
            self.assertIn(api_c.DATAFEED_DATA_SOURCE_NAME, data_feed)
            self.assertIn(api_c.NAME, data_feed)
            self.assertIn(api_c.RECORDS_PROCESSED, data_feed)
            self.assertIn(api_c.RECORDS_RECEIVED, data_feed)
            self.assertIn(api_c.RECORDS_PROCESSED_PERCENTAGE, data_feed)
            self.assertIn(
                api_c.VALUE, data_feed[api_c.RECORDS_PROCESSED_PERCENTAGE]
            )
            self.assertIn(
                api_c.FLAG_INDICATOR,
                data_feed[api_c.RECORDS_PROCESSED_PERCENTAGE],
            )
            self.assertIn(api_c.THIRTY_DAYS_AVG, data_feed)
            self.assertIn(api_c.VALUE, data_feed[api_c.THIRTY_DAYS_AVG])
            self.assertIn(
                api_c.FLAG_INDICATOR, data_feed[api_c.THIRTY_DAYS_AVG]
            )

    @given(
        start_date=st.dates().map(
            lambda date: date.strftime(api_c.DEFAULT_DATE_FORMAT)
        ),
        end_date=st.dates().map(
            lambda date: date.strftime(api_c.DEFAULT_DATE_FORMAT)
        ),
    )
    def test_get_idr_data_feeds_raise_dependency_error(
        self, start_date: str, end_date: str
    ) -> None:
        """Test get IDR data feeds raise dependency error.

        Args:
            start_date (str): start date value for request.
            end_date (str): end date value for request.
        """

        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_CONNECTION_SERVICE}"
            f"/{api_c.CDM_IDENTITY_ENDPOINT}/{api_c.DATAFEEDS}",
            json={},
        )
        self.request_mocker.start()

        with self.assertRaises(FailedAPIDependencyError):
            get_idr_data_feeds(
                token=t_c.TEST_AUTH_TOKEN,
                start_date=start_date,
                end_date=end_date,
            )

    @given(datafeed_id=st.integers(min_value=1, max_value=10))
    def test_get_idr_data_feed_details_raise_dependency_error(
        self, datafeed_id: int
    ) -> None:
        """Test get IDR data feed details raise dependency error.

        Args:
            datafeed_id (int): datafeed ID value for request.
        """

        self.request_mocker.stop()
        self.request_mocker.get(
            f"{t_c.TEST_CONFIG.CDP_CONNECTION_SERVICE}"
            f"/{api_c.CDM_IDENTITY_ENDPOINT}/{api_c.DATAFEEDS}/"
            f"{datafeed_id}",
            json={},
        )
        self.request_mocker.start()

        with self.assertRaises(FailedAPIDependencyError):
            get_idr_data_feed_details(
                token=t_c.TEST_AUTH_TOKEN, datafeed_id=datafeed_id
            )

    @given(data_source_type=st.text(alphabet=string.ascii_letters))
    @settings(deadline=100)
    def test_get_data_source_data_feeds_raise_dependency_error(
        self, data_source_type: str
    ) -> None:
        """Test get data source data feeds raise dependency error.

        Args:
            data_source_type (str): data source type value for request.
        """

        self.request_mocker.stop()
        self.request_mocker.get(
            f"{t_c.TEST_CONFIG.CDP_CONNECTION_SERVICE}"
            f"/{api_c.CDM_CONNECTIONS_ENDPOINT}/{data_source_type}/"
            f"{api_c.DATA_FEEDS}",
            json={},
        )
        self.request_mocker.start()

        with self.assertRaises(FailedAPIDependencyError):
            get_data_source_data_feeds(
                token=t_c.TEST_AUTH_TOKEN, data_source_type=data_source_type
            )

    @given(
        start_date=st.dates().map(
            lambda date: date.strftime(api_c.DEFAULT_DATE_FORMAT)
        ),
        end_date=st.dates().map(
            lambda date: date.strftime(api_c.DEFAULT_DATE_FORMAT)
        ),
    )
    def test_get_idr_matching_trends_raise_dependency_error(
        self, start_date: str, end_date: str
    ) -> None:
        """Test get IDR matching trends raise dependency error.

        Args:
            start_date (str): start date value for request.
            end_date (str): end date value for request.
        """

        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_CONNECTION_SERVICE}/identity/id-count-by"
            f"-day",
            json={},
        )
        self.request_mocker.start()

        with self.assertRaises(FailedAPIDependencyError):
            get_idr_matching_trends(
                token=t_c.TEST_AUTH_TOKEN,
                start_date=start_date,
                end_date=end_date,
            )

    def test_get_identity_overview(self):
        """Test fetching identity overview"""
        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_CONNECTION_SERVICE}/"
            f"{api_c.CDM_IDENTITY_ENDPOINT}/{api_c.INSIGHTS}",
            json=t_c.IDENTITY_INSIGHT_RESPONSE,
        )
        self.request_mocker.start()

        identity_insights = get_identity_overview(token="")

        self.assertEqual(
            t_c.IDENTITY_INSIGHT_RESPONSE[api_c.BODY], identity_insights
        )

    def test_get_identity_overview_raise_dependency_error(self):
        """Test fetching identity overview with default filter"""
        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_CONNECTION_SERVICE}/"
            f"{api_c.CDM_IDENTITY_ENDPOINT}/{api_c.INSIGHTS}",
            json={},
        )
        self.request_mocker.start()

        with self.assertRaises(FailedAPIDependencyError):
            get_identity_overview(token="")
