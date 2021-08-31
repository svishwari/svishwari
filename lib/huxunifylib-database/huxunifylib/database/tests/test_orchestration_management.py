"""Audience Management tests."""

import unittest
import mongomock
import pymongo

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
        self.audiences = self._setup_audience()

    def _setup_audience(self) -> dict:

        am.create_audience(
            self.database,
            "Audience1",
            self.audience_filters,
            user_name=self.user_name,
            size=1450,
        )

        am.create_audience(
            self.database,
            "Audience2",
            self.audience_filters,
            user_name=self.user_name,
            size=1500,
        )

        return am.get_all_audiences(self.database)

    def test_set_audience(self):
        """Audience is set."""

        audience_doc = am.get_audience(self.database, self.audiences[0][c.ID])

        self.assertIsNotNone(audience_doc)
        self.assertIn(c.ID, audience_doc)
        self.assertIn(c.SIZE, audience_doc)
        self.assertEqual(1450, audience_doc[c.SIZE])

    def test_get_audience_filter_variant(self):
        """Test get audiences. The filter variant of the function"""

        audience = am.get_audience_by_filter(
            self.database, filter_dict={c.ID: self.audiences[1][c.ID]}, limit=1
        )

        self.assertEqual("Audience2", audience[0][c.NAME])

    def test_get_audience_filter_variant_order_by_name(self):
        """Test get audiences. The filter variant of the function.
        Get the audiences ordered by name"""

        audience = am.get_audience_by_filter(
            self.database, sort_list=[("name", pymongo.DESCENDING)]
        )

        self.assertEqual("Audience2", audience[0][c.NAME])
        self.assertEqual("Audience1", audience[1][c.NAME])

    def test_get_audience_filter_variant_filter_for_name(self):
        """Test get audiences. The filter variant of the function.
        Get only the name of the audience"""

        audience = am.get_audience_by_filter(
            self.database, {}, {}, [("name", pymongo.DESCENDING)]
        )

        self.assertEqual("Audience2", audience[0][c.NAME])

    def test_get_audience(self):
        """Test get audience."""

        audience_doc = am.get_audience(self.database, self.audiences[0][c.ID])

        self.assertIsNotNone(audience_doc)
        self.assertTrue(c.ID in audience_doc)
        self.assertIsNotNone(audience_doc[c.AUDIENCE_FILTERS])
        self.assertIsNotNone(audience_doc[c.AUDIENCE_FILTERS][0])
        self.assertEqual(
            c.AUDIENCE_FILTER_AGGREGATOR_ALL,
            audience_doc[c.AUDIENCE_FILTERS][0][
                c.AUDIENCE_FILTERS_SECTION_AGGREGATOR
            ],
        )
        self.assertEqual(
            c.AUDIENCE_FILTER_AGGREGATOR_ANY,
            audience_doc[c.AUDIENCE_FILTERS][1][
                c.AUDIENCE_FILTERS_SECTION_AGGREGATOR
            ],
        )

    def test_get_audience_with_user(self):
        """Test get audience with user."""

        audience_doc = am.get_audience(self.database, self.audiences[0][c.ID])

        self.assertIsNotNone(audience_doc)
        self.assertIn(c.ID, audience_doc)
        self.assertTrue(audience_doc[c.AUDIENCE_FILTERS])
        self.assertEqual(self.user_name, audience_doc[c.CREATED_BY])

    def test_update_audience_name(self):
        """Test update audience name."""

        audience_doc = self.audiences[0]

        self.assertIsNotNone(audience_doc)

        # Update audience name
        new_name = "New name"
        doc = am.update_audience(
            self.database,
            audience_doc[c.ID],
            new_name,
        )

        self.assertTrue(doc is not None)
        self.assertTrue(c.AUDIENCE_NAME in doc)
        self.assertEqual(doc[c.AUDIENCE_NAME], new_name)

    def test_update_audience_name_unchanged(self):
        """Test update audience and check name remains unchanged"""

        audience_doc = self.audiences[0]

        self.assertIsNotNone(audience_doc)

        doc = am.update_audience(
            self.database,
            audience_doc[c.ID],
            destination_ids=self.destination_ids,
            user_name=self.user_name,
        )
        self.assertTrue(doc is not None)
        self.assertTrue(c.AUDIENCE_NAME in doc)
        self.assertEqual(audience_doc[c.AUDIENCE_NAME], doc[c.AUDIENCE_NAME])

    def test_duplicate_audience_name(self):
        """Test duplicate audience name."""

        audience_doc = am.get_audience(self.database, self.audiences[0][c.ID])

        self.assertIsNotNone(audience_doc)

        with self.assertRaises(de.DuplicateName):
            am.create_audience(
                self.database,
                "Audience1",
                self.audience_filters,
            )

    def test_update_audience_filters(self):
        """Test update audience filters."""

        audience_doc = self.audiences[0]

        self.assertIsNotNone(audience_doc)
        self.assertIsNotNone(audience_doc[c.AUDIENCE_FILTERS])
        self.assertIsNotNone(audience_doc[c.AUDIENCE_FILTERS][0])
        self.assertEqual(
            audience_doc[c.AUDIENCE_FILTERS][0][
                c.AUDIENCE_FILTERS_SECTION_AGGREGATOR
            ],
            c.AUDIENCE_FILTER_AGGREGATOR_ALL,
        )
        self.assertEqual(2, len(audience_doc[c.AUDIENCE_FILTERS]))

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
            audience_doc[c.ID],
            audience_doc[c.AUDIENCE_NAME],
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
        self.assertEqual(1, len(doc[c.AUDIENCE_FILTERS]))

    def test_delete_audience(self):
        """Test delete an audience"""

        all_audiences = am.get_all_audiences(self.database)

        self.assertTrue(
            am.delete_audience(self.database, self.audiences[0][c.ID])
        )

        audiences = am.get_all_audiences(self.database)

        self.assertEqual(len(all_audiences) - 1, len(audiences))

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
        self.assertEqual("destination_id1", doc[c.DESTINATIONS][0])
        self.assertEqual("destination_id2", doc[c.DESTINATIONS][1])

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
        self.assertEqual("destination_id1", doc[c.DESTINATIONS][0])
        self.assertEqual("destination_id2", doc[c.DESTINATIONS][1])

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
        self.assertEqual("destination_id1", updated_doc[c.DESTINATIONS][0])
        self.assertEqual("destination_id3", updated_doc[c.DESTINATIONS][1])

    def test_get_all_audiences(self):
        """Test get_all_audiences."""

        self.assertIsNotNone(self.audiences)
        self.assertEqual(2, len(self.audiences))

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
        self.assertEqual(len(audiences), 4)
        self.assertEqual("Audience1", audiences[0][c.AUDIENCE_NAME])
        self.assertEqual("Audience2", audiences[1][c.AUDIENCE_NAME])

    def test_get_all_audiences_with_users(self):
        """Test get_all_audiences with users."""

        self.assertIsNotNone(self.audiences)
        self.assertEqual(len(self.audiences), 2)

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
            self.assertIsNotNone(audience[c.DELIVERIES])

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
                self.assertEqual(
                    delivery[c.STATUS], c.AUDIENCE_STATUS_DELIVERING
                )
