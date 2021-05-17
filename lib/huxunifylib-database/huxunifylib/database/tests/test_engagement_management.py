"""Engagement Management Tests"""

import unittest
import datetime
import mongomock
from bson import ObjectId
import huxunifylib.database.engagement_management as em
import huxunifylib.database.constants as c
from huxunifylib.database.client import DatabaseClient


# pylint: disable=R0904
class TestEngagementManagement(unittest.TestCase):
    """Test engagement management module."""

    @mongomock.patch(servers=(("localhost", 27017),))
    def setUp(self) -> None:

        self.database = DatabaseClient(
            "localhost", 27017, None, None
        ).connect()
        self.database.drop_database(c.DATA_MANAGEMENT_DATABASE)

        self.sample_engagement = {
            c.ENGAGEMENT_NAME: "Engagement 1",
            c.ENGAGEMENT_DESCRIPTION: "Engagement 1 Description",
            c.AUDIENCES: [],
            c.ENGAGEMENT_DELIVERY_SCHEDULE: {},
            c.CREATE_TIME: datetime.datetime.utcnow(),
            c.CREATED_BY: ObjectId(),
            c.ENABLED: True,
        }

        self.engagement_doc = em.set_engagement(
            database=self.database,
            name=self.sample_engagement[c.ENGAGEMENT_NAME],
            description=self.sample_engagement[c.ENGAGEMENT_DESCRIPTION],
            audiences=self.sample_engagement[c.ENGAGEMENT_AUDIENCES],
            delivery_schedule=self.sample_engagement[
                c.ENGAGEMENT_DELIVERY_SCHEDULE
            ],
        )

    def test_set_engagement(self) -> None:
        """Test set_engagement routine

        Returns:
            Response: None

        """

        engagement_doc = em.set_engagement(
            database=self.database,
            name="Engagement 2",
            description="Engagement 2 Description",
            audiences=[],
            delivery_schedule={},
        )

        self.assertIsNotNone(engagement_doc)

    def test_get_engagements(self) -> None:
        """Test get_engagements routine

        Returns:
            Response: None

        """

        engagement_docs = em.get_engagements(database=self.database)

        self.assertIsNotNone(engagement_docs)

    def test_get_engagement(self) -> None:
        """Test get_engagement routine

        Returns:
            Response: None

        """

        engagement_docs = em.get_engagements(database=self.database)
        engagement_id = engagement_docs[0]["_id"]

        self.assertIsInstance(engagement_id, ObjectId)

        engagement_doc = em.get_engagement(
            database=self.database, engagement_id=engagement_id
        )

        self.assertIsNotNone(engagement_doc)

    def test_update_engagement(self) -> None:
        """Test update_engagement routine

        Returns:
            Response: None

        """

        new_name = "Engagement 3"
        new_description = "Engagement 3 description"
        engagement_docs = em.get_engagements(database=self.database)
        engagement_id = engagement_docs[0]["_id"]

        self.assertIsInstance(engagement_id, ObjectId)

        engagement_doc = em.update_engagement(
            database=self.database,
            engagement_id=engagement_id,
            name=new_name,
            description=new_description,
        )

        self.assertEqual(engagement_doc[c.ENGAGEMENT_NAME], new_name)
        self.assertEqual(
            engagement_doc[c.ENGAGEMENT_DESCRIPTION], new_description
        )
        self.assertEqual(engagement_doc[c.ENGAGEMENT_AUDIENCES], [])
        self.assertEqual(engagement_doc[c.ENGAGEMENT_DELIVERY_SCHEDULE], {})

    def test_disable_engagement(self) -> None:
        """Test delete_engagement routine

        Returns:
            Response: None

        """

        engagement_docs = em.get_engagements(database=self.database)
        engagement_id = engagement_docs[0]["_id"]

        self.assertIsInstance(engagement_id, ObjectId)

        delete_flag = em.disable_engagement(
            database=self.database, engagement_id=engagement_id
        )

        self.assertTrue(delete_flag)
