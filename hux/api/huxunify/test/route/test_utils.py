"""Purpose of this file is to house all the route/utils tests."""
from datetime import datetime, timedelta
from http import HTTPStatus
from unittest import TestCase, mock

import mongomock
from bson import ObjectId
from huxunifylib.connectors.util.client import db_client_factory
from huxunifylib.database.client import DatabaseClient
from hypothesis import given, strategies as st

from huxunify.api.data_connectors.tecton import Tecton
from huxunify.api.exceptions.unified_exceptions import (
    InputParamsValidationError,
)
from huxunify.api.route.utils import (
    handle_api_exception,
    get_friendly_delivered_time,
    update_metrics,
    Validation,
    convert_unique_city_filter,
    get_db_client,
    check_mongo_connection,
    get_health_check,
)

from huxunify.api import constants as api_c


class TestRouteUtils(TestCase):
    """Test routes utils."""

    def test_handle_api_exception(self):
        """Test handle API exception."""
        exception = BaseException()
        response = handle_api_exception(
            exception, description="Exception Raised"
        )

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status)
        self.assertEqual(HTTPStatus.BAD_REQUEST.description, response.title)
        self.assertEqual("Exception Raised", response.detail)

    def test_get_db_client(self):
        """Test get db client."""
        # init mongo patch initially
        mongo_patch = mongomock.patch(servers=(("localhost", 27017),))
        mongo_patch.start()

        # setup the mock DB client
        database = DatabaseClient("localhost", 27017, None, None).connect()

        mock.patch.object(
            db_client_factory, "get_resource", return_value=database
        ).start()

        db_client = get_db_client()
        self.assertEqual(database.host, db_client.host)

    def test_check_mongo_connection_success(self):
        """Test check mongo connection success."""
        # init mongo patch initially
        mongo_patch = mongomock.patch(servers=(("localhost", 27017),))
        mongo_patch.start()

        # setup the mock DB client
        database = DatabaseClient("localhost", 27017, None, None).connect()

        mock.patch(
            "huxunify.api.route.utils.get_db_client", return_value=database
        ).start()

        status, message = check_mongo_connection()
        self.assertTrue(status)
        self.assertEqual("Mongo available.", message)

    def test_check_mongo_connection_failure(self):
        """Test check mongo connection failure."""
        # init mongo patch initially
        mongo_patch = mongomock.patch(servers=(("localhost", 27017),))
        mongo_patch.start()

        mock.patch(
            "huxunify.api.route.utils.get_db_client", side_effect=Exception()
        ).start()

        status, message = check_mongo_connection()
        self.assertFalse(status)
        self.assertEqual("Mongo not available.", message)

    def test_health_check(self):
        """Test health check."""
        mock.patch(
            "huxunify.api.route.utils.check_mongo_connection",
            return_value=(True, "Mongo available"),
        ).start()
        mock.patch.object(
            Tecton,
            "check_tecton_connection",
            return_value=(True, "Tecton available."),
        ).start()
        mock.patch(
            "huxunify.api.route.utils.check_okta_connection",
            return_value=(True, "OKTA available."),
        ).start()
        mock.patch(
            "huxunify.api.route.utils.check_cdm_api_connection",
            return_value=(True, "CDM available."),
        ).start()
        mock.patch(
            "huxunify.api.route.utils.check_cdp_connections_api_connection",
            return_value=(True, "CDP connections available."),
        ).start()
        mock.patch(
            "huxunify.api.route.utils.check_aws_ssm",
            return_value=(True, "AWS SSM available"),
        ).start()
        mock.patch(
            "huxunify.api.route.utils.check_aws_batch",
            return_value=(True, "AWS Batch available"),
        ).start()

        health = get_health_check()
        self.assertTrue(health)

    def test_get_friendly_delivery_time(self):
        """Test get friendly delivered time."""

        delivered_time = datetime.utcnow() - timedelta(days=2)
        response = get_friendly_delivered_time(delivered_time)
        self.assertEqual("2 days ago", response)

        delivered_time = datetime.utcnow() - timedelta(hours=5)
        response = get_friendly_delivered_time(delivered_time)
        self.assertEqual("5 hours ago", response)

        delivered_time = datetime.utcnow() - timedelta(minutes=15)
        response = get_friendly_delivered_time(delivered_time)
        self.assertEqual("15 minutes ago", response)

        delivered_time = datetime.utcnow() - timedelta(seconds=15)
        response = get_friendly_delivered_time(delivered_time)
        self.assertEqual("15 seconds ago", response)

    def test_update_metrics(self):
        """Test update metrics."""

        target_id = ObjectId()
        perf_metric = update_metrics(
            target_id, "test_name", [], [], api_c.DISPLAY_ADS
        )

        self.assertEqual(str(target_id), perf_metric.get(api_c.ID))
        self.assertEqual("test_name", perf_metric.get(api_c.NAME))

    def test_validate_integer(self):
        """Tests the Validation class static method validate_integer."""

        with self.assertRaises(expected_exception=InputParamsValidationError):
            Validation.validate_integer("a")

        with self.assertRaises(expected_exception=InputParamsValidationError):
            Validation.validate_integer("1.1")

        with self.assertRaises(expected_exception=InputParamsValidationError):
            Validation.validate_integer("-1")

        with self.assertRaises(expected_exception=InputParamsValidationError):
            Validation.validate_integer("0")

        with self.assertRaises(expected_exception=InputParamsValidationError):
            Validation.validate_integer("12341234567123456")

        Validation.validate_integer("1")
        Validation.validate_integer("12345")

    def test_validate_boolean(self):
        """Tests the Validation class static method validate_boolean."""

        with self.assertRaises(expected_exception=InputParamsValidationError):
            Validation.validate_bool("tru")

        with self.assertRaises(expected_exception=InputParamsValidationError):
            Validation.validate_bool("0")

        Validation.validate_bool("true")
        Validation.validate_bool("false")
        Validation.validate_bool("TRUE")
        Validation.validate_bool("FALSE")
        Validation.validate_bool("TrUe")
        Validation.validate_bool("fAlSe")

    def test_validate_date(self):
        """Tests the Validation class static method validate_date."""

        with self.assertRaises(expected_exception=InputParamsValidationError):
            Validation.validate_date("2021-09-111")

        with self.assertRaises(expected_exception=InputParamsValidationError):
            Validation.validate_date("2021-09-aa")

        with self.assertRaises(expected_exception=InputParamsValidationError):
            Validation.validate_date("2021-09-1O")

        with self.assertRaises(expected_exception=InputParamsValidationError):
            Validation.validate_date("2021-13-1")

        with self.assertRaises(expected_exception=InputParamsValidationError):
            Validation.validate_date("20212-13-1")

        with self.assertRaises(expected_exception=InputParamsValidationError):
            Validation.validate_date("1969-0009-0001")

        Validation.validate_date("2021-12-1")
        Validation.validate_date("2021-09-01")
        Validation.validate_date("1969-9-1")

    def test_validate_date_range(self):
        """Tests the Validation class static method validate_date_range."""

        with self.assertRaises(expected_exception=InputParamsValidationError):
            Validation.validate_date_range("2021-09-11", "2021-13-11")

        with self.assertRaises(expected_exception=InputParamsValidationError):
            Validation.validate_date_range("2021-09-11", "2021-08")

        with self.assertRaises(expected_exception=InputParamsValidationError):
            Validation.validate_date_range("2021-09-11", "2021-08-01")

        Validation.validate_date_range("2021-9-11", "2021-9-12")
        Validation.validate_date_range("2021-9-11", "2021-09-11")

    def test_validate_hux_id(self):
        """Tests the Validation class static method validate_hux_id."""

        with self.assertRaises(expected_exception=InputParamsValidationError):
            Validation.validate_hux_id("HUX12345678901234")

        with self.assertRaises(expected_exception=InputParamsValidationError):
            Validation.validate_hux_id("123456789012345")

        with self.assertRaises(expected_exception=InputParamsValidationError):
            Validation.validate_hux_id("HUX1234567890l2345")

        Validation.validate_hux_id("HUX123456789012345")

    @given(
        city=st.sampled_from(["Wonderland", "Mind Palace"]),
        state=st.sampled_from(["Gotham", "Wakanda", "Starling"]),
        country=st.sampled_from(["USA"]),
    )
    def test_convert_unique_city_filter(
        self, city: str, state: str, country: str
    ):
        """Test conversion to unique city filters.

        Args:
            city (str): City name
            state (str): State name
            country (str): Country name

        """
        request_filter = {
            api_c.AUDIENCE_FILTERS: [
                {
                    api_c.AUDIENCE_SECTION_AGGREGATOR: "ALL",
                    api_c.AUDIENCE_SECTION_FILTERS: [
                        {
                            api_c.AUDIENCE_FILTER_FIELD: api_c.AUDIENCE_FILTER_CITY,
                            api_c.AUDIENCE_FILTER_TYPE: api_c.AUDIENCE_FILTERS_EQUALS,
                            api_c.AUDIENCE_FILTER_VALUE: f"{city}|{state}|{country}",
                        }
                    ],
                }
            ]
        }

        response = convert_unique_city_filter(request_filter)

        self.assertTrue(response)
        self.assertEqual(
            2,
            len(
                response[api_c.AUDIENCE_FILTERS][0][
                    api_c.AUDIENCE_SECTION_FILTERS
                ]
            ),
        )
        section_filters = []

        for section_filter in response[api_c.AUDIENCE_FILTERS][0][
            api_c.AUDIENCE_SECTION_FILTERS
        ]:
            section_filters.append(section_filter[api_c.AUDIENCE_FILTER_FIELD])
            if (
                section_filter[api_c.AUDIENCE_FILTER_FIELD]
                == api_c.AUDIENCE_FILTER_CITY
            ):
                self.assertEqual(
                    city, section_filter[api_c.AUDIENCE_FILTER_VALUE]
                )
            if section_filter[api_c.AUDIENCE_FILTER_FIELD] == api_c.STATE:
                self.assertEqual(
                    state, section_filter[api_c.AUDIENCE_FILTER_VALUE]
                )

        self.assertIn(api_c.AUDIENCE_FILTER_CITY, section_filters)
        self.assertIn(api_c.STATE, section_filters)

    def test_convert_unique_city_filter_value_error(self):
        """Test conversion of unique city filter for value error."""
        request_filter = {
            api_c.AUDIENCE_FILTERS: [
                {
                    api_c.AUDIENCE_SECTION_AGGREGATOR: "ALL",
                    api_c.AUDIENCE_SECTION_FILTERS: [
                        {
                            api_c.AUDIENCE_FILTER_FIELD: api_c.AUDIENCE_FILTER_CITY,
                            api_c.AUDIENCE_FILTER_TYPE: api_c.AUDIENCE_FILTERS_EQUALS,
                            api_c.AUDIENCE_FILTER_VALUE: "Las Vegas",
                        }
                    ],
                }
            ]
        }

        response = convert_unique_city_filter(request_filter)

        self.assertEqual(request_filter, response)

    def test_convert_unique_city_filter_key_error(self):
        """Test conversion of unique city filter for key error."""
        request_filter = {
            api_c.AUDIENCE_FILTERS: [
                {
                    api_c.AUDIENCE_SECTION_AGGREGATOR: "ALL",
                    api_c.AUDIENCE_SECTION_FILTERS: [
                        {
                            f"{api_c.AUDIENCE_FILTER_FIELD}s": api_c.AUDIENCE_FILTER_CITY,
                            api_c.AUDIENCE_FILTER_TYPE: api_c.AUDIENCE_FILTERS_EQUALS,
                            api_c.AUDIENCE_FILTER_VALUE: "Las Vegas",
                        }
                    ],
                }
            ]
        }

        response = convert_unique_city_filter(request_filter)

        self.assertEqual(request_filter, response)
