"""
purpose of this file is to house all the okta tests
"""
import json
from unittest import TestCase
import requests_mock
from requests_mock import Mocker
from flask import Flask
from bson import json_util
from huxunify.api.config import get_config
from huxunify.api.data_connectors import okta
from huxunify.api.route.utils import secured


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

    def test_secured_decorator_invalid_header(self):
        """Test secured decorator with an invalid header.

        Args:

        Returns:

        """
        invalid_header = ("You not authorized to visit this page.", 401)
        with Flask("invalid_test").test_request_context("/"):

            @secured()
            def demo_endpoint():
                return True

            self.assertEqual(invalid_header, demo_endpoint())

    def test_secured_decorator_valid_header_none_token(self):
        """Test secured decorator with a valid header, None token.

        Args:

        Returns:

        """
        invalid_header = ("Invalid authorization header.", 403)
        with Flask("invalid_test").test_request_context(
            "/", headers={"Authorization": None}
        ):

            @secured()
            def demo_endpoint():
                return True

            self.assertEqual(invalid_header, demo_endpoint())

    def test_secured_decorator_misspelled_bearer(self):
        """Test secured decorator with a misspelled bearer

        Args:

        Returns:

        """
        invalid_header = ("Invalid authorization header.", 403)
        with Flask("invalid_test").test_request_context(
            "/", headers={"Authorization": "Bearerr "}
        ):

            @secured()
            def demo_endpoint():
                return True

            self.assertEqual(invalid_header, demo_endpoint())

    def test_secured_decorator_bad_token(self):
        """Test secured decorator with a bad token

        Args:

        Returns:

        """
        invalid_header = ("You not authorized to visit this page.", 401)
        with Flask("invalid_test").test_request_context(
            "/", headers={"Authorization": "Bearer 123456789"}
        ):

            @secured()
            def demo_endpoint():
                return True

            self.assertEqual(invalid_header, demo_endpoint())

    @requests_mock.Mocker()
    def test_secured_decorator_valid_token(self, request_mocker: Mocker):
        """Test secured decorator with a good token

        Args:
            request_mocker (str): Request mock object.

        Returns:

        """

        # setup the request mock post
        request_mocker.post(self.introspect_call, json=VALID_RESPONSE)

        with Flask("valid_test").test_request_context(
            "/", headers={"Authorization": "Bearer 12345678"}
        ):

            @secured()
            def demo_endpoint():
                return True

            # true means the endpoint and token call were succesfully passed.
            self.assertTrue(demo_endpoint())

    def test_secured_decorator_exists(self):
        """Test if the secured decorator is attached to the endpoint

        Args:

        Returns:

        """

        @secured()
        def demo_endpoint():
            return True

        self.assertEqual(
            getattr(demo_endpoint, "__wrapped__").__name__, "demo_endpoint"
        )

    def test_unsecured_decorator_exists(self):
        """Test if the secured decorator is not attached to the endpoint

        Args:

        Returns:

        """

        def demo_endpoint():
            return True

        with self.assertRaises(AttributeError):
            getattr(demo_endpoint, "__wrapped__")
