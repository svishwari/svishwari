"""Purpose of this file is to house all tests related to decisioning"""
import json
from http import HTTPStatus
from unittest import mock

from huxunifylib.database import constants as db_c
from huxunifylib.database.collection_management import create_document
from hypothesis import given, settings, strategies as st

from huxunify.api import constants as api_c
from huxunify.api.data_connectors.tecton import Tecton
from huxunify.api.schema.model import (
    ModelSchema,
    ModelVersionSchema,
    FeatureSchema,
    ModelPipelinePerformanceSchema,
    ModelDriftSchema,
)
from huxunify.test import constants as t_c
from huxunify.test.route.route_test_util.route_test_case import RouteTestCase


# Allow 30 secs per hypothesis example (deadline is specified in milliseconds)
settings.register_profile(
    "hypothesis_setting_profile",
    deadline=30 * 1000,
)


class DecisioningTests(RouteTestCase):
    """Tests for decisioning."""

    def setUp(self) -> None:
        """Setup tests."""

        super().setUp()

        self.tecton = Tecton()

        # define relative paths used for mocking calls.
        self.models_rel_path = (
            "huxunify.api.data_connectors.tecton.Tecton.get_models"
        )
        self.versions_rel_path = (
            "huxunify.api.data_connectors."
            "tecton.Tecton.get_model_version_history"
        )

        # mock get_db_client()
        mock.patch(
            "huxunify.api.route.decisioning.get_db_client",
            return_value=self.database,
        ).start()

    def test_success_get_models(self):
        """Test get models from Tecton."""

        get_models_mock = mock.patch(self.models_rel_path).start()
        get_models_mock.return_value = t_c.MOCKED_MODEL_RESPONSE

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.MODELS_ENDPOINT}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertTrue(
            t_c.validate_schema(ModelSchema(), response.json, True)
        )

    def test_success_get_models_with_status(self):
        """Test get models with status."""

        get_models_mock = mock.patch(self.models_rel_path).start()
        get_models_mock.return_value = t_c.MOCKED_MODEL_RESPONSE

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.MODELS_ENDPOINT}?"
            f"{api_c.STATUS}={api_c.STATUS_ACTIVE}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertTrue(
            t_c.validate_schema(ModelSchema(), response.json, True)
        )
        self.assertTrue(all(api_c.STATUS in model for model in response.json))
        self.assertTrue(
            all(
                model[api_c.STATUS] == api_c.STATUS_ACTIVE
                for model in response.json
            )
        )

    def test_success_get_models_with_model_tags_filter(self):
        """Test get models with model tags filter."""

        get_models_mock = mock.patch(self.models_rel_path).start()
        get_models_mock.return_value = t_c.MOCKED_MODEL_RESPONSE

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.MODELS_ENDPOINT}?"
            f"{api_c.INDUSTRY_TAG}=healthcare&{api_c.INDUSTRY_TAG}=retail",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertTrue(
            t_c.validate_schema(ModelSchema(), response.json, True)
        )
        for model in response.json:
            self.assertIn(api_c.TAGS, model)
            self.assertIn(api_c.INDUSTRY, model[api_c.TAGS])
            # validate that at lease one of the industry tags sent as part of
            # request payload is present in response
            self.assertTrue(
                any(
                    industry_tag in ["healthcare", "retail"]
                    for industry_tag in model[api_c.TAGS][api_c.INDUSTRY]
                )
            )

    def test_success_request_model(self):
        """Test requesting a model."""

        status_request = [
            {
                api_c.STATUS: api_c.REQUESTED,
                api_c.ID: t_c.MOCKED_MODEL_RESPONSE[0][api_c.ID],
                api_c.NAME: t_c.MOCKED_MODEL_RESPONSE[0][api_c.NAME],
                api_c.TYPE: t_c.MOCKED_MODEL_RESPONSE[0][api_c.TYPE],
            },
            {
                api_c.STATUS: api_c.REQUESTED,
                api_c.ID: t_c.MOCKED_MODEL_RESPONSE[1][api_c.ID],
                api_c.NAME: t_c.MOCKED_MODEL_RESPONSE[1][api_c.NAME],
                api_c.TYPE: t_c.MOCKED_MODEL_RESPONSE[1][api_c.TYPE],
            },
        ]

        response = self.app.post(
            f"{t_c.BASE_ENDPOINT}{api_c.MODELS_ENDPOINT}",
            data=json.dumps(status_request),
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)

        get_models_mock = mock.patch(self.models_rel_path).start()
        get_models_mock.return_value = t_c.MOCKED_MODEL_RESPONSE

    def test_success_request_model_duplicate(self):
        """Test requesting a model."""

        status_request = [
            {
                api_c.STATUS: api_c.REQUESTED,
                api_c.ID: t_c.MOCKED_MODEL_RESPONSE[0][api_c.ID],
                api_c.NAME: t_c.MOCKED_MODEL_RESPONSE[0][api_c.NAME],
                api_c.TYPE: t_c.MOCKED_MODEL_RESPONSE[0][api_c.TYPE],
            }
        ]

        response = self.app.post(
            f"{t_c.BASE_ENDPOINT}{api_c.MODELS_ENDPOINT}",
            data=json.dumps(status_request),
            headers=t_c.STANDARD_HEADERS,
        )
        self.assertEqual(HTTPStatus.OK, response.status_code)

    def test_success_request_model_duplicate_name(self):
        """Test requesting a model."""

        status_request = [
            {
                api_c.STATUS: api_c.REQUESTED,
                api_c.ID: t_c.MOCKED_MODEL_RESPONSE[0][api_c.ID],
                api_c.NAME: t_c.MOCKED_MODEL_RESPONSE[0][api_c.NAME],
                api_c.TYPE: t_c.MOCKED_MODEL_RESPONSE[0][api_c.TYPE],
            }
        ]

        response = self.app.post(
            f"{t_c.BASE_ENDPOINT}{api_c.MODELS_ENDPOINT}",
            data=json.dumps(status_request),
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)

        status_request[0][api_c.TYPE] = "other"
        response = self.app.post(
            f"{t_c.BASE_ENDPOINT}{api_c.MODELS_ENDPOINT}",
            data=json.dumps(status_request),
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)

    def test_remove_model_success(self):
        """Test removing requested models from Unified DB."""

        # Request model to delete later
        status_request = {
            api_c.STATUS: api_c.REQUESTED,
            api_c.ID: "1",
            api_c.NAME: "Test Requested Model",
            api_c.TYPE: "test",
        }

        # Add a document for the requested model in Unified DB
        doc = create_document(
            database=self.database,
            collection=db_c.CONFIGURATIONS_COLLECTION,
            new_doc=status_request,
            username="Test User",
        )

        # API call to delete the requested model
        response = self.app.delete(
            f"{t_c.BASE_ENDPOINT}{api_c.MODELS_ENDPOINT}",
            query_string={api_c.MODEL_ID: doc[api_c.ID]},
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(
            {api_c.MESSAGE: api_c.OPERATION_SUCCESS}, response.json
        )

    def test_remove_model_failure_invalid_model_id(self):
        """Test removing requested models from Unified DB with invalid model id."""
        # API call to delete the requested model
        response = self.app.delete(
            f"{t_c.BASE_ENDPOINT}{api_c.MODELS_ENDPOINT}",
            query_string={api_c.MODEL_ID: 96},
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.NOT_FOUND, response.status_code)

    def test_remove_model_failure_no_params(self):
        """Test removing requested models from Unified DB."""

        # API call to delete the requested model
        response = self.app.delete(
            f"{t_c.BASE_ENDPOINT}{api_c.MODELS_ENDPOINT}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual(
            {api_c.MESSAGE: api_c.EMPTY_OBJECT_ERROR_MESSAGE}, response.json
        )

    @given(model_id=st.sampled_from(list(t_c.SUPPORTED_MODELS.keys())))
    def test_get_model_version_history_success(self, model_id: str):
        """Test get model version history

        Args:
            model_id (str): Model ID.
        """

        # mock the version history
        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.TECTON_FEATURE_SERVICE}",
            json=t_c.MOCKED_MODEL_VERSION_HISTORY,
        )
        self.request_mocker.start()

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.MODELS_ENDPOINT}/{model_id}/"
            f"{api_c.MODELS_VERSION_HISTORY}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertTrue(ModelVersionSchema(many=True).dump(response.json))

    @given(model_id=st.integers(min_value=100, max_value=1000))
    @settings(settings.load_profile("hypothesis_setting_profile"))
    def test_failure_get_model_version_history(self, model_id: int):
        """Test get model version history failed.

        Args:
            model_id (int): Model Id.
        """

        # mock the version history
        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.TECTON_FEATURE_SERVICE}",
            text=json.dumps({}),
        )
        self.request_mocker.start()

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.MODELS_ENDPOINT}/{model_id}/"
            f"{api_c.MODELS_VERSION_HISTORY}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertTrue(
            t_c.validate_schema(ModelVersionSchema(), response.json, True)
        )

    @given(model_id=st.sampled_from(list(t_c.SUPPORTED_MODELS.keys())))
    @settings(settings.load_profile("hypothesis_setting_profile"))
    def test_get_model_drift_success(self, model_id: int) -> None:
        """Test get model drift success.

        Args:
            model_id (int): Model ID.
        """

        get_model_version_mock = mock.patch(self.versions_rel_path).start()
        get_model_version_mock.return_value = (
            t_c.MOCKED_MODEL_VERSION_HISTORY_RESPONSE
        )

        # mock the features response
        self.request_mocker.stop()
        self.request_mocker.post(
            self.tecton.service,
            json=t_c.MOCKED_MODEL_DRIFT,
        )
        self.request_mocker.start()

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.MODELS_ENDPOINT}/{model_id}/"
            f"{api_c.DRIFT}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertTrue(
            t_c.validate_schema(ModelDriftSchema(), response.json, True)
        )

    @given(model_id=st.sampled_from(list(t_c.SUPPORTED_MODELS.keys())))
    @settings(settings.load_profile("hypothesis_setting_profile"))
    def test_get_model_features_success(self, model_id: int) -> None:
        """Test get model features success.

        Args:
            model_id (int): Model ID.
        """

        get_model_version_mock = mock.patch(self.versions_rel_path).start()
        get_model_version_mock.return_value = (
            t_c.MOCKED_MODEL_VERSION_HISTORY_RESPONSE
        )

        # mock the features response
        self.request_mocker.stop()
        self.request_mocker.post(
            self.tecton.service,
            json=t_c.MOCKED_MODEL_PROPENSITY_FEATURES,
        )
        self.request_mocker.start()

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.MODELS_ENDPOINT}/{model_id}/"
            f"{api_c.FEATURES}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertTrue(
            t_c.validate_schema(FeatureSchema(), response.json, True)
        )

    @given(model_id=st.integers(min_value=1, max_value=2))
    @settings(settings.load_profile("hypothesis_setting_profile"))
    def test_get_model_features_negative_score(self, model_id: int) -> None:
        """Test get model features negative score in response.

        Args:
            model_id (int): Model ID.
        """

        get_model_version_mock = mock.patch(self.versions_rel_path).start()
        get_model_version_mock.return_value = (
            t_c.MOCKED_MODEL_VERSION_HISTORY_RESPONSE
        )

        # mock the features response
        self.request_mocker.stop()
        self.request_mocker.post(
            self.tecton.service,
            json=t_c.MOCKED_MODEL_PROPENSITY_FEATURES_NEGATIVE_SCORE,
        )
        self.request_mocker.start()

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.MODELS_ENDPOINT}/{model_id}/"
            f"{api_c.FEATURES}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertTrue(
            t_c.validate_schema(FeatureSchema(), response.json, True)
        )
        self.assertEqual(20, len(response.json))

    @given(model_id=st.sampled_from(list(t_c.SUPPORTED_MODELS.keys())))
    @settings(settings.load_profile("hypothesis_setting_profile"))
    def test_get_model_feature_importance_success(self, model_id: str) -> None:
        """Test get model feature importance success.

        Args:
            model_id (str): Model ID.
        """

        get_model_version_mock = mock.patch(self.versions_rel_path).start()
        get_model_version_mock.return_value = (
            t_c.MOCKED_MODEL_VERSION_HISTORY_RESPONSE
        )

        # mock the features response
        self.request_mocker.stop()
        self.request_mocker.post(
            self.tecton.service,
            json=t_c.MOCKED_MODEL_PROPENSITY_FEATURES,
        )
        self.request_mocker.start()

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.MODELS_ENDPOINT}/{model_id}/"
            f"{api_c.FEATURE_IMPORTANCE}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertTrue(
            t_c.validate_schema(FeatureSchema(), response.json, True)
        )

    @given(model_id=st.integers(min_value=1, max_value=2))
    @settings(settings.load_profile("hypothesis_setting_profile"))
    def test_get_model_feature_importance_negative_score(
        self, model_id: int
    ) -> None:
        """Test get model feature importance negative score in response.

        Args:
            model_id (int): Model ID.
        """

        get_model_version_mock = mock.patch(self.versions_rel_path).start()
        get_model_version_mock.return_value = (
            t_c.MOCKED_MODEL_VERSION_HISTORY_RESPONSE
        )

        # mock the features response
        self.request_mocker.stop()
        self.request_mocker.post(
            self.tecton.service,
            json=t_c.MOCKED_MODEL_PROPENSITY_FEATURES_NEGATIVE_SCORE,
        )
        self.request_mocker.start()

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.MODELS_ENDPOINT}/{model_id}/"
            f"{api_c.FEATURE_IMPORTANCE}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertTrue(
            t_c.validate_schema(FeatureSchema(), response.json, True)
        )
        self.assertTrue(
            all((feature[api_c.SCORE] < 0 for feature in response.json))
        )

    @given(model_id=st.sampled_from(list(t_c.SUPPORTED_MODELS.keys())))
    def test_get_performance_pipeline(self, model_id: str):
        """Test get model performance pipeline.

        Args:
            model_id (str): Model ID.
        """

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.MODELS_ENDPOINT}/{model_id}/pipeline-performance",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)

        self.assertTrue(
            t_c.validate_schema(
                ModelPipelinePerformanceSchema(), response.json
            )
        )
