"""Engagement Management Tests"""

import unittest
import mongomock
import datetime
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

        self.assertTrue(engagement_doc is not None)

    def test_get_engagements(self) -> None:
        """Test get_all_engagements routine

        Returns:
            Response: None

        """

        engagement_docs = em.get_all_engagements(database=self.database)

        self.assertTrue(engagement_docs is not None)

    def test_get_engagement_by_id(self) -> None:
        """Test get_all_engagements routine

        Returns:
            Response: None

        """

        engagement_docs = em.get_all_engagements(database=self.database)
        engagement_id = engagement_docs[0]["_id"]

        engagement_doc = em.get_engagement_by_id(
            database=self.database, engagement_id=engagement_id
        )

        self.assertTrue(engagement_doc is not None)

    def test_update_engagement(self) -> None:
        """Test update_engagement routine

        Returns:
            Response: None

        """

        new_name = "Engagement 3"
        engagement_docs = em.get_all_engagements(database=self.database)
        engagement_id = engagement_docs[0]["_id"]
        engagement_doc = em.update_engagement(
            database=self.database, engagement_id=engagement_id, name=new_name
        )

        self.assertTrue(engagement_doc[c.ENGAGEMENT_NAME] == new_name)

    def test_delete_engagement(self) -> None:
        """Test delete_engagement routine

        Returns:
            Response: None

        """

        engagement_docs = em.get_all_engagements(database=self.database)
        engagement_id = engagement_docs[0]["_id"]

        delete_flag = em.delete_engagement(
            database=self.database, engagement_id=engagement_id
        )

        self.assertTrue(delete_flag)
