"""
Purpose of this file is to house all tests related to decisioning
"""

from http import HTTPStatus
from unittest import TestCase, mock

import dateutil.parser as parser
import requests_mock

from requests_mock import Mocker

from huxunify.api.config import get_config
from huxunify.api import constants as api_c
from huxunify.api.schema.model import ModelSchema
from huxunify.app import create_app
from huxunify.test import shared as sh


class DecisioningTests(TestCase):
    """
    Tests for decisioning
    """

    def setUp(self) -> None:
        """
        Setup tests

        Returns:

        """
        self.config = get_config("TEST")

        # setup the flask test client
        self.test_client = create_app().test_client()

        self.introspect_call = (
            f"{self.config.OKTA_ISSUER}"
            f"/oauth2/v1/introspect?client_id="
            f"{self.config.OKTA_CLIENT_ID}"
        )

    @requests_mock.Mocker()
    def test_get_models_success(self, requests_mocker: Mocker):
        """
        Test get models from Tecton

        Args:
            requests_mocker (Mocker): request mocker object

        Returns:
            None
        """
        requests_mocker.post(self.introspect_call, json=sh.VALID_RESPONSE)

        mocked_models = [
            {
                api_c.ID: 1,
                api_c.NAME: "Model1",
                api_c.DESCRIPTION: "Test Model",
                api_c.STATUS: api_c.OPERATION_SUCCESS.lower(),
                api_c.LATEST_VERSION: "0.1.1",
                api_c.PAST_VERSION_COUNT: 0,
                api_c.LAST_TRAINED: parser.parse("2021-06-22T11:33:19.658Z"),
                api_c.OWNER: "HUX Unified",
                api_c.LOOKBACK_WINDOW: 365,
                api_c.PREDICTION_WINDOW: 365,
                api_c.FULCRUM_DATE: parser.parse("2021-06-22T11:33:19.658Z"),
                api_c.TYPE: "test",
            }
        ]

        get_models_mock = mock.patch(
            "huxunify.api.data_connectors.tecton.get_models"
        ).start()
        get_models_mock.return_value = mocked_models

        response = self.test_client.get(
            f"{sh.BASE_ENDPOINT}{api_c.MODELS_ENDPOINT}",
            headers={
                "Authorization": sh.TEST_AUTH_TOKEN,
                "Content-Type": "application/json",
            },
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertTrue(sh.validate_schema(ModelSchema(), response.json, True))
