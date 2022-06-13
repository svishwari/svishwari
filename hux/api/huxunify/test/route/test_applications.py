"""Purpose of this file is to house all tests related to configurations."""
import string
from typing import Any
from unittest import mock
from http import HTTPStatus

from bson import ObjectId
from hypothesis import given, strategies as st

from huxunify.api.schema.applications import ApplicationsGETSchema
from huxunify.test.route.route_test_util.route_test_case import RouteTestCase
from huxunifylib.database.user_management import set_user
from huxunifylib.database.collection_management import (
    get_documents,
    create_document,
)
from huxunifylib.database import constants as db_c
import huxunify.test.constants as t_c
from huxunify.api import constants as api_c


class ApplicationsTests(RouteTestCase):
    """Tests for applications."""

    def setUp(self) -> None:
        """Setup resources before each test."""

        super().setUp()

        mock.patch(
            "huxunify.api.route.applications.get_db_client",
            return_value=self.database,
        ).start()

        # write a user to the database
        self.user_name = t_c.VALID_USER_RESPONSE.get(api_c.NAME)
        self.user_doc = set_user(
            self.database,
            t_c.VALID_INTROSPECTION_RESPONSE.get(api_c.OKTA_UID),
            t_c.VALID_USER_RESPONSE.get(api_c.EMAIL),
            display_name=self.user_name,
            role=t_c.VALID_USER_RESPONSE.get(api_c.ROLE),
        )

        applications = [
            {
                db_c.NAME: "Tableau",
                db_c.CATEGORY: "Reporting",
                db_c.ICON: "default.ico",
                db_c.ENABLED: True,
            },
            {
                db_c.NAME: "Snowflake",
                db_c.CATEGORY: "Data Storage",
                db_c.ICON: "default.ico",
                db_c.ENABLED: True,
            },
        ]

        self.applications = [
            create_document(
                self.database, db_c.APPLICATIONS_COLLECTION, application
            )
            for application in applications
        ]

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
            self.assertFalse(application[api_c.IS_ADDED])

    def test_get_all_applications_success_user_only(self):
        """Test get all applications successfully with no params."""
        application = self.applications[0]

        applications_request = {
            api_c.CATEGORY: application.get(api_c.CATEGORY),
            api_c.NAME: application.get(api_c.NAME),
            api_c.URL: "URL_Link",
        }
        # Creating application so it is added to user.
        self.app.post(
            f"{t_c.BASE_ENDPOINT}{api_c.APPLICATIONS_ENDPOINT}",
            headers=t_c.STANDARD_HEADERS,
            json=applications_request,
        )

        patch_request_body = {api_c.URL: "NEW_URL_Link"}

        self.app.patch(
            f"{t_c.BASE_ENDPOINT}{api_c.APPLICATIONS_ENDPOINT}/"
            f"{self.applications[0][db_c.ID]}",
            headers=t_c.STANDARD_HEADERS,
            json=patch_request_body,
        )

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.APPLICATIONS_ENDPOINT}",
            query_string={api_c.USER: True},
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertFalse(
            ApplicationsGETSchema(many=True).validate(response.json)
        )
        self.assertEqual(len(response.json), 1)
        self.assertEqual(
            response.json[0][api_c.ID], str(self.applications[0][db_c.ID])
        )
        self.assertTrue(response.json[0][api_c.IS_ADDED])

    def test_success_create_applications(self):
        """Test creating application successfully."""

        applications_request = {
            api_c.CATEGORY: "Uncategorized",
            api_c.NAME: "Custom Application",
            api_c.URL: "URL_Link",
        }

        # Ensure the application is created successfully
        response = self.app.post(
            f"{t_c.BASE_ENDPOINT}{api_c.APPLICATIONS_ENDPOINT}",
            headers=t_c.STANDARD_HEADERS,
            json=applications_request,
        )

        self.assertEqual(
            response.json[api_c.CATEGORY], applications_request[api_c.CATEGORY]
        )
        self.assertEqual(
            response.json[api_c.URL], applications_request[api_c.URL]
        )
        self.assertEqual(
            response.json[api_c.NAME], applications_request[api_c.NAME]
        )

        self.assertEqual(HTTPStatus.CREATED, response.status_code)

        # Ensure the application is created in applications collection
        applications = ApplicationsGETSchema(many=True).dump(
            get_documents(self.database, db_c.APPLICATIONS_COLLECTION)[
                db_c.DOCUMENTS
            ]
        )
        names = [i[api_c.NAME] for i in applications]
        self.assertEqual(len(applications), 3)
        self.assertIn(applications_request[api_c.NAME], names)

    def test_create_invalid_application(self):
        """Test create invalid application."""

        applications_request = {
            api_c.CATEGORY: "Uncategorized",
            api_c.NAME: "Custom Application",
        }
        response = self.app.post(
            f"{t_c.BASE_ENDPOINT}{api_c.APPLICATIONS_ENDPOINT}",
            headers=t_c.STANDARD_HEADERS,
            json=applications_request,
        )

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)

    def test_create_duplicate_application(self):
        """Test create invalid application."""

        applications_request = {
            api_c.CATEGORY: "Uncategorized",
            api_c.NAME: "Custom Application",
            api_c.URL: "URL_Link",
        }

        self.app.post(
            f"{t_c.BASE_ENDPOINT}{api_c.APPLICATIONS_ENDPOINT}",
            headers=t_c.STANDARD_HEADERS,
            json=applications_request,
        )

        # Ensure the application is created in applications collection
        applications = ApplicationsGETSchema(many=True).dump(
            get_documents(self.database, db_c.APPLICATIONS_COLLECTION)[
                db_c.DOCUMENTS
            ]
        )
        names = [i[api_c.NAME] for i in applications]
        self.assertEqual(len(applications), 3)
        self.assertIn(applications_request[api_c.NAME], names)

        applications_request = {
            api_c.CATEGORY: "Uncategorized",
            api_c.NAME: "Custom Application",
            api_c.URL: "URL_Link",
        }

        self.app.post(
            f"{t_c.BASE_ENDPOINT}{api_c.APPLICATIONS_ENDPOINT}",
            headers=t_c.STANDARD_HEADERS,
            json=applications_request,
        )

        # Ensure a duplicate application is NOT created in applications collection
        applications = ApplicationsGETSchema(many=True).dump(
            get_documents(self.database, db_c.APPLICATIONS_COLLECTION)[
                db_c.DOCUMENTS
            ]
        )
        names = [i[api_c.NAME] for i in applications]
        self.assertEqual(len(applications), 3)
        self.assertIn(applications_request[api_c.NAME], names)

    def test_success_add_existing_applications(self):
        """Test creating application successfully."""

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

        # Ensure no new application is created in applications collection
        applications = ApplicationsGETSchema(many=True).dump(
            get_documents(self.database, db_c.APPLICATIONS_COLLECTION)[
                db_c.DOCUMENTS
            ]
        )
        self.assertEqual(len(applications), 2)

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
            query_string={api_c.USER: value},
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual(
            {api_c.MESSAGE: f"'{value}' is not a valid boolean value"},
            response.json,
        )

    def test_applications_patch_endpoint_valid_request(self):
        """Test patch with correct request body"""
        patch_request_body = {
            api_c.URL: "NEW_URL_Link",
        }

        application = self.applications[0]

        applications_request = {
            api_c.CATEGORY: application.get(api_c.CATEGORY),
            api_c.NAME: application.get(api_c.NAME),
            api_c.URL: "URL_Link",
        }
        # Create the application ensuring it is added to the user collection.
        self.app.post(
            f"{t_c.BASE_ENDPOINT}{api_c.APPLICATIONS_ENDPOINT}",
            headers=t_c.STANDARD_HEADERS,
            json=applications_request,
        )

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

    def test_applications_patch_endpoint_soft_delete(self):
        """Test patch soft delete"""

        patch_request_body = {api_c.URL: "NEW_URL_Link", api_c.IS_ADDED: False}

        application = self.applications[0]

        applications_request = {
            api_c.CATEGORY: application.get(api_c.CATEGORY),
            api_c.NAME: application.get(api_c.NAME),
            api_c.URL: "URL_Link",
        }
        # Create the application ensuring it is added to the user collection.
        self.app.post(
            f"{t_c.BASE_ENDPOINT}{api_c.APPLICATIONS_ENDPOINT}",
            headers=t_c.STANDARD_HEADERS,
            json=applications_request,
        )

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

        # Ensure no applications are returned as it is soft deleted.
        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.APPLICATIONS_ENDPOINT}",
            query_string={api_c.USER: True},
            headers=t_c.STANDARD_HEADERS,
        )
        self.assertEqual(
            api_c.EMPTY_USER_APPLICATION_RESPONSE,
            response.json.get(api_c.MESSAGE),
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
