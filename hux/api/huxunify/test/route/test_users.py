# pylint: disable=too-many-lines
"""Purpose of this file is to house all the engagement API tests."""
from unittest import TestCase, mock
from http import HTTPStatus
import requests_mock
import mongomock

from huxunifylib.database import constants as db_c
from huxunifylib.database.client import DatabaseClient
from huxunifylib.database.delivery_platform_management import (
    set_delivery_platform,
)
from huxunifylib.database.engagement_management import set_engagement
from huxunifylib.database.orchestration_management import create_audience
from huxunifylib.database.user_management import set_user

from huxunify.app import create_app

from huxunify.api import constants as api_c
from huxunify.api.schema.user import UserSchema

import huxunify.test.constants as t_c


class TestUserRoutes(TestCase):
    """Tests for User APIs."""

    def setUp(self) -> None:
        """Setup resources before each test."""

        # mock request for introspect call
        request_mocker = requests_mock.Mocker()
        request_mocker.post(t_c.INTROSPECT_CALL, json=t_c.VALID_RESPONSE)
        request_mocker.start()

        self.app = create_app().test_client()

        # init mongo patch initially
        mongo_patch = mongomock.patch(servers=(("localhost", 27017),))
        mongo_patch.start()

        # setup the mock DB client
        self.database = DatabaseClient(
            "localhost", 27017, None, None
        ).connect()

        mock.patch(
            "huxunify.api.route.user.get_db_client",
            return_value=self.database,
        ).start()

        self.audience_id = create_audience(self.database, "Test Audience", [])[
            db_c.ID
        ]
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
            None,
            None,
            False,
        )

        # write a user to the database

        self.user_info = set_user(
            self.database,
            t_c.VALID_RESPONSE["uid"],
            "felix_hernandez@fake.com",
            display_name="Felix Hernandez",
        )

        self.addCleanup(mock.patch.stopall)

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

        self.assertEqual(response.json.get("message"), api_c.OPERATION_SUCCESS)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)

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
        self.assertEqual(response.json.get("message"), api_c.OPERATION_SUCCESS)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)

    def test_adding_invalid_audience_to_favorite(self):
        """Tests adding invalid audience as a user favorite.
        Testing by sending audience_id not in DB, here using engagement ID.
        """

        invalid_audience_id = self.engagement_id

        endpoint = (
            f"{t_c.BASE_ENDPOINT}"
            f"{api_c.USER_ENDPOINT}/"
            f"{db_c.AUDIENCES}/"
            f"{invalid_audience_id}/"
            f"{api_c.FAVORITE}"
        )

        response = self.app.post(
            endpoint,
            headers=t_c.STANDARD_HEADERS,
        )
        expected_response_message = (
            f"The ID <{invalid_audience_id}> does "
            f"not exist in the database!"
        )
        self.assertEqual(
            response.json.get("message"), expected_response_message
        )
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

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

        self.assertEqual(response.json.get("message"), api_c.OPERATION_SUCCESS)
        self.assertEqual(response.status_code, HTTPStatus.OK)

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
            response.json.get("message"), expected_response_message
        )

    def test_get_user_profile(self):
        """Tests getting user profile using Okta ID."""

        endpoint = (
            f"{t_c.BASE_ENDPOINT}" f"{api_c.USER_ENDPOINT}/" f"{api_c.PROFILE}"
        )

        response = self.app.get(
            endpoint,
            headers=t_c.STANDARD_HEADERS,
        )
        t_c.validate_schema(UserSchema(), response.json)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_get_all_users(self):
        """Tests getting all users."""

        endpoint = (
            f"{t_c.BASE_ENDPOINT}" f"{api_c.USER_ENDPOINT}"
        )

        response = self.app.get(
            endpoint,
            headers=t_c.STANDARD_HEADERS,
        )
        t_c.validate_schema(UserSchema(), response.json, True)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(1, len(response.json))
        self.assertIsNotNone(response.json[0][api_c.DISPLAY_NAME])
        self.assertIsNotNone(response.json[0][api_c.EMAIL])
        self.assertIsNotNone(response.json[0][api_c.USER_PHONE_NUMBER])
        self.assertIsNotNone(response.json[0][api_c.USER_ACCESS_LEVEL])
        self.assertIn(
            response.json[0][api_c.USER_ACCESS_LEVEL],
            ["Edit", "View-only", "Admin"],
        )
