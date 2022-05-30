"""Engagement Audience management tests."""

from datetime import datetime
import unittest
import mongomock
from bson import ObjectId

import huxunifylib.database.engagement_management as em
import huxunifylib.database.engagement_audience_management as eam
import huxunifylib.database.orchestration_management as om
import huxunifylib.database.delivery_platform_management as dpm
import huxunifylib.database.constants as db_c
from huxunifylib.database.client import DatabaseClient


class TestEngagementAudienceMgmt(unittest.TestCase):
    """Test engagement audience management module."""

    @mongomock.patch(servers=(("localhost", 27017),))
    def setUp(self):
        self.database = DatabaseClient(host="localhost", port=27017).connect()

        self.database.drop_database(db_c.DATA_MANAGEMENT_DATABASE)

        self.user_name = "joey galloway"

        self.destination = dpm.set_delivery_platform(
            self.database,
            db_c.DELIVERY_PLATFORM_FACEBOOK,
            "My delivery platform for Facebook",
            {
                "sample_access_token": "path1",
                "sample_app_secret": "path2",
                "sample_app_id": "path3",
                "sample_ad_account_id": "path4",
            },
        )

        # setup the delivery platform connection status
        dpm.set_connection_status(
            self.database,
            self.destination[db_c.ID],
            db_c.STATUS_SUCCEEDED,
        )

        self.audience_id = ObjectId()
        self.engagement_id = (
            self.database[db_c.DATA_MANAGEMENT_DATABASE][
                db_c.ENGAGEMENTS_COLLECTION
            ]
            .insert_one(
                {
                    "name": "arkells",
                    "description": "",
                    "create_time": datetime.utcnow(),
                    "created_by": "Douglas Long",
                    "updated_by": "",
                    "update_time": datetime.utcnow(),
                    "deleted": False,
                    "status": "Active",
                    "audiences": [
                        {
                            "id": self.audience_id,
                            "destinations": [
                                {"id": self.destination[db_c.ID]}
                            ],
                        }
                    ],
                }
            )
            .inserted_id
        )

    def test_set_destination_cron_expression(self):
        """Test setting the destination cron expression.

        Args:

        Returns:

        """

        # get the engagement first
        engagement = em.get_engagement(self.database, self.engagement_id)

        # test to ensure the field is not set
        self.assertNotIn(
            db_c.ENGAGEMENT_DELIVERY_SCHEDULE,
            engagement[db_c.AUDIENCES][0][db_c.DESTINATIONS][0],
        )

        # set the cron expression
        cron_expression = "15 23 ? * 1/2 *"
        eam.set_engagement_audience_destination_schedule(
            self.database,
            self.engagement_id,
            self.audience_id,
            self.destination[db_c.ID],
            cron_expression,
            "joe smith",
        )

        # grab the engagement again
        engagement = em.get_engagement(self.database, self.engagement_id)

        # test to ensure it was set
        self.assertIn(
            db_c.ENGAGEMENT_DELIVERY_SCHEDULE,
            engagement[db_c.AUDIENCES][0][db_c.DESTINATIONS][0],
        )
        self.assertEqual(
            cron_expression,
            engagement[db_c.AUDIENCES][0][db_c.DESTINATIONS][0][
                db_c.ENGAGEMENT_DELIVERY_SCHEDULE
            ],
        )

    def test_remove_destination_cron_expression(self):
        """Test removing the destination cron expression.

        Args:

        Returns:

        """

        # set the cron expression
        cron_expression = "15 23 ? * 1/2 *"
        eam.set_engagement_audience_destination_schedule(
            self.database,
            self.engagement_id,
            self.audience_id,
            self.destination[db_c.ID],
            cron_expression,
            "joe smith",
        )

        # grab the engagement again
        engagement = em.get_engagement(self.database, self.engagement_id)

        # test to ensure it was set
        self.assertEqual(
            cron_expression,
            engagement[db_c.AUDIENCES][0][db_c.DESTINATIONS][0][
                db_c.ENGAGEMENT_DELIVERY_SCHEDULE
            ],
        )

        # now remove it
        eam.set_engagement_audience_destination_schedule(
            self.database,
            self.engagement_id,
            self.audience_id,
            self.destination[db_c.ID],
            cron_expression,
            "joe smith",
            unset=True,
        )

        # grab the engagement again
        engagement = em.get_engagement(self.database, self.engagement_id)

        # test to ensure it was removed
        self.assertNotIn(
            db_c.ENGAGEMENT_DELIVERY_SCHEDULE,
            engagement[db_c.AUDIENCES][0][db_c.DESTINATIONS][0],
        )

    def test_set_engagement_audience_delivery_schedule(self):
        """Test setting the delivery schedule of an audience in an
        engagement."""
        # attach another audience to engagement
        engagement = em.append_audiences_to_engagement(
            database=self.database,
            engagement_id=self.engagement_id,
            user_name="Test User",
            audiences=[
                {
                    db_c.OBJECT_ID: ObjectId(),
                    db_c.DESTINATIONS: self.destination,
                }
            ],
        )

        # test to ensure the field is not set
        self.assertNotIn(
            db_c.ENGAGEMENT_DELIVERY_SCHEDULE,
            engagement[db_c.AUDIENCES][0],
        )
        self.assertNotIn(
            db_c.ENGAGEMENT_DELIVERY_SCHEDULE,
            engagement[db_c.AUDIENCES][1],
        )

        # set the delivery schedule into the first audience in the engagement
        delivery_schedule = {
            "schedule": {
                "periodicity": "Daily",
                "every": 1,
                "hour": 12,
                "minute": 15,
                "period": "AM",
            },
            "start_date": "2022-03-02T00:00:00.000Z",
            "end_date": "2022-04-02T00:00:00.000Z",
        }
        eam.set_engagement_audience_schedule(
            self.database,
            self.engagement_id,
            self.audience_id,
            delivery_schedule,
            "joe smith",
        )

        # grab the engagement again
        engagement = em.get_engagement(self.database, self.engagement_id)

        # test to ensure that delivery_schedule is set only against the first
        # audience in the engagement
        self.assertIn(
            db_c.ENGAGEMENT_DELIVERY_SCHEDULE,
            engagement[db_c.AUDIENCES][0],
        )
        self.assertNotIn(
            db_c.ENGAGEMENT_DELIVERY_SCHEDULE,
            engagement[db_c.AUDIENCES][1],
        )

    def test_remove_engagement_audience_delivery_schedule(self):
        """Test removing the delivery schedule of an audience in an
        engagement."""
        # attach another audience to engagement
        _ = em.append_audiences_to_engagement(
            database=self.database,
            engagement_id=self.engagement_id,
            user_name="Test User",
            audiences=[
                {
                    db_c.OBJECT_ID: ObjectId(),
                    db_c.DESTINATIONS: self.destination,
                }
            ],
        )

        # set the delivery schedule into the first audience in the engagement
        delivery_schedule = {
            "schedule": {
                "periodicity": "Daily",
                "every": 1,
                "hour": 12,
                "minute": 15,
                "period": "AM",
            },
            "start_date": "2022-03-02T00:00:00.000Z",
            "end_date": "2022-04-02T00:00:00.000Z",
        }

        eam.set_engagement_audience_schedule(
            self.database,
            self.engagement_id,
            self.audience_id,
            delivery_schedule,
            "joe smith",
        )

        # get the engagement first
        engagement = em.get_engagement(self.database, self.engagement_id)

        # test to ensure that delivery_schedule is set only against the first
        # audience in the engagement
        self.assertIn(
            db_c.ENGAGEMENT_DELIVERY_SCHEDULE,
            engagement[db_c.AUDIENCES][0],
        )
        self.assertNotIn(
            db_c.ENGAGEMENT_DELIVERY_SCHEDULE,
            engagement[db_c.AUDIENCES][1],
        )

        eam.set_engagement_audience_schedule(
            self.database,
            self.engagement_id,
            self.audience_id,
            delivery_schedule,
            "joe smith",
            unset=True,
        )

        # grab the engagement again
        engagement = em.get_engagement(self.database, self.engagement_id)

        # test to ensure the field is unset
        self.assertNotIn(
            db_c.ENGAGEMENT_DELIVERY_SCHEDULE,
            engagement[db_c.AUDIENCES][0],
        )
        self.assertNotIn(
            db_c.ENGAGEMENT_DELIVERY_SCHEDULE,
            engagement[db_c.AUDIENCES][1],
        )

    def generate_audience_delivery_jobs(self, index=0) -> dict:
        """A function to create an audience and delivery job.

        Args:
            index (DatabaseClient): A database client.

        Returns:
            dict:  An audience object.
        """

        audience = om.create_audience(
            self.database,
            f"My Test Audience-{index}",
            [],
            self.user_name,
            [{db_c.OBJECT_ID: self.destination[db_c.ID]}],
            100 + index,
        )

        audience.update({db_c.OBJECT_ID: audience[db_c.ID]})
        engagement_id = em.set_engagement(
            self.database,
            f"My Test Engagement-{index}",
            f"My Test Engagement Description-{index}",
            [audience],
            self.user_name,
        )

        # create delivery job
        dpm.set_delivery_job(
            database=self.database,
            audience_id=audience[db_c.ID],
            delivery_platform_id=self.destination[db_c.ID],
            delivery_platform_generic_campaigns=[],
            username=self.user_name,
            engagement_id=engagement_id,
        )

        return audience

    def test_get_all_engagement_audience_deliveries(self):
        """Test get all deliveries for engagement and audience pairs."""

        audiences = [
            self.generate_audience_delivery_jobs(i) for i in range(11)
        ]

        # get all audiences and deliveries
        audience_deliveries = eam.get_all_engagement_audience_deliveries(
            self.database, audience_ids=list(x.get(db_c.ID) for x in audiences)
        )
        self.assertTrue(audience_deliveries)
        self.assertGreater(len(audience_deliveries), 10)

        for audience_delivery in audience_deliveries.values():
            # test each audience_delivery
            self.assertIn(db_c.DELIVERIES, audience_delivery)
            self.assertIn(db_c.AUDIENCE_LAST_DELIVERED, audience_delivery)

            # test there are deliveries
            self.assertTrue(audience_delivery[db_c.DELIVERIES])

            for delivery in audience_delivery[db_c.DELIVERIES]:
                self.assertEqual(
                    delivery[db_c.DELIVERY_PLATFORM_TYPE],
                    self.destination[db_c.DELIVERY_PLATFORM_TYPE],
                )
                self.assertEqual(
                    delivery[db_c.METRICS_DELIVERY_PLATFORM_NAME],
                    self.destination[db_c.DELIVERY_PLATFORM_NAME],
                )
                self.assertIn(db_c.UPDATE_TIME, delivery)
                self.assertEqual(
                    delivery[db_c.STATUS], db_c.AUDIENCE_STATUS_DELIVERING
                )

    def test_get_all_audience_engagement_id_pairs(self):
        """Test get all get_all_audience_engagement_id_pairs."""

        audiences = [self.generate_audience_delivery_jobs(i) for i in range(4)]

        # get all audiences and deliveries
        audience_engagement_pairs = eam.get_all_audience_engagement_id_pairs(
            self.database, list(x.get(db_c.ID) for x in audiences)
        )

        self.assertTrue(audience_engagement_pairs)
        self.assertEqual(4, len(audience_engagement_pairs))

    def test_get_all_audience_engagement_latest_deliveries(self):
        """Test get all get_all_audience_engagement_latest_deliveries."""

        audiences = [self.generate_audience_delivery_jobs(i) for i in range(4)]

        # get all audiences and deliveries
        audience_engagement_pairs = eam.get_all_audience_engagement_id_pairs(
            self.database, list(x.get(db_c.ID) for x in audiences)
        )

        # get recent deliveries for each engagement pair.
        recent_deliveries = eam.get_all_audience_engagement_latest_deliveries(
            self.database, audience_engagement_pairs
        )

        self.assertTrue(recent_deliveries)
        self.assertEqual(4, len(recent_deliveries))

        for delivery in recent_deliveries:
            self.assertEqual(
                db_c.AUDIENCE_STATUS_DELIVERING, delivery.get(db_c.STATUS)
            )

    def test_align_audience_engagement_deliveries(self):
        """Test get all align_audience_engagement_deliveries."""

        audience_ids = [
            self.generate_audience_delivery_jobs(i)[db_c.ID] for i in range(4)
        ]

        # get all audiences and deliveries
        audience_engagement_pairs = eam.get_all_audience_engagement_id_pairs(
            self.database, audience_ids
        )
        self.assertTrue(audience_engagement_pairs)

        # get recent deliveries for each engagement pair.
        recent_deliveries = eam.get_all_audience_engagement_latest_deliveries(
            self.database, audience_engagement_pairs
        )
        self.assertTrue(audience_engagement_pairs)

        engagement_deliveries = eam.align_audience_engagement_deliveries(
            self.database, recent_deliveries, audience_ids
        )

        self.assertTrue(engagement_deliveries)
        self.assertEqual(4, len(engagement_deliveries))
        self.assertListEqual(audience_ids, list(engagement_deliveries.keys()))

    def test_set_replace_audience_flag_engaged_audience(self):
        """Test set_replace_audience flag_engaged_audience method"""
        engagement_doc = eam.set_replace_audience_flag_engaged_audience(
            database=self.database,
            engagement_id=self.engagement_id,
            audience_id=self.audience_id,
            destination_id=self.destination[db_c.ID],
            replace_audience=True,
            user_name="Test User",
        )
        for audience in engagement_doc[db_c.AUDIENCES]:
            for destination in audience[db_c.DESTINATIONS]:
                if (
                    destination[db_c.OBJECT_ID] == self.destination[db_c.ID]
                    and audience[db_c.OBJECT_ID] == self.audience_id
                ):
                    self.assertTrue(destination[db_c.REPLACE_AUDIENCE])
