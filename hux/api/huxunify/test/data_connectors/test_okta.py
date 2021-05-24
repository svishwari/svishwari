"""
purpose of this file is to house all the okta tests
"""
import json
from unittest import TestCase
import requests_mock
from requests_mock import Mocker
from bson import json_util
from huxunify.api.config import get_config
from huxunify.api.data_connectors import okta


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
INVALID_RESPONSE = {"active": False}
BEARER_SAMPLE = {
    "token_type": "Bearer",
    "expires_in": 3600,
    "access_token": "",
    "scope": "openid email profile",
    "id_token": "",
}


class OktaTest(TestCase):
    """
    Test Okta request methods
    """

    def setUp(self) -> None:
        """Setup tests

        Returns:

        """
        self.config = get_config()
        self.introspect_call = (
            f"{self.config.OKTA_ISSUER}"
            f"/oauth2/v1/introspect?client_id="
            f"{self.config.OKTA_CLIENT_ID}"
        )

    @requests_mock.Mocker()
    def test_introspection_invalid_call(self, request_mocker: Mocker):
        """Test token introspection with an invalid token.

        Args:
            request_mocker (str): Request mock object.

        Returns:

        """

        # setup the request mock post
        request_mocker.post(
            self.introspect_call,
            text=json.dumps(INVALID_RESPONSE, default=json_util.default),
        )

        response = okta.introspect_token("invalid")

        # # test that it was actually called and only once
        self.assertEqual(request_mocker.call_count, 1)
        self.assertTrue(request_mocker.called)

        # test correct payload sent
        expected_payload = "token=invalid&token_type_hint=access_token"
        self.assertEqual(request_mocker.last_request.text, expected_payload)

        # test expected response of None
        self.assertIsNone(response)

    @requests_mock.Mocker()
    def test_introspection_valid_call(self, request_mocker: Mocker):
        """Test token introspection with a valid token.

        Args:
            request_mocker (str): Request mock object.

        Returns:

        """

        # setup the request mock post
        request_mocker.post(self.introspect_call, json=VALID_RESPONSE)

        response = okta.introspect_token("valid")

        # # test that it was actually called and only once
        self.assertEqual(request_mocker.call_count, 1)
        self.assertTrue(request_mocker.called)

        # test correct payload sent
        expected_payload = "token=valid&token_type_hint=access_token"
        self.assertEqual(request_mocker.last_request.text, expected_payload)

        # test expected response of None
        expected_response = {"user_id": "1234567", "user_name": "davesmith"}
        self.assertDictEqual(response, expected_response)
