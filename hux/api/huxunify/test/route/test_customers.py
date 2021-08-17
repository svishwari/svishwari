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
    DataFeedPinning,
    DataFeedDetailsSchema,
    DataFeedStitched,
    DataFeedSchema,
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
            f"{api_c.CUSTOMERS_DEFAULT_BATCH_NUMBER}",
            headers=t_c.STANDARD_HEADERS,
        )
        self.assertEqual(HTTPStatus.OK, response.status_code)
        data = response.json

        response = self.test_client.get(
            f"{self.customers}?{api_c.QUERY_PARAMETER_BATCH_SIZE}=abc&"
            f"{api_c.QUERY_PARAMETER_BATCH_NUMBER}=def",
            headers=t_c.STANDARD_HEADERS,
        )
        self.assertEqual(
            HTTPStatus.INTERNAL_SERVER_ERROR, response.status_code
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
        self.assertTrue(data[api_c.TOTAL_RECORDS])
        self.assertTrue(data[api_c.MATCH_RATE])

    def test_get_idr_overview(self):
        """
        Test get customers idr overview

        Args:
            request_mocker (Mocker): Request mocker object.

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
        self.assertTrue(data[api_c.TOTAL_RECORDS])
        self.assertTrue(data[api_c.MATCH_RATE])

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
        self.assertTrue(data[api_c.FIRST_NAME])
        self.assertTrue(data[api_c.LAST_NAME])
        self.assertEqual(data[api_c.EMAIL], api_c.REDACTED)
        self.assertEqual(data[api_c.GENDER], api_c.REDACTED)
        self.assertEqual(data[api_c.CITY], api_c.REDACTED)
        self.assertEqual(data[api_c.ADDRESS], api_c.REDACTED)
        self.assertEqual(data[api_c.AGE], api_c.REDACTED)

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
        self.assertTrue(data[api_c.TOTAL_RECORDS])
        self.assertTrue(data[api_c.MATCH_RATE])

    def test_get_idr_data_feeds(self):
        """
        Test get IDR Datafeeds
        """

        # TODO: Update after integration of CDM APIs
        response = self.test_client.get(
            f"{t_c.BASE_ENDPOINT}{api_c.IDR_ENDPOINT}/{api_c.DATA_FEEDS}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(
            {}, DataFeedSchema().validate(response.json, many=True)
        )

    @given(datafeed=st.text(alphabet=string.ascii_letters))
    def test_get_idr_datafeed_report(self, datafeed: str):
        """
        Test get idr datafeed report

        Args:
            request_mocker (Mocker): Request mocker object.

        Returns:

        """
        if not datafeed:
            return

        response = self.test_client.get(
            f"{t_c.BASE_ENDPOINT}{api_c.IDR_ENDPOINT}/{api_c.DATA_FEEDS}/{datafeed}",
            headers=t_c.STANDARD_HEADERS,
        )
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertTrue(
            t_c.validate_schema(DataFeedDetailsSchema(), response.json)
        )
        self.assertTrue(
            t_c.validate_schema(DataFeedPinning(), response.json["pinning"])
        )
        self.assertTrue(
            t_c.validate_schema(DataFeedStitched(), response.json["stitched"])
        )

    def test_get_customers_geo(self):
        """
        Test get customers geo insights

        Args:

        Returns:

        """

        response = self.test_client.get(
            f"{t_c.BASE_ENDPOINT}/{api_c.CUSTOMERS_INSIGHTS}/{api_c.GEOGRAPHICAL}",
            headers=t_c.STANDARD_HEADERS,
        )
        self.assertEqual(HTTPStatus.OK, response.status_code)

        self.assertTrue(
            t_c.validate_schema(CustomerGeoVisualSchema(), response.json, True)
        )

    def test_post_customers_demo(self):
        """
        Test post customers demographical insights

        Args:

        Returns:

        """
        filter_attributes = {
            "filters": {
                "start_date": "2020-11-30T00:00:00Z",
                "end_date": "2021-04-30T00:00:00Z",
            }
        }

        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/insights/city-ltvs",
            json=t_c.MOCKED_CITY_LTVS_RESPONSE,
        )
        self.request_mocker.start()

        response = self.test_client.post(
            f"{t_c.BASE_ENDPOINT}/{api_c.CUSTOMERS_INSIGHTS}/{api_c.DEMOGRAPHIC}",
            data=json.dumps(filter_attributes),
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
                CustomerSpendingInsightsSchema(), response.json["spend"]
            )
        )
        self.assertTrue(
            t_c.validate_schema(
                CustomerGenderInsightsSchema(), response.json["gender"]
            )
        )
        self.assertTrue(
            t_c.validate_schema(
                CustomerIncomeInsightsSchema(), response.json["income"], True
            )
        )

    def test_get_idr_trends_ytd(self):
        """
        Test get matching trends YTD

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
        response = self.test_client.post(
            f"{t_c.BASE_ENDPOINT}{api_c.CUSTOMERS_ENDPOINT}/{customer_id}/events",
            headers=t_c.STANDARD_HEADERS,
        )
        self.assertEqual(HTTPStatus.OK, response.status_code)

        self.assertTrue(
            t_c.validate_schema(CustomerEventsSchema(), response.json, True)
        )

    def test_total_customer_insights(self):
        """
        Test get total customer insights

        Args:

        Returns:

        """
        self.request_mocker.stop()
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
