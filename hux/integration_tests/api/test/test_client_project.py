"""Purpose of this file is to test data sources."""
from http import HTTPStatus
from unittest import TestCase
import pytest
import requests
from hux.integration_tests.api.test.conftest import Crud


class TestClientProjects(TestCase):
    """Testing Client Projects."""

    CLIENT_PROJECTS = "client-projects"

    def test_get_client_projects(self):
        """Testing GET Client Projects endpoint."""

        response = requests.get(
            f"{pytest.API_URL}/{self.CLIENT_PROJECTS}",
            headers=pytest.HEADERS
        )

        # test success
        self.assertEqual(HTTPStatus.OK, response.status_code)

    def test_patch_client_projects(self):
        """Testing PATCH Client Projects endpoint."""

        get_response = requests.get(
            f"{pytest.API_URL}/{self.CLIENT_PROJECTS}",
            headers=pytest.HEADERS
        )

        id = get_response.json()[0].get("id")
        url = get_response.json()[0].get("url")

        response = requests.patch(
            f"{pytest.API_URL}/{self.CLIENT_PROJECTS}/{id}",
            json=
            {
                "url": url,
            }
            ,
            headers=pytest.HEADERS
        )

        # test success
        self.assertEqual(HTTPStatus.OK, response.status_code)
