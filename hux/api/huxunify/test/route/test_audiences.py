"""Purpose of this file is to house audience related tests."""
import csv
import string
from datetime import datetime
from http import HTTPStatus
from io import BytesIO
from unittest import TestCase, mock
from zipfile import ZipFile

import mongomock
import requests_mock
from bson import ObjectId
from hypothesis import given, strategies as st

from huxunifylib.connectors.connector_cdp import ConnectorCDP

from huxunifylib.database import constants as db_c
from huxunifylib.database.client import DatabaseClient
from huxunifylib.database.orchestration_management import (
    create_audience,
    get_audience,
    append_destination_to_standalone_audience,
)
from huxunifylib.database.delivery_platform_management import (
    set_delivery_platform,
)

from huxunify.api.data_connectors.cloud.cloud_client import CloudClient
from huxunify.api import constants as api_c
from huxunify.api.config import get_config
from huxunify.api.schema.customers import (
    CustomersInsightsCitiesSchema,
    CustomersInsightsStatesSchema,
    CustomersInsightsCountriesSchema,
    TotalCustomersInsightsSchema,
    CustomerRevenueInsightsSchema,
)
from huxunify.app import create_app
from huxunify.test import constants as t_c
from huxunify.test.route.route_test_util.route_test_case import RouteTestCase


class AudienceDownloadsTest(RouteTestCase):
    """Test audience download."""

    def setUp(self) -> None:
        """Setup tests."""
        config = get_config()
        config.CLOUD_PROVIDER = "aws"

        self.audiences_endpoint = (
            f"{t_c.BASE_ENDPOINT}{api_c.AUDIENCE_ENDPOINT}"
        )

        super().setUp()

        # mock get_db_client() in audiences
        mock.patch(
            "huxunify.api.route.audiences.get_db_client",
            return_value=self.database,
        ).start()

        mock.patch(
            "huxunify.api.route.audiences.get_db_client",
            return_value=self.database,
        ).start()

        # create audience first
        audience = {
            db_c.AUDIENCE_NAME: "Test Audience",
            "audience_filters": [],
            api_c.USER_NAME: self.user_name,
            api_c.DESTINATION_IDS: [],
        }
        self.audience = create_audience(self.database, **audience)

        mock.patch(
            "huxunify.api.route.utils.create_audience_audit",
            return_value={
                api_c.USER_NAME: self.user_name,
                api_c.AUDIENCE_ID: self.audience,
                db_c.DOWNLOAD_TIME: datetime.utcnow(),
                api_c.DOWNLOAD_TYPE: "google_ads",
                db_c.FILE_NAME: "abc.csv",
            },
        ).start()

        for subclass in CloudClient.__subclasses__():
            mock.patch.object(
                subclass,
                "upload_file",
                return_value=True,
            ).start()

    def test_download_google_ads(self) -> None:
        """Test to check download google_ads customers hashed data."""

        # mock read_batches() in ConnectorCDP class to a return a test generator
        mock.patch.object(
            ConnectorCDP,
            "read_batch",
            return_value=t_c.dataframe_method(),
        ).start()

        mock.patch.object(
            ConnectorCDP,
            "_connect",
            return_value=True,
        ).start()

        mock.patch.object(
            ConnectorCDP, "fetch_okta_token", return_value=t_c.TEST_AUTH_TOKEN
        ).start()

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.AUDIENCE_ENDPOINT}/"
            f"{self.audience[db_c.ID]}/download?download_types={api_c.GOOGLE_ADS}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual("application/zip", response.content_type)

    def test_download_amazon_ads(self) -> None:
        """Test to check download amazon_ads customers hashed data."""

        # mock read_batches() in ConnectorCDP class to a return a test generator
        mock.patch.object(
            ConnectorCDP,
            "read_batch",
            return_value=t_c.dataframe_method(),
        ).start()

        mock.patch.object(
            ConnectorCDP,
            "_connect",
            return_value=True,
        ).start()

        mock.patch.object(
            ConnectorCDP, "fetch_okta_token", return_value=t_c.TEST_AUTH_TOKEN
        ).start()

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.AUDIENCE_ENDPOINT}/"
            f"{self.audience[db_c.ID]}/download?download_types={api_c.AMAZON_ADS}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual("application/zip", response.content_type)

    def test_download_generic_ads(self) -> None:
        """Test to check download generic customers both hashed and PII data."""

        # mock read_batches() in ConnectorCDP class to a return a test generator
        mock.patch.object(
            ConnectorCDP,
            "read_batch",
            return_value=t_c.dataframe_method(),
        ).start()

        mock.patch.object(
            ConnectorCDP,
            "_connect",
            return_value=True,
        ).start()

        mock.patch.object(
            ConnectorCDP, "fetch_okta_token", return_value=t_c.TEST_AUTH_TOKEN
        ).start()

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.AUDIENCE_ENDPOINT}/"
            f"{self.audience[db_c.ID]}/download?download_types={api_c.GENERIC_ADS}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual("application/zip", response.content_type)

    def test_download_multiple_types(self) -> None:
        """Test to check download multiple types"""

        # mock read_batches() in ConnectorCDP class to a return a test generator
        mock.patch.object(
            ConnectorCDP,
            "read_batch",
            return_value=t_c.dataframe_method(),
        ).start()

        mock.patch.object(
            ConnectorCDP,
            "_connect",
            return_value=True,
        ).start()

        mock.patch.object(
            ConnectorCDP, "fetch_okta_token", return_value=t_c.TEST_AUTH_TOKEN
        ).start()

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.AUDIENCE_ENDPOINT}/"
            f"{self.audience[db_c.ID]}/download?download_types={api_c.GOOGLE_ADS}"
            f"&download_types={api_c.AMAZON_ADS}&download_types={api_c.GENERIC_ADS}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual("application/zip", response.content_type)

    def test_download_empty_google_ads(self) -> None:
        """Test to check download empty google_ads audience file."""

        # mock config to change the RETURN_EMPTY_AUDIENCE_FILE config value to
        # True since pytest mode's default value for this config is False
        self.config.RETURN_EMPTY_AUDIENCE_FILE = True
        mock.patch(
            "huxunify.api.config.get_config",
            return_value=self.config,
        ).start()

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.AUDIENCE_ENDPOINT}/"
            f"{self.audience[db_c.ID]}/download?download_types={api_c.GOOGLE_ADS}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual("application/zip", response.content_type)

        with ZipFile(BytesIO(response.data)) as zipfile:
            for file in zipfile.namelist():
                row_count = len(list(csv.reader(file.splitlines())))
                self.assertEqual(1, row_count)

    def test_download_empty_amazon_ads(self) -> None:
        """Test to check download empty amazon_ads audience file."""

        # mock config to change the RETURN_EMPTY_AUDIENCE_FILE config value to
        # True since pytest mode's default value for this config is False
        self.config.RETURN_EMPTY_AUDIENCE_FILE = True
        mock.patch(
            "huxunify.api.config.get_config",
            return_value=self.config,
        ).start()

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.AUDIENCE_ENDPOINT}/"
            f"{self.audience[db_c.ID]}/download?download_types={api_c.AMAZON_ADS}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual("application/zip", response.content_type)
        with ZipFile(BytesIO(response.data)) as zipfile:
            for file in zipfile.namelist():
                row_count = len(list(csv.reader(file.splitlines())))
                self.assertEqual(1, row_count)

    def test_download_empty_generic_ads(self) -> None:
        """Test to check download empty generic_ads audience file."""

        # mock config to change the RETURN_EMPTY_AUDIENCE_FILE config value to
        # True since pytest mode's default value for this config is False
        self.config.RETURN_EMPTY_AUDIENCE_FILE = True
        mock.patch(
            "huxunify.api.config.get_config",
            return_value=self.config,
        ).start()

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.AUDIENCE_ENDPOINT}/"
            f"{self.audience[db_c.ID]}/download?download_types={api_c.GENERIC_ADS}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual("application/zip", response.content_type)
        with ZipFile(BytesIO(response.data)) as zipfile:
            for file in zipfile.namelist():
                row_count = len(list(csv.reader(file.splitlines())))
                self.assertEqual(1, row_count)

    def test_download_empty_multiple_types(self) -> None:
        """Test to check download empty multiple types"""

        # mock config to change the RETURN_EMPTY_AUDIENCE_FILE config value to
        # True since pytest mode's default value for this config is False
        self.config.RETURN_EMPTY_AUDIENCE_FILE = True
        mock.patch(
            "huxunify.api.config.get_config",
            return_value=self.config,
        ).start()

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.AUDIENCE_ENDPOINT}/"
            f"{self.audience[db_c.ID]}/download?download_types={api_c.GOOGLE_ADS}"
            f"&download_types={api_c.AMAZON_ADS}&download_types={api_c.GENERIC_ADS}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual("application/zip", response.content_type)
        with ZipFile(BytesIO(response.data)) as zipfile:
            for file in zipfile.namelist():
                row_count = len(list(csv.reader(file.splitlines())))
                self.assertEqual(1, row_count)


class AudienceInsightsTest(TestCase):
    """Tests for Audience Insights"""

    def setUp(self) -> None:
        """Setup tests."""

        self.audiences_endpoint = (
            f"{t_c.BASE_ENDPOINT}{api_c.AUDIENCE_ENDPOINT}"
        )

        # init mongo patch initially
        mongo_patch = mongomock.patch(servers=(("localhost", 27017),))
        mongo_patch.start()

        # setup the mock DB client
        self.database = DatabaseClient(
            "localhost", 27017, None, None
        ).connect()

        # mock get_db_client() in utils
        mock.patch(
            "huxunify.api.route.utils.get_db_client",
            return_value=self.database,
        ).start()

        # mock get_db_client() in decorators
        mock.patch(
            "huxunify.api.route.decorators.get_db_client",
            return_value=self.database,
        ).start()

        # mock get_db_client() in audiences
        mock.patch(
            "huxunify.api.route.audiences.get_db_client",
            return_value=self.database,
        ).start()

        mock.patch(
            "huxunify.api.data_connectors.cache.get_db_client",
            return_value=self.database,
        ).start()

        # mock request for introspect call
        self.request_mocker = requests_mock.Mocker()
        self.request_mocker.post(
            t_c.INTROSPECT_CALL, json=t_c.VALID_INTROSPECTION_RESPONSE
        )
        self.request_mocker.get(
            t_c.USER_INFO_CALL, json=t_c.VALID_USER_RESPONSE
        )
        self.request_mocker.get(
            t_c.CDM_HEALTHCHECK_CALL, json=t_c.CDM_HEALTHCHECK_RESPONSE
        )
        self.request_mocker.start()

        # stop all mocks in cleanup
        self.addCleanup(mock.patch.stopall)

        # setup the flask test client
        self.app = create_app().test_client()

        self.database.drop_database(db_c.DATA_MANAGEMENT_DATABASE)

        self.user_name = "Joe Smithers"

        # create audience first
        audience = {
            db_c.AUDIENCE_NAME: "Test Audience",
            "audience_filters": api_c.CUSTOMER_OVERVIEW_DEFAULT_FILTER[
                api_c.AUDIENCE_FILTERS
            ],
            api_c.USER_NAME: self.user_name,
            api_c.DESTINATION_IDS: [],
        }
        self.audience = create_audience(self.database, **audience)

    def test_audience_insights_cities_success(self) -> None:
        """Test get audience insights by cities."""

        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.CUSTOMER_PROFILE_API}/customer-profiles/insights/city-ltvs",
            json=t_c.CUSTOMERS_INSIGHTS_BY_CITY_RESPONSE,
        )

        self.request_mocker.start()

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.AUDIENCE_ENDPOINT}/{self.audience[db_c.ID]}/{api_c.CITIES}",
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
            f"{t_c.BASE_ENDPOINT}{api_c.AUDIENCE_ENDPOINT}/{self.audience[db_c.ID]}/{api_c.STATES}",
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

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.AUDIENCE_ENDPOINT}/"
            f"{self.audience[db_c.ID]}/{api_c.COUNTRIES}",
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

    @given(
        city_substring=st.text(
            alphabet=string.ascii_letters, min_size=3, max_size=5
        )
    )
    def test_audience_location_rules_cities(self, city_substring: str) -> None:
        """Test get audience location rules cities.
        Args:
            city_substring (str): Substring for which cities need to be
            matched.
        """
        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.AUDIENCE_ENDPOINT}/rules/"
            f"{api_c.CITY}/{city_substring}",
            headers=t_c.STANDARD_HEADERS,
        )
        self.assertEqual(HTTPStatus.OK, response.status_code)

        substring_found = []
        for city in response.json:
            substring_found.append(
                city_substring.lower() in list(city.keys())[0].lower()
            )
        self.assertNotIn(False, substring_found)

    @given(zip_substring=st.integers(100, 9999))
    def test_audience_location_rules_zip(self, zip_substring: int) -> None:
        """Test get audience location rules zip.
        Args:
           zip_substring (int): Substring for which zip codes need to be
           matched.
        """
        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.AUDIENCE_ENDPOINT}/rules/"
            f"{api_c.ZIP_CODE}/{zip_substring}",
            headers=t_c.STANDARD_HEADERS,
        )
        self.assertEqual(HTTPStatus.OK, response.status_code)

        self.assertEqual(HTTPStatus.OK, response.status_code)

        substring_found = []
        for zip_code in response.json:
            substring_found.append(
                str(zip_substring) in list(zip_code.keys())[0].lower()
            )
        self.assertNotIn(False, substring_found)

    def test_audience_location_rules_unknown_field(self) -> None:
        """Test get audience location rules with unknown field."""
        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.AUDIENCE_ENDPOINT}/rules/"
            f"{api_c.USER}/ri",
            headers=t_c.STANDARD_HEADERS,
        )
        self.assertEqual(404, response.status_code)

    def test_audience_histogram_rules_age(self) -> None:
        """Test get audience location rules histogram for age field."""
        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.CUSTOMER_PROFILE_API}/customer-profiles/insights"
            f"/count-by-age",
            json=t_c.CDP_COUNT_BY_AGE_RESONSE,
        )
        self.request_mocker.start()

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.AUDIENCE_ENDPOINT}/rules/"
            f"{api_c.AGE}/histogram",
            headers=t_c.STANDARD_HEADERS,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json.get(api_c.VALUES))

    def test_audience_histogram_rules_model(self) -> None:
        """Test get audience rules histogram for model field."""
        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.CUSTOMER_PROFILE_API}/customer-profiles/insights"
            f"/counts/by-float-field",
            json=t_c.CDP_COUNTS_BY_FLOAT_RESONSE,
        )
        self.request_mocker.start()

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.AUDIENCE_ENDPOINT}/rules/"
            f"{api_c.MODEL}/histogram?{api_c.MODEL_NAME}=propensity_to_unsubscribe",
            headers=t_c.STANDARD_HEADERS,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json.get(api_c.VALUES))

    def test_audience_histogram_rules_model_unknown_name(self) -> None:
        """Test get audience rules histogram for model field unknown name."""
        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.AUDIENCE_ENDPOINT}/rules/"
            f"{api_c.MODEL}/histogram?{api_c.MODEL_NAME}=propensity_to_leave",
            headers=t_c.STANDARD_HEADERS,
        )
        self.assertEqual(response.status_code, 404)

    def test_audience_histogram_rules_unknown(self) -> None:
        """Test get audience rules histogram for field unknown name."""
        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.AUDIENCE_ENDPOINT}/rules/"
            f"{api_c.USER}/histogram",
            headers=t_c.STANDARD_HEADERS,
        )
        self.assertEqual(response.status_code, 404)

    def test_total_audience_insights_success(self) -> None:
        """Test get total audience insights success response."""

        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/insights/count-by-day",
            json=t_c.CUSTOMER_INSIGHTS_COUNT_BY_DAY_RESPONSE,
        )
        self.request_mocker.start()

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.AUDIENCE_ENDPOINT}/{self.audience[db_c.ID]}/{api_c.TOTAL}",
            headers=t_c.STANDARD_HEADERS,
        )
        self.assertEqual(HTTPStatus.OK, response.status_code)

        self.assertTrue(
            t_c.validate_schema(
                TotalCustomersInsightsSchema(), response.json, True
            )
        )

    def test_audience_revenue_insights_success(self) -> None:
        """Test get audience revenue insights success response."""

        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/insights"
            f"/spending-by-day",
            json=t_c.MOCKED_GENDER_SPENDING_BY_DAY,
        )
        self.request_mocker.start()

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.AUDIENCE_ENDPOINT}/"
            f"{self.audience[db_c.ID]}/{api_c.REVENUE}",
            headers=t_c.STANDARD_HEADERS,
        )
        self.assertEqual(HTTPStatus.OK, response.status_code)

        self.assertTrue(
            t_c.validate_schema(
                CustomerRevenueInsightsSchema(), response.json, True
            )
        )


class TestAudienceDestination(TestCase):
    """Test for Audience Destination"""

    def setUp(self):
        """Setup tests."""
        self.config = get_config(api_c.TEST_MODE)
        # init mongo patch initially
        mongo_patch = mongomock.patch(servers=(("localhost", 27017),))
        mongo_patch.start()

        # setup the mock DB client
        self.database = DatabaseClient(
            "localhost", 27017, None, None
        ).connect()

        # mock get_db_client() in utils
        mock.patch(
            "huxunify.api.route.utils.get_db_client",
            return_value=self.database,
        ).start()

        # mock get_db_client() in decorators
        mock.patch(
            "huxunify.api.route.decorators.get_db_client",
            return_value=self.database,
        ).start()

        # mock get_db_client() in audiences
        mock.patch(
            "huxunify.api.route.audiences.get_db_client",
            return_value=self.database,
        ).start()

        # mock request for introspect call
        self.request_mocker = requests_mock.Mocker()
        self.request_mocker.post(
            t_c.INTROSPECT_CALL, json=t_c.VALID_INTROSPECTION_RESPONSE
        )
        self.request_mocker.get(
            t_c.USER_INFO_CALL, json=t_c.VALID_USER_RESPONSE
        )
        self.request_mocker.get(
            t_c.CDM_HEALTHCHECK_CALL, json=t_c.CDM_HEALTHCHECK_RESPONSE
        )
        self.request_mocker.start()

        # stop all mocks in cleanup
        self.addCleanup(mock.patch.stopall)

        # setup the flask test client
        self.app = create_app().test_client()

        self.database.drop_database(db_c.DATA_MANAGEMENT_DATABASE)

        self.user_name = "Joe Smithers"

        self.delivery_platform_doc = set_delivery_platform(
            self.database,
            db_c.DELIVERY_PLATFORM_FACEBOOK,
            db_c.DELIVERY_PLATFORM_FACEBOOK.lower(),
            {
                "facebook_access_token": "path1",
                "facebook_app_secret": "path2",
                "facebook_app_id": "path3",
                "facebook_ad_account_id": "path4",
            },
        )
        self.audience = create_audience(
            self.database,
            **{
                db_c.AUDIENCE_NAME: "Test Audience",
                "audience_filters": [],
                api_c.USER_NAME: self.user_name,
                api_c.DESTINATION_IDS: [],
            },
        )

    def test_add_destination_audience(self) -> None:
        """Test Adding destination to audience"""
        destination = {"id": str(self.delivery_platform_doc[db_c.ID])}

        response = self.app.post(
            f"{t_c.BASE_ENDPOINT}{api_c.AUDIENCE_ENDPOINT}/{self.audience[db_c.ID]}/"
            f"destinations",
            json=destination,
            headers=t_c.STANDARD_HEADERS,
        )
        self.assertIn(
            destination[api_c.ID],
            [x[api_c.ID] for x in response.json[api_c.DESTINATIONS]],
        )

        audience_doc = get_audience(
            database=self.database, audience_id=self.audience[db_c.ID]
        )
        self.assertIn(
            ObjectId(destination[api_c.ID]),
            [x[api_c.ID] for x in audience_doc[api_c.DESTINATIONS]],
        )

    def test_delete_destination_audience(self) -> None:
        """Test Removing destination to audience"""
        destination = {"id": str(self.delivery_platform_doc[db_c.ID])}

        # append destination first
        append_destination_to_standalone_audience(
            database=self.database,
            audience_id=self.audience[db_c.ID],
            destination=destination,
            user_name=self.user_name,
        )

        # removing destination
        response = self.app.delete(
            f"{t_c.BASE_ENDPOINT}{api_c.AUDIENCE_ENDPOINT}/"
            f"{self.audience[db_c.ID]}/"
            f"destinations",
            json=destination,
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.NO_CONTENT, response.status_code)

        audience_doc = get_audience(
            database=self.database, audience_id=self.audience[db_c.ID]
        )
        self.assertNotIn(
            ObjectId(destination[api_c.ID]),
            audience_doc[api_c.DESTINATIONS],
        )
