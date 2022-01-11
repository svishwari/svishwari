"""Purpose of this file is to house all tests related to configurations."""
from unittest import TestCase, mock
from http import HTTPStatus

import requests_mock
import mongomock
from bson import ObjectId

from huxunifylib.database.client import DatabaseClient
from huxunifylib.database.user_management import (
    set_user,
)
from huxunifylib.database.collection_management import (
    get_documents,
)
from huxunifylib.database import constants as db_c
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
        self.database = DatabaseClient("localhost", 27017, None, None).connect()

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

        applications = get_documents(
            self.database, db_c.APPLICATIONS_COLLECTION
        )
        self.assertIsNotNone(applications[db_c.DOCUMENTS][0])
        self.assertEqual(
            applications[db_c.DOCUMENTS][0][api_c.NAME],
            applications_request[api_c.NAME],
        )
        self.assertEqual(
            applications[db_c.DOCUMENTS][0][api_c.CATEGORY],
            applications_request[api_c.CATEGORY],
        )
        self.assertEqual(
            applications[db_c.DOCUMENTS][0][api_c.TYPE],
            applications_request[api_c.TYPE],
        )

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

    def test_applications_patch_endpoint_valid_request(self):
        """Test patch with correct request body"""
        applications_request = {
            api_c.CATEGORY: "uncategorized",
            api_c.TYPE: "custom-application",
            api_c.NAME: "Custom Application",
            api_c.URL: "URL_Link",
        }

        patch_request_body = {
            api_c.URL: "NEW_URL_Link",
        }
        response = self.app.post(
            f"{t_c.BASE_ENDPOINT}{api_c.APPLICATIONS_ENDPOINT}",
            headers=t_c.STANDARD_HEADERS,
            json=applications_request,
        )

        response = self.app.patch(
            f"{t_c.BASE_ENDPOINT}{api_c.APPLICATIONS_ENDPOINT}/"
            f"{response.json.get(api_c.ID)}",
            headers=t_c.STANDARD_HEADERS,
            json=patch_request_body,
        )

        self.assertEqual(
            response.json.get(api_c.URL), patch_request_body.get(api_c.URL)
        )

    def test_applications_patch_endpoint_invalid_id(self):
        """Test patch with incorrect application id"""

        patch_request_body = {
            api_c.URL: "NEW_URL_Link",
        }

        response = self.app.patch(
            f"{t_c.BASE_ENDPOINT}{api_c.APPLICATIONS_ENDPOINT}/" f"{ObjectId()}",
            headers=t_c.STANDARD_HEADERS,
            json=patch_request_body,
        )

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
