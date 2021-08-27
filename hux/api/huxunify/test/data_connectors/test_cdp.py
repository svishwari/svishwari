"""
purpose of this file is to house all the cdp tests.
"""
import datetime
import string
from unittest import TestCase, mock
from http import HTTPStatus
import requests_mock
from hypothesis import given, strategies as st

from huxunify.api import constants as api_c
from huxunify.test import constants as t_c
from huxunify.api.data_connectors.cdp import (
    clean_cdm_fields,
    DATETIME_FIELDS,
    get_demographic_by_state,
    get_city_ltvs,
    get_idr_data_feed_details,
    get_idr_data_feeds,
)
from huxunify.app import create_app


class CDPTest(TestCase):
    """
    Test CDP request methods
    """

    def setUp(self) -> None:
        """Setup tests

        Returns:

        """
        self.data_sources_api_endpoint = (
            f"{t_c.BASE_ENDPOINT}{api_c.CDP_DATA_SOURCES_ENDPOINT}"
        )

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

    @given(customer_id=st.text(alphabet=string.ascii_letters))
    def test_get_customer(self, customer_id: str):
        """Test get customer profiles

        Args:
            customer_id (str): string for testing get customer.

        Returns:

        """

        # skip empty string from hypothesis
        if not customer_id:
            return

        expected_response = {
            "code": 200,
            "body": {
                api_c.HUX_ID: customer_id,
                api_c.FIRST_NAME: "Bertie",
                api_c.LAST_NAME: "Fox",
                api_c.EMAIL: "fake@fake.com",
                api_c.GENDER: "test_gender",
                api_c.CITY: "test_city",
                api_c.ADDRESS: "test_address",
                api_c.AGE: "test_age",
            },
            "message": "ok",
        }

        self.request_mocker.stop()
        self.request_mocker.get(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/{customer_id}",
            json=expected_response,
        )
        self.request_mocker.start()

        response = self.test_client.get(
            f"{t_c.BASE_ENDPOINT}{api_c.CUSTOMERS_ENDPOINT}/{customer_id}",
            headers=t_c.AUTH_HEADER,
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        data = response.json
        self.assertTrue(data[api_c.FIRST_NAME])
        self.assertTrue(data[api_c.LAST_NAME])
        self.assertEqual(data[api_c.EMAIL], api_c.REDACTED)
        self.assertEqual(data[api_c.GENDER], api_c.REDACTED)
        self.assertEqual(data[api_c.CITY], api_c.REDACTED)
        self.assertEqual(data[api_c.ADDRESS], api_c.REDACTED)
        self.assertEqual(data[api_c.AGE], api_c.REDACTED)

    @given(
        date_text=st.one_of(
            st.text(alphabet=string.ascii_letters), st.datetimes(), st.none()
        )
    )
    def test_cdm_data_mapping(self, date_text: str):
        """Test mapped customer data types.

        Args:
            date_text (str): string for testing cdm datetime mapping.

        Returns:

        """

        # ensure no errors are raised, otherwise it will fail.
        for value in clean_cdm_fields(
            {DATETIME_FIELDS[0]: date_text}
        ).values():
            if isinstance(date_text, datetime.datetime):
                # validate it is the same
                self.assertEqual(date_text, value)
                continue

            self.assertEqual(value, None)

    def test_get_idr_data_feeds(self):
        """
        Test fetch IDR data feeds

        Args:

        Returns:

        """

        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_CONNECTION_SERVICE}"
            f"{api_c.CDM_IDENTITY_ENDPOINT}/{api_c.CDM_DATAFEEDS}",
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
            f"{api_c.CDM_IDENTITY_ENDPOINT}/{api_c.CDM_DATAFEEDS}/"
            f"{datafeed_id}",
            json=t_c.IDR_DATAFEED_DETAILS_RESPONSE,
        )
        self.request_mocker.start()

        data_feed = get_idr_data_feed_details(
            token="", datafeed_id=datafeed_id
        )

        self.assertDictEqual(
            t_c.IDR_DATAFEED_DETAILS_RESPONSE[api_c.BODY][api_c.PINNING],
            data_feed[api_c.PINNING],
        )
        self.assertDictEqual(
            t_c.IDR_DATAFEED_DETAILS_RESPONSE[api_c.BODY][api_c.STITCHED],
            data_feed[api_c.STITCHED],
        )

    def test_get_customers_insights_count_by_day(self) -> None:
        """Test get customers insights count by day

        Args:

        Returns:
            None
        """

        expected_response = {
            "code": 200,
            "body": [
                {
                    api_c.RECORDED: "2021-04-01",
                    api_c.TOTAL_COUNT: 105080,
                    api_c.DIFFERENCE_COUNT: 4321,
                },
                {
                    api_c.RECORDED: "2021-04-06",
                    api_c.TOTAL_COUNT: 108200,
                    api_c.DIFFERENCE_COUNT: 3120,
                },
            ],
            "message": "ok",
        }

        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/insights/count-by-day",
            json=expected_response,
        )
        self.request_mocker.start()

        response = self.test_client.get(
            f"{t_c.BASE_ENDPOINT}/{api_c.CUSTOMERS_INSIGHTS}/{api_c.TOTAL}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        data = response.json
        self.assertTrue(data)
        for record in data:
            self.assertTrue(record[api_c.TOTAL_CUSTOMERS])
            self.assertIn(record[api_c.TOTAL_CUSTOMERS], [105080, 108200])
            self.assertTrue(record[api_c.NEW_CUSTOMERS_ADDED])
            self.assertIn(record[api_c.NEW_CUSTOMERS_ADDED], [4321, 3120])
            self.assertTrue(record[api_c.DATE])
            self.assertIn(
                record[api_c.DATE][0:10],
                [
                    "2021-04-01",
                    "2021-04-06",
                ],
            )

    def test_get_demographic_by_state(self) -> None:
        """Test get customers insights by state

        Args:

        Returns:
            None
        """
        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/insights/count-by-state",
            json=t_c.CUSTOMERS_INSIGHTS_BY_STATES_RESPONSE,
        )
        self.request_mocker.start()

        customer_insights_by_state = get_demographic_by_state(token="")

        self.assertTrue(customer_insights_by_state)
        for i, record in enumerate(customer_insights_by_state):
            test_record = t_c.CUSTOMERS_INSIGHTS_BY_STATES_RESPONSE[
                api_c.BODY
            ][i]
            self.assertTrue(record[api_c.POPULATION_PERCENTAGE])
            self.assertEqual(record[api_c.SIZE], test_record[api_c.SIZE])
            self.assertEqual(
                record[api_c.GENDER_MEN],
                round(test_record[api_c.GENDER_MEN] / record[api_c.SIZE], 4),
            )
            self.assertEqual(
                record[api_c.GENDER_WOMEN],
                round(test_record[api_c.GENDER_WOMEN] / record[api_c.SIZE], 4),
            )
            self.assertEqual(
                record[api_c.GENDER_OTHER],
                round(test_record[api_c.GENDER_OTHER] / record[api_c.SIZE], 4),
            )

            self.assertEqual(
                api_c.STATE_NAMES.get(test_record[api_c.STATE]),
                record[api_c.NAME],
            )

    def test_get_city_ltvs(self) -> None:
        """Test get customers insights by city

        Args:

        Returns:
            None
        """
        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/insights/city-ltvs",
            json=t_c.CUSTOMERS_INSIGHTS_BY_CITIES_RESPONSE,
        )
        self.request_mocker.start()

        filters = api_c.CUSTOMER_OVERVIEW_DEFAULT_FILTER
        filters[api_c.COUNT] = 5

        customer_insights_by_cities = get_city_ltvs(token="", filters=filters)

        self.assertTrue(customer_insights_by_cities)
        for i, record in enumerate(customer_insights_by_cities):
            test_record = t_c.CUSTOMERS_INSIGHTS_BY_CITIES_RESPONSE[
                api_c.BODY
            ][i]
            self.assertEqual(record[api_c.CITY], test_record[api_c.CITY])
            self.assertEqual(record[api_c.STATE], test_record[api_c.STATE])
            self.assertEqual(record[api_c.COUNTRY], test_record[api_c.COUNTRY])
            self.assertEqual(record[api_c.AVG_LTV], test_record[api_c.AVG_LTV])

    def test_get_customers_overview(self) -> None:
        """Test get customers overview

        Args:

        Returns:
            None
        """

        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/insights",
            json=t_c.CUSTOMER_INSIGHT_RESPONSE,
        )
        self.request_mocker.start()

        response = self.test_client.get(
            f"{t_c.BASE_ENDPOINT}{api_c.CUSTOMERS_ENDPOINT}/{api_c.OVERVIEW}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)

        data = response.json
        self.assertGreaterEqual(data[api_c.GENDER_MEN], 0)
        self.assertGreaterEqual(data[api_c.GENDER_WOMEN], 0)
        self.assertGreaterEqual(data[api_c.GENDER_OTHER], 0)
        self.assertGreaterEqual(data[api_c.GENDER_MEN_COUNT], 0)
        self.assertGreaterEqual(data[api_c.GENDER_WOMEN_COUNT], 0)
        self.assertGreaterEqual(data[api_c.GENDER_OTHER_COUNT], 0)
