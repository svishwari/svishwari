"""
purpose of this file is to house all the tecton api tests.
"""
from json import dumps
from unittest import TestCase
import requests
from huxunify.api import config


class TectonTest(TestCase):
    """
    Test Tecton request methods
    """

    def test_list_models(self):
        """test list models"""

        # setup the payload
        payload = dumps(
            {
                "params": {
                    "feature_service_name": "ui_metadata_models_service",
                    "join_key_map": {
                        "model_name": "ltv-model-365-30",
                        "version_number": "0.0.1",
                    },
                }
            }
        )

        # submit the post request to get the models
        response = requests.post(
            config.TECTON_FEATURE_SERVICE,
            payload,
            headers=config.TECTON_API_HEADERS,
        )

        # validate the response.
        self.assertEqual(response.status_code, 200)

        # validate the model response.
        self.assertDictEqual(response.json(), {})

    def test_model_version_history(self):
        """test model version history"""

        # setup the payload
        payload = dumps(
            {
                "params": {
                    "feature_service_name": "ui_metadata_models_service",
                    "join_key_map": {
                        "model_name": "ltv-model-365-30",
                        "version_number": "0.0.1",
                    },
                }
            }
        )

        # submit the post request to get the models
        response = requests.post(
            config.TECTON_FEATURE_SERVICE,
            payload,
            headers=config.TECTON_API_HEADERS,
        )

        # validate the response.
        self.assertEqual(response.status_code, 200)

        # validate the model response.
        self.assertDictEqual(response.json(), {})

    def test_list_features(self):
        """test list features for a model"""

        # TODO - when available.
        self.assertEqual(2 + 2, 4)

    def test_performance_metrics(self):
        """test getting performance metrics for a model"""

        # TODO - when available.
        self.assertEqual(2 + 2, 4)

    def test_feature_importance(self):
        """test getting feature importance for a model"""

        # TODO - when available.
        self.assertEqual(2 + 2, 4)

    def test_lift_chart(self):
        """test getting lift charts for a model"""

        # TODO - when available.
        self.assertEqual(2 + 2, 4)

    def test_drift(self):
        """test getting drif for a model"""

        # TODO - when available.
        self.assertEqual(2 + 2, 4)
