"""Purpose of this file is to test data sources."""
from http import HTTPStatus
from unittest import TestCase
import pytest
import requests
from prometheus_metrics import record_test_result, HttpMethod, Endpoints


class TestClientProjects(TestCase):
    """Testing Client Projects."""

    CLIENT_PROJECTS = "client-projects"

    @record_test_result(
        HttpMethod.GET, Endpoints.CLIENT_PROJECTS.GET_ALL_CLIENT_PROJECTS
    )
    def test_get_client_projects(self):
        """Testing GET Client Projects endpoint."""

        response = requests.get(
            f"{pytest.API_URL}/{self.CLIENT_PROJECTS}", headers=pytest.HEADERS
        )

        # test success
        self.assertEqual(HTTPStatus.OK, response.status_code)

    @record_test_result(
        HttpMethod.PATCH, Endpoints.CLIENT_PROJECTS.PATCH_UPDATE_CLIENT_PROJECT
    )
    def test_patch_client_projects(self):
        """Testing PATCH Client Projects endpoint."""

        get_response = requests.get(
            f"{pytest.API_URL}/{self.CLIENT_PROJECTS}", headers=pytest.HEADERS
        )

        client_project_id = get_response.json()[0].get("id")
        client_project_url = get_response.json()[0].get("url")

        response = requests.patch(
            f"{pytest.API_URL}/{self.CLIENT_PROJECTS}/{client_project_id}",
            json={
                "url": client_project_url,
            },
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.OK, response.status_code)
