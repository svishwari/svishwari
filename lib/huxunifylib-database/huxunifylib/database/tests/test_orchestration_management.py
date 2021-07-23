"""Audience Management tests."""

import unittest
import mongomock
import huxunifylib.database.orchestration_management as am
import huxunifylib.database.delivery_platform_management as dpm
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

        # write a user to the database
        self.user_name = "joey galloway"
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
            user_name=self.user_name,
            size=1450,
        )
        return audience_doc

    def test_set_audience(self):
        """Audience is set."""

        audience_doc = self._setup_audience()

        self.assertIsNotNone(audience_doc)
        self.assertIn(c.ID, audience_doc)
        self.assertIn(c.SIZE, audience_doc)
        self.assertEqual(audience_doc[c.SIZE], 1450)

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

    def test_get_audience_with_user(self):
        """Test get audience with user."""

        set_audience = self._setup_audience()
        audience_doc = am.get_audience(self.database, set_audience[c.ID])

        self.assertIsNotNone(audience_doc)
        self.assertIn(c.ID, audience_doc)
        self.assertTrue(audience_doc[c.AUDIENCE_FILTERS])
        self.assertEqual(audience_doc[c.CREATED_BY], self.user_name)

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

    def test_update_audience_name_unchanged(self):
        """Test update audience and check name remains unchanged"""

        set_audience = self._setup_audience()
        audience_doc = am.get_audience(self.database, set_audience[c.ID])

        self.assertIsNotNone(audience_doc)

        doc = am.update_audience(
            self.database,
            set_audience[c.ID],
            destination_ids=self.destination_ids,
            user_name=self.user_name,
        )
        self.assertTrue(doc is not None)
        self.assertTrue(c.AUDIENCE_NAME in doc)
        self.assertEqual(doc[c.AUDIENCE_NAME], set_audience[c.AUDIENCE_NAME])

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
            user_name=self.user_name,
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
            self.user_name,
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
            self.user_name,
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
            user_name=self.user_name,
        )

        am.create_audience(
            self.database,
            "New Audience 2",
            self.audience_filters,
            user_name=self.user_name,
        )

        audiences = am.get_all_audiences(self.database)

        self.assertIsNotNone(audiences)
        self.assertEqual(len(audiences), 3)
        self.assertEqual(audiences[0][c.AUDIENCE_NAME], "My Audience")
        self.assertEqual(audiences[1][c.AUDIENCE_NAME], "New Audience 1")

    def test_get_all_audiences_with_users(self):
        """Test get_all_audiences with users."""

        self._setup_audience()
        audiences = am.get_all_audiences(self.database)

        self.assertIsNotNone(audiences)
        self.assertEqual(len(audiences), 1)

        am.create_audience(
            self.database,
            "Audience User",
            self.audience_filters,
            user_name=self.user_name,
        )

        am.create_audience(
            self.database,
            "New Audience User",
            self.audience_filters,
            user_name=self.user_name,
        )

        audiences = am.get_all_audiences(self.database)

        self.assertIsNotNone(audiences)
        self.assertTrue(
            all(x[c.CREATED_BY] == self.user_name for x in audiences)
        )

    def test_get_all_audiences_with_deliveries(self):
        """Test get_all_audiences with deliveries."""

        # Set delivery platform
        delivery_platform_doc = dpm.set_delivery_platform(
            self.database,
            c.DELIVERY_PLATFORM_FACEBOOK,
            c.DELIVERY_PLATFORM_FACEBOOK.lower(),
            {
                "facebook_access_token": "path1",
                "facebook_app_secret": "path2",
                "facebook_app_id": "path3",
                "facebook_ad_account_id": "path4",
            },
        )

        # set connection status
        dpm.set_connection_status(
            self.database, delivery_platform_doc[c.ID], c.STATUS_SUCCEEDED
        )

        audiences = []
        for i in range(11):
            audience_doc = am.create_audience(
                self.database,
                f"My Audience-{i}",
                self.audience_filters,
                user_name=self.user_name,
                size=i * 1000,
            )
            # create delivery job
            dpm.set_delivery_job(
                self.database,
                audience_doc[c.ID],
                delivery_platform_doc[c.ID],
                [],
            )

            # store the audience obj
            audiences.append(audience_doc)

        # get all audiences and deliveries
        audiences = am.get_all_audiences_and_deliveries(self.database)
        self.assertTrue(audiences)
        self.assertGreater(len(audiences), 10)

        for audience in audiences:
            # test each audience
            self.assertIn(c.DELIVERIES, audience)
            self.assertIn(c.AUDIENCE_LAST_DELIVERED, audience)
            self.assertIn(c.ID, audience)

            # test there are deliveries
            self.assertTrue(audience[c.DELIVERIES])

            for delivery in audience[c.DELIVERIES]:
                self.assertEqual(
                    delivery[c.DELIVERY_PLATFORM_TYPE],
                    c.DELIVERY_PLATFORM_FACEBOOK,
                )
                self.assertEqual(
                    delivery[c.METRICS_DELIVERY_PLATFORM_NAME],
                    delivery_platform_doc[c.DELIVERY_PLATFORM_TYPE],
                )
                self.assertIn(c.UPDATE_TIME, delivery)
                self.assertEqual(delivery[c.STATUS], c.STATUS_PENDING)
