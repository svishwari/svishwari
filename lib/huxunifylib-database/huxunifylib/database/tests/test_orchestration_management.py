"""Audience Management tests."""

import unittest
import mongomock
import huxunifylib.database.orchestration_management as am
import huxunifylib.database.constants as c
from huxunifylib.database.client import DatabaseClient
import huxunifylib.database.db_exceptions as de


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
                "section_aggregator": c.AUDIENCE_FILTER_AGGREGATOR_ALL,
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
                c.AUDIENCE_FILTERS_SECTION_AGGREGATOR: c.AUDIENCE_FILTER_AGGREGATOR_ANY,
                c.AUDIENCE_FILTERS_SECTION: [
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
        self.destination_ids = ["destination_id1", "destination_id2"]
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

        set_audience = self._setup_audience()
        audience_doc = am.get_audience(self.database, set_audience[c.ID])

        self.assertIsNotNone(audience_doc)
        self.assertTrue(c.ID in audience_doc)
        self.assertIsNotNone(audience_doc[c.AUDIENCE_FILTERS])
        self.assertIsNotNone(audience_doc[c.AUDIENCE_FILTERS][0])
        self.assertEqual(
            audience_doc[c.AUDIENCE_FILTERS][0][
                c.AUDIENCE_FILTERS_SECTION_AGGREGATOR
            ],
            c.AUDIENCE_FILTER_AGGREGATOR_ALL,
        )
        self.assertEqual(
            audience_doc[c.AUDIENCE_FILTERS][1][
                c.AUDIENCE_FILTERS_SECTION_AGGREGATOR
            ],
            c.AUDIENCE_FILTER_AGGREGATOR_ANY,
        )

    def test_update_audience_name(self):
        """Test update audience name."""

        set_audience = self._setup_audience()
        audience_doc = am.get_audience(self.database, set_audience[c.ID])

        self.assertIsNotNone(audience_doc)

        # Update audience name
        new_name = "New name"
        doc = am.update_audience(
            self.database,
            set_audience[c.ID],
            new_name,
        )

        self.assertTrue(doc is not None)
        self.assertTrue(c.AUDIENCE_NAME in doc)
        self.assertEqual(doc[c.AUDIENCE_NAME], new_name)

    def test_duplicate_audience_name(self):
        """Test duplicate audience name."""

        set_audience = self._setup_audience()
        audience_doc = am.get_audience(self.database, set_audience[c.ID])

        self.assertIsNotNone(audience_doc)

        with self.assertRaises(de.DuplicateName):
            am.create_audience(
                self.database,
                "My Audience",
                self.audience_filters,
            )

    def test_update_audience_filters(self):
        """Test update audience filters."""

        set_audience = self._setup_audience()
        audience_doc = am.get_audience(self.database, set_audience[c.ID])

        self.assertIsNotNone(audience_doc)
        self.assertIsNotNone(audience_doc[c.AUDIENCE_FILTERS])
        self.assertIsNotNone(audience_doc[c.AUDIENCE_FILTERS][0])
        self.assertEqual(
            audience_doc[c.AUDIENCE_FILTERS][0][
                c.AUDIENCE_FILTERS_SECTION_AGGREGATOR
            ],
            c.AUDIENCE_FILTER_AGGREGATOR_ALL,
        )
        self.assertEqual(len(audience_doc[c.AUDIENCE_FILTERS]), 2)

        # Update audience filters
        new_filters = [
            {
                c.AUDIENCE_FILTERS_SECTION_AGGREGATOR: c.AUDIENCE_FILTER_AGGREGATOR_ANY,
                c.AUDIENCE_FILTERS_SECTION: [
                    {
                        "field": c.S_TYPE_AGE,
                        "type": c.AUDIENCE_FILTER_MAX,
                        "value": 60,
                    },
                ],
            }
        ]
        doc = am.update_audience(
            self.database,
            set_audience[c.ID],
            set_audience[c.AUDIENCE_NAME],
            new_filters,
        )

        self.assertTrue(doc is not None)
        self.assertTrue(c.AUDIENCE_FILTERS in doc)
        self.assertIsNotNone(doc[c.AUDIENCE_FILTERS][0])
        self.assertEqual(
            doc[c.AUDIENCE_FILTERS][0][c.AUDIENCE_FILTERS_SECTION_AGGREGATOR],
            c.AUDIENCE_FILTER_AGGREGATOR_ANY,
        )
        self.assertEqual(len(doc[c.AUDIENCE_FILTERS]), 1)

    def test_add_audience_with_destination(self):
        """Test add audience with destinations."""

        set_audience = am.create_audience(
            self.database,
            "My Audience",
            self.audience_filters,
            self.destination_ids,
        )
        doc = am.get_audience(self.database, set_audience[c.ID])

        self.assertTrue(doc is not None)
        self.assertTrue(c.AUDIENCE_FILTERS in doc)
        self.assertTrue(c.DESTINATIONS in doc)
        self.assertEqual(doc[c.DESTINATIONS][0], "destination_id1")
        self.assertEqual(doc[c.DESTINATIONS][1], "destination_id2")

    def test_update_audience_destination(self):
        """Test update audience destinations."""

        set_audience = am.create_audience(
            self.database,
            "My Audience",
            self.audience_filters,
            self.destination_ids,
        )
        doc = am.get_audience(self.database, set_audience[c.ID])

        self.assertTrue(doc is not None)
        self.assertTrue(c.AUDIENCE_FILTERS in doc)
        self.assertTrue(c.DESTINATIONS in doc)
        self.assertEqual(doc[c.DESTINATIONS][0], "destination_id1")
        self.assertEqual(doc[c.DESTINATIONS][1], "destination_id2")

        new_destination_ids = ["destination_id1", "destination_id3"]
        am.update_audience(
            self.database,
            set_audience[c.ID],
            "My Audience",
            self.audience_filters,
            new_destination_ids,
        )
        updated_doc = am.get_audience(self.database, set_audience[c.ID])

        self.assertTrue(updated_doc is not None)
        self.assertTrue(c.DESTINATIONS in updated_doc)
        self.assertEqual(updated_doc[c.DESTINATIONS][0], "destination_id1")
        self.assertEqual(updated_doc[c.DESTINATIONS][1], "destination_id3")

    def test_get_all_audiences(self):
        """Test get_all_audiences."""

        self._setup_audience()
        audiences = am.get_all_audiences(self.database)

        self.assertIsNotNone(audiences)
        self.assertEqual(len(audiences), 1)

        am.create_audience(
            self.database,
            "New Audience 1",
            self.audience_filters,
        )

        am.create_audience(
            self.database,
            "New Audience 2",
            self.audience_filters,
        )

        audiences = am.get_all_audiences(self.database)

        self.assertIsNotNone(audiences)
        self.assertEqual(len(audiences), 3)
        self.assertEqual(audiences[0][c.AUDIENCE_NAME], "My Audience")
        self.assertEqual(audiences[1][c.AUDIENCE_NAME], "New Audience 1")
