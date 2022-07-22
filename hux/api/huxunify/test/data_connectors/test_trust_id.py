"""Purpose of this file is to house tests for methods in TrustID connectors."""
from unittest import TestCase
from unittest import mock
import mongomock

from huxunify.api import constants as api_c
from huxunify.api.data_connectors.trust_id import (
    get_trust_id_overview_data,
    get_trust_id_attributes_data,
    get_trust_id_comparison_data,
)
import huxunifylib.database.constants as db_c
from huxunifylib.database.client import DatabaseClient
from huxunifylib.database.collection_management import create_document
from huxunifylib.database.survey_metrics_management import (
    set_survey_responses_bulk,
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
            "huxunify.api.data_connectors.cache.get_db_client",
            return_value=self.database,
        ).start()

        create_document(
            self.database,
            db_c.CONFIGURATIONS_COLLECTION,
            {
                db_c.CONFIGURATION_FIELD_TYPE: db_c.TRUST_ID_ATTRIBUTES,
                db_c.CONFIGURATION_FIELD_NAME: "TrustID Attributes",
                db_c.ATTRIBUTES: t_c.TRUST_ID_ATTRIBUTE_DESCRIPTION_MAP,
            },
        )
        set_survey_responses_bulk(self.database, t_c.TRUST_ID_SURVEY_RESPONSES)

    def test_get_trust_id_attributes(self):
        """Test get_trust_attributes method."""
        mock.patch(
            "huxunify.api.data_connectors.trust_id.get_trust_id_attributes",
            return_value=t_c.TRUST_ID_ATTRIBUTE_SAMPLE_DATA,
        ).start()

        attributes = get_trust_id_attributes_data(self.database)

        self.assertIsInstance(attributes, list)
        # Ensure all attributes are for list of factors.
        filtered_attributes = list(
            filter(
                lambda x: bool(
                    x.get(api_c.TRUST_ID_FACTOR_NAME)
                    in api_c.TRUST_ID_LIST_OF_FACTORS
                ),
                attributes,
            )
        )
        self.assertEqual(len(attributes), len(filtered_attributes))

        self.assertEqual(
            t_c.TRUST_ID_AGGREGATED_ATTRIBUTE_SAMPLE_DATA, attributes
        )

    def test_get_trust_id_overview(self):
        """Test get_trust_id_overview method."""

        mock.patch(
            "huxunify.api.data_connectors.trust_id.get_trust_id_overview",
            return_value=t_c.TRUST_ID_OVERVIEW_SAMPLE_DATA,
        ).start()
        overview = get_trust_id_overview_data(self.database)

        # Ensure all factors in list
        factors_present = sorted(
            list(
                map(
                    lambda x: x.get(api_c.TRUST_ID_FACTOR_NAME),
                    overview.get(api_c.TRUST_ID_FACTORS),
                )
            )
        )
        self.assertEqual(
            sorted(api_c.TRUST_ID_LIST_OF_FACTORS), factors_present
        )

        # Ensure Trust ID score is present.
        self.assertEqual(
            t_c.TRUST_ID_AGGREGATED_OVERVIEW_SAMPLE_DATA[api_c.TRUST_ID_SCORE],
            overview.get(api_c.TRUST_ID_SCORE),
        )

    def test_get_trust_id_comparison_data(self):
        """Test get_trust_id_comparison_data method."""
        mock.patch(
            "huxunify.api.data_connectors.trust_id.get_trust_id_attributes",
            return_value=t_c.TRUST_ID_ATTRIBUTE_SAMPLE_DATA,
        ).start()

        segments = [
            {
                api_c.TRUST_ID_SEGMENT_NAME: api_c.DEFAULT_TRUST_SEGMENT,
                api_c.TRUST_ID_SEGMENT_FILTERS: [],
                api_c.DEFAULT: True,
            }
        ]
        comparison_data = get_trust_id_comparison_data(self.database, segments)
        self.assertIsInstance(comparison_data, list)
        self.assertIsInstance(comparison_data[0], dict)
