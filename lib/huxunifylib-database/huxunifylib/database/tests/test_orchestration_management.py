"""Audience Management tests."""

import unittest
from unittest import mock

import mongomock
import pymongo
from bson import ObjectId

import huxunifylib.database.orchestration_management as am
import huxunifylib.database.delivery_platform_management as dpm
from huxunifylib.database.user_management import set_user
import huxunifylib.database.constants as db_c
from huxunifylib.database.client import DatabaseClient
import huxunifylib.database.db_exceptions as de


class TestAudienceManagement(unittest.TestCase):
    """Test audience management module."""

    @mongomock.patch(servers=(("localhost", 27017),))
    def setUp(self):

        self.database = DatabaseClient(
            "localhost", 27017, None, None
        ).connect()
        self.database.drop_database(db_c.DATA_MANAGEMENT_DATABASE)

        # write a user to the database
        self.user_name = "joey galloway"
        self.audience_filters = [
            {
                "section_aggregator": db_c.AUDIENCE_FILTER_AGGREGATOR_ALL,
                "section_filters": [
                    {
                        "field": db_c.S_TYPE_AGE,
                        "type": db_c.AUDIENCE_FILTER_MAX,
                        "value": 60,
                    },
                    {
                        "field": db_c.S_TYPE_COUNTRY_CODE,
                        "type": db_c.AUDIENCE_FILTER_INCLUDE,
                        "value": "UK",
                    },
                    {
                        "field": db_c.S_TYPE_CITY,
                        "type": db_c.AUDIENCE_FILTER_EXCLUDE,
                        "value": ["London"],
                    },
                ],
            },
            {
                db_c.AUDIENCE_FILTERS_SECTION_AGGREGATOR: db_c.AUDIENCE_FILTER_AGGREGATOR_ANY,
                db_c.AUDIENCE_FILTERS_SECTION: [
                    {
                        "field": db_c.S_TYPE_AGE,
                        "type": db_c.AUDIENCE_FILTER_MAX,
                        "value": 50,
                    },
                    {
                        "field": db_c.S_TYPE_COUNTRY_CODE,
                        "type": db_c.AUDIENCE_FILTER_INCLUDE,
                        "value": "US",
                    },
                ],
            },
        ]
        self.destination_ids = ["destination_id1", "destination_id2"]
        self.audience_doc = None

        self.sample_user = {
            db_c.OKTA_ID: "00ub0oNGTSWTBKOLGLNR",
            db_c.S_TYPE_EMAIL: "user1@deloitte.com",
            db_c.USER_ORGANIZATION: "deloitte",
            db_c.USER_DISPLAY_NAME: "User1",
            db_c.USER_ROLE: db_c.USER_ROLE_ADMIN,
            db_c.USER_PROFILE_PHOTO: "https://s3/unififed/3.png",
        }

        set_user(self.database, **self.sample_user)

    def _setup_audience(self) -> list:
        """Setup audience

        Returns:
            (list): List of all audiences
        """
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

        audiences = self._setup_audience()
        audience_doc = am.get_audience(self.database, audiences[0][db_c.ID])

        self.assertIsNotNone(audience_doc)
        self.assertIn(db_c.ID, audience_doc)
        self.assertIn(db_c.SIZE, audience_doc)
        self.assertEqual(audience_doc[db_c.SIZE], 1450)

    def test_get_audience_filter_variant(self):
        """Test get audiences. The filter variant of the function"""

        audiences = self._setup_audience()

        audience = am.get_audience_by_filter(
            self.database,
            filter_dict={db_c.ID: audiences[1][db_c.ID]},
            limit=1,
        )

        self.assertEqual("Audience2", audience[0][db_c.NAME])

    def test_get_audience_filter_variant_order_by_name(self):
        """Test get audiences. The filter variant of the function.
        Get the audiences ordered by name"""

        self._setup_audience()

        audience = am.get_audience_by_filter(
            self.database, sort_list=[("name", pymongo.DESCENDING)]
        )

        self.assertEqual("Audience2", audience[0][db_c.NAME])
        self.assertEqual("Audience1", audience[1][db_c.NAME])

    def test_get_audience_filter_variant_filter_for_name(self):
        """Test get audiences. The filter variant of the function.
        Get only the name of the audience"""

        self._setup_audience()

        audience = am.get_audience_by_filter(
            self.database, {}, {}, [("name", pymongo.DESCENDING)]
        )

        self.assertEqual("Audience2", audience[0][db_c.NAME])

    def test_get_audience(self):
        """Test get audience."""

        set_audience = self._setup_audience()
        audience_doc = am.get_audience(self.database, set_audience[0][db_c.ID])

        self.assertIsNotNone(audience_doc)
        self.assertTrue(db_c.ID in audience_doc)
        self.assertIsNotNone(audience_doc[db_c.AUDIENCE_FILTERS])
        self.assertIsNotNone(audience_doc[db_c.AUDIENCE_FILTERS][0])
        self.assertEqual(
            audience_doc[db_c.AUDIENCE_FILTERS][0][
                db_c.AUDIENCE_FILTERS_SECTION_AGGREGATOR
            ],
            db_c.AUDIENCE_FILTER_AGGREGATOR_ALL,
        )
        self.assertEqual(
            audience_doc[db_c.AUDIENCE_FILTERS][1][
                db_c.AUDIENCE_FILTERS_SECTION_AGGREGATOR
            ],
            db_c.AUDIENCE_FILTER_AGGREGATOR_ANY,
        )

    def test_get_audience_with_user(self):
        """Test get audience with user."""

        set_audience = self._setup_audience()
        audience_doc = am.get_audience(self.database, set_audience[0][db_c.ID])

        self.assertIsNotNone(audience_doc)
        self.assertIn(db_c.ID, audience_doc)
        self.assertTrue(audience_doc[db_c.AUDIENCE_FILTERS])
        self.assertEqual(audience_doc[db_c.CREATED_BY], self.user_name)

    def test_update_audience_name(self):
        """Test update audience name."""

        set_audience = self._setup_audience()
        audience_doc = am.get_audience(self.database, set_audience[0][db_c.ID])

        self.assertIsNotNone(audience_doc)

        # Update audience name
        new_name = "New name"
        doc = am.update_audience(
            self.database,
            audience_doc[db_c.ID],
            self.user_name,
            new_name,
        )

        self.assertTrue(doc is not None)
        self.assertTrue(db_c.AUDIENCE_NAME in doc)
        self.assertEqual(doc[db_c.AUDIENCE_NAME], new_name)

    def test_update_audience_name_unchanged(self):
        """Test update audience and check name remains unchanged"""

        set_audience = self._setup_audience()
        audience_doc = am.get_audience(self.database, set_audience[0][db_c.ID])

        self.assertIsNotNone(audience_doc)

        doc = am.update_audience(
            self.database,
            audience_doc[db_c.ID],
            user_name=self.user_name,
            destination_ids=self.destination_ids,
        )
        self.assertTrue(doc is not None)
        self.assertTrue(db_c.AUDIENCE_NAME in doc)
        self.assertEqual(
            doc[db_c.AUDIENCE_NAME], audience_doc[db_c.AUDIENCE_NAME]
        )

    def test_duplicate_audience_name(self):
        """Test duplicate audience name."""

        set_audience = self._setup_audience()
        audience_doc = am.get_audience(self.database, set_audience[0][db_c.ID])

        self.assertIsNotNone(audience_doc)

        with self.assertRaises(de.DuplicateName):
            am.create_audience(
                self.database,
                "Audience1",
                self.audience_filters,
                self.user_name,
            )

    def test_update_audience_filters(self):
        """Test update audience filters."""

        set_audience = self._setup_audience()
        audience_doc = am.get_audience(self.database, set_audience[0][db_c.ID])

        self.assertIsNotNone(audience_doc)
        self.assertIsNotNone(audience_doc[db_c.AUDIENCE_FILTERS])
        self.assertIsNotNone(audience_doc[db_c.AUDIENCE_FILTERS][0])
        self.assertEqual(
            audience_doc[db_c.AUDIENCE_FILTERS][0][
                db_c.AUDIENCE_FILTERS_SECTION_AGGREGATOR
            ],
            db_c.AUDIENCE_FILTER_AGGREGATOR_ALL,
        )
        self.assertEqual(len(audience_doc[db_c.AUDIENCE_FILTERS]), 2)

        # Update audience filters
        new_filters = [
            {
                db_c.AUDIENCE_FILTERS_SECTION_AGGREGATOR: db_c.AUDIENCE_FILTER_AGGREGATOR_ANY,
                db_c.AUDIENCE_FILTERS_SECTION: [
                    {
                        "field": db_c.S_TYPE_AGE,
                        "type": db_c.AUDIENCE_FILTER_MAX,
                        "value": 60,
                    },
                ],
            }
        ]
        doc = am.update_audience(
            self.database,
            audience_doc[db_c.ID],
            self.user_name,
            audience_doc[db_c.AUDIENCE_NAME],
            new_filters,
        )

        self.assertTrue(doc is not None)
        self.assertTrue(db_c.AUDIENCE_FILTERS in doc)
        self.assertIsNotNone(doc[db_c.AUDIENCE_FILTERS][0])
        self.assertEqual(
            doc[db_c.AUDIENCE_FILTERS][0][
                db_c.AUDIENCE_FILTERS_SECTION_AGGREGATOR
            ],
            db_c.AUDIENCE_FILTER_AGGREGATOR_ANY,
        )
        self.assertEqual(len(doc[db_c.AUDIENCE_FILTERS]), 1)

    def test_add_audience_with_destination(self):
        """Test add audience with destinations."""

        set_audience = am.create_audience(
            self.database,
            "My Audience",
            self.audience_filters,
            self.user_name,
            self.destination_ids,
        )
        doc = am.get_audience(self.database, set_audience[db_c.ID])

        self.assertTrue(doc is not None)
        self.assertTrue(db_c.AUDIENCE_FILTERS in doc)
        self.assertTrue(db_c.DESTINATIONS in doc)
        self.assertEqual(doc[db_c.DESTINATIONS][0], "destination_id1")
        self.assertEqual(doc[db_c.DESTINATIONS][1], "destination_id2")

    def test_update_audience_destination(self):
        """Test update audience destinations."""

        set_audience = am.create_audience(
            self.database,
            "My Audience",
            self.audience_filters,
            self.user_name,
            self.destination_ids,
        )
        doc = am.get_audience(self.database, set_audience[db_c.ID])

        self.assertTrue(doc is not None)
        self.assertTrue(db_c.AUDIENCE_FILTERS in doc)
        self.assertTrue(db_c.DESTINATIONS in doc)
        self.assertEqual(doc[db_c.DESTINATIONS][0], "destination_id1")
        self.assertEqual(doc[db_c.DESTINATIONS][1], "destination_id2")

        new_destination_ids = ["destination_id1", "destination_id3"]
        am.update_audience(
            self.database,
            set_audience[db_c.ID],
            self.user_name,
            "My Audience",
            self.audience_filters,
            new_destination_ids,
        )
        updated_doc = am.get_audience(self.database, set_audience[db_c.ID])

        self.assertTrue(updated_doc is not None)
        self.assertTrue(db_c.DESTINATIONS in updated_doc)
        self.assertEqual(updated_doc[db_c.DESTINATIONS][0], "destination_id1")
        self.assertEqual(updated_doc[db_c.DESTINATIONS][1], "destination_id3")

    def test_get_all_audiences(self):
        """Test get_all_audiences."""

        self._setup_audience()
        audiences = am.get_all_audiences(self.database)

        self.assertIsNotNone(audiences)
        self.assertEqual(len(audiences), 2)

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
        self.assertEqual(audiences[0][db_c.AUDIENCE_NAME], "Audience1")
        self.assertEqual(audiences[1][db_c.AUDIENCE_NAME], "Audience2")

    def test_get_all_audiences_filter(self):
        """Test get_all_audiences with filters."""
        audience_1 = am.create_audience(
            self.database,
            "Audience1",
            self.audience_filters,
            user_name=self.user_name,
            size=1450,
        )

        am.create_audience(
            self.database,
            "User1 Audience",
            [],
            user_name=self.sample_user.get(db_c.USER_DISPLAY_NAME),
            size=1500,
        )

        # Attribute filters.
        filters = {db_c.ATTRIBUTE: [db_c.AGE, db_c.S_TYPE_CITY]}
        filtered_audiences = am.get_all_audiences(
            self.database, filters=filters
        )
        self.assertEqual(len(filtered_audiences), 1)

        # Worked by filter.
        filters = {
            db_c.WORKED_BY: self.sample_user.get(db_c.USER_DISPLAY_NAME)
        }
        filtered_audiences = am.get_all_audiences(
            self.database, filters=filters
        )
        self.assertEqual(
            filtered_audiences[0][db_c.CREATED_BY],
            self.sample_user.get(db_c.USER_DISPLAY_NAME),
        )

        # List of audience_ids
        filters = {db_c.ATTRIBUTE: [db_c.AGE, db_c.S_TYPE_CITY]}
        filtered_audiences = am.get_all_audiences(
            self.database,
            filters=filters,
            audience_ids=[audience_1.get(db_c.ID)],
        )
        self.assertEqual(
            filtered_audiences[0][db_c.ID], audience_1.get(db_c.ID)
        )

    def test_get_all_audiences_with_users(self):
        """Test get_all_audiences with users."""

        self._setup_audience()
        audiences = am.get_all_audiences(self.database)

        self.assertIsNotNone(audiences)
        self.assertEqual(len(audiences), 2)

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
            all(x[db_c.CREATED_BY] == self.user_name for x in audiences)
        )

    def test_get_all_audiences_with_deliveries(self):
        """Test get_all_audiences with deliveries."""

        # Set delivery platform
        delivery_platform_doc = dpm.set_delivery_platform(
            self.database,
            db_c.DELIVERY_PLATFORM_FACEBOOK,
            db_c.DELIVERY_PLATFORM_FACEBOOK.lower(),
            {
                "facebook_access_token": "path1",
                "facebook_app_secret": "path2",
                "facebook_app_id": "path3",
                "facebook_ad_account_id": "path4",
            },
        )

        # set connection status
        dpm.set_connection_status(
            self.database,
            delivery_platform_doc[db_c.ID],
            db_c.STATUS_SUCCEEDED,
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
                audience_doc[db_c.ID],
                delivery_platform_doc[db_c.ID],
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
            self.assertIn(db_c.DELIVERIES, audience)
            self.assertIn(db_c.AUDIENCE_LAST_DELIVERED, audience)
            self.assertIn(db_c.ID, audience)

            # test there are deliveries
            self.assertTrue(audience[db_c.DELIVERIES])

            for delivery in audience[db_c.DELIVERIES]:
                self.assertEqual(
                    delivery[db_c.DELIVERY_PLATFORM_TYPE],
                    db_c.DELIVERY_PLATFORM_FACEBOOK,
                )
                self.assertEqual(
                    delivery[db_c.METRICS_DELIVERY_PLATFORM_NAME],
                    delivery_platform_doc[db_c.DELIVERY_PLATFORM_TYPE],
                )
                self.assertIn(db_c.UPDATE_TIME, delivery)
                self.assertEqual(
                    delivery[db_c.STATUS], db_c.AUDIENCE_STATUS_DELIVERING
                )

    def test_get_all_audiences_with_deliveries_filters(self):
        """Test get_all_audiences with deliveries and filters."""

        # Set delivery platform
        delivery_platform_doc = dpm.set_delivery_platform(
            self.database,
            db_c.DELIVERY_PLATFORM_FACEBOOK,
            db_c.DELIVERY_PLATFORM_FACEBOOK.lower(),
            {
                "facebook_access_token": "path1",
                "facebook_app_secret": "path2",
                "facebook_app_id": "path3",
                "facebook_ad_account_id": "path4",
            },
        )

        # set connection status
        dpm.set_connection_status(
            self.database,
            delivery_platform_doc[db_c.ID],
            db_c.STATUS_SUCCEEDED,
        )

        audiences = []
        for i in range(2):
            audience_doc = am.create_audience(
                self.database,
                f"My Audience-{i}",
                self.audience_filters,
                user_name=self.sample_user.get(db_c.USER_DISPLAY_NAME),
                size=i * 1000,
            )
            # create delivery job
            dpm.set_delivery_job(
                self.database,
                audience_doc[db_c.ID],
                delivery_platform_doc[db_c.ID],
                [],
            )

            # store the audience obj
            audiences.append(audience_doc)

        # Worked by filters.
        filters = {
            db_c.WORKED_BY: self.sample_user.get(db_c.USER_DISPLAY_NAME),
        }
        audiences_filtered = am.get_all_audiences_and_deliveries(
            self.database, filters=filters
        )
        self.assertEqual(audiences_filtered[0][db_c.ID], audiences[0][db_c.ID])

        # Attribute filters.
        filters = {
            db_c.ATTRIBUTE: [db_c.AGE, db_c.S_TYPE_CITY],
        }
        audiences_filtered = am.get_all_audiences_and_deliveries(
            self.database, filters=filters
        )
        self.assertEqual(len(audiences_filtered), 2)

        # List of audience IDs
        audiences_filtered = am.get_all_audiences_and_deliveries(
            self.database,
            audience_ids=[
                audiences[0].get(db_c.ID),
                audiences[1].get(db_c.ID),
            ],
        )
        self.assertEqual(len(audiences_filtered), 2)

    def test_delete_audience(self):
        """Test delete an audience"""
        _ = self._setup_audience()

        all_audiences = am.get_all_audiences(self.database)

        self.assertTrue(
            am.delete_audience(
                self.database, ObjectId(all_audiences[0][db_c.ID])
            )
        )

        audiences = am.get_all_audiences(self.database)

        self.assertEqual(len(all_audiences) - 1, len(audiences))

    def test_append_destination_to_standalone_audience(self):
        """Test add destination to audience."""

        set_audience = am.create_audience(
            self.database,
            "My Audience",
            self.audience_filters,
            self.user_name,
        )
        mock.patch(
            "huxunifylib.database.delivery_platform_management"
            ".get_delivery_platforms_by_id",
            return_value=[
                {
                    db_c.DELIVERY_PLATFORM_NAME: db_c.DELIVERY_PLATFORM_FACEBOOK,
                    db_c.DELIVERY_PLATFORM_TYPE: db_c.DELIVERY_PLATFORM_FACEBOOK,
                    db_c.LINK: "https://business.facebook.com/",
                    db_c.CATEGORY: db_c.ADVERTISING,
                    db_c.STATUS: db_c.ACTIVE,
                    db_c.ENABLED: True,
                    db_c.ADDED: False,
                    db_c.IS_AD_PLATFORM: True,
                    db_c.ID: "60b9601a6021710aa146df2f",
                }
            ],
        ).start()
        destination = {
            "id": "60b9601a6021710aa146df2f",
            "delivery_platform_config": {
                "data_extension_name": "SFMC Test Audience"
            },
        }
        doc = am.append_destination_to_standalone_audience(
            database=self.database,
            audience_id=set_audience[db_c.ID],
            destination=destination,
            user_name=self.user_name,
        )

        self.assertIn(
            destination[db_c.OBJECT_ID],
            [x[db_c.ID] for x in doc[db_c.DESTINATIONS]],
        )
