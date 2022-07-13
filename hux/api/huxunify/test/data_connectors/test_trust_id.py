"""Purpose of this file is to house tests for methods in TrustID connectors."""
from unittest import TestCase
from unittest import mock
import mongomock

from huxunify.api import constants as api_c
from huxunify.api.data_connectors.trust_id import (
    aggregate_attributes,
    get_trust_id_attributes,
    get_trust_id_overview,
    get_trust_id_comparison_data,
)
from huxunify.api.data_connectors.trust_id import populate_trust_id_segments

from huxunifylib.database.client import DatabaseClient
from huxunifylib.database.survey_metrics_management import (
    set_survey_responses_bulk,
    get_survey_responses,
)

import huxunify.test.constants as t_c


class TrustIDTest(TestCase):
    """Test cases for methods in TrustID data_connectors."""

    def setUp(self) -> None:
        """Setup tests."""

        mongo_patch = mongomock.patch(servers=(("localhost", 27017),))
        mongo_patch.start()

        self.database = DatabaseClient(
            "localhost", 27017, None, None
        ).connect()

        mock.patch(
            "huxunify.api.route.utils.get_db_client",
            return_value=self.database,
        ).start()

        set_survey_responses_bulk(self.database, t_c.TRUST_ID_SURVEY_RESPONSES)

    def test_aggregate_attributes(self):
        """Test aggregate_attributes method."""

        survey_responses = get_survey_responses(self.database)
        aggregated_attributes = aggregate_attributes(survey_responses)

        self.assertIsInstance(aggregated_attributes, dict)

        # Ensure all factors are present.
        api_c.LIST_OF_FACTORS.sort()
        self.assertEqual(
            api_c.LIST_OF_FACTORS, sorted(list(aggregated_attributes.keys()))
        )

        self.assertIsInstance(
            aggregated_attributes[api_c.LIST_OF_FACTORS[0]], dict
        )

        # Check if sample data is present in data.
        for (
            attr_name,
            expected_attr_val,
        ) in t_c.TRUST_ID_SAMPLE_HUMANITY_ATTRIBUTE_AGG.items():
            attribute = aggregated_attributes[api_c.HUMANITY].get(attr_name)
            self.assertEqual(expected_attr_val, attribute)

    def test_get_trust_id_attributes(self):
        """Test get_trust_attributes method."""

        survey_responses = get_survey_responses(self.database)
        attributes = get_trust_id_attributes(survey_responses)

        self.assertIsInstance(attributes, list)
        # Ensure all attributes are for list of factors.
        filtered_attributes = list(
            filter(
                lambda x: bool(
                    x.get(api_c.FACTOR_NAME) in api_c.LIST_OF_FACTORS
                ),
                attributes,
            )
        )
        self.assertEqual(len(attributes), len(filtered_attributes))

        # Ensure sample humanity attribute in list.
        self.assertIn(t_c.TRUST_ID_SAMPLE_HUMANITY_ATTRIBUTE, attributes)

    def test_get_trust_id_overview(self):
        """Test get_trust_id_overview method."""

        survey_responses = get_survey_responses(self.database)
        overview = get_trust_id_overview(survey_responses)
        self.assertEqual(True, True)

        # Ensure all factors in list
        factors_present = sorted(
            list(
                map(
                    lambda x: x.get(api_c.FACTOR_NAME),
                    overview.get(api_c.FACTORS),
                )
            )
        )
        self.assertEqual(sorted(api_c.LIST_OF_FACTORS), factors_present)

        self.assertIn(
            t_c.TRUST_ID_SAMPLE_HUMANITY_OVERVIEW, overview.get(api_c.FACTORS)
        )

        # Ensure Trust ID score is present.
        self.assertEqual(overview.get(api_c.TRUST_ID_SCORE), 100)

    def test_get_trust_id_comparison_data(self):
        """Test get_trust_id_comparison_data method."""

        segments_data = populate_trust_id_segments(
            database=self.database,
            custom_segments=t_c.TRUST_ID_SAMPLE_USER_SEGMENT,
        )

        comparison_data = get_trust_id_comparison_data(segments_data)
        self.assertIsInstance(comparison_data, list)
        self.assertIsInstance(comparison_data[0], dict)

        self.assertIsInstance(comparison_data[1].get(api_c.SEGMENTS), list)

        self.assertEqual(
            t_c.TRUST_ID_SAMPLE_USER_SEGMENT[0].get(api_c.SEGMENT_NAME),
            comparison_data[1].get(api_c.SEGMENTS)[1].get(api_c.SEGMENT_NAME),
        )

        self.assertEqual(
            t_c.TRUST_ID_SAMPLE_USER_SEGMENT[0].get(api_c.SEGMENT_FILTERS),
            comparison_data[1]
            .get(api_c.SEGMENTS)[1]
            .get(api_c.SEGMENT_FILTERS),
        )
