"""Purpose of this file is to test applications endpoints."""
from http import HTTPStatus
from unittest import TestCase
import pytest
import requests
from conftest import Crud
from prometheus_metrics import record_test_result, HttpMethod, Endpoints


class TestApplications(TestCase):
    """Application endpoints test class"""

    APPLICATIONS = "applications"
    COLLECTION = "applications"

    @record_test_result(
        HttpMethod.GET, Endpoints.APPLICATIONS.GET_ALL_APPLICATIONS
    )
    def test_get_all_applications(self):
        """Test get all applications"""

        response = requests.get(
            f"{pytest.API_URL}/{self.APPLICATIONS}",
            headers=pytest.HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIsInstance(response.json(), list)

    @record_test_result(
        HttpMethod.POST, Endpoints.APPLICATIONS.POST_CREATE_APPLICATION
    )
    def test_create_application(self):
        """Test create application"""

        response = requests.post(
            f"{pytest.API_URL}/{self.APPLICATIONS}",
            json={
                "category": "Uncategorized",
                "name": "int_test_create_application",
                "url": "www.inttestapplication.com",
            },
            headers=pytest.HEADERS,
        )

        pytest.CRUD_OBJECTS += [Crud(self.COLLECTION, response.json()["id"])]

        self.assertEqual(HTTPStatus.CREATED, response.status_code)
        self.assertIsInstance(response.json(), dict)

    @record_test_result(
        HttpMethod.PATCH, Endpoints.APPLICATIONS.PATCH_UPDATE_APPLICATION
    )
    def test_update_application(self):
        """Test update application"""

        response = requests.post(
            f"{pytest.API_URL}/{self.APPLICATIONS}",
            json={
                "category": "Uncategorized",
                "name": "int_test_update_application",
                "url": "www.inttestupdateapplication1.com",
            },
            headers=pytest.HEADERS,
        )

        pytest.CRUD_OBJECTS += [Crud(self.COLLECTION, response.json()["id"])]

        self.assertEqual(HTTPStatus.CREATED, response.status_code)
        self.assertIsInstance(response.json(), dict)

        response = requests.patch(
            f'{pytest.API_URL}/{self.APPLICATIONS}/{response.json()["id"]}',
            json={"url": "www.inttestupdateapplication2.com"},
            headers=pytest.HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIsInstance(response.json(), dict)
        self.assertEqual(
            "www.inttestupdateapplication2.com", response.json()["url"]
        )
