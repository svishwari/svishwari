# pylint: disable=too-many-lines
"""Purpose of this file is to house all the destination api tests."""
from datetime import datetime
from unittest import mock
from unittest.mock import MagicMock, patch
from http import HTTPStatus

from bson import ObjectId

from huxunifylib.connectors import FacebookConnector

from huxunifylib.database import (
    delivery_platform_management as destination_management,
    collection_management,
    constants as db_c,
)
from huxunifylib.database.orchestration_management import (
    create_audience,
    get_audience,
)
from huxunifylib.database.engagement_management import (
    set_engagement,
    get_engagement,
)
import huxunify.test.constants as t_c
from huxunify.test.route.route_test_util.route_test_case import RouteTestCase
from huxunify.api.data_connectors.cloud.cloud_client import CloudClient
from huxunify.api.schema.destinations import (
    DestinationDataExtGetSchema,
    DestinationGetSchema,
)
from huxunify.api import constants as api_c


# pylint: disable=too-many-public-methods
class TestDestinationRoutes(RouteTestCase):
    """Test Destination Routes."""

    def setUp(self) -> None:
        """Setup resources before each test."""

        super().setUp()
        self.load_test_data(self.database)

        self.new_auth_details = {
            api_c.AUTHENTICATION_DETAILS: {
                api_c.FACEBOOK_ACCESS_TOKEN: "fake_fake",
                api_c.FACEBOOK_APP_SECRET: "fake",
                api_c.FACEBOOK_APP_ID: "1234",
                api_c.FACEBOOK_AD_ACCOUNT_ID: "12345678",
            }
        }

        # mock get db client from destinations
        mock.patch(
            "huxunify.api.route.destination.get_db_client",
            return_value=self.database,
        ).start()

        for subclass in CloudClient.__subclasses__():
            # mock parameter store store secret
            mock.patch.object(subclass, "set_secret").start()

            # mock parameter store get store value
            mock.patch.object(
                subclass, "get_secret", return_value="secret"
            ).start()

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

    def test_get_all_destinations_refresh_all(self):
        """Test get all destinations with refresh all."""

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.DESTINATIONS_ENDPOINT}",
            query_string={api_c.DESTINATION_REFRESH: True},
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
    def test_request_existing_destination(
        self, jira_class_init, jira_create_issue_mock
    ):
        """Test request existing destination.

        Args:
            jira_class_init (MagicMock): Mock creating jira class.
            jira_create_issue_mock (MagicMock): Mock creating jira issue.
        """

        new_destination_request = {
            api_c.NAME: "test_destinaion_1",
            api_c.CONTACT_EMAIL: "test_email@gmail.com",
            api_c.CLIENT_REQUEST: True,
            api_c.CLIENT_ACCOUNT: True,
            api_c.USE_CASE: "Testing",
        }

        jira_class_init.return_value = None
        jira_create_issue_mock.return_value = {db_c.CONSTANT_KEY: ""}
        # Request new destination.
        self.app.post(
            f"{t_c.BASE_ENDPOINT}{api_c.DESTINATIONS_ENDPOINT}/request",
            headers=t_c.STANDARD_HEADERS,
            json=new_destination_request,
        )

        # Re-request destination.
        response = self.app.post(
            f"{t_c.BASE_ENDPOINT}{api_c.DESTINATIONS_ENDPOINT}/request",
            headers=t_c.STANDARD_HEADERS,
            json=new_destination_request,
        )

        self.assertEqual(HTTPStatus.CONFLICT, response.status_code)
        self.assertEqual(
            "Destination already present.", response.json[api_c.MESSAGE]
        )

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
        for destination in response.json:
            self.assertEqual({}, DestinationGetSchema().validate(destination))

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

        valid_response = {api_c.MESSAGE: api_c.DESTINATION_NOT_FOUND}

        self.assertEqual(valid_response, response.json)
        self.assertEqual(HTTPStatus.NOT_FOUND, response.status_code)

    def test_get_destination_invalid_object_id(self):
        """Test get destination with an invalid ObjectID."""

        destination_id = "asdfgh2345"

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.DESTINATIONS_ENDPOINT}/{destination_id}",
            headers=t_c.STANDARD_HEADERS,
        )

        valid_response = {api_c.MESSAGE: api_c.BSON_INVALID_ID(destination_id)}

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

    def test_update_destination_with_no_destination_link(self):
        """Test update destination with no destination link."""

        destination_id = self.destinations[0][db_c.ID]
        input_json = self.new_auth_details
        input_json[db_c.LINK] = None

        response = self.app.put(
            f"{t_c.BASE_ENDPOINT}{api_c.DESTINATIONS_ENDPOINT}"
            f"/{destination_id}/{api_c.AUTHENTICATION}",
            json=input_json,
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
            api_c.MESSAGE: api_c.DESTINATION_AUTHENTICATION_SUCCESS
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
            api_c.MESSAGE: api_c.DESTINATION_AUTHENTICATION_FAILED
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
            api_c.MESSAGE: api_c.DESTINATION_AUTHENTICATION_SUCCESS,
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
            api_c.MESSAGE: api_c.DESTINATION_AUTHENTICATION_FAILED
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
            api_c.MESSAGE: api_c.DESTINATION_AUTHENTICATION_SUCCESS,
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
            api_c.MESSAGE: api_c.DESTINATION_AUTHENTICATION_FAILED
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
            api_c.MESSAGE: api_c.DESTINATION_AUTHENTICATION_SUCCESS,
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
            api_c.MESSAGE: api_c.DESTINATION_AUTHENTICATION_FAILED
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
            api_c.MESSAGE: api_c.DESTINATION_AUTHENTICATION_SUCCESS,
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
            api_c.MESSAGE: api_c.DESTINATION_AUTHENTICATION_FAILED
        }

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual(validation_failed, response.json)

    @mock.patch("huxunify.api.route.destination.SFMCConnector")
    def test_create_data_extension(self, mock_connector: MagicMock):
        """Test create data extension.

        Args:
            mock_connector (MagicMock): magic mock of SFMCConnector
        """

        extension_name = "salesforce_data_ext_name"

        mock_sfmc_instance = mock_connector.return_value
        # TODO HUS-1909 this value should be updated to accurately
        # TODO reflect a return value from orch
        mock_sfmc_instance.create_data_extension.return_value = {
            api_c.NAME: extension_name,
            "data_extension_id": "some_id",
        }

        destination_id = self.destinations[2][db_c.ID]

        data_extension = {"data_extension": extension_name}

        response = self.app.post(
            f"{t_c.BASE_ENDPOINT}{api_c.DESTINATIONS_ENDPOINT}/{destination_id}/data-extensions",
            json=data_extension,
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.CREATED, response.status_code)
        # TODO HUS-1909 this check should succeed after schema is corrected
        # self.assertEqual("salesforce_data_ext_name", response.json[api_c.NAME])

    def test_create_data_extension_invalid_id(self):
        """Test create data extension where id is invalid."""

        destination_id = "asdfg123456"

        data_extension = {"data_extension": "salesforce_data_ext_name"}

        response = self.app.post(
            f"{t_c.BASE_ENDPOINT}{api_c.DESTINATIONS_ENDPOINT}/{destination_id}/data-extensions",
            json=data_extension,
            headers=t_c.STANDARD_HEADERS,
        )

        valid_response = {api_c.MESSAGE: api_c.BSON_INVALID_ID(destination_id)}

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

        valid_response = {api_c.MESSAGE: api_c.DESTINATION_NOT_FOUND}

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
                api_c.SFMC_DATA_EXTENSION_NAME: "data_extension_name_2",
                api_c.SFMC_CUSTOMER_KEY: "id12345",
                "createdDate": datetime.strptime(
                    "2021-10-19 00:10:20.345", "%Y-%m-%d %H:%M:%S.%f"
                ),
            },
            {
                api_c.SFMC_DATA_EXTENSION_NAME: "data_extension_name_3",
                api_c.SFMC_CUSTOMER_KEY: "id123456",
                "createdDate": datetime.strptime(
                    "2021-10-25 00:10:20.345", "%Y-%m-%d %H:%M:%S.%f"
                ),
            },
            {
                api_c.SFMC_DATA_EXTENSION_NAME: "data_extension_name_1",
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

        destination_id = t_c.INVALID_ID

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.DESTINATIONS_ENDPOINT}/{destination_id}/data-extensions",
            headers=t_c.STANDARD_HEADERS,
        )

        valid_response = {api_c.MESSAGE: api_c.BSON_INVALID_ID(destination_id)}

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual(valid_response, response.json)

    def test_retrieve_destination_data_extensions_destination_not_found(self):
        """Test create data extension where id is invalid."""

        destination_id = ObjectId()

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.DESTINATIONS_ENDPOINT}/{destination_id}/data-extensions",
            headers=t_c.STANDARD_HEADERS,
        )

        valid_response = {api_c.MESSAGE: api_c.DESTINATION_NOT_FOUND}

        self.assertEqual(HTTPStatus.NOT_FOUND, response.status_code)
        self.assertEqual(valid_response, response.json)

    def test_patch_destination_set_enabled(self):
        """Test patch destination set the field to be enabled."""

        # get destination ID
        destination = destination_management.get_delivery_platform_by_type(
            self.database, db_c.DELIVERY_PLATFORM_FACEBOOK
        )

        # validate enabled flag
        self.assertTrue(destination.get(db_c.ENABLED))

        response = self.app.patch(
            f"{t_c.BASE_ENDPOINT}{api_c.DESTINATIONS_ENDPOINT}/{destination[db_c.ID]}",
            json={db_c.ENABLED: not destination.get(db_c.ENABLED)},
            headers=t_c.STANDARD_HEADERS,
        )

        # patch destination
        self.assertTrue(HTTPStatus.OK, response.status_code)

        # grab from database again
        destination = destination_management.get_delivery_platform(
            self.database, self.destinations[0][db_c.ID]
        )
        # confirm db entry
        self.assertFalse(destination[db_c.ENABLED])
        # field should not be sent in API
        self.assertNotIn(db_c.ENABLED, response.json)

    def test_patch_destination_set_new_link(self):
        """Test patch destination edit the link field."""

        # get destination ID
        destination = destination_management.get_delivery_platform_by_type(
            self.database, db_c.DELIVERY_PLATFORM_FACEBOOK
        )
        new_link = "https://www.new-link.com/login"

        # patch destination
        response = self.app.patch(
            f"{t_c.BASE_ENDPOINT}{api_c.DESTINATIONS_ENDPOINT}/{destination[db_c.ID]}",
            json={db_c.LINK: new_link},
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)

        # grab from database again to confirm
        destination = destination_management.get_delivery_platform(
            self.database, destination[db_c.ID]
        )
        # confirm db entry
        self.assertEqual(new_link, destination[db_c.LINK])
        # confirm return value from api
        self.assertEqual(new_link, response.json[db_c.LINK])

    def test_patch_destination_no_body(self):
        """Test patch destination where no body is provided."""

        # get destination ID
        destination = destination_management.get_delivery_platform_by_type(
            self.database, db_c.DELIVERY_PLATFORM_FACEBOOK
        )

        # patch destination
        self.assertTrue(
            HTTPStatus.BAD_REQUEST,
            self.app.patch(
                f"{t_c.BASE_ENDPOINT}{api_c.DESTINATIONS_ENDPOINT}/{destination[db_c.ID]}",
                json={},
                headers=t_c.STANDARD_HEADERS,
            ).status_code,
        )

    def test_patch_destination_removed(self):
        """Test patch destination added = False."""

        # get destination ID
        destination_id = self.destinations[0][db_c.ID]

        # create audience
        audience = create_audience(
            self.database,
            "Audience for Destination Removal",
            [],
            "test user",
            [{api_c.ID: destination_id}],
            100,
        )

        audiences = [
            {
                api_c.ID: audience[db_c.ID],
                api_c.DESTINATIONS: [
                    {
                        api_c.ID: destination_id,
                    },
                ],
            }
        ]

        # test engagement to ensure the destination exists
        engagement = get_engagement(
            self.database,
            set_engagement(
                self.database,
                "Test engagement",
                None,
                audiences,
                t_c.TEST_USER_NAME,
                None,
                False,
            ),
        )

        # test to ensure the destination is assigned to the engagement.
        self.assertTrue(
            [
                a
                for x in engagement.get(db_c.AUDIENCES)
                for a in x.get(db_c.DESTINATIONS)
                if a.get(db_c.OBJECT_ID) == destination_id
            ]
        )

        # test to ensure the destination is assigned to the audience
        self.assertTrue(
            [
                d
                for d in audience.get(db_c.DESTINATIONS)
                if d.get(db_c.OBJECT_ID) == destination_id
            ]
        )

        # patch destination
        self.assertTrue(
            HTTPStatus.OK,
            self.app.patch(
                f"{t_c.BASE_ENDPOINT}{api_c.DESTINATIONS_ENDPOINT}/{destination_id}",
                json={db_c.ADDED: False},
                headers=t_c.STANDARD_HEADERS,
            ).status_code,
        )

        # validate the destination was removed from any engagements.
        # test engagement to ensure the destination exists
        updated_engagement = get_engagement(
            self.database, engagement.get(db_c.ID)
        )

        # test to ensure the destination is removed from the engagement.
        self.assertFalse(
            [
                a
                for x in updated_engagement.get(db_c.AUDIENCES)
                for a in x.get(db_c.DESTINATIONS)
                if a.get(db_c.OBJECT_ID) == destination_id
            ]
        )

        # validate the destination was removed from any audiences
        # test audience to ensure the destination exists
        updated_audience = get_audience(self.database, audience.get(db_c.ID))

        # test to ensure the destination is removed from the audience
        self.assertFalse(
            [
                d
                for d in updated_audience.get(db_c.DESTINATIONS)
                if d.get(db_c.OBJECT_ID) == destination_id
            ]
        )

    def test_delete_destination(self):
        """Test delete destination"""

        # get destination ID
        destination_id = self.destinations[0][db_c.ID]

        response = self.app.delete(
            f"{t_c.BASE_ENDPOINT}{api_c.DESTINATIONS_ENDPOINT}/{destination_id}",
            headers=t_c.STANDARD_HEADERS,
        )
        destination = destination_management.get_delivery_platform(
            self.database, destination_id
        )

        self.assertEqual(HTTPStatus.NO_CONTENT, response.status_code)
        self.assertIsNone(destination)

    def test_delete_destination_where_destination_does_not_exist(self):
        """Test delete destination where destination does not exist"""

        # get destination ID
        destination_id = ObjectId()

        response = self.app.delete(
            f"{t_c.BASE_ENDPOINT}{api_c.DESTINATIONS_ENDPOINT}/{destination_id}",
            headers=t_c.STANDARD_HEADERS,
        )
        destination = destination_management.get_delivery_platform(
            self.database, destination_id
        )

        self.assertEqual(HTTPStatus.NO_CONTENT, response.status_code)
        self.assertIsNone(destination)
