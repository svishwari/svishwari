"""Purpose of this file is to test core application checks."""
from http import HTTPStatus
from unittest import TestCase
import pytest
import requests
from prometheus_metrics import record_test_result, HttpMethod, Endpoints


class TestCoreAppChecks(TestCase):
    """API application basic checks test class."""

    SWAGGER_UI = "ui"
    API_SPEC = "apispec_1"
    HEALTH_CHECK = "health-check"
    METRICS = "metrics"

    @record_test_result(HttpMethod.GET, Endpoints.CORE_APP.GET_SWAGGER_DOCS)
    def test_get_swagger_docs(self):
        """Test get swagger docs page."""

        response = requests.get(f"{pytest.API_URL}/{self.SWAGGER_UI}/")

        self.assertEqual(HTTPStatus.OK, response.status_code)

    @record_test_result(HttpMethod.GET, Endpoints.CORE_APP.GET_API_SPEC)
    def test_get_apispec(self):
        """Test open apispec."""

        response = requests.get(f"{pytest.APP_URL}/{self.API_SPEC}.json")

        self.assertEqual(HTTPStatus.OK, response.status_code)
        response_json = response.json()
        self.assertIsInstance(response_json, dict)
        self.assertIn("info", response_json)
        self.assertIn("title", response_json["info"])
        self.assertEqual("Hux API", response_json["info"]["title"])

    @record_test_result(HttpMethod.GET, Endpoints.CORE_APP.GET_HEALTH_CHECK)
    def test_get_core_health_check(self):
        """Test get API application's core health check."""

        response = requests.get(f"{pytest.APP_URL}/{self.HEALTH_CHECK}")

        self.assertEqual(HTTPStatus.OK, response.status_code)
        response_json = response.json()
        self.assertIsInstance(response_json, dict)
        self.assertIn("results", response_json)
        response_json_results = response_json["results"]
        self.assertTrue(
            all(
                "passed" in result and result["passed"]
                for result in response_json_results
            )
        )

    @record_test_result(HttpMethod.GET, Endpoints.CORE_APP.GET_METRICS)
    def test_get_api_metrics(self):
        """Test get API prometheus metrics."""

        response = requests.get(f"{pytest.APP_URL}/{self.METRICS}")

        self.assertEqual(HTTPStatus.OK, response.status_code)
