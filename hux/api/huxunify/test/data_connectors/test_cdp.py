"""
purpose of this file is to house all the cdp tests.
"""
from datetime import datetime
import string
from unittest import TestCase, mock
from http import HTTPStatus
import requests_mock
from dateutil.relativedelta import relativedelta
from hypothesis import given, strategies as st

from huxunify.api import constants as api_c
from huxunify.test import constants as t_c
from huxunify.api.data_connectors.cdp import (
    clean_cdm_fields,
    DATETIME_FIELDS,
    get_demographic_by_state,
    get_city_ltvs,
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
            if isinstance(date_text, datetime):
                # validate it is the same
                self.assertEqual(date_text, value)
                continue

            self.assertEqual(value, None)

    def test_get_customers_insights_count_by_day(self) -> None:
        """Test get customers insights count by day

        Args:

        Returns:
            None
        """
        start_date = datetime.utcnow().date() - relativedelta(months=9)
        end_date = datetime.utcnow().date()
        expected_response = {
            "code": 200,
            "body": [
                {
                    api_c.RECORDED: datetime.strftime(
                        start_date + relativedelta(days=14), "%Y-%m-%d"
                    ),
                    api_c.TOTAL_COUNT: 105080,
                    api_c.DIFFERENCE_COUNT: 4321,
                },
                {
                    api_c.RECORDED: datetime.strftime(
                        end_date - relativedelta(days=14), "%Y-%m-%d"
                    ),
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
            self.assertIn(
                record[api_c.TOTAL_CUSTOMERS],
                [(105080 - 4321), 105080, 108200],
            )
            self.assertIsNotNone(record[api_c.NEW_CUSTOMERS_ADDED])
            self.assertIn(record[api_c.NEW_CUSTOMERS_ADDED], [0, 4321, 3120])
            self.assertTrue(record[api_c.DATE])
            self.assertIn(
                record[api_c.DATE][0:10],
                [
                    datetime.strftime(
                        start_date + relativedelta(days=n), "%Y-%m-%d"
                    )
                    for n in range(int((end_date - start_date).days) + 1)
                ],
            )

    def test_get_demographic_by_country(self) -> None:
        """Test get customers insights by state

        Args:

        Returns:
            None
        """
        # TODO: Uncomment and update once CDM API is available
        # self.request_mocker.stop()
        # self.request_mocker.post(
        #     f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/insights/count-by-state",
        #     json=t_c.CUSTOMERS_INSIGHTS_BY_STATES_RESPONSE,
        # )
        # self.request_mocker.start()
        #
        customer_insights_by_country = (
            t_c.CUSTOMERS_INSIGHTS_BY_COUNTRIES_RESPONSE[api_c.BODY]
        )

        self.assertTrue(customer_insights_by_country)
        for i, record in enumerate(customer_insights_by_country):
            test_record = t_c.CUSTOMERS_INSIGHTS_BY_COUNTRIES_RESPONSE[
                api_c.BODY
            ][i]
            self.assertIn(api_c.NAME, record)
            self.assertEqual(record[api_c.NAME], test_record[api_c.NAME])
            self.assertIn(api_c.SIZE, record)
            self.assertEqual(record[api_c.SIZE], test_record[api_c.SIZE])

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
