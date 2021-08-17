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
from huxunify.test import constants as t_c


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

        models = tecton.get_models()

        # test that it was actually called and only once
        self.assertEqual(request_mocker.call_count, 1)
        self.assertTrue(request_mocker.called)

        # test correct payload sent
        self.assertDictEqual(
            request_mocker.last_request.json(), constants.MODEL_LIST_PAYLOAD
        )

        self.assertEqual(models[0][constants.LATEST_VERSION], "0.2.4")
        self.assertEqual(models[0][constants.PAST_VERSION_COUNT], 0)

    @requests_mock.Mocker()
    def test_map_model_performance_response_ltv(self, request_mocker: Mocker):
        """Test map model performance response for ltv.

        Args:
            request_mocker (Mocker): Request mock object.

        Returns:

        """
        # setup the request mock post
        request_mocker.post(
            self.config.TECTON_FEATURE_SERVICE,
            text=json.dumps(
                t_c.MOCKED_MODEL_PERFORMANCE_LTV, default=json_util.default
            ),
            headers=self.config.TECTON_API_HEADERS,
        )

        model = tecton.get_model_performance_metrics(
            2, constants.LTV, "21.7.30"
        )

        # test that it was actually called and only once
        self.assertEqual(request_mocker.call_count, 1)
        self.assertTrue(request_mocker.called)

        # test correct payload sent
        self.assertDictEqual(
            request_mocker.last_request.json(), t_c.MOCKED_MODEL_LTV_PAYLOAD
        )
        self.assertDictEqual(
            model,
            {
                constants.ID: 2,
                constants.RMSE: 215.5,
                constants.AUC: 0,
                constants.PRECISION: 0,
                constants.RECALL: 0,
                constants.CURRENT_VERSION: "21.7.30",
            },
        )

    @requests_mock.Mocker()
    def test_map_model_performance_response_unsubscribe(
        self, request_mocker: Mocker
    ):
        """Test map model performance response for unsubscribe.

        Args:
            request_mocker (Mocker): Request mock object.

        Returns:

        """
        # setup the request mock post
        request_mocker.post(
            self.config.TECTON_FEATURE_SERVICE,
            text=json.dumps(
                t_c.MOCKED_MODEL_PERFORMANCE_UNSUBSCRIBE,
                default=json_util.default,
            ),
            headers=self.config.TECTON_API_HEADERS,
        )

        model = tecton.get_model_performance_metrics(
            1, constants.UNSUBSCRIBE, "21.7.31"
        )

        # test that it was actually called and only once
        self.assertEqual(request_mocker.call_count, 1)
        self.assertTrue(request_mocker.called)

        # test correct payload sent
        self.assertDictEqual(
            request_mocker.last_request.json(),
            t_c.MOCKED_MODEL_UNSUBSCRIBE_PAYLOAD,
        )
        self.assertDictEqual(
            model,
            {
                constants.ID: 1,
                constants.RMSE: 0,
                constants.AUC: 0.85,
                constants.PRECISION: 0.71,
                constants.RECALL: 0.58,
                constants.CURRENT_VERSION: "21.7.31",
            },
        )

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
