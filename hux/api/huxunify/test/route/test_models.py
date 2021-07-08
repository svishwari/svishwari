"""
Purpose of this file is to house all the models api tests
"""
from unittest import TestCase, mock
from http import HTTPStatus
import requests_mock
import mongomock

from huxunifylib.database.client import DatabaseClient
import huxunify.test.constants as t_c
from huxunify.api import constants as api_c
from huxunify.app import create_app

MOCK_MODEL_RESPONSE = {
    "results": [
        {
            "features": [
                "2021-04-26 00:00:00",
                "Propensity of a customer making a purchase after "
                "receiving an email.",
                "2021-04-26 00:00:00",
                "365",
                "Propensity to Unsubscribe",
                "unsubscribe",
                "Susan Miller",
                "smiller@xyz.com",
                "success",
                "0.2.4",
            ],
            "joinKeys": ["1"],
        },
        {
            "features": [
                "2021-01-25 00:00:00",
                "Predict the lifetime value of a customer.",
                "2021-01-25 00:00:00",
                "365",
                "Lifetime Value",
                "ltv",
                "John Smith",
                "jsmith@xyz.com",
                "success",
                "0.4.5",
            ],
            "joinKeys": ["2"],
        },
    ]
}


class TestModelRoutes(TestCase):
    """Test Model Endpoints"""

    def setUp(self) -> None:
        """
        Setup resources before each test

        Args:

        Returns:
        """

        # mock request for introspect call
        self.request_mocker = requests_mock.Mocker()
        self.request_mocker.post(t_c.INTROSPECT_CALL, json=t_c.VALID_RESPONSE)
        self.request_mocker.start()

        self.app = create_app().test_client()

        # init mongo patch initially
        mongo_patch = mongomock.patch(servers=(("localhost", 27017),))
        mongo_patch.start()

        # setup the mock DB client
        self.database = DatabaseClient(
            "localhost", 27017, None, None
        ).connect()

        self.addCleanup(mock.patch.stopall)

    def test_get_all_models(self):
        """
        Test get all models from Tecton

        Args:

        Returns:

        """
        self.request_mocker.stop()
        self.request_mocker.post(
            t_c.TEST_CONFIG.TECTON_FEATURE_SERVICE,
            json=MOCK_MODEL_RESPONSE,
        )
        self.request_mocker.start()

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.MODELS_ENDPOINT}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(2, len(response.json))

    def test_retrieve_performance_metrics_for_model(self):
        """
        Test get performance metrics for a model from Tecton

        Args:

        Returns:

        """

        model_name = "model1"
        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.MODELS_ENDPOINT}/{model_name}/performance-metrics",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual([], response.json)

    def test_retrieve_feature_importance_for_model(self):
        """
        Test get performance metrics for a model from Tecton

        Args:

        Returns:

        """
        model_name = "model1"
        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.MODELS_ENDPOINT}/{model_name}/feature-importance",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual([], response.json)

    def test_retrieve_version_history_for_model(self):
        """
        Test get version history for a model from Tecton

        Args:

        Returns:

        """
        model_name = "model1"
        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.MODELS_ENDPOINT}/{model_name}/version-history",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual([], response.json)

    def test_retrieve_features_for_model(self):
        """
        Test get features for a model from Tecton

        Args:

        Returns:

        """
        model_name = "model1"
        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.MODELS_ENDPOINT}/{model_name}/features",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual([], response.json)

    def test_retrieve_drift_details_for_model(self):
        """
        Test get drift details for a model from Tecton

        Args:

        Returns:

        """
        model_name = "model1"
        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.MODELS_ENDPOINT}/{model_name}/drift",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual([], response.json)

    def test_retrieve_lift_details_for_model(self):
        """
        Test get lift details for a model from Tecton

        Args:

        Returns:

        """
        model_name = "model1"
        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.MODELS_ENDPOINT}/{model_name}/lift",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual([], response.json)
