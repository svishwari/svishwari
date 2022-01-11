"""Purpose of this file is to house all tests related to configurations."""
from unittest import TestCase, mock
from http import HTTPStatus

import requests_mock
import mongomock

from huxunifylib.database.client import DatabaseClient
from huxunifylib.database.user_management import (
    set_user,
)
import huxunify.test.constants as t_c
from huxunify.api import constants as api_c
from huxunify.app import create_app


class ApplicationsTests(TestCase):
    """Tests for applications."""

    def setUp(self) -> None:
        """Setup resources before each test."""

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

        mock.patch(
            "huxunify.api.route.applications.get_db_client",
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

        # write a user to the database
        self.user_name = t_c.VALID_USER_RESPONSE.get(api_c.NAME)
        self.user_doc = set_user(
            self.database,
            t_c.VALID_RESPONSE.get(api_c.OKTA_UID),
            t_c.VALID_USER_RESPONSE.get(api_c.EMAIL),
            display_name=self.user_name,
        )

        self.addCleanup(mock.patch.stopall)

    def test_success_create_applications(self):
        """Test get configurations."""

        applications_request = {
            api_c.CATEGORY: "uncategorized",
            api_c.TYPE: "custom-application",
            api_c.NAME: "Custom Application",
            api_c.URL: "URL_Link",
        }
        response = self.app.post(
            f"{t_c.BASE_ENDPOINT}{api_c.APPLICATIONS_ENDPOINT}",
            headers=t_c.STANDARD_HEADERS,
            json=applications_request,
        )

        self.assertEqual(HTTPStatus.CREATED, response.status_code)

    def test_success_invalid_applications(self):
        """Test get configurations."""

        applications_request = {
            api_c.CATEGORY: "uncategorized",
            api_c.TYPE: "custom-application",
            api_c.NAME: "Custom Application",
        }
        response = self.app.post(
            f"{t_c.BASE_ENDPOINT}{api_c.APPLICATIONS_ENDPOINT}",
            headers=t_c.STANDARD_HEADERS,
            json=applications_request,
        )

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)

    def test_success_duplicate_applications(self):
        """Test get configurations."""

        applications_request = {
            api_c.CATEGORY: "uncategorized",
            api_c.TYPE: "custom-application",
            api_c.NAME: "Custom Application",
            api_c.URL: "URL_Link",
        }
        response = self.app.post(
            f"{t_c.BASE_ENDPOINT}{api_c.APPLICATIONS_ENDPOINT}",
            headers=t_c.STANDARD_HEADERS,
            json=applications_request,
        )

        self.assertEqual(HTTPStatus.CREATED, response.status_code)

        applications_request = {
            api_c.CATEGORY: "uncategorized",
            api_c.TYPE: "custom-application",
            api_c.NAME: "Custom Application",
            api_c.URL: "URL_Link_New",
        }
        response = self.app.post(
            f"{t_c.BASE_ENDPOINT}{api_c.APPLICATIONS_ENDPOINT}",
            headers=t_c.STANDARD_HEADERS,
            json=applications_request,
        )

        self.assertEqual(HTTPStatus.FORBIDDEN, response.status_code)
