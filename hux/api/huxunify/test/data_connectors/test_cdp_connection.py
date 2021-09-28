"""purpose of this file is to house all the cdp connections tests."""
from unittest import TestCase, mock
import string
import requests_mock
from hypothesis import given, strategies as st

from huxunify.api import constants as api_c
from huxunify.api.exceptions.integration_api_exceptions import (
    FailedAPIDependencyError,
)
from huxunify.test import constants as t_c
from huxunify.api.data_connectors.cdp_connection import (
    get_idr_data_feeds,
    get_idr_data_feed_details,
    get_data_source_data_feeds,
    get_idr_matching_trends, get_data_sources,
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

    def test_get_data_sources(self) -> None:
        """Test fetch data sources"""
        self.request_mocker.stop()
        self.request_mocker.get(
            f"{t_c.TEST_CONFIG.CDP_CONNECTION_SERVICE}"
            f"/{api_c.CDM_CONNECTIONS_ENDPOINT}/{api_c.DATASOURCES}",
            json=t_c.DATASOURCES_RESPONSE,
        )
        self.request_mocker.start()

        data_sources = get_data_sources(token="")

        for data_source in data_sources:
            self.assertIn(api_c.NAME, data_source)
            self.assertIn(api_c.LABEL, data_source)
            self.assertIn(api_c.STATUS, data_source)

    def test_get_data_source_data_feeds(self) -> None:
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
            self.assertIn(api_c.THIRTY_DAYS_AVG, data_feed)

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

        Returns:
            None
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

        Returns:
            None
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
    def test_get_data_source_data_feeds_raise_dependency_error(
        self, data_source_type: str
    ) -> None:
        """Test get data source data feeds raise dependency error.

        Args:
            data_source_type (str): data source type value for request.

        Returns:
            None
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

        Returns:
            None
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
