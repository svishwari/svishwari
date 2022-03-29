"""Purpose of this file is to integration test for configurations."""
from unittest import TestCase
from http import HTTPStatus
import pytest
import requests


class TestConfigurations(TestCase):
    """Test Configurations."""

    CONFIGURATIONS = "configurations"
    COLLECTION = "configurations"

    def test_get_all_configurations(self):
        """Test get all configurations."""

        response = requests.get(
            f"{pytest.API_URL}/{self.CONFIGURATIONS}/modules",
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIsInstance(response.json(), list)

    def test_get_all_configurations_status_active(self):
        """Test get all configurations with status active."""

        response = requests.get(
            f"{pytest.API_URL}/{self.CONFIGURATIONS}/modules?status=active",
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIsInstance(response.json(), list)
        for configuration in response.json():
            self.assertEqual("active", configuration["status"])

    def test_get_navigation_settings_type_configurations(self):
        """Test get configurations of type navigation settings."""

        response = requests.get(
            f"{pytest.API_URL}/{self.CONFIGURATIONS}/navigation",
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIsInstance(response.json(), dict)
        self.assertTrue("settings" in response.json())
        self.assertIsInstance(response.json()["settings"], list)

    def test_update_navigation_settings_type_configuration(self):
        """Test update configuration of a navigation settings type."""

        # get navigation setting to update
        response = requests.get(
            f"{pytest.API_URL}/{self.CONFIGURATIONS}/navigation",
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIsInstance(response.json(), dict)
        self.assertTrue("settings" in response.json())
        self.assertIsInstance(response.json()["settings"], list)

        request_settings_size = len(response.json()["settings"])
        update_response = requests.put(
            f"{pytest.API_URL}/{self.CONFIGURATIONS}/navigation",
            json=response.json(),
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.OK, update_response.status_code)
        self.assertIsInstance(update_response.json(), dict)
        self.assertTrue("settings" in update_response.json())
        self.assertIsInstance(update_response.json()["settings"], list)
        self.assertEqual(
            request_settings_size, len(update_response.json()["settings"])
        )
