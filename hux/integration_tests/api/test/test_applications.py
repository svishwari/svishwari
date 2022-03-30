"""Purpose of this file is to test applications endpoints."""
from http import HTTPStatus
from unittest import TestCase
import pytest
import requests
from hux.integration_tests.api.test.conftest import Crud


class TestApplications(TestCase):
    """Application endpoints test class"""

    APPLICATIONS = "applications"
    COLLECTION = "applications"

    def test_get_all_applications(self):
        """Test get all applications"""

        response = requests.get(
            f"{pytest.API_URL}/{self.APPLICATIONS}",
            headers=pytest.HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)

    def test_create_application(self):
        """Test create application"""

        response = requests.post(
            f"{pytest.API_URL}/{self.APPLICATIONS}",
            json={
                "category": "test_category",
                "name": "test_create_application",
                "url": "www.testapplication.com",
            },
            headers=pytest.HEADERS,
        )

        self.assertEqual(HTTPStatus.CREATED, response.status_code)
        pytest.CRUD_OBJECTS += [Crud(self.COLLECTION, response.json()["id"])]

    def test_update_application(self):
        """Test update application"""

        response = requests.post(
            f"{pytest.API_URL}/{self.APPLICATIONS}",
            json={
                "category": "test_category",
                "name": "test_update_application",
                "url": "www.testupdateapplication1.com",
            },
            headers=pytest.HEADERS,
        )

        self.assertEqual(HTTPStatus.CREATED, response.status_code)
        pytest.CRUD_OBJECTS += [Crud(self.COLLECTION, response.json()["id"])]

        response = requests.patch(
            f"{pytest.API_URL}/{self.APPLICATIONS}",
            json={"url": "www.testupdateapplication2.com"},
            headers=pytest.HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(
            "www.testupdateapplication2.com", response.json()["url"]
        )
