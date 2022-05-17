"""Purpose of this file is to test user endpoints."""
from http import HTTPStatus
from unittest import TestCase
import pytest
import requests


class TestUsers(TestCase):
    """User endpoints test class."""

    USERS = "users"
    COLLECTION = "users"

    def setUp(self) -> None:
        """Setup for user tests."""

        response = requests.get(
            f"{pytest.API_URL}/{self.USERS}/profile",
            headers=pytest.HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.test_user = response.json()
        self.original_alerts = self.test_user["alerts"]

    def tearDown(self) -> None:
        """Resets the test user after each test."""

        # set the original alerts back to the original value
        alert_preferences_all_off = {
            "alerts": {
                "data_management": {
                    "data_sources": {
                        "informational": False,
                        "success": False,
                        "critical": False,
                    }
                },
                "decisioning": {
                    "models": {
                        "informational": False,
                        "success": False,
                        "critical": False,
                    }
                },
                "orchestration": {
                    "destinations": {
                        "informational": False,
                        "success": False,
                        "critical": False,
                    },
                    "engagements": {
                        "informational": False,
                        "success": False,
                        "critical": False,
                    },
                    "audiences": {
                        "informational": False,
                        "success": False,
                        "critical": False,
                    },
                    "delivery": {
                        "informational": False,
                        "success": False,
                        "critical": False,
                    },
                },
            }
        }

        requests.put(
            f"{pytest.API_URL}/{self.USERS}/preferences",
            json=alert_preferences_all_off,
            headers=pytest.HEADERS,
        )

        # reset dashboard config to a blank dict
        requests.patch(
            f"{pytest.API_URL}/{self.USERS}",
            json={"dashboard_configuration": {}},
            headers=pytest.HEADERS,
        )

        # remove all user favorites iteratively
        response = requests.get(
            f"{pytest.API_URL}/{self.USERS}/profile",
            headers=pytest.HEADERS,
        )

        user = response.json()

        for engagement_id in user["favorites"]["engagements"]:
            requests.delete(
                f"{pytest.API_URL}/{self.USERS}/engagements/{engagement_id}/favorite",
                headers=pytest.HEADERS,
            )

        for audience_id in user["favorites"]["audiences"]:
            requests.delete(
                f"{pytest.API_URL}/{self.USERS}/audiences/{audience_id}/favorite",
                headers=pytest.HEADERS,
            )

        for destination_id in user["favorites"]["destinations"]:
            requests.delete(
                f"{pytest.API_URL}/{self.USERS}/destinations/{destination_id}/favorite",
                headers=pytest.HEADERS,
            )

    def test_retrieve_requested_users(self):
        """Test retrieve requested users."""

        response = requests.get(
            f"{pytest.API_URL}/{self.USERS}/requested_users",
            headers=pytest.HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIsInstance(response.json(), list)

    def test_retrieve_all_users(self):
        """Test retrieve all users."""

        response = requests.get(
            f"{pytest.API_URL}/{self.USERS}",
            headers=pytest.HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIsInstance(response.json(), list)

    def test_retrieve_user_profile(self):
        """Test retrieve the user profile."""

        response = requests.get(
            f"{pytest.API_URL}/{self.USERS}/profile",
            headers=pytest.HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIsInstance(response.json(), dict)

    def test_update_user_preferences(self):
        """Test update user preferences."""

        alert_preferences = {
            "alerts": {
                "data_management": {
                    "data_sources": {
                        "informational": True,
                        "success": False,
                        "critical": False,
                    }
                },
                "decisioning": {
                    "models": {
                        "informational": False,
                        "success": False,
                        "critical": False,
                    }
                },
                "orchestration": {
                    "destinations": {
                        "informational": False,
                        "success": False,
                        "critical": False,
                    },
                    "engagements": {
                        "informational": False,
                        "success": False,
                        "critical": False,
                    },
                    "audiences": {
                        "informational": False,
                        "success": False,
                        "critical": False,
                    },
                    "delivery": {
                        "informational": False,
                        "success": False,
                        "critical": False,
                    },
                },
            }
        }

        response = requests.put(
            f"{pytest.API_URL}/{self.USERS}/preferences",
            json=alert_preferences,
            headers=pytest.HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIsInstance(response.json(), dict)

    def test_update_user(self):
        """Test update user."""

        new_config = {"dashboard_configuration": {"test_config_field": 1}}

        response = requests.patch(
            f"{pytest.API_URL}/{self.USERS}",
            json=new_config,
            headers=pytest.HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIsInstance(response.json(), dict)

    def test_create_and_delete_a_user_favorite(self):
        """Test create and delete user favorite."""

        # retrieve all audiences
        response = requests.get(
            f"{pytest.API_URL}/audiences",
            headers=pytest.HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIsInstance(response.json(), dict)

        # get the first audience ID
        audience_id = response.json()["audiences"][0]["id"]

        response = requests.post(
            f"{pytest.API_URL}/{self.USERS}/audiences/{audience_id}/favorite",
            headers=pytest.HEADERS,
        )

        self.assertEqual(HTTPStatus.CREATED, response.status_code)
        self.assertIsInstance(response.json(), dict)

        response = requests.delete(
            f"{pytest.API_URL}/{self.USERS}/audiences/{audience_id}/favorite",
            headers=pytest.HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIsInstance(response.json(), dict)

    def test_retrieve_user_requested_tickets(self):
        """Test retrieve user requested tickets."""

        response = requests.get(
            f"{pytest.API_URL}/{self.USERS}/tickets",
            headers=pytest.HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)

    def test_user_seen_notifications(self):
        """Test user seen notifications."""

        response = requests.get(
            f"{pytest.API_URL}/{self.USERS}/seen_notifications",
            headers=pytest.HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIsInstance(response.json(), dict)
