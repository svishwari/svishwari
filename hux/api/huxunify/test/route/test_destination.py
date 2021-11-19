"""Purpose of this file is to house all the destination api tests."""
from datetime import datetime
from unittest import TestCase, mock
from unittest.mock import MagicMock, patch
from http import HTTPStatus

import requests_mock
import mongomock
from bson import ObjectId

from huxunifylib.connectors import FacebookConnector
from huxunifylib.database import constants as db_c
from huxunifylib.database.client import DatabaseClient
from huxunifylib.database import (
    delivery_platform_management as destination_management,
    collection_management,
)
import huxunify.test.constants as t_c
from huxunify.api.data_connectors.aws import parameter_store
from huxunify.api.schema.destinations import DestinationDataExtGetSchema
from huxunify.api import constants as api_c
from huxunify.app import create_app


# pylint: disable=too-many-public-methods
class TestDestinationRoutes(TestCase):
    """Test Destination Routes."""

    def setUp(self) -> None:
        """Setup resources before each test."""

        # mock request for introspect call
        request_mocker = requests_mock.Mocker()
        request_mocker.post(t_c.INTROSPECT_CALL, json=t_c.VALID_RESPONSE)
        request_mocker.get(t_c.USER_INFO_CALL, json=t_c.VALID_USER_RESPONSE)
        request_mocker.start()

        self.app = create_app().test_client()
        self.new_auth_details = {
            api_c.AUTHENTICATION_DETAILS: {
                api_c.FACEBOOK_ACCESS_TOKEN: "fake_fake",
                api_c.FACEBOOK_APP_SECRET: "fake",
                api_c.FACEBOOK_APP_ID: "1234",
                api_c.FACEBOOK_AD_ACCOUNT_ID: "12345678",
            }
        }

        # init mongo patch initially
        mongo_patch = mongomock.patch(servers=(("localhost", 27017),))
        mongo_patch.start()

        # setup the mock DB client
        self.database = DatabaseClient(
            "localhost", 27017, None, None
        ).connect()

        # mock get db client from destinations
        mock.patch(
            "huxunify.api.route.destination.get_db_client",
            return_value=self.database,
        ).start()

        # mock get_db_client() for the userinfo decorator.
        mock.patch(
            "huxunify.api.route.decorators.get_db_client",
            return_value=self.database,
        ).start()

        # mock get_db_client() for the userinfo utils.
        mock.patch(
            "huxunify.api.route.utils.get_db_client",
            return_value=self.database,
        ).start()

        # mock parameter store store secret
        mock.patch.object(parameter_store, "store_secret").start()

        # mock parameter store get store value
        mock.patch.object(
            parameter_store, "get_store_value", return_value="secret"
        ).start()

        destinations = [
            {
                api_c.DELIVERY_PLATFORM_TYPE: db_c.DELIVERY_PLATFORM_FACEBOOK,
                api_c.NAME: db_c.DELIVERY_PLATFORM_FACEBOOK,
                api_c.AUTHENTICATION_DETAILS: {},
            },
            {
                api_c.DELIVERY_PLATFORM_TYPE: "amazon-advertising",
                api_c.NAME: "Amazon Advertising",
                api_c.AUTHENTICATION_DETAILS: {},
            },
            {
                api_c.DELIVERY_PLATFORM_TYPE: db_c.DELIVERY_PLATFORM_SFMC,
                api_c.NAME: "Salesforce Marketing Cloud",
                api_c.AUTHENTICATION_DETAILS: {
                    api_c.SFMC_ACCOUNT_ID: "id12345",
                    api_c.SFMC_AUTH_BASE_URI: "base_uri",
                    api_c.SFMC_CLIENT_ID: "id12345",
                    api_c.SFMC_CLIENT_SECRET: "client_secret",
                    api_c.SFMC_SOAP_BASE_URI: "soap_base_uri",
                    api_c.SFMC_REST_BASE_URI: "rest_base_uri",
                },
            },
        ]

        for destination in destinations:
            destination_management.set_delivery_platform(
                self.database, **destination
            )

        self.destinations = destination_management.get_all_delivery_platforms(
            self.database
        )

        self.addCleanup(mock.patch.stopall)

    def test_get_all_destinations(self):
        """Test get all destinations."""

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.DESTINATIONS_ENDPOINT}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(len(self.destinations), len(response.json))

    def test_request_existing_destination_invalid_id(self):
        """Test request existing destinations with invalid id."""

        existing_destination_request = {
            api_c.ID: "id",
            api_c.NAME: "Adobe",
            api_c.CONTACT_EMAIL: "test_email@gmail.com",
            api_c.CLIENT_REQUEST: True,
            api_c.CLIENT_ACCOUNT: True,
            api_c.USE_CASE: "Testing",
        }
        response = self.app.post(
            f"{t_c.BASE_ENDPOINT}{api_c.DESTINATIONS_ENDPOINT}/request",
            headers=t_c.STANDARD_HEADERS,
            json=existing_destination_request,
        )

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)

    @mock.patch(
        "huxunify.api.route.destination.JiraConnection.create_jira_issue"
    )
    @mock.patch("huxunify.api.route.destination.JiraConnection.__init__")
    def test_request_new_destination(
        self, jira_class_init, jira_create_issue_mock
    ):
        """Test request new destinations.

        Args:
            jira_class_init (MagicMock): Mock creating jira class.
            jira_create_issue_mock (MagicMock): Mock creating jira issue.
        """

        new_destination_request = {
            api_c.NAME: "My custom destination",
            api_c.CONTACT_EMAIL: "test_email@gmail.com",
            api_c.CLIENT_REQUEST: True,
            api_c.CLIENT_ACCOUNT: True,
            api_c.USE_CASE: "Testing",
        }

        jira_class_init.return_value = None
        jira_create_issue_mock.return_value = {db_c.CONSTANT_KEY: ""}

        response = self.app.post(
            f"{t_c.BASE_ENDPOINT}{api_c.DESTINATIONS_ENDPOINT}/request",
            headers=t_c.STANDARD_HEADERS,
            json=new_destination_request,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)

        # test value is in the data base.
        destinations = collection_management.get_documents(
            self.database,
            db_c.DELIVERY_PLATFORM_COLLECTION,
            {
                db_c.NAME: {
                    "$regex": new_destination_request[db_c.NAME],
                    "$options": "i",
                }
            },
            batch_size=1,
        )

        # check list was returned
        self.assertTrue(destinations[db_c.DOCUMENTS])
        # check length of list
        self.assertEqual(1, len(destinations[db_c.DOCUMENTS]))
        # check status is equal to requested
        self.assertEqual(
            db_c.STATUS_REQUESTED,
            destinations[db_c.DOCUMENTS][0][db_c.DELIVERY_PLATFORM_STATUS],
        )

    # pylint: disable=unused-argument
    @patch(
        "huxunify.api.route.destination.FacebookConnector",
        **{"return_value.raiseError.side_effect": Exception()},
    )
    @patch(
        "huxunify.api.route.destination.SFMCConnector",
        **{"return_value.raiseError.side_effect": Exception()},
    )
    def test_get_all_destinations_with_refresh(
        self,
        mock_facebook_connector: MagicMock,
        mock_sfmc_connector: MagicMock,
    ):
        """Test get all destinations with refresh.

        Args:
            mock_facebook_connector (MagicMock): MagicMock of the Facebook Connector.
            mock_sfmc_connector (MagicMock): MagicMock of the SFMC Connector.
        """

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.DESTINATIONS_ENDPOINT}?refresh_all=False",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(len(self.destinations), len(response.json))
        self.assertEqual(response.json[0][db_c.STATUS], api_c.STATUS_PENDING)

        destination_id = self.destinations[0][db_c.ID]

        self.app.put(
            f"{t_c.BASE_ENDPOINT}{api_c.DESTINATIONS_ENDPOINT}"
            f"/{destination_id}/{api_c.AUTHENTICATION}",
            json=self.new_auth_details,
            headers=t_c.STANDARD_HEADERS,
        )

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.DESTINATIONS_ENDPOINT}?refresh_all=True",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(len(self.destinations), len(response.json))
        self.assertEqual(response.json[0][db_c.STATUS], api_c.STATUS_ACTIVE)
        self.assertEqual(response.json[2][db_c.STATUS], api_c.STATUS_ACTIVE)

    def test_get_destination_with_valid_id(self):
        """Test get destination with valid ID."""

        destination_id = self.destinations[0][db_c.ID]

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.DESTINATIONS_ENDPOINT}/{destination_id}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(
            self.destinations[0][db_c.NAME], response.json[db_c.NAME]
        )

    def test_get_destination_where_destination_not_found(self):
        """Test get destination with a valid ID that is not in the DB."""

        destination_id = ObjectId()

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.DESTINATIONS_ENDPOINT}/{destination_id}",
            headers=t_c.STANDARD_HEADERS,
        )

        valid_response = {"message": api_c.DESTINATION_NOT_FOUND}

        self.assertEqual(valid_response, response.json)
        self.assertEqual(HTTPStatus.NOT_FOUND, response.status_code)

    def test_get_destination_invalid_object_id(self):
        """Test get destination with an invalid ObjectID."""

        destination_id = "asdfgh2345"

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.DESTINATIONS_ENDPOINT}/{destination_id}",
            headers=t_c.STANDARD_HEADERS,
        )

        valid_response = {"message": api_c.BSON_INVALID_ID(destination_id)}

        self.assertEqual(valid_response, response.json)
        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)

    def test_update_destination_auth_details(self):
        """Test update destination."""

        destination_id = self.destinations[0][db_c.ID]

        response = self.app.put(
            f"{t_c.BASE_ENDPOINT}{api_c.DESTINATIONS_ENDPOINT}"
            f"/{destination_id}/{api_c.AUTHENTICATION}",
            json=self.new_auth_details,
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)

    def test_update_destination_auth_details_where_destination_not_found(self):
        """Test update destination where no destination is found."""

        destination_id = ObjectId()

        response = self.app.put(
            f"{t_c.BASE_ENDPOINT}{api_c.DESTINATIONS_ENDPOINT}"
            f"/{destination_id}/{api_c.AUTHENTICATION}",
            json=self.new_auth_details,
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.NOT_FOUND, response.status_code)

    def test_update_destination_auth_details_invalid_object_id(self):
        """Test update destination where invalid ID given."""

        destination_id = t_c.INVALID_ID

        response = self.app.put(
            f"{t_c.BASE_ENDPOINT}{api_c.DESTINATIONS_ENDPOINT}"
            f"/{destination_id}/{api_c.AUTHENTICATION}",
            json=self.new_auth_details,
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)

    def test_retrieve_destinations_constants(self):
        """Test retrieve all destination constants."""

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.DESTINATIONS_ENDPOINT}/constants",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIn(db_c.DELIVERY_PLATFORM_FACEBOOK, response.json)
        self.assertIn(db_c.DELIVERY_PLATFORM_SFMC, response.json)
        self.assertIn(db_c.DELIVERY_PLATFORM_SENDGRID, response.json)
        self.assertIn(api_c.GOOGLE_ADS, response.json)

    def test_validate_facebook_credentials(self):
        """Test validation of facebook credentials."""

        mock_facebook_connector = mock.patch.object(
            FacebookConnector, "check_connection", return_value=True
        )
        mock_facebook_connector.start()

        validation_details = {
            "type": "facebook",
            "authentication_details": {
                "facebook_access_token": "MkU3Ojgwm",
                "facebook_app_secret": "717bdOQqZO99",
                "facebook_app_id": "2951925002021888",
                "facebook_ad_account_id": "111333777",
            },
        }

        response = self.app.post(
            f"{t_c.BASE_ENDPOINT}{api_c.DESTINATIONS_ENDPOINT}/validate",
            json=validation_details,
            headers=t_c.STANDARD_HEADERS,
        )

        mock_facebook_connector.stop()
        validation_success = {
            "message": api_c.DESTINATION_AUTHENTICATION_SUCCESS
        }

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(validation_success, response.json)

    @patch(
        "huxunify.api.route.destination.FacebookConnector",
        **{"return_value.raiseError.side_effect": Exception()},
    )
    def test_validate_facebook_failure_bad_credentials(
        self, mock_connector: MagicMock
    ):
        """Test failure to authenticate with facebook due to bad credentials.

        Args:
            mock_connector (MagicMock): MagicMock of the Facebook Connector.
        """

        mock_facebook_connector = mock_connector.return_value
        mock_facebook_connector.check_connection.return_value = False

        validation_details = {
            "type": db_c.DELIVERY_PLATFORM_FACEBOOK,
            "authentication_details": {
                "facebook_access_token": "MkU3Ojgwm",
                "facebook_app_secret": "717bdOQqZO99",
                "facebook_app_id": "2951925002021888",
                "facebook_ad_account_id": "111333777",
            },
        }

        response = self.app.post(
            f"{t_c.BASE_ENDPOINT}{api_c.DESTINATIONS_ENDPOINT}/validate",
            json=validation_details,
            headers=t_c.STANDARD_HEADERS,
        )

        validation_failed = {
            "message": api_c.DESTINATION_AUTHENTICATION_FAILED
        }

        self.assertEqual(HTTPStatus.FORBIDDEN, response.status_code)
        self.assertEqual(validation_failed, response.json)

    # pylint: disable=unused-argument
    @patch(
        "huxunify.api.route.destination.SendgridConnector",
        **{"return_value.raiseError.side_effect": Exception()},
    )
    def test_validate_sendgrid_credentials(self, mock_connector: MagicMock):
        """Test successful authentication with sendgrid.

        Args:
            mock_connector (MagicMock): MagicMock of the Sendgrid Connector.
        """

        validation_details = {
            api_c.TYPE: db_c.DELIVERY_PLATFORM_SENDGRID,
            api_c.AUTHENTICATION_DETAILS: {
                api_c.SENDGRID_AUTH_TOKEN: "123456",
            },
        }

        response = self.app.post(
            f"{t_c.BASE_ENDPOINT}{api_c.DESTINATIONS_ENDPOINT}/validate",
            json=validation_details,
            headers=t_c.STANDARD_HEADERS,
        )

        validation_succeeded = {
            "message": api_c.DESTINATION_AUTHENTICATION_SUCCESS,
        }

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(validation_succeeded, response.json)

    @patch(
        "huxunify.api.route.destination.SendgridConnector",
        **{"return_value.raiseError.side_effect": Exception()},
    )
    def test_validate_sendgrid_credentials_failure_bad_credentials(
        self, mock_connector: MagicMock
    ):
        """Test failure to authenticate with sendgrid due to bad credentials

        Args:
            mock_connector (MagicMock): MagicMock of the Sendgrid Connector.
        """

        # mocks the return value of the SendgridConnector Constructor
        mock_connector.side_effect = Exception("Test Exception")

        validation_details = {
            api_c.TYPE: db_c.DELIVERY_PLATFORM_SENDGRID,
            api_c.AUTHENTICATION_DETAILS: {
                api_c.SENDGRID_AUTH_TOKEN: "123456",
            },
        }

        response = self.app.post(
            f"{t_c.BASE_ENDPOINT}{api_c.DESTINATIONS_ENDPOINT}/validate",
            json=validation_details,
            headers=t_c.STANDARD_HEADERS,
        )

        validation_failed = {
            "message": api_c.DESTINATION_AUTHENTICATION_FAILED
        }

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual(validation_failed, response.json)

    @patch(
        "huxunify.api.route.destination.GoogleConnector",
        **{"return_value.raiseError.side_effect": Exception()},
    )
    def test_validate_google_ads_credentials(self, mock_connector: MagicMock):
        """Test successful authentication with google ads.

        Args:
            mock_connector (MagicMock): MagicMock of the Google Connector.
        """

        validation_details = {
            api_c.TYPE: db_c.DELIVERY_PLATFORM_GOOGLE,
            api_c.AUTHENTICATION_DETAILS: {
                api_c.GOOGLE_DEVELOPER_TOKEN: "dZ%z4Mt4UY=7L6?jSanGsS",
                api_c.GOOGLE_REFRESH_TOKEN: "Z8BOWqt^PKVVNl&uOoQcL7",
                api_c.GOOGLE_CLIENT_CUSTOMER_ID: "527-056-0438",
                api_c.GOOGLE_CLIENT_ID: "ChM263kbF!f.apps.googleusercontent.com",
                api_c.GOOGLE_CLIENT_SECRET: "Gbh+@gUzVc658Ry=6kgw@_Bx",
            },
        }

        response = self.app.post(
            f"{t_c.BASE_ENDPOINT}{api_c.DESTINATIONS_ENDPOINT}/validate",
            json=validation_details,
            headers=t_c.STANDARD_HEADERS,
        )

        validation_succeeded = {
            "message": api_c.DESTINATION_AUTHENTICATION_SUCCESS,
        }

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(validation_succeeded, response.json)

    @patch(
        "huxunify.api.route.destination.GoogleConnector",
        **{"return_value.raiseError.side_effect": Exception()},
    )
    def test_validate_google_ads_credentials_failure_bad_credentials(
        self, mock_connector: MagicMock
    ):
        """Test failure to authenticate with qualtrics due to bad credentials.

        Args:
            mock_connector (MagicMock): MagicMock of the Qualtrics Connector.
        """

        # mocks the return value of the GoogleConnector Constructor
        mock_connector.side_effect = Exception("Test Exception")

        validation_details = {
            api_c.TYPE: db_c.DELIVERY_PLATFORM_GOOGLE,
            api_c.AUTHENTICATION_DETAILS: {
                api_c.GOOGLE_DEVELOPER_TOKEN: "dZ%z4Mt4UY=7L6?jSanGsS",
                api_c.GOOGLE_REFRESH_TOKEN: "Z8BOWqt^PKVVNl&uOoQcL7",
                api_c.GOOGLE_CLIENT_CUSTOMER_ID: "527-056-0438",
                api_c.GOOGLE_CLIENT_ID: "ChM263kbF!f.apps.googleusercontent.com",
                api_c.GOOGLE_CLIENT_SECRET: "Gbh+@gUzVc658Ry=6kgw@_Bx",
            },
        }

        response = self.app.post(
            f"{t_c.BASE_ENDPOINT}{api_c.DESTINATIONS_ENDPOINT}/validate",
            json=validation_details,
            headers=t_c.STANDARD_HEADERS,
        )

        validation_failed = {
            "message": api_c.DESTINATION_AUTHENTICATION_FAILED
        }

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual(validation_failed, response.json)

    # pylint: disable=unused-argument
    @patch(
        "huxunify.api.route.destination.QualtricsConnector",
        **{"return_value.raiseError.side_effect": Exception()},
    )
    def test_validate_qualtrics_credentials(self, mock_connector: MagicMock):
        """Test successful authentication with qualtrics.

        Args:
            mock_connector (MagicMock): MagicMock of the Qualtrics Connector.
        """

        validation_details = {
            api_c.TYPE: db_c.DELIVERY_PLATFORM_QUALTRICS,
            api_c.AUTHENTICATION_DETAILS: {
                api_c.QUALTRICS_API_TOKEN: "123456wqjhdq",
                api_c.QUALTRICS_DIRECTORY_ID: "eqjfd13289412",
                api_c.QUALTRICS_OWNER_ID: "fjndnqer812e821ue",
                api_c.QUALTRICS_DATA_CENTER: "data-center ",
            },
        }

        response = self.app.post(
            f"{t_c.BASE_ENDPOINT}{api_c.DESTINATIONS_ENDPOINT}/validate",
            json=validation_details,
            headers=t_c.STANDARD_HEADERS,
        )

        validation_succeeded = {
            "message": api_c.DESTINATION_AUTHENTICATION_SUCCESS,
        }

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(validation_succeeded, response.json)

    @patch(
        "huxunify.api.route.destination.QualtricsConnector",
        **{"return_value.raiseError.side_effect": Exception()},
    )
    def test_validate_qualtrics_credentials_failure_bad_credentials(
        self, mock_connector: MagicMock
    ):
        """Test failure to authenticate with qualtrics due to bad credentials.

        Args:
            mock_connector (MagicMock): MagicMock of the Qualtrics Connector.
        """

        # mocks the return value of the QualtricsConnector Constructor
        mock_connector.side_effect = Exception("Test Exception")

        validation_details = {
            api_c.TYPE: db_c.DELIVERY_PLATFORM_QUALTRICS,
            api_c.AUTHENTICATION_DETAILS: {
                api_c.QUALTRICS_API_TOKEN: "123456wqjhdq",
                api_c.QUALTRICS_DIRECTORY_ID: "eqjfd13289412",
                api_c.QUALTRICS_OWNER_ID: "fjndnqer812e821ue",
                api_c.QUALTRICS_DATA_CENTER: "data-center ",
            },
        }

        response = self.app.post(
            f"{t_c.BASE_ENDPOINT}{api_c.DESTINATIONS_ENDPOINT}/validate",
            json=validation_details,
            headers=t_c.STANDARD_HEADERS,
        )

        validation_failed = {
            "message": api_c.DESTINATION_AUTHENTICATION_FAILED
        }

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual(validation_failed, response.json)

    # pylint: disable=unused-argument
    @patch(
        "huxunify.api.route.destination.SFMCConnector",
        **{"return_value.raiseError.side_effect": Exception()},
    )
    def test_validate_sfmc_credentials(self, mock_connector: MagicMock):
        """Test successful authentication with sfmc.

        Args:
            mock_connector (MagicMock): MagicMock of the SFMC Connector.
        """

        validation_details = {
            "type": db_c.DELIVERY_PLATFORM_SFMC,
            "authentication_details": {
                "accountId": "123456",
                "sfmc_auth_base_uri": "some_url",
                "sfmc_client_id": "abcdefg",
                "sfmc_client_secret": "hijklmno",
                "sfmc_soap_base_uri": "some_url",
                "sfmc_rest_base_uri": "some_url",
            },
        }

        response = self.app.post(
            f"{t_c.BASE_ENDPOINT}{api_c.DESTINATIONS_ENDPOINT}/validate",
            json=validation_details,
            headers=t_c.STANDARD_HEADERS,
        )

        validation_succeeded = {
            "message": api_c.DESTINATION_AUTHENTICATION_SUCCESS,
            "perf_data_extensions": [],
        }

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(validation_succeeded, response.json)

    @patch(
        "huxunify.api.route.destination.SFMCConnector",
        **{"return_value.raiseError.side_effect": Exception()},
    )
    def test_validate_sfmc_credentials_failure_bad_credentials(
        self, mock_connector: MagicMock
    ):
        """Test failure to authenticate with sfmc due to bad credentials.

        Args:
            mock_connector (MagicMock): MagicMock of the SFMC Connector.
        """

        # mocks the return value of the SFMCConnector Constructor
        mock_connector.side_effect = Exception("Test Exception")

        validation_details = {
            "type": db_c.DELIVERY_PLATFORM_SFMC,
            "authentication_details": {
                "accountId": "123456",
                "sfmc_auth_base_uri": "some_url",
                "sfmc_client_id": "abcdefg",
                "sfmc_client_secret": "hijklmno",
                "sfmc_soap_base_uri": "some_url",
                "sfmc_rest_base_uri": "some_url",
            },
        }

        response = self.app.post(
            f"{t_c.BASE_ENDPOINT}{api_c.DESTINATIONS_ENDPOINT}/validate",
            json=validation_details,
            headers=t_c.STANDARD_HEADERS,
        )

        validation_failed = {
            "message": api_c.DESTINATION_AUTHENTICATION_FAILED
        }

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual(validation_failed, response.json)

    @mock.patch("huxunify.api.route.destination.SFMCConnector")
    def test_create_data_extension(self, mock_connector: MagicMock):
        """Test create data extension.

        Args:
            mock_connector (MagicMock): magic mock of SFMCConnector
        """

        mock_sfmc_instance = mock_connector.return_value
        mock_sfmc_instance.create_data_extension.return_value = {}

        destination_id = self.destinations[2][db_c.ID]

        data_extension = {"data_extension": "salesforce_data_ext_name"}

        response = self.app.post(
            f"{t_c.BASE_ENDPOINT}{api_c.DESTINATIONS_ENDPOINT}/{destination_id}/data-extensions",
            json=data_extension,
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.CREATED, response.status_code)

    def test_create_data_extension_invalid_id(self):
        """Test create data extension where id is invalid."""

        destination_id = "asdfg123456"

        data_extension = {"data_extension": "salesforce_data_ext_name"}

        response = self.app.post(
            f"{t_c.BASE_ENDPOINT}{api_c.DESTINATIONS_ENDPOINT}/{destination_id}/data-extensions",
            json=data_extension,
            headers=t_c.STANDARD_HEADERS,
        )

        valid_response = {"message": api_c.BSON_INVALID_ID(destination_id)}

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual(valid_response, response.json)

    def test_create_data_extension_destination_not_found(self):
        """Test create data extension where id is invalid."""

        destination_id = ObjectId()

        data_extension = {"data_extension": "salesforce_data_ext_name"}

        response = self.app.post(
            f"{t_c.BASE_ENDPOINT}{api_c.DESTINATIONS_ENDPOINT}/{destination_id}/data-extensions",
            json=data_extension,
            headers=t_c.STANDARD_HEADERS,
        )

        valid_response = {"message": api_c.DESTINATION_NOT_FOUND}

        self.assertEqual(HTTPStatus.NOT_FOUND, response.status_code)
        self.assertEqual(valid_response, response.json)

    @mock.patch("huxunify.api.route.destination.SFMCConnector")
    def test_retrieve_ordered_destination_data_extensions(
        self, mock_sfmc: MagicMock
    ):
        """Test retrieve destination data extensions.

        Args:
            mock_sfmc (MagicMock): magic mock of SFMCConnector.
        """

        return_value = [
            {
                api_c.SFMC_DATA_EXTENSION_NAME: "extension_name",
                api_c.SFMC_CUSTOMER_KEY: "id12345",
                "createdDate": datetime.strptime(
                    "2021-10-19 00:10:20.345", "%Y-%m-%d %H:%M:%S.%f"
                ),
            },
            {
                api_c.SFMC_DATA_EXTENSION_NAME: "data_extension_name",
                api_c.SFMC_CUSTOMER_KEY: "id12345678",
                "createdDate": datetime.strptime(
                    "2021-10-09 00:10:20.345", "%Y-%m-%d %H:%M:%S.%f"
                ),
            },
        ]
        mock_sfmc_instance = mock_sfmc.return_value
        mock_sfmc_instance.get_list_of_data_extensions.return_value = (
            return_value
        )

        expected_response = sorted(
            DestinationDataExtGetSchema().dump(return_value, many=True),
            key=lambda i: i[db_c.CREATE_TIME],
            reverse=True,
        )
        destination_id = self.destinations[2][db_c.ID]

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.DESTINATIONS_ENDPOINT}/{destination_id}/data-extensions",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        for idx, data_extension in enumerate(response.json):
            self.assertEqual(
                data_extension[api_c.NAME], expected_response[idx][api_c.NAME]
            )
            self.assertEqual(
                data_extension[api_c.DATA_EXTENSION_ID],
                expected_response[idx][api_c.DATA_EXTENSION_ID],
            )
            self.assertEqual(
                data_extension[db_c.CREATE_TIME],
                expected_response[idx][db_c.CREATE_TIME],
            )

    @mock.patch("huxunify.api.route.destination.SFMCConnector")
    def test_retrieve_empty_destination_data_extensions(
        self, mock_sfmc: MagicMock
    ):
        """Test retrieve destination data extensions.

        Args:
            mock_sfmc (MagicMock): magic mock of SFMCConnector.
        """

        return_value = []
        mock_sfmc_instance = mock_sfmc.return_value
        mock_sfmc_instance.get_list_of_data_extensions.return_value = (
            return_value
        )

        destination_id = self.destinations[2][db_c.ID]

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.DESTINATIONS_ENDPOINT}/{destination_id}/data-extensions",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(response.json, [])

    def test_retrieve_destination_data_extensions_invalid_id(self):
        """Test create data extension where id is invalid."""

        destination_id = "asdfg123456"

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.DESTINATIONS_ENDPOINT}/{destination_id}/data-extensions",
            headers=t_c.STANDARD_HEADERS,
        )

        valid_response = {"message": api_c.BSON_INVALID_ID(destination_id)}

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual(valid_response, response.json)

    def test_retrieve_destination_data_extensions_destination_not_found(self):
        """Test create data extension where id is invalid."""

        destination_id = ObjectId()

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.DESTINATIONS_ENDPOINT}/{destination_id}/data-extensions",
            headers=t_c.STANDARD_HEADERS,
        )

        valid_response = {"message": api_c.DESTINATION_NOT_FOUND}

        self.assertEqual(HTTPStatus.NOT_FOUND, response.status_code)
        self.assertEqual(valid_response, response.json)

    def test_patch_destination(self):
        """Test patch destination."""

        # get destination ID
        destination_id = self.destinations[0][db_c.ID]

        # get from database
        destination = destination_management.get_delivery_platform(
            self.database, self.destinations[0][db_c.ID]
        )

        # validate enabled flag
        self.assertFalse(destination.get(db_c.ENABLED))

        # patch destination
        self.assertTrue(
            HTTPStatus.OK,
            self.app.patch(
                f"{t_c.BASE_ENDPOINT}{api_c.DESTINATIONS_ENDPOINT}/{destination_id}",
                json={db_c.ENABLED: not destination.get(db_c.ENABLED)},
                headers=t_c.STANDARD_HEADERS,
            ).status_code,
        )

        # grab from database again and check update flag to True.
        destination = destination_management.get_delivery_platform(
            self.database, self.destinations[0][db_c.ID]
        )
        self.assertTrue(destination[db_c.ENABLED])

    def test_delete_destination(self):
        """Test delete destination"""

        # get destination ID
        destination_id = self.destinations[0][db_c.ID]

        response = self.app.delete(
            f"{t_c.BASE_ENDPOINT}{api_c.DESTINATIONS_ENDPOINT}/{destination_id}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.NO_CONTENT, response.status_code)

    def test_delete_destination_(self):
        """Test delete destination"""

        # get destination ID
        destination_id = ObjectId()

        response = self.app.delete(
            f"{t_c.BASE_ENDPOINT}{api_c.DESTINATIONS_ENDPOINT}/{destination_id}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.NO_CONTENT, response.status_code)
