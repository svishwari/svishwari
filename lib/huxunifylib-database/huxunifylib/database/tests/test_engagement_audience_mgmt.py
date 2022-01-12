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
        self.database = DatabaseClient(
            "localhost", 27017, None, None
        ).connect()

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

    def test_set_destination_cron_expression(self):
        """Test setting the destination cron expression.

        Args:

        Returns:

        """
        # manually create the engagement
        audience_id = ObjectId()
        destination_id = ObjectId()
        engagement_id = (
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
                            "id": audience_id,
                            "destinations": [
                                {
                                    "id": destination_id,
                                }
                            ],
                        }
                    ],
                }
            )
            .inserted_id
        )

        # get the engagement first
        engagement = em.get_engagement(self.database, engagement_id)

        # test to ensure the field is not set
        self.assertNotIn(
            db_c.ENGAGEMENT_DELIVERY_SCHEDULE,
            engagement[db_c.AUDIENCES][0][db_c.DESTINATIONS][0],
        )

        # set the cron expression
        cron_expression = "15 23 ? * 1/2 *"
        eam.set_engagement_audience_destination_schedule(
            self.database,
            engagement_id,
            audience_id,
            destination_id,
            cron_expression,
            "joe smith",
        )

        # grab the engagement again
        engagement = em.get_engagement(self.database, engagement_id)

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
        # manually create the engagement
        audience_id = ObjectId()
        destination_id = ObjectId()
        engagement_id = (
            self.database[db_c.DATA_MANAGEMENT_DATABASE][
                db_c.ENGAGEMENTS_COLLECTION
            ]
            .insert_one(
                {
                    "name": "arkells 2",
                    "description": "",
                    "create_time": datetime.utcnow(),
                    "created_by": "Douglas Long",
                    "updated_by": "",
                    "update_time": datetime.utcnow(),
                    "deleted": False,
                    "status": "Active",
                    "audiences": [
                        {
                            "id": audience_id,
                            "destinations": [
                                {
                                    "id": destination_id,
                                }
                            ],
                        }
                    ],
                }
            )
            .inserted_id
        )

        # set the cron expression
        cron_expression = "15 23 ? * 1/2 *"
        eam.set_engagement_audience_destination_schedule(
            self.database,
            engagement_id,
            audience_id,
            destination_id,
            cron_expression,
            "joe smith",
        )

        # grab the engagement again
        engagement = em.get_engagement(self.database, engagement_id)

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
            engagement_id,
            audience_id,
            destination_id,
            cron_expression,
            "joe smith",
            unset=True,
        )

        # grab the engagement again
        engagement = em.get_engagement(self.database, engagement_id)

        # test to ensure it was removed
        self.assertNotIn(
            db_c.ENGAGEMENT_DELIVERY_SCHEDULE,
            engagement[db_c.AUDIENCES][0][db_c.DESTINATIONS][0],
        )

    def test_get_all_engagement_audience_deliveries(self):
        """Test get all deliveries for engagement and audience pairs."""

        audiences = []
        for i in range(11):
            audience = om.create_audience(
                self.database,
                f"My Test Audience-{i}",
                [],
                self.user_name,
                [{db_c.OBJECT_ID: self.destination[db_c.ID]}],
                100 + i,
            )
            audiences.append(audience)

            audience.update({db_c.OBJECT_ID: audience[db_c.ID]})
            engagement_id = em.set_engagement(
                self.database,
                f"My Test Engagement-{i}",
                f"My Test Engagement Description-{i}",
                [audience],
                self.user_name,
            )

            # create delivery job
            dpm.set_delivery_job(
                self.database,
                audience[db_c.ID],
                self.destination[db_c.ID],
                [],
                engagement_id,
            )

        # get all audiences and deliveries
        audience_deliveries = eam.get_all_engagement_audience_deliveries(
            self.database, audience_ids=list(x.get(db_c.ID) for x in audiences)
        )
        self.assertTrue(audience_deliveries)
        self.assertGreater(len(audience_deliveries), 10)

        for audience_delivery in audience_deliveries:
            # test each audience_delivery
            self.assertIn(db_c.DELIVERIES, audience_delivery)
            self.assertIn(db_c.AUDIENCE_LAST_DELIVERED, audience_delivery)
            self.assertIn(db_c.AUDIENCE_ID, audience_delivery)

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
