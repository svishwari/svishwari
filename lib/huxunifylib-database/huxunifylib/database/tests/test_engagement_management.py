"""Engagement Management Tests"""
# pylint: disable=too-many-lines
import unittest
import mongomock
import pymongo
from bson import ObjectId
import huxunifylib.database.engagement_management as em
import huxunifylib.database.constants as c
from huxunifylib.database.client import DatabaseClient
from huxunifylib.database import (
    audience_management as am,
    data_management as dm,
    delivery_platform_management as dpm,
    orchestration_management as om,
    engagement_audience_management as eam,
)

# pylint: disable=R0904
class TestEngagementManagement(unittest.TestCase):
    """Test engagement management module."""

    @mongomock.patch(servers=(("localhost", 27017),))
    def setUp(self) -> None:

        self.database = DatabaseClient(
            "localhost", 27017, None, None
        ).connect()
        self.database.drop_database(c.DATA_MANAGEMENT_DATABASE)

        # write a user to the database
        self.user_name = "joey galloway"

        # setup the audience
        self.audience = om.create_audience(
            self.database, "all", [], [], self.user_name, 184
        )

        self.audience[c.OBJECT_ID] = self.audience[c.ID]

        self.engagement_id = em.set_engagement(
            self.database,
            "Spring 2021",
            "spring of 2021",
            [{c.OBJECT_ID: self.audience[c.ID], c.DESTINATIONS: []}],
            self.user_name,
        )

        # setup a few destinations
        self.destinations = []
        for destination in [
            c.DELIVERY_PLATFORM_FACEBOOK,
            c.DELIVERY_PLATFORM_AMAZON,
        ]:
            destination = dpm.set_delivery_platform(
                self.database,
                destination,
                destination,
                user_name=self.user_name,
            )
            dpm.set_connection_status(
                self.database,
                destination[c.ID],
                c.STATUS_SUCCEEDED,
            )

            self.destinations.append(
                dpm.get_delivery_platform(self.database, destination[c.ID])
            )

        self.destination = dpm.set_delivery_platform(
            self.database,
            c.DELIVERY_PLATFORM_FACEBOOK,
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
            self.destination[c.ID],
            c.STATUS_SUCCEEDED,
        )

    def test_set_engagement(self) -> None:
        """Test set_engagement routine"""

        engagement_id = em.set_engagement(
            self.database,
            "Engagement 2",
            "Engagement 2 Description",
            [self.audience],
            self.user_name,
        )

        self.assertIsInstance(engagement_id, ObjectId)

    def test_set_engagement_string_audience_id(self) -> None:
        """Test set_engagement routine with string audience id"""

        # change audience_id to string
        audience = self.audience.copy()
        audience[c.OBJECT_ID] = str(audience[c.OBJECT_ID])

        with self.assertRaises(ValueError):
            em.set_engagement(
                self.database,
                "Engagement string audience",
                "string audience",
                [audience],
                self.user_name,
            )

    def test_get_engagements(self) -> None:
        """Test get_engagements routine"""

        # test for a list with data.
        engagement_docs = em.get_engagements(database=self.database)
        self.assertTrue(engagement_docs)
        self.assertFalse([e for e in engagement_docs if c.DELETED in e])

    def test_get_engagements_with_users(self) -> None:
        """Test get_engagements with users routine"""

        # test for a list with data.
        engagements = em.get_engagements(self.database)
        self.assertTrue(engagements)
        self.assertEqual(engagements[0][c.CREATED_BY], self.user_name)

    def test_get_engagement(self) -> None:
        """Test get_engagement routine"""

        # take the first document
        engagement_docs = em.get_engagements(database=self.database)
        engagement_id = engagement_docs[0]["_id"]

        self.assertIsInstance(engagement_id, ObjectId)

        engagement_doc = em.get_engagement(
            database=self.database, engagement_id=engagement_id
        )

        self.assertIsNotNone(engagement_doc)
        self.assertFalse(c.DELETED in engagement_doc)

    def test_get_engagement_with_user(self) -> None:
        """Test get_engagement with user routine"""

        # take the first document
        engagement_doc = em.get_engagement(self.database, self.engagement_id)
        self.assertTrue(engagement_doc)
        self.assertEqual(engagement_doc[c.CREATED_BY], self.user_name)

    def test_update_engagement(self) -> None:
        """Test update_engagement routine"""

        new_name = "Engagement 3"
        new_description = "Engagement 3 description"
        engagement_docs = em.get_engagements(database=self.database)
        engagement_id = engagement_docs[0]["_id"]

        self.assertIsInstance(engagement_id, ObjectId)

        engagement_doc = em.update_engagement(
            self.database,
            engagement_id,
            self.user_name,
            new_name,
            new_description,
        )

        self.assertEqual(engagement_doc[c.ENGAGEMENT_NAME], new_name)
        self.assertEqual(
            engagement_doc[c.ENGAGEMENT_DESCRIPTION], new_description
        )
        self.assertNotIn(c.ENGAGEMENT_DELIVERY_SCHEDULE, engagement_doc)
        self.assertEqual(self.user_name, engagement_doc[c.CREATED_BY])
        self.assertEqual(self.user_name, engagement_doc[c.UPDATED_BY])

    def test_update_engagement_status(self) -> None:
        """Test update_engagement status"""

        engagement_docs = em.get_engagements(database=self.database)
        engagement_id = engagement_docs[0]["_id"]
        # pylint: disable=unexpected-keyword-arg
        engagement_doc = em.update_engagement(
            self.database,
            engagement_id,
            self.user_name,
            status="Inactive",
        )

        self.assertEqual(engagement_doc[c.STATUS], "Inactive")

    def test_update_engagement_bad_string_id(self) -> None:
        """Test update_engagement routine with a bad string id"""

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
                self.user_name,
                new_name,
                new_description,
                [audience],
            )

    def test_delete_engagement(self) -> None:
        """Test delete_engagement routine"""

        # create engagement
        engagement_id = em.set_engagement(
            self.database,
            "Fall 2024",
            "fall of 2024",
            [self.audience],
            self.user_name,
        )

        self.assertIsInstance(engagement_id, ObjectId)

        # delete created engagement
        delete_flag = em.delete_engagement(self.database, engagement_id)

        self.assertTrue(delete_flag)

        # validate the engagement was deleted
        engagement_doc = em.get_engagement(self.database, engagement_id)
        self.assertIsNone(engagement_doc)

    def test_create_and_get_engagement_with_many_audiences(self) -> None:
        """Test creating an engagement with many audiences"""

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
            self.user_name,
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
        """Test creating an engagement and remove an audience after"""

        engagement_id = em.set_engagement(
            self.database,
            "Engagement 2",
            "Engagement 2 Description",
            [self.audience],
            self.user_name,
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
            self.user_name,
            [self.audience[c.OBJECT_ID]],
        )
        self.assertTrue(result)

        # ensure the audience was removed
        updated = em.get_engagement(self.database, engagement_id)
        self.assertIn(c.AUDIENCES, updated)

        # test audience should not be there
        self.assertFalse(updated[c.AUDIENCES])

    def test_set_engagement_remove_audience_str_audience(self) -> None:
        """Test creating an engagement and remove a string audience id"""

        # create audience normally
        engagement_id = em.set_engagement(
            self.database,
            "Engagement 2",
            "Engagement 2 Description",
            [self.audience],
            self.user_name,
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
                self.user_name,
                [str(self.audience[c.OBJECT_ID])],
            )

    def test_set_engagement_attach_audience_after(self) -> None:
        """Test creating an engagement and attaching an audience after"""

        engagement_id = em.set_engagement(
            self.database,
            "Engagement 2",
            "Engagement 2 Description",
            [self.audience],
            self.user_name,
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
            self.database, engagement_id, self.user_name, [new_audience]
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
        with a str object id"""

        engagement_id = em.set_engagement(
            self.database,
            "Engagement 2",
            "Engagement 2 Description",
            [self.audience],
            self.user_name,
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
                self.database, engagement_id, self.user_name, [new_audience]
            )

    def test_set_engagement_attach_lookalike_audience(self):
        """Test creating an engagement and attaching a lookalike
        audience after"""
        engagement_id = em.set_engagement(
            self.database,
            "Engagement 2",
            "Engagement 2 Description",
            [self.audience],
            self.user_name,
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
            c.LOOKALIKE: True,
            c.OBJECT_ID: lookalike_audience[c.ID],
            c.LOOKALIKE_SOURCE_AUD_ID: source_audience_id,
            c.LOOKALIKE_AUD_NAME: lookalike_audience[c.NAME],
        }

        # attach the lookalike audience
        result = em.append_audiences_to_engagement(
            self.database,
            engagement_id,
            self.user_name,
            [new_lookalike_audience],
        )
        self.assertTrue(result)

        # ensure the audience was updated
        updated = em.get_engagement(self.database, engagement_id)
        self.assertIn(c.AUDIENCES, updated)

        # test audience appears as expected
        self.assertTrue(updated[c.AUDIENCES])
        self.assertEqual(len(updated[c.AUDIENCES]), 2)
        self.assertTrue(updated[c.AUDIENCES][1][c.LOOKALIKE])

    def test_get_engagements_via_audience_id(self) -> None:
        """Test getting engagements with an audience_id"""

        engagements = []
        for item in range(2):
            # create audience normally
            engagement_id = em.set_engagement(
                self.database,
                f"Engagement {item}",
                f"Engagement {item} Description",
                [self.audience],
                self.user_name,
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
        self.assertFalse([e for e in engagements if c.DELETED in e])

    # pylint: disable=too-many-function-args
    def test_get_engaged_audience_insights(self) -> None:
        """Test getting engaged audience insights"""

        engagements = []
        for item in range(2):

            # set destination for audience
            audience = self.audience
            audience[c.DESTINATIONS].append(
                {c.OBJECT_ID: self.destination[c.ID]}
            )

            # create engagement normally
            engagement_id = em.set_engagement(
                self.database,
                f"Engagement Aud {item}",
                f"Engagement {item} Description",
                [audience],
                self.user_name,
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
        audience_insights = om.get_audience_insights(
            self.database, self.audience[c.ID]
        )

        # test list
        self.assertTrue(audience_insights, dict)
        self.assertEqual(len(audience_insights), 3)

        for engagement in audience_insights:
            self.assertIn(c.DELIVERIES, engagement)
            self.assertIn(c.AUDIENCE_LAST_DELIVERED, engagement)
            self.assertIn(c.ID, engagement)
            self.assertIn(c.ENGAGEMENT, engagement)

            matched_engagements = [
                x
                for x in engagements
                if x[c.ID] == engagement[c.ENGAGEMENT][c.ID]
            ]
            if not matched_engagements:
                continue

            self.assertTrue(matched_engagements)
            self.assertEqual(len(matched_engagements), 1)

            # now test the engagement to ensure lookup done properly
            for matched_engagement in matched_engagements:
                for key, value in matched_engagement.items():
                    # test all the engagement params to the looked up ones.
                    if key == c.AUDIENCES:
                        continue
                    self.assertEqual(engagement[c.ENGAGEMENT][key], value)

    def test_add_delivery_jobs_to_engaged_audience_destination(self) -> None:
        """Test adding a delivery job to the engaged_audience_destination"""

        # create an engagement
        new_engagement = {
            c.ENGAGEMENT_NAME: "Spring 2027",
            c.ENGAGEMENT_DESCRIPTION: "high ltv for spring 2027",
            c.AUDIENCES: [
                {
                    c.OBJECT_ID: self.audience[c.ID],
                    c.DESTINATIONS: [
                        {c.OBJECT_ID: self.destination[c.ID]},
                    ],
                },
            ],
        }

        engagement_id = em.set_engagement(
            self.database,
            new_engagement[c.ENGAGEMENT_NAME],
            new_engagement[c.ENGAGEMENT_DESCRIPTION],
            new_engagement[c.AUDIENCES],
            self.user_name,
        )

        # get engagement to verify that it was created
        self.assertTrue(engagement_id)

        # create a delivery job
        audience_delivery_job = dpm.set_delivery_job(
            self.database,
            self.audience[c.ID],
            self.destination[c.ID],
            [],
            engagement_id,
        )
        self.assertTrue(audience_delivery_job)

        # mongomock does not support array_filters but pymongo and documentDB do.
        with self.assertRaises(TypeError):
            doc = em.add_delivery_job(
                self.database,
                engagement_id,
                self.audience[c.ID],
                self.destination[c.ID],
                audience_delivery_job[c.ID],
            )

            # validate the delivery job was set correctly
            self.assertEqual(
                doc[c.AUDIENCES][0][c.DESTINATIONS][0][c.DELIVERY_JOB_ID],
                audience_delivery_job[c.ID],
            )

    def test_get_engagements_summary(self) -> None:
        """Test get_engagements routine"""

        # create another audience
        audience = om.create_audience(
            self.database, "audience_group", [], [], self.user_name, 1560
        )

        for i in range(20):
            # an audience with two destinations
            new_engagement = {
                c.ENGAGEMENT_NAME: f"Spring 2202{i}",
                c.ENGAGEMENT_DESCRIPTION: f"high ltv for spring 202{i}",
                c.AUDIENCES: [
                    {
                        c.OBJECT_ID: audience[c.ID],
                        c.DESTINATIONS: [
                            {
                                c.OBJECT_ID: self.destinations[0][c.ID],
                                c.DELIVERY_PLATFORM_CONTACT_LIST: "random_extension",
                                c.STATUS: c.STATUS_PENDING,
                            },
                            {
                                c.OBJECT_ID: self.destinations[1][c.ID],
                                c.STATUS: c.AUDIENCE_STATUS_ERROR
                                if i % 5 == 0
                                else c.STATUS_SUCCEEDED,
                            },
                        ],
                    },
                    {
                        c.OBJECT_ID: self.audience[c.ID],
                        c.DESTINATIONS: [
                            {
                                c.OBJECT_ID: self.destinations[1][c.ID],
                                c.STATUS: c.STATUS_FAILED
                                if i % 5 == 0
                                else c.STATUS_SUCCEEDED,
                            }
                        ],
                    },
                ],
            }

            em.set_engagement(
                self.database,
                new_engagement[c.ENGAGEMENT_NAME],
                new_engagement[c.ENGAGEMENT_DESCRIPTION],
                new_engagement[c.AUDIENCES],
                self.user_name,
            )

        engagement_docs = em.get_engagements_summary(database=self.database)

        # get all engagements for validation
        all_engagements = em.get_engagements(self.database)

        self.assertTrue(engagement_docs)
        self.assertFalse([e for e in engagement_docs if c.DELETED in e])

        # ensure length of grouped engagements is equal to length of all engagements.
        # this checks to ensure the grouping was done correctly.
        self.assertEqual(len(engagement_docs), len(all_engagements))

        # test the grouped engagements for existence of key fields
        for engagement in engagement_docs:
            self.assertIn(c.ID, engagement)
            self.assertIn(c.NAME, engagement)
            self.assertIn(c.ENGAGEMENT_DESCRIPTION, engagement)
            self.assertIn(c.CREATED_BY, engagement)
            self.assertIn(c.UPDATED_BY, engagement)
            self.assertIn(c.CREATE_TIME, engagement)
            self.assertIn(c.UPDATE_TIME, engagement)
            self.assertIn(c.AUDIENCES, engagement)
            self.assertIn(c.SIZE, engagement)

            for audience in engagement[c.AUDIENCES]:
                self.assertIn(c.NAME, audience)
                self.assertIn(c.DESTINATIONS, audience)
                self.assertIn(c.OBJECT_ID, audience)
                self.assertIn(c.SIZE, audience)
                if not audience[c.DESTINATIONS]:
                    continue
                for destination in audience[c.DESTINATIONS]:
                    self.assertIn(c.NAME, destination)
                    self.assertIn(c.OBJECT_ID, destination)

    def test_get_engagement_summary(self) -> None:
        """Test get_engagement_summary routine"""

        # create another audience
        audience = om.create_audience(
            self.database,
            "audience_group",
            [],
            [],
            user_name=self.user_name,
            size=1609,
        )

        # an audience with two destinations
        new_engagement = {
            c.ENGAGEMENT_NAME: "Autumn 2024",
            c.ENGAGEMENT_DESCRIPTION: "high ltv for Autumn 2024",
            c.AUDIENCES: [
                {
                    c.OBJECT_ID: audience[c.ID],
                    c.SIZE: audience[c.SIZE],
                    c.DESTINATIONS: [
                        {
                            c.OBJECT_ID: self.destinations[0][c.ID],
                            c.DELIVERY_PLATFORM_CONTACT_LIST: "random_extension",
                            c.STATUS: c.STATUS_PENDING,
                        },
                        {
                            c.OBJECT_ID: self.destinations[1][c.ID],
                            c.STATUS: c.STATUS_SUCCEEDED,
                        },
                    ],
                },
                {
                    c.OBJECT_ID: self.audience[c.ID],
                    c.SIZE: audience[c.SIZE],
                    c.DESTINATIONS: [
                        {
                            c.OBJECT_ID: self.destinations[1][c.ID],
                            c.STATUS: c.STATUS_SUCCEEDED,
                        }
                    ],
                },
            ],
        }

        engagement_id = em.set_engagement(
            self.database,
            new_engagement[c.ENGAGEMENT_NAME],
            new_engagement[c.ENGAGEMENT_DESCRIPTION],
            new_engagement[c.AUDIENCES],
            self.user_name,
        )

        engagement_docs = em.get_engagements_summary(
            self.database, [engagement_id]
        )

        # ensure length of grouped engagements is equal to one
        self.assertEqual(len(engagement_docs), 1)
        engagement = engagement_docs[0]

        # test the grouped engagements for existence of key fields
        self.assertIn(c.ID, engagement)
        self.assertIn(c.NAME, engagement)
        self.assertIn(c.ENGAGEMENT_DESCRIPTION, engagement)
        self.assertIn(c.CREATED_BY, engagement)
        self.assertIn(c.UPDATED_BY, engagement)
        self.assertIn(c.CREATE_TIME, engagement)
        self.assertIn(c.UPDATE_TIME, engagement)
        self.assertIn(c.AUDIENCES, engagement)
        self.assertEqual(
            engagement[c.SIZE], audience[c.SIZE] + self.audience[c.SIZE]
        )

        for audience in engagement[c.AUDIENCES]:
            self.assertIn(c.NAME, audience)
            self.assertIn(c.DESTINATIONS, audience)
            self.assertIn(c.OBJECT_ID, audience)
            self.assertIn(c.SIZE, audience)
            if not audience[c.DESTINATIONS]:
                continue
            for destination in audience[c.DESTINATIONS]:
                self.assertIn(c.NAME, destination)
                self.assertIn(c.OBJECT_ID, destination)

    def test_append_destination_to_engagement_audience(self):
        """Test appending a destination to an engagement audience"""

        destination = dpm.get_delivery_platform_by_type(
            self.database, c.DELIVERY_PLATFORM_FACEBOOK
        )

        destination_to_add = {c.OBJECT_ID: destination[c.ID]}

        audience_one = om.create_audience(
            self.database, "Audience1", [], [], self.user_name, 201
        )
        audience_two = om.create_audience(
            self.database, "Audience2", [], [], self.user_name, 202
        )

        audience_one_dict = {
            c.OBJECT_ID: audience_one[c.ID],
            c.DESTINATIONS: [],
        }
        audience_two_dict = {
            c.OBJECT_ID: audience_two[c.ID],
            c.DESTINATIONS: [],
        }

        engagement_id = em.set_engagement(
            self.database,
            "Engagement1",
            "Engagement1",
            [audience_one_dict, audience_two_dict],
            self.user_name,
        )

        # due to mocking issues certain queries do not work
        # but have been verified on a real database
        with self.assertRaises(pymongo.errors.WriteError):
            em.append_destination_to_engagement_audience(
                self.database,
                engagement_id,
                audience_one[c.ID],
                destination_to_add,
                self.user_name,
            )

    def test_remove_destination_from_engagement_audience(self):
        """Test removing a destination from an engagement audience"""
        audience_one = om.create_audience(
            self.database, "Audience1", [], [], self.user_name, 201
        )
        audience_two = om.create_audience(
            self.database, "Audience2", [], [], self.user_name, 202
        )

        audience_one_dict = {
            c.OBJECT_ID: audience_one[c.ID],
            c.DESTINATIONS: [{c.OBJECT_ID: self.destinations[0][c.ID]}],
        }
        audience_two_dict = {
            c.OBJECT_ID: audience_two[c.ID],
            c.DESTINATIONS: [],
        }

        engagement_id = em.set_engagement(
            self.database,
            "Engagement1",
            "Engagement1",
            [audience_one_dict, audience_two_dict],
            self.user_name,
        )

        # due to mocking issues certain queries do not work
        # but have been verified on a real database
        # Due to that issue this return will be None when the DB is mocked
        with self.assertRaises(pymongo.errors.WriteError):
            em.remove_destination_from_engagement_audience(
                self.database,
                engagement_id,
                audience_one[c.ID],
                self.destinations[0][c.ID],
                self.user_name,
            )

    def test_check_active_engagement_deliveries(self) -> None:
        """Test check_active_engagement_deliveries routine"""

        # an audience with two destinations
        new_engagement = {
            c.ENGAGEMENT_NAME: "Autumn Check",
            c.ENGAGEMENT_DESCRIPTION: "Check for Autumn 2024",
            c.AUDIENCES: [
                {
                    c.OBJECT_ID: self.audience[c.ID],
                    c.SIZE: 5000,
                    c.DESTINATIONS: [
                        {
                            c.OBJECT_ID: self.destinations[1][c.ID],
                            c.STATUS: c.STATUS_SUCCEEDED,
                        }
                    ],
                },
            ],
        }

        engagement_id = em.set_engagement(
            self.database,
            new_engagement[c.ENGAGEMENT_NAME],
            new_engagement[c.ENGAGEMENT_DESCRIPTION],
            new_engagement[c.AUDIENCES],
            self.user_name,
        )
        self.assertIsNotNone(engagement_id)

        # simulate setting a delivery job directly
        delivery_job_id = (
            self.database[c.DATA_MANAGEMENT_DATABASE][
                c.DELIVERY_JOBS_COLLECTION
            ]
            .insert_one(
                {
                    c.AUDIENCE_ID: self.audience[c.ID],
                    c.ENGAGEMENT_ID: engagement_id,
                    c.JOB_STATUS: c.AUDIENCE_STATUS_DELIVERED,
                    c.DELIVERY_PLATFORM_ID: self.destinations[1][c.ID],
                }
            )
            .inserted_id
        )

        # assign the delivery job to the engagement
        # mongomock does not support double nested push, so we will do it manually.
        engagement = em.get_engagement(self.database, engagement_id)
        engagement[c.AUDIENCES][0][c.DESTINATIONS][0][
            c.DELIVERY_JOB_ID
        ] = delivery_job_id

        # update the doc
        self.database[c.DATA_MANAGEMENT_DATABASE][
            c.ENGAGEMENTS_COLLECTION
        ].find_one_and_update({c.ID: engagement_id}, {"$set": engagement})

        active_deliveries = em.check_active_engagement_deliveries(
            self.database
        )

        self.assertTrue(active_deliveries)
        self.assertIn(c.DELIVERY_JOB_ID, active_deliveries[0])

    def test_check_active_engagement_deliveries_non_delivered(self) -> None:
        """Test check_active_engagement_deliveries routine with no deliveries"""

        # an audience with two destinations
        new_engagement = {
            c.ENGAGEMENT_NAME: "Autumn Check",
            c.ENGAGEMENT_DESCRIPTION: "Check for Autumn 2024",
            c.AUDIENCES: [
                {
                    c.OBJECT_ID: self.audience[c.ID],
                    c.SIZE: 5000,
                    c.DESTINATIONS: [
                        {
                            c.OBJECT_ID: self.destinations[1][c.ID],
                            c.STATUS: c.STATUS_SUCCEEDED,
                        }
                    ],
                },
            ],
        }

        engagement_id = em.set_engagement(
            self.database,
            new_engagement[c.ENGAGEMENT_NAME],
            new_engagement[c.ENGAGEMENT_DESCRIPTION],
            new_engagement[c.AUDIENCES],
            self.user_name,
        )
        self.assertIsNotNone(engagement_id)

        active_deliveries = em.check_active_engagement_deliveries(
            self.database
        )

        self.assertFalse(active_deliveries)

    def test_get_all_audience_destinations(self) -> None:
        """Test getting all audiences and their unique assigned
        destinations across engagements."""

        engagements = []
        for item in range(2):

            # set destination for audience
            audience = self.audience
            audience[c.DESTINATIONS] = [
                {c.OBJECT_ID: x[c.ID]} for x in self.destinations
            ]

            # create engagement normally
            engagement_id = em.set_engagement(
                self.database,
                f"Engagement Aud {item}",
                f"Engagement {item} Description",
                [audience],
                self.user_name,
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
        audience_destinations = eam.get_all_engagement_audience_destinations(
            self.database, [self.audience[c.ID]]
        )

        # test the response
        self.assertTrue(audience_destinations)
        self.assertIsInstance(audience_destinations, list)

        # grab the first audience
        audience_destination = audience_destinations[0]

        # test each destination
        self.assertIn(c.DESTINATIONS, audience_destination)
        self.assertEqual(len(audience_destination[c.DESTINATIONS]), 2)
        for destination in audience_destination[c.DESTINATIONS]:
            # find the matching destination and ensure it is identical.
            matched_destinations = [
                x for x in self.destinations if x[c.ID] == destination[c.ID]
            ]
            self.assertTrue(matched_destinations)
            self.assertEqual(destination, matched_destinations[0])
