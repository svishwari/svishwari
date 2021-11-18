"""Purpose of this file is to house all the customers api tests."""
import json
import string
from unittest import TestCase, mock
from http import HTTPStatus

import mongomock
import requests_mock
from hypothesis import given, strategies as st

from huxunifylib.database.client import DatabaseClient
import huxunifylib.database.constants as db_c
import huxunify.test.constants as t_c
from huxunify.api import constants as api_c
from huxunify.api.schema.customers import (
    DataFeedDetailsSchema,
    DataFeedSchema,
    CustomersInsightsCitiesSchema,
    CustomersInsightsStatesSchema,
    CustomersInsightsCountriesSchema,
    CustomerRevenueInsightsSchema,
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
from huxunify.app import create_app


# pylint: disable=R0904
class TestCustomersOverview(TestCase):
    """Purpose of this class is to test Customers overview."""

    def setUp(self):  # pylint: disable=arguments-differ
        """Sets up Test Client."""

        self.customers = f"{t_c.BASE_ENDPOINT}{api_c.CUSTOMERS_ENDPOINT}"
        self.idr = f"{t_c.BASE_ENDPOINT}{api_c.IDR_ENDPOINT}"

        # mock request for introspect call
        self.request_mocker = requests_mock.Mocker()
        self.request_mocker.post(t_c.INTROSPECT_CALL, json=t_c.VALID_RESPONSE)
        self.request_mocker.start()

        # init mongo patch initially
        mongo_patch = mongomock.patch(servers=(("localhost", 27017),))
        mongo_patch.start()

        # setup the mock DB client
        self.database = DatabaseClient(
            "localhost", 27017, None, None
        ).connect()

        mock.patch(
            "huxunify.api.route.customers.get_db_client",
            return_value=self.database,
        ).start()

        # setup the flask test client
        self.test_client = create_app().test_client()
        self.database.drop_database(db_c.DATA_MANAGEMENT_DATABASE)

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

        response = self.test_client.get(
            f"{self.customers}?{api_c.QUERY_PARAMETER_BATCH_SIZE}="
            f"{api_c.CUSTOMERS_DEFAULT_BATCH_SIZE}&"
            f"{api_c.QUERY_PARAMETER_BATCH_NUMBER}="
            f"{api_c.DEFAULT_BATCH_NUMBER}",
            headers=t_c.STANDARD_HEADERS,
        )
        self.assertEqual(HTTPStatus.OK, response.status_code)
        data = response.json

        response = self.test_client.get(
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
        self.request_mocker.start()

        response = self.test_client.get(
            f"{self.customers}/{api_c.OVERVIEW}",
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

    def test_get_idr_overview(self):
        """Test get customers idr overview."""

        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/insights",
            json=t_c.CUSTOMER_INSIGHT_RESPONSE,
        )
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_CONNECTION_SERVICE}/identity/id-count-by"
            f"-day",
            json=t_c.IDR_MATCHING_TRENDS_BY_DAY_DATA,
        )
        self.request_mocker.start()

        response = self.test_client.get(
            f"{self.idr}/{api_c.OVERVIEW}",
            headers=t_c.STANDARD_HEADERS,
        )
        self.assertEqual(HTTPStatus.OK, response.status_code)
        data = response.json
        self.assertTrue(data[api_c.OVERVIEW])
        self.assertTrue(data[api_c.DATE_RANGE])
        self.assertTrue(data[api_c.OVERVIEW][api_c.TOTAL_CUSTOMERS])
        self.assertTrue(data[api_c.OVERVIEW][api_c.TOTAL_KNOWN_IDS])

    def test_get_customer_by_id(self):
        """Test get customer by ID."""

        customer_id = "HUX123456789012345"

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
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/{customer_id}",
            json=expected_response,
        )
        self.request_mocker.start()

        response = self.test_client.get(
            f"{self.customers}/{customer_id}",
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
        self.request_mocker.start()

        response = self.test_client.post(
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
        self.request_mocker.start()

        response = self.test_client.post(
            f"{self.customers}/{api_c.OVERVIEW}",
            data=json.dumps(filter_attributes),
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)

    def test_get_idr_data_feeds(self):
        """Test get IDR Datafeeds."""

        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_CONNECTION_SERVICE}"
            f"/{api_c.CDM_IDENTITY_ENDPOINT}/{api_c.DATAFEEDS}",
            json=t_c.IDR_DATAFEEDS_RESPONSE,
        )
        self.request_mocker.start()

        response = self.test_client.get(
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
        self.request_mocker.start()

        response = self.test_client.get(
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

        response = self.test_client.get(
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

        response = self.test_client.get(
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

        response = self.test_client.get(
            f"{t_c.BASE_ENDPOINT}{api_c.IDR_ENDPOINT}/{api_c.MATCHING_TRENDS}",
            headers=t_c.STANDARD_HEADERS,
        )
        self.assertEqual(HTTPStatus.OK, response.status_code)

        self.assertTrue(
            t_c.validate_schema(MatchingTrendsSchema(), response.json, True)
        )

    def test_customer_events(self):
        """Test customer events for a hux-id."""

        hux_id = "HUX123456789012345"

        filter_attributes = {
            "start_date": "2021-01-01",
            "end_date": "2021-01-02",
        }

        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/{hux_id}/events",
            json=t_c.CUSTOMER_EVENT_RESPONSE,
        )
        self.request_mocker.start()

        response = self.test_client.post(
            f"{t_c.BASE_ENDPOINT}{api_c.CUSTOMERS_ENDPOINT}/{hux_id}/events",
            data=json.dumps(filter_attributes),
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

        response = self.test_client.get(
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
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/insights/spending-by-month",
            json=t_c.MOCKED_GENDER_SPENDING,
        )
        self.request_mocker.start()

        response = self.test_client.get(
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

        response = self.test_client.get(
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

        response = self.test_client.get(
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
            f"{t_c.CUSTOMER_PROFILE_API}/customer-profiles/insights/count-by-state",
            json=t_c.CUSTOMERS_INSIGHTS_BY_STATES_RESPONSE,
        )

        self.request_mocker.start()

        response = self.test_client.get(
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

    def test_get_customer_overview_dependency_failure(self) -> None:
        """Test get customer overview 424 dependency failure."""

        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/insights",
            json={},
        )
        self.request_mocker.start()

        response = self.test_client.get(
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

        response = self.test_client.get(
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

        response = self.test_client.get(
            f"{t_c.BASE_ENDPOINT}{api_c.CUSTOMERS_ENDPOINT}/{hux_id}",
            headers=t_c.AUTH_HEADER,
        )

        self.assertEqual(HTTPStatus.FAILED_DEPENDENCY, response.status_code)

    def test_get_idr_overview_dependency_failure(self) -> None:
        """Test get idr overview 424 dependency failure."""

        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/insights",
            json={},
        )
        self.request_mocker.start()

        response = self.test_client.get(
            f"{t_c.BASE_ENDPOINT}{api_c.IDR_ENDPOINT}/{api_c.OVERVIEW}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.FAILED_DEPENDENCY, response.status_code)

    def test_get_customer_events_dependency_failure(self) -> None:
        """Test get customer events 424 dependency failure."""

        hux_id = "HUX123456789012345"

        filter_attributes = {
            "start_date": "2021-01-01",
            "end_date": "2021-01-02",
        }

        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/{hux_id}/events",
            json={},
        )
        self.request_mocker.start()

        response = self.test_client.post(
            f"{t_c.BASE_ENDPOINT}{api_c.CUSTOMERS_ENDPOINT}/{hux_id}/events",
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

        response = self.test_client.get(
            f"{t_c.BASE_ENDPOINT}/{api_c.CUSTOMERS_INSIGHTS}/{api_c.GEOGRAPHICAL}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.FAILED_DEPENDENCY, response.status_code)

    def test_customers_insights_countries_dependency_failure(self) -> None:
        """Test get customer insights countries 424 dependency failure."""

        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.CUSTOMER_PROFILE_API}/customer-profiles/insights/count-by-state",
            json={},
        )

        self.request_mocker.start()

        response = self.test_client.get(
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

        response = self.test_client.get(
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

        response = self.test_client.get(
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

        response = self.test_client.get(
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
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/insights/spending-by-month",
            json={},
        )
        self.request_mocker.start()

        response = self.test_client.get(
            f"{t_c.BASE_ENDPOINT}/{api_c.CUSTOMERS_INSIGHTS}/{api_c.REVENUE}",
            headers=t_c.STANDARD_HEADERS,
        )
        self.assertEqual(HTTPStatus.FAILED_DEPENDENCY, response.status_code)

    @given(hux_id=st.text(alphabet=string.ascii_letters))
    def test_get_customer_profile_invalid_hux_id(self, hux_id: str):
        """Test retrieving customer profile with an invalid hux ID.

        Args:
            hux_id (str): HUX ID.
        """

        if len(hux_id) == 0:
            return

        response = self.test_client.get(
            f"{t_c.BASE_ENDPOINT}{api_c.CUSTOMERS_ENDPOINT}/{hux_id}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)

    @given(hux_id=st.text(alphabet=string.ascii_letters))
    def test_get_events_for_a_customer_invalid_hux_id(self, hux_id: str):
        """Test retrieving customer events with an invalid hux ID.

        Args:
            hux_id (str): HUX ID.
        """

        if len(hux_id) == 0:
            return

        response = self.test_client.post(
            f"{t_c.BASE_ENDPOINT}{api_c.CUSTOMERS_ENDPOINT}/{hux_id}/events",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)

    @given(batch_size=st.text(alphabet=string.ascii_letters))
    def test_get_customer_overview_invalid_batch_size(self, batch_size: str):
        """Test get customer list and provide an invalid batch size.

        Args:
            batch_size (str): HUX ID.
        """

        if len(batch_size) == 0:
            return

        response = self.test_client.get(
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

        response = self.test_client.get(
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

        response = self.test_client.get(
            f"{t_c.BASE_ENDPOINT}{api_c.CUSTOMERS_ENDPOINT}/{api_c.CITIES}?batch_size={batch_size}",
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

        response = self.test_client.get(
            f"{t_c.BASE_ENDPOINT}{api_c.CUSTOMERS_ENDPOINT}"
            f"/{api_c.CITIES}?batch_number={batch_number}",
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

        response = self.test_client.get(
            f"{t_c.BASE_ENDPOINT}{api_c.IDR_ENDPOINT}/{api_c.DATAFEEDS}/{datafeed_id}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
