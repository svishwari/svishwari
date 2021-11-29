"""Engagement Audience management tests."""

from datetime import datetime
import unittest
import mongomock
from bson import ObjectId

import huxunifylib.database.engagement_management as em
import huxunifylib.database.engagement_audience_management as eam
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
