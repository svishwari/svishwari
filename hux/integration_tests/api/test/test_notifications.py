"""This file holds the integration tests for notifications."""
from http import HTTPStatus
from unittest import TestCase
import pytest
import requests
from conftest import Crud
from prometheus_metrics import record_test_result, HttpMethod, Endpoints


class TestNotifications(TestCase):
    """Notifications tests class."""

    NOTIFICATIONS = "notifications"
    COLLECTION = "notifications"

    @record_test_result(
        HttpMethod.GET, Endpoints.NOTIFICATIONS.GET_DISTINCT_USERS
    )
    def test_distinct_users(self) -> None:
        """Test GET /notifications/users."""

        response = requests.get(
            f"{pytest.API_URL}/{self.NOTIFICATIONS}/users",
            headers=pytest.HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIsInstance(response.json(), list)

    @record_test_result(
        HttpMethod.POST, Endpoints.NOTIFICATIONS.POST_CREATE_NOTIFICATION
    )
    def test_create_notification(self) -> None:
        """Test create a notification."""

        response = requests.post(
            f"{pytest.API_URL}/{self.NOTIFICATIONS}",
            json={
                "category": "delivery",
                "type": "success",
                "description": "E2E integration test to create notification.",
            },
            headers=pytest.HEADERS,
        )

        notification_id = response.json()["id"]
        pytest.CRUD_OBJECTS += [Crud(self.COLLECTION, notification_id)]

        self.assertEqual(HTTPStatus.CREATED, response.status_code)
        self.assertIsInstance(response.json(), dict)

    @record_test_result(
        HttpMethod.GET, Endpoints.NOTIFICATIONS.GET_ALL_NOTIFICATIONS
    )
    def test_get_notifications(self) -> None:
        """Test get notifications."""

        response = requests.get(
            f"{pytest.API_URL}/{self.NOTIFICATIONS}",
            headers=pytest.HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIsInstance(response.json(), dict)

    @record_test_result(
        HttpMethod.GET, Endpoints.NOTIFICATIONS.GET_NOTIFICATION
    )
    def test_get_notification(self) -> None:
        """Test get a notification."""

        response = requests.post(
            f"{pytest.API_URL}/{self.NOTIFICATIONS}",
            json={
                "category": "delivery",
                "type": "success",
                "description": "E2E integration test to get notification.",
            },
            headers=pytest.HEADERS,
        )

        notification_id = response.json()["id"]
        pytest.CRUD_OBJECTS += [Crud(self.COLLECTION, notification_id)]

        self.assertEqual(HTTPStatus.CREATED, response.status_code)
        self.assertIsInstance(response.json(), dict)

        response = requests.get(
            f"{pytest.API_URL}/{self.NOTIFICATIONS}/{notification_id}",
            headers=pytest.HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIsInstance(response.json(), dict)

    @record_test_result(
        HttpMethod.DELETE, Endpoints.NOTIFICATIONS.DELETE_NOTIFICATION
    )
    def test_delete_notification(self) -> None:
        """Test delete a notification."""

        # create a notification that will be deleted
        response = requests.post(
            f"{pytest.API_URL}/{self.NOTIFICATIONS}",
            json={
                "category": "delivery",
                "type": "success",
                "description": "E2E integration test to delete a notification.",
            },
            headers=pytest.HEADERS,
        )

        notification_id = response.json()["id"]
        pytest.CRUD_OBJECTS += [Crud(self.COLLECTION, notification_id)]

        self.assertEqual(HTTPStatus.CREATED, response.status_code)
        self.assertIsInstance(response.json(), dict)

        response = requests.delete(
            f"{pytest.API_URL}/{self.NOTIFICATIONS}/{notification_id}",
            headers=pytest.HEADERS,
        )

        self.assertEqual(HTTPStatus.NO_CONTENT, response.status_code)
