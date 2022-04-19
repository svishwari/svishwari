"""This file holds the integration tests for orchestration"""
from http import HTTPStatus
from time import time
from unittest import TestCase
import huxunifylib.database.constants as db_c
import pytest
import requests

from hux.integration_tests.api.test.conftest import Crud


class TestOrchestration(TestCase):
    """Orchestration tests class"""

    AUDIENCES = "audiences"
    DESTINATIONS = "destinations"
    COLLECTION = db_c.AUDIENCES_COLLECTION

    def test_get_audience_rules(self):
        """Test get audience rules"""

        response = requests.get(
            f"{pytest.API_URL}/{self.AUDIENCES}/rules",
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIsInstance(response.json(), dict)

    def test_get_all_audiences(self):
        """Test get all audiences."""

        response = requests.get(
            f"{pytest.API_URL}/{self.AUDIENCES}", headers=pytest.HEADERS
        )

        # test success
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIsInstance(response.json(), dict)

    def test_create_new_audience(self):
        """Test create new audience."""

        response = requests.post(
            f"{pytest.API_URL}/{self.AUDIENCES}",
            json={
                "filters": [
                    {
                        "section_aggregator": "ALL",
                        "section_filters": [
                            {
                                "field": "age",
                                "type": "range",
                                "value": [18, 78],
                            },
                            {
                                "field": "State",
                                "type": "equals",
                                "value": "AL",
                            },
                        ],
                    }
                ],
                "name": f"E2E test_audiences Integration Test-"
                f"{int(time() * 1000)}",
            },
            headers=pytest.HEADERS,
        )
        # test success
        self.assertEqual(HTTPStatus.CREATED, response.status_code)
        self.assertIsInstance(response.json(), dict)

        # add the crud object to pytest for cleaning after
        pytest.CRUD_OBJECTS += [Crud(self.COLLECTION, response.json()["id"])]

    def test_get_histogram_data(self):
        """Test get rules histogram data."""

        response = requests.get(
            f"{pytest.API_URL}/{self.AUDIENCES}/rules/age/histogram",
            headers=pytest.HEADERS,
        )

        rules_data = response.json()
        # test success
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIsInstance(rules_data, dict)

        self.assertEqual("Age", rules_data.get("name"))
        self.assertEqual("range", rules_data.get("type"))

        self.assertIsInstance(rules_data.get("min"), int)
        self.assertIsInstance(rules_data.get("max"), int)
        self.assertIsInstance(rules_data.get("steps"), int)
        self.assertIsInstance(rules_data.get("values"), list)

    def test_get_histogram_models_data(self):
        """Test get histogram data for models."""

        response = requests.get(
            f"{pytest.API_URL}/{self.AUDIENCES}/rules/model/histogram?"
            f"model_name=propensity_to_unsubscribe",
            headers=pytest.HEADERS,
        )

        rules_data = response.json()
        # test success
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIsInstance(rules_data, dict)

        self.assertEqual("Propensity to unsubscribe", rules_data.get("name"))
        self.assertEqual("range", rules_data.get("type"))

        self.assertIsInstance(rules_data.get("min"), float)
        self.assertIsInstance(rules_data.get("max"), float)
        self.assertIsInstance(rules_data.get("values"), list)

    def test_get_location_rules_constant(self):
        """Test get location rules constant."""

        response = requests.get(
            f"{pytest.API_URL}/{self.AUDIENCES}/rules/city/ka",
            headers=pytest.HEADERS,
        )

        rules_data = response.json()
        # test success
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIsInstance(rules_data, list)

        self.assertTrue(str(list(rules_data[0].keys())[0]).find("ka"))

    def test_get_audience_insights(self):
        """Test get audience insights."""

        # Create the audience.
        response = requests.post(
            f"{pytest.API_URL}/{self.AUDIENCES}",
            json={
                "filters": [
                    {
                        "section_aggregator": "ALL",
                        "section_filters": [
                            {
                                "field": "age",
                                "type": "range",
                                "value": [18, 78],
                            },
                            {
                                "field": "State",
                                "type": "equals",
                                "value": "AL",
                            },
                        ],
                    }
                ],
                "name": f"E2E test_audiences Integration Test-"
                f"{int(time() * 1000)}",
            },
            headers=pytest.HEADERS,
        )
        # test success
        self.assertEqual(HTTPStatus.CREATED, response.status_code)
        self.assertIsInstance(response.json(), dict)

        audience_id = response.json().get("id")
        # Get Audience insights.
        response = requests.get(
            f"{pytest.API_URL}/{self.AUDIENCES}/{audience_id}/audience_insights",
            headers=pytest.HEADERS,
        )
        # test success
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIsInstance(response.json(), dict)
        # add the crud object to pytest for cleaning after
        pytest.CRUD_OBJECTS += [Crud(self.COLLECTION, audience_id)]

    def test_add_destination_to_audience(self):
        """Test add destination to audience."""

        # Get the destination.
        response = requests.get(
            f"{pytest.API_URL}/{self.DESTINATIONS}", headers=pytest.HEADERS
        )

        # test success
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIsInstance(response.json(), list)

        destination_id = response.json()[0].get("id")

        # Create the audience.
        response = requests.post(
            f"{pytest.API_URL}/{self.AUDIENCES}",
            json={
                "filters": [
                    {
                        "section_aggregator": "ALL",
                        "section_filters": [
                            {
                                "field": "age",
                                "type": "range",
                                "value": [18, 78],
                            },
                            {
                                "field": "State",
                                "type": "equals",
                                "value": "AL",
                            },
                        ],
                    }
                ],
                "name": f"E2E test_audiences Integration Test-"
                f"{int(time() * 1000)}",
            },
            headers=pytest.HEADERS,
        )
        # test success
        self.assertEqual(HTTPStatus.CREATED, response.status_code)
        self.assertIsInstance(response.json(), dict)

        audience_id = response.json().get("id")
        response = requests.post(
            f"{pytest.API_URL}/{self.AUDIENCES}/{audience_id}/destinations",
            json={"id": destination_id},
            headers=pytest.HEADERS,
        )

        self.assertEqual(HTTPStatus.CREATED, response.status_code)
        self.assertIsInstance(response.json(), dict)

        # Ensure destination is added.
        self.assertEqual(
            destination_id, response.json().get("destinations")[0].get("id")
        )

        pytest.CRUD_OBJECTS += [Crud(self.COLLECTION, audience_id)]

    def test_remove_destination_from_audience(self):
        """Test remove destination from audience."""

        # Get the destination.
        response = requests.get(
            f"{pytest.API_URL}/{self.DESTINATIONS}", headers=pytest.HEADERS
        )

        # test success
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIsInstance(response.json(), list)

        destination_id = response.json()[0].get("id")

        # Create the audience.
        response = requests.post(
            f"{pytest.API_URL}/{self.AUDIENCES}",
            json={
                "filters": [
                    {
                        "section_aggregator": "ALL",
                        "section_filters": [
                            {
                                "field": "age",
                                "type": "range",
                                "value": [18, 78],
                            },
                            {
                                "field": "State",
                                "type": "equals",
                                "value": "AL",
                            },
                        ],
                    }
                ],
                "name": f"E2E test_audiences Integration Test-"
                f"{int(time() * 1000)}",
            },
            headers=pytest.HEADERS,
        )
        # test success
        self.assertEqual(HTTPStatus.CREATED, response.status_code)
        self.assertIsInstance(response.json(), dict)

        audience_id = response.json().get("id")
        response = requests.post(
            f"{pytest.API_URL}/{self.AUDIENCES}/{audience_id}/destinations",
            json={"id": destination_id},
            headers=pytest.HEADERS,
        )

        self.assertEqual(HTTPStatus.CREATED, response.status_code)
        self.assertIsInstance(response.json(), dict)

        # Ensure destination is added.
        self.assertEqual(
            destination_id, response.json().get("destinations")[0].get("id")
        )

        # Delete
        response = requests.delete(
            f"{pytest.API_URL}/{self.AUDIENCES}/{audience_id}/destinations",
            json={"id": destination_id},
            headers=pytest.HEADERS,
        )
        self.assertEqual(HTTPStatus.NO_CONTENT, response.status_code)

        pytest.CRUD_OBJECTS += [Crud(self.COLLECTION, audience_id)]

    def test_get_country_level_audience_insights(self):
        """Test get country level audience Insights."""

        # Create the audience.
        response = requests.post(
            f"{pytest.API_URL}/{self.AUDIENCES}",
            json={
                "filters": [
                    {
                        "section_aggregator": "ALL",
                        "section_filters": [
                            {
                                "field": "age",
                                "type": "range",
                                "value": [18, 78],
                            },
                            {
                                "field": "State",
                                "type": "equals",
                                "value": "AL",
                            },
                        ],
                    }
                ],
                "name": f"E2E test_audiences Integration Test-"
                f"{int(time() * 1000)}",
            },
            headers=pytest.HEADERS,
        )
        # test success
        self.assertEqual(HTTPStatus.CREATED, response.status_code)
        self.assertIsInstance(response.json(), dict)

        audience_id = response.json().get("id")

        response = requests.get(
            f"{pytest.API_URL}/{self.AUDIENCES}/{audience_id}/countries",
            headers=pytest.HEADERS,
        )
        # test success
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIsInstance(response.json(), list)

        pytest.CRUD_OBJECTS += [Crud(self.COLLECTION, audience_id)]

    def test_get_state_level_audience_insights(self):
        """Test get state level audience Insights."""

        # Create the audience.
        response = requests.post(
            f"{pytest.API_URL}/{self.AUDIENCES}",
            json={
                "filters": [
                    {
                        "section_aggregator": "ALL",
                        "section_filters": [
                            {
                                "field": "age",
                                "type": "range",
                                "value": [18, 78],
                            },
                            {
                                "field": "State",
                                "type": "equals",
                                "value": "AL",
                            },
                        ],
                    }
                ],
                "name": f"E2E test_audiences Integration Test-"
                f"{int(time() * 1000)}",
            },
            headers=pytest.HEADERS,
        )
        # test success
        self.assertEqual(HTTPStatus.CREATED, response.status_code)
        self.assertIsInstance(response.json(), dict)

        audience_id = response.json().get("id")

        response = requests.get(
            f"{pytest.API_URL}/{self.AUDIENCES}/{audience_id}/states",
            headers=pytest.HEADERS,
        )
        # test success
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIsInstance(response.json(), list)

        pytest.CRUD_OBJECTS += [Crud(self.COLLECTION, audience_id)]

    def test_get_city_level_audience_insights(self):
        """Test get city level audience Insights."""

        # Create the audience.
        response = requests.post(
            f"{pytest.API_URL}/{self.AUDIENCES}",
            json={
                "filters": [
                    {
                        "section_aggregator": "ALL",
                        "section_filters": [
                            {
                                "field": "age",
                                "type": "range",
                                "value": [18, 78],
                            },
                            {
                                "field": "State",
                                "type": "equals",
                                "value": "AL",
                            },
                        ],
                    }
                ],
                "name": f"E2E test_audiences Integration Test-"
                f"{int(time() * 1000)}",
            },
            headers=pytest.HEADERS,
        )
        # test success
        self.assertEqual(HTTPStatus.CREATED, response.status_code)
        self.assertIsInstance(response.json(), dict)

        audience_id = response.json().get("id")

        response = requests.get(
            f"{pytest.API_URL}/{self.AUDIENCES}/{audience_id}/cities",
            headers=pytest.HEADERS,
        )
        # test success
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIsInstance(response.json(), list)

        pytest.CRUD_OBJECTS += [Crud(self.COLLECTION, audience_id)]

    def test_get_audience_download(self):
        """Test download audience file."""
        # Create the audience.
        response = requests.post(
            f"{pytest.API_URL}/{self.AUDIENCES}",
            json={
                "filters": [
                    {
                        "section_aggregator": "ALL",
                        "section_filters": [
                            {
                                "field": "age",
                                "type": "range",
                                "value": [18, 78],
                            },
                            {
                                "field": "State",
                                "type": "equals",
                                "value": "AL",
                            },
                        ],
                    }
                ],
                "name": f"E2E test_audiences Integration Test-"
                f"{int(time() * 1000)}",
            },
            headers=pytest.HEADERS,
        )
        # test success

        self.assertEqual(HTTPStatus.CREATED, response.status_code)
        self.assertIsInstance(response.json(), dict)

        audience_id = response.json().get("id")

        # Download Audience Files.
        response = requests.get(
            f"{pytest.API_URL}/{self.AUDIENCES}/"
            f"{audience_id}/download?"
            f"download_types=amazon_ads"
            f"&download_types=google_ads",
            headers=pytest.HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(
            "application/zip", response.headers.get("content-type")
        )

        pytest.CRUD_OBJECTS += [Crud(self.COLLECTION, audience_id)]

    def test_get_audience_by_id(self):
        """Test get audience by id."""

        response = requests.post(
            f"{pytest.API_URL}/{self.AUDIENCES}",
            json={
                "filters": [
                    {
                        "section_aggregator": "ALL",
                        "section_filters": [
                            {
                                "field": "age",
                                "type": "range",
                                "value": [18, 78],
                            },
                            {
                                "field": "State",
                                "type": "equals",
                                "value": "AL",
                            },
                        ],
                    }
                ],
                "name": f"E2E test_audiences Integration Test-"
                f"{int(time() * 1000)}",
            },
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.CREATED, response.status_code)
        self.assertIsInstance(response.json(), dict)

        audience_id = response.json().get("id")

        response = requests.get(
            f"{pytest.API_URL}/{self.AUDIENCES}/{audience_id}",
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIsInstance(response.json(), dict)

        pytest.CRUD_OBJECTS += [Crud(self.COLLECTION, audience_id)]

    def test_update_audience(self):
        """Test update audience."""

        response = requests.post(
            f"{pytest.API_URL}/{self.AUDIENCES}",
            json={
                "filters": [
                    {
                        "section_aggregator": "ALL",
                        "section_filters": [
                            {
                                "field": "age",
                                "type": "range",
                                "value": [18, 78],
                            },
                            {
                                "field": "State",
                                "type": "equals",
                                "value": "AL",
                            },
                        ],
                    }
                ],
                "name": f"E2E test_audiences Integration Test-"
                f"{int(time() * 1000)}",
            },
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.CREATED, response.status_code)
        self.assertIsInstance(response.json(), dict)

        audience_id = response.json().get("id")

        response = requests.put(
            f"{pytest.API_URL}/{self.AUDIENCES}/{audience_id}",
            json={
                "filters": [
                    {
                        "section_aggregator": "ALL",
                        "section_filters": [
                            {
                                "field": "age",
                                "type": "range",
                                "value": [18, 58],
                            },
                            {
                                "field": "State",
                                "type": "equals",
                                "value": "AL",
                            },
                        ],
                    }
                ]
            },
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIsInstance(response.json(), dict)

        pytest.CRUD_OBJECTS += [Crud(self.COLLECTION, audience_id)]

    def test_delete_audience(self):
        """Test delete audience."""

        response = requests.post(
            f"{pytest.API_URL}/{self.AUDIENCES}",
            json={
                "filters": [
                    {
                        "section_aggregator": "ALL",
                        "section_filters": [
                            {
                                "field": "age",
                                "type": "range",
                                "value": [18, 78],
                            },
                            {
                                "field": "State",
                                "type": "equals",
                                "value": "AL",
                            },
                        ],
                    }
                ],
                "name": f"E2E test_audiences Integration Test-"
                f"{int(time() * 1000)}",
            },
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.CREATED, response.status_code)
        self.assertIsInstance(response.json(), dict)

        audience_id = response.json().get("id")

        response = requests.delete(
            f"{pytest.API_URL}/{self.AUDIENCES}/{audience_id}",
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.NO_CONTENT, response.status_code)
