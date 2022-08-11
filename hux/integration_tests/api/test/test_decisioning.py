"""Purpose of this file is to integration test for models."""
from time import time
from unittest import TestCase
from http import HTTPStatus
import pytest
import requests
from prometheus_metrics import record_test_result, HttpMethod, Endpoints
from huxunify.api import constants as api_c

class TestModels(TestCase):
    """Test Models/Decisioning."""

    MODELS = "models"
    COLLECTION = "models"

    def setUp(self) -> None:
        """Setup resources before each test."""

        get_models_response = requests.get(
            f"{pytest.API_URL}/{self.MODELS}",
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.OK, get_models_response.status_code)
        self.assertIsInstance(get_models_response.json(), list)

        # get the model id for propensity to open model
        self.test_model_id = [
            model["id"]
            for model in get_models_response.json()
            if api_c.ID in model
        ][0]

    @record_test_result(HttpMethod.POST, Endpoints.MODEL.POST_REQUEST_MODEL)
    def test_create_and_delete_model(self):
        """Test creating and deleting a model."""
        # TODO https://jira.hux.deloitte.com/browse/HUS-3637

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

    @record_test_result(HttpMethod.GET, Endpoints.MODEL.GET_ALL_MODELS)
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

    @record_test_result(
        HttpMethod.GET, Endpoints.MODEL.GET_MODEL_PIPELINE_PERFORMANCE
    )
    def test_get_model_pipeline_performance(self):
        """Test get model's pipeline performance."""

        # get the pipeline-performance of model
        fetch_response = requests.get(
            f"{pytest.API_URL}/{self.MODELS}/"
            f"{self.test_model_id}/pipeline-performance",
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.OK, fetch_response.status_code)
        self.assertIsInstance(fetch_response.json(), dict)
        self.assertIsNotNone(fetch_response.json()["training"])
        self.assertIsNotNone(fetch_response.json()["scoring"])

    @record_test_result(
        HttpMethod.GET, Endpoints.MODEL.GET_MODEL_VERSION_HISTORY
    )
    def test_get_model_version_history(self):
        """Test get model's version history."""

        # get the version-history of model
        fetch_response = requests.get(
            f"{pytest.API_URL}/{self.MODELS}/"
            f"{self.test_model_id}/version-history",
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.OK, fetch_response.status_code)
        self.assertIsInstance(fetch_response.json(), list)

    @record_test_result(HttpMethod.GET, Endpoints.MODEL.GET_MODEL_OVERVIEW)
    def test_get_model_overview(self):
        """Test get model's overview."""

        # get the overview of model
        fetch_response = requests.get(
            f"{pytest.API_URL}/{self.MODELS}/"
            f"{self.test_model_id}/overview",
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.OK, fetch_response.status_code)
        self.assertIsInstance(fetch_response.json(), dict)

    @record_test_result(HttpMethod.GET, Endpoints.MODEL.GET_MODEL_FEATURES)
    def test_get_model_features(self):
        """Test get model's features."""

        # get the features of model
        fetch_response = requests.get(
            f"{pytest.API_URL}/{self.MODELS}/"
            f"{self.test_model_id}/features",
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.OK, fetch_response.status_code)
        self.assertIsInstance(fetch_response.json(), list)

    @record_test_result(HttpMethod.GET, Endpoints.MODEL.GET_MODEL_DRIFT)
    def test_get_model_drift(self):
        """Test get model's drift."""

        # get the drift of model
        fetch_response = requests.get(
            f"{pytest.API_URL}/{self.MODELS}/" f"{self.test_model_id}/drift",
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.OK, fetch_response.status_code)
        self.assertIsInstance(fetch_response.json(), list)

    @record_test_result(HttpMethod.GET, Endpoints.MODEL.GET_MODEL_LIFT)
    def test_get_model_lift(self):
        """Test get model's lift."""

        # get the lift of model
        fetch_response = requests.get(
            f"{pytest.API_URL}/{self.MODELS}/" f"{self.test_model_id}/lift",
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.OK, fetch_response.status_code)
        self.assertIsInstance(fetch_response.json(), list)
