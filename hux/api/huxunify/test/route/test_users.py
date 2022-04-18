# pylint: disable=too-many-lines,too-many-public-methods
"""Purpose of this file is to house all the engagement API tests."""
from unittest import mock
from unittest.mock import MagicMock
from http import HTTPStatus

import requests_mock
from bson import ObjectId

from huxunifylib.database import constants as db_c
from huxunifylib.database.delivery_platform_management import (
    set_delivery_platform,
)
from huxunifylib.database.engagement_management import set_engagement
from huxunifylib.database.orchestration_management import create_audience
from huxunifylib.database.user_management import get_user

from huxunify.api import constants as api_c
from huxunify.api.route.utils import get_user_favorites
from huxunify.api.schema.user import UserSchema
from huxunify.test.route.route_test_util.route_test_case import RouteTestCase
import huxunify.test.constants as t_c


class TestUserRoutes(RouteTestCase):
    """Tests for User APIs."""

    def setUp(self) -> None:
        """Setup resources before each test."""

        super().setUp()
        self.load_test_data(self.database)

        # mock get_db_client() in users
        mock.patch(
            "huxunify.api.route.user.get_db_client",
            return_value=self.database,
        ).start()

        self.audience_id = create_audience(
            self.database,
            "Test Audience",
            [],
            t_c.VALID_USER_RESPONSE[api_c.NAME],
        )[db_c.ID]
        self.delivery_platform = set_delivery_platform(
            self.database,
            db_c.DELIVERY_PLATFORM_FACEBOOK,
            "facebook_delivery_platform",
            authentication_details={},
            status=db_c.STATUS_SUCCEEDED,
        )
        self.audiences = [
            {
                api_c.ID: self.audience_id,
                api_c.DESTINATIONS: [
                    {
                        api_c.ID: self.delivery_platform[db_c.ID],
                    },
                ],
            }
        ]
        self.engagement_id = set_engagement(
            self.database,
            "Test engagement",
            None,
            self.audiences,
            "Felix Hernandez",
            None,
            False,
        )

        # write a user to the database
        self.user_info = get_user(
            self.database,
            okta_id=t_c.VALID_USER_RESPONSE[api_c.OKTA_ID_SUB],
        )

    def test_adding_engagement_to_favorite(self):
        """Tests adding engagement as a user favorite."""

        endpoint = (
            f"{t_c.BASE_ENDPOINT}"
            f"{api_c.USER_ENDPOINT}/"
            f"{db_c.ENGAGEMENTS}/"
            f"{self.engagement_id}/"
            f"{api_c.FAVORITE}"
        )

        response = self.app.post(
            endpoint,
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(api_c.OPERATION_SUCCESS, response.json.get("message"))
        self.assertEqual(HTTPStatus.CREATED, response.status_code)

    def test_adding_audience_to_favorite(self):
        """Tests adding audience as a user favorite."""

        endpoint = (
            f"{t_c.BASE_ENDPOINT}"
            f"{api_c.USER_ENDPOINT}/"
            f"{db_c.AUDIENCES}/"
            f"{self.audience_id}/"
            f"{api_c.FAVORITE}"
        )

        response = self.app.post(
            endpoint,
            headers=t_c.STANDARD_HEADERS,
        )
        self.assertEqual(api_c.OPERATION_SUCCESS, response.json.get("message"))
        self.assertEqual(HTTPStatus.CREATED, response.status_code)

    def test_adding_DNE_audience_to_favorite(self):
        """Tests adding invalid audience as a user favorite.
        Testing by sending audience_id not in DB, here using engagement ID.
        """

        audience_id = ObjectId()

        endpoint = (
            f"{t_c.BASE_ENDPOINT}"
            f"{api_c.USER_ENDPOINT}/"
            f"{db_c.AUDIENCES}/"
            f"{audience_id}/"
            f"{api_c.FAVORITE}"
        )

        response = self.app.post(
            endpoint,
            headers=t_c.STANDARD_HEADERS,
        )
        expected_response_message = (
            f"The ID <{audience_id}> does " f"not exist in the database!"
        )
        self.assertEqual(
            expected_response_message, response.json.get("message")
        )
        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)

    def test_deleting_DNE_audience_from_favorite(self):
        """Tests deleting DNE audience as a user favorite."""

        audience_id = ObjectId()

        endpoint = (
            f"{t_c.BASE_ENDPOINT}"
            f"{api_c.USER_ENDPOINT}/"
            f"{db_c.AUDIENCES}/"
            f"{audience_id}/"
            f"{api_c.FAVORITE}"
        )

        response = self.app.delete(
            endpoint,
            headers=t_c.STANDARD_HEADERS,
        )
        self.assertEqual(HTTPStatus.OK, response.status_code)

    def test_deleting_audience_from_favorite(self):
        """Tests deleting/un-favorite an audience."""

        endpoint = (
            f"{t_c.BASE_ENDPOINT}"
            f"{api_c.USER_ENDPOINT}/"
            f"{db_c.AUDIENCES}/"
            f"{self.audience_id}/"
            f"{api_c.FAVORITE}"
        )

        # Add the audience as favorite first
        self.app.post(
            endpoint,
            headers=t_c.STANDARD_HEADERS,
        )

        response = self.app.delete(
            endpoint,
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(api_c.OPERATION_SUCCESS, response.json.get("message"))
        self.assertEqual(HTTPStatus.OK, response.status_code)

    def test_deleting_audience_not_in_favorite(self):
        """Tests deleting/un-favorite an audience not in favorites."""

        endpoint = (
            f"{t_c.BASE_ENDPOINT}"
            f"{api_c.USER_ENDPOINT}/"
            f"{db_c.AUDIENCES}/"
            f"{self.audience_id}/"
            f"{api_c.FAVORITE}"
        )

        response = self.app.delete(
            endpoint,
            headers=t_c.STANDARD_HEADERS,
        )

        expected_response_message = (
            f"{self.audience_id} not part of user " f"favorites"
        )
        self.assertEqual(
            expected_response_message, response.json.get("message")
        )

    def test_get_user_profile_success(self):
        """Test success response of getting user profile using Okta ID."""

        endpoint = f"{t_c.BASE_ENDPOINT}{api_c.USER_ENDPOINT}/{api_c.PROFILE}"

        response = self.app.get(
            endpoint,
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        t_c.validate_schema(UserSchema(), response.json)
        self.assertIn(db_c.AUDIENCES, response.json[db_c.USER_FAVORITES])

    def test_get_all_users(self):
        """Tests getting all users."""

        endpoint = f"{t_c.BASE_ENDPOINT}" f"{api_c.USER_ENDPOINT}"

        response = self.app.get(
            endpoint,
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        t_c.validate_schema(UserSchema(), response.json, True)

    def test_get_user_profile_bad_request_failure(self):
        """Test 400 response of getting user profile using Okta ID."""

        # mock invalid request for introspect call
        request_mocker = requests_mock.Mocker()
        request_mocker.post(
            t_c.INTROSPECT_CALL, json=t_c.INVALID_INTROSPECTION_RESPONSE
        )
        request_mocker.start()

        endpoint = f"{t_c.BASE_ENDPOINT}{api_c.USER_ENDPOINT}/{api_c.PROFILE}"

        response = self.app.get(
            endpoint,
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)

    def test_get_user_profile_not_found_failure(self):
        """Test 404 response of getting user profile using Okta ID."""

        incorrect_okta_response = {
            "active": True,
            "username": "john smith",
            "uid": "12345678",
        }

        user_response = {
            api_c.OKTA_ID_SUB: "12345678",
            api_c.EMAIL: "johnsmith@fake.com",
            api_c.NAME: "john smith",
            api_c.ROLE: "admin",
            api_c.USER_PII_ACCESS: True,
        }

        # mock incorrect request for introspect call so that the user is not
        # present in mock DB
        request_mocker = requests_mock.Mocker()
        request_mocker.post(t_c.INTROSPECT_CALL, json=incorrect_okta_response)
        request_mocker.get(t_c.USER_INFO_CALL, json=user_response)
        request_mocker.start()

        mock.patch(
            "huxunify.api.route.utils.set_user",
            return_value=None,
        ).start()

        endpoint = f"{t_c.BASE_ENDPOINT}{api_c.USER_ENDPOINT}/{api_c.PROFILE}"

        response = self.app.get(
            endpoint,
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.NOT_FOUND, response.status_code)
        self.assertEqual({api_c.MESSAGE: api_c.USER_NOT_FOUND}, response.json)

    def test_update_user(self):
        """Test successfully updating a user"""
        role = "admin"
        display_name = "NEW_DISPLAY_NAME"

        update_body = {
            db_c.USER_ROLE: role,
            db_c.USER_DISPLAY_NAME: display_name,
        }

        response = self.app.patch(
            f"{t_c.BASE_ENDPOINT}{api_c.USER_ENDPOINT}",
            headers=t_c.STANDARD_HEADERS,
            json=update_body,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(role, response.json[db_c.USER_ROLE])
        self.assertEqual(display_name, response.json[db_c.USER_DISPLAY_NAME])

    def test_update_different_user(self):
        """Test successfully updating a different user"""
        role = "admin"
        display_name = "NEW_DISPLAY_NAME"

        update_body = {
            api_c.ID: str(self.user_info[db_c.ID]),
            db_c.USER_ROLE: role,
            db_c.USER_DISPLAY_NAME: display_name,
        }

        response = self.app.patch(
            f"{t_c.BASE_ENDPOINT}{api_c.USER_ENDPOINT}",
            headers=t_c.STANDARD_HEADERS,
            json=update_body,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(role, response.json[db_c.USER_ROLE])
        self.assertEqual(display_name, response.json[db_c.USER_DISPLAY_NAME])

    def test_update_user_invalid_update_body(self):
        """Test successfully updating a user"""
        role = "admin"
        display_name = "NEW_DISPLAY_NAME"

        update_body = {"bad_field": role, db_c.USER_DISPLAY_NAME: display_name}

        response = self.app.patch(
            f"{t_c.BASE_ENDPOINT}{api_c.USER_ENDPOINT}",
            headers=t_c.STANDARD_HEADERS,
            json=update_body,
        )
        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)

    def test_get_user_favorites(self):
        """Test getting user favorites"""
        self.assertFalse(
            get_user_favorites(
                self.database,
                self.user_info[db_c.USER_DISPLAY_NAME],
                db_c.ENGAGEMENTS,
            )
        )

    def test_get_user_favorites_user_does_not_exist(self):
        """Test getting user favorites with a user that does not exist."""
        self.assertFalse(
            get_user_favorites(self.database, None, db_c.ENGAGEMENTS)
        )

    @mock.patch("huxunify.api.route.user.JiraConnection")
    def test_create_jira_issue(self, mock_jira: MagicMock):
        """Test jira issue creation.

        Args:
            mock_jira (MagicMock): magic mock of JiraConnection
        """

        reported_issue = {
            api_c.ISSUE_TYPE: api_c.TICKET_TYPE_BUG,
            api_c.SUMMARY: "Test creation of JIRA ticket",
            api_c.DESCRIPTION: "",
        }

        expected_response = reported_issue.copy()
        expected_response.update({api_c.ID: 1234, api_c.KEY: "ABC-123"})

        mock_jira_instance = mock_jira.return_value
        mock_jira_instance.create_jira_issue.return_value = expected_response

        response = self.app.post(
            f"{t_c.BASE_ENDPOINT}{api_c.USER_ENDPOINT}/{api_c.CONTACT_US}",
            json=reported_issue,
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.CREATED, response.status_code)
        self.assertDictEqual(expected_response, response.json)

    @mock.patch("huxunify.api.route.user.JiraConnection")
    def test_create_new_user_request(self, mock_jira: MagicMock):
        """Test new user request.

        Args:
            mock_jira (MagicMock): magic mock of JiraConnection
        """

        new_user_request = {
            api_c.FIRST_NAME: "Sarah",
            api_c.LAST_NAME: "Huxley",
            api_c.EMAIL: "sh@fake.com",
            api_c.USER_ACCESS_LEVEL: "admin",
            api_c.USER_PII_ACCESS: False,
            api_c.REASON_FOR_REQUEST: "na",
        }

        expected_response = {api_c.ID: 1234, api_c.KEY: "ABC-123"}

        mock_jira_instance = mock_jira.return_value
        mock_jira_instance.check_jira_connection.return_value = True
        mock_jira_instance.create_jira_issue.return_value = expected_response

        response = self.app.post(
            f"{t_c.BASE_ENDPOINT}{api_c.USER_ENDPOINT}/{api_c.REQUEST_NEW_USER}",
            json=new_user_request,
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.CREATED, response.status_code)
        self.assertDictEqual(expected_response, response.json)

    def test_update_user_notifications(self):
        """Test successfully updating a users notification preferences"""

        update_body = {
            api_c.ALERTS: {
                api_c.DATA_MANAGEMENT: {
                    api_c.DATA_SOURCES: {
                        db_c.NOTIFICATION_TYPE_INFORMATIONAL: True,
                        db_c.NOTIFICATION_TYPE_SUCCESS: False,
                        db_c.NOTIFICATION_TYPE_CRITICAL: True,
                    },
                },
                api_c.DECISIONING: {
                    api_c.MODELS: {
                        db_c.NOTIFICATION_TYPE_INFORMATIONAL: True,
                        db_c.NOTIFICATION_TYPE_SUCCESS: False,
                        db_c.NOTIFICATION_TYPE_CRITICAL: True,
                    },
                },
                api_c.ORCHESTRATION_TAG: {
                    api_c.DESTINATIONS: {
                        db_c.NOTIFICATION_TYPE_INFORMATIONAL: True,
                        db_c.NOTIFICATION_TYPE_SUCCESS: False,
                        db_c.NOTIFICATION_TYPE_CRITICAL: True,
                    },
                    api_c.AUDIENCE_ENGAGEMENTS: {
                        db_c.NOTIFICATION_TYPE_INFORMATIONAL: True,
                        db_c.NOTIFICATION_TYPE_SUCCESS: False,
                        db_c.NOTIFICATION_TYPE_CRITICAL: True,
                    },
                    api_c.AUDIENCES: {
                        db_c.NOTIFICATION_TYPE_INFORMATIONAL: True,
                        db_c.NOTIFICATION_TYPE_SUCCESS: False,
                        db_c.NOTIFICATION_TYPE_CRITICAL: True,
                    },
                    api_c.DELIVERY_TAG: {
                        db_c.NOTIFICATION_TYPE_INFORMATIONAL: True,
                        db_c.NOTIFICATION_TYPE_SUCCESS: False,
                        db_c.NOTIFICATION_TYPE_CRITICAL: True,
                    },
                },
            }
        }

        # get user before update
        user_pre_update = get_user(
            self.database, t_c.VALID_USER_RESPONSE[api_c.OKTA_ID_SUB]
        )
        self.assertEqual(self.user_info, user_pre_update)

        response = self.app.put(
            f"{t_c.BASE_ENDPOINT}{api_c.USER_ENDPOINT}/{api_c.USER_PREFERENCES}",
            headers=t_c.STANDARD_HEADERS,
            json=update_body,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)

        # get user post update
        user_post_update = get_user(
            self.database, t_c.VALID_USER_RESPONSE[api_c.OKTA_ID_SUB]
        )
        self.assertDictEqual(
            update_body[db_c.USER_ALERTS], user_post_update[db_c.USER_ALERTS]
        )

    def test_remove_user_notifications(self):
        """Test successfully removing a users notification preferences"""

        update_body = {
            api_c.ALERTS: {
                api_c.ORCHESTRATION_TAG: {
                    api_c.DESTINATIONS: {
                        db_c.NOTIFICATION_TYPE_INFORMATIONAL: True,
                        db_c.NOTIFICATION_TYPE_SUCCESS: False,
                        db_c.NOTIFICATION_TYPE_CRITICAL: True,
                    }
                },
            }
        }

        # set alerts first
        response = self.app.put(
            f"{t_c.BASE_ENDPOINT}{api_c.USER_ENDPOINT}/{api_c.USER_PREFERENCES}",
            headers=t_c.STANDARD_HEADERS,
            json=update_body,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)

        # get user post update
        user_post_update = get_user(
            self.database, t_c.VALID_USER_RESPONSE[api_c.OKTA_ID_SUB]
        )
        self.assertDictEqual(
            update_body[db_c.USER_ALERTS], user_post_update[db_c.USER_ALERTS]
        )

        # remove alerts
        self.assertEqual(
            HTTPStatus.OK,
            self.app.put(
                f"{t_c.BASE_ENDPOINT}{api_c.USER_ENDPOINT}/{api_c.USER_PREFERENCES}",
                headers=t_c.STANDARD_HEADERS,
                json={db_c.USER_ALERTS: {}},
            ).status_code,
        )

        # get the user again and validate that the alerts are empty.
        self.assertFalse(
            get_user(
                self.database, t_c.VALID_USER_RESPONSE[api_c.OKTA_ID_SUB]
            )[db_c.USER_ALERTS]
        )

    @mock.patch("huxunify.api.route.user.JiraConnection")
    def test_get_user_tickets(self, mock_jira: MagicMock):
        """Test get user tickets endpoint.

        Args:
            mock_jira (MagicMock): magic mock of JiraConnection
        """

        expected_response = {
            api_c.ID: 1234,
            api_c.KEY: "HUS-0000",
            api_c.SUMMARY: "Test ticket summary",
            api_c.STATUS: "To Do",
            api_c.CREATE_TIME: "2021-12-01T15:35:18.000Z",
        }

        mock_jira_instance = mock_jira.return_value
        mock_jira_instance.check_jira_connection.return_value = True
        mock_jira_instance.search_jira_issues.return_value = (
            t_c.SAMPLE_USER_JIRA_TICKETS
        )

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.USER_ENDPOINT}/{t_c.TICKETS}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(len(response.json), 1)
        self.assertDictEqual(expected_response, response.json[0])

    @mock.patch("huxunify.api.route.user.JiraConnection")
    def test_get_user_tickets_no_tickets(self, mock_jira: MagicMock):
        """Test get user tickets endpoint no tickets returned.

        Args:
            mock_jira (MagicMock): magic mock of JiraConnection
        """

        empty_jira_response = {
            "startAt": 0,
            "maxResults": 50,
            "total": 0,
            "issues": [],
        }

        mock_jira_instance = mock_jira.return_value
        mock_jira_instance.check_jira_connection.return_value = True
        mock_jira_instance.search_jira_issues.return_value = (
            empty_jira_response
        )

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.USER_ENDPOINT}/{t_c.TICKETS}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(
            "No matching tickets found for user", response.json[api_c.MESSAGE]
        )

    @mock.patch("huxunify.api.route.user.JiraConnection")
    def test_get_requested_user(self, mock_jira: MagicMock):
        """Test get requested users.

        Args:
            mock_jira (MagicMock): magic mock of JiraConnection
        """

        expected_response = {
            "display_name": "Sarah, Huxley",
            "created": "2022-01-12T15:25:54.000Z",
            "updated": "2022-01-12T15:25:55.000Z",
            "key": "HUS-2010",
            "email": "sh@fake.com",
            "pii_access": False,
            "status": "In Progress",
            "access_level": "admin",
        }

        mock_jira_instance = mock_jira.return_value
        mock_jira_instance.check_jira_connection.return_value = True
        mock_jira_instance.search_jira_issues.return_value = (
            t_c.SAMPLE_USER_REQUEST_JIRA_ISSUES
        )

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.USER_ENDPOINT}/{api_c.REQUESTED_USERS}",
            headers=t_c.STANDARD_HEADERS,
        )
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIn(expected_response, response.json)

    @mock.patch("huxunify.api.route.user.JiraConnection")
    def test_get_requested_users_no_requests(self, mock_jira: MagicMock):
        """Test get requested users when no issues for request found.

        Args:
            mock_jira (MagicMock): magic mock of JiraConnection
        """

        empty_issue_jira_response = {
            "startAt": 0,
            "maxResults": 50,
            "total": 0,
            "issues": [],
        }

        mock_jira_instance = mock_jira.return_value
        mock_jira_instance.check_jira_connection.return_value = True
        mock_jira_instance.search_jira_issues.return_value = (
            empty_issue_jira_response
        )

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.USER_ENDPOINT}/{api_c.REQUESTED_USERS}",
            headers=t_c.STANDARD_HEADERS,
        )
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(
            "No user requests found.", response.json.get(api_c.MESSAGE)
        )
