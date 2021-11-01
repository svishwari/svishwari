"""Purpose of this file is to house all the tecton api tests."""
import json
import string
from unittest import TestCase, mock
from datetime import datetime
import requests_mock
from requests_mock import Mocker
from bson import json_util
from hypothesis import given, strategies as st

from huxunify.api import constants
from huxunify.api.config import get_config
from huxunify.api.data_connectors import tecton
from huxunify.api.exceptions.integration_api_exceptions import (
    FailedAPIDependencyError,
    EmptyAPIResponseError,
)
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
    """Test Tecton request API endpoint methods."""

    def setUp(self) -> None:
        """Setup tests."""

        self.config = get_config()

    @requests_mock.Mocker()
    def test_list_models(self, request_mocker: Mocker):
        """Test list models.

        Args:
            request_mocker (Mocker): Request mock object.
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
                constants.AUC: -1,
                constants.PRECISION: -1,
                constants.RECALL: -1,
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
                constants.RMSE: -1,
                constants.AUC: 0.85,
                constants.PRECISION: 0.71,
                constants.RECALL: 0.58,
                constants.CURRENT_VERSION: "21.7.31",
            },
        )

    @requests_mock.Mocker()
    def test_map_model_performance_response_empty_response(
        self, request_mocker: Mocker
    ):
        """Test map model performance response for an empty response.

        Args:
            request_mocker (Mocker): Request mock object.
        """

        # setup the request mock post
        request_mocker.post(
            self.config.TECTON_FEATURE_SERVICE,
            text=json.dumps(
                {},
                default=json_util.default,
            ),
            headers=self.config.TECTON_API_HEADERS,
        )

        self.assertFalse(
            tecton.get_model_performance_metrics(
                1, constants.UNSUBSCRIBE, "21.7.31"
            )
        )

    @requests_mock.Mocker()
    def test_model_version_history(self, request_mocker: Mocker):
        """Test model version history.

        Args:
            request_mocker (Mocker): Request mock object.
        """

        # setup the request mock post
        request_mocker.post(
            self.config.TECTON_FEATURE_SERVICE,
            text=json.dumps(
                t_c.MOCKED_MODEL_VERSION_HISTORY,
                default=json_util.default,
            ),
            headers=self.config.TECTON_API_HEADERS,
        )

        models = tecton.get_model_version_history(1)

        # test that it was actually called and only once
        self.assertEqual(request_mocker.call_count, 1)
        self.assertTrue(request_mocker.called)

        self.assertTrue(models)

        # test the last model
        self.assertDictEqual(
            models[-1],
            {
                "id": 1,
                "last_trained": datetime(2021, 7, 31, 0, 0),
                "description": "Propensity of a customer unsubscribing "
                "after receiving an email.",
                "fulcrum_date": datetime(2021, 7, 17, 0, 0),
                "lookback_window": 90,
                "name": "Propensity to Unsubscribe",
                "type": "unsubscribe",
                "owner": "Susan Miller",
                "status": "Active",
                "current_version": "21.7.31",
                "prediction_window": 90,
            },
        )

    @requests_mock.Mocker()
    def test_get_model_features_success(self, request_mocker: Mocker) -> None:
        """Test get features for a model.

        Args:
            request_mocker (Mocker): request mocker object.
        """

        # setup the request mock post
        request_mocker.post(
            self.config.TECTON_FEATURE_SERVICE,
            text=json.dumps(
                t_c.MOCKED_MODEL_PROPENSITY_FEATURES,
                default=json_util.default,
            ),
            headers=self.config.TECTON_API_HEADERS,
        )

        model_features = tecton.get_model_features(1, "21.7.30")

        self.assertTrue(model_features)

    @requests_mock.Mocker()
    def test_get_model_features_negative_score_success(
        self, request_mocker: Mocker
    ) -> None:
        """Test get features for a model.

        Args:
            request_mocker (Mocker): request mocker object.
        """

        # setup the request mock post
        request_mocker.post(
            self.config.TECTON_FEATURE_SERVICE,
            text=json.dumps(
                t_c.MOCKED_MODEL_PROPENSITY_FEATURES_NEGATIVE_SCORE,
                default=json_util.default,
            ),
            headers=self.config.TECTON_API_HEADERS,
        )

        model_features = tecton.get_model_features(1, "21.7.30")

        self.assertTrue(model_features)
        self.assertTrue(
            all((feature[constants.SCORE] < 0 for feature in model_features))
        )

    def test_lift_chart(self):
        """Test getting lift charts for a model."""

        # TODO- find async post mocker
        mock.patch(
            "huxunify.api.data_connectors.tecton.get_model_lift_async",
            return_value=t_c.MOCKED_MODEL_LIFT_CHART,
        ).start()

        lift_data = tecton.get_model_lift_async(1)

        self.assertTrue(lift_data)

        # test the last lift chart data
        self.assertDictEqual(
            lift_data[-1],
            {
                constants.BUCKET: 100,
                constants.ACTUAL_VALUE: 2602,
                constants.ACTUAL_LIFT: 1,
                constants.PREDICTED_LIFT: 1.0000000895,
                constants.PREDICTED_VALUE: 2726.7827,
                constants.PROFILE_COUNT: 95369,
                constants.ACTUAL_RATE: 0.0272834988,
                constants.PREDICTED_RATE: 0.0285919189,
                constants.PROFILE_SIZE_PERCENT: 0,
            },
        )

    @requests_mock.Mocker()
    def test_drift(self, request_mocker: Mocker):
        """Test getting drift charts for a model.

        Args:
            request_mocker (Mocker): request mocker object.
        """

        # setup the request mock post
        request_mocker.post(
            self.config.TECTON_FEATURE_SERVICE,
            text=json.dumps(
                t_c.MOCKED_MODEL_DRIFT,
                default=json_util.default,
            ),
            headers=self.config.TECTON_API_HEADERS,
        )

        drift_data = tecton.get_model_drift(2, constants.LTV)

        # test that it was actually called and only once
        self.assertEqual(request_mocker.call_count, 1)
        self.assertTrue(request_mocker.called)

        self.assertTrue(drift_data)

        # test the last model
        self.assertDictEqual(
            drift_data[-1],
            {
                constants.DRIFT: 215.5,
                constants.RUN_DATE: datetime(2021, 7, 30, 0, 0),
            },
        )

    @requests_mock.Mocker()
    def test_get_models_raise_dependency_error(
        self, request_mocker: Mocker
    ) -> None:
        """Test get models raise dependency error.

        Args:
            request_mocker (Mocker): request mocker object.
        """

        request_mocker.post(
            self.config.TECTON_FEATURE_SERVICE,
            text=json.dumps({}),
            headers=self.config.TECTON_API_HEADERS,
        )

        with self.assertRaises(FailedAPIDependencyError):
            tecton.get_models()

    @requests_mock.Mocker()
    @given(model_id=st.integers(min_value=100, max_value=1000))
    def test_get_model_version_history_raise_empty_response_dependency_error(
        self, request_mocker: Mocker, model_id: int
    ) -> None:
        """Test get model version history raise empty response dependency error.

        Args:
            request_mocker (Mocker): request mocker object.
            model_id (int): model ID value for request.
        """

        request_mocker.post(
            self.config.TECTON_FEATURE_SERVICE,
            text=json.dumps({}),
            headers=self.config.TECTON_API_HEADERS,
        )

        with self.assertRaises(EmptyAPIResponseError):
            tecton.get_model_version_history(model_id=model_id)

    @requests_mock.Mocker()
    @given(
        model_id=st.integers(min_value=100, max_value=1000),
        model_type=st.text(alphabet=string.ascii_letters),
    )
    def test_get_model_drift_raise_empty_response_dependency_error(
        self, request_mocker: Mocker, model_id: int, model_type: str
    ) -> None:
        """Test get model drift raise empty response dependency error.

        Args:
            request_mocker (Mocker): request mocker object.
            model_id (int): model ID value for request.
            model_type (str): model type value for request.
        """

        request_mocker.post(
            self.config.TECTON_FEATURE_SERVICE,
            text=json.dumps({}),
            headers=self.config.TECTON_API_HEADERS,
        )

        with self.assertRaises(EmptyAPIResponseError):
            tecton.get_model_drift(model_id=model_id, model_type=model_type)

    @requests_mock.Mocker()
    @given(
        model_id=st.integers(min_value=100, max_value=1000),
        model_version=st.text(alphabet=string.ascii_letters),
    )
    def test_get_model_features_raise_dependency_error(
        self, request_mocker: Mocker, model_id: int, model_version: str
    ) -> None:
        """Test get model features raise dependency error.

        Args:
            request_mocker (Mocker): request mocker object.
            model_id (int): model ID value for request.
            model_version (str): model version value for request.
        """

        request_mocker.post(
            self.config.TECTON_FEATURE_SERVICE,
            text=json.dumps({}),
            headers=self.config.TECTON_API_HEADERS,
        )

        with self.assertRaises(FailedAPIDependencyError):
            tecton.get_model_features(
                model_id=model_id, model_version=model_version
            )
