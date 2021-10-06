"""Purpose of this file is to house all tests related to decisioning."""


import json
from http import HTTPStatus
from unittest import TestCase, mock

import mongomock
from huxunifylib.database.client import DatabaseClient
from hypothesis import given, settings, strategies as st

import requests_mock

from huxunify.api.config import get_config
from huxunify.api import constants as api_c
from huxunify.api.schema.model import (
    ModelSchema,
    ModelVersionSchema,
    FeatureSchema,
)
from huxunify.app import create_app
from huxunify.test import constants as t_c


class DecisioningTests(TestCase):
    """Tests for decisioning."""

    def setUp(self) -> None:
        """Setup tests."""

        self.config = get_config(api_c.TEST_MODE)

        # setup the flask test client
        self.test_client = create_app().test_client()

        self.introspect_call = (
            f"{self.config.OKTA_ISSUER}"
            f"/oauth2/v1/introspect?client_id="
            f"{self.config.OKTA_CLIENT_ID}"
        )

        # init mongo patch initially
        mongo_patch = mongomock.patch(servers=(("localhost", 27017),))
        mongo_patch.start()

        # setup the mock DB client
        self.database = DatabaseClient(
            "localhost", 27017, None, None
        ).connect()

        # mock get_db_client()
        mock.patch(
            "huxunify.api.route.decisioning.get_db_client",
            return_value=self.database,
        ).start()

        self.request_mocker = requests_mock.Mocker()
        self.request_mocker.post(t_c.INTROSPECT_CALL, json=t_c.VALID_RESPONSE)
        self.request_mocker.start()

    def test_sucess_get_models(self):
        """Test get models from Tecton."""

        get_models_mock = mock.patch(
            "huxunify.api.data_connectors.tecton.get_models"
        ).start()
        get_models_mock.return_value = t_c.MOCKED_MODEL_RESPONSE

        response = self.test_client.get(
            f"{t_c.BASE_ENDPOINT}{api_c.MODELS_ENDPOINT}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertTrue(
            t_c.validate_schema(ModelSchema(), response.json, True)
        )

        self.assertEqual(
            [x[api_c.NAME] for x in response.json],
            sorted([x[api_c.NAME] for x in t_c.MOCKED_MODEL_RESPONSE]),
        )

    @given(model_id=st.sampled_from(list(t_c.SUPPORTED_MODELS.keys())))
    def test_get_model_version_history_success(self, model_id: int):
        """Test get model version history

        Args:
            model_id (int): Model ID.
        """

        # mock the version history
        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.TECTON_FEATURE_SERVICE}",
            json=t_c.MOCKED_MODEL_VERSION_HISTORY,
        )
        self.request_mocker.start()

        response = self.test_client.get(
            f"{t_c.BASE_ENDPOINT}{api_c.MODELS_ENDPOINT}/{model_id}/{api_c.MODELS_VERSION_HISTORY}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertTrue(ModelVersionSchema(many=True).dump(response))

    @given(model_id=st.integers(min_value=100, max_value=1000))
    @settings(deadline=600)
    def test_get_model_version_history_failed(self, model_id: int):
        """
        Test get model version history failed

        Args:
            model_id (int): Model Id.

        Returns:
            None
        """

        # mock the version history
        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.TECTON_FEATURE_SERVICE}",
            text=json.dumps({}),
        )
        self.request_mocker.start()

        response = self.test_client.get(
            f"{t_c.BASE_ENDPOINT}{api_c.MODELS_ENDPOINT}/{model_id}/{api_c.MODELS_VERSION_HISTORY}",
            headers=t_c.STANDARD_HEADERS,
        )
        if model_id in t_c.SUPPORTED_MODELS:
            self.assertEqual(HTTPStatus.OK, response.status_code)
        else:
            self.assertEqual(HTTPStatus.NOT_FOUND, response.status_code)

    @given(model_id=st.sampled_from(list(t_c.SUPPORTED_MODELS.keys())))
    @settings(deadline=600)
    def test_success_get_model_features(self, model_id: int) -> None:
        """Test get model features

        Args:
            model_id (int): Model ID.
        """

        get_model_version_mock = mock.patch(
            "huxunify.api.data_connectors.tecton.get_model_version_history"
        ).start()
        get_model_version_mock.return_value = (
            t_c.MOCKED_MODEL_VERSION_HISTORY_RESPONSE
        )

        # mock the features response
        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.TECTON_FEATURE_SERVICE}",
            json=t_c.MOCKED_MODEL_PROPENSITY_FEATURES,
        )
        self.request_mocker.start()

        response = self.test_client.get(
            f"{t_c.BASE_ENDPOINT}{api_c.MODELS_ENDPOINT}/{model_id}/{api_c.FEATURES}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertTrue(FeatureSchema(many=True).dump(response))
