"""This file holds the integration tests for orchestration"""
from http import HTTPStatus
from time import time
from unittest import TestCase
import pytest
import requests
from conftest import Crud
from prometheus_metrics import record_test_result, HttpMethod, Endpoints


class TestOrchestration(TestCase):
    """Orchestration tests class"""

    AUDIENCES = "audiences"
    LOOKALIKE_AUDIENCES = "lookalike-audiences"
    DESTINATIONS = "destinations"
    COLLECTION = "audiences"
    LOOKALIKE_AUDIENCES_COLLECTION = "lookalike_audiences"
    DEFAULT_AUDIENCE_FILTERS = [
        {
            "section_aggregator": "ALL",
            "section_filters": [
                {
                    "field": "age",
                    "type": "range",
                    "value": [50, 60],
                },
                {
                    "field": "State",
                    "type": "equals",
                    "value": "AL",
                },
            ],
        }
    ]

    @record_test_result(
        HttpMethod.GET, Endpoints.ORCHESTRATION.GET_AUDIENCE_RULES
    )
    def test_get_audience_rules(self):
        """Test get audience rules"""

        response = requests.get(
            f"{pytest.API_URL}/{self.AUDIENCES}/rules",
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIsInstance(response.json(), dict)

    @record_test_result(
        HttpMethod.GET, Endpoints.ORCHESTRATION.GET_ALL_AUDIENCES
    )
    def test_get_all_audiences(self):
        """Test get all audiences."""

        response = requests.get(
            f"{pytest.API_URL}/{self.AUDIENCES}", headers=pytest.HEADERS
        )

        # test success
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIsInstance(response.json(), dict)

    @record_test_result(
        HttpMethod.POST, Endpoints.ORCHESTRATION.POST_CREATE_AUDIENCE
    )
    def test_create_new_audience(self):
        """Test create new audience."""

        response = requests.post(
            f"{pytest.API_URL}/{self.AUDIENCES}",
            json={
                "filters": self.DEFAULT_AUDIENCE_FILTERS,
                "name": f"E2E test_audiences Integration Test-"
                f"{int(time() * 1000)}",
            },
            headers=pytest.HEADERS,
        )

        # add the crud object to pytest for cleaning after
        pytest.CRUD_OBJECTS += [Crud(self.COLLECTION, response.json()["id"])]

        # test success
        self.assertEqual(HTTPStatus.CREATED, response.status_code)
        self.assertIsInstance(response.json(), dict)

    @record_test_result(
        HttpMethod.GET, Endpoints.ORCHESTRATION.GET_HISTOGRAM_DATA
    )
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

    @record_test_result(
        HttpMethod.GET, Endpoints.ORCHESTRATION.GET_HISTOGRAM_DATA
    )
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

    @record_test_result(
        HttpMethod.GET, Endpoints.ORCHESTRATION.GET_LOCATION_RULES_CONTSTANTS
    )
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

    @record_test_result(
        HttpMethod.GET, Endpoints.ORCHESTRATION.GET_AUDIENCE_INSIGHTS
    )
    def test_get_audience_insights(self):
        """Test get audience insights."""

        # Create the audience.
        response = requests.post(
            f"{pytest.API_URL}/{self.AUDIENCES}",
            json={
                "filters": self.DEFAULT_AUDIENCE_FILTERS,
                "name": f"E2E test_audiences Integration Test-"
                f"{int(time() * 1000)}",
            },
            headers=pytest.HEADERS,
        )

        audience_id = response.json().get("id")
        # add the crud object to pytest for cleaning after
        pytest.CRUD_OBJECTS += [Crud(self.COLLECTION, audience_id)]

        # test success
        self.assertEqual(HTTPStatus.CREATED, response.status_code)
        self.assertIsInstance(response.json(), dict)

        # Get Audience insights.
        response = requests.get(
            f"{pytest.API_URL}/{self.AUDIENCES}/{audience_id}/audience_insights",
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIsInstance(response.json(), dict)

    @record_test_result(
        HttpMethod.POST,
        Endpoints.ORCHESTRATION.POST_ADD_DESTINATION_TO_AUDIENCE,
    )
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
                "filters": self.DEFAULT_AUDIENCE_FILTERS,
                "name": f"E2E test_audiences Integration Test-"
                f"{int(time() * 1000)}",
            },
            headers=pytest.HEADERS,
        )

        audience_id = response.json().get("id")
        pytest.CRUD_OBJECTS += [Crud(self.COLLECTION, audience_id)]

        # test success
        self.assertEqual(HTTPStatus.CREATED, response.status_code)
        self.assertIsInstance(response.json(), dict)

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

    @record_test_result(
        HttpMethod.DELETE,
        Endpoints.ORCHESTRATION.DELETE_DESTINATION_FROM_AUDIENCE,
    )
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
                "filters": self.DEFAULT_AUDIENCE_FILTERS,
                "name": f"E2E test_audiences Integration Test-"
                f"{int(time() * 1000)}",
            },
            headers=pytest.HEADERS,
        )

        audience_id = response.json().get("id")
        pytest.CRUD_OBJECTS += [Crud(self.COLLECTION, audience_id)]

        # test success
        self.assertEqual(HTTPStatus.CREATED, response.status_code)
        self.assertIsInstance(response.json(), dict)

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

    @record_test_result(
        HttpMethod.GET, Endpoints.ORCHESTRATION.GET_AUDIENCE_INSIGHTS_COUNTRIES
    )
    def test_get_country_level_audience_insights(self):
        """Test get country level audience Insights."""

        # Create the audience.
        response = requests.post(
            f"{pytest.API_URL}/{self.AUDIENCES}",
            json={
                "filters": self.DEFAULT_AUDIENCE_FILTERS,
                "name": f"E2E test_audiences Integration Test-"
                f"{int(time() * 1000)}",
            },
            headers=pytest.HEADERS,
        )

        audience_id = response.json().get("id")
        pytest.CRUD_OBJECTS += [Crud(self.COLLECTION, audience_id)]

        # test success
        self.assertEqual(HTTPStatus.CREATED, response.status_code)
        self.assertIsInstance(response.json(), dict)

        response = requests.get(
            f"{pytest.API_URL}/{self.AUDIENCES}/{audience_id}/countries",
            headers=pytest.HEADERS,
        )
        # test success
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIsInstance(response.json(), list)

    @record_test_result(
        HttpMethod.GET, Endpoints.ORCHESTRATION.GET_AUDIENCE_INSIGHTS_STATES
    )
    def test_get_state_level_audience_insights(self):
        """Test get state level audience Insights."""

        # Create the audience.
        response = requests.post(
            f"{pytest.API_URL}/{self.AUDIENCES}",
            json={
                "filters": self.DEFAULT_AUDIENCE_FILTERS,
                "name": f"E2E test_audiences Integration Test-"
                f"{int(time() * 1000)}",
            },
            headers=pytest.HEADERS,
        )

        audience_id = response.json().get("id")
        pytest.CRUD_OBJECTS += [Crud(self.COLLECTION, audience_id)]

        # test success
        self.assertEqual(HTTPStatus.CREATED, response.status_code)
        self.assertIsInstance(response.json(), dict)

        response = requests.get(
            f"{pytest.API_URL}/{self.AUDIENCES}/{audience_id}/states",
            headers=pytest.HEADERS,
        )
        # test success
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIsInstance(response.json(), list)

    @record_test_result(
        HttpMethod.GET, Endpoints.ORCHESTRATION.GET_AUDIENCE_INSIGHTS_CITIES
    )
    def test_get_city_level_audience_insights(self):
        """Test get city level audience Insights."""

        # Create the audience.
        response = requests.post(
            f"{pytest.API_URL}/{self.AUDIENCES}",
            json={
                "filters": self.DEFAULT_AUDIENCE_FILTERS,
                "name": f"E2E test_audiences Integration Test-"
                f"{int(time() * 1000)}",
            },
            headers=pytest.HEADERS,
        )

        audience_id = response.json().get("id")
        pytest.CRUD_OBJECTS += [Crud(self.COLLECTION, audience_id)]

        # test success
        self.assertEqual(HTTPStatus.CREATED, response.status_code)
        self.assertIsInstance(response.json(), dict)

        response = requests.get(
            f"{pytest.API_URL}/{self.AUDIENCES}/{audience_id}/cities",
            headers=pytest.HEADERS,
        )
        # test success
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIsInstance(response.json(), list)

    @record_test_result(
        HttpMethod.GET, Endpoints.ORCHESTRATION.GET_DOWNLOAD_AUDIENCE
    )
    def test_get_audience_download(self):
        """Test download audience file."""
        # Create the audience.
        response = requests.post(
            f"{pytest.API_URL}/{self.AUDIENCES}",
            json={
                "filters": self.DEFAULT_AUDIENCE_FILTERS,
                "name": f"E2E test_audiences Integration Test-"
                f"{int(time() * 1000)}",
            },
            headers=pytest.HEADERS,
        )

        audience_id = response.json().get("id")
        pytest.CRUD_OBJECTS += [Crud(self.COLLECTION, audience_id)]

        # test success
        self.assertEqual(HTTPStatus.CREATED, response.status_code)
        self.assertIsInstance(response.json(), dict)

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

    @record_test_result(HttpMethod.GET, Endpoints.ORCHESTRATION.GET_AUDIENCE)
    def test_get_audience_by_id(self):
        """Test get audience by id."""

        response = requests.post(
            f"{pytest.API_URL}/{self.AUDIENCES}",
            json={
                "filters": self.DEFAULT_AUDIENCE_FILTERS,
                "name": f"E2E test_audiences Integration Test-"
                f"{int(time() * 1000)}",
            },
            headers=pytest.HEADERS,
        )

        audience_id = response.json().get("id")
        pytest.CRUD_OBJECTS += [Crud(self.COLLECTION, audience_id)]

        # test success
        self.assertEqual(HTTPStatus.CREATED, response.status_code)
        self.assertIsInstance(response.json(), dict)

        response = requests.get(
            f"{pytest.API_URL}/{self.AUDIENCES}/{audience_id}",
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIsInstance(response.json(), dict)

    @record_test_result(
        HttpMethod.PUT, Endpoints.ORCHESTRATION.PUT_UPDATE_AUDIENCE
    )
    def test_update_audience(self):
        """Test update audience."""

        response = requests.post(
            f"{pytest.API_URL}/{self.AUDIENCES}",
            json={
                "filters": self.DEFAULT_AUDIENCE_FILTERS,
                "name": f"E2E test_audiences Integration Test-"
                f"{int(time() * 1000)}",
            },
            headers=pytest.HEADERS,
        )

        audience_id = response.json().get("id")
        pytest.CRUD_OBJECTS += [Crud(self.COLLECTION, audience_id)]

        # test success
        self.assertEqual(HTTPStatus.CREATED, response.status_code)
        self.assertIsInstance(response.json(), dict)

        response = requests.put(
            f"{pytest.API_URL}/{self.AUDIENCES}/{audience_id}",
            json={
                "filters": self.DEFAULT_AUDIENCE_FILTERS,
            },
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIsInstance(response.json(), dict)

    @record_test_result(
        HttpMethod.DELETE, Endpoints.ORCHESTRATION.DELETE_AUDIENCE
    )
    def test_delete_audience(self):
        """Test delete audience."""

        response = requests.post(
            f"{pytest.API_URL}/{self.AUDIENCES}",
            json={
                "filters": self.DEFAULT_AUDIENCE_FILTERS,
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

    @record_test_result(
        HttpMethod.POST, Endpoints.ORCHESTRATION.POST_CREATE_LOOKALIKE_AUDIENCE
    )
    def test_create_and_update_lookalike_audience(self):
        """Test create and update lookalike audience."""
        # TODO https://jira.hux.deloitte.com/browse/HUS-3678

        # get all audiences to get a lookalikable active source audience id
        response = requests.get(
            f"{pytest.API_URL}/{self.AUDIENCES}", headers=pytest.HEADERS
        )
        # test success
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIsInstance(response.json(), dict)

        source_audience_id = None
        lookalikeable_audiences_id = [
            source_audience["id"]
            for source_audience in response.json()["audiences"]
            if source_audience
            and "lookalikeable" in source_audience
            and source_audience["lookalikeable"] == "Active"
        ]
        if lookalikeable_audiences_id and len(lookalikeable_audiences_id) > 0:
            source_audience_id = lookalikeable_audiences_id[0]

        if source_audience_id:
            response = requests.post(
                f"{pytest.API_URL}/{self.LOOKALIKE_AUDIENCES}",
                json={
                    "name": f"E2E test_orchestration Integration Test-"
                    f"{int(time() * 1000)}",
                    "audience_id": source_audience_id,
                    "audience_size_percentage": 1.5,
                },
                headers=pytest.HEADERS,
            )

            lookalike_audience_id = response.json().get("id")
            pytest.CRUD_OBJECTS += [
                Crud(
                    self.LOOKALIKE_AUDIENCES_COLLECTION, lookalike_audience_id
                )
            ]

            # test success
            self.assertEqual(HTTPStatus.ACCEPTED, response.status_code)
            self.assertIsInstance(response.json(), dict)

            updated_lookalike_audience_name = (
                f"E2E test_orchestration Integration Test-{int(time() * 1000)}"
            )

            response = requests.put(
                f"{pytest.API_URL}/{self.LOOKALIKE_AUDIENCES}/"
                f"{lookalike_audience_id}",
                json={"name": updated_lookalike_audience_name},
                headers=pytest.HEADERS,
            )

            # test success
            self.assertEqual(HTTPStatus.OK, response.status_code)
            self.assertIsInstance(response.json(), dict)
            self.assertEqual(
                updated_lookalike_audience_name, response.json()["name"]
            )
