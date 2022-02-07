"""Tests for trust ID APIs."""
from http import HTTPStatus

from hypothesis import given, strategies as st

from huxunify.api.schema.trust_id import (
    TrustIdOverviewSchema,
    SignalOverviewSchema,
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

    def test_trust_id_overview_filters(self):
        """Test for trust_id overview endpoint with filters."""

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}"
            f"{api_c.TRUST_ID_ENDPOINT}/overview?gender=male&max_age=40",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)

        self.assertTrue(
            t_c.validate_schema(TrustIdOverviewSchema(), response.json)
        )

    @given(st.sampled_from(api_c.LIST_OF_SIGNALS))
    def test_trust_id_signal_data(self, signal_name: str):
        """Test for trust_id signal data endpoint.
        Args:
            signal_name (str): Name of the signal.
        """

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}"
            f"{api_c.TRUST_ID_ENDPOINT}/signal/{signal_name}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)

        self.assertTrue(
            t_c.validate_schema(SignalOverviewSchema(), response.json)
        )

    def test_trust_id_invalid_signal(self):
        """Test for trust_id signal data endpoint for invalid signal."""

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}" f"{api_c.TRUST_ID_ENDPOINT}/signal/random",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
