"""
purpose of this file is to house all the route is secured tests
"""
from unittest import TestCase
import requests_mock
from requests_mock import Mocker
from huxunify.api.config import get_config
from huxunify import app


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
UNSECURED_ROUTES = [
    "/api/v1/ui/",
    "/apidocs/index.html",
    "/apispec_1.json",
    "/health-check",
    "/swagger/<path:filename>",
    "/static/<path:filename>",
]


class OktaTest(TestCase):
    """
    Test Okta request methods
    """

    def setUp(self) -> None:
        """Setup tests

        Returns:

        """
        print("getting config")
        self.config = get_config()

        print("creating app")
        # setup the flask test client
        self.app = app.create_app()

        print("listing routes")
        self.routes = list(self.app.url_map.iter_rules())
        print("introspect_call routes")
        self.introspect_call = (
            f"{self.config.OKTA_ISSUER}"
            f"/oauth2/v1/introspect?client_id="
            f"{self.config.OKTA_CLIENT_ID}"
        )

    @requests_mock.Mocker()
    def test_secured_all_endpoints_invalid_response(
        self, request_mocker: Mocker
    ):
        """Test all endpoints with a mocked invalid response

        Args:
            request_mocker (str): Request mock object.

        Returns:

        """
        print("test_secured_all_endpoints_invalid_response")
        # setup the request mock post
        request_mocker.post(self.introspect_call, json=INVALID_RESPONSE)
        mock_header = {"Authorization": "Bearer 1234567"}

        # process each of the headers at once
        with self.app.test_client() as client:
            for route in self.routes:
                # skip unsecured routes
                if route.rule in UNSECURED_ROUTES:
                    continue

                print(f"Testing {route.rule}")
                result = getattr(client, get_method(route.methods))(
                    route.rule, headers=mock_header
                )
                self.assertEqual(401, result.status_code)

    @requests_mock.Mocker()
    def test_secured_all_endpoints_invalid_header(
        self, request_mocker: Mocker
    ):
        """Test all endpoints with a mocked invalid header

        Args:
            request_mocker (str): Request mock object.

        Returns:

        """
        print("test_secured_all_endpoints_invalid_header")
        # setup the request mock post
        request_mocker.post(self.introspect_call, json=INVALID_RESPONSE)
        mock_header = {"Authorization": "Bearer"}

        # process each of the headers at once
        with self.app.test_client() as client:
            for route in self.routes:
                # skip unsecured routes
                if route.rule in UNSECURED_ROUTES:
                    continue

                print(f"Testing {route.rule}")
                result = getattr(client, get_method(route.methods))(
                    route.rule, headers=mock_header
                )
                self.assertEqual(403, result.status_code)

    @requests_mock.Mocker()
    def test_secured_all_endpoints_valid_header_bad_token(
        self, request_mocker: Mocker
    ):
        """Test all endpoints with a mocked valid header, bad token

        Args:
            request_mocker (str): Request mock object.

        Returns:

        """
        print("test_secured_all_endpoints_valid_header_bad_token")
        # setup the request mock post
        request_mocker.post(self.introspect_call, json=INVALID_RESPONSE)
        mock_header = {"Authorization": "Bearer 123456765"}

        # process each of the headers at once
        with self.app.test_client() as client:
            for route in self.routes:
                # skip unsecured routes
                if route.rule in UNSECURED_ROUTES:
                    continue

                print(f"Testing {route.rule}")
                result = getattr(client, get_method(route.methods))(
                    route.rule, headers=mock_header
                )
                self.assertEqual(401, result.status_code)

    @requests_mock.Mocker()
    def test_secured_all_endpoints_valid_header_good_token(
        self, request_mocker: Mocker
    ):
        """Test all endpoints with a mocked valid header, good token

        Args:
            request_mocker (str): Request mock object.

        Returns:

        """
        print("test_secured_all_endpoints_valid_header_good_token")
        # setup the request mock post
        request_mocker.post(self.introspect_call, json=VALID_RESPONSE)
        mock_header = {"Authorization": "Bearer 123456765"}

        # process each of the headers at once
        with self.app.test_client() as client:
            for route in self.routes:
                # skip unsecured routes
                if route.rule in UNSECURED_ROUTES:
                    continue

                print(f"Testing {route.rule}")
                result = getattr(client, get_method(route.methods))(
                    route.rule, headers=mock_header
                )
                # check status codes for invalid header and invalid token.
                self.assertNotIn(result.status_code, [401, 403])


def get_method(methods: set) -> str:
    """Support function for extracting method from swaggerview endpoint.

    Args:
        methods (set): set of methods for an endpoint.

    Returns:
        str: returns the method to invoke.
    """
    # get method
    if "GET" in methods:
        method = "get"
    elif "POST" in methods:
        method = "post"
    elif "DELETE" in methods:
        method = "delete"
    elif "PUT" in methods:
        method = "put"
    else:
        raise AttributeError(f"Unknown methods {methods}")
    return method
