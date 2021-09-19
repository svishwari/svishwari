"""
Purpose of this file is to house all the customers api tests
"""
import string
import json
from unittest import TestCase
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
    """
    Purpose of this class is to test Customers overview
    """

    def setUp(self):  # pylint: disable=arguments-differ
        """
        Sets up Test Client

        Returns:
        """
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

        # setup the flask test client
        self.test_client = create_app().test_client()
        self.database.drop_database(db_c.DATA_MANAGEMENT_DATABASE)

    def test_get_customers(self):
        """
        Test get customers

        Args:

        Returns:

        """

        expected_response = {
            "code": 200,
            "body": [
                {
                    api_c.HUX_ID: "1531-2039-22",
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

        with self.assertRaises(TypeError):
            self.test_client.get(
                f"{self.customers}?{api_c.QUERY_PARAMETER_BATCH_SIZE}=abc&"
                f"{api_c.QUERY_PARAMETER_BATCH_NUMBER}=def",
                headers=t_c.STANDARD_HEADERS,
            )

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
        """
        Test get customers overview

        Args:

        Returns:

        """

        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/insights",
            json=t_c.CUSTOMER_INSIGHT_RESPONSE,
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
        """
        Test get customers idr overview

        Args:

        Returns:

        """

        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/insights",
            json=t_c.CUSTOMER_INSIGHT_RESPONSE,
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

    @given(customer_id=st.text(alphabet=string.ascii_letters))
    def test_get_customer_by_id(self, customer_id: str):
        """
        Test get customer by id

        Args:
            customer_id (str): customer id.

        Returns:

        """

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

    def test_post_customer_overview_by_attributes(self) -> None:
        """
        Test get customer over by attributes

        Args:

        Returns:
            None
        """

        filter_attributes = {
            "filters": {
                "section_aggregator": "ALL",
                "section_filters": [
                    {"field": "max_age", "type": "equals", "value": 87},
                    {"field": "min_age", "type": "equals", "value": 25},
                ],
            }
        }

        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/insights",
            json=t_c.CUSTOMER_INSIGHT_RESPONSE,
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

    def test_get_idr_data_feeds(self):
        """
        Test get IDR Datafeeds
        """

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
        """
        Test get idr datafeed details

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

        response = self.test_client.get(
            f"{t_c.BASE_ENDPOINT}{api_c.IDR_ENDPOINT}/{api_c.DATAFEEDS}/"
            f"{datafeed_id}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertFalse(DataFeedDetailsSchema().validate(response.json))

    def test_get_customers_geo(self):
        """
        Test get customers geo insights

        Args:

        Returns:

        """

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
        """
        Test get customers demographical insights

        Args:

        Returns:

        """

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
            data={api_c.START_DATE: start_date, api_c.END_DATE: end_date},
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
        """
        Test get matching trends.

        Args:

        Returns:

        """
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

    @given(customer_id=st.text(alphabet=string.ascii_letters))
    def test_customer_events(self, customer_id: str):
        """
        Test customer events for a hux-id

        Args:
            customer_id (str): HUX ID of a customer.
        Returns:

        """
        if not customer_id:
            return
        filter_attributes = {
            "start_date": "2021-01-01",
            "end_date": "2021-01-02",
        }

        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/{customer_id}/events",
            json=t_c.CUSTOMER_EVENT_RESPONSE,
        )
        self.request_mocker.start()

        response = self.test_client.post(
            f"{t_c.BASE_ENDPOINT}{api_c.CUSTOMERS_ENDPOINT}/{customer_id}/events",
            data=json.dumps(filter_attributes),
            headers=t_c.STANDARD_HEADERS,
        )
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(
            t_c.CUSTOMER_EVENT_RESPONSE.get("body"), response.json
        )

        self.assertTrue(
            t_c.validate_schema(CustomerEventsSchema(), response.json, True)
        )

    def test_total_customer_insights_success(self) -> None:
        """
        Test get total customer insights success response

        Args:

        Returns:
            None
        """

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

    def test_customers_insights_cities_success(self) -> None:
        """Test get customers insights by cities

        Args:

        Returns:
            None
        """

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
        """Test get customers insights by states

        Args:

        Returns:
            None
        """

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
        """Test get customers insights by countries

        Args:

        Returns:
            None
        """

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
        """Test get customer overview 424 dependency failure.

        Args:

        Returns:
            None
        """

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

        self.assertEqual(response.status_code, HTTPStatus.FAILED_DEPENDENCY)

    def test_get_customers_dependency_failure(self) -> None:
        """Test get customers 424 dependency failure.

        Args:

        Returns:
            None
        """

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

        self.assertEqual(response.status_code, HTTPStatus.FAILED_DEPENDENCY)

    def test_get_customer_by_id_dependency_failure(self) -> None:
        """Test get customer by ID 424 dependency failure.

        Args:

        Returns:
            None
        """

        self.request_mocker.stop()
        self.request_mocker.get(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/abc",
            json={},
        )
        self.request_mocker.start()

        response = self.test_client.get(
            f"{t_c.BASE_ENDPOINT}{api_c.CUSTOMERS_ENDPOINT}/abc",
            headers=t_c.AUTH_HEADER,
        )

        self.assertEqual(response.status_code, HTTPStatus.FAILED_DEPENDENCY)

    def test_get_idr_overview_dependency_failure(self) -> None:
        """Test get idr overview 424 dependency failure.

        Args:

        Returns:
            None
        """

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

        self.assertEqual(response.status_code, HTTPStatus.FAILED_DEPENDENCY)

    def test_get_customer_events_dependency_failure(self) -> None:
        """Test get customer events 424 dependency failure.

        Args:

        Returns:
            None
        """

        filter_attributes = {
            "start_date": "2021-01-01",
            "end_date": "2021-01-02",
        }

        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/abc/events",
            json={},
        )
        self.request_mocker.start()

        response = self.test_client.post(
            f"{t_c.BASE_ENDPOINT}{api_c.CUSTOMERS_ENDPOINT}/abc/events",
            data=json.dumps(filter_attributes),
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(response.status_code, HTTPStatus.FAILED_DEPENDENCY)

    def test_get_customers_geo_dependency_failure(self) -> None:
        """Test get customer geographic 424 dependency failure.

        Args:

        Returns:
            None
        """

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

        self.assertEqual(response.status_code, HTTPStatus.FAILED_DEPENDENCY)

    def test_customers_insights_countries_dependency_failure(self) -> None:
        """Test get customer insights countries 424 dependency failure.

        Args:

        Returns:
            None
        """

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

        self.assertEqual(response.status_code, HTTPStatus.FAILED_DEPENDENCY)

    def test_total_customer_insights_dependency_failure(self) -> None:
        """Test get total customer insights 424 dependency failure.

        Args:

        Returns:
            None
        """

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

        self.assertEqual(response.status_code, HTTPStatus.FAILED_DEPENDENCY)

    def test_customers_insights_cities_dependency_failure(self) -> None:
        """Test get customers insights cities 424 dependency failure.

        Args:

        Returns:
            None
        """

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

        self.assertEqual(response.status_code, HTTPStatus.FAILED_DEPENDENCY)

    def test_get_customers_demographics_dependency_failure(self) -> None:
        """Test get customer demographics 424 dependency failure.

        Args:

        Returns:
            None
        """

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
            data={
                api_c.START_DATE: "2021-04-01",
                api_c.END_DATE: "2021-08-01",
            },
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(response.status_code, HTTPStatus.FAILED_DEPENDENCY)
