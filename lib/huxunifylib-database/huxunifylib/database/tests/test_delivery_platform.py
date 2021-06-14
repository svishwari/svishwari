"""Delivery Platform management tests."""

import datetime
import unittest
import mongomock
from bson import ObjectId

import huxunifylib.database.delivery_platform_management as dpm
import huxunifylib.database.audience_management as am
import huxunifylib.database.data_management as dm
import huxunifylib.database.constants as c
from huxunifylib.database import delete_util
from huxunifylib.database.client import DatabaseClient
import huxunifylib.database.db_exceptions as de


# pylint: disable=R0902,R0904,C0302
class TestDeliveryPlatform(unittest.TestCase):
    """Test delivery platform management module."""

    # pylint: disable=too-many-instance-attributes

    @mongomock.patch(servers=(("localhost", 27017),))
    def setUp(self):

        self.database = DatabaseClient(
            "localhost", 27017, None, None
        ).connect()

        self.database.drop_database(c.DATA_MANAGEMENT_DATABASE)

        self.generic_campaigns = [
            {"campaign_id": "campaign_id_1", "ad_set_id": "ad_set_id_2"}
        ]

        # Set delivery platform
        self.auth_details_facebook = {
            "facebook_access_token": "path1",
            "facebook_app_secret": "path2",
            "facebook_app_id": "path3",
            "facebook_ad_account_id": "path4",
        }

        self.auth_details_sfmc = {
            "sfmc_client_id": "path1",
            "sfmc_client_secret": "path2",
            "sfmc_account_id": "path3",
            "sfmc_auth_base_uri": "path4",
            "sfmc_rest_base_uri": "path5",
            "sfmc_soap_base_uri": "path5",
        }

        self.delivery_platform_doc = dpm.set_delivery_platform(
            self.database,
            c.DELIVERY_PLATFORM_FACEBOOK,
            "My delivery platform for Facebook",
            self.auth_details_facebook,
        )

        self.delivery_platform_doc_sfmc = dpm.set_delivery_platform(
            self.database,
            c.DELIVERY_PLATFORM_SFMC,
            "My delivery platform for SFMC",
            self.auth_details_sfmc,
        )

        self.delivery_platform_doc_user = dpm.set_delivery_platform(
            self.database,
            c.DELIVERY_PLATFORM_SFMC,
            "My second delivery platform for SFMC",
            "test_user",
            self.auth_details_sfmc,
        )

        self.ingestion_job_doc = dm.set_ingestion_job(
            self.database, ObjectId("5dff99c10345af022f219bbf")
        )

        self.source_audience_doc = am.create_audience(
            self.database,
            "My Audience",
            [],
            self.ingestion_job_doc[c.ID],
        )

        self.audience_2_doc = am.create_audience(
            self.database,
            "My Audience 2",
            [],
            self.ingestion_job_doc[c.ID],
        )

        doc = dpm.set_connection_status(
            self.database,
            self.delivery_platform_doc[c.ID],
            c.STATUS_SUCCEEDED,
        )

        self.assertTrue(doc is not None)

        self.delivery_job_doc = dpm.set_delivery_job(
            self.database,
            self.source_audience_doc[c.ID],
            self.delivery_platform_doc[c.ID],
            self.generic_campaigns,
        )

        self.delivery_job_2_doc = dpm.set_delivery_job(
            self.database,
            self.audience_2_doc[c.ID],
            self.delivery_platform_doc[c.ID],
            self.generic_campaigns,
        )

        self.lookalike_audience_doc = (
            dpm.create_delivery_platform_lookalike_audience(
                self.database,
                self.delivery_platform_doc[c.ID],
                self.source_audience_doc[c.ID],
                "Lookalike audience",
                0.01,
                "US",
            )
        )

        doc = dpm.set_connection_status(
            self.database,
            self.delivery_platform_doc[c.ID],
            c.STATUS_PENDING,
        )

        self.assertTrue(doc is not None)

    def _set_delivery_job(self) -> ObjectId:
        """Set delivery_job.

        Returns:
            ObjectId: Delivery job ID.
        """
        dpm.set_connection_status(
            self.database,
            self.delivery_platform_doc[c.ID],
            c.STATUS_SUCCEEDED,
        )
        return dpm.set_delivery_job(
            self.database,
            self.source_audience_doc[c.ID],
            self.delivery_platform_doc[c.ID],
            self.generic_campaigns,
        )[c.ID]

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_set_delivery_platform_facebook(self):
        """Test set_delivery_platform for facebook."""

        doc = dpm.set_delivery_platform(
            self.database,
            c.DELIVERY_PLATFORM_FACEBOOK,
            "My delivery platform 1",
            self.auth_details_facebook,
        )

        self.assertTrue(doc is not None)
        self.assertTrue(doc[c.ID] is not None)

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_set_duplicate_delivery_platform_facebook(self):
        """Test set_delivery_platform for facebook."""

        doc1 = dpm.set_delivery_platform(
            self.database,
            c.DELIVERY_PLATFORM_FACEBOOK,
            "Test duplicate Facebook",
            self.auth_details_facebook,
        )

        self.assertIsNotNone(doc1)
        self.assertIsNotNone(doc1[c.ID])

        with self.assertRaises(de.DuplicateName):
            dpm.set_delivery_platform(
                self.database,
                c.DELIVERY_PLATFORM_FACEBOOK,
                doc1[c.DELIVERY_PLATFORM_NAME],
                self.auth_details_facebook,
            )

    def test_set_delivery_platform_sfmc(self):
        """Test set_delivery_platform for sfmc."""

        doc = dpm.set_delivery_platform(
            self.database,
            c.DELIVERY_PLATFORM_SFMC,
            "My delivery platform 2",
            self.auth_details_sfmc,
        )

        self.assertIsNotNone(doc)
        self.assertIsNotNone(doc[c.ID])

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_set_delivery_platform_facebook_with_user(self):
        """Test set_delivery_platform for facebook with user."""

        doc = dpm.set_delivery_platform(
            self.database,
            c.DELIVERY_PLATFORM_FACEBOOK,
            "My delivery platform 1",
            "user_id_or_email",
            self.auth_details_facebook,
        )

        self.assertIsNotNone(doc)
        self.assertIsNotNone(doc[c.ID])

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_get_deleted_delivery_platform(self):
        """Test get_deleted_delivery_platform."""

        doc = dpm.set_delivery_platform(
            self.database,
            c.DELIVERY_PLATFORM_FACEBOOK,
            "My delivery platform 1",
            "user_id_or_email",
            self.auth_details_facebook,
            deleted=True,
        )
        self.assertIsNone(doc)

        doc = dpm.get_delivery_platform(
            self.database, self.delivery_platform_doc[c.ID]
        )
        self.assertIsNotNone(doc)

        dpm.update_delivery_platform(
            database=self.database,
            delivery_platform_id=self.delivery_platform_doc[c.ID],
            name="Updated name",
            delivery_platform_type=c.DELIVERY_PLATFORM_FACEBOOK,
            deleted=True,
        )
        doc = dpm.get_delivery_platform(
            self.database, self.delivery_platform_doc[c.ID]
        )
        self.assertIsNone(doc)

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_get_delivery_platform(self):
        """Test get_delivery_platform."""

        # Get delivery platform
        doc = dpm.get_delivery_platform(
            self.database, self.delivery_platform_doc[c.ID]
        )

        self.assertIsNotNone(doc)
        self.assertTrue(c.DELIVERY_PLATFORM_NAME in doc)
        self.assertTrue(c.DELIVERY_PLATFORM_TYPE in doc)
        self.assertTrue(c.DELIVERY_PLATFORM_AUTH in doc)
        self.assertTrue(c.DELIVERY_PLATFORM_STATUS in doc)

        self.assertEqual(
            doc[c.DELIVERY_PLATFORM_NAME], "My delivery platform for Facebook"
        )

        self.assertEqual(
            doc[c.DELIVERY_PLATFORM_TYPE], c.DELIVERY_PLATFORM_FACEBOOK
        )

        self.assertEqual(
            doc[c.DELIVERY_PLATFORM_AUTH], self.auth_details_facebook
        )
        self.assertEqual(doc[c.DELIVERY_PLATFORM_STATUS], c.STATUS_PENDING)

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_get_delivery_platforms_by_id(self):
        """Test get_delivery_platforms list"""

        # Get delivery platform
        ids = [self.delivery_platform_doc[c.ID]]
        docs = dpm.get_delivery_platforms_by_id(self.database, ids)

        self.assertIsNotNone(docs[0])
        self.assertTrue(c.DELIVERY_PLATFORM_NAME in docs[0])
        self.assertTrue(c.DELIVERY_PLATFORM_TYPE in docs[0])
        self.assertTrue(c.DELIVERY_PLATFORM_AUTH in docs[0])
        self.assertTrue(c.DELIVERY_PLATFORM_STATUS in docs[0])

        self.assertEqual(
            docs[0][c.DELIVERY_PLATFORM_NAME],
            "My delivery platform for Facebook",
        )

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_get_delivery_platform_with_user(self):
        """Test get_delivery_platform."""

        # Get delivery platform
        doc = dpm.get_delivery_platform(
            self.database, self.delivery_platform_doc_user[c.ID]
        )

        self.assertIsNotNone(doc)
        self.assertTrue(c.DELIVERY_PLATFORM_NAME in doc)
        self.assertTrue(c.DELIVERY_PLATFORM_TYPE in doc)
        self.assertTrue(c.DELIVERY_PLATFORM_AUTH in doc)
        self.assertTrue(c.DELIVERY_PLATFORM_STATUS in doc)

        self.assertEqual(
            doc[c.DELIVERY_PLATFORM_NAME],
            "My second delivery platform for SFMC",
        )

        self.assertEqual(
            doc[c.DELIVERY_PLATFORM_TYPE], c.DELIVERY_PLATFORM_SFMC
        )

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_get_delivery_platform_sfmc(self):
        """Test get_delivery_platform for sfmc."""

        # Get delivery platform
        doc = dpm.get_delivery_platform(
            self.database, self.delivery_platform_doc_sfmc[c.ID]
        )

        self.assertIsNotNone(doc)
        self.assertTrue(c.DELIVERY_PLATFORM_NAME in doc)
        self.assertTrue(c.DELIVERY_PLATFORM_TYPE in doc)
        self.assertTrue(c.DELIVERY_PLATFORM_AUTH in doc)
        self.assertTrue(c.DELIVERY_PLATFORM_STATUS in doc)

        self.assertEqual(
            doc[c.DELIVERY_PLATFORM_NAME], "My delivery platform for SFMC"
        )

        self.assertEqual(
            doc[c.DELIVERY_PLATFORM_TYPE], c.DELIVERY_PLATFORM_SFMC
        )

        self.assertEqual(doc[c.DELIVERY_PLATFORM_AUTH], self.auth_details_sfmc)
        self.assertEqual(doc[c.DELIVERY_PLATFORM_STATUS], c.STATUS_PENDING)

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_get_all_delivery_platforms(self):
        """Test get_all_delivery_platforms."""

        # Get all existing delivery platforms
        platforms = dpm.get_all_delivery_platforms(self.database)

        self.assertIsNotNone(platforms)
        self.assertEqual(len(platforms), 3)

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_connection_status(self):
        """Test connection status functions."""

        # Set and get connection status
        doc = dpm.set_connection_status(
            self.database,
            self.delivery_platform_doc[c.ID],
            c.STATUS_SUCCEEDED,
        )

        self.assertIsNotNone(doc)
        self.assertTrue(c.DELIVERY_PLATFORM_STATUS in doc)

        connection_status = dpm.get_connection_status(
            self.database,
            self.delivery_platform_doc[c.ID],
        )

        self.assertEqual(connection_status, c.STATUS_SUCCEEDED)

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_authentication_details(self):
        """Test set/get auth details functions."""

        new_auth_details = {
            "facebook_access_token": "path10",
            "facebook_app_secret": "path20",
            "facebook_app_id": "path30",
            "facebook_ad_account_id": "path40",
        }

        doc = dpm.set_authentication_details(
            self.database, self.delivery_platform_doc[c.ID], new_auth_details
        )

        self.assertIsNotNone(doc)
        self.assertTrue(c.DELIVERY_PLATFORM_AUTH in doc)

        auth_details = dpm.get_authentication_details(
            self.database, self.delivery_platform_doc[c.ID]
        )

        self.assertEqual(auth_details, new_auth_details)

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_delivery_platform_name(self):
        """Test set/get delivery platform name functions."""

        # Set and get name
        new_name = "New name"

        doc = dpm.set_name(
            self.database, self.delivery_platform_doc[c.ID], new_name
        )

        self.assertIsNotNone(doc)
        self.assertTrue(c.DELIVERY_PLATFORM_NAME in doc)

        name = dpm.get_name(self.database, self.delivery_platform_doc[c.ID])

        self.assertEqual(name, new_name)

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_delivery_platform_type(self):
        """Test set/get delivery platform type functions."""

        # Set and get platform type
        new_platform_type = c.DELIVERY_PLATFORM_GOOGLE

        doc = dpm.set_platform_type(
            self.database,
            self.delivery_platform_doc[c.ID],
            new_platform_type,
        )

        self.assertIsNotNone(doc)
        self.assertTrue(c.DELIVERY_PLATFORM_TYPE in doc)

        platform_type = dpm.get_platform_type(
            self.database, self.delivery_platform_doc[c.ID]
        )

        self.assertEqual(platform_type, new_platform_type)

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_update_delivery_platform(self):
        """Test delivery platform update functions."""

        new_auth_details = {
            "facebook_access_token": "path10",
            "facebook_app_secret": "path20",
            "facebook_app_id": "path30",
            "facebook_ad_account_id": "path40",
        }

        doc = dpm.update_delivery_platform(
            database=self.database,
            delivery_platform_id=self.delivery_platform_doc[c.ID],
            name="Updated name",
            delivery_platform_type=c.DELIVERY_PLATFORM_FACEBOOK,
            authentication_details=new_auth_details,
        )

        self.assertIsNotNone(doc)
        self.assertTrue(c.DELIVERY_PLATFORM_TYPE in doc)
        self.assertTrue(c.DELIVERY_PLATFORM_NAME in doc)
        self.assertTrue(c.DELIVERY_PLATFORM_AUTH in doc)

        self.assertEqual(doc[c.DELIVERY_PLATFORM_NAME], "Updated name")
        self.assertEqual(
            doc[c.DELIVERY_PLATFORM_TYPE], c.DELIVERY_PLATFORM_FACEBOOK
        )
        self.assertEqual(doc[c.DELIVERY_PLATFORM_AUTH], new_auth_details)
        self.assertFalse(doc[c.ADDED])
        self.assertFalse(c.DELETED in doc)

        # update two fields
        doc = dpm.update_delivery_platform(
            database=self.database,
            delivery_platform_id=self.delivery_platform_doc[c.ID],
            name="Test name",
            delivery_platform_type=c.DELIVERY_PLATFORM_GOOGLE,
            added=True,
        )

        self.assertIsNotNone(doc)
        self.assertTrue(c.DELIVERY_PLATFORM_TYPE in doc)
        self.assertTrue(c.DELIVERY_PLATFORM_NAME in doc)
        self.assertTrue(c.DELIVERY_PLATFORM_AUTH in doc)

        self.assertEqual(doc[c.DELIVERY_PLATFORM_NAME], "Test name")
        self.assertEqual(
            doc[c.DELIVERY_PLATFORM_TYPE], c.DELIVERY_PLATFORM_GOOGLE
        )
        self.assertEqual(doc[c.DELIVERY_PLATFORM_AUTH], new_auth_details)
        self.assertTrue(doc[c.ADDED])

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_set_delivery_job(self):
        """Test set_delivery_job."""

        doc = dpm.set_connection_status(
            self.database,
            self.delivery_platform_doc[c.ID],
            c.STATUS_SUCCEEDED,
        )

        self.assertIsNotNone(doc)

        doc = dpm.set_delivery_job(
            self.database,
            self.delivery_platform_doc[c.ID],
            self.delivery_platform_doc[c.ID],
            self.generic_campaigns,
        )

        self.assertIsNotNone(doc)
        self.assertTrue(c.ID in doc)
        self.assertIsNotNone(doc[c.ID])

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_get_delivery_job(self):
        """Test get_delivery_job."""

        delivery_job = dpm.get_delivery_job(
            self.database, self.delivery_job_doc[c.ID]
        )

        self.assertIsNotNone(delivery_job)
        self.assertTrue(c.AUDIENCE_ID in delivery_job)
        self.assertTrue(c.CREATE_TIME in delivery_job)
        self.assertTrue(c.JOB_STATUS in delivery_job)
        self.assertTrue(c.DELIVERY_PLATFORM_ID in delivery_job)
        self.assertEqual(
            delivery_job[c.AUDIENCE_ID], self.source_audience_doc[c.ID]
        )
        self.assertEqual(delivery_job[c.JOB_STATUS], c.STATUS_PENDING)

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_delivery_job_status(self):
        """Test delivery job status functions."""

        doc = dpm.set_delivery_job_status(
            self.database,
            self.delivery_job_doc[c.ID],
            c.STATUS_SUCCEEDED,
        )

        self.assertTrue(doc is not None)
        self.assertTrue(c.AUDIENCE_ID in doc)
        self.assertTrue(c.CREATE_TIME in doc)
        self.assertTrue(c.JOB_END_TIME in doc)
        self.assertTrue(c.JOB_STATUS in doc)
        self.assertEqual(doc[c.JOB_STATUS], c.STATUS_SUCCEEDED)

        status = dpm.get_delivery_job_status(
            self.database, self.delivery_job_doc[c.ID]
        )

        self.assertEqual(status, c.STATUS_SUCCEEDED)

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_delivery_job_audience_size(self):
        """Test delivery job audience size functions."""

        # Set delivery job audience size
        doc = dpm.set_delivery_job_audience_size(
            self.database,
            self.delivery_job_doc[c.ID],
            1000,
        )

        self.assertTrue(doc is not None)
        self.assertTrue(c.DELIVERY_PLATFORM_AUD_SIZE in doc)
        self.assertEqual(doc[c.DELIVERY_PLATFORM_AUD_SIZE], 1000)

        # Get delivery job audience size
        audience_size = dpm.get_delivery_job_audience_size(
            self.database,
            self.delivery_job_doc[c.ID],
        )

        self.assertTrue(audience_size is not None)
        self.assertEqual(audience_size, 1000)

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_delivery_job_lookalike_audiences(self):
        """Test delivery job lookalike audiences functions."""

        # Set delivery job lookalike audiences
        lookalike_audiences = [self.lookalike_audience_doc[c.ID]]
        doc = dpm.set_delivery_job_lookalike_audiences(
            self.database,
            self.delivery_job_doc[c.ID],
            lookalike_audiences,
        )

        self.assertTrue(doc is not None)
        self.assertTrue(c.DELIVERY_PLATFORM_LOOKALIKE_AUDS in doc)
        self.assertEqual(
            doc[c.DELIVERY_PLATFORM_LOOKALIKE_AUDS], lookalike_audiences
        )

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_get_audience_recent_delivery_job(self):
        """Test get_audience_recent_delivery_job."""

        # Get the most recent audience delivery job ID
        most_recent_delivery = dpm.get_audience_recent_delivery_job(
            self.database,
            self.source_audience_doc[c.ID],
            self.delivery_platform_doc[c.ID],
        )

        self.assertTrue(
            self.delivery_job_doc[c.ID], most_recent_delivery[c.ID]
        )

    def test_get_delivery_jobs(self):
        """Test get_audience_delivery_job."""

        # Get all delivery jobs for an audience
        delivery_jobs = dpm.get_delivery_jobs(
            self.database,
            self.source_audience_doc[c.ID],
        )

        self.assertTrue(delivery_jobs is not None)
        self.assertEqual(len(delivery_jobs), 1)

    def test_get_all_delivery_jobs(self):
        """All delivery jobs are retrieved."""

        all_delivery_jobs = dpm.get_delivery_jobs(self.database)

        self.assertEqual(len(all_delivery_jobs), 2)

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_get_ingestion_job_audience_delivery_jobs(self):
        """Test get_ingestion_job_audience_delivery_jobs."""

        all_deliveries = dpm.get_ingestion_job_audience_delivery_jobs(
            self.database,
            self.ingestion_job_doc[c.ID],
        )

        self.assertTrue(all_deliveries is not None)

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_create_delivery_platform_lookalike_audience(self):
        """Test to create data platform lookalike audience."""

        delivery_platform_id = self.delivery_platform_doc[c.ID]
        source_audience_id = self.source_audience_doc[c.ID]

        # Set connection status
        dpm.set_connection_status(
            self.database, delivery_platform_id, c.STATUS_SUCCEEDED
        )

        # create lookalike audience without delivery job associated with
        # source audience
        doc = dpm.create_delivery_platform_lookalike_audience(
            self.database,
            delivery_platform_id,
            source_audience_id,
            "Lookalike audience new",
            0.01,
            "US",
        )

        self.assertTrue(doc is not None)
        self.assertTrue(c.DELIVERY_PLATFORM_ID in doc)
        self.assertTrue(c.LOOKALIKE_SOURCE_AUD_ID in doc)
        self.assertTrue(c.LOOKALIKE_AUD_NAME in doc)
        self.assertTrue(c.LOOKALIKE_AUD_COUNTRY in doc)
        self.assertTrue(c.LOOKALIKE_AUD_SIZE_PERCENTAGE in doc)

        delivery_job_doc = dpm.set_delivery_job(
            self.database,
            source_audience_id,
            delivery_platform_id,
            self.generic_campaigns,
        )

        # create lookalike audience with delivery job associated with
        # source audience
        doc = dpm.create_delivery_platform_lookalike_audience(
            self.database,
            delivery_platform_id,
            source_audience_id,
            "Lookalike audience new 2",
            0.01,
            "US",
        )

        self.assertTrue(doc is not None)
        self.assertTrue(c.DELIVERY_PLATFORM_ID in doc)
        self.assertTrue(c.LOOKALIKE_SOURCE_AUD_ID in doc)
        self.assertTrue(c.LOOKALIKE_AUD_NAME in doc)
        self.assertTrue(c.LOOKALIKE_AUD_COUNTRY in doc)
        self.assertTrue(c.LOOKALIKE_AUD_SIZE_PERCENTAGE in doc)

        # check if lookalike audiences is set for the delivery job
        updated_delivery_job_doc = dpm.get_delivery_job(
            self.database, delivery_job_doc[c.ID]
        )
        self.assertTrue(
            c.DELIVERY_PLATFORM_LOOKALIKE_AUDS in updated_delivery_job_doc
        )

        # create another lookalike audience with delivery job associated with
        # source audience
        doc = dpm.create_delivery_platform_lookalike_audience(
            self.database,
            delivery_platform_id,
            source_audience_id,
            "Lookalike audience added",
            0.05,
            "US",
        )

        self.assertTrue(doc is not None)

        # check if lookalike audiences are appended in the delivery job
        updated_delivery_job_doc = dpm.get_delivery_job(
            self.database, delivery_job_doc[c.ID]
        )
        self.assertEqual(
            len(updated_delivery_job_doc[c.DELIVERY_PLATFORM_LOOKALIKE_AUDS]),
            2,
        )

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_get_all_delivery_platform_lookalike_audiences(self):
        """Test get_all_delivery_platform_lookalike_audiences ."""

        doc = dpm.create_delivery_platform_lookalike_audience(
            self.database,
            self.delivery_platform_doc[c.ID],
            self.source_audience_doc[c.ID],
            "My Lookalike audience",
            0.01,
            "US",
        )

        self.assertTrue(doc is not None)

        docs = dpm.get_all_delivery_platform_lookalike_audiences(self.database)

        self.assertTrue(docs is not None)
        self.assertEqual(len(docs), 2)

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_get_update_lookalike_audience(self):
        """Test update_lookalike_audience."""

        doc = dpm.create_delivery_platform_lookalike_audience(
            self.database,
            self.delivery_platform_doc[c.ID],
            self.source_audience_doc[c.ID],
            "New lookalike audience",
            0.01,
            "US",
        )

        self.assertTrue(doc is not None)
        self.assertTrue(c.ID in doc)
        self.assertTrue(doc[c.ID] is not None)

        lookalike_audience_id = doc[c.ID]

        doc = dpm.update_lookalike_audience(
            database=self.database,
            lookalike_audience_id=lookalike_audience_id,
            audience_size_percentage=0.03,
            country="UK",
        )

        self.assertTrue(doc is not None)
        self.assertEqual(doc[c.LOOKALIKE_AUD_SIZE_PERCENTAGE], 0.03)
        self.assertEqual(doc[c.LOOKALIKE_AUD_NAME], "New lookalike audience")
        self.assertEqual(
            doc[c.LOOKALIKE_AUD_COUNTRY],
            "UK",
        )

        doc = dpm.update_lookalike_audience_name(
            self.database,
            lookalike_audience_id,
            "New name",
        )
        self.assertTrue(doc is not None)
        self.assertTrue(c.LOOKALIKE_AUD_NAME in doc)
        self.assertEqual(doc[c.LOOKALIKE_AUD_NAME], "New name")

        doc = dpm.update_lookalike_audience_size_percentage(
            self.database,
            lookalike_audience_id,
            0.05,
        )
        self.assertTrue(doc is not None)
        self.assertTrue(c.LOOKALIKE_AUD_SIZE_PERCENTAGE in doc)
        self.assertEqual(doc[c.LOOKALIKE_AUD_SIZE_PERCENTAGE], 0.05)

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_favorite_delivery_platform(self):
        """Test favorite_delivery_platform."""

        # Test favorite functions
        doc = dpm.favorite_delivery_platform(
            self.database, self.delivery_platform_doc[c.ID]
        )

        self.assertTrue(doc is not None)
        self.assertTrue(c.FAVORITE in doc)
        self.assertTrue(doc[c.FAVORITE])

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_unfavorite_delivery_platform(self):
        """Test unfavorite_delivery_platform."""

        doc = dpm.unfavorite_delivery_platform(
            self.database, self.delivery_platform_doc[c.ID]
        )

        self.assertTrue(doc is not None)
        self.assertTrue(c.FAVORITE in doc)
        self.assertTrue(not doc[c.FAVORITE])

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_favorite_lookalike_audience(self):
        """Test favorite_lookalike_audience."""

        doc = dpm.favorite_lookalike_audience(
            self.database,
            self.lookalike_audience_doc[c.ID],
        )

        self.assertTrue(doc is not None)
        self.assertTrue(c.FAVORITE in doc)
        self.assertTrue(doc[c.FAVORITE])

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_unfavorite_lookalike_audience(self):
        """Test unfavorite_lookalike_audience."""

        doc = dpm.unfavorite_lookalike_audience(
            self.database,
            self.lookalike_audience_doc[c.ID],
        )

        self.assertTrue(doc is not None)
        self.assertTrue(c.FAVORITE in doc)
        self.assertTrue(not doc[c.FAVORITE])

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_set_get_performance_metrics(self):
        """Performance metrics are set and retrieved."""

        delivery_job_id = self._set_delivery_job()
        end_time = datetime.datetime.utcnow()
        start_time = end_time - datetime.timedelta(days=7)

        doc = dpm.set_performance_metrics(
            database=self.database,
            delivery_platform_id=ObjectId(),
            delivery_platform_name="Facebook",
            delivery_job_id=delivery_job_id,
            metrics_dict={"Clicks": 10000, "Conversions": 50},
            start_time=start_time,
            end_time=end_time,
            generic_campaign_id=self.generic_campaigns[0],
        )

        self.assertTrue(doc is not None)

        metrics_list = dpm.get_performance_metrics(
            self.database, delivery_job_id
        )

        self.assertTrue(metrics_list is not None)
        self.assertEqual(len(metrics_list), 1)

        doc = metrics_list[0]

        self.assertTrue(doc is not None)
        self.assertIn(c.DELIVERY_JOB_ID, doc)
        self.assertIn(c.METRICS_DELIVERY_PLATFORM_ID, doc)
        self.assertIn(c.METRICS_DELIVERY_PLATFORM_NAME, doc)
        self.assertIn(c.CREATE_TIME, doc)
        self.assertIn(c.PERFORMANCE_METRICS, doc)
        self.assertIn(c.METRICS_START_TIME, doc)
        self.assertIn(c.METRICS_END_TIME, doc)
        self.assertIn(c.DELIVERY_PLATFORM_GENERIC_CAMPAIGN_ID, doc)

        # Status is to be set to non-transferred automatically
        self.assertEqual(doc[c.STATUS_TRANSFERRED_FOR_FEEDBACK], False)

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_get_performance_metrics_by_engagement(self):
        """Performance metrics are set and retrieved."""

        delivery_job_id = self._set_delivery_job()
        end_time = datetime.datetime.utcnow()
        start_time = end_time - datetime.timedelta(days=7)

        doc = dpm.set_performance_metrics(
            database=self.database,
            delivery_platform_id=ObjectId(),
            delivery_platform_name="Facebook",
            delivery_job_id=delivery_job_id,
            metrics_dict={"Clicks": 10000, "Conversions": 50},
            start_time=start_time,
            end_time=end_time,
            generic_campaign_id=[{"engagement_id": "engagement_id_1"}],
        )
        self.assertTrue(doc is not None)

        metrics_list = dpm.get_performance_metrics_by_engagement_id(
            self.database, "engagement_id_1"
        )

        self.assertTrue(metrics_list is not None)
        self.assertEqual(len(metrics_list), 1)

        metrics_list = dpm.get_performance_metrics_by_engagement_id(
            self.database, "engagement_id_2"
        )

        self.assertEqual(len(metrics_list), 0)

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_set_get_performance_metrics_status(self):
        """Performance metrics status is set properly."""

        delivery_job_id = self._set_delivery_job()
        end_time = datetime.datetime.utcnow()
        start_time = end_time - datetime.timedelta(days=7)

        metrics_init_doc = dpm.set_performance_metrics(
            database=self.database,
            delivery_platform_id=ObjectId(),
            delivery_platform_name="Facebook",
            delivery_job_id=delivery_job_id,
            metrics_dict={"Clicks": 10000, "Conversions": 50},
            start_time=start_time,
            end_time=end_time,
            generic_campaign_id=self.generic_campaigns[0],
        )

        doc = dpm.set_transferred_for_feedback(
            database=self.database,
            performance_metrics_id=metrics_init_doc[c.ID],
        )
        self.assertTrue(doc[c.STATUS_TRANSFERRED_FOR_FEEDBACK])

        # Read metrics separately of setting
        metrics_list = dpm.get_performance_metrics(
            self.database, delivery_job_id
        )
        self.assertTrue(metrics_list[0][c.STATUS_TRANSFERRED_FOR_FEEDBACK])

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_get_metrics_pending_transfer_feedback(self):
        """Performance metrics pending transfer for feedback are retrieved."""

        delivery_job_id = self._set_delivery_job()
        end_time = datetime.datetime.utcnow()
        start_time = end_time - datetime.timedelta(days=7)

        metrics_doc_1 = dpm.set_performance_metrics(
            database=self.database,
            delivery_platform_id=ObjectId(),
            delivery_platform_name="Facebook",
            delivery_job_id=delivery_job_id,
            metrics_dict={"Clicks": 10000, "Conversions": 50},
            start_time=start_time,
            end_time=end_time,
            generic_campaign_id=self.generic_campaigns[0],
        )

        metrics_doc_2 = dpm.set_performance_metrics(
            database=self.database,
            delivery_platform_id=ObjectId(),
            delivery_platform_name="Facebook",
            delivery_job_id=delivery_job_id,
            metrics_dict={"Clicks": 11234, "Conversions": 150},
            start_time=start_time,
            end_time=end_time,
            generic_campaign_id=self.generic_campaigns[0],
        )

        dpm.set_transferred_for_feedback(
            database=self.database,
            performance_metrics_id=metrics_doc_2[c.ID],
        )

        metrics_list = dpm.get_performance_metrics(
            database=self.database,
            delivery_job_id=delivery_job_id,
            pending_transfer_for_feedback=True,  # only pending transfer
        )
        self.assertTrue(len(metrics_list) == 1)
        self.assertEqual(metrics_list[0][c.ID], metrics_doc_1[c.ID])

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_get_delivery_platforms_count(self):
        """Test to retrieve count of delivery platforms documents."""

        delivery_platform_id = self.delivery_platform_doc[c.ID]

        # count of delivery platforms documents
        count = dpm.get_delivery_platforms_count(database=self.database)
        self.assertEqual(count, 3)

        # count of delivery platforms documents after soft deletion
        success_flag = delete_util.delete_delivery_platform(
            self.database, delivery_platform_id
        )
        self.assertTrue(success_flag)

        count = dpm.get_delivery_platforms_count(database=self.database)
        self.assertEqual(count, 2)

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_get_lookalike_audiences_count(self):
        """Test to to retrieve count of lookalike audiences documents."""

        delivery_platform_id = self.delivery_platform_doc[c.ID]
        source_audience_id = self.source_audience_doc[c.ID]

        # Set connection status
        dpm.set_connection_status(
            self.database, delivery_platform_id, c.STATUS_SUCCEEDED
        )

        dpm.set_delivery_job(
            self.database,
            source_audience_id,
            delivery_platform_id,
            self.generic_campaigns,
        )

        # create lookalike audience
        lookalike_audience = dpm.create_delivery_platform_lookalike_audience(
            self.database,
            delivery_platform_id,
            source_audience_id,
            "Lookalike audience new",
            0.01,
            "US",
        )

        self.assertTrue(lookalike_audience is not None)

        # create another lookalike audience
        lookalike_audience_new = (
            dpm.create_delivery_platform_lookalike_audience(
                self.database,
                delivery_platform_id,
                source_audience_id,
                "Lookalike audience added",
                0.05,
                "US",
            )
        )

        self.assertTrue(lookalike_audience_new is not None)

        # count of lookalike audiences documents
        count = dpm.get_lookalike_audiences_count(database=self.database)
        self.assertEqual(count, 3)

        # count of lookalike audiences documents after soft deletion
        success_flag = delete_util.delete_lookalike_audience(
            self.database, lookalike_audience_new[c.ID]
        )
        self.assertTrue(success_flag)

        count = dpm.get_lookalike_audiences_count(database=self.database)
        self.assertEqual(count, 2)

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_set_delivery_job_for_destination(self):
        """Test set_delivery_job with engagement id."""

        # set the engagement id
        engagement_id = ObjectId()

        # set status
        self.assertIsNotNone(
            dpm.set_connection_status(
                self.database,
                self.delivery_platform_doc[c.ID],
                c.STATUS_SUCCEEDED,
            )
        )

        # set the delivery job
        doc = dpm.set_delivery_job(
            self.database,
            self.source_audience_doc[c.ID],
            self.delivery_platform_doc[c.ID],
            self.generic_campaigns,
            engagement_id,
        )

        self.assertIsNotNone(doc)
        self.assertIn(c.ID, doc)
        self.assertIsNotNone(doc[c.ID])
        self.assertIn(c.ENGAGEMENT_ID, doc)
        self.assertEqual(doc[c.ENGAGEMENT_ID], engagement_id)

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_set_multiple_delivery_jobs_for_destination(self):
        """Test set_delivery_job for multiple destinations."""

        # set the engagement id
        engagement_id = ObjectId()

        # simulate processing multiple at a time.
        for destination in [
            self.delivery_platform_doc,
            self.delivery_platform_doc_sfmc,
        ]:

            # set status
            self.assertIsNotNone(
                dpm.set_connection_status(
                    self.database,
                    destination[c.ID],
                    c.STATUS_SUCCEEDED,
                )
            )

            # set the delivery job
            doc = dpm.set_delivery_job(
                self.database,
                self.source_audience_doc[c.ID],
                destination[c.ID],
                self.generic_campaigns,
                engagement_id,
            )

            self.assertIsNotNone(doc)
            self.assertIn(c.ID, doc)
            self.assertIsNotNone(doc[c.ID])
            self.assertIn(c.ENGAGEMENT_ID, doc)
            self.assertEqual(doc[c.ENGAGEMENT_ID], engagement_id)

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_get_delivery_job_with_engagement(self):
        """Test get_delivery_job has engagement id."""

        # set engagement id
        engagement_id = ObjectId()

        # set status
        self.assertIsNotNone(
            dpm.set_connection_status(
                self.database,
                self.delivery_platform_doc[c.ID],
                c.STATUS_SUCCEEDED,
            )
        )

        # set delivery job
        doc = dpm.set_delivery_job(
            self.database,
            self.source_audience_doc[c.ID],
            self.delivery_platform_doc[c.ID],
            self.generic_campaigns,
            engagement_id,
        )

        self.assertIsNotNone(doc)

        delivery_job = dpm.get_delivery_job(
            self.database, doc[c.ID], engagement_id
        )

        self.assertIsNotNone(delivery_job)
        self.assertIn(c.AUDIENCE_ID, delivery_job)
        self.assertIn(c.CREATE_TIME, delivery_job)
        self.assertIn(c.JOB_STATUS, delivery_job)
        self.assertIn(c.DELIVERY_PLATFORM_ID, delivery_job)
        self.assertEqual(
            delivery_job[c.AUDIENCE_ID], self.source_audience_doc[c.ID]
        )
        self.assertEqual(delivery_job[c.JOB_STATUS], c.STATUS_PENDING)
        self.assertIn(c.ENGAGEMENT_ID, delivery_job)
        self.assertEqual(engagement_id, delivery_job[c.ENGAGEMENT_ID])

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_get_delivery_jobs_with_engagement(self):
        """Test get_delivery_jobs has engagement id."""

        # set engagement id
        engagement_id = ObjectId()

        for destination in [
            self.delivery_platform_doc,
            self.delivery_platform_doc_sfmc,
        ]:

            # set status
            self.assertIsNotNone(
                dpm.set_connection_status(
                    self.database,
                    destination[c.ID],
                    c.STATUS_SUCCEEDED,
                )
            )

            # set delivery job
            doc = dpm.set_delivery_job(
                self.database,
                self.source_audience_doc[c.ID],
                destination[c.ID],
                self.generic_campaigns,
                engagement_id,
            )

            self.assertIsNotNone(doc)

        delivery_jobs = dpm.get_delivery_jobs(
            self.database, self.source_audience_doc[c.ID], engagement_id
        )

        # test list
        self.assertTrue(delivery_jobs)
        self.assertEqual(2, len(delivery_jobs))

        # test all
        for delivery_job in delivery_jobs:
            self.assertIsNotNone(delivery_job)
            self.assertIn(c.AUDIENCE_ID, delivery_job)
            self.assertIn(c.CREATE_TIME, delivery_job)
            self.assertIn(c.JOB_STATUS, delivery_job)
            self.assertIn(c.DELIVERY_PLATFORM_ID, delivery_job)
            self.assertEqual(
                delivery_job[c.AUDIENCE_ID], self.source_audience_doc[c.ID]
            )
            self.assertEqual(delivery_job[c.JOB_STATUS], c.STATUS_PENDING)
            self.assertIn(c.ENGAGEMENT_ID, delivery_job)
            self.assertEqual(engagement_id, delivery_job[c.ENGAGEMENT_ID])
