"""Purpose of this file is to house all the route is secured tests."""
from unittest import TestCase
import requests_mock
from requests_mock import Mocker
from huxunify.api.config import get_config
from huxunify.app import create_app
from huxunify.api import constants as api_c
from huxunify.test import constants as t_c


UNSECURED_ROUTES = [
    "/api/v1/ui/",
    "/apidocs/index.html",
    "/apispec_1.json",
    "/health-check",
    "/swagger/<path:filename>",
    "/static/<path:filename>",
]


class OktaTest(TestCase):
    """Test Okta request methods."""

    def setUp(self) -> None:
        """Setup tests."""

        self.config = get_config(api_c.TEST_MODE)

        # setup the flask test client
        self.app = create_app().test_client()
        self.routes = list(create_app().url_map.iter_rules())

    @requests_mock.Mocker()
    def test_secured_all_endpoints_invalid_response(
        self, request_mocker: Mocker
    ):
        """Test all endpoints with a mocked invalid response.

        Args:
            request_mocker (Mocker): Request mock object.
        """

        # setup the request mock post
        request_mocker.post(
            t_c.INTROSPECT_CALL, json=t_c.INVALID_OKTA_RESPONSE
        )
        mock_header = {"Authorization": "Bearer 1234567"}

        # process each of the headers at once
        for route in self.routes:
            # skip unsecured routes
            if route.rule in UNSECURED_ROUTES:
                continue

            result = getattr(self.app, get_method(route.methods))(
                route.rule, headers=mock_header
            )
            self.assertEqual(400, result.status_code)

    @requests_mock.Mocker()
    def test_secured_all_endpoints_invalid_header(
        self, request_mocker: Mocker
    ):
        """Test all endpoints with a mocked invalid header.

        Args:
            request_mocker (Mocker): Request mock object.
        """

        # setup the request mock post
        request_mocker.post(
            t_c.INTROSPECT_CALL, json=t_c.INVALID_OKTA_RESPONSE
        )
        mock_header = {"Authorization": "Bearer"}

        # process each of the headers at once
        for route in self.routes:
            # skip unsecured routes
            if route.rule in UNSECURED_ROUTES:
                continue

            result = getattr(self.app, get_method(route.methods))(
                route.rule, headers=mock_header
            )
            self.assertEqual(401, result.status_code)

    @requests_mock.Mocker()
    def test_secured_all_endpoints_valid_header_bad_token(
        self, request_mocker: Mocker
    ):
        """Test all endpoints with a mocked valid header, bad token.

        Args:
            request_mocker (Mocker): Request mock object.
        """

        # setup the request mock post
        request_mocker.post(
            t_c.INTROSPECT_CALL, json=t_c.INVALID_OKTA_RESPONSE
        )
        mock_header = {"Authorization": "Bearer 123456765"}

        # process each of the headers at once
        for route in self.routes:
            # skip unsecured routes
            if route.rule in UNSECURED_ROUTES:
                continue

            result = getattr(self.app, get_method(route.methods))(
                route.rule, headers=mock_header
            )
            self.assertEqual(400, result.status_code)


def get_method(methods: set) -> str:
    """Support function for extracting method from swagger view endpoint.

    Args:
        methods (set): set of methods for an endpoint.

    Returns:
        str: returns the method to invoke.

    Raises:
        AttributeError: If the method name is not one of the acceptable REST
            method type.
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
    elif "PATCH" in methods:
        method = "patch"
    else:
        raise AttributeError(f"Unknown methods {methods}")
    return method
