"""Purpose of this file is to integration test for models."""
from time import time
from unittest import TestCase
from http import HTTPStatus
import pytest
import requests


class TestModels(TestCase):
    """Test Models/Decisioning."""

    MODELS = "models"
    COLLECTION = "models"

    def test_create_and_delete_model(self):
        """Test creating and deleting a model."""

        create_response = requests.post(
            f"{pytest.API_URL}/{self.MODELS}",
            json=[
                {
                    "type": "model",
                    "name": f"E2E test_decisioning Integration Test-"
                    f"{int(time() * 1000)}",
                    "id": "9a44c346ba034ac8a699ae0ab3314003",
                    "status": "requested",
                }
            ],
            headers=pytest.HEADERS,
        )

        # test create success
        self.assertEqual(HTTPStatus.OK, create_response.status_code)
        self.assertIsInstance(create_response.json(), list)
        self.assertEqual(len(create_response.json()), 1)

        delete_response = requests.delete(
            f"{pytest.API_URL}/{self.MODELS}?"
            f'model_id={create_response.json()[0]["id"]}',
            headers=pytest.HEADERS,
        )

        # test delete success
        self.assertEqual(HTTPStatus.OK, delete_response.status_code)
        self.assertIsInstance(delete_response.json(), dict)

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
        """Test updating a model."""

        model_name = (
            f"E2E test_decisioning Integration Test-{int(time() * 1000)}"
        )

        # create a test model to update it
        create_response = requests.post(
            f"{pytest.API_URL}/{self.MODELS}",
            json=[
                {
                    "type": "Classification",
                    "name": model_name,
                    "id": "9a44c346ba034ac8a699ae0ab3314003",
                    "category": "Email",
                    "description": "Likelihood of customer to purchase",
                    "status": "requested",
                    "is_added": True,
                }
            ],
            headers=pytest.HEADERS,
        )

        # test model created successfully
        self.assertEqual(HTTPStatus.OK, create_response.status_code)
        self.assertIsInstance(create_response.json(), list)
        self.assertEqual(len(create_response.json()), 1)
        self.assertEqual(model_name, create_response.json()[0]["name"])

        update_response = requests.patch(
            f"{pytest.API_URL}/{self.MODELS}",
            json=[
                {
                    "id": create_response.json()[0]["id"],
                    "type": "Classification",
                    "name": model_name,
                    "description": "Likelihood of customer to purchase updated",
                }
            ],
            headers=pytest.HEADERS,
        )

        # test update success
        self.assertEqual(HTTPStatus.OK, update_response.status_code)
        self.assertIsInstance(update_response.json(), list)
        self.assertEqual(len(update_response.json()), 1)
        self.assertEqual(model_name, update_response.json()[0]["name"])
        self.assertEqual(
            "Likelihood of customer to purchase updated",
            update_response.json()[0]["description"],
        )

        # now delete the model from DB
        delete_response = requests.delete(
            f"{pytest.API_URL}/{self.MODELS}?"
            f'model_id={create_response.json()[0]["id"]}',
            headers=pytest.HEADERS,
        )

        # test delete success
        self.assertEqual(HTTPStatus.OK, delete_response.status_code)
        self.assertIsInstance(delete_response.json(), dict)

    def test_get_model_by_id_pipeline_performance(self):
        """Test get model by ID."""

        # create a test model to fetch by ID
        create_response = requests.post(
            f"{pytest.API_URL}/{self.MODELS}",
            json=[
                {
                    "type": "model",
                    "name": f"E2E test_decisioning Integration Test-"
                    f"{int(time() * 1000)}",
                    "id": "9a44c346ba034ac8a699ae0ab3314003",
                    "status": "requested",
                }
            ],
            headers=pytest.HEADERS,
        )

        # test model created successfully
        self.assertEqual(HTTPStatus.OK, create_response.status_code)
        self.assertIsInstance(create_response.json(), list)
        self.assertEqual(len(create_response.json()), 1)

        model_id = create_response.json()[0]["id"]

        # get the model by id
        fetch_response = requests.get(
            f"{pytest.API_URL}/{self.MODELS}/{model_id}/pipeline-performance",
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.OK, fetch_response.status_code)
        self.assertIsInstance(fetch_response.json(), dict)
        self.assertIsNotNone(fetch_response.json()["training"])
        self.assertIsNotNone(fetch_response.json()["scoring"])
