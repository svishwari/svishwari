"""Tests for trust ID APIs."""
from http import HTTPStatus
from unittest import mock

import huxunifylib.database.constants as db_c
from huxunifylib.database.collection_management import create_document
from huxunifylib.database.survey_metrics_management import (
    set_survey_responses_bulk,
)
from huxunify.api import constants as api_c
from huxunify.api.schema.trust_id import (
    TrustIdOverviewSchema,
    TrustIdAttributesSchema,
    TrustIdComparisonSchema,
)
import huxunify.test.constants as t_c
from huxunify.test.route.route_test_util.route_test_case import RouteTestCase


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

        # mock get_db_client() for the cache.
        mock.patch(
            "huxunify.api.data_connectors.cache.get_db_client",
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
        mock.patch(
            "huxunify.api.data_connectors.trust_id.get_trust_id_attributes",
            return_value=t_c.TRUST_ID_ATTRIBUTE_SAMPLE_DATA,
        ).start()

        mock.patch(
            "huxunify.api.data_connectors.trust_id.get_trust_id_overview",
            return_value=t_c.TRUST_ID_OVERVIEW_SAMPLE_DATA,
        ).start()

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.TRUST_ID_ENDPOINT}/comparison",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertFalse(
            TrustIdComparisonSchema().validate(response.json, many=True)
        )

        # Ensure only one segment is present.
        self.assertEqual(1, len(response.json[0].get(api_c.TRUST_ID_SEGMENTS)))

        # Ensure it is the default segment.
        self.assertTrue(
            response.json[0].get(api_c.TRUST_ID_SEGMENTS)[0].get(api_c.DEFAULT)
        )

    def test_trust_id_comparison_default_false(self):
        """Test for trust_id comparison data endpoint using default false."""
        mock.patch(
            "huxunify.api.data_connectors.trust_id.get_trust_id_attributes",
            return_value=t_c.TRUST_ID_ATTRIBUTE_SAMPLE_DATA,
        ).start()

        mock.patch(
            "huxunify.api.data_connectors.trust_id.get_trust_id_overview",
            return_value=t_c.TRUST_ID_OVERVIEW_SAMPLE_DATA,
        ).start()

        # Add segment.
        response = self.app.post(
            f"{t_c.BASE_ENDPOINT}{api_c.TRUST_ID_ENDPOINT}/segment",
            query_string={api_c.DEFAULT: False},
            json={"segment_name": "Test Add Segment", "segment_filters": []},
            headers=t_c.STANDARD_HEADERS,
        )
        self.assertEqual(HTTPStatus.CREATED, response.status_code)

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.TRUST_ID_ENDPOINT}/comparison",
            query_string={api_c.DEFAULT: False},
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)

        self.assertFalse(
            TrustIdComparisonSchema().validate(response.json, many=True)
        )

        # Ensure only one segment is present.
        self.assertEqual(1, len(response.json[0].get(api_c.TRUST_ID_SEGMENTS)))

        # Ensure it is not the default segment.
        self.assertFalse(
            response.json[0].get(api_c.TRUST_ID_SEGMENTS)[0].get(api_c.DEFAULT)
        )

    def test_trust_id_comparison_default_true(self):
        """Test for trust_id comparison data endpoint using default true."""
        mock.patch(
            "huxunify.api.data_connectors.trust_id.get_trust_id_attributes",
            return_value=t_c.TRUST_ID_ATTRIBUTE_SAMPLE_DATA,
        ).start()

        mock.patch(
            "huxunify.api.data_connectors.trust_id.get_trust_id_overview",
            return_value=t_c.TRUST_ID_OVERVIEW_SAMPLE_DATA,
        ).start()

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.TRUST_ID_ENDPOINT}/comparison",
            query_string={api_c.DEFAULT: True},
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)

        self.assertFalse(
            TrustIdComparisonSchema().validate(response.json, many=True)
        )

        # Ensure only one segment is present.
        self.assertEqual(1, len(response.json[0].get(api_c.TRUST_ID_SEGMENTS)))

        # Ensure it is the default segment.
        self.assertTrue(
            response.json[0].get(api_c.TRUST_ID_SEGMENTS)[0].get(api_c.DEFAULT)
        )

    def test_add_trust_id_segment_default_false(self):
        """Test for trust_id segment addition endpoint with default set to false."""
        mock.patch(
            "huxunify.api.data_connectors.trust_id.get_trust_id_attributes",
            return_value=t_c.TRUST_ID_ATTRIBUTE_SAMPLE_DATA,
        ).start()

        mock.patch(
            "huxunify.api.data_connectors.trust_id.get_trust_id_overview",
            return_value=t_c.TRUST_ID_OVERVIEW_SAMPLE_DATA,
        ).start()

        response = self.app.post(
            f"{t_c.BASE_ENDPOINT}{api_c.TRUST_ID_ENDPOINT}/segment",
            query_string={api_c.DEFAULT: False},
            json=t_c.TRUST_ID_SAMPLE_USER_SEGMENT,
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.CREATED, response.status_code)

        self.assertFalse(
            TrustIdComparisonSchema().validate(response.json, many=True)
        )

        # Ensure only one segment is present.
        self.assertEqual(1, len(response.json[0].get(api_c.TRUST_ID_SEGMENTS)))

        # Ensure it is the default segment.
        self.assertFalse(
            response.json[0].get(api_c.TRUST_ID_SEGMENTS)[0].get(api_c.DEFAULT)
        )
        self.assertEqual(
            t_c.TRUST_ID_SAMPLE_USER_SEGMENT[api_c.TRUST_ID_SEGMENT_FILTERS],
            response.json[0].get(api_c.TRUST_ID_SEGMENTS)[0][
                api_c.TRUST_ID_SEGMENT_FILTERS
            ],
        )
        self.assertEqual(
            t_c.TRUST_ID_SAMPLE_USER_SEGMENT[api_c.TRUST_ID_SEGMENT_NAME],
            response.json[0].get(api_c.TRUST_ID_SEGMENTS)[0][
                api_c.TRUST_ID_SEGMENT_NAME
            ],
        )

    def test_add_trust_id_segment_default_true(self):
        """Test for trust_id segment addition endpoint with default set to true."""
        mock.patch(
            "huxunify.api.data_connectors.trust_id.get_trust_id_attributes",
            return_value=t_c.TRUST_ID_ATTRIBUTE_SAMPLE_DATA,
        ).start()

        mock.patch(
            "huxunify.api.data_connectors.trust_id.get_trust_id_overview",
            return_value=t_c.TRUST_ID_OVERVIEW_SAMPLE_DATA,
        ).start()

        response = self.app.post(
            f"{t_c.BASE_ENDPOINT}{api_c.TRUST_ID_ENDPOINT}/segment",
            query_string={api_c.DEFAULT: True},
            json=t_c.TRUST_ID_SAMPLE_USER_SEGMENT,
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.CREATED, response.status_code)

        self.assertFalse(
            TrustIdComparisonSchema().validate(response.json, many=True)
        )

        # Ensure 2 segments is present.
        self.assertEqual(2, len(response.json[0].get(api_c.TRUST_ID_SEGMENTS)))

        # Ensure the first segment is default.
        self.assertTrue(
            response.json[0].get(api_c.TRUST_ID_SEGMENTS)[0].get(api_c.DEFAULT)
        )
        # Ensure one of the segment is not default.
        self.assertFalse(
            response.json[0].get(api_c.TRUST_ID_SEGMENTS)[1].get(api_c.DEFAULT)
        )
        self.assertEqual(
            t_c.TRUST_ID_SAMPLE_USER_SEGMENT[api_c.TRUST_ID_SEGMENT_FILTERS],
            response.json[0].get(api_c.TRUST_ID_SEGMENTS)[1][
                api_c.TRUST_ID_SEGMENT_FILTERS
            ],
        )
        self.assertEqual(
            t_c.TRUST_ID_SAMPLE_USER_SEGMENT[api_c.TRUST_ID_SEGMENT_NAME],
            response.json[0].get(api_c.TRUST_ID_SEGMENTS)[1][
                api_c.TRUST_ID_SEGMENT_NAME
            ],
        )

    def test_remove_trust_id_segment_default_true(self):
        """Test for trust_id segment removal endpoint with default set to true."""

        mock.patch(
            "huxunify.api.data_connectors.trust_id.get_trust_id_attributes",
            return_value=t_c.TRUST_ID_ATTRIBUTE_SAMPLE_DATA,
        ).start()

        mock.patch(
            "huxunify.api.data_connectors.trust_id.get_trust_id_overview",
            return_value=t_c.TRUST_ID_OVERVIEW_SAMPLE_DATA,
        ).start()

        response = self.app.post(
            f"{t_c.BASE_ENDPOINT}{api_c.TRUST_ID_ENDPOINT}/segment",
            query_string={api_c.DEFAULT: True},
            json=t_c.TRUST_ID_SAMPLE_USER_SEGMENT,
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.CREATED, response.status_code)

        self.assertFalse(
            TrustIdComparisonSchema().validate(response.json, many=True)
        )
        # Ensure 2 segments is present.
        self.assertEqual(2, len(response.json[0].get(api_c.TRUST_ID_SEGMENTS)))

        # Ensure the first segment is default.
        self.assertTrue(
            response.json[0].get(api_c.TRUST_ID_SEGMENTS)[0].get(api_c.DEFAULT)
        )
        # Ensure one of the segment is not default.
        self.assertFalse(
            response.json[0].get(api_c.TRUST_ID_SEGMENTS)[1].get(api_c.DEFAULT)
        )

        response = self.app.delete(
            f"{t_c.BASE_ENDPOINT}{api_c.TRUST_ID_ENDPOINT}/segment",
            query_string={
                api_c.DEFAULT: True,
                api_c.TRUST_ID_SEGMENT_NAME: t_c.TRUST_ID_SAMPLE_USER_SEGMENT[
                    api_c.TRUST_ID_SEGMENT_NAME
                ],
            },
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)

        # Ensure 1 segment is present.
        self.assertEqual(1, len(response.json[0].get(api_c.TRUST_ID_SEGMENTS)))

        # Ensure the segment is default.
        self.assertTrue(
            response.json[0].get(api_c.TRUST_ID_SEGMENTS)[0].get(api_c.DEFAULT)
        )

    def test_remove_trust_id_segment_default_false(self):
        """Test for trust_id segment removal endpoint with default set to true."""

        mock.patch(
            "huxunify.api.data_connectors.trust_id.get_trust_id_attributes",
            return_value=t_c.TRUST_ID_ATTRIBUTE_SAMPLE_DATA,
        ).start()

        mock.patch(
            "huxunify.api.data_connectors.trust_id.get_trust_id_overview",
            return_value=t_c.TRUST_ID_OVERVIEW_SAMPLE_DATA,
        ).start()

        response = self.app.post(
            f"{t_c.BASE_ENDPOINT}{api_c.TRUST_ID_ENDPOINT}/segment",
            query_string={api_c.DEFAULT: False},
            json=t_c.TRUST_ID_SAMPLE_USER_SEGMENT,
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.CREATED, response.status_code)

        # Ensure 1 segment is present.
        self.assertEqual(1, len(response.json[0].get(api_c.TRUST_ID_SEGMENTS)))

        # Ensure the segment is not default.
        self.assertFalse(
            response.json[0].get(api_c.TRUST_ID_SEGMENTS)[0].get(api_c.DEFAULT)
        )

        response = self.app.delete(
            f"{t_c.BASE_ENDPOINT}{api_c.TRUST_ID_ENDPOINT}/segment",
            query_string={
                api_c.DEFAULT: False,
                api_c.TRUST_ID_SEGMENT_NAME: t_c.TRUST_ID_SAMPLE_USER_SEGMENT[
                    api_c.TRUST_ID_SEGMENT_NAME
                ],
            },
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)

        self.assertFalse(
            TrustIdComparisonSchema().validate(response.json, many=True)
        )

        # Ensure 1 segment is present.
        self.assertEqual(1, len(response.json[0].get(api_c.TRUST_ID_SEGMENTS)))

        # Ensure the segment is default.
        self.assertTrue(
            response.json[0].get(api_c.TRUST_ID_SEGMENTS)[0].get(api_c.DEFAULT)
        )
