"""Purpose of this file is to house all the customers api tests."""
import json
import string
from unittest import mock
from http import HTTPStatus

from hypothesis import given, strategies as st

from huxunify.test.route.route_test_util.route_test_case import RouteTestCase
import huxunify.test.constants as t_c
from huxunify.api import constants as api_c
from huxunify.api.schema.customers import (
    DataFeedDetailsSchema,
    DataFeedSchema,
    CustomersInsightsCitiesSchema,
    CustomersInsightsStatesSchema,
    CustomersInsightsCountriesSchema,
    CustomerRevenueInsightsSchema,
    CustomerOverviewSchema,
    CustomerProfileContactPreferencesSchema,
    IDROverviewSchema,
)
from huxunify.api.data_connectors.cdp import (
    get_geographic_customers_data,
    clean_cdm_fields,
)
from huxunify.api.schema.customers import (
    CustomerGeoVisualSchema,
    CustomerDemographicInsightsSchema,
    CustomerSpendingInsightsSchema,
    CustomerGenderInsightsSchema,
    CustomerIncomeInsightsSchema,
    MatchingTrendsSchema,
    CustomerEventsSchema,
    TotalCustomersInsightsSchema,
)

# pylint: disable=too-many-public-methods,too-many-lines
from huxunify.test.route.route_test_util.test_data_loading.users import (
    load_users,
)


class TestCustomersOverview(RouteTestCase):
    """Purpose of this class is to test Customers overview."""

    def setUp(self):  # pylint: disable=arguments-differ
        """Sets up Test Client."""

        super().setUp()

        load_users(self.database)

        self.customers = f"{t_c.BASE_ENDPOINT}{api_c.CUSTOMERS_ENDPOINT}"
        self.idr = f"{t_c.BASE_ENDPOINT}{api_c.IDR_ENDPOINT}"

        mock.patch(
            "huxunify.api.route.customers.get_db_client",
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

    def test_get_customers(self):
        """Test get customers."""

        hux_id = "HUX123456789012345"

        expected_response = {
            "code": 200,
            "body": [
                {
                    api_c.HUX_ID: hux_id,
                    api_c.FIRST_NAME: "Bertie",
                    api_c.LAST_NAME: "Fox",
                    api_c.MATCH_CONFIDENCE: 0.97,
                },
            ],
            "message": "ok",
        }
        self.request_mocker.stop()
        self.request_mocker.get(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles",
            json=expected_response,
        )
        self.request_mocker.start()

        response = self.app.get(
            f"{self.customers}?{api_c.QUERY_PARAMETER_BATCH_SIZE}="
            f"{api_c.CUSTOMERS_DEFAULT_BATCH_SIZE}&"
            f"{api_c.QUERY_PARAMETER_BATCH_NUMBER}="
            f"{api_c.DEFAULT_BATCH_NUMBER}",
            headers=t_c.STANDARD_HEADERS,
        )
        self.assertEqual(HTTPStatus.OK, response.status_code)
        data = response.json

        response = self.app.get(
            f"{self.customers}",
            headers=t_c.STANDARD_HEADERS,
        )
        self.assertEqual(HTTPStatus.OK, response.status_code)

        self.assertEqual(data[api_c.TOTAL_CUSTOMERS], 1)
        self.assertTrue(data[api_c.CUSTOMERS_TAG])
        customer = data[api_c.CUSTOMERS_TAG][0]
        self.assertEqual(customer[api_c.FIRST_NAME], "Bertie")
        self.assertEqual(customer[api_c.LAST_NAME], "Fox")
        self.assertEqual(customer[api_c.MATCH_CONFIDENCE], 0.97)

    def test_get_customer_overview(self):
        """Test get customers overview."""

        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/insights",
            json=t_c.CUSTOMER_INSIGHT_RESPONSE,
        )
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/insights/count-by-state",
            json=t_c.CUSTOMERS_INSIGHTS_BY_STATES_RESPONSE,
        )
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_CONNECTION_SERVICE}/"
            f"{api_c.CDM_IDENTITY_ENDPOINT}/{api_c.INSIGHTS}",
            json=t_c.IDENTITY_INSIGHT_RESPONSE,
        )
        self.request_mocker.start()

        response = self.app.get(
            f"{self.customers}/{api_c.OVERVIEW}",
            headers=t_c.STANDARD_HEADERS,
        )
        self.assertEqual(HTTPStatus.OK, response.status_code)

        expected_response = t_c.CUSTOMER_INSIGHT_RESPONSE[api_c.BODY].copy()

        expected_response[api_c.IDR_INSIGHTS] = IDROverviewSchema().dump(
            clean_cdm_fields(t_c.IDENTITY_INSIGHT_RESPONSE[api_c.BODY].copy())
        )
        expected_response[api_c.GEOGRAPHICAL] = get_geographic_customers_data(
            t_c.CUSTOMERS_INSIGHTS_BY_STATES_RESPONSE[api_c.BODY]
        )
        expected_response.update(
            {
                api_c.GENDER_WOMEN_COUNT: expected_response[
                    api_c.GENDER_WOMEN
                ],
                api_c.GENDER_MEN_COUNT: expected_response[api_c.GENDER_MEN],
                api_c.GENDER_OTHER_COUNT: expected_response[
                    api_c.GENDER_OTHER
                ],
                api_c.GENDER_WOMEN: round(
                    expected_response[api_c.GENDER_WOMEN]
                    / (
                        expected_response[api_c.GENDER_WOMEN]
                        + expected_response[api_c.GENDER_MEN]
                        + expected_response[api_c.GENDER_OTHER]
                    ),
                    4,
                ),
                api_c.GENDER_MEN: round(
                    expected_response[api_c.GENDER_MEN]
                    / (
                        expected_response[api_c.GENDER_WOMEN]
                        + expected_response[api_c.GENDER_MEN]
                        + expected_response[api_c.GENDER_OTHER]
                    ),
                    4,
                ),
                api_c.GENDER_OTHER: round(
                    expected_response[api_c.GENDER_OTHER]
                    / (
                        expected_response[api_c.GENDER_WOMEN]
                        + expected_response[api_c.GENDER_MEN]
                        + expected_response[api_c.GENDER_OTHER]
                    ),
                    4,
                ),
            }
        )

        data = response.json
        for key, value in data.items():
            if isinstance(value, list):
                self.assertEqual(
                    len(value), len(expected_response[api_c.GEOGRAPHICAL])
                )
                continue
            if value:
                self.assertEqual(value, expected_response[key])

    def test_get_idr_overview(self):
        """Test get customers idr overview."""

        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_CONNECTION_SERVICE}/"
            f"{api_c.CDM_IDENTITY_ENDPOINT}/{api_c.INSIGHTS}",
            json=t_c.IDENTITY_INSIGHT_RESPONSE,
        )
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_CONNECTION_SERVICE}/identity/id-count-by"
            f"-day",
            json=t_c.IDR_MATCHING_TRENDS_BY_DAY_DATA,
        )
        self.request_mocker.start()

        response = self.app.get(
            f"{self.idr}/{api_c.OVERVIEW}",
            headers=t_c.STANDARD_HEADERS,
        )
        self.assertEqual(HTTPStatus.OK, response.status_code)
        data = response.json
        self.assertTrue(data[api_c.OVERVIEW])
        self.assertTrue(data[api_c.DATE_RANGE])
        expected_response = IDROverviewSchema().dump(
            clean_cdm_fields(t_c.IDENTITY_INSIGHT_RESPONSE[api_c.BODY].copy())
        )
        for key, value in data[api_c.OVERVIEW].items():
            self.assertEqual(expected_response[key], value)

    def test_get_customer_by_id(self):
        """Test get customer by ID."""

        self.request_mocker.stop()
        self.request_mocker.get(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/{t_c.SAMPLE_CUSTOMER_ID}",
            json=t_c.CUSTOMER_PROFILE_RESPONSE,
        )
        self.request_mocker.start()

        response = self.app.get(
            f"{self.customers}/{t_c.SAMPLE_CUSTOMER_ID}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)

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
        self.assertTrue(
            data[api_c.IDENTITY_RESOLUTION][api_c.NAME][api_c.CO_OCCURRENCES]
        )
        self.assertTrue(data[api_c.CONTACT_PREFERENCES])
        self.assertEqual(
            CustomerProfileContactPreferencesSchema().dump(
                t_c.CUSTOMER_PROFILE_RESPONSE[api_c.BODY]
            ),
            data[api_c.CONTACT_PREFERENCES],
        )

    def test_get_customer_by_id_pii_access(self):
        """Test get customer by ID with PII Access"""

        self.request_mocker.stop()
        self.request_mocker.get(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/{t_c.SAMPLE_CUSTOMER_ID}",
            json=t_c.CUSTOMER_PROFILE_RESPONSE,
        )
        self.request_mocker.start()

        response = self.app.get(
            f"{self.customers}/{t_c.SAMPLE_CUSTOMER_ID}?{api_c.REDACT_FIELD}=False",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        data = response.json
        self.assertTrue(data[api_c.OVERVIEW])
        self.assertEqual(
            data[api_c.OVERVIEW][api_c.FIRST_NAME],
            t_c.CUSTOMER_PROFILE_RESPONSE[api_c.BODY][api_c.FIRST_NAME],
        )
        self.assertEqual(
            data[api_c.OVERVIEW][api_c.LAST_NAME],
            t_c.CUSTOMER_PROFILE_RESPONSE[api_c.BODY][api_c.LAST_NAME],
        )
        self.assertTrue(data[api_c.INSIGHTS])
        self.assertEqual(
            data[api_c.INSIGHTS][api_c.EMAIL],
            t_c.CUSTOMER_PROFILE_RESPONSE[api_c.BODY][api_c.EMAIL],
        )
        self.assertEqual(
            data[api_c.INSIGHTS][api_c.GENDER],
            t_c.CUSTOMER_PROFILE_RESPONSE[api_c.BODY][api_c.GENDER],
        )
        self.assertEqual(
            data[api_c.INSIGHTS][api_c.CITY],
            t_c.CUSTOMER_PROFILE_RESPONSE[api_c.BODY][api_c.CITY],
        )
        self.assertEqual(
            data[api_c.INSIGHTS][api_c.ADDRESS],
            t_c.CUSTOMER_PROFILE_RESPONSE[api_c.BODY][api_c.ADDRESS],
        )
        self.assertEqual(
            data[api_c.INSIGHTS][api_c.AGE],
            t_c.CUSTOMER_PROFILE_RESPONSE[api_c.BODY][api_c.AGE],
        )

    def test_post_customer_overview_by_attributes(self) -> None:
        """Test get customer over by attributes."""

        filter_attributes = {
            "filters": [
                {
                    "section_aggregator": "ALL",
                    "section_filters": [
                        {"field": "max_age", "type": "equals", "value": 87},
                        {"field": "min_age", "type": "equals", "value": 25},
                    ],
                }
            ]
        }

        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/insights",
            json=t_c.CUSTOMER_INSIGHT_RESPONSE,
        )
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/insights/count-by-state",
            json=t_c.CUSTOMERS_INSIGHTS_BY_STATES_RESPONSE,
        )
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_CONNECTION_SERVICE}/"
            f"{api_c.CDM_IDENTITY_ENDPOINT}/{api_c.INSIGHTS}",
            json=t_c.IDENTITY_INSIGHT_RESPONSE,
        )
        self.request_mocker.get(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/event-types",
            json=t_c.EVENT_TYPES_RESPONSE,
        )
        self.request_mocker.start()

        response = self.app.post(
            f"{self.customers}/{api_c.OVERVIEW}",
            data=json.dumps(filter_attributes),
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        data = response.json
        self.assertGreaterEqual(data[api_c.GENDER_MEN], 0)
        self.assertGreaterEqual(data[api_c.GENDER_WOMEN], 0)
        self.assertGreaterEqual(data[api_c.GENDER_OTHER], 0)
        self.assertGreaterEqual(data[api_c.GENDER_MEN_COUNT], 0)
        self.assertGreaterEqual(data[api_c.GENDER_WOMEN_COUNT], 0)
        self.assertGreaterEqual(data[api_c.GENDER_OTHER_COUNT], 0)

    def test_post_customer_overview_invalid_filters(self) -> None:
        """Test get customer overview with invalid filters."""

        filter_attributes = {
            "filters": [
                {
                    "section_aggregator": "ALL",
                    "section_filters": [
                        {"value": ""},
                    ],
                }
            ]
        }

        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/insights",
            json=t_c.CUSTOMER_INSIGHT_RESPONSE,
        )
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/insights/count-by-state",
            json=t_c.CUSTOMERS_INSIGHTS_BY_STATES_RESPONSE,
        )
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_CONNECTION_SERVICE}/"
            f"{api_c.CDM_IDENTITY_ENDPOINT}/{api_c.INSIGHTS}",
            json=t_c.IDENTITY_INSIGHT_RESPONSE,
        )
        self.request_mocker.start()

        response = self.app.post(
            f"{self.customers}/{api_c.OVERVIEW}",
            data=json.dumps(filter_attributes),
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertTrue(CustomerOverviewSchema().validate(response.json))
        self.assertEqual(0, response.json.get(api_c.TOTAL_CUSTOMERS))

    def test_get_idr_data_feeds(self):
        """Test get IDR Datafeeds."""

        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_CONNECTION_SERVICE}"
            f"/{api_c.CDM_IDENTITY_ENDPOINT}/{api_c.DATAFEEDS}",
            json=t_c.IDR_DATAFEEDS_RESPONSE,
        )
        self.request_mocker.start()

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.IDR_ENDPOINT}/{api_c.DATAFEEDS}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(
            {}, DataFeedSchema().validate(response.json, many=True)
        )
        for datafeed in response.json:
            self.assertIn("num_records_processed", datafeed)
            self.assertIn("new_ids_generated", datafeed)

    def test_get_idr_data_feed_details(self) -> None:
        """Test get idr datafeed details."""

        datafeed_id = 1
        self.request_mocker.stop()
        self.request_mocker.get(
            f"{t_c.TEST_CONFIG.CDP_CONNECTION_SERVICE}"
            f"/{api_c.CDM_IDENTITY_ENDPOINT}/{api_c.DATAFEEDS}/"
            f"{datafeed_id}",
            json=t_c.IDR_DATAFEED_DETAILS_RESPONSE,
        )

        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_CONNECTION_SERVICE}"
            f"/{api_c.CDM_IDENTITY_ENDPOINT}/{api_c.DATAFEEDS}",
            json=t_c.IDR_DATAFEEDS_RESPONSE,
        )
        self.request_mocker.start()

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.IDR_ENDPOINT}/{api_c.DATAFEEDS}/"
            f"{datafeed_id}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertFalse(DataFeedDetailsSchema().validate(response.json))

    def test_get_customers_geo(self):
        """Test get customers geo insights."""

        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/insights/count-by-state",
            json=t_c.CUSTOMERS_INSIGHTS_BY_STATES_RESPONSE,
        )
        self.request_mocker.start()

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}/{api_c.CUSTOMERS_INSIGHTS}/{api_c.GEOGRAPHICAL}",
            headers=t_c.STANDARD_HEADERS,
        )
        self.assertEqual(HTTPStatus.OK, response.status_code)

        self.assertTrue(
            t_c.validate_schema(CustomerGeoVisualSchema(), response.json, True)
        )

    def test_get_customers_demographics(self):
        """Test get customers demographic insights."""

        start_date = "2021-04-01"
        end_date = "2021-08-01"

        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/insights",
            json=t_c.CUSTOMER_INSIGHT_RESPONSE,
        )
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/insights/city-ltvs",
            json=t_c.MOCKED_CITY_LTVS_RESPONSE,
        )
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/insights/spending-by-month",
            json=t_c.MOCKED_GENDER_SPENDING,
        )
        self.request_mocker.start()

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}/{api_c.CUSTOMERS_INSIGHTS}/"
            f"{api_c.DEMOGRAPHIC}",
            query_string={
                api_c.START_DATE: start_date,
                api_c.END_DATE: end_date,
            },
            headers=t_c.STANDARD_HEADERS,
        )
        self.assertEqual(HTTPStatus.OK, response.status_code)

        self.assertTrue(
            t_c.validate_schema(
                CustomerDemographicInsightsSchema(), response.json
            )
        )
        self.assertTrue(
            t_c.validate_schema(
                CustomerSpendingInsightsSchema(), response.json[api_c.SPEND]
            )
        )
        self.assertTrue(
            t_c.validate_schema(
                CustomerGenderInsightsSchema(), response.json[api_c.GENDER]
            )
        )
        self.assertTrue(
            t_c.validate_schema(
                CustomerIncomeInsightsSchema(),
                response.json[api_c.INCOME],
                True,
            )
        )

    def test_get_idr_trends(self):
        """Test get matching trends."""

        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_CONNECTION_SERVICE}/identity/id-count-by"
            f"-day",
            json=t_c.IDR_MATCHING_TRENDS_BY_DAY_DATA,
        )
        self.request_mocker.start()

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.IDR_ENDPOINT}/{api_c.MATCHING_TRENDS}",
            headers=t_c.STANDARD_HEADERS,
        )
        self.assertEqual(HTTPStatus.OK, response.status_code)

        self.assertTrue(
            t_c.validate_schema(MatchingTrendsSchema(), response.json, True)
        )

    @given(interval=st.sampled_from(["", api_c.DAY, api_c.WEEK, api_c.MONTH]))
    def test_customer_events(self, interval: str):
        """Test fetching customer events for default interval for a hux-id.

        Args:
            interval (str): Interval by which the data is to be fetched
        """

        hux_id = "HUX123456789012345"

        filter_attributes = {
            "start_date": "2021-01-01",
            "end_date": "2021-01-02",
        }
        interval = interval if interval else api_c.DAY

        expected_response = {
            api_c.DAY: t_c.CUSTOMER_EVENT_BY_DAY_RESPONSE,
            api_c.WEEK: t_c.CUSTOMER_EVENT_BY_WEEK_RESPONSE,
            api_c.MONTH: t_c.CUSTOMER_EVENT_BY_MONTH_RESPONSE,
        }

        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/{hux_id}/events",
            json=expected_response[interval],
        )
        self.request_mocker.start()

        response = self.app.post(
            f"{t_c.BASE_ENDPOINT}{api_c.CUSTOMERS_ENDPOINT}/{hux_id}/events",
            query_string={api_c.INTERVAL: interval},
            data=json.dumps(filter_attributes),
            headers=t_c.STANDARD_HEADERS,
        )
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertTrue(
            t_c.validate_schema(CustomerEventsSchema(), response.json, True)
        )

    def test_customer_events_default_interval_empty_body(self):
        """Test fetching customer events for default interval for a hux-id
        with empty body."""

        hux_id = "HUX123456789012345"

        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/{hux_id}/events",
            json=t_c.CUSTOMER_EVENT_BY_DAY_RESPONSE,
        )
        self.request_mocker.start()

        response = self.app.post(
            f"{t_c.BASE_ENDPOINT}{api_c.CUSTOMERS_ENDPOINT}/{hux_id}/events",
            data=json.dumps({}),
            headers=t_c.STANDARD_HEADERS,
        )
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertTrue(
            t_c.validate_schema(CustomerEventsSchema(), response.json, True)
        )

    def test_total_customer_insights_success(self) -> None:
        """Test get total customer insights success response."""

        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/insights/count-by-day",
            json=t_c.CUSTOMER_INSIGHTS_COUNT_BY_DAY_RESPONSE,
        )
        self.request_mocker.start()

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}/{api_c.CUSTOMERS_INSIGHTS}/{api_c.TOTAL}",
            headers=t_c.STANDARD_HEADERS,
        )
        self.assertEqual(HTTPStatus.OK, response.status_code)

        self.assertTrue(
            t_c.validate_schema(
                TotalCustomersInsightsSchema(), response.json, True
            )
        )

    def test_customer_revenue_insights_success(self) -> None:
        """Test get customer revenue insights success response."""

        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/insights"
            f"/spending-by-day",
            json=t_c.MOCKED_GENDER_SPENDING_BY_DAY,
        )
        self.request_mocker.start()

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}/{api_c.CUSTOMERS_INSIGHTS}/{api_c.REVENUE}",
            headers=t_c.STANDARD_HEADERS,
        )
        self.assertEqual(HTTPStatus.OK, response.status_code)

        self.assertTrue(
            t_c.validate_schema(
                CustomerRevenueInsightsSchema(), response.json, True
            )
        )

    def test_customers_insights_cities_success(self) -> None:
        """Test get customers insights by cities."""

        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.CUSTOMER_PROFILE_API}/customer-profiles/insights/city-ltvs",
            json=t_c.CUSTOMERS_INSIGHTS_BY_CITY_RESPONSE,
        )

        self.request_mocker.start()

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}/{api_c.CUSTOMERS_INSIGHTS}/{api_c.CITIES}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)

        self.assertTrue(
            t_c.validate_schema(
                CustomersInsightsCitiesSchema(),
                response.json,
                True,
            )
        )

    def test_customers_insights_states_success(self) -> None:
        """Test get customers insights by states."""

        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.CUSTOMER_PROFILE_API}/customer-profiles/insights/count-by-state",
            json=t_c.CUSTOMERS_INSIGHTS_BY_STATES_RESPONSE,
        )

        self.request_mocker.start()

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}/{api_c.CUSTOMERS_INSIGHTS}/{api_c.STATES}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)

        self.assertTrue(
            t_c.validate_schema(
                CustomersInsightsStatesSchema(),
                response.json,
                True,
            )
        )

    def test_customers_insights_countries_success(self) -> None:
        """Test get customers insights by countries."""

        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.CUSTOMER_PROFILE_API}/customer-profiles/countries",
            json=t_c.CUSTOMERS_INSIGHTS_BY_COUNTRIES_RESPONSE,
        )

        self.request_mocker.start()

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}/{api_c.CUSTOMERS_INSIGHTS}/{api_c.COUNTRIES}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)

        self.assertTrue(
            t_c.validate_schema(
                CustomersInsightsCountriesSchema(),
                response.json,
                True,
            )
        )

    def test_get_idr_overview_empty_body(self):
        """Test get customers idr overview empty data."""

        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_CONNECTION_SERVICE}/"
            f"{api_c.CDM_IDENTITY_ENDPOINT}/{api_c.INSIGHTS}",
            json=t_c.IDENTITY_INSIGHT_EMPTY_RESPONSE,
        )
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_CONNECTION_SERVICE}/identity/id-count-by"
            f"-day",
            json=t_c.IDR_MATCHING_TRENDS_BY_DAY_EMPTY_DATA,
        )
        self.request_mocker.start()

        response = self.app.get(
            f"{self.idr}/{api_c.OVERVIEW}",
            headers=t_c.STANDARD_HEADERS,
        )
        self.assertEqual(HTTPStatus.OK, response.status_code)
        data = response.json
        self.assertTrue(data[api_c.OVERVIEW])
        self.assertTrue(data[api_c.DATE_RANGE])

        expected_response = IDROverviewSchema().dump(
            clean_cdm_fields(
                t_c.IDENTITY_INSIGHT_EMPTY_RESPONSE[api_c.BODY].copy()
            )
        )
        for key, value in data[api_c.OVERVIEW].items():
            self.assertEqual(expected_response[key], value)

    def test_get_idr_trends_empty_body(self):
        """Test get matching trends with empty data."""

        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_CONNECTION_SERVICE}/identity/id-count-by"
            f"-day",
            json=t_c.IDR_MATCHING_TRENDS_BY_DAY_EMPTY_DATA,
        )
        self.request_mocker.start()

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.IDR_ENDPOINT}/{api_c.MATCHING_TRENDS}",
            headers=t_c.STANDARD_HEADERS,
        )
        self.assertEqual(HTTPStatus.OK, response.status_code)

        self.assertFalse(
            MatchingTrendsSchema().validate(response.json, many=True)
        )

    def test_get_idr_data_feeds_empty_data(self):
        """Test get IDR Datafeeds with empty body."""

        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_CONNECTION_SERVICE}"
            f"/{api_c.CDM_IDENTITY_ENDPOINT}/{api_c.DATAFEEDS}",
            json=t_c.IDR_DATAFEEDS_EMPTY_RESPONSE,
        )
        self.request_mocker.start()

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.IDR_ENDPOINT}/{api_c.DATAFEEDS}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertFalse(response.json)
        self.assertEqual(0, len(response.json))

    def test_get_idr_data_feed_details_empty_data(self) -> None:
        """Test get idr datafeed details for empty data."""

        datafeed_id = 1
        self.request_mocker.stop()
        self.request_mocker.get(
            f"{t_c.TEST_CONFIG.CDP_CONNECTION_SERVICE}"
            f"/{api_c.CDM_IDENTITY_ENDPOINT}/{api_c.DATAFEEDS}/"
            f"{datafeed_id}",
            json=t_c.IDR_DATAFEED_DETAILS_EMPTY_RESPONSE,
        )

        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_CONNECTION_SERVICE}"
            f"/{api_c.CDM_IDENTITY_ENDPOINT}/{api_c.DATAFEEDS}",
            json=t_c.IDR_DATAFEEDS_EMPTY_RESPONSE,
        )
        self.request_mocker.start()

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.IDR_ENDPOINT}/{api_c.DATAFEEDS}/"
            f"{datafeed_id}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertFalse(DataFeedDetailsSchema().validate(response.json))

    def test_get_customer_overview_dependency_failure(self) -> None:
        """Test get customer overview 424 dependency failure."""

        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/insights",
            json={},
        )
        self.request_mocker.start()

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.CUSTOMERS_ENDPOINT}/{api_c.OVERVIEW}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.FAILED_DEPENDENCY, response.status_code)

    def test_get_customers_dependency_failure(self) -> None:
        """Test get customers 424 dependency failure."""

        self.request_mocker.stop()
        self.request_mocker.get(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles",
            json={},
        )
        self.request_mocker.start()

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.CUSTOMERS_ENDPOINT}?{api_c.QUERY_PARAMETER_BATCH_SIZE}="
            f"{api_c.CUSTOMERS_DEFAULT_BATCH_SIZE}&"
            f"{api_c.QUERY_PARAMETER_BATCH_NUMBER}="
            f"{api_c.DEFAULT_BATCH_NUMBER}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.FAILED_DEPENDENCY, response.status_code)

    def test_get_customer_by_id_dependency_failure(self) -> None:
        """Test get customer by ID 424 dependency failure."""

        hux_id = "HUX123456789012345"

        self.request_mocker.stop()
        self.request_mocker.get(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/{hux_id}",
            json={},
        )
        self.request_mocker.start()

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.CUSTOMERS_ENDPOINT}/{hux_id}",
            headers=t_c.AUTH_HEADER,
        )

        self.assertEqual(HTTPStatus.FAILED_DEPENDENCY, response.status_code)

    def test_get_idr_overview_dependency_failure(self) -> None:
        """Test get idr overview 424 dependency failure."""

        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_CONNECTION_SERVICE}/"
            f"{api_c.CDM_IDENTITY_ENDPOINT}/{api_c.INSIGHTS}",
            json={},
        )
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_CONNECTION_SERVICE}/"
            f"{api_c.CDM_IDENTITY_ENDPOINT}/id-count-by-day",
            json={},
        )
        self.request_mocker.start()

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.IDR_ENDPOINT}/{api_c.OVERVIEW}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.FAILED_DEPENDENCY, response.status_code)

    @given(interval=st.sampled_from(["", api_c.DAY, api_c.WEEK, api_c.MONTH]))
    def test_get_customer_events_dependency_failure(
        self, interval: str
    ) -> None:
        """Test get customer events 424 dependency failure.

        Args:
            interval (str): Interval to aggregate events data on
        """

        hux_id = "HUX123456789012345"

        filter_attributes = {
            "start_date": "2021-01-01",
            "end_date": "2021-01-02",
        }

        interval = interval if interval else api_c.DAY

        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/{hux_id}/events",
            json={},
        )
        self.request_mocker.start()

        response = self.app.post(
            f"{t_c.BASE_ENDPOINT}{api_c.CUSTOMERS_ENDPOINT}/{hux_id}/events",
            query_string={api_c.INTERVAL: interval},
            data=json.dumps(filter_attributes),
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.FAILED_DEPENDENCY, response.status_code)

    def test_get_customers_geo_dependency_failure(self) -> None:
        """Test get customer geographic 424 dependency failure."""

        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/insights/count-by-state",
            json={},
        )
        self.request_mocker.start()

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}/{api_c.CUSTOMERS_INSIGHTS}/{api_c.GEOGRAPHICAL}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.FAILED_DEPENDENCY, response.status_code)

    def test_customers_insights_countries_dependency_failure(self) -> None:
        """Test get customer insights countries 424 dependency failure."""

        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.CUSTOMER_PROFILE_API}/customer-profiles/countries",
            json={},
        )

        self.request_mocker.start()

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}/{api_c.CUSTOMERS_INSIGHTS}/{api_c.COUNTRIES}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.FAILED_DEPENDENCY, response.status_code)

    def test_total_customer_insights_dependency_failure(self) -> None:
        """Test get total customer insights 424 dependency failure."""

        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/insights/count-by-day",
            json={},
        )
        self.request_mocker.start()

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}/{api_c.CUSTOMERS_INSIGHTS}/{api_c.TOTAL}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.FAILED_DEPENDENCY, response.status_code)

    def test_customers_insights_cities_dependency_failure(self) -> None:
        """Test get customers insights cities 424 dependency failure."""

        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.CUSTOMER_PROFILE_API}/customer-profiles/insights/city-ltvs",
            json={},
        )

        self.request_mocker.start()

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}/{api_c.CUSTOMERS_INSIGHTS}/{api_c.CITIES}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.FAILED_DEPENDENCY, response.status_code)

    def test_get_customers_demographics_dependency_failure(self) -> None:
        """Test get customer demographics 424 dependency failure."""

        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/insights",
            json=t_c.CUSTOMER_INSIGHT_RESPONSE,
        )
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/insights/city-ltvs",
            json=t_c.MOCKED_CITY_LTVS_RESPONSE,
        )
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/insights/spending-by-month",
            json={},
        )
        self.request_mocker.start()

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}/{api_c.CUSTOMERS_INSIGHTS}/"
            f"{api_c.DEMOGRAPHIC}",
            query_string={
                api_c.START_DATE: "2021-04-01",
                api_c.END_DATE: "2021-08-01",
            },
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.FAILED_DEPENDENCY, response.status_code)

    def test_customer_revenue_insights_dependency_failure(self) -> None:
        """Test get customer revenue insights dependency failure."""

        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/insights"
            f"/spending-by-day",
            json={},
        )
        self.request_mocker.start()

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}/{api_c.CUSTOMERS_INSIGHTS}/{api_c.REVENUE}",
            headers=t_c.STANDARD_HEADERS,
        )
        self.assertEqual(HTTPStatus.FAILED_DEPENDENCY, response.status_code)

    # TODO Implement test once logic for HUXID is set again

    # @given(hux_id=st.text(alphabet=string.ascii_letters))
    # def test_get_customer_profile_invalid_hux_id(self, hux_id: str):
    #     """Test retrieving customer profile with an invalid hux ID.
    #
    #     Args:
    #         hux_id (str): HUX ID.
    #     """
    #
    #     if len(hux_id) == 0:
    #         return
    #
    #     response = self.app.get(
    #         f"{t_c.BASE_ENDPOINT}{api_c.CUSTOMERS_ENDPOINT}/{hux_id}",
    #         headers=t_c.STANDARD_HEADERS,
    #     )
    #
    #     self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)

    # @given(hux_id=st.text(alphabet=string.ascii_letters))
    # def test_get_events_for_a_customer_invalid_hux_id(self, hux_id: str):
    #     """Test retrieving customer events with an invalid hux ID.
    #
    #     Args:
    #         hux_id (str): HUX ID.
    #     """
    #
    #     if len(hux_id) == 0:
    #         return
    #
    #     response = self.app.post(
    #         f"{t_c.BASE_ENDPOINT}{api_c.CUSTOMERS_ENDPOINT}/{hux_id}/events",
    #         headers=t_c.STANDARD_HEADERS,
    #     )
    #
    #     self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)

    @given(batch_size=st.text(alphabet=string.ascii_letters))
    def test_get_customer_overview_invalid_batch_size(self, batch_size: str):
        """Test get customer list and provide an invalid batch size.

        Args:
            batch_size (str): HUX ID.
        """

        if len(batch_size) == 0:
            return

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.CUSTOMERS_ENDPOINT}?batch_size={batch_size}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)

    @given(batch_number=st.text(alphabet=string.ascii_letters))
    def test_get_customer_overview_invalid_batch_number(
        self, batch_number: str
    ):
        """Test get customer list and provide an invalid batch number.

        Args:
            batch_number (str): batch number of what should be served to the user
        """

        if len(batch_number) == 0:
            return

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.CUSTOMERS_ENDPOINT}?batch_number={batch_number}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)

    @given(batch_size=st.text(alphabet=string.ascii_letters))
    def test_get_customer_insights_by_city_invalid_batch_size(
        self, batch_size: str
    ):
        """Test get customer insights by city and provide an invalid batch size.

        Args:
            batch_size (str): Size of the batch that should be returned to the user.
        """

        if len(batch_size) == 0:
            return

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}/{api_c.CUSTOMERS_INSIGHTS}/{api_c.CITIES}",
            query_string={"batch_size": batch_size},
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)

    @given(batch_number=st.text(alphabet=string.ascii_letters))
    def test_get_customer_insights_by_city_invalid_batch_number(
        self, batch_number: str
    ):
        """Test get customer insights by city and provide an invalid batch size.

        Args:
            batch_number (str): batch number of what should be served to the user
        """

        if len(batch_number) == 0:
            return

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}/{api_c.CUSTOMERS_INSIGHTS}/{api_c.CITIES}",
            query_string={"batch_number": batch_number},
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)

    @given(datafeed_id=st.text(alphabet=string.ascii_letters))
    def test_get_datafeed_invalid_datafeed_id(self, datafeed_id: str):
        """Test get datafeed using an invalid datafeed ID.

        Args:
            datafeed_id (str): datafeed ID.
        """

        if len(datafeed_id) == 0:
            return

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.IDR_ENDPOINT}/{api_c.DATAFEEDS}/{datafeed_id}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
