"""Purpose of this file is to house all tests related to client projects."""
from unittest import mock
from http import HTTPStatus

from bson import ObjectId
from huxunify.api.schema.client_projects import ClientProjectGetSchema
from huxunify.test.route.route_test_util.route_test_case import RouteTestCase
from huxunifylib.database.user_management import (
    set_user,
)
from huxunifylib.database.collection_management import create_document
from huxunifylib.database import constants as db_c
import huxunify.test.constants as t_c
from huxunify.api import constants as api_c


class ClientProjectsTests(RouteTestCase):
    """Tests for client projects."""

    def setUp(self) -> None:
        """Setup resources before each test."""

        super().setUp()

        mock.patch(
            "huxunify.api.route.client_projects.get_db_client",
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

        client_projects = [
            {
                api_c.NAME: "Custom Test Client Project 1",
                api_c.TYPE: "custom-test-client-project-1",
                api_c.DESCRIPTION: "Custom Test Client Project 1 Description",
                api_c.URL: "https://localhost/custom-test-client-project-1",
                api_c.ICON: "custom-test-client-project-1.ico",
                api_c.USER_ACCESS_LEVEL: "viewer",
            },
            {
                api_c.NAME: "Custom Test Client Project 2",
                api_c.TYPE: "custom-test-client-project-2",
                api_c.DESCRIPTION: "Custom Test Client Project 2 Description",
                api_c.URL: "https://localhost/custom-test-client-project-2",
                api_c.ICON: "custom-test-client-project-2.ico",
                api_c.USER_ACCESS_LEVEL: "editor",
            },
        ]

        self.client_projects = [
            create_document(
                self.database, db_c.CLIENT_PROJECTS_COLLECTION, client_project
            )
            for client_project in client_projects
        ]

        # self.addCleanup(mock.patch.stopall)

    def test_get_all_client_projects(self):
        """Test get all client projects successfully."""

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.CLIENT_PROJECTS_ENDPOINT}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertFalse(
            ClientProjectGetSchema(many=True).validate(response.json)
        )

    def test_client_project_patch_endpoint_valid_request(self):
        """Test client project patch with correct request body."""

        patch_request_body = {
            api_c.URL: "NEW_URL_Link",
        }

        response = self.app.patch(
            f"{t_c.BASE_ENDPOINT}{api_c.CLIENT_PROJECTS_ENDPOINT}/"
            f"{self.client_projects[0][db_c.ID]}",
            headers=t_c.STANDARD_HEADERS,
            json=patch_request_body,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertFalse(ClientProjectGetSchema().validate(response.json))
        self.assertEqual(
            str(self.client_projects[0][db_c.ID]), response.json.get(api_c.ID)
        )
        self.assertEqual(
            patch_request_body.get(api_c.URL), response.json.get(api_c.URL)
        )

    def test_client_project_patch_endpoint_empty_body(self):
        """Test client project patch with empty request body"""

        response = self.app.patch(
            f"{t_c.BASE_ENDPOINT}{api_c.CLIENT_PROJECTS_ENDPOINT}/"
            f"{self.client_projects[0][db_c.ID]}",
            headers=t_c.STANDARD_HEADERS,
            json={},
        )

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual(
            {api_c.MESSAGE: "No request body provided."}, response.json
        )

    def test_client_project__patch_endpoint_invalid_id(self):
        """Test client project patch with incorrect client_project_id"""

        patch_request_body = {
            api_c.URL: "NEW_URL_Link",
        }

        response = self.app.patch(
            f"{t_c.BASE_ENDPOINT}{api_c.CLIENT_PROJECTS_ENDPOINT}/"
            f"{ObjectId()}",
            headers=t_c.STANDARD_HEADERS,
            json=patch_request_body,
        )

        self.assertEqual(HTTPStatus.NOT_FOUND, response.status_code)
