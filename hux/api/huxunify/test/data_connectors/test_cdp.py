"""Purpose of this file is to house all the cdp tests."""
from datetime import datetime
import string
from unittest import TestCase, mock
from http import HTTPStatus
import requests_mock
import mongomock
from dateutil.relativedelta import relativedelta
from hypothesis import given, strategies as st, settings

import huxunifylib.database.constants as db_c
from huxunifylib.database.client import DatabaseClient
from huxunify.api import constants as api_c
from huxunify.api.exceptions.integration_api_exceptions import (
    FailedAPIDependencyError,
)
from huxunify.api.schema.customers import CustomerRevenueInsightsSchema
from huxunify.api.data_connectors.cdp import (
    clean_cdm_fields,
    clean_cdm_gender_fields,
    DATETIME_FIELDS,
    get_demographic_by_state,
    get_city_ltvs,
    get_customers_overview,
    get_customer_profiles,
    get_customer_profile,
    get_customer_events_data,
    get_customer_count_by_state,
    get_demographic_by_country,
    get_customers_insights_count_by_day,
    get_spending_by_gender,
    get_revenue_by_day,
    get_customer_event_types,
    get_customer_product_categories,
)
from huxunify.api.data_connectors.cdp_connection import get_identity_overview
from huxunify.app import create_app
from huxunify.test import constants as t_c
from huxunify.test.route.route_test_util.test_data_loading.users import (
    load_users,
)


# pylint: disable=too-many-public-methods
class CDPTest(TestCase):
    """Test CDP API endpoint methods."""

    def setUp(self) -> None:
        """Setup tests."""

        # setup the flask test client
        self.test_client = create_app().test_client()

        self.request_mocker = requests_mock.Mocker()
        self.request_mocker.post(
            t_c.INTROSPECT_CALL, json=t_c.VALID_INTROSPECTION_RESPONSE
        )
        self.request_mocker.start()

        # setup the mock DB client
        # init mongo patch initially
        mongo_patch = mongomock.patch(servers=(("localhost", 27017),))
        mongo_patch.start()

        self.database = DatabaseClient(
            "localhost", 27017, None, None
        ).connect()

        load_users(self.database)

        mock.patch(
            "huxunify.api.route.customers.get_db_client",
            return_value=self.database,
        ).start()

        mock.patch(
            "huxunify.api.route.utils.get_db_client",
            return_value=self.database,
        ).start()

        mock.patch(
            "huxunify.api.data_connectors.cache.get_db_client",
            return_value=self.database,
        ).start()

        mock.patch(
            "huxunify.api.route.utils.get_user_info",
            return_value=t_c.VALID_USER_RESPONSE,
        ).start()

        self.database.drop_database(db_c.DATA_MANAGEMENT_DATABASE)
        self.addCleanup(mock.patch.stopall)

    def test_get_customer(self):
        """Test get customer profiles."""

        hux_id = "HUX123456789012345"

        expected_response = {
            "code": 200,
            "body": {
                api_c.HUX_ID: hux_id,
                api_c.FIRST_NAME: "Bertie",
                api_c.LAST_NAME: "Fox",
                api_c.EMAIL: "fake@fake.com",
                api_c.GENDER: "test_gender",
                api_c.CITY: "test_city",
                api_c.ADDRESS: "test_address",
                api_c.AGE: "test_age",
                api_c.IDENTITY_RESOLUTION: {
                    api_c.NAME: {
                        api_c.PERCENTAGE: 0.26,
                        api_c.COUNT: 23,
                        api_c.DATA_SOURCE: [
                            {
                                api_c.ID: "585t749997acad4bac4373b",
                                api_c.NAME: "Netsuite",
                                api_c.TYPE: "Net-suite",
                                api_c.PERCENTAGE: 0.49,
                                api_c.COUNT: 15,
                            },
                            {
                                api_c.ID: "685t749997acad4bac4373b",
                                api_c.NAME: "Aqfer",
                                api_c.TYPE: "Aqfer",
                                api_c.PERCENTAGE: 0.51,
                                api_c.COUNT: 5,
                            },
                        ],
                        api_c.CO_OCCURRENCES: [
                            {
                                api_c.IDENTIFIER: "address",
                                api_c.COUNT: 10,
                                api_c.PERCENTAGE: 0.5,
                            },
                            {
                                api_c.IDENTIFIER: "email",
                                api_c.COUNT: 10,
                                api_c.PERCENTAGE: 0.5,
                            },
                        ],
                    },
                    api_c.ADDRESS: {
                        api_c.PERCENTAGE: 0.2,
                        api_c.COUNT: 12,
                        api_c.DATA_SOURCE: [],
                        api_c.CO_OCCURRENCES: [],
                    },
                    "email": {
                        api_c.PERCENTAGE: 0.34,
                        api_c.COUNT: 2,
                        api_c.DATA_SOURCE: [],
                        api_c.CO_OCCURRENCES: [],
                    },
                    "phone": {
                        api_c.PERCENTAGE: 0.14,
                        api_c.COUNT: 7,
                        api_c.DATA_SOURCE: [],
                        api_c.CO_OCCURRENCES: [],
                    },
                    "cookie": {
                        api_c.PERCENTAGE: 0.1,
                        api_c.COUNT: 5,
                        api_c.DATA_SOURCE: [],
                        api_c.CO_OCCURRENCES: [],
                    },
                },
            },
            "message": "ok",
        }

        self.request_mocker.stop()
        self.request_mocker.get(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/{hux_id}",
            json=expected_response,
        )
        self.request_mocker.start()

        response = self.test_client.get(
            f"{t_c.BASE_ENDPOINT}{api_c.CUSTOMERS_ENDPOINT}/{hux_id}",
            headers=t_c.AUTH_HEADER,
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        data = response.json
        self.assertTrue(data[api_c.OVERVIEW])
        self.assertTrue(data[api_c.OVERVIEW][api_c.FIRST_NAME])
        self.assertTrue(data[api_c.OVERVIEW][api_c.LAST_NAME])
        self.assertTrue(data[api_c.INSIGHTS])
        self.assertEqual(data[api_c.INSIGHTS][api_c.EMAIL], api_c.REDACTED)
        self.assertEqual(data[api_c.INSIGHTS][api_c.GENDER], api_c.REDACTED)
        self.assertEqual(data[api_c.INSIGHTS][api_c.CITY], api_c.REDACTED)
        self.assertEqual(data[api_c.INSIGHTS][api_c.ADDRESS], api_c.REDACTED)
        self.assertEqual(data[api_c.INSIGHTS][api_c.AGE], api_c.REDACTED)

    @given(
        date_text=st.one_of(
            st.text(alphabet=string.ascii_letters), st.datetimes(), st.none()
        )
    )
    def test_cdm_data_mapping(self, date_text: str):
        """Test mapped customer data types.

        Args:
            date_text (str): string for testing cdm datetime mapping.
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
        """Test get customers insights count by day."""

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

    def test_get_demographic_by_country_no_filter(self) -> None:
        """Test get customers insights by country."""

        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/countries",
            json=t_c.CUSTOMERS_INSIGHTS_BY_COUNTRIES_RESPONSE,
        )
        self.request_mocker.start()

        countries = set(
            data[api_c.COUNTRY]
            for data in t_c.CUSTOMERS_INSIGHTS_BY_COUNTRIES_RESPONSE[
                api_c.BODY
            ]
        )

        customer_insights_by_country = get_demographic_by_country("")

        self.assertTrue(customer_insights_by_country)
        self.assertEqual(len(countries), len(customer_insights_by_country))
        for record in customer_insights_by_country:
            self.assertIn(api_c.COUNTRY, record)
            self.assertIn(record[api_c.COUNTRY], countries)
            self.assertIn(api_c.SIZE, record)
            self.assertIn(api_c.LTV, record)

    def test_get_demographic_by_country_with_single_state_filter(self) -> None:
        """Test get customers insights by country with filter."""

        filters = [
            {
                "section_aggregator": "ALL",
                "section_filters": [
                    {"field": "State", "type": "equals", "value": "CO"}
                ],
            }
        ]

        expected_response = {
            "code": 200,
            "body": [
                {
                    api_c.STATE: "CO",
                    api_c.COUNTRY: "Test Country",
                    api_c.GENDER_MEN: 2656,
                    api_c.GENDER_WOMEN: 2344,
                    api_c.GENDER_OTHER: 12,
                    api_c.SIZE: 1234,
                    api_c.AVG_LTV: 324.45,
                }
            ],
            "message": "ok",
        }
        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/countries",
            json=t_c.CUSTOMERS_INSIGHTS_BY_COUNTRIES_RESPONSE,
        )
        self.request_mocker.start()

        customer_insights_by_country = get_demographic_by_country(
            token="", filters=filters
        )

        self.assertTrue(customer_insights_by_country)
        self.assertIn(api_c.COUNTRY, customer_insights_by_country[0])
        self.assertEqual(
            expected_response[api_c.BODY][0][api_c.COUNTRY],
            customer_insights_by_country[0][api_c.COUNTRY],
        )
        self.assertIn(api_c.SIZE, customer_insights_by_country[0])
        self.assertEqual(
            expected_response[api_c.BODY][0][api_c.SIZE],
            customer_insights_by_country[0][api_c.SIZE],
        )
        self.assertIn(api_c.LTV, customer_insights_by_country[0])
        self.assertEqual(
            expected_response[api_c.BODY][0][api_c.AVG_LTV],
            customer_insights_by_country[0][api_c.LTV],
        )

    def test_get_demographic_by_state(self) -> None:
        """Test get customers insights by state."""

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
            self.assertEqual(
                test_record[api_c.COUNTRY],
                record[api_c.COUNTRY],
            )

    def test_get_city_ltvs(self) -> None:
        """Test get customers insights by city."""

        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/insights/city-ltvs",
            json=t_c.CUSTOMERS_INSIGHTS_BY_CITIES_RESPONSE,
        )
        self.request_mocker.start()

        customer_insights_by_cities = get_city_ltvs(
            token="",
            filters={
                api_c.AUDIENCE_FILTERS: api_c.CUSTOMER_OVERVIEW_DEFAULT_FILTER
            },
        )

        self.assertTrue(customer_insights_by_cities)
        for i, record in enumerate(customer_insights_by_cities):
            test_record = t_c.CUSTOMERS_INSIGHTS_BY_CITIES_RESPONSE[
                api_c.BODY
            ][i]
            self.assertEqual(record[api_c.COUNTRY], test_record[api_c.COUNTRY])
            self.assertEqual(record[api_c.CITY], test_record[api_c.CITY])
            self.assertEqual(record[api_c.STATE], test_record[api_c.STATE])
            self.assertEqual(record[api_c.COUNTRY], test_record[api_c.COUNTRY])
            self.assertEqual(record[api_c.AVG_LTV], test_record[api_c.AVG_LTV])

    def test_get_customers_overview_raise_dependency_error(self) -> None:
        """Test get customers overview raise dependency error."""

        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/insights",
            json={},
        )
        self.request_mocker.start()

        with self.assertRaises(FailedAPIDependencyError):
            get_customers_overview(token=t_c.TEST_AUTH_TOKEN)

    def test_get_customer_profiles_raise_dependency_error(self) -> None:
        """Test get customer profiles raise dependency error."""

        self.request_mocker.stop()
        self.request_mocker.get(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles",
            json={},
        )
        self.request_mocker.start()

        with self.assertRaises(FailedAPIDependencyError):
            get_customer_profiles(
                token=t_c.TEST_AUTH_TOKEN, batch_size=5, offset=3
            )

    @given(customer_id=st.text(alphabet=string.ascii_letters))
    def test_get_customer_profile_raise_dependency_error(
        self, customer_id: str
    ) -> None:
        """Test get customer profile raise dependency error.

        Args:
            customer_id (str): customer ID value for request.
        """

        self.request_mocker.stop()
        self.request_mocker.get(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/{customer_id}",
            json={},
        )
        self.request_mocker.start()

        with self.assertRaises(FailedAPIDependencyError):
            get_customer_profile(token=t_c.TEST_AUTH_TOKEN, hux_id=customer_id)

    def test_get_idr_overview_raise_dependency_error(self) -> None:
        """Test get IDR overview raise dependency error."""

        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_CONNECTION_SERVICE}/"
            f"{api_c.CDM_IDENTITY_ENDPOINT}/{api_c.INSIGHTS}",
            json={},
        )
        self.request_mocker.start()

        with self.assertRaises(FailedAPIDependencyError):
            get_identity_overview(token=t_c.TEST_AUTH_TOKEN)

    @given(customer_id=st.text(alphabet=string.ascii_letters))
    def test_get_customer_events_raise_dependency_error(
        self, customer_id: str
    ) -> None:
        """Test get customer events raise dependency error.

        Args:
            customer_id (str): customer ID value for request.
        """

        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/{customer_id}/events",
            json={},
        )
        self.request_mocker.start()

        with self.assertRaises(FailedAPIDependencyError):
            get_customer_events_data(
                token=t_c.TEST_AUTH_TOKEN,
                hux_id=customer_id,
                start_date_str=datetime.utcnow()
                .date()
                .strftime(api_c.DEFAULT_DATE_FORMAT),
                end_date_str=datetime.utcnow()
                .date()
                .strftime(api_c.DEFAULT_DATE_FORMAT),
                interval="day",
            )

    def test_get_customer_count_by_state_raise_dependency_error(self) -> None:
        """Test get customer count by state raise dependency error."""

        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/insights/count-by-state",
            json={},
        )
        self.request_mocker.start()

        with self.assertRaises(FailedAPIDependencyError):
            get_customer_count_by_state(token=t_c.TEST_AUTH_TOKEN)

    def test_get_demographic_by_state_raise_dependency_error(self) -> None:
        """Test get customer demographic by state raise dependency error."""

        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/insights/count-by-state",
            json={},
        )
        self.request_mocker.start()

        with self.assertRaises(FailedAPIDependencyError):
            get_demographic_by_state(token=t_c.TEST_AUTH_TOKEN)

    def test_get_demographic_by_country_raise_dependency_error(self) -> None:
        """Test get customer demographic by country raise dependency error."""

        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.CUSTOMER_PROFILE_API}/customer-profiles/countries",
            json={},
        )
        self.request_mocker.start()

        with self.assertRaises(FailedAPIDependencyError):
            get_demographic_by_country(token=t_c.TEST_AUTH_TOKEN)

    @given(
        date_filters=st.fixed_dictionaries(
            {
                api_c.START_DATE: st.dates().map(
                    lambda date: date.strftime(api_c.DEFAULT_DATE_FORMAT)
                ),
                api_c.END_DATE: st.dates().map(
                    lambda date: date.strftime(api_c.DEFAULT_DATE_FORMAT)
                ),
            }
        )
    )
    def test_get_customers_count_by_day_raise_dependency_error(
        self, date_filters: dict
    ) -> None:
        """Test get customers insights count by day raise dependency error.

        Args:
            date_filters (dict): date filters dictionary.
        """

        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/insights/count-by-day",
            json={},
        )
        self.request_mocker.start()

        with self.assertRaises(FailedAPIDependencyError):
            get_customers_insights_count_by_day(
                token=t_c.TEST_AUTH_TOKEN, date_filters=date_filters
            )

    def test_get_city_ltvs_raise_dependency_error(self) -> None:
        """Test get customers insights by city raise dependency error."""

        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.CUSTOMER_PROFILE_API}/customer-profiles/insights/city-ltvs",
            json={},
        )
        self.request_mocker.start()

        with self.assertRaises(FailedAPIDependencyError):
            get_city_ltvs(token=t_c.TEST_AUTH_TOKEN)

    @given(
        start_date=st.dates().map(
            lambda date: date.strftime(api_c.DEFAULT_DATE_FORMAT)
        ),
        end_date=st.dates().map(
            lambda date: date.strftime(api_c.DEFAULT_DATE_FORMAT)
        ),
    )
    @settings(deadline=None)
    def test_get_spending_by_gender_raise_dependency_error(
        self, start_date: str, end_date: str
    ) -> None:
        """Test get customer spending by gender raise dependency error.

        Args:
            start_date (str): start date value for request.
            end_date (str): end date value for request.
        """

        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/insights/spending-by-month",
            json={},
        )
        self.request_mocker.start()

        with self.assertRaises(FailedAPIDependencyError):
            get_spending_by_gender(
                token=t_c.TEST_AUTH_TOKEN,
                start_date=start_date,
                end_date=end_date,
            )

    def test_get_revenue_by_day(self) -> None:
        """Test get customer revenue by day."""
        start_date = datetime.utcnow().date() - relativedelta(month=6)
        end_date = datetime.utcnow().date()
        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/insights"
            f"/spending-by-day",
            json=t_c.MOCKED_GENDER_SPENDING_BY_DAY,
        )
        self.request_mocker.start()

        revenue_by_day = CustomerRevenueInsightsSchema().dump(
            get_revenue_by_day(
                token=t_c.TEST_AUTH_TOKEN,
                start_date=datetime.strftime(
                    start_date, api_c.DEFAULT_DATE_FORMAT
                ),
                end_date=datetime.strftime(
                    end_date, api_c.DEFAULT_DATE_FORMAT
                ),
            ),
            many=True,
        )

        self.assertTrue(
            t_c.validate_schema(
                CustomerRevenueInsightsSchema(), revenue_by_day, True
            )
        )

    def test_get_customer_event_types(self) -> None:
        """Test get customer event types."""
        self.request_mocker.stop()
        self.request_mocker.get(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/event-types",
            json=t_c.MOCKED_CUSTOMER_EVENT_TYPES,
        )
        self.request_mocker.start()

        event_types = get_customer_event_types(token=t_c.TEST_AUTH_TOKEN)
        self.assertIsNotNone(event_types)
        self.assertEqual(len(event_types), 3)

    def test_get_product_categories(self) -> None:
        """Test get product categories."""

        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/products-by-categories",
            json=t_c.CUSTOMERS_PRODUCT_CATEGORIES_RESPONSE,
        )
        self.request_mocker.start()

        customer_product_categories = get_customer_product_categories("")

        self.assertTrue(customer_product_categories)
        self.assertEqual(len(customer_product_categories.keys()), 1)
        self.assertEqual(
            list(customer_product_categories.keys())[0], "Shoes & accessories"
        )


class CdpFieldTests(TestCase):
    """Test CDP Field methods."""

    def test_cdm_clean_gender_fields(self):
        """Test clean_cdm_gender_fields function."""

        # ensure no errors are raised, otherwise it will fail.
        partial_none_response = {
            "total_records": 316574,
            "match_rate": 0.5,
            "total_unique_ids": 156485,
            "total_unknown_ids": 0,
            "total_known_ids": 156485,
            "total_individual_ids": 126629,
            "total_household_ids": 31658,
            "updated": datetime(2021, 7, 30, 11, 28, 49, 109000),
            "total_customers": 0,
            "total_countries": 0,
            "total_us_states": 0,
            "total_cities": 0,
            "min_age": None,
            "max_age": None,
            "avg_age": None,
            "gender_women": None,
            "gender_men": None,
            "gender_other": None,
            "max_ltv_actual": None,
            "max_ltv_predicted": None,
            "min_ltv_actual": None,
            "min_ltv_predicted": None,
        }

        self.assertDictEqual(
            clean_cdm_gender_fields(partial_none_response),
            partial_none_response,
        )
