"""
purpose of this file is to house all the tecton api tests.
"""
import json
from unittest import TestCase
import requests_mock
from requests_mock import Mocker
from huxunify.api import config
from huxunify.api import constants
from huxunify.api.data_connectors import tecton


class TectonTest(TestCase):
    """
    Test Tecton request methods
    """

    @requests_mock.Mocker()
    def test_list_models(self, request_mocker: Mocker):
        """Test list models

        Args:
            request_mocker (str): Request mock object.

        Returns:

        """

        # setup the request mock post
        request_mocker.post(
            config.TECTON_FEATURE_SERVICE,
            text=json.dumps(constants.MODEL_LIST_PAYLOAD),
            headers=config.TECTON_API_HEADERS,
        )

        models = tecton.get_models(constants.MODEL_LIST_PAYLOAD)

        # test that it was actually called and only once
        self.assertEqual(request_mocker.call_count, 1)
        self.assertTrue(request_mocker.called)

        # test correct payload sent
        self.assertDictEqual(
            request_mocker.last_request.json(), constants.MODEL_LIST_PAYLOAD
        )
        # test correct headers sent.
        self.assertEqual(models.headers, config.TECTON_API_HEADERS)

    def test_model_version_history(self):
        """test model version history"""

        # TODO - when available.
        self.assertEqual(2 + 2, 4)

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
