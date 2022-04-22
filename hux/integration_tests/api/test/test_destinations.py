"""Purpose of this file is to integration test for destinations."""
from unittest import TestCase
from http import HTTPStatus
import pytest
import requests


class TestDestinations(TestCase):
    """Test Destinations."""

    DESTINATIONS = "destinations"
    COLLECTION = "delivery_platforms"
    DELIVERY_PLATFORM_SFMC = "sfmc"

    def test_get_destinations(self):
        """Test get all destinations."""

        response = requests.get(
            f"{pytest.API_URL}/{self.DESTINATIONS}",
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIsInstance(response.json(), list)
        self.assertGreaterEqual(len(response.json()), 1)

    def test_get_destination(self):
        """Test get destination."""

        response = requests.get(
            f"{pytest.API_URL}/{self.DESTINATIONS}",
            headers=pytest.HEADERS,
        )
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(response.json(), list)

        destinations = response.json()

        destination_response = requests.get(
            f"{pytest.API_URL}/{self.DESTINATIONS}/{destinations[0]['id']}",
            headers=pytest.HEADERS,
        )
        # test success
        self.assertEqual(HTTPStatus.OK, destination_response.status_code)
        self.assertIsInstance(destination_response.json(), dict)

    def test_get_destination_constants(self):
        """Test get destination constants."""

        response = requests.get(
            f"{pytest.API_URL}/{self.DESTINATIONS}/constants",
            headers=pytest.HEADERS,
        )
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(response.json(), dict)

    def test_get_destination_data_extension(self):
        """Test get destination data extensions."""
        response = requests.get(
            f"{pytest.API_URL}/{self.DESTINATIONS}",
            headers=pytest.HEADERS,
        )
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(response.json(), list)

        destinations = response.json()
        sfmc_destination = [
            destination
            for destination in destinations
            if destination["type"] == self.DELIVERY_PLATFORM_SFMC
        ][0]

        response = requests.get(
            f"{pytest.API_URL}/{self.DESTINATIONS}/{sfmc_destination['id']}/data-extensions",
            headers=pytest.HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIsInstance(response.json(), list)
        self.assertGreaterEqual(len(response.json()), 1)

    def test_update_destination(self):
        """Test update destination."""
        response = requests.get(
            f"{pytest.API_URL}/{self.DESTINATIONS}",
            headers=pytest.HEADERS,
        )
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(response.json(), list)

        destination = response.json()[0]

        response = requests.patch(
            f"{pytest.API_URL}/{self.DESTINATIONS}/{destination['id']}",
            json={
                "enabled": destination["is_enabled"]
            },
            headers=pytest.HEADERS,
        )
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIsInstance(response.json(), list)
        self.assertGreaterEqual(len(response.json()), 1)
