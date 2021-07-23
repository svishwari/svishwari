"""
purpose of this file is to house all the okta tests
"""
import unittest
import json
from unittest import TestCase
import requests_mock
import mongomock
from requests_mock import Mocker
from flask import Flask
from bson import json_util
from hypothesis import given, strategies as st
from huxunifylib.database.client import DatabaseClient
from huxunify.api.config import get_config
from huxunify.api import constants
from huxunify.api.data_connectors import okta
from huxunify.api.route.utils import secured, get_user_name
from huxunify.api.data_connectors.okta import (
    get_user_info,
    get_token_from_request,
)


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

VALID_USER_RESPONSE = {
    constants.OKTA_ID_SUB: "8548bfh8d",
    constants.EMAIL: "davesmith@fake.com",
    constants.NAME: "dave smith",
}

# response missing some fields
INVALID_USER_RESPONSE = {
    constants.EMAIL: "davesmith@fake.com",
}

INVALID_RESPONSE = {"active": False}


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
        self.user_info_call = f"{self.config.OKTA_ISSUER}/oauth2/v1/userinfo"

        # init mongo patch initially
        mongo_patch = mongomock.patch(servers=(("localhost", 27017),))
        mongo_patch.start()

        # setup the mock DB client
        self.database = DatabaseClient(
            "localhost", 27017, None, None
        ).connect()

        # mock get_db_client()
        unittest.mock.patch(
            "huxunify.api.route.utils.get_db_client",
            return_value=self.database,
        ).start()

        self.addCleanup(unittest.mock.patch.stopall)

    @requests_mock.Mocker()
    def test_introspection_invalid_call(self, request_mocker: Mocker):
        """Test token introspection with an invalid token.

        Args:
            request_mocker (Mocker): Request mock object.

        Returns:

        """

        # setup the request mock post
        request_mocker.post(
            self.introspect_call,
            text=json.dumps(INVALID_RESPONSE, default=json_util.default),
        )

        response = okta.introspect_token("invalid")

        # test that it was actually called and only once
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
            request_mocker (Mocker): Request mock object.

        Returns:

        """

        # setup the request mock post
        request_mocker.post(self.introspect_call, json=VALID_RESPONSE)

        response = okta.introspect_token("valid")

        # test that it was actually called and only once
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
        invalid_header = (constants.INVALID_AUTH_HEADER, 401)
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
        invalid_header = (constants.INVALID_AUTH_HEADER, 401)
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
        invalid_header = (constants.INVALID_AUTH_HEADER, 401)
        with Flask("invalid_test").test_request_context(
            "/", headers={"Authorization": "Bearerr "}
        ):

            @secured()
            def demo_endpoint():
                return True

            self.assertEqual(invalid_header, demo_endpoint())

    @requests_mock.Mocker()
    def test_secured_decorator_bad_token(self, request_mocker: Mocker):
        """Test secured decorator with a bad token

        Args:
            request_mocker (Mocker): Request mock object.

        Returns:

        """

        request_mocker.post(self.introspect_call, json=INVALID_RESPONSE)

        invalid_header = (constants.INVALID_AUTH, 400)
        with Flask("invalid_token").test_request_context(
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
            request_mocker (Mocker): Request mock object.

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

            # true means the endpoint and token call were successfully passed.
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

    def test_secured_decorator_get_user_id_invalid_header(self):
        """Test secured decorator with an invalid header to get_user_id.

        Args:

        Returns:

        """
        invalid_header = (constants.INVALID_AUTH_HEADER, 401)
        with Flask("invalid_test").test_request_context("/"):

            @get_user_name()
            def demo_endpoint():
                return True

            self.assertEqual(invalid_header, demo_endpoint())

    @requests_mock.Mocker()
    def test_secured_decorator_valid_token_user_id(
        self, request_mocker: Mocker
    ):
        """Test secured decorator with a good token to get user id

        Args:
            request_mocker (Mocker): Request mock object.

        Returns:

        """

        # setup the request mock post
        request_mocker.get(self.user_info_call, json=VALID_USER_RESPONSE)

        with Flask("valid_test").test_request_context(
            "/", headers={"Authorization": "Bearer 12345678"}
        ):

            @get_user_name()
            def demo_endpoint(user_name=None):
                return user_name

            # true means the endpoint and token call were succesfully passed.
            self.assertIsInstance(demo_endpoint(), str)

    @given(access_token=st.one_of(st.text(), st.floats(), st.none()))
    @requests_mock.Mocker()
    def test_get_user_info_invalid(
        self, request_mocker: Mocker, access_token: str
    ):
        """Test get_user_info with an invalid response.

        Args:
            request_mocker (Mocker): Request mock object.
            access_token (str): hypothesis random data.

        Returns:

        """
        # run an invalid response (empty)
        # try to break by throwing a bunch of random data into it.
        request_mocker.get(self.user_info_call, json={})

        # get user info should always resolve to False in this test.
        self.assertFalse(get_user_info(access_token))

    @requests_mock.Mocker()
    def test_get_user_info(self, request_mocker: Mocker):
        """Test get_user_info with a valid response.

        Args:
            request_mocker (Mocker): Request mock object.

        Returns:

        """
        # run an invalid response (empty)
        # try to break by throwing a bunch of random data into it.
        request_mocker.get(self.user_info_call, json=VALID_RESPONSE)

        # get user info should always resolve to False in this test.
        response = get_user_info("access_token")

        # test that it was actually called and only once
        self.assertEqual(request_mocker.call_count, 1)
        self.assertTrue(request_mocker.called)

        # test that payload was empty.
        self.assertIsNone(request_mocker.last_request.text)

        # test expected response
        self.assertDictEqual(response, VALID_RESPONSE)

    @given(random_data=st.one_of(st.text(), st.floats(), st.none()))
    def test_get_token_from_request_invalid(self, random_data: str):
        """Test get_token_from_request with invalid data trying to break it.

        Args:
            random_data (str): hypothesis random data.

        Returns:

        """

        # should always return a 401
        response = get_token_from_request(random_data)
        self.assertEqual(401, response[1])

    @requests_mock.Mocker()
    def test_get_user_info_invalid_response(self, request_mocker: Mocker):
        """Test get_user_info with an invalid response.

        The token allows introspection but gives an invalid response when
        used with get_user_info

        Args:
            request_mocker (Mocker): Request mock object.

        Returns:

        """
        # valid response after introspection with token
        request_mocker.post(self.introspect_call, json=VALID_RESPONSE)
        response = okta.introspect_token("access_token")
        expected_response = {"user_id": "1234567", "user_name": "davesmith"}
        self.assertDictEqual(response, expected_response)

        # user info call returning
        request_mocker.get(self.user_info_call, json=INVALID_USER_RESPONSE)
        response = get_user_info("access_token")
        # check if all valid keys exists
        self.assertFalse(response.keys() == VALID_USER_RESPONSE.keys())

    @requests_mock.Mocker()
    def test_get_user_info_empty_response(self, request_mocker: Mocker):
        """Test get_user_info with an empty response.

        The token allows introspection but gives an empty response when
        used with get_user_info

        Args:
            request_mocker (Mocker): Request mock object.

        Returns:

        """
        # valid response after introspection with token
        request_mocker.post(self.introspect_call, json=VALID_RESPONSE)
        response = okta.introspect_token("access_token")
        expected_response = {"user_id": "1234567", "user_name": "davesmith"}
        self.assertDictEqual(response, expected_response)

        # simulating user response is empty
        request_mocker.get(self.user_info_call, json={})
        response = get_user_info("access_token")
        # check if all valid keys exists
        self.assertFalse(response.keys() == VALID_USER_RESPONSE.keys())
