"""Purpose of this file is to house all the tecton api tests."""
import json
import string
from unittest import TestCase, mock
from datetime import datetime
import requests_mock
from requests_mock import Mocker
from bson import json_util
from hypothesis import given, strategies as st

from huxunify.api import constants as api_c
from huxunify.api.config import get_config
from huxunify.api.data_connectors.tecton import Tecton
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
                "7",
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
                "7",
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
        self.tecton = Tecton()

    @requests_mock.Mocker()
    def test_list_models(self, request_mocker: Mocker):
        """Test list models.

        Args:
            request_mocker (Mocker): Request mock object.
        """

        # setup the request mock post
        request_mocker.post(
            self.tecton.service,
            text=json.dumps(MOCK_MODEL_RESPONSE, default=json_util.default),
            headers=self.tecton.headers,
        )

        models = self.tecton.get_models()

        # test that it was actually called and only once
        self.assertEqual(request_mocker.call_count, 1)
        self.assertTrue(request_mocker.called)

        # test correct payload sent
        self.assertDictEqual(
            request_mocker.last_request.json(),
            {
                "params": {
                    "feature_service_name": self.tecton.feature_service.FEATURE_MODELS,
                    "join_key_map": {"model_metadata_client": "HUS"},
                }
            },
        )

        self.assertEqual(models[0][api_c.LATEST_VERSION], "0.2.4")
        self.assertEqual(models[0][api_c.PAST_VERSION_COUNT], 0)

    @requests_mock.Mocker()
    def test_map_model_performance_response_ltv(self, request_mocker: Mocker):
        """Test map model performance response for ltv.

        Args:
            request_mocker (Mocker): Request mock object.
        """

        # setup the request mock post
        request_mocker.post(
            self.tecton.service,
            text=json.dumps(
                t_c.MOCKED_MODEL_PERFORMANCE_LTV, default=json_util.default
            ),
            headers=self.tecton.headers,
        )

        model = self.tecton.get_model_performance_metrics(
            2, api_c.LTV, "21.7.30"
        )

        # test that it was actually called and only once
        self.assertEqual(request_mocker.call_count, 1)
        self.assertTrue(request_mocker.called)

        # test correct payload sent
        drift = (
            self.tecton.feature_service.FEATURE_DRIFT_REGRESSION_MODEL_SERVICE
        )
        self.assertDictEqual(
            request_mocker.last_request.json(),
            {
                "params": {
                    "feature_service_name": drift,
                    "join_key_map": {"model_id": "2"},
                }
            },
        )
        self.assertDictEqual(
            model,
            {
                api_c.ID: 2,
                api_c.RMSE: 215.5,
                api_c.AUC: -1,
                api_c.PRECISION: -1,
                api_c.RECALL: -1,
                api_c.CURRENT_VERSION: "21.7.30",
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
            self.tecton.service,
            text=json.dumps(
                t_c.MOCKED_MODEL_PERFORMANCE_UNSUBSCRIBE,
                default=json_util.default,
            ),
            headers=self.tecton.headers,
        )

        model = self.tecton.get_model_performance_metrics(
            1, api_c.UNSUBSCRIBE, "21.7.31"
        )

        # test that it was actually called and only once
        self.assertEqual(request_mocker.call_count, 1)
        self.assertTrue(request_mocker.called)

        # test correct payload sent
        drift = (
            self.tecton.feature_service.FEATURE_DRIFT_CLASSIFICATION_MODEL_SERVICE
        )
        self.assertDictEqual(
            request_mocker.last_request.json(),
            {
                "params": {
                    "feature_service_name": drift,
                    "join_key_map": {"model_id": "1"},
                }
            },
        )
        self.assertDictEqual(
            model,
            {
                api_c.ID: 1,
                api_c.RMSE: -1,
                api_c.AUC: 0.85,
                api_c.PRECISION: 0.71,
                api_c.RECALL: 0.58,
                api_c.CURRENT_VERSION: "21.7.31",
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
            self.tecton.service,
            text=json.dumps(
                {},
                default=json_util.default,
            ),
            headers=self.tecton.headers,
        )

        self.assertFalse(
            self.tecton.get_model_performance_metrics(
                1, api_c.UNSUBSCRIBE, "21.7.31"
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
            self.tecton.service,
            text=json.dumps(
                t_c.MOCKED_MODEL_VERSION_HISTORY,
                default=json_util.default,
            ),
            headers=self.tecton.headers,
        )

        models = self.tecton.get_model_version_history(1)

        # test that it was actually called and only once
        self.assertEqual(request_mocker.call_count, 1)
        self.assertTrue(request_mocker.called)

        self.assertTrue(models)

        # test the last model
        self.assertDictEqual(
            models[0],
            {
                "id": 1,
                "last_trained": datetime(2021, 7, 31, 0, 0),
                "description": "Propensity of a customer unsubscribing "
                "after receiving an email.",
                "fulcrum_date": datetime(2021, 7, 17, 0, 0),
                "lookback_window": 7,
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
            self.tecton.service,
            text=json.dumps(
                t_c.MOCKED_MODEL_PROPENSITY_FEATURES,
                default=json_util.default,
            ),
            headers=self.tecton.headers,
        )

        model_features = self.tecton.get_model_features(1, "21.7.30")

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
            self.tecton.service,
            text=json.dumps(
                t_c.MOCKED_MODEL_PROPENSITY_FEATURES_NEGATIVE_SCORE,
                default=json_util.default,
            ),
            headers=self.tecton.headers,
        )

        model_features = self.tecton.get_model_features(1, "21.7.30")

        self.assertTrue(model_features)
        self.assertTrue(
            all((feature[api_c.SCORE] < 0 for feature in model_features))
        )

    def test_lift_chart(self):
        """Test getting lift charts for a model."""

        # TODO- find async post mocker
        mock.patch(
            "huxunify.api.data_connectors.tecton.Tecton.get_model_lift_async",
            return_value=t_c.MOCKED_MODEL_LIFT_CHART,
        ).start()

        lift_data = self.tecton.get_model_lift_async(1)

        self.assertTrue(lift_data)

        # test the last lift chart data
        self.assertDictEqual(
            lift_data[-1],
            {
                api_c.BUCKET: 100,
                api_c.ACTUAL_VALUE: 2602,
                api_c.ACTUAL_LIFT: 1,
                api_c.PREDICTED_LIFT: 1.0000000895,
                api_c.PREDICTED_VALUE: 2726.7827,
                api_c.PROFILE_COUNT: 95369,
                api_c.ACTUAL_RATE: 0.0272834988,
                api_c.PREDICTED_RATE: 0.0285919189,
                api_c.PROFILE_SIZE_PERCENT: 0,
            },
        )

    @requests_mock.Mocker()
    def test_drift(self, request_mocker: Mocker):
        """Test getting drift charts for a model.

        Args:
            request_mocker (Mocker): request mocker object.
        """

        # setup the request mock post for version history
        request_mocker.post(
            self.tecton.service,
            text=json.dumps(
                t_c.MOCKED_MODEL_VERSION_HISTORY,
                default=json_util.default,
            ),
            headers=self.tecton.headers,
        )

        models = self.tecton.get_model_version_history(2)

        # setup the request mock post
        request_mocker.post(
            self.tecton.service,
            text=json.dumps(
                t_c.MOCKED_MODEL_DRIFT,
                default=json_util.default,
            ),
            headers=self.tecton.headers,
        )

        drift_data = self.tecton.get_model_drift(2, api_c.LTV, models)

        # test that it was actually called and only once
        self.assertEqual(request_mocker.call_count, 2)
        self.assertTrue(request_mocker.called)

        self.assertTrue(drift_data)

        # test the last model
        self.assertDictEqual(
            drift_data[-1],
            {
                api_c.DRIFT: 215.5,
                api_c.RUN_DATE: datetime(2021, 7, 30, 0, 0),
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
            self.tecton.service,
            text=json.dumps({}),
            headers=self.tecton.headers,
        )

        with self.assertRaises(FailedAPIDependencyError):
            self.tecton.get_models()

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
            self.tecton.service,
            text=json.dumps({}),
            headers=self.tecton.headers,
        )

        with self.assertRaises(EmptyAPIResponseError):
            self.tecton.get_model_version_history(model_id=model_id)

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
            self.tecton.service,
            text=json.dumps({}),
            headers=self.tecton.headers,
        )

        with self.assertRaises(EmptyAPIResponseError):
            self.tecton.get_model_drift(
                model_id=model_id, model_type=model_type, models=[]
            )

    @requests_mock.Mocker()
    @given(
        model_id=st.integers(min_value=100, max_value=1000),
        model_version=st.text(alphabet=string.ascii_letters),
    )
    def test_get_model_features_no_data_available(
        self, request_mocker: Mocker, model_id: int, model_version: str
    ) -> None:
        """Test get model features when there is no data available.

        Args:
            request_mocker (Mocker): request mocker object.
            model_id (int): model ID value for request.
            model_version (str): model version value for request.
        """

        request_mocker.post(
            self.tecton.service,
            text=json.dumps({}),
            headers=self.tecton.headers,
        )
        self.assertFalse(
            self.tecton.get_model_features(model_id, model_version)
        )
