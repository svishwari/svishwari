"""
Purpose of this file is to house all tests related to decisioning
"""

from http import HTTPStatus
from unittest import TestCase, mock

import dateutil.parser as parser
import requests_mock
from flask_marshmallow import Schema
from marshmallow import ValidationError
from requests_mock import Mocker

from huxunify.api.config import get_config
from huxunify.api import constants as api_c
from huxunify.api.schema.model import ModelSchema
from huxunify.app import create_app

BASE_ENDPOINT = "/api/v1"
TEST_AUTH_TOKEN = "Bearer 12345678"
VALID_RESPONSE = {
    "active": True,
    "scope": "openid email profile",
    "username": "davesmith",
    "exp": 1234,
    "iat": 12345,
    "sub": "davesmith@fake",
    "aud": "sample_aud",
    "iss": "sample_iss",
    "jti": "sample_jti",
    "token_type": "Bearer",
    "client_id": "1234",
    "uid": "1234567",
}


def validate_schema(
    schema: Schema, response_json: dict, is_multiple: bool = False
) -> bool:
    """
    Validate if the response confirms with the given schema

    Args:
        schema (Schema): Instance of the Schema to validate against
        response_json (dict): Response json as dict
        is_multiple (bool): If response is a collection of objects

    Returns:
        (bool): True/False
    """

    try:
        schema.load(response_json, many=is_multiple)
        return True
    except ValidationError:
        return False


class MyTestCase(TestCase):
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
        requests_mocker.post(self.introspect_call, json=VALID_RESPONSE)

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
            f"{BASE_ENDPOINT}{api_c.MODELS_ENDPOINT}",
            headers={
                "Authorization": TEST_AUTH_TOKEN,
                "Content-Type": "application/json",
            },
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertTrue(validate_schema(ModelSchema(), response.json, True))
