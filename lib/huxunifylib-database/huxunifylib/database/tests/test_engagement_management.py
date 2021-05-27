"""Engagement Management Tests"""

import unittest
import mongomock
from bson import ObjectId
import huxunifylib.database.engagement_management as em
import huxunifylib.database.constants as c
from huxunifylib.database.client import DatabaseClient
from huxunifylib.database import orchestration_management as om
from huxunifylib.database import delivery_platform_management as dpm


class TestEngagementManagement(unittest.TestCase):
    """Test engagement management module."""

    @mongomock.patch(servers=(("localhost", 27017),))
    def setUp(self) -> None:

        self.database = DatabaseClient(
            "localhost", 27017, None, None
        ).connect()
        self.database.drop_database(c.DATA_MANAGEMENT_DATABASE)

        self.user_id = ObjectId()

        # setup the audience
        self.audience = om.create_audience(
            self.database, "all", [], self.user_id
        )

        self.audience[c.AUDIENCE_ID] = self.audience[c.ID]

        self.engagement_id = em.set_engagement(
            self.database,
            "Spring 2021",
            "spring of 2021",
            [self.audience],
            self.user_id,
        )

        # setup a few destinations
        self.destinations = []
        for destination in [
            c.DELIVERY_PLATFORM_FACEBOOK,
            c.DELIVERY_PLATFORM_AMAZON,
        ]:
            self.destinations.append(
                dpm.set_delivery_platform(
                    self.database,
                    destination,
                    destination,
                    user_id=self.user_id,
                )
            )

    def test_set_engagement(self) -> None:
        """Test set_engagement routine

        Returns:
            Response: None

        """

        engagement_id = em.set_engagement(
            self.database,
            "Engagement 2",
            "Engagement 2 Description",
            [self.audience],
            self.user_id,
        )

        self.assertIsInstance(engagement_id, ObjectId)

    def test_get_engagements(self) -> None:
        """Test get_engagements routine

        Returns:
            Response: None

        """

        # test for a list with data.
        self.assertTrue(em.get_engagements(database=self.database))

    def test_get_engagement(self) -> None:
        """Test get_engagement routine

        Returns:
            Response: None

        """

        # take the first document
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
            self.database,
            engagement_id,
            self.user_id,
            new_name,
            new_description,
        )

        self.assertEqual(engagement_doc[c.ENGAGEMENT_NAME], new_name)
        self.assertEqual(
            engagement_doc[c.ENGAGEMENT_DESCRIPTION], new_description
        )
        self.assertIn(c.ENGAGEMENT_DELIVERY_SCHEDULE, engagement_doc)
        self.assertEqual(self.user_id, engagement_doc[c.CREATED_BY])

    def test_delete_engagement(self) -> None:
        """Test delete_engagement routine

        Returns:
            Response: None

        """

        # create engagement
        engagement_id = em.set_engagement(
            self.database,
            "Fall 2024",
            "fall of 2024",
            [self.audience[c.ID]],
            self.user_id,
        )

        self.assertIsInstance(engagement_id, ObjectId)

        # delete created engagement
        delete_flag = em.delete_engagement(self.database, engagement_id)

        self.assertTrue(delete_flag)

    # def test_create_engagement_audience(self) -> None:
    #     """Test create engagement audience
    #
    #     Returns:
    #         Response: None
    #
    #     """
    #
    #     # define expected doc
    #     expected = {
    #         c.ENGAGEMENT_ID: self.engagement_id,
    #         c.AUDIENCE_ID: self.audience[c.ID],
    #         c.DESTINATIONS: [x[c.ID] for x in self.destinations],
    #         c.ENABLED: True,
    #         c.DELIVERIES: [],
    #     }
    #
    #     # create the engagement audience
    #     new_doc = em.create_engagement_audience(
    #         self.database,
    #         self.audience[c.ID],
    #         self.engagement_id,
    #         expected[c.DESTINATIONS],
    #     )
    #
    #     # check if anything created
    #     self.assertTrue(new_doc)
    #
    #     # validate the docs
    #     del new_doc[c.ID]
    #
    #     self.assertDictEqual(new_doc, expected)
    #
    # def test_create_engagement_audience_invalid_engagement(self) -> None:
    #     """Test create engagement audience with an invalid engagement
    #
    #     Returns:
    #         Response: None
    #
    #     """
    #
    #     # define expected doc
    #     fake_engagement_id = ObjectId()
    #
    #     # create the engagement audience
    #     msg = f"Engagement does not exist {fake_engagement_id}."
    #     with self.assertRaises(Exception) as context:
    #         em.create_engagement_audience(
    #             self.database,
    #             self.audience[c.ID],
    #             fake_engagement_id,
    #             [x[c.ID] for x in self.destinations],
    #         )
    #     self.assertEqual(str(context.exception), msg)
    #
    # def test_create_engagement_audience_invalid_audience(self) -> None:
    #     """Test create engagement audience with an invalid audience
    #
    #     Returns:
    #         Response: None
    #
    #     """
    #
    #     fake_audience_id = ObjectId()
    #
    #     # create the engagement audience
    #     msg = f"Audience does not exist {fake_audience_id}."
    #     with self.assertRaises(Exception) as context:
    #         em.create_engagement_audience(
    #             self.database,
    #             fake_audience_id,
    #             self.engagement_id,
    #             [x[c.ID] for x in self.destinations],
    #         )
    #     self.assertEqual(str(context.exception), msg)
    #
    # def test_create_engagement_audience_invalid_destination(self) -> None:
    #     """Test create engagement audience with an invalid destination
    #
    #     Returns:
    #         Response: None
    #
    #     """
    #
    #     fake_destination_id = ObjectId()
    #     destinations = [x[c.ID] for x in self.destinations]
    #
    #     # create the engagement audience
    #     msg = f"Destination does not exist {fake_destination_id}."
    #     with self.assertRaises(Exception) as context:
    #         em.create_engagement_audience(
    #             self.database,
    #             self.audience[c.ID],
    #             self.engagement_id,
    #             destinations + [fake_destination_id],
    #         )
    #     self.assertEqual(str(context.exception), msg)
    #
    # def test_create_engagement_audience_duplicate(self) -> None:
    #     """Test create engagement audience duplicate.
    #
    #     Returns:
    #         Response: None
    #
    #     """
    #
    #     # create initial engagement
    #     engagement = em.create_engagement_audience(
    #         self.database,
    #         self.audience[c.ID],
    #         self.engagement_id,
    #         [x[c.ID] for x in self.destinations],
    #     )
    #
    #     self.assertIsNotNone(engagement)
    #
    #     # create the engagement audience, duplicate exception expected
    #     msg = f"Engagement Audience Exists {engagement[c.ID]}."
    #     with self.assertRaises(Exception) as context:
    #         em.create_engagement_audience(
    #             self.database,
    #             self.audience[c.ID],
    #             self.engagement_id,
    #             [x[c.ID] for x in self.destinations],
    #         )
    #     self.assertEqual(str(context.exception), msg)
    #
    # def test_get_engagement_audience(self) -> None:
    #     """Test get engagement audience
    #
    #     Returns:
    #         Response: None
    #
    #     """
    #
    #     # define expected doc
    #     expected = {
    #         c.ENGAGEMENT_ID: self.engagement_id,
    #         c.AUDIENCE_ID: self.audience[c.ID],
    #         c.DESTINATIONS: [x[c.ID] for x in self.destinations],
    #     }
    #
    #     # create the engagement audience
    #     new_doc = em.create_engagement_audience(
    #         self.database,
    #         self.audience[c.ID],
    #         self.engagement_id,
    #         expected[c.DESTINATIONS],
    #     )
    #
    #     # check if anything created
    #     self.assertTrue(new_doc)
    #
    #     audiences = em.get_engagement_audiences(self.database, [new_doc[c.ID]])
    #     self.assertTrue(audiences)
    #
    # def test_attach_deliveries_to_engagement_audience(self) -> None:
    #     """Test attaching deliveries to an engagement audience
    #
    #     Returns:
    #         Response: None
    #
    #     """
    #
    #     # define expected doc
    #     expected = {
    #         c.ENGAGEMENT_ID: self.engagement_id,
    #         c.AUDIENCE_ID: self.audience[c.ID],
    #         c.DESTINATIONS: [x[c.ID] for x in self.destinations],
    #     }
    #
    #     # create the engagement audience
    #     new_doc = em.create_engagement_audience(
    #         self.database,
    #         self.audience[c.ID],
    #         self.engagement_id,
    #         expected[c.DESTINATIONS],
    #     )
    #
    #     # check if anything created
    #     self.assertTrue(new_doc)
    #
    #     # test attaching deliveries
    #     deliveries = [ObjectId() for x in range(5)]
    #     updated_doc = em.add_deliveries_to_engagement_audience(
    #         self.database, new_doc[c.ID], deliveries
    #     )
    #
    #     # validate the results.
    #     self.assertIsNotNone(updated_doc)
    #     self.assertIn(c.DELIVERIES, updated_doc)
    #     self.assertListEqual(
    #         expected[c.DESTINATIONS], updated_doc[c.DESTINATIONS]
    #     )
    #
    # def test_get_engagements_with_engaged_audiences(self) -> None:
    #     """Test get engagements with engaged audiences
    #
    #     Returns:
    #         Response: None
    #
    #     """
    #
    #     # define expected doc
    #     destinations = [x[c.ID] for x in self.destinations]
    #
    #     # create the engagements
    #     engagement_ids = []
    #     for i in range(5):
    #         engagement_ids.append(
    #             em.set_engagement(
    #                 self.database,
    #                 f"Fall 202{i}",
    #                 f"description for {i}",
    #                 self.user_id,
    #             )
    #         )
    #
    #     # ensure engagements were created
    #     self.assertTrue(engagement_ids)
    #     self.assertEqual(len(engagement_ids), 5)
    #
    #     # create audiences
    #     audiences = []
    #     for i in range(5):
    #         audiences.append(
    #             om.create_audience(
    #                 self.database, f"description {i}", [], self.user_id
    #             )
    #         )
    #
    #     # ensure audiences were created
    #     self.assertTrue(audiences)
    #     self.assertEqual(len(audiences), 5)
    #
    #     # create the engagement audiences
    #     engagement_audience_ids = []
    #     for audience, engagement_id in zip(audiences, engagement_ids):
    #         new_doc = em.create_engagement_audience(
    #             self.database,
    #             audience[c.ID],
    #             engagement_id,
    #             destinations,
    #         )
    #
    #         # test document was created.
    #         self.assertTrue(new_doc)
    #
    #         engagement_audience_ids.append(new_doc[c.ID])
    #
    #         # attach deliveries
    #         deliveries = [ObjectId() for x in range(5)]
    #         updated_doc = em.add_deliveries_to_engagement_audience(
    #             self.database, new_doc[c.ID], deliveries
    #         )
    #
    #         # validate the results.
    #         self.assertIsNotNone(updated_doc)
    #         self.assertIn(c.DELIVERIES, updated_doc)
    #         self.assertListEqual(deliveries, updated_doc[c.DELIVERIES])
    #
    #     # now test engagements
    #     engagements = em.get_engagements(self.database)
    #
    #     self.assertTrue(engagements)
    #     self.assertEqual(len(engagements), 6)
    #     found_engaged_audiences = []
    #     for i, engagement in enumerate(engagements):
    #         if not engagement[c.ID] in engagement_ids:
    #             continue
    #
    #         # validate engagement_audiences is in the result.
    #         self.assertIn(c.ENGAGEMENT_AUDIENCES_COLLECTION, engagement)
    #
    #         engagement_audience = engagement[
    #             c.ENGAGEMENT_AUDIENCES_COLLECTION
    #         ][0]
    #
    #         self.assertIn(c.DELIVERIES, engagement_audience)
    #         self.assertIn(c.DESTINATIONS, engagement_audience)
    #
    #         # validate the length of the engagement_audiences
    #         self.assertEqual(len(engagement_audience[c.DESTINATIONS]), 2)
    #         self.assertEqual(len(engagement_audience[c.DELIVERIES]), 5)
    #
    #         found_engaged_audiences.append(engagement_audience[c.ID])
    #
    #     self.assertTrue(found_engaged_audiences)
    #     self.assertListEqual(found_engaged_audiences, engagement_audience_ids)
