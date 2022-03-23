"""This file holds the integration tests for notifications"""
from http import HTTPStatus
from unittest import TestCase
import huxunifylib.database.constants as db_c
import pytest
import requests

from hux.integration_tests.api.test.conftest import Crud


class TestNotifications(TestCase):
    """Notifications tests class"""

    NOTIFICATIONS = "notifications"
    COLLECTION = db_c.NOTIFICATIONS_COLLECTION

    def test_distinct_users(self) -> None:
        """Test GET /notifications/users"""

        response = requests.get(
            f"{pytest.API_URL}/{self.NOTIFICATIONS}/users",
            headers=pytest.HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)

    def test_create_notification(self) -> None:
        """Test create a notification"""

        response = requests.post(
            f"{pytest.API_URL}/{self.NOTIFICATIONS}",
            json={
                "category": db_c.NOTIFICATION_CATEGORY_DELIVERY,
                "type": db_c.NOTIFICATION_TYPE_SUCCESS,
                "description": "E2E integration test to create notification.",
            },
            headers=pytest.HEADERS,
        )

        notification_id = response.json()["id"]
        pytest.CRUD_OBJECTS += [Crud(self.COLLECTION, notification_id)]
        self.assertEqual(HTTPStatus.CREATED, response.status_code)

    def test_get_notification(self) -> None:
        """Test get a notification"""

        response = requests.post(
            f"{pytest.API_URL}/{self.NOTIFICATIONS}",
            json={
                "category": db_c.NOTIFICATION_CATEGORY_DELIVERY,
                "type": db_c.NOTIFICATION_TYPE_SUCCESS,
                "description": "E2E integration test to get notification.",
            },
            headers=pytest.HEADERS,
        )

        notification_id = response.json()["id"]
        pytest.CRUD_OBJECTS += [Crud(self.COLLECTION, notification_id)]
        self.assertEqual(HTTPStatus.CREATED, response.status_code)

        response = requests.get(
            f"{pytest.API_URL}/{self.NOTIFICATIONS}/{notification_id}",
            headers=pytest.HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)

    def test_delete_notification(self) -> None:
        """Test delete a notification"""

        # create a notification that will be deleted
        response = requests.post(
            f"{pytest.API_URL}/{self.NOTIFICATIONS}",
            json={
                "category": db_c.NOTIFICATION_CATEGORY_DELIVERY,
                "type": db_c.NOTIFICATION_TYPE_SUCCESS,
                "description": "E2E integration test to delete a notification.",
            },
            headers=pytest.HEADERS,
        )

        notification_id = response.json()["id"]
        pytest.CRUD_OBJECTS += [Crud(self.COLLECTION, notification_id)]
        self.assertEqual(HTTPStatus.CREATED, response.status_code)

        response = requests.delete(
            f"{pytest.API_URL}/{self.NOTIFICATIONS}/{notification_id}",
            headers=pytest.HEADERS,
        )

        self.assertEqual(HTTPStatus.NO_CONTENT, response.status_code)
