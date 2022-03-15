"""Purpose of this file is to house all tests related to apispec."""
from http import HTTPStatus

from huxunify.api import constants as api_c
from huxunify.api.schema.apispec import ApiSpecSchema

from huxunify.test.route.route_test_util.route_test_case import RouteTestCase


class ApiSpecTests(RouteTestCase):
    """Tests for ApiSpecs"""

    def test_apispec_schema(self):
        """Test api spec schema"""
        response = self.app.get(f"/{api_c.API_SPEC}")
        self.assertEqual(HTTPStatus.OK, response.status_code)

        self.assertFalse(ApiSpecSchema().validate(response.json))
