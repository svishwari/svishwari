"""Delivery Platform management tests."""

import datetime
import unittest
import mongomock
from bson import ObjectId

import huxunifylib.database.delivery_platform_management as dpm
import huxunifylib.database.audience_management as am
import huxunifylib.database.data_management as dm
import huxunifylib.database.constants as db_c
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

        self.database.drop_database(db_c.DATA_MANAGEMENT_DATABASE)

        self.generic_campaigns = [
            {"campaign_id": "campaign_id_1", "ad_set_id": "ad_set_id_2"}
        ]
        self.individual_generic_campaigns = [
            {"engagement_id": "engage_id_1", "audience_id": "audience_id_1"}
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
            db_c.DELIVERY_PLATFORM_FACEBOOK,
            "My delivery platform for Facebook",
            self.auth_details_facebook,
        )

        self.delivery_platform_doc_sfmc = dpm.set_delivery_platform(
            self.database,
            db_c.DELIVERY_PLATFORM_SFMC,
            "My delivery platform for SFMC",
            self.auth_details_sfmc,
        )

        self.delivery_platform_doc_user = dpm.set_delivery_platform(
            self.database,
            db_c.DELIVERY_PLATFORM_SFMC,
            "My second delivery platform for SFMC",
            "test_user",
            self.auth_details_sfmc,
        )

        self.ingestion_job_doc = dm.set_ingestion_job(
            self.database, ObjectId()
        )

        self.source_audience_doc = am.create_audience(
            self.database,
            "My Audience",
            [],
            self.ingestion_job_doc[db_c.ID],
        )

        self.audience_2_doc = am.create_audience(
            self.database,
            "My Audience 2",
            [],
            self.ingestion_job_doc[db_c.ID],
        )

        doc = dpm.set_connection_status(
            self.database,
            self.delivery_platform_doc[db_c.ID],
            db_c.STATUS_SUCCEEDED,
        )

        self.assertTrue(doc is not None)

        self.delivery_job_doc = dpm.set_delivery_job(
            self.database,
            self.source_audience_doc[db_c.ID],
            self.delivery_platform_doc[db_c.ID],
            self.generic_campaigns,
        )

        self.delivery_job_2_doc = dpm.set_delivery_job(
            self.database,
            self.audience_2_doc[db_c.ID],
            self.delivery_platform_doc[db_c.ID],
            self.generic_campaigns,
        )

        self.lookalike_audience_doc = (
            dpm.create_delivery_platform_lookalike_audience(
                self.database,
                self.delivery_platform_doc[db_c.ID],
                self.source_audience_doc,
                "Lookalike audience",
                0.01,
                "US",
                "Kam Chancellor",
                31,
            )
        )

        doc = dpm.set_connection_status(
            self.database,
            self.delivery_platform_doc[db_c.ID],
            db_c.STATUS_PENDING,
        )

        self.assertTrue(doc is not None)

    def _set_delivery_job(self) -> ObjectId:
        """Set delivery_job.

        Returns:
            ObjectId: Delivery job ID.
        """
        dpm.set_connection_status(
            self.database,
            self.delivery_platform_doc[db_c.ID],
            db_c.STATUS_SUCCEEDED,
        )
        return dpm.set_delivery_job(
            self.database,
            self.source_audience_doc[db_c.ID],
            self.delivery_platform_doc[db_c.ID],
            self.generic_campaigns,
        )[db_c.ID]

    def test_set_delivery_platform_facebook(self):
        """Test set_delivery_platform for facebook."""

        doc = dpm.set_delivery_platform(
            self.database,
            db_c.DELIVERY_PLATFORM_FACEBOOK,
            "My delivery platform 1",
            self.auth_details_facebook,
        )

        self.assertTrue(doc is not None)
        self.assertTrue(doc[db_c.ID] is not None)
        self.assertFalse(db_c.DELETED in doc)

    def test_set_duplicate_delivery_platform_facebook(self):
        """Test set_delivery_platform for facebook."""

        doc1 = dpm.set_delivery_platform(
            self.database,
            db_c.DELIVERY_PLATFORM_FACEBOOK,
            "Test duplicate Facebook",
            self.auth_details_facebook,
        )

        self.assertIsNotNone(doc1)
        self.assertIsNotNone(doc1[db_c.ID])

        with self.assertRaises(de.DuplicateName):
            dpm.set_delivery_platform(
                self.database,
                db_c.DELIVERY_PLATFORM_FACEBOOK,
                doc1[db_c.DELIVERY_PLATFORM_NAME],
                self.auth_details_facebook,
            )

    def test_set_delivery_platform_sfmc(self):
        """Test set_delivery_platform for sfmc."""
        sfmc_configuration = {
            db_c.PERFORMANCE_METRICS_DATA_EXTENSION: "data_extension"
        }
        doc = dpm.set_delivery_platform(
            self.database,
            db_c.DELIVERY_PLATFORM_SFMC,
            "My delivery platform 2",
            self.auth_details_sfmc,
            configuration=sfmc_configuration,
        )

        self.assertIsNotNone(doc)
        self.assertIsNotNone(doc[db_c.ID])
        self.assertFalse(db_c.DELETED in doc)
        self.assertIsNotNone(doc[db_c.CONFIGURATION])

    def test_set_delivery_platform_facebook_with_user(self):
        """Test set_delivery_platform for facebook with user."""

        doc = dpm.set_delivery_platform(
            self.database,
            db_c.DELIVERY_PLATFORM_FACEBOOK,
            "My delivery platform 1",
            "user_id_or_email",
            self.auth_details_facebook,
        )

        self.assertIsNotNone(doc)
        self.assertIsNotNone(doc[db_c.ID])
        self.assertFalse(db_c.DELETED in doc)

    def test_get_deleted_delivery_platform(self):
        """Test get_deleted_delivery_platform."""

        doc = dpm.set_delivery_platform(
            self.database,
            db_c.DELIVERY_PLATFORM_FACEBOOK,
            "My delivery platform 1",
            "user_id_or_email",
            self.auth_details_facebook,
            deleted=True,
        )
        self.assertIsNone(doc)

        doc = dpm.get_delivery_platform(
            self.database, self.delivery_platform_doc[db_c.ID]
        )
        self.assertIsNotNone(doc)

        doc = dpm.get_delivery_platform_by_type(
            self.database,
            self.delivery_platform_doc[db_c.DELIVERY_PLATFORM_TYPE],
        )
        self.assertIsNotNone(doc)

        dpm.update_delivery_platform(
            database=self.database,
            delivery_platform_id=self.delivery_platform_doc[db_c.ID],
            name="Updated name",
            delivery_platform_type=db_c.DELIVERY_PLATFORM_FACEBOOK,
            deleted=True,
        )
        doc = dpm.get_delivery_platform(
            self.database, self.delivery_platform_doc[db_c.ID]
        )
        self.assertIsNone(doc)

    def test_get_delivery_platform(self):
        """Test get_delivery_platform."""

        # Get delivery platform
        doc = dpm.get_delivery_platform(
            self.database, self.delivery_platform_doc[db_c.ID]
        )

        self.assertIsNotNone(doc)
        self.assertTrue(db_c.DELIVERY_PLATFORM_NAME in doc)
        self.assertTrue(db_c.DELIVERY_PLATFORM_TYPE in doc)
        self.assertTrue(db_c.DELIVERY_PLATFORM_AUTH in doc)
        self.assertTrue(db_c.DELIVERY_PLATFORM_STATUS in doc)

        self.assertEqual(
            doc[db_c.DELIVERY_PLATFORM_NAME],
            "My delivery platform for Facebook",
        )

        self.assertEqual(
            doc[db_c.DELIVERY_PLATFORM_TYPE], db_c.DELIVERY_PLATFORM_FACEBOOK
        )

        self.assertEqual(
            doc[db_c.DELIVERY_PLATFORM_AUTH], self.auth_details_facebook
        )
        self.assertEqual(
            doc[db_c.DELIVERY_PLATFORM_STATUS], db_c.STATUS_PENDING
        )

    def test_get_delivery_platforms_by_id(self):
        """Test get_delivery_platforms list"""

        # Get delivery platform
        ids = [self.delivery_platform_doc[db_c.ID]]
        docs = dpm.get_delivery_platforms_by_id(self.database, ids)

        self.assertIsNotNone(docs[0])
        self.assertTrue(db_c.DELIVERY_PLATFORM_NAME in docs[0])
        self.assertTrue(db_c.DELIVERY_PLATFORM_TYPE in docs[0])
        self.assertTrue(db_c.DELIVERY_PLATFORM_AUTH in docs[0])
        self.assertTrue(db_c.DELIVERY_PLATFORM_STATUS in docs[0])

        self.assertEqual(
            docs[0][db_c.DELIVERY_PLATFORM_NAME],
            "My delivery platform for Facebook",
        )
        self.assertFalse([d for d in docs if db_c.DELETED in d])

    def test_get_delivery_platform_with_user(self):
        """Test get_delivery_platform."""

        # Get delivery platform
        doc = dpm.get_delivery_platform(
            self.database, self.delivery_platform_doc_user[db_c.ID]
        )

        self.assertIsNotNone(doc)
        self.assertTrue(db_c.DELIVERY_PLATFORM_NAME in doc)
        self.assertTrue(db_c.DELIVERY_PLATFORM_TYPE in doc)
        self.assertTrue(db_c.DELIVERY_PLATFORM_AUTH in doc)
        self.assertTrue(db_c.DELIVERY_PLATFORM_STATUS in doc)

        self.assertEqual(
            doc[db_c.DELIVERY_PLATFORM_NAME],
            "My second delivery platform for SFMC",
        )

        self.assertEqual(
            doc[db_c.DELIVERY_PLATFORM_TYPE], db_c.DELIVERY_PLATFORM_SFMC
        )

    def test_get_delivery_platform_sfmc(self):
        """Test get_delivery_platform for sfmc."""

        # Get delivery platform
        doc = dpm.get_delivery_platform(
            self.database, self.delivery_platform_doc_sfmc[db_c.ID]
        )

        self.assertIsNotNone(doc)
        self.assertTrue(db_c.DELIVERY_PLATFORM_NAME in doc)
        self.assertTrue(db_c.DELIVERY_PLATFORM_TYPE in doc)
        self.assertTrue(db_c.DELIVERY_PLATFORM_AUTH in doc)
        self.assertTrue(db_c.DELIVERY_PLATFORM_STATUS in doc)

        self.assertEqual(
            doc[db_c.DELIVERY_PLATFORM_NAME], "My delivery platform for SFMC"
        )

        self.assertEqual(
            doc[db_c.DELIVERY_PLATFORM_TYPE], db_c.DELIVERY_PLATFORM_SFMC
        )

        self.assertEqual(
            doc[db_c.DELIVERY_PLATFORM_AUTH], self.auth_details_sfmc
        )
        self.assertEqual(
            doc[db_c.DELIVERY_PLATFORM_STATUS], db_c.STATUS_PENDING
        )
        self.assertFalse(db_c.DELETED in doc)

    def test_get_all_delivery_platforms(self):
        """Test get_all_delivery_platforms."""

        # Get all existing delivery platforms
        platforms = dpm.get_all_delivery_platforms(self.database)

        self.assertIsNotNone(platforms)
        self.assertEqual(len(platforms), 3)
        self.assertFalse([p for p in platforms if db_c.DELETED in p])

    def test_update_doc_delivery_platform(self):
        """Test update doc delivery platform."""

        # Get delivery platform
        doc = dpm.get_delivery_platform(
            self.database, self.delivery_platform_doc[db_c.ID]
        )
        # ensure enabled is False
        self.assertFalse(doc.get(db_c.ENABLED))

        # update enabled to True
        doc = dpm.update_delivery_platform_doc(
            self.database, doc[db_c.ID], {db_c.ENABLED: True}
        )

        # ensure enabled is True
        self.assertTrue(doc.get(db_c.ENABLED))

    def test_connection_status(self):
        """Test connection status functions."""

        # Set and get connection status
        doc = dpm.set_connection_status(
            self.database,
            self.delivery_platform_doc[db_c.ID],
            db_c.STATUS_SUCCEEDED,
        )

        self.assertIsNotNone(doc)
        self.assertTrue(db_c.DELIVERY_PLATFORM_STATUS in doc)

        connection_status = dpm.get_connection_status(
            self.database,
            self.delivery_platform_doc[db_c.ID],
        )

        self.assertEqual(connection_status, db_c.STATUS_SUCCEEDED)

    def test_authentication_details(self):
        """Test set/get auth details functions."""

        new_auth_details = {
            "facebook_access_token": "path10",
            "facebook_app_secret": "path20",
            "facebook_app_id": "path30",
            "facebook_ad_account_id": "path40",
        }

        doc = dpm.set_authentication_details(
            self.database,
            self.delivery_platform_doc[db_c.ID],
            new_auth_details,
        )

        self.assertIsNotNone(doc)
        self.assertTrue(db_c.DELIVERY_PLATFORM_AUTH in doc)

        auth_details = dpm.get_authentication_details(
            self.database, self.delivery_platform_doc[db_c.ID]
        )

        self.assertEqual(auth_details, new_auth_details)

    def test_delivery_platform_name(self):
        """Test set/get delivery platform name functions."""

        # Set and get name
        new_name = "New name"

        doc = dpm.set_name(
            self.database, self.delivery_platform_doc[db_c.ID], new_name
        )

        self.assertIsNotNone(doc)
        self.assertTrue(db_c.DELIVERY_PLATFORM_NAME in doc)

        name = dpm.get_name(self.database, self.delivery_platform_doc[db_c.ID])

        self.assertEqual(name, new_name)

    def test_delivery_platform_type(self):
        """Test set/get delivery platform type functions."""

        # Set and get platform type
        new_platform_type = db_c.DELIVERY_PLATFORM_GOOGLE

        doc = dpm.set_platform_type(
            self.database,
            self.delivery_platform_doc[db_c.ID],
            new_platform_type,
        )

        self.assertIsNotNone(doc)
        self.assertTrue(db_c.DELIVERY_PLATFORM_TYPE in doc)

        platform_type = dpm.get_platform_type(
            self.database, self.delivery_platform_doc[db_c.ID]
        )

        self.assertEqual(platform_type, new_platform_type)

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
            delivery_platform_id=self.delivery_platform_doc[db_c.ID],
            name="Updated name",
            delivery_platform_type=db_c.DELIVERY_PLATFORM_FACEBOOK,
            authentication_details=new_auth_details,
        )

        self.assertIsNotNone(doc)
        self.assertTrue(db_c.DELIVERY_PLATFORM_TYPE in doc)
        self.assertTrue(db_c.DELIVERY_PLATFORM_NAME in doc)
        self.assertTrue(db_c.DELIVERY_PLATFORM_AUTH in doc)

        self.assertEqual(doc[db_c.DELIVERY_PLATFORM_NAME], "Updated name")
        self.assertEqual(
            doc[db_c.DELIVERY_PLATFORM_TYPE], db_c.DELIVERY_PLATFORM_FACEBOOK
        )
        self.assertEqual(doc[db_c.DELIVERY_PLATFORM_AUTH], new_auth_details)
        self.assertFalse(doc[db_c.ADDED])
        self.assertFalse(db_c.DELETED in doc)

        # update two fields
        doc = dpm.update_delivery_platform(
            database=self.database,
            delivery_platform_id=self.delivery_platform_doc[db_c.ID],
            name="Test name",
            delivery_platform_type=db_c.DELIVERY_PLATFORM_GOOGLE,
            added=True,
        )

        self.assertIsNotNone(doc)
        self.assertTrue(db_c.DELIVERY_PLATFORM_TYPE in doc)
        self.assertTrue(db_c.DELIVERY_PLATFORM_NAME in doc)
        self.assertTrue(db_c.DELIVERY_PLATFORM_AUTH in doc)

        self.assertEqual(doc[db_c.DELIVERY_PLATFORM_NAME], "Test name")
        self.assertEqual(
            doc[db_c.DELIVERY_PLATFORM_TYPE], db_c.DELIVERY_PLATFORM_GOOGLE
        )
        self.assertEqual(doc[db_c.DELIVERY_PLATFORM_AUTH], new_auth_details)
        self.assertTrue(doc[db_c.ADDED])

    def test_update_sfmc_performance_data_extension(self) -> None:
        """For testing update of Performance Data Extension only for SFMC"""

        performance_data_extension = {
            db_c.DELIVERY_PLATFORM_SFMC_DATA_EXT_NAME: "HUX Performance Ext",
            db_c.DELIVERY_PLATFORM_SFMC_DATA_EXT_ID: "ED-26787B1792F6",
        }

        campaign_data_extension = {
            db_c.DELIVERY_PLATFORM_SFMC_DATA_EXT_NAME: "HUX Campaign Ext",
            db_c.DELIVERY_PLATFORM_SFMC_DATA_EXT_ID: "CE-123456789012",
        }

        dpm.update_delivery_platform(
            database=self.database,
            delivery_platform_id=self.delivery_platform_doc_sfmc[db_c.ID],
            name="My delivery platform for SFMC",
            delivery_platform_type=db_c.DELIVERY_PLATFORM_SFMC,
            added=True,
            performance_de=performance_data_extension,
            campaign_de=campaign_data_extension,
        )

        get_doc = dpm.get_delivery_platform(
            database=self.database,
            delivery_platform_id=self.delivery_platform_doc_sfmc[db_c.ID],
        )

        self.assertTrue(
            get_doc[db_c.CONFIGURATION][
                db_c.PERFORMANCE_METRICS_DATA_EXTENSION
            ]
        )
        self.assertTrue(
            get_doc[db_c.CONFIGURATION][db_c.CAMPAIGN_ACTIVITY_DATA_EXTENSION]
        )

        self.assertEqual(
            get_doc[db_c.CONFIGURATION][
                db_c.PERFORMANCE_METRICS_DATA_EXTENSION
            ],
            performance_data_extension,
        )
        self.assertEqual(
            get_doc[db_c.CONFIGURATION][db_c.CAMPAIGN_ACTIVITY_DATA_EXTENSION],
            campaign_data_extension,
        )

    def test_set_delivery_job(self):
        """Test set_delivery_job."""

        doc = dpm.set_connection_status(
            self.database,
            self.delivery_platform_doc[db_c.ID],
            db_c.STATUS_SUCCEEDED,
        )

        self.assertIsNotNone(doc)

        doc = dpm.set_delivery_job(
            self.database,
            self.delivery_platform_doc[db_c.ID],
            self.delivery_platform_doc[db_c.ID],
            self.generic_campaigns,
        )

        self.assertIsNotNone(doc)
        self.assertTrue(db_c.ID in doc)
        self.assertIsNotNone(doc[db_c.ID])

    def test_get_delivery_job(self):
        """Test get_delivery_job."""

        delivery_job = dpm.get_delivery_job(
            self.database, self.delivery_job_doc[db_c.ID]
        )

        self.assertIsNotNone(delivery_job)
        self.assertTrue(db_c.AUDIENCE_ID in delivery_job)
        self.assertTrue(db_c.CREATE_TIME in delivery_job)
        self.assertTrue(db_c.JOB_STATUS in delivery_job)
        self.assertTrue(db_c.DELIVERY_PLATFORM_ID in delivery_job)
        self.assertEqual(
            delivery_job[db_c.AUDIENCE_ID], self.source_audience_doc[db_c.ID]
        )
        self.assertEqual(
            delivery_job[db_c.JOB_STATUS], db_c.AUDIENCE_STATUS_DELIVERING
        )

    def test_delivery_job_status(self):
        """Test delivery job status functions."""

        doc = dpm.set_delivery_job_status(
            self.database,
            self.delivery_job_doc[db_c.ID],
            db_c.AUDIENCE_STATUS_DELIVERED,
        )

        self.assertTrue(doc is not None)
        self.assertTrue(db_c.AUDIENCE_ID in doc)
        self.assertTrue(db_c.CREATE_TIME in doc)
        self.assertTrue(db_c.JOB_END_TIME in doc)
        self.assertTrue(db_c.JOB_STATUS in doc)
        self.assertEqual(doc[db_c.JOB_STATUS], db_c.AUDIENCE_STATUS_DELIVERED)

        status = dpm.get_delivery_job_status(
            self.database, self.delivery_job_doc[db_c.ID]
        )

        self.assertEqual(status, db_c.AUDIENCE_STATUS_DELIVERED)

    def test_delivery_job_audience_size(self):
        """Test delivery job audience size functions."""

        # Set delivery job audience size
        doc = dpm.set_delivery_job_audience_size(
            self.database,
            self.delivery_job_doc[db_c.ID],
            1000,
        )

        self.assertTrue(doc is not None)
        self.assertTrue(db_c.DELIVERY_PLATFORM_AUD_SIZE in doc)
        self.assertEqual(doc[db_c.DELIVERY_PLATFORM_AUD_SIZE], 1000)

        # Get delivery job audience size
        audience_size = dpm.get_delivery_job_audience_size(
            self.database,
            self.delivery_job_doc[db_c.ID],
        )

        self.assertTrue(audience_size is not None)
        self.assertEqual(audience_size, 1000)

    def test_get_all_delivery_jobs_filters(self):
        """Test test_get_all_delivery_jobs."""

        delivery_jobs = dpm.get_all_delivery_jobs(
            self.database,
            {
                db_c.AUDIENCE_ID: self.source_audience_doc[db_c.ID],
                db_c.JOB_STATUS: db_c.AUDIENCE_STATUS_DELIVERING,
            },
        )
        delivery_job = delivery_jobs[0] if delivery_jobs else {}

        self.assertIsNotNone(delivery_job)
        self.assertIn(db_c.AUDIENCE_ID, delivery_job)
        self.assertIn(db_c.CREATE_TIME, delivery_job)
        self.assertIn(db_c.JOB_STATUS, delivery_job)
        self.assertIn(db_c.DELIVERY_PLATFORM_ID, delivery_job)
        self.assertEqual(
            delivery_job[db_c.AUDIENCE_ID], self.source_audience_doc[db_c.ID]
        )
        self.assertEqual(
            delivery_job[db_c.STATUS], db_c.AUDIENCE_STATUS_DELIVERING
        )

    def test_get_all_delivery_jobs_sort(self):
        """Test test_get_all_delivery_job."""

        delivery_jobs = dpm.get_all_delivery_jobs(
            self.database,
            {db_c.JOB_STATUS: db_c.AUDIENCE_STATUS_DELIVERING},
            limit=5,
        )

        # test has data and limit
        self.assertTrue(delivery_jobs)
        self.assertLessEqual(len(delivery_jobs), 5)

        # test the sort order is correct. first item should be max value
        self.assertEqual(
            delivery_jobs[0][db_c.CREATE_TIME],
            max([x[db_c.CREATE_TIME] for x in delivery_jobs]),
        )

    def test_delivery_job_lookalike_audiences(self):
        """Test delivery job lookalike audiences functions."""

        # Set delivery job lookalike audiences
        lookalike_audiences = [self.lookalike_audience_doc[db_c.ID]]
        doc = dpm.set_delivery_job_lookalike_audiences(
            self.database,
            self.delivery_job_doc[db_c.ID],
            lookalike_audiences,
        )

        self.assertTrue(doc is not None)
        self.assertTrue(db_c.DELIVERY_PLATFORM_LOOKALIKE_AUDS in doc)
        self.assertEqual(
            doc[db_c.DELIVERY_PLATFORM_LOOKALIKE_AUDS], lookalike_audiences
        )

    def test_get_lookalike_audiences(self):
        """Test get lookalike audiences functions."""

        # Set delivery job lookalike audiences
        lookalike_audiences = (
            dpm.get_all_delivery_platform_lookalike_audiences(self.database)
        )

        # test that data was returned.
        self.assertTrue(lookalike_audiences)

        # get the country of the audience and filter by it
        lookalike_audience = lookalike_audiences[0]
        country_audiences = dpm.get_all_delivery_platform_lookalike_audiences(
            self.database,
            {
                db_c.LOOKALIKE_AUD_COUNTRY: lookalike_audience[
                    db_c.LOOKALIKE_AUD_COUNTRY
                ]
            },
        )

        # test audience
        self.assertTrue(country_audiences)

        # ensure the country for all returned audiences are what we filtered on
        for audience in country_audiences:
            self.assertEqual(
                lookalike_audience[db_c.LOOKALIKE_AUD_COUNTRY],
                audience[db_c.LOOKALIKE_AUD_COUNTRY],
            )

    def test_get_audience_recent_delivery_job(self):
        """Test get_audience_recent_delivery_job."""

        # Get the most recent audience delivery job ID
        most_recent_delivery = dpm.get_audience_recent_delivery_job(
            self.database,
            self.source_audience_doc[db_c.ID],
            self.delivery_platform_doc[db_c.ID],
        )

        self.assertTrue(
            self.delivery_job_doc[db_c.ID], most_recent_delivery[db_c.ID]
        )

    def test_get_delivery_jobs(self):
        """Test get_audience_delivery_job."""

        # Get all delivery jobs for an audience
        delivery_jobs = dpm.get_delivery_jobs(
            self.database,
            self.source_audience_doc[db_c.ID],
        )

        self.assertTrue(delivery_jobs is not None)
        self.assertEqual(len(delivery_jobs), 1)

    def test_get_all_delivery_jobs(self):
        """All delivery jobs are retrieved."""

        all_delivery_jobs = dpm.get_delivery_jobs(self.database)

        self.assertEqual(len(all_delivery_jobs), 2)

    def test_get_ingestion_job_audience_delivery_jobs(self):
        """Test get_ingestion_job_audience_delivery_jobs."""

        all_deliveries = dpm.get_ingestion_job_audience_delivery_jobs(
            self.database,
            self.ingestion_job_doc[db_c.ID],
        )

        self.assertTrue(all_deliveries is not None)

    def test_create_delivery_platform_lookalike_audience(self):
        """Test to create data platform lookalike audience."""

        delivery_platform_id = self.delivery_platform_doc[db_c.ID]
        source_audience_id = self.source_audience_doc[db_c.ID]

        # Set connection status
        dpm.set_connection_status(
            self.database, delivery_platform_id, db_c.STATUS_SUCCEEDED
        )

        # create lookalike audience without delivery job associated with
        # source audience
        doc = dpm.create_delivery_platform_lookalike_audience(
            self.database,
            delivery_platform_id,
            self.source_audience_doc,
            "Lookalike audience new",
            0.01,
            "US",
            "Kam Chancellor",
            31,
            db_c.AUDIENCE_STATUS_ERROR,
        )

        self.assertTrue(doc is not None)
        self.assertTrue(db_c.DELIVERY_PLATFORM_ID in doc)
        self.assertTrue(db_c.LOOKALIKE_SOURCE_AUD_ID in doc)
        self.assertTrue(db_c.LOOKALIKE_AUD_NAME in doc)
        self.assertTrue(db_c.LOOKALIKE_AUD_COUNTRY in doc)
        self.assertTrue(db_c.LOOKALIKE_AUD_SIZE_PERCENTAGE in doc)
        self.assertEqual(doc[db_c.CREATED_BY], "Kam Chancellor")
        self.assertEqual(doc[db_c.SIZE], 31)
        self.assertEqual(doc[db_c.STATUS], db_c.AUDIENCE_STATUS_ERROR)

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
            self.source_audience_doc,
            "Lookalike audience new 2",
            0.01,
            "US",
        )

        self.assertTrue(doc is not None)
        self.assertTrue(db_c.DELIVERY_PLATFORM_ID in doc)
        self.assertTrue(db_c.LOOKALIKE_SOURCE_AUD_ID in doc)
        self.assertTrue(db_c.LOOKALIKE_AUD_NAME in doc)
        self.assertTrue(db_c.LOOKALIKE_AUD_COUNTRY in doc)
        self.assertTrue(db_c.LOOKALIKE_AUD_SIZE_PERCENTAGE in doc)
        self.assertFalse(db_c.DELETED in doc)

        # check if lookalike audiences is set for the delivery job
        updated_delivery_job_doc = dpm.get_delivery_job(
            self.database, delivery_job_doc[db_c.ID]
        )
        self.assertTrue(
            db_c.DELIVERY_PLATFORM_LOOKALIKE_AUDS in updated_delivery_job_doc
        )

        # create another lookalike audience with delivery job associated with
        # source audience
        doc = dpm.create_delivery_platform_lookalike_audience(
            self.database,
            delivery_platform_id,
            self.source_audience_doc,
            "Lookalike audience added",
            0.05,
            "US",
        )

        self.assertTrue(doc is not None)
        self.assertFalse(db_c.DELETED in doc)

        # check if lookalike audiences are appended in the delivery job
        updated_delivery_job_doc = dpm.get_delivery_job(
            self.database, delivery_job_doc[db_c.ID]
        )
        self.assertEqual(
            len(
                updated_delivery_job_doc[db_c.DELIVERY_PLATFORM_LOOKALIKE_AUDS]
            ),
            2,
        )

    def test_get_all_delivery_platform_lookalike_audiences(self):
        """Test get_all_delivery_platform_lookalike_audiences ."""

        doc = dpm.create_delivery_platform_lookalike_audience(
            self.database,
            self.delivery_platform_doc[db_c.ID],
            self.source_audience_doc,
            "My Lookalike audience",
            0.01,
            "US",
        )

        self.assertTrue(doc is not None)

        docs = dpm.get_all_delivery_platform_lookalike_audiences(self.database)

        self.assertTrue(docs is not None)
        self.assertEqual(len(docs), 2)
        self.assertFalse([d for d in docs if db_c.DELETED in d])

    def test_get_update_lookalike_audience(self):
        """Test update_lookalike_audience."""

        doc = dpm.create_delivery_platform_lookalike_audience(
            self.database,
            self.delivery_platform_doc[db_c.ID],
            self.source_audience_doc,
            "New lookalike audience",
            0.01,
            "US",
        )

        self.assertTrue(doc is not None)
        self.assertTrue(db_c.ID in doc)
        self.assertTrue(doc[db_c.ID] is not None)

        lookalike_audience_id = doc[db_c.ID]

        doc = dpm.update_lookalike_audience(
            database=self.database,
            lookalike_audience_id=lookalike_audience_id,
            audience_size_percentage=0.03,
            country="UK",
            user_name="Marshawn Lynch",
            audience_size=24,
        )

        self.assertTrue(doc is not None)
        self.assertEqual(doc[db_c.LOOKALIKE_AUD_SIZE_PERCENTAGE], 0.03)
        self.assertEqual(
            doc[db_c.LOOKALIKE_AUD_NAME], "New lookalike audience"
        )
        self.assertEqual(
            doc[db_c.LOOKALIKE_AUD_COUNTRY],
            "UK",
        )
        self.assertEqual(doc[db_c.SIZE], 24)
        self.assertEqual(doc[db_c.UPDATED_BY], "Marshawn Lynch")

        doc = dpm.update_lookalike_audience_name(
            self.database,
            lookalike_audience_id,
            "New name",
        )
        self.assertTrue(doc is not None)
        self.assertTrue(db_c.LOOKALIKE_AUD_NAME in doc)
        self.assertEqual(doc[db_c.LOOKALIKE_AUD_NAME], "New name")

        doc = dpm.update_lookalike_audience_size_percentage(
            self.database,
            lookalike_audience_id,
            0.05,
        )
        self.assertTrue(doc is not None)
        self.assertTrue(db_c.LOOKALIKE_AUD_SIZE_PERCENTAGE in doc)
        self.assertEqual(doc[db_c.LOOKALIKE_AUD_SIZE_PERCENTAGE], 0.05)

    def test_favorite_delivery_platform(self):
        """Test favorite_delivery_platform."""

        # Test favorite functions
        doc = dpm.favorite_delivery_platform(
            self.database, self.delivery_platform_doc[db_c.ID]
        )

        self.assertTrue(doc is not None)
        self.assertTrue(db_c.FAVORITE in doc)
        self.assertTrue(doc[db_c.FAVORITE])

    def test_unfavorite_delivery_platform(self):
        """Test unfavorite_delivery_platform."""

        doc = dpm.unfavorite_delivery_platform(
            self.database, self.delivery_platform_doc[db_c.ID]
        )

        self.assertTrue(doc is not None)
        self.assertTrue(db_c.FAVORITE in doc)
        self.assertTrue(not doc[db_c.FAVORITE])

    def test_favorite_lookalike_audience(self):
        """Test favorite_lookalike_audience."""

        doc = dpm.favorite_lookalike_audience(
            self.database,
            self.lookalike_audience_doc[db_c.ID],
        )

        self.assertTrue(doc is not None)
        self.assertTrue(db_c.FAVORITE in doc)
        self.assertTrue(doc[db_c.FAVORITE])

    def test_unfavorite_lookalike_audience(self):
        """Test unfavorite_lookalike_audience."""

        doc = dpm.unfavorite_lookalike_audience(
            self.database,
            self.lookalike_audience_doc[db_c.ID],
        )

        self.assertTrue(doc is not None)
        self.assertTrue(db_c.FAVORITE in doc)
        self.assertTrue(not doc[db_c.FAVORITE])

    def test_set_get_performance_metrics(self):
        """Performance metrics are set and retrieved."""

        delivery_job_id = self._set_delivery_job()
        end_time = datetime.datetime.utcnow()
        start_time = end_time - datetime.timedelta(days=7)

        doc = dpm.set_performance_metrics(
            database=self.database,
            delivery_platform_id=ObjectId(),
            delivery_platform_type="facebook",
            delivery_job_id=delivery_job_id,
            metrics_dict={"Clicks": 10000, "Conversions": 50},
            start_time=start_time,
            end_time=end_time,
            generic_campaigns=self.generic_campaigns[0],
        )

        self.assertTrue(doc is not None)

        metrics_list = dpm.get_performance_metrics(
            database=self.database, delivery_job_id=delivery_job_id
        )

        self.assertTrue(metrics_list is not None)
        self.assertEqual(len(metrics_list), 1)

        doc = metrics_list[0]

        self.assertTrue(doc is not None)
        self.assertIn(db_c.DELIVERY_JOB_ID, doc)
        self.assertIn(db_c.METRICS_DELIVERY_PLATFORM_ID, doc)
        self.assertIn(db_c.METRICS_DELIVERY_PLATFORM_TYPE, doc)
        self.assertIn(db_c.CREATE_TIME, doc)
        self.assertIn(db_c.PERFORMANCE_METRICS, doc)
        self.assertIn(db_c.METRICS_START_TIME, doc)
        self.assertIn(db_c.METRICS_END_TIME, doc)
        self.assertIn(db_c.DELIVERY_PLATFORM_GENERIC_CAMPAIGNS, doc)

        # Status is to be set to non-transferred automatically
        self.assertEqual(doc[db_c.STATUS_TRANSFERRED_FOR_FEEDBACK], False)

    def test_get_performance_metrics_by_engagement(self):
        """Performance metrics are set and retrieved."""

        end_time = datetime.datetime.utcnow()
        start_time = end_time - datetime.timedelta(days=7)

        engagement_id = ObjectId()
        delivery_platform_id = self.delivery_platform_doc[db_c.ID]

        dpm.set_connection_status(
            self.database,
            self.delivery_platform_doc[db_c.ID],
            db_c.STATUS_SUCCEEDED,
        )

        doc = dpm.set_delivery_job(
            self.database,
            self.source_audience_doc[db_c.ID],
            self.delivery_platform_doc[db_c.ID],
            self.generic_campaigns,
            engagement_id=engagement_id,
        )

        dpm.set_performance_metrics(
            database=self.database,
            delivery_platform_id=delivery_platform_id,
            delivery_platform_type="facebook",
            delivery_job_id=doc[db_c.ID],
            metrics_dict={"Clicks": 10000, "Conversions": 50},
            start_time=start_time,
            end_time=end_time,
            generic_campaigns=[],
        )

        metrics_list = dpm.get_performance_metrics_by_engagement_details(
            self.database, engagement_id, [delivery_platform_id]
        )

        self.assertTrue(metrics_list is not None)
        self.assertEqual(len(metrics_list), 1)

        metrics_list = dpm.get_performance_metrics_by_engagement_details(
            self.database, ObjectId(), delivery_platform_id
        )

        self.assertIsNotNone(metrics_list)
        self.assertFalse(metrics_list)

        metrics_list = dpm.get_performance_metrics_by_engagement_details(
            self.database, engagement_id, [ObjectId()]
        )

        self.assertTrue(metrics_list is not None)
        self.assertEqual(len(metrics_list), 0)

    def test_set_get_performance_metrics_status(self):
        """Performance metrics status is set properly."""

        delivery_job_id = self._set_delivery_job()
        end_time = datetime.datetime.utcnow()
        start_time = end_time - datetime.timedelta(days=7)

        metrics_init_doc = dpm.set_performance_metrics(
            database=self.database,
            delivery_platform_id=ObjectId(),
            delivery_platform_type="facebook",
            delivery_job_id=delivery_job_id,
            metrics_dict={"Clicks": 10000, "Conversions": 50},
            start_time=start_time,
            end_time=end_time,
            generic_campaigns=self.generic_campaigns[0],
        )

        doc = dpm.set_metrics_transferred_for_feedback(
            database=self.database,
            performance_metrics_id=metrics_init_doc[db_c.ID],
        )
        self.assertTrue(doc[db_c.STATUS_TRANSFERRED_FOR_FEEDBACK])

        # Read metrics separately of setting
        metrics_list = dpm.get_performance_metrics(
            database=self.database, delivery_job_id=delivery_job_id
        )
        self.assertTrue(metrics_list[0][db_c.STATUS_TRANSFERRED_FOR_FEEDBACK])

    def test_get_metrics_pending_transfer_feedback(self):
        """Performance metrics pending transfer for feedback are retrieved."""

        delivery_job_id = self._set_delivery_job()
        end_time = datetime.datetime.utcnow()
        start_time = end_time - datetime.timedelta(days=7)

        metrics_doc_1 = dpm.set_performance_metrics(
            database=self.database,
            delivery_platform_id=ObjectId(),
            delivery_platform_type="facebook",
            delivery_job_id=delivery_job_id,
            metrics_dict={"Clicks": 10000, "Conversions": 50},
            start_time=start_time,
            end_time=end_time,
            generic_campaigns=self.generic_campaigns[0],
        )

        metrics_doc_2 = dpm.set_performance_metrics(
            database=self.database,
            delivery_platform_id=ObjectId(),
            delivery_platform_type="facebook",
            delivery_job_id=delivery_job_id,
            metrics_dict={"Clicks": 11234, "Conversions": 150},
            start_time=start_time,
            end_time=end_time,
            generic_campaigns=self.generic_campaigns[0],
        )

        dpm.set_metrics_transferred_for_feedback(
            database=self.database,
            performance_metrics_id=metrics_doc_2[db_c.ID],
        )

        metrics_list = dpm.get_performance_metrics(
            database=self.database,
            delivery_job_id=delivery_job_id,
            pending_transfer_for_feedback=True,  # only pending transfer
        )
        self.assertTrue(len(metrics_list) == 1)
        self.assertEqual(metrics_list[0][db_c.ID], metrics_doc_1[db_c.ID])

    def test_get_delivery_platforms_count(self):
        """Test to retrieve count of delivery platforms documents."""

        delivery_platform_id = self.delivery_platform_doc[db_c.ID]

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

    def test_get_lookalike_audiences_count(self):
        """Test to to retrieve count of lookalike audiences documents."""

        delivery_platform_id = self.delivery_platform_doc[db_c.ID]
        source_audience_id = self.source_audience_doc[db_c.ID]

        # Set connection status
        dpm.set_connection_status(
            self.database, delivery_platform_id, db_c.STATUS_SUCCEEDED
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
            self.source_audience_doc,
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
                self.source_audience_doc,
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
            self.database, lookalike_audience_new[db_c.ID]
        )
        self.assertTrue(success_flag)

        count = dpm.get_lookalike_audiences_count(database=self.database)
        self.assertEqual(count, 2)

    def test_set_delivery_job_for_destination(self):
        """Test set_delivery_job with engagement id."""

        # set the engagement id
        engagement_id = ObjectId()

        # set status
        self.assertIsNotNone(
            dpm.set_connection_status(
                self.database,
                self.delivery_platform_doc[db_c.ID],
                db_c.STATUS_SUCCEEDED,
            )
        )

        # set the delivery job
        doc = dpm.set_delivery_job(
            self.database,
            self.source_audience_doc[db_c.ID],
            self.delivery_platform_doc[db_c.ID],
            self.generic_campaigns,
            engagement_id,
        )

        self.assertIsNotNone(doc)
        self.assertIn(db_c.ID, doc)
        self.assertIsNotNone(doc[db_c.ID])
        self.assertIn(db_c.ENGAGEMENT_ID, doc)
        self.assertEqual(doc[db_c.ENGAGEMENT_ID], engagement_id)

    def test_set_delivery_job_for_destination_with_config(self):
        """Test set_delivery_job with the config"""

        # set the engagement id
        engagement_id = ObjectId()

        # set status
        self.assertIsNotNone(
            dpm.set_connection_status(
                self.database,
                self.delivery_platform_doc[db_c.ID],
                db_c.STATUS_SUCCEEDED,
            )
        )

        delivery_config = {
            db_c.DELIVERY_PLATFORM_SFMC_DATA_EXT_NAME: "Test SFMC"
        }

        # set the delivery job
        # pylint: disable=E1121
        doc = dpm.set_delivery_job(
            self.database,
            self.source_audience_doc[db_c.ID],
            self.delivery_platform_doc[db_c.ID],
            self.generic_campaigns,
            engagement_id,
            delivery_config,
        )

        self.assertIsNotNone(doc)
        self.assertIn(db_c.ID, doc)
        self.assertIsNotNone(doc[db_c.ID])
        self.assertIn(db_c.ENGAGEMENT_ID, doc)
        self.assertEqual(doc[db_c.ENGAGEMENT_ID], engagement_id)

        # check the delivery config was set
        self.assertIn(db_c.DELIVERY_PLATFORM_CONFIG, doc)
        self.assertDictEqual(
            doc[db_c.DELIVERY_PLATFORM_CONFIG], delivery_config
        )

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
                    destination[db_c.ID],
                    db_c.STATUS_SUCCEEDED,
                )
            )

            # set the delivery job
            doc = dpm.set_delivery_job(
                self.database,
                self.source_audience_doc[db_c.ID],
                destination[db_c.ID],
                self.generic_campaigns,
                engagement_id,
            )

            self.assertIsNotNone(doc)
            self.assertIn(db_c.ID, doc)
            self.assertIsNotNone(doc[db_c.ID])
            self.assertIn(db_c.ENGAGEMENT_ID, doc)
            self.assertEqual(doc[db_c.ENGAGEMENT_ID], engagement_id)

    def test_get_delivery_job_with_engagement(self):
        """Test get_delivery_job has engagement id."""

        # set engagement id
        engagement_id = ObjectId()

        # set status
        self.assertIsNotNone(
            dpm.set_connection_status(
                self.database,
                self.delivery_platform_doc[db_c.ID],
                db_c.STATUS_SUCCEEDED,
            )
        )

        # set delivery job
        doc = dpm.set_delivery_job(
            self.database,
            self.source_audience_doc[db_c.ID],
            self.delivery_platform_doc[db_c.ID],
            self.generic_campaigns,
            engagement_id,
        )

        self.assertIsNotNone(doc)

        delivery_job = dpm.get_delivery_job(
            self.database, doc[db_c.ID], engagement_id
        )

        self.assertIsNotNone(delivery_job)
        self.assertIn(db_c.AUDIENCE_ID, delivery_job)
        self.assertIn(db_c.CREATE_TIME, delivery_job)
        self.assertIn(db_c.JOB_STATUS, delivery_job)
        self.assertIn(db_c.DELIVERY_PLATFORM_ID, delivery_job)
        self.assertEqual(
            delivery_job[db_c.AUDIENCE_ID], self.source_audience_doc[db_c.ID]
        )
        self.assertEqual(
            delivery_job[db_c.JOB_STATUS], db_c.AUDIENCE_STATUS_DELIVERING
        )
        self.assertIn(db_c.ENGAGEMENT_ID, delivery_job)
        self.assertEqual(engagement_id, delivery_job[db_c.ENGAGEMENT_ID])
        self.assertFalse(db_c.DELETED in delivery_job)

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
                    destination[db_c.ID],
                    db_c.STATUS_SUCCEEDED,
                )
            )

            # set delivery job
            doc = dpm.set_delivery_job(
                self.database,
                self.source_audience_doc[db_c.ID],
                destination[db_c.ID],
                self.generic_campaigns,
                engagement_id,
            )

            self.assertIsNotNone(doc)

        delivery_jobs = dpm.get_delivery_jobs(
            self.database, self.source_audience_doc[db_c.ID], engagement_id
        )

        # test list
        self.assertTrue(delivery_jobs)
        self.assertEqual(2, len(delivery_jobs))

        # test all
        for delivery_job in delivery_jobs:
            self.assertIsNotNone(delivery_job)
            self.assertIn(db_c.AUDIENCE_ID, delivery_job)
            self.assertIn(db_c.CREATE_TIME, delivery_job)
            self.assertIn(db_c.JOB_STATUS, delivery_job)
            self.assertIn(db_c.DELIVERY_PLATFORM_ID, delivery_job)
            self.assertEqual(
                delivery_job[db_c.AUDIENCE_ID],
                self.source_audience_doc[db_c.ID],
            )
            self.assertEqual(
                delivery_job[db_c.JOB_STATUS], db_c.AUDIENCE_STATUS_DELIVERING
            )
            self.assertIn(db_c.ENGAGEMENT_ID, delivery_job)
            self.assertEqual(engagement_id, delivery_job[db_c.ENGAGEMENT_ID])

    def test_set_get_campaign_activity(self):
        """Campaign Activity docs are set and retrieved."""

        delivery_job_id = self._set_delivery_job()
        event_details = {
            "event": "sent",
            "event_date": "2021-06-17T12:21:27.970Z",
        }

        doc = dpm.set_campaign_activity(
            database=self.database,
            delivery_platform_id=ObjectId(),
            delivery_platform_type=db_c.DELIVERY_PLATFORM_SFMC,
            delivery_job_id=delivery_job_id,
            event_details=event_details,
            generic_campaigns=self.individual_generic_campaigns[0],
        )

        self.assertIsNotNone(doc)

        events_list = dpm.get_campaign_activity(
            database=self.database, delivery_job_id=delivery_job_id
        )

        self.assertIsNotNone(events_list)
        self.assertEqual(len(events_list), 1)

        doc = events_list[0]

        self.assertIsNotNone(doc)
        self.assertIn(db_c.DELIVERY_JOB_ID, doc)
        self.assertIn(db_c.METRICS_DELIVERY_PLATFORM_ID, doc)
        self.assertIn(db_c.METRICS_DELIVERY_PLATFORM_TYPE, doc)
        self.assertIn(db_c.CREATE_TIME, doc)
        self.assertIn(db_c.EVENT_DETAILS, doc)
        self.assertEqual(doc[db_c.EVENT_DETAILS]["event"], "sent")
        self.assertEqual(
            doc[db_c.EVENT_DETAILS]["event_date"], "2021-06-17T12:21:27.970Z"
        )
        self.assertIn(db_c.DELIVERY_PLATFORM_GENERIC_CAMPAIGNS, doc)

        # Status is to be set to non-transferred automatically
        self.assertFalse(doc[db_c.STATUS_TRANSFERRED_FOR_FEEDBACK])

    def test_create_delivery_job_generic_campaigns(self):
        """Campaigns are set and retrieved."""

        engagement_id = ObjectId()

        dpm.set_connection_status(
            self.database,
            self.delivery_platform_doc[db_c.ID],
            db_c.STATUS_SUCCEEDED,
        )

        doc = dpm.set_delivery_job(
            self.database,
            self.source_audience_doc[db_c.ID],
            self.delivery_platform_doc[db_c.ID],
            self.generic_campaigns,
            engagement_id=engagement_id,
        )

        updated_doc = dpm.create_delivery_job_generic_campaigns(
            self.database, doc[db_c.ID], self.generic_campaigns
        )

        self.assertIsNotNone(updated_doc)
        self.assertEqual(
            len(updated_doc[db_c.DELIVERY_PLATFORM_GENERIC_CAMPAIGNS]), 1
        )

    def test_get_delivery_job_engagement_detail(self):
        """Delivery job is set with engagement/audience id and retrieved."""

        engagement_id = ObjectId()

        dpm.set_connection_status(
            self.database,
            self.delivery_platform_doc[db_c.ID],
            db_c.STATUS_SUCCEEDED,
        )

        doc = dpm.set_delivery_job(
            self.database,
            self.source_audience_doc[db_c.ID],
            self.delivery_platform_doc[db_c.ID],
            self.generic_campaigns,
            engagement_id=engagement_id,
        )
        self.assertIsNotNone(doc)

        delivery_jobs = dpm.get_delivery_jobs_using_metadata(
            self.database,
            engagement_id,
            self.source_audience_doc[db_c.ID],
            self.delivery_platform_doc[db_c.ID],
            audience_ids=[
                self.source_audience_doc[db_c.ID],
                self.audience_2_doc[db_c.ID],
            ],
        )

        self.assertIsNotNone(delivery_jobs)
        self.assertEqual(1, len(delivery_jobs))
        self.assertIn(db_c.ENGAGEMENT_ID, delivery_jobs[0])
        self.assertEqual(engagement_id, delivery_jobs[0][db_c.ENGAGEMENT_ID])

        self.assertIn(db_c.AUDIENCE_ID, delivery_jobs[0])
        self.assertEqual(
            self.source_audience_doc[db_c.ID],
            delivery_jobs[0][db_c.AUDIENCE_ID],
        )

        self.assertIn(db_c.DELIVERY_PLATFORM_ID, delivery_jobs[0])
        self.assertEqual(
            self.delivery_platform_doc[db_c.ID],
            delivery_jobs[0][db_c.DELIVERY_PLATFORM_ID],
        )

    def test_delete_delivery_job_generic_campaigns(self):
        """Generic campaigns are set and deleted."""

        engagement_id = ObjectId()

        dpm.set_connection_status(
            self.database,
            self.delivery_platform_doc[db_c.ID],
            db_c.STATUS_SUCCEEDED,
        )

        doc = dpm.set_delivery_job(
            self.database,
            self.source_audience_doc[db_c.ID],
            self.delivery_platform_doc[db_c.ID],
            self.generic_campaigns,
            engagement_id=engagement_id,
        )

        self.assertIsNotNone(doc)
        self.assertEqual(len(doc[db_c.DELIVERY_PLATFORM_GENERIC_CAMPAIGNS]), 1)

        count = dpm.delete_delivery_job_generic_campaigns(
            self.database, [doc[db_c.ID]]
        )
        self.assertEqual(count, 1)

        doc = dpm.get_delivery_job(self.database, doc[db_c.ID])

        self.assertIsNotNone(doc)
        self.assertFalse(doc[db_c.DELIVERY_PLATFORM_GENERIC_CAMPAIGNS])

    def test_set_get_campaign_activities(self):
        """Campaign Activity batch docs are set and retrieved."""

        delivery_job_id = self._set_delivery_job()
        campaign_activity_docs = [
            {
                "event_details": {
                    "subscriber_key": "1001",
                    "event_type": "click",
                    "event_date": "6/27/2021 12:00:00 AM",
                    "url": "https://google.com",
                },
                "name": "My SFMC delivery platform",
                "delivery_job_id": delivery_job_id,
            },
            {
                "event_details": {
                    "subscriber_key": "1001",
                    "event_type": "sent",
                    "event_date": "6/27/2021 12:00:00 AM",
                },
                "name": "My SFMC delivery platform",
                "delivery_job_id": delivery_job_id,
            },
        ]

        status = dpm.set_campaign_activities(
            database=self.database,
            performance_metric_docs=campaign_activity_docs,
        )

        self.assertTrue(status)

        campaign_activity_doc_list = dpm.get_campaign_activity(
            database=self.database, delivery_job_id=delivery_job_id
        )

        self.assertIsNotNone(campaign_activity_doc_list)
        self.assertEqual(len(campaign_activity_doc_list), 2)

        doc1 = campaign_activity_doc_list[0]
        doc2 = campaign_activity_doc_list[1]

        self.assertIsNotNone(doc1)
        self.assertIsNotNone(doc2)

        self.assertEqual(doc1[db_c.EVENT_DETAILS]["event_type"], "click")
        self.assertEqual(doc1[db_c.EVENT_DETAILS]["subscriber_key"], "1001")
        self.assertEqual(doc2[db_c.EVENT_DETAILS]["event_type"], "sent")
        self.assertEqual(doc2[db_c.EVENT_DETAILS]["subscriber_key"], "1001")

    def test_get_all_feedback_campaign_activities(self):
        """Campaign Activity docs are set and feedback false documents are retrieved."""

        delivery_job_id = self._set_delivery_job()
        campaign_activity_docs = [
            {
                "event_details": {
                    "subscriber_key": "1001",
                    "event_type": "click",
                    "event_date": "6/27/2021 12:00:00 AM",
                    "url": "https://google.com",
                },
                "name": "My SFMC delivery platform",
                "delivery_job_id": delivery_job_id,
                "transferred_for_feedback": True,
            },
            {
                "event_details": {
                    "subscriber_key": "1001",
                    "event_type": "sent",
                    "event_date": "6/27/2021 12:00:00 AM",
                },
                "name": "My SFMC delivery platform",
                "delivery_job_id": delivery_job_id,
                "transferred_for_feedback": False,
            },
            {
                "event_details": {
                    "subscriber_key": "1001",
                    "event_type": "open",
                    "event_date": "6/27/2021 12:00:00 AM",
                },
                "name": "My SFMC delivery platform",
                "delivery_job_id": delivery_job_id,
                "transferred_for_feedback": False,
            },
        ]

        status = dpm.set_campaign_activities(
            database=self.database,
            performance_metric_docs=campaign_activity_docs,
        )

        self.assertTrue(status)

        campaign_activity_doc_list = dpm.get_all_campaign_activities(
            self.database, pending_transfer_for_feedback=True
        )

        self.assertIsNotNone(campaign_activity_doc_list)
        self.assertEqual(len(campaign_activity_doc_list), 2)

        doc1 = campaign_activity_doc_list[0]
        doc2 = campaign_activity_doc_list[1]

        self.assertIsNotNone(doc1)
        self.assertIsNotNone(doc2)
        self.assertIn(db_c.EVENT_DETAILS, doc1)
        self.assertIn(db_c.EVENT_DETAILS, doc1)

        self.assertFalse(doc1[db_c.STATUS_TRANSFERRED_FOR_FEEDBACK])
        self.assertFalse(doc2[db_c.STATUS_TRANSFERRED_FOR_FEEDBACK])

    def test_set_get_campaign_activity_status(self):
        """Campaign Activity Feedback status is set properly."""

        delivery_job_id = self._set_delivery_job()
        event_details = {
            "event": "sent",
            "event_date": "2021-06-17T12:21:27.970Z",
        }

        doc = dpm.set_campaign_activity(
            database=self.database,
            delivery_platform_id=ObjectId(),
            delivery_platform_type=db_c.DELIVERY_PLATFORM_SFMC,
            delivery_job_id=delivery_job_id,
            event_details=event_details,
            generic_campaigns=self.individual_generic_campaigns[0],
        )

        doc = dpm.set_campaign_activity_transferred_for_feedback(
            database=self.database,
            performance_metrics_id=doc[db_c.ID],
        )
        self.assertTrue(doc[db_c.STATUS_TRANSFERRED_FOR_FEEDBACK])

        # Read activities separately of setting
        campaign_activities_list = dpm.get_campaign_activity(
            database=self.database, delivery_job_id=delivery_job_id
        )
        self.assertTrue(
            campaign_activities_list[0][db_c.STATUS_TRANSFERRED_FOR_FEEDBACK]
        )

    def test_set_audience_customers(self):
        """Audience customers are set properly."""

        customer_list = [
            "customer_id_1",
            "customer_id_2",
            "customer_id_3",
            "customer_id_4",
            "customer_id_5",
        ]

        doc = dpm.set_audience_customers(
            database=self.database,
            delivery_job_id=self.delivery_job_doc[db_c.ID],
            customer_list=customer_list,
        )

        self.assertIsNotNone(doc)
        self.assertEqual(doc[db_c.AUDIENCE_CUSTOMER_LIST], customer_list)

    def test_get_all_audience_customers(self):
        """All audience customers are fetched properly."""

        customer_list_1 = [
            "customer_id_1",
            "customer_id_2",
            "customer_id_3",
            "customer_id_4",
            "customer_id_5",
        ]

        customer_list_2 = [
            "customer_id_10",
            "customer_id_20",
            "customer_id_30",
            "customer_id_40",
            "customer_id_50",
        ]

        # set 2 customer audience docs with `delivery_job_doc`
        doc = dpm.set_audience_customers(
            database=self.database,
            delivery_job_id=self.delivery_job_doc[db_c.ID],
            customer_list=customer_list_1,
        )
        self.assertIsNotNone(doc)

        doc = dpm.set_audience_customers(
            database=self.database,
            delivery_job_id=self.delivery_job_doc[db_c.ID],
            customer_list=customer_list_2,
        )
        self.assertIsNotNone(doc)

        # set a customer audience doc with `delivery_job_2_doc`
        doc = dpm.set_audience_customers(
            database=self.database,
            delivery_job_id=self.delivery_job_2_doc[db_c.ID],
            customer_list=customer_list_2,
        )
        self.assertIsNotNone(doc)

        # fetch customer audience doc for `delivery_job_doc`
        all_docs = list(
            dpm.get_all_audience_customers(
                database=self.database,
                delivery_job_id=self.delivery_job_doc[db_c.ID],
            )
        )

        self.assertIsNotNone(all_docs)
        self.assertEqual(len(all_docs), 2)

    def test_set_get_performance_metrics_bulk(self):
        """Bulk Performance Metrics docs are set and most
        recent metric is retrieved."""

        delivery_job_id = self._set_delivery_job()
        performance_metrics_docs = [
            {
                "delivery_platform_name": "sfmc",
                "delivery_job_id": delivery_job_id,
                "create_time": datetime.datetime(
                    2021, 6, 26, 14, 4, 15, 369000
                ),
                "start_time": datetime.datetime(2021, 6, 25, 0, 0),
                "end_time": datetime.datetime(2021, 6, 26, 0, 0),
                "delivery_platform_generic_campaigns": {
                    "engagement_id": "Pro18",
                    "audience_id": "Aud2",
                    "data_extension_id": "D2988EE7-3AEB-40F5-82A4-DC49A473AAA4",
                },
                "performance_metrics": {
                    "journey_id": "6A1D3452-4DF9-40C3-B02A-65876C413115",
                    "journey_name": "Journey Demo I",
                    "journey_creation_date": "2021-05-20 05:23:00",
                    "hux_engagement_id": "Pro18",
                    "hux_audience_id": "Aud2",
                    "delivered": "0",
                    "opens": "9",
                    "unique_opens": "3",
                    "clicks": "7",
                    "unique_clicks": "7",
                    "unsubscribes": "0",
                    "hard_bounces": "0",
                    "bounces": "0",
                    "sent": "0",
                },
                "transferred_for_feedback": False,
            },
            {
                "delivery_platform_name": "sfmc",
                "delivery_job_id": delivery_job_id,
                "create_time": datetime.datetime(
                    2021, 6, 25, 14, 4, 15, 369000
                ),
                "start_time": datetime.datetime(2021, 6, 24, 0, 0),
                "end_time": datetime.datetime(2021, 6, 25, 0, 0),
                "delivery_platform_generic_campaigns": {
                    "engagement_id": "Pro18",
                    "audience_id": "Aud2",
                    "data_extension_id": "D2988EE7-3AEB-40F5-82A4-DC49A473AAA4",
                },
                "performance_metrics": {
                    "journey_id": "6A1D3452-4DF9-40C3-B02A-65876C413115",
                    "journey_name": "Journey Demo I",
                    "journey_creation_date": "2021-05-20 05:23:00",
                    "hux_engagement_id": "Pro18",
                    "hux_audience_id": "Aud2",
                    "delivered": "50",
                    "opens": "10",
                    "unique_opens": "1",
                    "clicks": "0",
                    "unique_clicks": "0",
                    "unsubscribes": "0",
                    "hard_bounces": "5",
                    "bounces": "10",
                    "sent": "60",
                },
                "transferred_for_feedback": True,
            },
        ]

        status = dpm.set_performance_metrics_bulk(
            database=self.database,
            performance_metric_docs=performance_metrics_docs,
        )
        self.assertTrue(status["insert_status"])

        performance_metrics_docs_list = dpm.get_performance_metrics(
            database=self.database, delivery_job_id=delivery_job_id
        )
        self.assertIsNotNone(performance_metrics_docs_list)
        self.assertEqual(len(performance_metrics_docs_list), 2)

        doc1 = performance_metrics_docs_list[0]
        doc2 = performance_metrics_docs_list[1]

        self.assertIsNotNone(doc1)
        self.assertIsNotNone(doc2)

        recent_performance_metrics_doc = (
            dpm.get_most_recent_performance_metric_by_delivery_job(
                self.database, delivery_job_id
            )
        )
        self.assertIsNotNone(recent_performance_metrics_doc)

        self.assertEqual(
            recent_performance_metrics_doc[db_c.JOB_END_TIME],
            datetime.datetime(2021, 6, 26, 0, 0),
        )

    def test_get_most_recent_campaign_activity_by_delivery_job(self):
        """Campaign Activity batch docs are set and
        latest campaign activity event is retrieved."""

        delivery_job_id = self._set_delivery_job()
        campaign_activity_docs = [
            {
                "event_details": {
                    "subscriber_key": "1001",
                    "event_type": "click",
                    "event_date": datetime.datetime(2021, 6, 28, 0, 0),
                    "url": "https://google.com",
                },
                "name": "My SFMC delivery platform",
                "delivery_job_id": delivery_job_id,
            },
            {
                "event_details": {
                    "subscriber_key": "1001",
                    "event_type": "sent",
                    "event_date": datetime.datetime(2021, 6, 27, 0, 0),
                },
                "name": "My SFMC delivery platform",
                "delivery_job_id": delivery_job_id,
            },
        ]

        status = dpm.set_campaign_activities(
            database=self.database,
            performance_metric_docs=campaign_activity_docs,
        )

        self.assertTrue(status)

        recent_campaign_activity_doc = (
            dpm.get_most_recent_campaign_activity_by_delivery_job(
                self.database, delivery_job_id
            )
        )

        self.assertIsNotNone(recent_campaign_activity_doc)

        self.assertEqual(
            recent_campaign_activity_doc[db_c.EVENT_DETAILS][db_c.EVENT_DATE],
            datetime.datetime(2021, 6, 28, 0, 0),
        )

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_update_pending_delivery_jobs(self):
        """Test update delivery jobs status."""
        updated_delivery_jobs = dpm.update_pending_delivery_jobs(self.database)
        self.assertEqual(updated_delivery_jobs, 0)
