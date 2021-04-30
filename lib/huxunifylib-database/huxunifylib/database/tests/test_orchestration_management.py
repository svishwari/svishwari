"""Audience Management tests."""

import unittest
import mongomock
import huxunifylib.database.orchestration_management as am
import huxunifylib.database.constants as c
from huxunifylib.database.client import DatabaseClient


# pylint: disable=R0904
class TestAudienceManagement(unittest.TestCase):
    """Test audience management module."""

    @mongomock.patch(servers=(("localhost", 27017),))
    def setUp(self):

        self.database = DatabaseClient(
            "localhost", 27017, None, None
        ).connect()
        self.database.drop_database(c.DATA_MANAGEMENT_DATABASE)

        self.audience_filters = [
            {
                "section_aggregator": "ALL",
                "section_filters": [
                    {
                        "field": c.S_TYPE_AGE,
                        "type": c.AUDIENCE_FILTER_MAX,
                        "value": 60,
                    },
                    {
                        "field": c.S_TYPE_COUNTRY_CODE,
                        "type": c.AUDIENCE_FILTER_INCLUDE,
                        "value": "UK",
                    },
                    {
                        "field": c.S_TYPE_CITY,
                        "type": c.AUDIENCE_FILTER_EXCLUDE,
                        "value": ["London"],
                    },
                ],
            },
            {
                "section_aggregator": "ALL",
                "section_filters": [
                    {
                        "field": c.S_TYPE_AGE,
                        "type": c.AUDIENCE_FILTER_MAX,
                        "value": 50,
                    },
                    {
                        "field": c.S_TYPE_COUNTRY_CODE,
                        "type": c.AUDIENCE_FILTER_INCLUDE,
                        "value": "US",
                    },
                ],
            },
        ]

        self.audience_doc = None

    def _setup_audience(self) -> dict:

        audience_doc = am.create_audience(
            self.database,
            "My Audience",
            self.audience_filters,
        )
        return audience_doc

    def test_set_audience(self):
        """Audience is set."""

        audience_doc = self._setup_audience()

        self.assertIsNotNone(audience_doc)
        self.assertTrue(c.ID in audience_doc)

    def test_get_audience(self):
        """Test get audience."""

        audience_doc = am.get_audience_doc(self.database, c.ID)

        self.assertIsNotNone(audience_doc)
        self.assertTrue(c.ID in audience_doc)
        self.assertIsNotNone(audience_doc[c.AUDIENCE_FILTERS])
        self.assertIsNotNone(audience_doc[c.AUDIENCE_FILTERS][0])
