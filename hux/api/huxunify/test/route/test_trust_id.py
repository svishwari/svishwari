"""Tests for trust ID APIs."""
from http import HTTPStatus
from unittest import mock

import huxunifylib.database.constants as db_c
from huxunifylib.database.collection_management import create_document
from huxunifylib.database.survey_metrics_management import (
    set_survey_responses_bulk,
)
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

        create_document(
            self.database,
            db_c.CONFIGURATIONS_COLLECTION,
            {
                db_c.CONFIGURATION_FIELD_TYPE: db_c.TRUST_ID_ATTRIBUTES,
                db_c.CONFIGURATION_FIELD_NAME: "TrustID Attributes",
                db_c.ATTRIBUTES: t_c.TRUST_ID_ATTRIBUTE_DESCRIPTION_MAP,
            },
        )
        self.request_mocker.get(
            t_c.USER_INFO_CALL, json=t_c.VALID_TRUSTID_USER_RESPONSE
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
        mock.patch(
            "huxunify.api.data_connectors.trust_id.get_trust_id_attributes",
            return_value=t_c.TRUST_ID_ATTRIBUTE_RATINGS,
        ).start()

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.TRUST_ID_ENDPOINT}/attributes",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)

        self.assertFalse(
            TrustIdAttributesSchema(many=True).validate(response.json)
        )

    def test_trust_id_comparison_data(self):
        """Test for trust_id comparison data endpoint."""

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.TRUST_ID_ENDPOINT}/comparison",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertFalse(
            TrustIdComparisonSchema().validate(response.json, many=True)
        )

    def test_trust_id_comparison_default_false(self):
        """Test for trust_id comparison data endpoint using default false."""

        # Add segment.
        response = self.app.post(
            f"{t_c.BASE_ENDPOINT}{api_c.TRUST_ID_ENDPOINT}/segment",
            json={"segment_name": "Test Add Segment", "segment_filters": []},
            headers=t_c.STANDARD_HEADERS,
        )
        self.assertEqual(HTTPStatus.CREATED, response.status_code)

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.TRUST_ID_ENDPOINT}/comparison?default=false",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)

        # Ensure only one segment is present.
        self.assertEqual(1, len(response.json[0].get(api_c.SEGMENTS)))

        # Ensure it is not the default segment.
        self.assertFalse(
            response.json[0].get(api_c.SEGMENTS)[0].get(api_c.DEFAULT)
        )

    def test_trust_id_comparison_default_true(self):
        """Test for trust_id comparison data endpoint using default true."""

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.TRUST_ID_ENDPOINT}/comparison?default=true",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)

        # Ensure only one segment is present.
        self.assertEqual(1, len(response.json[0].get(api_c.SEGMENTS)))

        # Ensure it is the default segment.
        self.assertTrue(
            response.json[0].get(api_c.SEGMENTS)[0].get(api_c.DEFAULT)
        )

    def test_add_trust_id_segment(self):
        """Test for trust_id segment addition endpoint."""

        response = self.app.post(
            f"{t_c.BASE_ENDPOINT}{api_c.TRUST_ID_ENDPOINT}/segment",
            json={"segment_name": "Test Add Segment", "segment_filters": []},
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.CREATED, response.status_code)
        self.assertFalse(
            TrustIdComparisonSchema().validate(response.json, many=True)
        )

    def test_remove_trust_id_segment(self):
        """Test for trust_id segment removal endpoint."""

        response = self.app.post(
            f"{t_c.BASE_ENDPOINT}{api_c.TRUST_ID_ENDPOINT}/segment",
            json={"segment_name": "Test Segment", "segment_filters": []},
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.CREATED, response.status_code)
        self.assertFalse(
            TrustIdComparisonSchema().validate(response.json, many=True)
        )

        response = self.app.delete(
            f"{t_c.BASE_ENDPOINT}{api_c.TRUST_ID_ENDPOINT}/segment",
            query_string={"segment_name": "Test Segment"},
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertFalse(
            TrustIdComparisonSchema().validate(response.json, many=True)
        )
