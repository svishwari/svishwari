"""
purpose of this file is to house all the cdp tests.
"""
import datetime
import string
from unittest import TestCase, mock
from http import HTTPStatus
import requests_mock
from hypothesis import given, strategies as st

from huxunifylib.database import constants as db_c

from huxunify.api import constants as api_c
from huxunify.test import constants as t_c
from huxunify.api.data_connectors.cdp import (
    clean_cdm_fields,
    DATETIME_FIELDS,
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

        # TODO: Add logic when CDM API is available
        expected_response = {
            "code": 200,
            "body": [
                {
                    api_c.DATAFEED_ID: "60e87d6d70815aade4d6c4fc",
                    api_c.DATAFEED_NAME: "Really_long_Feed_Name_106",
                    api_c.DATAFEED_DATA_SOURCE: db_c.CDP_DATA_SOURCE_BLUECORE,
                    api_c.DATAFEED_NEW_IDS_COUNT: 21,
                    api_c.DATAFEED_RECORDS_PROCESSED_COUNT: 2023532,
                    api_c.MATCH_RATE: 0.98,
                    api_c.DATAFEED_LAST_RUN_DATE: datetime.datetime.utcnow(),
                },
                {
                    api_c.DATAFEED_ID: "60e87d6d70815aade4d6c4fd",
                    api_c.DATAFEED_NAME: "Really_long_Feed_Name_105",
                    api_c.DATAFEED_DATA_SOURCE: db_c.CDP_DATA_SOURCE_BLUECORE,
                    api_c.DATAFEED_NEW_IDS_COUNT: 54,
                    api_c.DATAFEED_RECORDS_PROCESSED_COUNT: 3232,
                    api_c.MATCH_RATE: 0.97,
                    api_c.DATAFEED_LAST_RUN_DATE: datetime.datetime.utcnow()
                    - datetime.timedelta(days=1),
                },
                {
                    api_c.DATAFEED_ID: "60e87d6d70815aade4d6c4fe",
                    api_c.DATAFEED_NAME: "Really_long_Feed_Name_102",
                    api_c.DATAFEED_DATA_SOURCE: db_c.CDP_DATA_SOURCE_BLUECORE,
                    api_c.DATAFEED_NEW_IDS_COUNT: 300,
                    api_c.DATAFEED_RECORDS_PROCESSED_COUNT: 3012,
                    api_c.MATCH_RATE: 0.98,
                    api_c.DATAFEED_LAST_RUN_DATE: datetime.datetime.utcnow()
                    - datetime.timedelta(days=7),
                },
                {
                    api_c.DATAFEED_ID: "60e87d6d70815aade4d6c4ff",
                    api_c.DATAFEED_NAME: "Really_long_Feed_Name_100",
                    api_c.DATAFEED_DATA_SOURCE: db_c.CDP_DATA_SOURCE_BLUECORE,
                    api_c.DATAFEED_NEW_IDS_COUNT: 612,
                    api_c.DATAFEED_RECORDS_PROCESSED_COUNT: 2045,
                    api_c.MATCH_RATE: 0.98,
                    api_c.DATAFEED_LAST_RUN_DATE: datetime.datetime.utcnow()
                    - datetime.timedelta(days=30),
                },
            ],
            "message": "ok",
        }

        self.assertEqual(HTTPStatus.OK, expected_response["code"])

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
