"""
Purpose of this file is to house all the destination api tests
"""

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
)
import huxunify.test.constants as t_c
from huxunify.api.data_connectors.aws import parameter_store
from huxunify.api import constants as api_c
from huxunify.app import create_app


# pylint: disable=too-many-public-methods
class TestDestinationRoutes(TestCase):
    """Test Destination Routes"""

    def setUp(self) -> None:
        """
        Setup resources before each test

        Args:

        Returns:
        """

        # mock request for introspect call
        request_mocker = requests_mock.Mocker()
        request_mocker.post(t_c.INTROSPECT_CALL, json=t_c.VALID_RESPONSE)
        request_mocker.get(t_c.USER_INFO_CALL, json=t_c.VALID_USER_RESPONSE)
        request_mocker.start()

        self.app = create_app().test_client()

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
        """
        Test get all destinations

        Returns:

        """
        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.DESTINATIONS_ENDPOINT}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(len(self.destinations), len(response.json))

    def test_get_destination_with_valid_id(self):
        """
        Test get destination with valid id

        Returns:

        """
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
        """
        Test get destination with a valid id that is not in the db

        Returns:

        """
        destination_id = ObjectId()

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.DESTINATIONS_ENDPOINT}/{destination_id}",
            headers=t_c.STANDARD_HEADERS,
        )

        valid_response = {"message": api_c.DESTINATION_NOT_FOUND}

        self.assertEqual(valid_response, response.json)
        self.assertEqual(HTTPStatus.NOT_FOUND, response.status_code)

    def test_get_destination_invalid_object_id(self):
        """
        Test get destination with an invalid ObjectID

        Returns:

        """
        destination_id = "asdfgh2345"

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.DESTINATIONS_ENDPOINT}/{destination_id}",
            headers=t_c.STANDARD_HEADERS,
        )

        valid_response = {"message": api_c.BSON_INVALID_ID(destination_id)}

        self.assertEqual(valid_response, response.json)
        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)

    def test_update_destination(self):
        """
        Test update destination

        Returns:

        """
        destination_id = self.destinations[0][db_c.ID]

        new_auth_details = {
            "authentication_details": {
                api_c.FACEBOOK_ACCESS_TOKEN: "MkU3Ojgwm",
                api_c.FACEBOOK_APP_SECRET: "unified_fb_secret",
                api_c.FACEBOOK_APP_ID: "2951925002021888",
                api_c.FACEBOOK_AD_ACCOUNT_ID: "111333777",
            }
        }

        response = self.app.put(
            f"{t_c.BASE_ENDPOINT}{api_c.DESTINATIONS_ENDPOINT}/{destination_id}",
            json=new_auth_details,
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)

    def test_update_destination_where_destination_not_found(self):
        """
        Test update destination where no destination is found

        Returns:

        """
        destination_id = ObjectId()

        new_auth_details = {
            "authentication_details": {
                "access_token": "MkU3Ojgwm",
                "app_secret": "717bdOQqZO99",
                "app_id": "2951925002021888",
                "ad_account_id": "111333777",
            }
        }

        response = self.app.put(
            f"{t_c.BASE_ENDPOINT}{api_c.DESTINATIONS_ENDPOINT}/{destination_id}",
            json=new_auth_details,
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.NOT_FOUND, response.status_code)

    def test_update_destination_invalid_object_id(self):
        """
        Test update destination where invalid id given

        Returns:

        """
        destination_id = "asdfg1234"

        new_auth_details = {
            "authentication_details": {
                "access_token": "MkU3Ojgwm",
                "app_secret": "717bdOQqZO99",
                "app_id": "2951925002021888",
                "ad_account_id": "111333777",
            }
        }

        response = self.app.put(
            f"{t_c.BASE_ENDPOINT}{api_c.DESTINATIONS_ENDPOINT}/{destination_id}",
            json=new_auth_details,
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)

    def test_retrieve_destinations_constants(self):
        """
        Test retrieve all destination constants

        Returns:

        """

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.DESTINATIONS_ENDPOINT}/constants",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIn(db_c.DELIVERY_PLATFORM_FACEBOOK, response.json)
        self.assertIn(db_c.DELIVERY_PLATFORM_SFMC, response.json)
        self.assertIn(db_c.DELIVERY_PLATFORM_TWILIO, response.json)

    def test_validate_facebook_credentials(self):
        """
        Test validation of facebook credentials

        Returns:

        """

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
        """
        Test failure to authenticate with facebook due to bad credentials

        Args:
            mock_connector (MagicMock): MagicMock of the Facebook Connector

        Returns:

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

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual(validation_failed, response.json)

    # pylint: disable=unused-argument
    @patch(
        "huxunify.api.route.destination.TwilioConnector",
        **{"return_value.raiseError.side_effect": Exception()},
    )
    def test_validate_twilio_credentials(self, mock_connector: MagicMock):
        """
        Test successful authentication with twilio

        Args:
            mock_connector (MagicMock): MagicMock of the Twilio Connector

        Returns:
        """

        validation_details = {
            api_c.TYPE: db_c.DELIVERY_PLATFORM_TWILIO,
            api_c.AUTHENTICATION_DETAILS: {
                api_c.TWILIO_AUTH_TOKEN: "123456",
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
        "huxunify.api.route.destination.TwilioConnector",
        **{"return_value.raiseError.side_effect": Exception()},
    )
    def test_validate_twilio_credentials_failure_bad_credentials(
        self, mock_connector: MagicMock
    ):
        """
        Test failure to authenticate with twilio due to bad credentials

        Args:
            mock_connector (MagicMock): MagicMock of the Twilio Connector

        Returns:

        """

        # mocks the return value of the TwilioConnector Constructor
        mock_connector.side_effect = Exception("Test Exception")

        validation_details = {
            api_c.TYPE: db_c.DELIVERY_PLATFORM_TWILIO,
            api_c.AUTHENTICATION_DETAILS: {
                api_c.TWILIO_AUTH_TOKEN: "123456",
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
        """
        Test successful authentication with sfmc

        Args:
            mock_connector (MagicMock): MagicMock of the SFMC Connector

        Returns:

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
        """
        Test failure to authenticate with sfmc due to bad credentials

        Args:
            mock_connector (MagicMock): MagicMock of the SFMC Connector

        Returns:

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
        """
        Test create data extension

        Args:
            mock_connector (MagicMock): magic mock of SFMCConnector

        Returns:

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
        """
        Test create data extension where id is invalid

        Args:

        Returns:

        """

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
        """
        Test create data extension where id is invalid

        Args:

        Returns:

        """

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
        """
        Test retrieve destination data extensions

        Args:
            mock_sfmc (MagicMock): magic mock of SFMCConnector

        Returns:

        """

        return_value = [
            {
                api_c.SFMC_DATA_EXTENSION_NAME: "extension_name",
                api_c.SFMC_CUSTOMER_KEY: "id12345",
            },
            {
                api_c.SFMC_DATA_EXTENSION_NAME: "data_extension_name",
                api_c.SFMC_CUSTOMER_KEY: "id12345678",
            },
        ]
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
        self.assertEqual(response.json[0][api_c.NAME], "data_extension_name")
        self.assertEqual(
            response.json[0][api_c.DATA_EXTENSION_ID], "id12345678"
        )

    @mock.patch("huxunify.api.route.destination.SFMCConnector")
    def test_retrieve_empty_destination_data_extensions(
        self, mock_sfmc: MagicMock
    ):
        """
        Test retrieve destination data extensions

        Args:
            mock_sfmc (MagicMock): magic mock of SFMCConnector

        Returns:

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
        """
        Test create data extension where id is invalid

        Args:

        Returns:

        """

        destination_id = "asdfg123456"

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.DESTINATIONS_ENDPOINT}/{destination_id}/data-extensions",
            headers=t_c.STANDARD_HEADERS,
        )

        valid_response = {"message": api_c.BSON_INVALID_ID(destination_id)}

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual(valid_response, response.json)

    def test_retrieve_destination_data_extensions_destination_not_found(self):
        """
        Test create data extension where id is invalid

        Args:

        Returns:

        """

        destination_id = ObjectId()

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.DESTINATIONS_ENDPOINT}/{destination_id}/data-extensions",
            headers=t_c.STANDARD_HEADERS,
        )

        valid_response = {"message": api_c.DESTINATION_NOT_FOUND}

        self.assertEqual(HTTPStatus.NOT_FOUND, response.status_code)
        self.assertEqual(valid_response, response.json)
