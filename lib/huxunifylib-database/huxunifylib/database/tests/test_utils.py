"""Database util tests."""

import os
import unittest
import mongomock
import huxunifylib.database.constants as c
import huxunifylib.database.data_management as dm
import huxunifylib.database.audience_management as am
import huxunifylib.database.delivery_platform_management as dpm
import huxunifylib.database.delete_util as delete_util

from huxunifylib.database.client import DatabaseClient


# pylint: disable=R0902,R0914,R0915
class TestUtils(unittest.TestCase):
    """Test utils module."""

    @mongomock.patch(servers=(("localhost", 27017),))
    def setUp(self):

        # Connect
        self.database = DatabaseClient(
            "localhost", 27017, None, None
        ).connect()

        self.database.drop_database(c.DATA_MANAGEMENT_DATABASE)

        # Create data sources
        self.data_source_doc_1 = dm.set_data_source(
            database=self.database,
            data_source_name="My Data Source 1",
            data_source_type=c.DATA_SOURCE_TYPE_FIRST_PARTY,
            data_source_format="CSV",
            location_type="S3",
            location_details={
                "bucket": "my.s3.bucket",
                "key": "my.s3.key",
            },
            fields=[
                {"header": "fn", "special_type": c.S_TYPE_FIRST_NAME},
                {"header": "ln", "special_type": c.S_TYPE_LAST_NAME},
                {"header": "gender", "special_type": c.S_TYPE_GENDER},
                {
                    "header": "customer_id",
                    "special_type": c.S_TYPE_CUSTOMER_ID,
                },
            ],
        )

        self.data_source_doc_2 = dm.set_data_source(
            database=self.database,
            data_source_name="My Data Source 2",
            data_source_type=c.DATA_SOURCE_TYPE_FIRST_PARTY,
            data_source_format="TSV",
            location_type="S3",
            location_details={
                "bucket": "my.s3.bucket",
                "key": "my.s3.key",
            },
            fields=[
                {"header": "fn", "special_type": c.S_TYPE_FIRST_NAME},
                {"header": "ln", "special_type": c.S_TYPE_LAST_NAME},
            ],
        )

        # Create ingestion jobs
        self.ingestion_job_doc_1 = dm.set_ingestion_job(
            self.database,
            self.data_source_doc_1[c.ID],
        )

        self.ingestion_job_doc_2 = dm.set_ingestion_job(
            self.database,
            self.data_source_doc_1[c.ID],
        )

        # Create audiences
        self.audience_doc_1 = am.create_audience(
            self.database,
            self.ingestion_job_doc_1[c.ID],
            "My Audience 1",
            [],
        )

        self.audience_doc_2 = am.create_audience(
            self.database,
            self.ingestion_job_doc_2[c.ID],
            "My Audience 2",
            [],
        )

        # Set delivery platforms
        self.delivery_platform_doc_1 = dpm.set_delivery_platform(
            self.database,
            c.DELIVERY_PLATFORM_FACEBOOK,
            "My delivery platform 1",
            {
                "facebook_access_token": "path1",
                "facebook_app_secret": "path2",
                "facebook_app_id": "path3",
                "facebook_ad_account_id": "path4",
            },
        )

        self.delivery_platform_doc_2 = dpm.set_delivery_platform(
            self.database,
            c.DELIVERY_PLATFORM_GOOGLE,
            "My delivery platform 2",
            {
                "google_access_token": "path1",
                "google_app_secret": "path2",
                "google_app_id": "path3",
                "google_ad_account_id": "path4",
            },
        )

        # Create a lookalike audiences
        self.lookalike_doc_1 = dpm.create_delivery_platform_lookalike_audience(
            self.database,
            self.delivery_platform_doc_1[c.ID],
            self.audience_doc_1[c.ID],
            "My lookalike audience 1",
            0.01,
            "US",
        )

        self.lookalike_doc_2 = dpm.create_delivery_platform_lookalike_audience(
            self.database,
            self.delivery_platform_doc_2[c.ID],
            self.audience_doc_2[c.ID],
            "My lookalike audience 2",
            0.01,
            "US",
        )

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_data_management(self):
        """Test different routines of data management module."""

        # details based on a local MongoDB configuration
        host = "localhost"
        port = 27017
        username = None
        password = None

        if "MONGO_DB_USERNAME" in os.environ:
            username = os.environ["MONGO_DB_USERNAME"]

        if "MONGO_DB_PASSWORD" in os.environ:
            password = os.environ["MONGO_DB_PASSWORD"]

        # Set up the database client
        client = DatabaseClient(host, port, username, password)

        # Connect
        database = client.connect()

        self.assertTrue(database is not None)

        # data source to be created
        sample_data_source = {
            c.DATA_SOURCE_NAME: "My Data Source",
            c.DATA_SOURCE_TYPE: 1,
            c.DATA_SOURCE_FORMAT: "CSV",
            c.DATA_SOURCE_LOCATION_TYPE: "S3",
            c.DATA_SOURCE_LOCATION_DETAILS: {
                "bucket": "my.s3.bucket",
                "key": "my.s3.key",
            },
            c.DATA_SOURCE_FIELDS: [
                {"header": "fn", "special_type": c.S_TYPE_FIRST_NAME},
                {"header": "ln", "special_type": c.S_TYPE_LAST_NAME},
                {"header": "gender", "special_type": c.S_TYPE_GENDER},
            ],
            c.DATA_SOURCE_NON_BREAKDOWN_FIELDS: [],
            c.ENABLED: True,
        }

        # Set a data source
        data_source_doc = dm.set_data_source(
            database=database,
            data_source_name=sample_data_source["name"],
            data_source_type=sample_data_source["type"],
            data_source_format=sample_data_source["format"],
            location_type=sample_data_source["location_type"],
            location_details=sample_data_source["location_details"],
            fields=sample_data_source["fields"],
        )

        self.assertTrue(data_source_doc is not None)
        self.assertTrue(c.ID in data_source_doc)

        data_source_id = data_source_doc[c.ID]

        # Set an ingestion job
        ingestion_job_doc = dm.set_ingestion_job(database, data_source_id)

        self.assertTrue(ingestion_job_doc is not None)
        self.assertTrue(c.ID in ingestion_job_doc)

        ingestion_job_id = ingestion_job_doc[c.ID]

        # Create an audience
        audience_doc = am.create_audience(
            database,
            ingestion_job_id,
            "My Audience",
            [],
        )

        self.assertTrue(audience_doc is not None)
        self.assertTrue(c.ID in audience_doc)

        audience_id = audience_doc[c.ID]

        # Set delivery platform
        auth_details = {
            "facebook_access_token": "path1",
            "facebook_app_secret": "path2",
            "facebook_app_id": "path3",
            "facebook_ad_account_id": "path4",
        }

        delivery_platform_doc = dpm.set_delivery_platform(
            database,
            c.DELIVERY_PLATFORM_FACEBOOK,
            "My delivery platform",
            auth_details,
        )

        delivery_platform_id = delivery_platform_doc[c.ID]

        self.assertTrue(delivery_platform_id is not None)

        doc = dpm.set_connection_status(
            database, delivery_platform_id, c.STATUS_SUCCEEDED
        )

        self.assertTrue(doc is not None)
        self.assertTrue(c.DELIVERY_PLATFORM_STATUS in doc)

        # Create a delivery job
        delivery_doc = dpm.set_delivery_job(
            database, audience_id, delivery_platform_id
        )

        self.assertTrue(delivery_doc is not None)
        self.assertTrue(c.ID in delivery_doc)

        delivery_id = delivery_doc[c.ID]

        # Create a lookalike audience
        doc = dpm.create_delivery_platform_lookalike_audience(
            database,
            delivery_platform_id,
            audience_id,
            "My lookalike audience",
            0.01,
            "US",
        )

        self.assertTrue(doc is not None)
        self.assertTrue(c.DELIVERY_PLATFORM_ID in doc)
        self.assertTrue(c.LOOKALIKE_SOURCE_AUD_ID in doc)
        self.assertTrue(c.LOOKALIKE_AUD_NAME in doc)
        self.assertTrue(c.LOOKALIKE_AUD_SIZE_PERCENTAGE in doc)
        self.assertTrue(c.LOOKALIKE_AUD_COUNTRY in doc)

        lookalike_audience_id = doc[c.ID]

        # Set delivery job lookalike audiences
        lookalike_audiences = [lookalike_audience_id]
        doc = dpm.set_delivery_job_lookalike_audiences(
            database,
            delivery_id,
            lookalike_audiences,
        )

        self.assertTrue(doc is not None)
        self.assertTrue(c.DELIVERY_PLATFORM_LOOKALIKE_AUDS in doc)
        self.assertEqual(
            doc[c.DELIVERY_PLATFORM_LOOKALIKE_AUDS], lookalike_audiences
        )

        # Create another delivery job with no lookalike audiences
        delivery_doc = dpm.set_delivery_job(
            database, audience_id, delivery_platform_id
        )

        self.assertTrue(delivery_doc is not None)
        self.assertTrue(c.ID in delivery_doc)

        delivery_id_2 = delivery_doc[c.ID]

        # Test soft delete functions
        success_flag = delete_util.delete_audience(database, audience_id)

        self.assertTrue(success_flag)

        success_flag = delete_util.delete_ingestion_job(
            database, ingestion_job_id
        )

        self.assertTrue(success_flag)

        success_flag = delete_util.delete_data_source(database, data_source_id)

        self.assertTrue(success_flag)

        success_flag = delete_util.delete_lookalike_audience(
            database,
            lookalike_audience_id,
        )

        self.assertTrue(success_flag)

        success_flag = delete_util.delete_delivery_job(database, delivery_id)

        self.assertTrue(success_flag)

        success_flag = delete_util.delete_delivery_job(database, delivery_id_2)

        self.assertTrue(success_flag)

        success_flag = delete_util.delete_delivery_platform(
            database,
            delivery_platform_id,
        )

        self.assertTrue(success_flag)

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_delete_lookalike_audiences_bulk(self):
        """Test bulk deletion of lookalike audiences."""

        success_flag = delete_util.delete_lookalike_audiences_bulk(
            self.database,
            [self.lookalike_doc_1[c.ID], self.lookalike_doc_2[c.ID]],
        )
        self.assertTrue(success_flag)

        doc = dpm.get_delivery_platform_lookalike_audience(
            self.database,
            self.lookalike_doc_1[c.ID],
        )
        self.assertTrue(doc is None)

        doc = dpm.get_delivery_platform_lookalike_audience(
            self.database,
            self.lookalike_doc_2[c.ID],
        )
        self.assertTrue(doc is None)

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_delete_audiences_bulk(self):
        """Test bulk deletion of audiences."""

        success_flag = delete_util.delete_audiences_bulk(
            self.database,
            [self.audience_doc_1[c.ID], self.audience_doc_2[c.ID]],
        )
        self.assertTrue(success_flag)

        doc = am.get_audience_config(
            self.database,
            self.audience_doc_1[c.ID],
        )
        self.assertTrue(doc is None)

        doc = am.get_audience_config(
            self.database,
            self.audience_doc_2[c.ID],
        )
        self.assertTrue(doc is None)

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_delete_delivery_platforms_bulk(self):
        """Test bulk deletion of delivery platforms."""

        success_flag = delete_util.delete_delivery_platforms_bulk(
            self.database,
            [
                self.delivery_platform_doc_1[c.ID],
                self.delivery_platform_doc_2[c.ID],
            ],
        )
        self.assertTrue(success_flag)

        doc = dpm.get_delivery_platform(
            self.database,
            self.delivery_platform_doc_1[c.ID],
        )
        self.assertTrue(doc is None)

        doc = dpm.get_delivery_platform(
            self.database,
            self.delivery_platform_doc_2[c.ID],
        )
        self.assertTrue(doc is None)

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_delete_data_sources_bulk(self):
        """Test bulk deletion of delivery platforms."""

        success_flag = delete_util.delete_data_sources_bulk(
            self.database,
            [self.data_source_doc_1[c.ID], self.data_source_doc_2[c.ID]],
        )
        self.assertTrue(success_flag)

        doc = dm.get_data_source(
            self.database,
            self.data_source_doc_1[c.ID],
        )
        self.assertTrue(doc is None)

        doc = dm.get_data_source(
            self.database,
            self.data_source_doc_2[c.ID],
        )
        self.assertTrue(doc is None)
