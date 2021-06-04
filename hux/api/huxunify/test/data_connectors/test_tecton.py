"""
purpose of this file is to house all the tecton api tests.
"""
import json
from unittest import TestCase
import requests_mock
from requests_mock import Mocker
from bson import json_util
from huxunify.api import constants
from huxunify.api.config import get_config
from huxunify.api.data_connectors import tecton


MOCK_MODEL_RESPONSE = {
    "results": [
        {
            "features": [
                "2021-05-04 00:00:00",
                "LTV prediction of Customers over 30 days"
                "proxy from 2021-04-04 using Hux Blueprints",
                "2021-04-04 00:00:00",
                "365",
                "HUS",
                "ltv-model-365-30",
                "Dave Smith",
                "dsmith@domain.com",
                None,
            ],
            "joinKeys": ["0.2.1"],
        },
        {
            "features": [
                "2021-05-05 00:00:00",
                "LTV prediction of Customers over 30 days"
                "proxy from 2021-04-05 using Hux Blueprints",
                "2021-04-05 00:00:00",
                "365",
                "HUS",
                "ltv-model-365-30",
                "Dave Smith",
                "dsmith@domain.com",
                None,
            ],
            "joinKeys": ["0.2.2"],
        },
        {
            "features": [
                "2021-05-06 00:00:00",
                "LTV prediction of Customers over 30 days"
                " proxy from 2021-04-06 using Hux Blueprints",
                "2021-04-06 00:00:00",
                "365",
                "HUS",
                "ltv-model-365-30",
                "Dave Smith",
                "dsmith@domain.com",
                None,
            ],
            "joinKeys": ["0.2.3"],
        },
        {
            "features": [
                "2021-05-07 00:00:00",
                "LTV prediction of Customers over 30 days"
                " proxy from 2021-04-07 using Hux Blueprints",
                "2021-04-07 00:00:00",
                "365",
                "HUS",
                "ltv-model-365-30",
                "Dave Smith",
                "dsmith@domain.com",
                None,
            ],
            "joinKeys": ["0.2.4"],
        },
    ]
}


class TectonTest(TestCase):
    """
    Test Tecton request methods
    """

    def setUp(self) -> None:
        """Setup tests

        Returns:

        """
        self.config = get_config()

    @requests_mock.Mocker()
    def test_list_models(self, request_mocker: Mocker):
        """Test list models

        Args:
            request_mocker (Mocker): Request mock object.

        Returns:

        """

        # setup the request mock post
        request_mocker.post(
            self.config.TECTON_FEATURE_SERVICE,
            text=json.dumps(MOCK_MODEL_RESPONSE, default=json_util.default),
            headers=self.config.TECTON_API_HEADERS,
        )

        models = tecton.get_models(model_ids=[1])

        # test that it was actually called and only once
        self.assertEqual(request_mocker.call_count, 1)
        self.assertTrue(request_mocker.called)

        # test correct payload sent
        self.assertDictEqual(
            request_mocker.last_request.json(), constants.MODEL_LIST_PAYLOAD
        )

        self.assertEqual(models[0][constants.LATEST_VERSION], "0.2.4")
        self.assertEqual(models[0][constants.PAST_VERSION_COUNT], 3)

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
