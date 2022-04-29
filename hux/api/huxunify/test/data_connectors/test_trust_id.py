"""Purpose of this file is to house tests for methods in TrustID connectors."""
from unittest import TestCase

import mongomock

from huxunify.api import constants as api_c
from huxunify.api.data_connectors.trust_id import aggregate_attributes

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

        set_survey_responses_bulk(self.database, t_c.TRUST_ID_SURVEY_RESPONSES)

    def test_aggregate_attributes(self):
        """Test aggregate_attributes method."""

        survey_responses = get_survey_responses(self.database)
        aggregated_attributes = aggregate_attributes(survey_responses)
        self.assertIsInstance(aggregated_attributes, dict)

        # Ensure all factors are present.
        api_c.LIST_OF_FACTORS.sort()
        self.assertEqual(api_c.LIST_OF_FACTORS,
                         sorted(list(aggregated_attributes.keys())))

        self.assertIsInstance(aggregated_attributes[api_c.LIST_OF_FACTORS[0]],
                              dict)

