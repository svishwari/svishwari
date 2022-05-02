"""Tests for trust ID APIs."""
from http import HTTPStatus
from unittest import mock

from huxunifylib.database.survey_metrics_management import (
    set_survey_responses_bulk,
)
from huxunify.api.schema.trust_id import (
    TrustIdOverviewSchema,
    TrustIdAttributesSchema,
)
from huxunify.test.route.route_test_util.route_test_case import RouteTestCase

import huxunify.test.constants as t_c
from huxunify.api import constants as api_c


class TestTrustIDRoutes(RouteTestCase):
    """Tests for trust ID endpoints."""

    def setUp(self):
        """Set up resources"""
        super().setUp()

        # mock get_db_client() for the trust id.
        mock.patch(
            "huxunify.api.route.trust_id.get_db_client",
            return_value=self.database,
        ).start()

        _ = set_survey_responses_bulk(
            self.database, t_c.TRUST_ID_SURVEY_RESPONSES
        )

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

    # def test_trust_id_comparison_data(self):
    #     """Test for trust_id comparison data endpoint."""
    #
    #     response = self.app.get(
    #         f"{t_c.BASE_ENDPOINT}{api_c.TRUST_ID_ENDPOINT}/comparison",
    #         headers=t_c.STANDARD_HEADERS,
    #     )
    #
    #     self.assertEqual(HTTPStatus.OK, response.status_code)
    #     self.assertFalse(
    #         TrustIdComparisonSchema().validate(response.json, many=True)
    #     )
    #
    # def test_add_trust_id_segment(self):
    #     """Test for trust_id segment addition endpoint."""
    #
    #     response = self.app.post(
    #         f"{t_c.BASE_ENDPOINT}{api_c.TRUST_ID_ENDPOINT}/segment",
    #         json={"segment_name": "Test Add Segment", "segment_filters": []},
    #         headers=t_c.STANDARD_HEADERS,
    #     )
    #
    #     self.assertEqual(HTTPStatus.CREATED, response.status_code)
    #     self.assertFalse(
    #         TrustIdComparisonSchema().validate(response.json, many=True)
    #     )
    #
    # def test_remove_trust_id_segment(self):
    #     """Test for trust_id segment removal endpoint."""
    #
    #     response = self.app.post(
    #         f"{t_c.BASE_ENDPOINT}{api_c.TRUST_ID_ENDPOINT}/segment",
    #         json={"segment_name": "Test Segment", "segment_filters": []},
    #         headers=t_c.STANDARD_HEADERS,
    #     )
    #
    #     self.assertEqual(HTTPStatus.CREATED, response.status_code)
    #     self.assertFalse(
    #         TrustIdComparisonSchema().validate(response.json, many=True)
    #     )
    #
    #     response = self.app.delete(
    #         f"{t_c.BASE_ENDPOINT}{api_c.TRUST_ID_ENDPOINT}/segment",
    #         query_string={"segment_name": "Test Segment"},
    #         headers=t_c.STANDARD_HEADERS,
    #     )
    #
    #     self.assertEqual(HTTPStatus.OK, response.status_code)
    #     self.assertFalse(
    #         TrustIdComparisonSchema().validate(response.json, many=True)
    #     )
