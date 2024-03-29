"""Data Management tests."""

import unittest
import mongomock
import pandas as pd
import huxunifylib.database.data_management as dm
import huxunifylib.database.audience_management as am
import huxunifylib.database.constants as db_c
from huxunifylib.database import delete_util

from huxunifylib.database.client import DatabaseClient
from huxunifylib.database.utils import detect_non_breakdown_fields
from huxunifylib.database.db_exceptions import DataSourceLocked


class TestDataManagement(unittest.TestCase):
    """Test data management module."""

    @mongomock.patch(servers=(("localhost", 27017),))
    def setUp(self):

        # Connect
        self.database = DatabaseClient(host="localhost", port=27017).connect()

        self.database.drop_database(db_c.DATA_MANAGEMENT_DATABASE)

        # data source to be created
        self.sample_data_source = {
            db_c.DATA_SOURCE_NAME: "My Data Source",
            db_c.DATA_SOURCE_TYPE: db_c.DATA_SOURCE_TYPE_FIRST_PARTY,
            db_c.DATA_SOURCE_FORMAT: "CSV",
            db_c.DATA_SOURCE_LOCATION_TYPE: "S3",
            db_c.DATA_SOURCE_LOCATION_DETAILS: {
                "bucket": "my.s3.bucket",
                "key": "my.s3.key",
            },
            db_c.DATA_SOURCE_FIELDS: [
                {"header": "fn", "special_type": db_c.S_TYPE_FIRST_NAME},
                {"header": "ln", "special_type": db_c.S_TYPE_LAST_NAME},
                {"header": "gender", "special_type": db_c.S_TYPE_GENDER},
                {"header": "city", "special_type": db_c.S_TYPE_CITY},
                {
                    "header": "country_code",
                    "special_type": db_c.S_TYPE_COUNTRY_CODE,
                },
                {
                    "header": "state",
                    "special_type": db_c.S_TYPE_STATE_OR_PROVINCE,
                },
                {
                    "header": "customer_id",
                    "special_type": db_c.S_TYPE_CUSTOMER_ID,
                },
                {"header": "custom_field"},
                {"header": "custom_field_extra"},
            ],
            db_c.DATA_SOURCE_NON_BREAKDOWN_FIELDS: [],
            db_c.ENABLED: True,
        }

        # Set a data source
        self.data_source_doc = dm.set_data_source(
            database=self.database,
            data_source_name=self.sample_data_source["name"],
            data_source_type=self.sample_data_source["type"],
            data_source_format=self.sample_data_source["format"],
            location_type=self.sample_data_source["location_type"],
            location_details=self.sample_data_source["location_details"],
            fields=self.sample_data_source["fields"],
        )

        # Set ingestion job
        self.ingestion_job_doc = dm.set_ingestion_job(
            self.database,
            self.data_source_doc[db_c.ID],
        )

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_set_data_source(self):
        """Test set_data_source routine."""

        # Set a data source
        data_source_doc = dm.set_data_source(
            database=self.database,
            data_source_name="My Data Source 1",
            data_source_type=self.sample_data_source["type"],
            data_source_format=self.sample_data_source["format"],
            location_type=self.sample_data_source["location_type"],
            location_details=self.sample_data_source["location_details"],
            fields=self.sample_data_source["fields"],
        )

        self.assertTrue(data_source_doc is not None)

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_get_data_source(self):
        """Test get_data_source routine."""

        data_source = dm.get_data_source(
            self.database, self.data_source_doc[db_c.ID]
        )

        self.assertTrue(data_source is not None)
        self.assertEqual(data_source[db_c.DATA_SOURCE_NAME], "My Data Source")
        self.assertFalse(db_c.DELETED in data_source)

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_get_data_sources_count(self):
        """Test get_data_sources_count routine."""

        data_source_doc_new = dm.set_data_source(
            database=self.database,
            data_source_name="My Data Source new",
            data_source_type=self.sample_data_source["type"],
            data_source_format=self.sample_data_source["format"],
            location_type=self.sample_data_source["location_type"],
            location_details=self.sample_data_source["location_details"],
            fields=self.sample_data_source["fields"],
        )

        self.assertTrue(data_source_doc_new is not None)

        count = dm.get_data_sources_count(database=self.database)

        self.assertEqual(count, 2)

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_get_all_data_sources(self):
        """Test get_all_data_sources routine."""

        # get all data sources
        data_sources_actual = dm.get_all_data_sources(self.database)

        self.assertTrue(data_sources_actual is not None)
        self.assertEqual(len(data_sources_actual), 1)
        self.assertFalse([d for d in data_sources_actual if db_c.DELETED in d])

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_delete_data_source(self):
        """Test delete_data_source routine."""

        success_flag = delete_util.delete_data_source(
            self.database, self.data_source_doc[db_c.ID]
        )
        self.assertTrue(success_flag)

        count = dm.get_data_sources_count(database=self.database)
        self.assertEqual(count, 0)

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_update_data_source(self):
        """Test data source update rotines."""

        # Set ingestion job status to fail so that data source can be updated
        status = db_c.STATUS_FAILED
        status_msg = "Ingestion job failed!"

        doc = am.set_ingestion_job_status(
            self.database, self.ingestion_job_doc[db_c.ID], status, status_msg
        )

        self.assertTrue(doc is not None)

        # Update data source name
        doc = dm.update_data_source_name(
            self.database,
            self.data_source_doc[db_c.ID],
            "New name",
        )

        self.assertTrue(doc is not None)
        self.assertTrue(db_c.DATA_SOURCE_NAME in doc)
        self.assertEqual(doc[db_c.DATA_SOURCE_NAME], "New name")

        # Update data source format
        doc = dm.update_data_source_format(
            self.database,
            self.data_source_doc[db_c.ID],
            "TSV",
        )

        self.assertTrue(doc is not None)
        self.assertTrue(db_c.DATA_SOURCE_FORMAT in doc)
        self.assertEqual(doc[db_c.DATA_SOURCE_FORMAT], "TSV")

        # Update data source location type
        doc = dm.update_data_source_location_type(
            self.database,
            self.data_source_doc[db_c.ID],
            "S3",
        )

        self.assertTrue(doc is not None)
        self.assertTrue(db_c.DATA_SOURCE_LOCATION_TYPE in doc)
        self.assertEqual(doc[db_c.DATA_SOURCE_LOCATION_TYPE], "S3")

        # Update data source location details
        new_location_details = {"bucket": "new.s3.bucket", "key": "new.s3.key"}
        doc = dm.update_data_source_location_details(
            self.database,
            self.data_source_doc[db_c.ID],
            new_location_details,
        )

        self.assertTrue(doc is not None)
        self.assertTrue(db_c.DATA_SOURCE_LOCATION_DETAILS in doc)
        self.assertEqual(
            doc[db_c.DATA_SOURCE_LOCATION_DETAILS], new_location_details
        )

        # Update data source fields
        new_fields = [
            {"header": "fn", "special_type": db_c.S_TYPE_FIRST_NAME},
            {"header": "ln", "special_type": db_c.S_TYPE_LAST_NAME},
        ]

        doc = dm.update_data_source_fields(
            self.database, self.data_source_doc[db_c.ID], new_fields
        )

        self.assertTrue(doc is not None)
        self.assertTrue(db_c.DATA_SOURCE_FIELDS in doc)
        self.assertEqual(doc[db_c.DATA_SOURCE_FIELDS], new_fields)

        # Update data source parameters
        updated_fields = [
            {"header": "fn", "special_type": db_c.S_TYPE_FIRST_NAME},
            {"header": "ln", "special_type": db_c.S_TYPE_LAST_NAME},
            {"header": "city", "special_type": db_c.S_TYPE_CITY},
            {
                "header": "country_code",
                "special_type": db_c.S_TYPE_COUNTRY_CODE,
            },
            {"header": "state", "special_type": db_c.S_TYPE_STATE_OR_PROVINCE},
            {"header": "gender", "special_type": db_c.S_TYPE_GENDER},
            {"header": "custom_field"},
            {"header": "custom_field_extra"},
        ]

        updated_location_details = {
            "bucket": "updated.s3.bucket",
            "key": "updated.s3.key",
        }

        doc = dm.update_data_source(
            database=self.database,
            data_source_id=self.data_source_doc[db_c.ID],
            name="Updated Data Source name",
            location_details=updated_location_details,
            fields=updated_fields,
        )

        self.assertTrue(doc is not None)
        self.assertEqual(
            doc[db_c.DATA_SOURCE_NAME], "Updated Data Source name"
        )
        self.assertEqual(
            doc[db_c.DATA_SOURCE_TYPE], db_c.DATA_SOURCE_TYPE_FIRST_PARTY
        )
        self.assertEqual(doc[db_c.DATA_SOURCE_FIELDS], updated_fields)
        self.assertEqual(doc[db_c.DATA_SOURCE_FORMAT], "TSV")
        self.assertEqual(doc[db_c.DATA_SOURCE_LOCATION_TYPE], "S3")
        self.assertEqual(
            doc[db_c.DATA_SOURCE_LOCATION_DETAILS], updated_location_details
        )

        # Test updating data source with a successful ingestion job
        status = db_c.STATUS_SUCCEEDED
        status_msg = "Ingestion job succeeded!"

        doc = am.set_ingestion_job_status(
            self.database, self.ingestion_job_doc[db_c.ID], status, status_msg
        )

        self.assertTrue(doc is not None)

        expected_exc_msg = (
            f"Data source with ID <{self.data_source_doc[db_c.ID]}> "
            f"is associated to an ingestion job and cannot be updated!"
        )

        try:
            doc = dm.update_data_source_format(
                self.database, self.data_source_doc[db_c.ID], "CSV"
            )
        except DataSourceLocked as exc_msg:
            self.assertEqual(str(exc_msg), expected_exc_msg)

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_set_ingestion_job(self):
        """Test set_ingestion_job."""

        # Set ingestion job
        ingestion_job_doc = dm.set_ingestion_job(
            self.database,
            self.data_source_doc[db_c.ID],
        )

        self.assertTrue(ingestion_job_doc is not None)
        self.assertTrue(db_c.ID in ingestion_job_doc)

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_get_ingestion_job(self):
        """Test get_ingestion_job."""

        ingestion_job = dm.get_ingestion_job(
            self.database, self.ingestion_job_doc[db_c.ID]
        )

        self.assertTrue(ingestion_job is not None)
        self.assertFalse(db_c.DELETED in ingestion_job)

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_set_ingestion_job_status(self):
        """Test set_ingestion_job_status."""

        status = db_c.AUDIENCE_STATUS_DELIVERING
        status_msg = "This is a test."

        doc = am.set_ingestion_job_status(
            self.database,
            self.ingestion_job_doc[db_c.ID],
            status,
            status_msg,
        )

        self.assertTrue(doc is not None)
        self.assertTrue(db_c.JOB_STATUS in doc)
        self.assertTrue(db_c.STATUS_MESSAGE in doc)
        self.assertTrue(db_c.CREATE_TIME in doc)
        self.assertTrue(db_c.UPDATE_TIME in doc)
        self.assertTrue(db_c.JOB_START_TIME in doc)

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_get_ingestion_job_status(self):
        """Test get_ingestion_job_status."""

        status = db_c.STATUS_IN_PROGRESS
        status_msg = "This is a test."

        doc = am.set_ingestion_job_status(
            self.database,
            self.ingestion_job_doc[db_c.ID],
            status,
            status_msg,
        )

        ret_status, ret_status_msg = dm.get_ingestion_job_status(
            self.database,
            self.ingestion_job_doc[db_c.ID],
        )

        self.assertTrue(doc is not None)
        self.assertTrue(db_c.JOB_STATUS in doc)
        self.assertTrue(db_c.STATUS_MESSAGE in doc)
        self.assertEqual(ret_status, status)
        self.assertEqual(ret_status_msg, status_msg)

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_get_ingestion_job_custom_fields(self):
        """Test get_ingestion_job_custom_fields."""

        custom_fields = dm.get_ingestion_job_custom_fields(
            self.database,
            self.ingestion_job_doc[db_c.ID],
        )

        expected_custom_fields = ["custom_field", "custom_field_extra"]

        self.assertEqual(custom_fields, expected_custom_fields)

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_append_ingested_job_data(self):
        """Test append_ingested_job_data."""

        # Ingest a batch of data
        ingested_data = pd.DataFrame(
            {
                db_c.S_TYPE_FIRST_NAME: [
                    "first_name_1",
                    "first_name_2",
                    "first_name_3",
                ],
                db_c.S_TYPE_LAST_NAME: [
                    "last_name_1",
                    "last_name_2",
                    "last_name_3",
                ],
                db_c.S_TYPE_EMAIL: ["email_1", "email_2", "email_3"],
                db_c.S_TYPE_CUSTOMER_ID: ["1", "1", "3"],
            }
        )

        success_flag = dm.append_ingested_data(
            self.database, self.ingestion_job_doc[db_c.ID], ingested_data
        )

        self.assertTrue(success_flag)

        dm_db = self.database[db_c.DATA_MANAGEMENT_DATABASE]
        collection = dm_db[db_c.INGESTED_DATA_COLLECTION]
        cursor = collection.find()

        doc_count = 0
        for item in cursor:
            self.assertTrue(db_c.INGESTED_DATA in item)
            doc_count += 1

        # Make sure duplicate customer ID has not been inserted
        self.assertEqual(doc_count, 2)

        # Ingest a second batch
        ingested_data = pd.DataFrame(
            {
                db_c.S_TYPE_FIRST_NAME: [
                    "first_name_4",
                    "first_name_5",
                    "first_name_6",
                ],
                db_c.S_TYPE_LAST_NAME: [
                    "last_name_4",
                    "last_name_5",
                    "last_name_6",
                ],
                db_c.S_TYPE_EMAIL: ["email_4", "email_5", "email_6"],
                db_c.S_TYPE_CUSTOMER_ID: ["4", "3", "6"],
            }
        )

        success_flag = dm.append_ingested_data(
            self.database, self.ingestion_job_doc[db_c.ID], ingested_data
        )

        self.assertTrue(success_flag)

        dm_db = self.database[db_c.DATA_MANAGEMENT_DATABASE]
        collection = dm_db[db_c.INGESTED_DATA_COLLECTION]
        cursor = collection.find()

        doc_count = 0
        for item in cursor:
            self.assertTrue(db_c.INGESTED_DATA in item)
            doc_count += 1

        # Make sure duplicate customer ID has not been inserted
        self.assertEqual(doc_count, 4)

        # Ingest a third batch without customer IDs
        ingested_data = pd.DataFrame(
            {
                db_c.S_TYPE_FIRST_NAME: [
                    "first_name_7",
                    "first_name_8",
                ],
                db_c.S_TYPE_LAST_NAME: [
                    "last_name_7",
                    "last_name_8",
                ],
                db_c.S_TYPE_EMAIL: ["email_7", "email_8"],
            }
        )

        success_flag = dm.append_ingested_data(
            self.database, self.ingestion_job_doc[db_c.ID], ingested_data
        )

        self.assertTrue(success_flag)

        # Make sure internal customer ID has been created
        dm_db = self.database[db_c.DATA_MANAGEMENT_DATABASE]
        collection = dm_db[db_c.INGESTED_DATA_COLLECTION]
        cursor = collection.find()

        for item in cursor:
            self.assertTrue(db_c.INGESTED_DATA in item)
            self.assertTrue(
                db_c.S_TYPE_CUSTOMER_ID in item[db_c.INGESTED_DATA]
            )

    # pylint: disable=R0904,R0915
    @mongomock.patch(servers=(("localhost", 27017),))
    def test_append_ingested_job_data_stats(self):
        """Test append_ingested_job_data_stats."""

        # Create new ingested data stats
        ingested_data = pd.DataFrame(
            {
                db_c.S_TYPE_FIRST_NAME: [
                    "first_name_1",
                    "first_name_2",
                    "first_name_3",
                ],
                db_c.S_TYPE_LAST_NAME: [
                    "last_name_1",
                    "last_name_2",
                    "last_name_3",
                ],
                db_c.S_TYPE_EMAIL: ["email_1", "email_2", "email_3"],
                db_c.S_TYPE_CITY: ["New York", None, "San Francisco"],
                db_c.S_TYPE_COUNTRY_CODE: ["US", None, "US"],
                db_c.S_TYPE_STATE_OR_PROVINCE: ["NY", None, "CA"],
                db_c.S_TYPE_GENDER: ["m", "f", None],
                db_c.S_TYPE_AGE: [35, 29, 65],
                "custom_field": ["value_1", "value_2", None],
                "custom_field_extra": ["value_10", None, "value_30"],
            }
        )

        stats_doc = dm.append_ingested_data_stats(
            self.database,
            self.ingestion_job_doc[db_c.ID],
            ingested_data,
            ["custom_field_extra"],
        )

        self.assertTrue(stats_doc is not None)

        self.assertTrue(db_c.S_TYPE_FIRST_NAME in stats_doc)
        self.assertTrue(db_c.S_TYPE_LAST_NAME in stats_doc)
        self.assertTrue(db_c.S_TYPE_CITY in stats_doc)
        self.assertTrue(db_c.S_TYPE_COUNTRY_CODE in stats_doc)
        self.assertTrue(db_c.S_TYPE_STATE_OR_PROVINCE in stats_doc)
        self.assertTrue(db_c.S_TYPE_GENDER in stats_doc)
        self.assertTrue("custom_field" in stats_doc)
        self.assertTrue("custom_field_extra" in stats_doc)

        self.assertTrue(db_c.S_TYPE_AGE not in stats_doc)

        self.assertTrue(db_c.STATS_BREAKDOWN in stats_doc[db_c.S_TYPE_CITY])
        self.assertTrue(
            db_c.STATS_BREAKDOWN in stats_doc[db_c.S_TYPE_STATE_OR_PROVINCE]
        )
        self.assertTrue(
            db_c.STATS_BREAKDOWN in stats_doc[db_c.S_TYPE_COUNTRY_CODE]
        )
        self.assertTrue(db_c.STATS_BREAKDOWN in stats_doc[db_c.S_TYPE_GENDER])
        self.assertTrue(
            db_c.STATS_BREAKDOWN in stats_doc["custom_field_extra"]
        )

        self.assertTrue(
            db_c.STATS_BREAKDOWN not in stats_doc[db_c.S_TYPE_FIRST_NAME]
        )
        self.assertTrue(
            db_c.STATS_BREAKDOWN not in stats_doc[db_c.S_TYPE_LAST_NAME]
        )
        self.assertTrue(db_c.STATS_BREAKDOWN not in stats_doc["custom_field"])

        doc = dm.get_ingested_data_stats(
            self.database, self.ingestion_job_doc[db_c.ID]
        )

        self.assertTrue(doc is not None)
        self.assertTrue(db_c.JOB_ID in doc)
        self.assertEqual(doc[db_c.JOB_ID], self.ingestion_job_doc[db_c.ID])
        self.assertTrue(db_c.S_TYPE_CITY in doc)
        self.assertTrue(db_c.S_TYPE_COUNTRY_CODE in doc)
        self.assertTrue(db_c.S_TYPE_STATE_OR_PROVINCE in doc)
        self.assertTrue(db_c.S_TYPE_GENDER in doc)
        self.assertTrue(db_c.STATS_COVERAGE in doc[db_c.S_TYPE_CITY])
        self.assertTrue(db_c.STATS_COVERAGE in doc[db_c.S_TYPE_COUNTRY_CODE])
        self.assertTrue(
            db_c.STATS_COVERAGE in doc[db_c.S_TYPE_STATE_OR_PROVINCE]
        )
        self.assertTrue(db_c.STATS_COVERAGE in doc[db_c.S_TYPE_GENDER])
        self.assertTrue(db_c.STATS_BREAKDOWN in doc[db_c.S_TYPE_CITY])
        self.assertTrue(db_c.STATS_BREAKDOWN in doc[db_c.S_TYPE_COUNTRY_CODE])
        self.assertTrue(
            db_c.STATS_BREAKDOWN in doc[db_c.S_TYPE_STATE_OR_PROVINCE]
        )
        self.assertTrue(db_c.STATS_BREAKDOWN in doc[db_c.S_TYPE_GENDER])
        self.assertEqual(doc[db_c.DATA_COUNT], 3)
        self.assertEqual(
            doc[db_c.S_TYPE_CITY],
            {
                "coverage": 0.6666666666666666,
                "breakdown": {"New York": 0.5, "San Francisco": 0.5},
            },
        )
        self.assertEqual(
            doc[db_c.S_TYPE_GENDER],
            {
                "coverage": 0.6666666666666666,
                "breakdown": {"m": 0.5, "f": 0.5},
            },
        )

        # Update ingested data stats
        ingested_data = pd.DataFrame(
            {
                db_c.S_TYPE_FIRST_NAME: ["first_name_4", "first_name_5"],
                db_c.S_TYPE_LAST_NAME: ["last_name_4", "last_name_5"],
                db_c.S_TYPE_EMAIL: ["email_4", "email_5"],
                db_c.S_TYPE_CITY: ["London", "San Francisco"],
                db_c.S_TYPE_COUNTRY_CODE: ["UK", "US"],
                db_c.S_TYPE_STATE_OR_PROVINCE: ["JS", "CA"],
                db_c.S_TYPE_GENDER: ["other", "f"],
                db_c.S_TYPE_AGE: [44, 20],
                "custom_field": ["value_4", "value_5"],
            }
        )

        stats_doc = dm.append_ingested_data_stats(
            self.database,
            self.ingestion_job_doc[db_c.ID],
            ingested_data,
            ["custom_field"],
        )

        self.assertTrue(stats_doc is not None)

        self.assertTrue(db_c.S_TYPE_FIRST_NAME in stats_doc)
        self.assertTrue(db_c.S_TYPE_LAST_NAME in stats_doc)
        self.assertTrue(db_c.S_TYPE_CITY in stats_doc)
        self.assertTrue(db_c.S_TYPE_COUNTRY_CODE in stats_doc)
        self.assertTrue(db_c.S_TYPE_STATE_OR_PROVINCE in stats_doc)
        self.assertTrue(db_c.S_TYPE_GENDER in stats_doc)
        self.assertTrue("custom_field" in stats_doc)

        self.assertTrue(db_c.S_TYPE_AGE not in stats_doc)

        self.assertTrue(db_c.STATS_BREAKDOWN in stats_doc[db_c.S_TYPE_CITY])
        self.assertTrue(
            db_c.STATS_BREAKDOWN in stats_doc[db_c.S_TYPE_STATE_OR_PROVINCE]
        )
        self.assertTrue(
            db_c.STATS_BREAKDOWN in stats_doc[db_c.S_TYPE_COUNTRY_CODE]
        )
        self.assertTrue(db_c.STATS_BREAKDOWN in stats_doc[db_c.S_TYPE_GENDER])
        self.assertTrue(db_c.STATS_BREAKDOWN in stats_doc["custom_field"])
        self.assertTrue(
            db_c.STATS_BREAKDOWN not in stats_doc[db_c.S_TYPE_FIRST_NAME]
        )
        self.assertTrue(
            db_c.STATS_BREAKDOWN not in stats_doc[db_c.S_TYPE_LAST_NAME]
        )

        doc = dm.get_ingested_data_stats(
            self.database, self.ingestion_job_doc[db_c.ID]
        )

        self.assertTrue(doc is not None)
        self.assertTrue(db_c.JOB_ID in doc)
        self.assertEqual(doc[db_c.JOB_ID], self.ingestion_job_doc[db_c.ID])
        self.assertTrue(db_c.S_TYPE_CITY in doc)
        self.assertTrue(db_c.S_TYPE_COUNTRY_CODE in doc)
        self.assertTrue(db_c.S_TYPE_STATE_OR_PROVINCE in doc)
        self.assertTrue(db_c.S_TYPE_GENDER in doc)
        self.assertTrue(db_c.STATS_COVERAGE in doc[db_c.S_TYPE_CITY])
        self.assertTrue(db_c.STATS_COVERAGE in doc[db_c.S_TYPE_COUNTRY_CODE])
        self.assertTrue(
            db_c.STATS_COVERAGE in doc[db_c.S_TYPE_STATE_OR_PROVINCE]
        )
        self.assertTrue(db_c.STATS_COVERAGE in doc[db_c.S_TYPE_GENDER])
        self.assertTrue(db_c.STATS_BREAKDOWN in doc[db_c.S_TYPE_CITY])
        self.assertTrue(db_c.STATS_BREAKDOWN in doc[db_c.S_TYPE_COUNTRY_CODE])
        self.assertTrue(
            db_c.STATS_BREAKDOWN in doc[db_c.S_TYPE_STATE_OR_PROVINCE]
        )
        self.assertTrue(db_c.STATS_BREAKDOWN in doc[db_c.S_TYPE_GENDER])
        self.assertEqual(doc[db_c.DATA_COUNT], 5)
        self.assertEqual(
            doc[db_c.S_TYPE_CITY],
            {
                "coverage": 0.8,
                "breakdown": {
                    "San Francisco": 0.5,
                    "London": 0.25,
                    "New York": 0.25,
                },
            },
        )
        self.assertEqual(
            doc[db_c.S_TYPE_GENDER],
            {
                "coverage": 0.8,
                "breakdown": {"other": 0.25, "f": 0.5, "m": 0.25},
            },
        )

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_get_all_data_source_ids(self):
        """Test get_all_data_source_ids."""

        # Get all existing data source ids
        data_source_list = dm.get_all_data_source_ids(self.database)

        self.assertTrue(data_source_list is not None)
        self.assertEqual(len(data_source_list), 1)
        self.assertEqual(data_source_list[0], self.data_source_doc[db_c.ID])

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_get_data_source_recent_ingestion_job_id(self):
        """Test get_data_source_recent_ingestion_job_id."""

        # Get most recent ingestion_job_id
        recent_job_id = dm.get_data_source_recent_ingestion_job_id(
            self.database,
            self.data_source_doc[db_c.ID],
        )

        self.assertTrue(recent_job_id is not None)
        self.assertEqual(recent_job_id, self.ingestion_job_doc[db_c.ID])

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_update_data_source_non_breakdown_fields(self):
        """Test update_data_source_non_breakdown_fields."""

        # Detect and store non_breakdown fields
        new_data = pd.DataFrame(
            {
                db_c.S_TYPE_FIRST_NAME: ["first_name_10", "first_name_11"],
                db_c.S_TYPE_LAST_NAME: ["last_name_10", "last_name_11"],
                db_c.S_TYPE_EMAIL: ["email_10", "email_11"],
                "custom_field": ["value_10", "value_11"],
                "custom_field_extra": ["value_20", "value_$1"],
            }
        )

        non_breakdown_fields = detect_non_breakdown_fields(
            new_data,
            new_data.columns,
        )

        self.assertEqual(len(non_breakdown_fields), 1)
        self.assertEqual(non_breakdown_fields[0], "custom_field_extra")

        doc = dm.update_data_source_non_breakdown_fields(
            self.database,
            self.data_source_doc[db_c.ID],
            non_breakdown_fields,
        )

        self.assertTrue(doc is not None)

        tmp_fields = dm.get_data_source_non_breakdown_fields(
            self.database,
            self.data_source_doc[db_c.ID],
        )

        self.assertEqual(len(tmp_fields), 1)
        self.assertEqual(tmp_fields[0], "custom_field_extra")

    @mongomock.patch(servers=(("localhost", 27017),))
    def favorite_data_source(self):
        """Test favorite_data_source."""

        # Test favorite functions
        doc = dm.favorite_data_source(
            self.database, self.data_source_doc[db_c.ID]
        )

        self.assertTrue(doc is not None)
        self.assertTrue(db_c.FAVORITE in doc)
        self.assertTrue(doc[db_c.FAVORITE])

    @mongomock.patch(servers=(("localhost", 27017),))
    def unfavorite_data_source(self):
        """Test unfavorite_data_source."""

        doc = dm.unfavorite_data_source(
            self.database, self.data_source_doc[db_c.ID]
        )

        self.assertTrue(doc is not None)
        self.assertTrue(db_c.FAVORITE in doc)
        self.assertTrue(not doc[db_c.FAVORITE])
