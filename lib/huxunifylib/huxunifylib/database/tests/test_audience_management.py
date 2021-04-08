"""Database client tests."""

import unittest
import mongomock
import pandas as pd
import huxunifylib.database.audience_management as am
import huxunifylib.database.data_management as dm
import huxunifylib.database.constants as c
from huxunifylib.database import utils

from huxunifylib.database.client import DatabaseClient


class TestAudienceManagement(unittest.TestCase):
    """Test audience management module."""

    @mongomock.patch(servers=(("localhost", 27017),))
    def setUp(self):

        # Connect
        self.database = DatabaseClient(
            "localhost", 27017, None, None
        ).connect()

        self.database.drop_database(c.DATA_MANAGEMENT_DATABASE)

        # Set ingestion job
        data_source_doc = dm.set_data_source(
            self.database,
            "My data source",
            1,
            "CSV",
            "S3",
            None,
            None,
        )
        self.ingestion_job_doc = dm.set_ingestion_job(
            self.database, data_source_doc[c.ID]
        )

        self.assertTrue(self.ingestion_job_doc is not None)
        self.assertTrue(c.ID in self.ingestion_job_doc)

        ingestion_job_id = self.ingestion_job_doc[c.ID]

        doc = dm.set_ingestion_job_status(
            self.database, ingestion_job_id, c.STATUS_SUCCEEDED
        )

        self.assertTrue(doc is not None)
        self.assertTrue(c.JOB_STATUS in doc)
        self.assertTrue(c.JOB_END_TIME in doc)

        # Store ingested data and create an audience
        ingested_data_frame = pd.DataFrame(
            {
                c.S_TYPE_FIRST_NAME: [
                    "first_name_10",
                    "first_name_20",
                    "first_name_30",
                    "first_name_40",
                ],
                c.S_TYPE_LAST_NAME: [
                    "last_name_10",
                    "last_name_20",
                    "last_name_30",
                    "last_name_40",
                ],
                c.S_TYPE_EMAIL: [
                    "email_10",
                    "email_20",
                    "email_30",
                    "email_40",
                ],
                c.S_TYPE_CITY: [
                    "New York",
                    "London",
                    "San Francisco",
                    "Chicago",
                ],
                c.S_TYPE_COUNTRY_CODE: ["US", "UK", "US", "US"],
                c.S_TYPE_STATE_OR_PROVINCE: ["NY", None, "CA", "IL"],
                c.S_TYPE_GENDER: ["m", "f", None, "m"],
                c.S_TYPE_AGE: [33, 28, 64, 59],
                "custom_field": ["val_10", "val_20", "val_30", "val_40"],
            }
        )

        success_flag = dm.append_ingested_data(
            self.database, ingestion_job_id, ingested_data_frame
        )

        self.assertTrue(success_flag)

        # Append records with different fields
        new_data_frame = pd.DataFrame(
            {
                c.S_TYPE_FIRST_NAME: [
                    "first_name_50",
                    "first_name_60",
                ],
                c.S_TYPE_LAST_NAME: [
                    "last_name_50",
                    "last_name_60",
                ],
                c.S_TYPE_EMAIL: [
                    "email_50",
                    "email_60",
                ],
                c.S_TYPE_AGE: [43, 48],
                "new_custom_field": ["new_val_50", "new_val_60"],
            }
        )

        success_flag = dm.append_ingested_data(
            self.database, ingestion_job_id, new_data_frame
        )

        self.assertTrue(success_flag)

        self.audience_filters = [
            {
                "field": c.S_TYPE_AGE,
                "type": c.AUDIENCE_FILTER_MAX,
                "value": 60,
            },
            {
                "field": c.S_TYPE_COUNTRY_CODE,
                "type": c.AUDIENCE_FILTER_INCLUDE,
                "value": "US",
            },
            {
                "field": c.S_TYPE_CITY,
                "type": c.AUDIENCE_FILTER_EXCLUDE,
                "value": ["London"],
            },
        ]

        self.audience_doc = am.create_audience(
            self.database,
            ingestion_job_id,
            "My Audience",
            self.audience_filters,
        )

        self.assertTrue(self.audience_doc is not None)
        self.assertTrue(c.ID in self.audience_doc)

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_create_count_audience(self):
        """Test create and count audiences."""

        doc = am.create_audience(
            self.database,
            self.ingestion_job_doc[c.ID],
            "My Audience new",
            self.audience_filters,
        )

        self.assertTrue(doc is not None)

        count = am.get_audiences_count(database=self.database)

        self.assertEqual(count, 3)

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_get_audience(self):
        """Test get audiences."""

        audience_data_1, next_start_id = am.get_audience(
            self.database,
            self.audience_doc[c.ID],
            None,
            1,
        )

        self.assertEqual(audience_data_1.shape[0], 1)
        self.assertTrue(c.S_TYPE_CUSTOMER_ID in audience_data_1.columns)

        audience_data_2, next_start_id = am.get_audience(
            self.database,
            self.audience_doc[c.ID],
            next_start_id,
            1,
        )

        self.assertEqual(audience_data_2.shape[0], 1)
        self.assertTrue(c.S_TYPE_CUSTOMER_ID in audience_data_1.columns)

        audience_data = pd.concat([audience_data_1, audience_data_2])

        self.assertTrue(audience_data is not None)

        self.assertEqual(audience_data.shape[0], 2)
        self.assertEqual(set(audience_data[c.S_TYPE_COUNTRY_CODE]), {"US"})
        self.assertEqual(
            set(audience_data[c.S_TYPE_CITY]), {"New York", "Chicago"}
        )
        self.assertEqual(set(audience_data[c.S_TYPE_AGE]), {33, 59})

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_get_audience_batches(self):
        """Test get audiences in batches."""

        # Get audience in batches
        fetch = am.get_audience_batches(
            self.database, self.audience_doc[c.ID], 1
        )

        for audience_batch in fetch:
            self.assertEqual(audience_batch.shape[0], 1)

        fetch = am.get_audience_batches(
            self.database, self.audience_doc[c.ID], 2
        )

        for audience_batch in fetch:
            self.assertEqual(audience_batch.shape[0], 2)

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_delete_audience(self):
        """Test delete audiences."""

        # count of audiences documents after soft deletion
        success_flag = utils.delete_audience(
            self.database, self.audience_doc[c.ID]
        )
        self.assertTrue(success_flag)

        count = am.get_audiences_count(database=self.database)
        self.assertEqual(count, 1)

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_append_audience_insights(self):
        """Test append audience insights."""

        audience_data, _ = am.get_audience(
            self.database,
            self.audience_doc[c.ID],
        )

        insights = am.append_audience_insights(
            self.database, self.audience_doc[c.ID], audience_data
        )

        self.assertTrue(insights is not None)
        self.assertTrue(c.AUDIENCE_ID in insights)
        self.assertEqual(insights[c.AUDIENCE_ID], self.audience_doc[c.ID])
        self.assertTrue(c.S_TYPE_CITY in insights)
        self.assertTrue(c.S_TYPE_COUNTRY_CODE in insights)
        self.assertTrue(c.S_TYPE_STATE_OR_PROVINCE in insights)
        self.assertTrue(c.S_TYPE_GENDER in insights)
        self.assertTrue(c.S_TYPE_AGE in insights)
        self.assertTrue(c.STATS_COVERAGE in insights[c.S_TYPE_CITY])
        self.assertTrue(c.STATS_COVERAGE in insights[c.S_TYPE_COUNTRY_CODE])
        self.assertTrue(
            c.STATS_COVERAGE in insights[c.S_TYPE_STATE_OR_PROVINCE]
        )
        self.assertTrue(c.STATS_COVERAGE in insights[c.S_TYPE_GENDER])
        self.assertTrue(c.STATS_COVERAGE in insights[c.S_TYPE_AGE])
        self.assertTrue(c.STATS_BREAKDOWN in insights[c.S_TYPE_CITY])
        self.assertTrue(c.STATS_BREAKDOWN in insights[c.S_TYPE_COUNTRY_CODE])
        self.assertTrue(
            c.STATS_BREAKDOWN in insights[c.S_TYPE_STATE_OR_PROVINCE]
        )
        self.assertTrue(c.STATS_BREAKDOWN in insights[c.S_TYPE_GENDER])
        self.assertTrue(c.STATS_BREAKDOWN in insights[c.S_TYPE_AGE])
        self.assertTrue(c.STATS_BREAKDOWN not in insights[c.S_TYPE_FIRST_NAME])
        self.assertTrue(c.STATS_BREAKDOWN not in insights[c.S_TYPE_LAST_NAME])
        self.assertTrue(c.STATS_BREAKDOWN not in insights[c.S_TYPE_EMAIL])

        self.assertEqual(insights[c.DATA_COUNT], 2)
        self.assertEqual(
            insights[c.S_TYPE_CITY],
            {"coverage": 1.0, "breakdown": {"New York": 0.5, "Chicago": 0.5}},
        )
        self.assertEqual(
            insights[c.S_TYPE_GENDER],
            {"coverage": 1.0, "breakdown": {"m": 1.0}},
        )

        # Append more data to insights
        new_audience_data = pd.DataFrame(
            {
                c.S_TYPE_FIRST_NAME: [
                    "first_name_4",
                    "first_name_5",
                    "first_name_6",
                ],
                c.S_TYPE_LAST_NAME: [
                    "last_name_4",
                    "last_name_5",
                    "last_name_6",
                ],
                c.S_TYPE_EMAIL: ["email_4", "email_5", "email_6"],
                c.S_TYPE_CITY: ["New York", "Chicago", "San Francisco"],
                c.S_TYPE_COUNTRY_CODE: ["US", "US", "US"],
                c.S_TYPE_STATE_OR_PROVINCE: ["NY", "IL", "CA"],
                c.S_TYPE_GENDER: ["m", "f", "f"],
                c.S_TYPE_AGE: [59, 50, 35],
                "custom_field": [
                    "val_4",
                    "val_5",
                    "val_6",
                ],
                "custom_field_extra": [
                    "val_7",
                    None,
                    "val_8",
                ],
            }
        )

        insights = am.append_audience_insights(
            self.database,
            self.audience_doc[c.ID],
            new_audience_data,
            ["custom_field", "custom_field_extra"],
        )

        assert insights is not None

        self.assertTrue(insights is not None)
        self.assertTrue(c.AUDIENCE_ID in insights)
        self.assertEqual(insights[c.AUDIENCE_ID], self.audience_doc[c.ID])
        self.assertTrue(c.S_TYPE_CITY in insights)
        self.assertTrue(c.S_TYPE_COUNTRY_CODE in insights)
        self.assertTrue(c.S_TYPE_STATE_OR_PROVINCE in insights)
        self.assertTrue(c.S_TYPE_GENDER in insights)
        self.assertTrue(c.S_TYPE_AGE in insights)
        self.assertTrue("custom_field" in insights)
        self.assertTrue("custom_field_extra" in insights)
        self.assertTrue(c.STATS_COVERAGE in insights[c.S_TYPE_CITY])
        self.assertTrue(c.STATS_COVERAGE in insights[c.S_TYPE_COUNTRY_CODE])
        self.assertTrue(
            c.STATS_COVERAGE in insights[c.S_TYPE_STATE_OR_PROVINCE]
        )
        self.assertTrue(c.STATS_COVERAGE in insights[c.S_TYPE_GENDER])
        self.assertTrue(c.STATS_COVERAGE in insights[c.S_TYPE_AGE])
        self.assertTrue(c.STATS_BREAKDOWN in insights[c.S_TYPE_CITY])
        self.assertTrue(c.STATS_BREAKDOWN in insights[c.S_TYPE_COUNTRY_CODE])
        self.assertTrue(
            c.STATS_BREAKDOWN in insights[c.S_TYPE_STATE_OR_PROVINCE]
        )
        self.assertTrue(c.STATS_BREAKDOWN in insights[c.S_TYPE_GENDER])
        self.assertTrue(c.STATS_BREAKDOWN in insights[c.S_TYPE_AGE])
        self.assertTrue(c.STATS_BREAKDOWN in insights["custom_field"])
        self.assertTrue(c.STATS_BREAKDOWN in insights["custom_field_extra"])
        self.assertTrue(c.STATS_BREAKDOWN not in insights[c.S_TYPE_FIRST_NAME])
        self.assertTrue(c.STATS_BREAKDOWN not in insights[c.S_TYPE_LAST_NAME])
        self.assertTrue(c.STATS_BREAKDOWN not in insights[c.S_TYPE_EMAIL])

        self.assertEqual(insights[c.DATA_COUNT], 5)
        self.assertEqual(
            insights[c.S_TYPE_CITY],
            {
                "coverage": 1.0,
                "breakdown": {
                    "Chicago": 0.4,
                    "San Francisco": 0.2,
                    "New York": 0.4,
                },
            },
        )

        # Get insights
        stored_insights = am.get_audience_insights(
            self.database,
            self.audience_doc[c.ID],
        )

        self.assertTrue(stored_insights is not None)
        self.assertEqual(stored_insights, insights)

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_get_audience_config(self):
        """Test get audience config."""

        # Get audience configuration
        doc = am.get_audience_config(
            self.database,
            self.audience_doc[c.ID],
        )

        self.assertTrue(doc is not None)

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_get_audience_name(self):
        """Test get audience name."""

        # Get audience name
        audience_name = am.get_audience_name(
            self.database,
            self.audience_doc[c.ID],
        )

        self.assertTrue(audience_name is not None)
        self.assertEqual(audience_name, "My Audience")

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_update_audience_name(self):
        """Test update audience name."""

        # Update audience name
        new_name = "New name"
        doc = am.update_audience_name(
            self.database,
            self.audience_doc[c.ID],
            new_name,
        )

        self.assertTrue(doc is not None)
        self.assertTrue(c.AUDIENCE_NAME in doc)
        self.assertEqual(doc[c.AUDIENCE_NAME], new_name)

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_update_audience_filters(self):
        """Test update audience filters."""

        # Update audience filters
        new_filters = []
        doc = am.update_audience_filters(
            self.database,
            self.audience_doc[c.ID],
            new_filters,
        )

        self.assertTrue(doc is not None)
        self.assertTrue(c.AUDIENCE_FILTERS in doc)
        self.assertEqual(doc[c.AUDIENCE_FILTERS], new_filters)

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_get_default_audience_id(self):
        """Test get_default_audience_id."""

        # Get the default audience ID given an ingestion job
        default_audience_id = am.get_default_audience_id(
            self.database,
            self.ingestion_job_doc[c.ID],
        )

        self.assertTrue(default_audience_id is not None)

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_get_ingestion_job_audience_ids(self):
        """Test get_ingestion_job_audience_ids."""

        # Get all audience IDs given an ingestion job
        audience_ids = am.get_ingestion_job_audience_ids(
            self.database,
            self.ingestion_job_doc[c.ID],
        )

        self.assertTrue(audience_ids is not None)

        default_audience_id = am.get_default_audience_id(
            self.database,
            self.ingestion_job_doc[c.ID],
        )

        self.assertEqual(len(audience_ids), 2)
        self.assertEqual(
            set(audience_ids),
            {default_audience_id, self.audience_doc[c.ID]},
        )

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_get_ingestion_job_audience_insights(self):
        """Test get_ingestion_job_audience_insights."""

        # Create insights
        audience_data, _ = am.get_audience(
            self.database,
            self.audience_doc[c.ID],
        )

        insights = am.append_audience_insights(
            self.database,
            self.audience_doc[c.ID],
            audience_data,
        )

        self.assertTrue(insights is not None)

        # Get all insights given an ingestion job
        all_insights = am.get_ingestion_job_audience_insights(
            self.database,
            self.ingestion_job_doc[c.ID],
        )

        self.assertTrue(all_insights is not None)
        self.assertEqual(len(all_insights), 1)
        self.assertEqual(
            all_insights[0][c.AUDIENCE_ID], self.audience_doc[c.ID]
        )

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_delete_audience_insights(self):
        """Test delete_job_audience_insights."""

        # Create insights
        audience_data, _ = am.get_audience(
            self.database,
            self.audience_doc[c.ID],
        )

        insights = am.append_audience_insights(
            self.database,
            self.audience_doc[c.ID],
            audience_data,
        )

        self.assertTrue(insights is not None)

        # Delete insights
        success_flag = am.delete_audience_insights(
            self.database,
            self.audience_doc[c.ID],
        )
        self.assertTrue(success_flag)

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_refresh_audience_insights(self):
        """Test refresh_job_audience_insights."""

        # Create insights
        audience_data, _ = am.get_audience(
            self.database,
            self.audience_doc[c.ID],
        )

        insights = am.append_audience_insights(
            self.database, self.audience_doc[c.ID], audience_data
        )

        self.assertTrue(insights is not None)

        # Refresh an audience's insights
        doc = am.refresh_audience_insights(
            self.database,
            self.audience_doc[c.ID],
        )
        self.assertTrue(doc is not None)

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_get_all_recent_audiences(self):
        """Test get_all_recent_audiences."""

        # Get audiences of all most recent ingestion jobs
        audiences = am.get_all_recent_audiences(self.database)

        self.assertTrue(audiences is not None)
        self.assertEqual(len(audiences), 2)

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_get_all_audiences(self):
        """Test get_all_audiences."""

        # Get all existing audiences
        audiences = am.get_all_audiences(self.database)

        self.assertTrue(audiences is not None)
        self.assertEqual(len(audiences), 2)

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_favorite_audience(self):
        """Test favorite_audience."""

        doc = am.favorite_audience(self.database, self.audience_doc[c.ID])

        self.assertTrue(doc is not None)
        self.assertTrue(c.FAVORITE in doc)
        self.assertTrue(doc[c.FAVORITE])

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_unfavorite_audience(self):
        """Test unfavorite_audience."""

        doc = am.unfavorite_audience(self.database, self.audience_doc[c.ID])

        self.assertTrue(doc is not None)
        self.assertTrue(c.FAVORITE in doc)
        self.assertTrue(not doc[c.FAVORITE])
