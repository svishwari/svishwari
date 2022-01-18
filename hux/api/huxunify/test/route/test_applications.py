"""Purpose of this file is to house all tests related to configurations."""
import string
from typing import Any
from unittest import TestCase, mock
from http import HTTPStatus

import requests_mock
import mongomock
from bson import ObjectId
from hypothesis import given, strategies as st

from huxunify.api.schema.applications import ApplicationsGETSchema
from huxunifylib.database.client import DatabaseClient
from huxunifylib.database.user_management import (
    set_user,
)
from huxunifylib.database.collection_management import (
    get_documents,
    create_document,
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

        applications = [
            {
                api_c.CATEGORY: "uncategorized",
                api_c.TYPE: "custom-test-application-1",
                api_c.NAME: "Custom Test Application 1",
                api_c.URL: "CTA1_URL_Link",
                api_c.STATUS: "Active",
            },
            {
                api_c.CATEGORY: "uncategorized",
                api_c.TYPE: "custom-test-application-2",
                api_c.NAME: "Custom Test Application 2",
                api_c.URL: "CTA2_URL_Link",
                api_c.STATUS: "Pending",
            },
        ]

        self.applications = [
            create_document(
                self.database, db_c.APPLICATIONS_COLLECTION, application
            )
            for application in applications
        ]

        self.addCleanup(mock.patch.stopall)

    def test_get_all_applications_success_no_params(self):
        """Test get all applications successfully with no params."""
        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.APPLICATIONS_ENDPOINT}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertFalse(
            ApplicationsGETSchema(many=True).validate(response.json)
        )
        for application in response.json:
            self.assertIn(
                application[api_c.STATUS],
                [api_c.STATUS_ACTIVE, api_c.STATUS_PENDING],
            )

    def test_get_all_applications_success_with_params(self):
        """Test get all applications successfully with params."""
        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.APPLICATIONS_ENDPOINT}",
            query_string={api_c.ONLY_ACTIVE: False},
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertFalse(
            ApplicationsGETSchema(many=True).validate(response.json)
        )
        for application in response.json:
            self.assertIn(
                application[api_c.STATUS],
                [api_c.STATUS_ACTIVE, api_c.STATUS_PENDING],
            )

    def test_get_active_applications_success(self):
        """Test get all active applications successfully with params."""
        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.APPLICATIONS_ENDPOINT}",
            query_string={api_c.ONLY_ACTIVE: True},
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertFalse(
            ApplicationsGETSchema(many=True).validate(response.json)
        )
        for application in response.json:
            self.assertEqual(application[api_c.STATUS], api_c.STATUS_ACTIVE)
            self.assertNotEqual(
                application[api_c.STATUS], api_c.STATUS_PENDING
            )

    @given(
        value=st.one_of(
            [
                st.text(alphabet=string.ascii_letters, min_size=1),
                st.integers(),
                st.floats(),
            ]
        )
    )
    def test_get_all_applications_with_invalid_param_values(self, value: Any):
        """Test get all applications with invalid param values.

        Args:
            value (Any): param value, can be integer, float or string
        """
        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.APPLICATIONS_ENDPOINT}",
            query_string={api_c.ONLY_ACTIVE: value},
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual(
            {api_c.MESSAGE: f"'{value}' is not a valid boolean value"},
            response.json,
        )

    def test_success_create_applications(self):
        """Test creating application successfully."""

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

        self.assertEqual(
            response.json[api_c.TYPE],
            applications_request[api_c.TYPE],
        )
        self.assertTrue(response.json[api_c.IS_ADDED])

        self.assertEqual(HTTPStatus.CREATED, response.status_code)

        applications = ApplicationsGETSchema(many=True).dump(
            get_documents(self.database, db_c.APPLICATIONS_COLLECTION)[
                db_c.DOCUMENTS
            ]
        )
        self.assertIn(response.json, applications)

    def test_create_invalid_application(self):
        """Test create invalid application."""

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

    def test_create_duplicate_applications(self):
        """Test creating duplicate application."""

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
        patch_request_body = {
            api_c.URL: "NEW_URL_Link",
        }

        response = self.app.patch(
            f"{t_c.BASE_ENDPOINT}{api_c.APPLICATIONS_ENDPOINT}/"
            f"{self.applications[0][db_c.ID]}",
            headers=t_c.STANDARD_HEADERS,
            json=patch_request_body,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertFalse(ApplicationsGETSchema().validate(response.json))
        self.assertEqual(
            str(self.applications[0][db_c.ID]), response.json.get(api_c.ID)
        )
        self.assertEqual(
            patch_request_body.get(api_c.URL), response.json.get(api_c.URL)
        )

    def test_applications_patch_endpoint_empty_body(self):
        """Test patch with empty request body"""

        response = self.app.patch(
            f"{t_c.BASE_ENDPOINT}{api_c.APPLICATIONS_ENDPOINT}/"
            f"{self.applications[0][db_c.ID]}",
            headers=t_c.STANDARD_HEADERS,
            json={},
        )

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual({api_c.MESSAGE: "No body provided."}, response.json)

    def test_applications_patch_endpoint_invalid_id(self):
        """Test patch with incorrect application id"""

        patch_request_body = {
            api_c.URL: "NEW_URL_Link",
        }

        response = self.app.patch(
            f"{t_c.BASE_ENDPOINT}{api_c.APPLICATIONS_ENDPOINT}/"
            f"{ObjectId()}",
            headers=t_c.STANDARD_HEADERS,
            json=patch_request_body,
        )

        self.assertEqual(HTTPStatus.NOT_FOUND, response.status_code)
