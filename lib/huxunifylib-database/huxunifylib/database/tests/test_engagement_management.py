"""Engagement Management Tests"""

import unittest
import mongomock
from bson import ObjectId
import huxunifylib.database.engagement_management as em
import huxunifylib.database.constants as c
from huxunifylib.database.client import DatabaseClient
from huxunifylib.database import orchestration_management as om
from huxunifylib.database import audience_management as am
from huxunifylib.database import data_management as dm
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

        self.audience[c.OBJECT_ID] = self.audience[c.ID]

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

    def test_set_engagement_string_audience_id(self) -> None:
        """Test set_engagement routine with string audience id

        Returns:
            Response: None

        """

        # change audience_id to string
        audience = self.audience.copy()
        audience[c.OBJECT_ID] = str(audience[c.OBJECT_ID])

        with self.assertRaises(ValueError):
            em.set_engagement(
                self.database,
                "Engagement string audience",
                "string audience",
                [audience],
                self.user_id,
            )

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
        self.assertNotIn(c.ENGAGEMENT_DELIVERY_SCHEDULE, engagement_doc)
        self.assertEqual(self.user_id, engagement_doc[c.CREATED_BY])

    def test_update_engagement_bad_string_id(self) -> None:
        """Test update_engagement routine with a bad string id

        Returns:
            Response: None

        """

        new_name = "Engagement 3"
        new_description = "Engagement 3 description"
        engagement_docs = em.get_engagements(database=self.database)
        engagement_id = engagement_docs[0]["_id"]

        self.assertIsInstance(engagement_id, ObjectId)

        # change audience_id to string
        audience = self.audience.copy()
        audience[c.OBJECT_ID] = str(audience[c.OBJECT_ID])

        with self.assertRaises(ValueError):
            em.update_engagement(
                self.database,
                engagement_id,
                self.user_id,
                new_name,
                new_description,
                [audience],
            )

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
            [self.audience],
            self.user_id,
        )

        self.assertIsInstance(engagement_id, ObjectId)

        # delete created engagement
        delete_flag = em.delete_engagement(self.database, engagement_id)

        self.assertTrue(delete_flag)

        # validate the engagement was deleted
        engagement_doc = em.get_engagement(self.database, engagement_id)
        self.assertIsNone(engagement_doc)

    def test_create_and_get_engagement_with_many_audiences(self) -> None:
        """Test creating an engagement with many audiences

        Returns:
            Response: None

        """

        # create an engagement that has
        # an audience with three destinations
        # an audience with two destinations
        new_engagement = {
            c.ENGAGEMENT_NAME: "Spring 2024",
            c.ENGAGEMENT_DESCRIPTION: "high ltv for spring 2024",
            c.AUDIENCES: [
                {
                    c.OBJECT_ID: ObjectId(),
                    c.DESTINATIONS: [
                        {
                            c.OBJECT_ID: ObjectId(),
                            c.DELIVERY_PLATFORM_CONTACT_LIST: "random_extension",
                        },
                        {c.OBJECT_ID: ObjectId()},
                        {c.OBJECT_ID: ObjectId()},
                    ],
                },
                {
                    c.OBJECT_ID: ObjectId(),
                    c.DESTINATIONS: [{c.OBJECT_ID: ObjectId()}],
                },
            ],
        }

        engagement_id = em.set_engagement(
            self.database,
            new_engagement[c.ENGAGEMENT_NAME],
            new_engagement[c.ENGAGEMENT_DESCRIPTION],
            new_engagement[c.AUDIENCES],
            self.user_id,
        )

        # validate it was created
        self.assertIsInstance(engagement_id, ObjectId)

        # get the created engagement to check values
        engagement = em.get_engagement(self.database, engagement_id)

        self.assertIsNotNone(engagement)

        # test audiences
        self.assertIn(c.AUDIENCES, engagement)
        self.assertEqual(len(engagement[c.AUDIENCES]), 2)
        self.assertListEqual(
            engagement[c.AUDIENCES], new_engagement[c.AUDIENCES]
        )

    def test_set_engagement_remove_audience_after(self) -> None:
        """Test creating an engagement and remove an audience after

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

        engagement = em.get_engagement(self.database, engagement_id)

        # check engagement
        self.assertIn(c.AUDIENCES, engagement)
        self.assertEqual(len(engagement[c.AUDIENCES]), 1)
        self.assertEqual(
            engagement[c.AUDIENCES][0][c.OBJECT_ID],
            self.audience[c.OBJECT_ID],
        )
        self.assertIsInstance(engagement_id, ObjectId)

        # remove an audience
        result = em.remove_audiences_from_engagement(
            self.database,
            engagement_id,
            self.user_id,
            [self.audience[c.OBJECT_ID]],
        )
        self.assertTrue(result)

        # ensure the audience was removed
        updated = em.get_engagement(self.database, engagement_id)
        self.assertIn(c.AUDIENCES, updated)

        # test audience should not be there
        self.assertFalse(updated[c.AUDIENCES])

    def test_set_engagement_remove_audience_str_audience(self) -> None:
        """Test creating an engagement and remove a string audience id

        Returns:
            Response: None

        """

        # create audience normally
        engagement_id = em.set_engagement(
            self.database,
            "Engagement 2",
            "Engagement 2 Description",
            [self.audience],
            self.user_id,
        )

        engagement = em.get_engagement(self.database, engagement_id)

        # check engagement
        self.assertIn(c.AUDIENCES, engagement)
        self.assertEqual(len(engagement[c.AUDIENCES]), 1)
        self.assertEqual(
            engagement[c.AUDIENCES][0][c.OBJECT_ID],
            self.audience[c.OBJECT_ID],
        )
        self.assertIsInstance(engagement_id, ObjectId)

        with self.assertRaises(ValueError):
            # remove an audience
            em.remove_audiences_from_engagement(
                self.database,
                engagement_id,
                self.user_id,
                [str(self.audience[c.OBJECT_ID])],
            )

    def test_set_engagement_attach_audience_after(self) -> None:
        """Test creating an engagement and attaching an audience after

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

        engagement = em.get_engagement(self.database, engagement_id)

        # check engagement
        self.assertIn(c.AUDIENCES, engagement)
        self.assertEqual(len(engagement[c.AUDIENCES]), 1)
        self.assertEqual(
            engagement[c.AUDIENCES][0][c.OBJECT_ID],
            self.audience[c.OBJECT_ID],
        )
        self.assertIsInstance(engagement_id, ObjectId)

        # setup a few destinations
        new_audience = {
            c.OBJECT_ID: ObjectId(),
            c.DESTINATIONS: self.destinations,
        }

        result = em.append_audiences_to_engagement(
            self.database, engagement_id, self.user_id, [new_audience]
        )
        self.assertTrue(result)

        # ensure the audience was updated
        updated = em.get_engagement(self.database, engagement_id)
        self.assertIn(c.AUDIENCES, updated)

        # test audience appears as expected
        self.assertTrue(updated[c.AUDIENCES])
        self.assertEqual(len(updated[c.AUDIENCES]), 2)

    def test_set_engagement_attach_audience_str_id(self) -> None:
        """Test creating an engagement and attaching an audience
            with a str object id

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

        engagement = em.get_engagement(self.database, engagement_id)

        # check engagement
        self.assertIn(c.AUDIENCES, engagement)
        self.assertEqual(len(engagement[c.AUDIENCES]), 1)
        self.assertEqual(
            engagement[c.AUDIENCES][0][c.OBJECT_ID],
            self.audience[c.OBJECT_ID],
        )
        self.assertIsInstance(engagement_id, ObjectId)

        # setup a few destinations
        new_audience = {
            c.OBJECT_ID: str(ObjectId()),
            c.DESTINATIONS: self.destinations,
        }

        with self.assertRaises(ValueError):
            em.append_audiences_to_engagement(
                self.database, engagement_id, self.user_id, [new_audience]
            )

    def test_set_engagement_attach_lookalike_audience(self):
        """Test creating an engagement and attaching a lookalike audience after

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

        # create an ingestion job
        data_source_id = ObjectId()
        ingestion_job = dm.set_ingestion_job(self.database, data_source_id)
        ingestion_job_id = ingestion_job[c.ID]

        # create a delivery platform
        delivery_platform = dpm.set_delivery_platform(
            self.database,
            "Facebook",
            "Facebook Delivery Platform",
            authentication_details={},
        )
        delivery_platform_id = delivery_platform[c.ID]

        # create a source audience
        source_audience = am.create_audience(
            self.database, "Source Audience", [], ingestion_job_id
        )
        source_audience_id = source_audience[c.ID]

        # create a lookalike audience
        lookalike_audience = dpm.create_delivery_platform_lookalike_audience(
            self.database,
            delivery_platform_id,
            source_audience_id,
            "LA Audience",
            0.55,
        )

        engagement = em.get_engagement(self.database, engagement_id)

        # check engagement
        self.assertIn(c.AUDIENCES, engagement)
        self.assertEqual(len(engagement[c.AUDIENCES]), 1)
        self.assertEqual(
            engagement[c.AUDIENCES][0][c.OBJECT_ID],
            self.audience[c.OBJECT_ID],
        )
        self.assertIsInstance(engagement_id, ObjectId)

        new_lookalike_audience = {
            c.OBJECT_ID: lookalike_audience[c.ID],
            c.LOOKALIKE_SOURCE_AUD_ID: source_audience_id,
            c.LOOKALIKE_AUD_NAME: lookalike_audience[c.NAME],
        }

        # attach the lookalike audience
        result = em.append_audiences_to_engagement(
            self.database,
            engagement_id,
            self.user_id,
            [new_lookalike_audience],
        )
        self.assertTrue(result)

        # ensure the audience was updated
        updated = em.get_engagement(self.database, engagement_id)
        self.assertIn(c.AUDIENCES, updated)

        # test audience appears as expected
        self.assertTrue(updated[c.AUDIENCES])
        self.assertEqual(len(updated[c.AUDIENCES]), 2)

    def test_get_engagements_via_audience_id(self) -> None:
        """Test getting engagements with an audience_id

        Returns:
            Response: None

        """

        engagements = []
        for item in range(2):
            # create audience normally
            engagement_id = em.set_engagement(
                self.database,
                f"Engagement {item}",
                f"Engagement {item} Description",
                [self.audience],
                self.user_id,
            )

            engagement = em.get_engagement(self.database, engagement_id)

            # check engagement
            self.assertIn(c.AUDIENCES, engagement)
            self.assertEqual(len(engagement[c.AUDIENCES]), 1)
            self.assertEqual(
                engagement[c.AUDIENCES][0][c.OBJECT_ID],
                self.audience[c.ID],
            )
            self.assertIsInstance(engagement_id, ObjectId)

            engagements.append(engagement)

        # find all three.
        engagements = em.get_engagements_by_audience(
            self.database, self.audience[c.ID]
        )
        self.assertTrue(engagements)
        self.assertEqual(len(engagements), 3)
