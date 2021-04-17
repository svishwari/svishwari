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


# pylint: disable=R0904
class TestDeliveryPlatform(unittest.TestCase):
    """Test delivery platform management module."""

    @mongomock.patch(servers=(("localhost", 27017),))
    def setUp(self):

        # Connect
        self.database = DatabaseClient(
            "localhost", 27017, None, None
        ).connect()

        self.database.drop_database(c.DATA_MANAGEMENT_DATABASE)

        # Set delivery platform
        self.auth_details = {
            "facebook_access_token": "path1",
            "facebook_app_secret": "path2",
            "facebook_app_id": "path3",
            "facebook_ad_account_id": "path4",
        }

        self.delivery_platform_doc = dpm.set_delivery_platform(
            self.database,
            c.DELIVERY_PLATFORM_FACEBOOK,
            "My delivery platform",
            self.auth_details,
        )

        self.ingestion_job_doc = dm.set_ingestion_job(
            self.database, ObjectId("5dff99c10345af022f219bbf")
        )

        self.source_audience_doc = am.create_audience(
            self.database,
            self.ingestion_job_doc[c.ID],
            "My Audience",
            [],
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

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_set_delivery_platform(self):
        """Test set_delivery_platform."""

        doc = dpm.set_delivery_platform(
            self.database,
            c.DELIVERY_PLATFORM_FACEBOOK,
            "My delivery platform 1",
            self.auth_details,
        )

        self.assertTrue(doc is not None)
        self.assertTrue(doc[c.ID] is not None)

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_get_delivery_platform(self):
        """Test get_delivery_platform."""

        # Get delivery platform
        doc = dpm.get_delivery_platform(
            self.database, self.delivery_platform_doc[c.ID]
        )

        self.assertTrue(doc is not None)
        self.assertTrue(c.DELIVERY_PLATFORM_NAME in doc)
        self.assertTrue(c.DELIVERY_PLATFORM_TYPE in doc)
        self.assertTrue(c.DELIVERY_PLATFORM_AUTH in doc)
        self.assertTrue(c.DELIVERY_PLATFORM_STATUS in doc)

        self.assertEqual(doc[c.DELIVERY_PLATFORM_NAME], "My delivery platform")

        self.assertEqual(
            doc[c.DELIVERY_PLATFORM_TYPE], c.DELIVERY_PLATFORM_FACEBOOK
        )

        self.assertEqual(doc[c.DELIVERY_PLATFORM_AUTH], self.auth_details)
        self.assertEqual(doc[c.DELIVERY_PLATFORM_STATUS], c.STATUS_PENDING)

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_get_all_delivery_platforms(self):
        """Test get_all_delivery_platforms."""

        # Get all existing delivery platforms
        platforms = dpm.get_all_delivery_platforms(self.database)

        self.assertTrue(platforms is not None)
        self.assertEqual(len(platforms), 1)

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_connection_status(self):
        """Test connection status functions."""

        # Set and get connection status
        doc = dpm.set_connection_status(
            self.database,
            self.delivery_platform_doc[c.ID],
            c.STATUS_SUCCEEDED,
        )

        self.assertTrue(doc is not None)
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

        self.assertTrue(doc is not None)
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

        self.assertTrue(doc is not None)
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

        self.assertTrue(doc is not None)
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

        self.assertTrue(doc is not None)
        self.assertTrue(c.DELIVERY_PLATFORM_TYPE in doc)
        self.assertTrue(c.DELIVERY_PLATFORM_NAME in doc)
        self.assertTrue(c.DELIVERY_PLATFORM_AUTH in doc)

        self.assertEqual(doc[c.DELIVERY_PLATFORM_NAME], "Updated name")
        self.assertEqual(
            doc[c.DELIVERY_PLATFORM_TYPE], c.DELIVERY_PLATFORM_FACEBOOK
        )
        self.assertEqual(doc[c.DELIVERY_PLATFORM_AUTH], new_auth_details)

        # update two fields
        doc = dpm.update_delivery_platform(
            database=self.database,
            delivery_platform_id=self.delivery_platform_doc[c.ID],
            name="Test name",
            delivery_platform_type=c.DELIVERY_PLATFORM_GOOGLE,
        )

        self.assertTrue(doc is not None)
        self.assertTrue(c.DELIVERY_PLATFORM_TYPE in doc)
        self.assertTrue(c.DELIVERY_PLATFORM_NAME in doc)
        self.assertTrue(c.DELIVERY_PLATFORM_AUTH in doc)

        self.assertEqual(doc[c.DELIVERY_PLATFORM_NAME], "Test name")
        self.assertEqual(
            doc[c.DELIVERY_PLATFORM_TYPE], c.DELIVERY_PLATFORM_GOOGLE
        )
        self.assertEqual(doc[c.DELIVERY_PLATFORM_AUTH], new_auth_details)

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_set_delivery_job(self):
        """Test set_delivery_job."""

        doc = dpm.set_connection_status(
            self.database,
            self.delivery_platform_doc[c.ID],
            c.STATUS_SUCCEEDED,
        )

        self.assertTrue(doc is not None)

        doc = dpm.set_delivery_job(
            self.database,
            self.delivery_platform_doc[c.ID],
            self.delivery_platform_doc[c.ID],
        )

        self.assertTrue(doc is not None)
        self.assertTrue(c.ID in doc)
        self.assertTrue(doc[c.ID] is not None)

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_get_delivery_job(self):
        """Test get_delivery_job."""

        delivery_job = dpm.get_delivery_job(
            self.database, self.delivery_job_doc[c.ID]
        )

        self.assertTrue(delivery_job is not None)
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

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_get_audience_delivery_jobs(self):
        """Test get_audience_delivery_job."""

        # Get all delivery jobs for an audience
        delivery_jobs = dpm.get_audience_delivery_jobs(
            self.database,
            self.source_audience_doc[c.ID],
        )

        self.assertTrue(delivery_jobs is not None)
        self.assertEqual(len(delivery_jobs), 1)

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
            self.database, source_audience_id, delivery_platform_id
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

    def test_metrics(self):
        """Test performance metrics functions."""

        self.assertTrue(self.database is not None)

        delivery_job_id = self.delivery_job_doc[c.ID]

        end_time = datetime.datetime.utcnow()
        start_time = end_time - datetime.timedelta(days=7)

        doc = dpm.set_delivered_audience_performance_metrics(
            database=self.database,
            delivery_job_id=delivery_job_id,
            metrics_dict={"Clicks": 10000, "Conversions": 50},
            start_time=start_time,
            end_time=end_time,
            delivery_platform_ad_sets=[
                ("my_campaign_id_1", "my_ad_set_id_1"),
                ("my_campaign_id_2", "my_ad_set_id_2"),
            ],
        )

        self.assertTrue(doc is not None)

        metrics_list = dpm.get_delivered_audience_performance_metrics(
            self.database,
            delivery_job_id,
        )

        self.assertTrue(metrics_list is not None)
        self.assertEqual(len(metrics_list), 1)

        doc = metrics_list[0]

        self.assertTrue(doc is not None)
        self.assertTrue(c.DELIVERY_JOB_ID in doc)
        self.assertTrue(c.CREATE_TIME in doc)
        self.assertTrue(c.PERFORMANCE_METRICS in doc)
        self.assertTrue(c.METRICS_START_TIME in doc)
        self.assertTrue(c.METRICS_END_TIME in doc)
        self.assertTrue(c.DELIVERY_PLATFORM_AD_SETS in doc)

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_get_delivery_platforms_count(self):
        """Test to retrieve count of delivery platforms documents."""

        delivery_platform_id = self.delivery_platform_doc[c.ID]

        # count of delivery platforms documents
        count = dpm.get_delivery_platforms_count(database=self.database)
        self.assertEqual(count, 1)

        # count of delivery platforms documents after soft deletion
        success_flag = delete_util.delete_delivery_platform(
            self.database, delivery_platform_id
        )
        self.assertTrue(success_flag)

        count = dpm.get_delivery_platforms_count(database=self.database)
        self.assertEqual(count, 0)

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
            self.database, source_audience_id, delivery_platform_id
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
