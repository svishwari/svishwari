"""Purpose of this file is to integration test for models."""
from unittest import TestCase
from http import HTTPStatus
import pytest
import requests
from hux.integration_tests.api.test.conftest import Crud


class TestModels(TestCase):
    """Test Models / Decisioning."""

    MODELS = "models"
    COLLECTION = "models"

    def test_create_model(self):
        """Test creating an model."""

        response = requests.post(
            f"{pytest.API_URL}/{self.MODELS}",
            json=[
                {
                    "type": "purchase",
                    "name": "Propensity to Purchase",
                    "id": "9a44c346ba034ac8a699ae0ab3314003",
                    "status": "requested",
                },
                {
                    "type": "unsubscribe",
                    "name": "Propensity to Unsubscribe",
                    "id": "eb5f35e34c0047d3b9022ef330952dd1",
                    "status": "requested",
                },
            ],
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.CREATED, response.status_code)
        self.assertIsInstance(response.json(), dict)

        # add the crud object to pytest for cleaning after
        pytest.CRUD_OBJECTS += [Crud(self.COLLECTION, response.json()["id"])]

    def test_get_models(self):
        """Test get all models."""

        response = requests.get(
            f"{pytest.API_URL}/{self.MODELS}",
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIsInstance(response.json(), list)
        self.assertGreaterEqual(len(response.json()), 1)

    def test_update_model(self):
        """Test updating an model."""

        # create a test model to update it
        create_response = requests.post(
            f"{pytest.API_URL}/{self.MODELS}",
            json=[
                {
                    "type": "Classification",
                    "name": "Propensity to Purchase",
                    "category": "Email",
                    "description": "Likelihood of customer to purchase",
                    "status": "requested",
                    "is_added": True,
                }
            ],
            headers=pytest.HEADERS,
        )

        # test model created successfully
        self.assertEqual(HTTPStatus.CREATED, create_response.status_code)
        self.assertIsInstance(create_response.json(), dict)

        model_id = create_response.json()["id"]

        # test model name
        self.assertEqual(
            "Propensity to Purchase", create_response.json()["name"]
        )

        update_response = requests.patch(
            f"{pytest.API_URL}/{self.MODELS}",
            json=[
                {
                    "id": model_id,
                    "type": "Classification",
                    "name": "Propensity to Purchase - Updated",
                    "category": "Email",
                    "description": "Likelihood of customer to purchase",
                    "status": "requested",
                    "is_added": True,
                }
            ],
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.OK, update_response.status_code)
        self.assertIsInstance(update_response.json(), dict)
        self.assertEqual(model_id, update_response.json()["id"])
        self.assertEqual(
            "Propensity to Purchase - Updated", update_response.json()["name"]
        )
        # add the crud object to pytest for cleaning after
        pytest.CRUD_OBJECTS += [Crud(self.COLLECTION, model_id)]

    def test_delete_model(self):
        """Test deleting an model."""

        # create a test model to delete it
        create_response = requests.post(
            f"{pytest.API_URL}/{self.MODELS}",
            json=[
                {
                    "type": "Classification",
                    "name": "Propensity to Purchase",
                    "category": "Email",
                    "description": "Likelihood of customer to purchase",
                    "status": "requested",
                    "is_added": True,
                }
            ],
            headers=pytest.HEADERS,
        )

        # test model created successfully
        self.assertEqual(HTTPStatus.CREATED, create_response.status_code)
        self.assertIsInstance(create_response.json(), dict)

        model_id = create_response.json()["id"]

        delete_response = requests.delete(
            f"{pytest.API_URL}/{self.MODELS}?model_id={model_id}",
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.NO_CONTENT, delete_response.status_code)

        # add the crud object to pytest for cleaning after
        pytest.CRUD_OBJECTS += [Crud(self.COLLECTION, model_id)]

    def test_get_model_by_id_pipeline_performance(self):
        """Test get model by ID."""

        # create a test model to fetch by ID
        create_response = requests.post(
            f"{pytest.API_URL}/{self.MODELS}/pipeline-performance",
            json=[
                {
                    "type": "purchase",
                    "name": "Propensity to Purchase",
                    "id": "9a44c346ba034ac8a699ae0ab3314003",
                    "status": "requested",
                }
            ],
            headers=pytest.HEADERS,
        )

        # test model created successfully
        self.assertEqual(HTTPStatus.CREATED, create_response.status_code)
        self.assertIsInstance(create_response.json(), dict)

        model_id = create_response.json()["id"]

        # get the model by id
        fetch_response = requests.get(
            f"{pytest.API_URL}/{self.MODELS}/{model_id}/pipeline-performance",
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.OK, fetch_response.status_code)
        self.assertIsInstance(fetch_response.json(), dict)
        self.assertEqual(model_id, fetch_response.json()["id"])
        self.assertIsNone(fetch_response.json()["training"])
        self.assertIsNone(fetch_response.json()["scoring"])

        # add the crud object to pytest for cleaning after
        pytest.CRUD_OBJECTS += [Crud(self.COLLECTION, model_id)]
