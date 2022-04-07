"""Tests for trust ID APIs."""
from http import HTTPStatus


from huxunify.api.schema.trust_id import (
    TrustIdOverviewSchema,
    TrustIdAttributesSchema,
    TrustIdComparisonSchema,
)
from huxunify.test.route.route_test_util.route_test_case import RouteTestCase

import huxunify.test.constants as t_c
from huxunify.api import constants as api_c


class TestTrustIDRoutes(RouteTestCase):
    """Tests for trust ID endpoints."""

    def test_trust_id_overview(self):
        """Test for trust_id overview endpoint."""

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}" f"{api_c.TRUST_ID_ENDPOINT}/overview",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)

        self.assertTrue(
            t_c.validate_schema(TrustIdOverviewSchema(), response.json)
        )

    def test_trust_id_attributes_data(self):
        """Test for trust_id attributes data endpoint."""

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.TRUST_ID_ENDPOINT}/attributes",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)

        self.assertFalse(
            TrustIdAttributesSchema(many=True).validate(response.json)
        )

    def test_trust_id_comparison_data(self):
        """Test for trust_id comparison data endpoint for invalid signal."""

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.TRUST_ID_ENDPOINT}/comparison",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertFalse(
            TrustIdComparisonSchema().validate(response.json, many=True)
        )
