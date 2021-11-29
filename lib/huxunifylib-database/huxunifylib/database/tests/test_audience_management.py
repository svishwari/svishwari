"""Audience Management tests."""

import unittest
from typing import Union

import mongomock
import pandas as pd
import huxunifylib.database.audience_management as am
import huxunifylib.database.data_management as dm
import huxunifylib.database.constants as db_c
from huxunifylib.database import delete_util
from huxunifylib.database.client import DatabaseClient


# pylint: disable=R0904
class TestAudienceManagement(unittest.TestCase):
    """Test audience management module."""

    @mongomock.patch(servers=(("localhost", 27017),))
    def setUp(self):

        self.database = DatabaseClient(
            "localhost", 27017, None, None
        ).connect()
        self.database.drop_database(db_c.DATA_MANAGEMENT_DATABASE)

        self.data_source_params = [
            "My data source",
            1,
            "CSV",
            "S3",
            None,
            None,
        ]

        self.ingested_data_frame = pd.DataFrame(
            {
                db_c.S_TYPE_FIRST_NAME: [
                    "first_name_10",
                    "first_name_20",
                    "first_name_30",
                    "first_name_40",
                ],
                db_c.S_TYPE_LAST_NAME: [
                    "last_name_10",
                    "last_name_20",
                    "last_name_30",
                    "last_name_40",
                ],
                db_c.S_TYPE_EMAIL: [
                    "email_10",
                    "email_20",
                    "email_30",
                    "email_40",
                ],
                db_c.S_TYPE_CITY: [
                    "New York",
                    "London",
                    "San Francisco",
                    "Chicago",
                ],
                db_c.S_TYPE_COUNTRY_CODE: ["US", "UK", "US", "US"],
                db_c.S_TYPE_STATE_OR_PROVINCE: ["NY", None, "CA", "IL"],
                db_c.S_TYPE_GENDER: ["m", "f", None, "m"],
                db_c.S_TYPE_AGE: [33, 28, 64, 59],
                "custom_field": ["val_10", "val_20", "val_30", "val_40"],
            }
        )

        self.new_data_frame = pd.DataFrame(
            {
                db_c.S_TYPE_FIRST_NAME: [
                    "first_name_50",
                    "first_name_60",
                ],
                db_c.S_TYPE_LAST_NAME: [
                    "last_name_50",
                    "last_name_60",
                ],
                db_c.S_TYPE_EMAIL: [
                    "email_50",
                    "email_60",
                ],
                db_c.S_TYPE_AGE: [43, 48],
                "new_custom_field": ["new_val_50", "new_val_60"],
            }
        )

        self.audience_filters = [
            {
                "field": db_c.S_TYPE_AGE,
                "type": db_c.AUDIENCE_FILTER_MAX,
                "value": 60,
            },
            {
                "field": db_c.S_TYPE_COUNTRY_CODE,
                "type": db_c.AUDIENCE_FILTER_INCLUDE,
                "value": "US",
            },
            {
                "field": db_c.S_TYPE_CITY,
                "type": db_c.AUDIENCE_FILTER_EXCLUDE,
                "value": ["London"],
            },
        ]

        self.ingestion_job_doc = None
        self.audience_doc = None

    def _setup_ingestion_job(self) -> dict:
        """Setup ingestion job

        Returns:
            ingestion_job_doc (dict): Ingestion job document

        """
        data_source_doc = dm.set_data_source(
            self.database, *self.data_source_params
        )
        ingestion_job_doc = dm.set_ingestion_job(
            self.database, data_source_doc[db_c.ID]
        )
        return ingestion_job_doc

    def _setup_audience(self) -> Union[tuple, dict]:
        """Setup audience

        Returns:
            audience_doc (dict): Audience document
            ingestion_job_doc (dict): Ingestion job document

        """
        ingestion_job_doc = self._setup_ingestion_job()
        ingestion_job_id = ingestion_job_doc[db_c.ID]

        dm.append_ingested_data(
            self.database, ingestion_job_id, self.ingested_data_frame
        )
        dm.append_ingested_data(
            self.database, ingestion_job_id, self.new_data_frame
        )
        audience_doc = am.create_audience(
            self.database,
            "My Audience",
            self.audience_filters,
            ingestion_job_id,
        )
        return audience_doc, ingestion_job_doc

    def _setup_ingestion_succeeded_and_audience(self) -> None:

        ingestion_job_doc = self._setup_ingestion_job()
        ingestion_job_id = ingestion_job_doc[db_c.ID]

        dm.append_ingested_data(
            self.database, ingestion_job_id, self.ingested_data_frame
        )
        dm.append_ingested_data(
            self.database, ingestion_job_id, self.new_data_frame
        )
        self.ingestion_job_doc = am.set_ingestion_job_status(
            self.database, ingestion_job_id, db_c.STATUS_SUCCEEDED
        )
        self.audience_doc = am.create_audience(
            self.database,
            "My Audience",
            self.audience_filters,
            ingestion_job_id,
        )

    def test_set_ingestion_job(self):
        """Ingestion job created and status is set."""

        ingestion_job_doc = self._setup_ingestion_job()

        self.assertTrue(ingestion_job_doc is not None)
        self.assertTrue(db_c.ID in ingestion_job_doc)

        ingestion_job_id = ingestion_job_doc[db_c.ID]
        doc = am.set_ingestion_job_status(
            self.database, ingestion_job_id, db_c.STATUS_SUCCEEDED
        )
        self.assertTrue(doc is not None)
        self.assertTrue(db_c.JOB_STATUS in doc)
        self.assertTrue(db_c.JOB_END_TIME in doc)

        success_flag = dm.append_ingested_data(
            self.database, ingestion_job_id, self.ingested_data_frame
        )
        self.assertTrue(success_flag)

        success_flag = dm.append_ingested_data(
            self.database, ingestion_job_id, self.new_data_frame
        )
        self.assertTrue(success_flag)

    def test_set_audience(self):
        """Audience is set."""

        audience_doc, _ = self._setup_audience()

        self.assertTrue(audience_doc is not None)
        self.assertTrue(db_c.ID in audience_doc)
        self.assertFalse(db_c.DELETED in audience_doc)

    def test_audience_count(self):
        """Created audiences are counted properly."""

        _, ingestion_job_doc = self._setup_audience()
        ingestion_job_id = ingestion_job_doc[db_c.ID]

        doc = am.create_audience(
            self.database,
            "My Audience new",
            self.audience_filters,
            ingestion_job_id,
        )

        self.assertTrue(doc is not None)

        # Two explicitly created audiences before ingestion job success
        count = am.get_audiences_count(database=self.database)
        self.assertEqual(count, 2)

    def test_get_audience(self):
        """Test get audiences."""

        self._setup_ingestion_succeeded_and_audience()

        audience_data_1, next_start_id = am.get_audience(
            self.database,
            self.audience_doc[db_c.ID],
            None,
            1,
        )

        self.assertEqual(audience_data_1.shape[0], 1)
        self.assertTrue(db_c.S_TYPE_CUSTOMER_ID in audience_data_1.columns)

        audience_data_2, next_start_id = am.get_audience(
            self.database,
            self.audience_doc[db_c.ID],
            next_start_id,
            1,
        )

        self.assertEqual(audience_data_2.shape[0], 1)
        self.assertTrue(db_c.S_TYPE_CUSTOMER_ID in audience_data_1.columns)

        audience_data = pd.concat([audience_data_1, audience_data_2])

        self.assertTrue(audience_data is not None)

        self.assertEqual(audience_data.shape[0], 2)
        self.assertEqual(set(audience_data[db_c.S_TYPE_COUNTRY_CODE]), {"US"})
        self.assertEqual(
            set(audience_data[db_c.S_TYPE_CITY]), {"New York", "Chicago"}
        )
        self.assertEqual(set(audience_data[db_c.S_TYPE_AGE]), {33, 59})

    def test_get_audience_batches(self):
        """Test get audiences in batches."""

        self._setup_ingestion_succeeded_and_audience()

        fetch = am.get_audience_batches(
            self.database, self.audience_doc[db_c.ID], 1
        )

        for audience_batch in fetch:
            self.assertEqual(audience_batch.shape[0], 1)

        fetch = am.get_audience_batches(
            self.database, self.audience_doc[db_c.ID], 2
        )

        for audience_batch in fetch:
            self.assertEqual(audience_batch.shape[0], 2)

    def test_delete_audience(self):
        """Test delete audiences."""

        self._setup_ingestion_succeeded_and_audience()

        # count of audiences documents after soft deletion
        success_flag = delete_util.delete_audience(
            self.database, self.audience_doc[db_c.ID]
        )
        self.assertTrue(success_flag)

    # pylint: disable=R0915
    def test_append_audience_insights(self):
        """Test append audience insights."""

        self._setup_ingestion_succeeded_and_audience()

        audience_data, _ = am.get_audience(
            self.database,
            self.audience_doc[db_c.ID],
        )

        insights = am.append_audience_insights(
            self.database, self.audience_doc[db_c.ID], audience_data
        )

        self.assertTrue(insights is not None)
        self.assertTrue(db_c.AUDIENCE_ID in insights)
        self.assertEqual(
            insights[db_c.AUDIENCE_ID], self.audience_doc[db_c.ID]
        )
        self.assertTrue(db_c.S_TYPE_CITY in insights)
        self.assertTrue(db_c.S_TYPE_COUNTRY_CODE in insights)
        self.assertTrue(db_c.S_TYPE_STATE_OR_PROVINCE in insights)
        self.assertTrue(db_c.S_TYPE_GENDER in insights)
        self.assertTrue(db_c.S_TYPE_AGE in insights)
        self.assertTrue(db_c.STATS_COVERAGE in insights[db_c.S_TYPE_CITY])
        self.assertTrue(
            db_c.STATS_COVERAGE in insights[db_c.S_TYPE_COUNTRY_CODE]
        )
        self.assertTrue(
            db_c.STATS_COVERAGE in insights[db_c.S_TYPE_STATE_OR_PROVINCE]
        )
        self.assertTrue(db_c.STATS_COVERAGE in insights[db_c.S_TYPE_GENDER])
        self.assertTrue(db_c.STATS_COVERAGE in insights[db_c.S_TYPE_AGE])
        self.assertTrue(db_c.STATS_BREAKDOWN in insights[db_c.S_TYPE_CITY])
        self.assertTrue(
            db_c.STATS_BREAKDOWN in insights[db_c.S_TYPE_COUNTRY_CODE]
        )
        self.assertTrue(
            db_c.STATS_BREAKDOWN in insights[db_c.S_TYPE_STATE_OR_PROVINCE]
        )
        self.assertTrue(db_c.STATS_BREAKDOWN in insights[db_c.S_TYPE_GENDER])
        self.assertTrue(db_c.STATS_BREAKDOWN in insights[db_c.S_TYPE_AGE])
        self.assertTrue(
            db_c.STATS_BREAKDOWN not in insights[db_c.S_TYPE_FIRST_NAME]
        )
        self.assertTrue(
            db_c.STATS_BREAKDOWN not in insights[db_c.S_TYPE_LAST_NAME]
        )
        self.assertTrue(
            db_c.STATS_BREAKDOWN not in insights[db_c.S_TYPE_EMAIL]
        )

        self.assertEqual(insights[db_c.DATA_COUNT], 2)
        self.assertEqual(
            insights[db_c.S_TYPE_CITY],
            {"coverage": 1.0, "breakdown": {"New York": 0.5, "Chicago": 0.5}},
        )
        self.assertEqual(
            insights[db_c.S_TYPE_GENDER],
            {"coverage": 1.0, "breakdown": {"m": 1.0}},
        )

        # Append more data to insights
        new_audience_data = pd.DataFrame(
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
                db_c.S_TYPE_CITY: ["New York", "Chicago", "San Francisco"],
                db_c.S_TYPE_COUNTRY_CODE: ["US", "US", "US"],
                db_c.S_TYPE_STATE_OR_PROVINCE: ["NY", "IL", "CA"],
                db_c.S_TYPE_GENDER: ["m", "f", "f"],
                db_c.S_TYPE_AGE: [59, 50, 35],
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
            self.audience_doc[db_c.ID],
            new_audience_data,
            ["custom_field", "custom_field_extra"],
        )

        assert insights is not None

        self.assertTrue(insights is not None)
        self.assertTrue(db_c.AUDIENCE_ID in insights)
        self.assertEqual(
            insights[db_c.AUDIENCE_ID], self.audience_doc[db_c.ID]
        )
        self.assertTrue(db_c.S_TYPE_CITY in insights)
        self.assertTrue(db_c.S_TYPE_COUNTRY_CODE in insights)
        self.assertTrue(db_c.S_TYPE_STATE_OR_PROVINCE in insights)
        self.assertTrue(db_c.S_TYPE_GENDER in insights)
        self.assertTrue(db_c.S_TYPE_AGE in insights)
        self.assertTrue("custom_field" in insights)
        self.assertTrue("custom_field_extra" in insights)
        self.assertTrue(db_c.STATS_COVERAGE in insights[db_c.S_TYPE_CITY])
        self.assertTrue(
            db_c.STATS_COVERAGE in insights[db_c.S_TYPE_COUNTRY_CODE]
        )
        self.assertTrue(
            db_c.STATS_COVERAGE in insights[db_c.S_TYPE_STATE_OR_PROVINCE]
        )
        self.assertTrue(db_c.STATS_COVERAGE in insights[db_c.S_TYPE_GENDER])
        self.assertTrue(db_c.STATS_COVERAGE in insights[db_c.S_TYPE_AGE])
        self.assertTrue(db_c.STATS_BREAKDOWN in insights[db_c.S_TYPE_CITY])
        self.assertTrue(
            db_c.STATS_BREAKDOWN in insights[db_c.S_TYPE_COUNTRY_CODE]
        )
        self.assertTrue(
            db_c.STATS_BREAKDOWN in insights[db_c.S_TYPE_STATE_OR_PROVINCE]
        )
        self.assertTrue(db_c.STATS_BREAKDOWN in insights[db_c.S_TYPE_GENDER])
        self.assertTrue(db_c.STATS_BREAKDOWN in insights[db_c.S_TYPE_AGE])
        self.assertTrue(db_c.STATS_BREAKDOWN in insights["custom_field"])
        self.assertTrue(db_c.STATS_BREAKDOWN in insights["custom_field_extra"])
        self.assertTrue(
            db_c.STATS_BREAKDOWN not in insights[db_c.S_TYPE_FIRST_NAME]
        )
        self.assertTrue(
            db_c.STATS_BREAKDOWN not in insights[db_c.S_TYPE_LAST_NAME]
        )
        self.assertTrue(
            db_c.STATS_BREAKDOWN not in insights[db_c.S_TYPE_EMAIL]
        )

        self.assertEqual(insights[db_c.DATA_COUNT], 5)
        self.assertEqual(
            insights[db_c.S_TYPE_CITY],
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
            self.audience_doc[db_c.ID],
        )

        self.assertTrue(stored_insights is not None)
        self.assertEqual(stored_insights, insights)

    def test_get_audience_config(self):
        """Test get audience config."""

        self._setup_ingestion_succeeded_and_audience()

        # Get audience configuration
        doc = am.get_audience_config(
            self.database,
            self.audience_doc[db_c.ID],
        )

        self.assertTrue(doc is not None)
        self.assertFalse(db_c.DELETED in doc)

    def test_get_audience_name(self):
        """Test get audience name."""

        self._setup_ingestion_succeeded_and_audience()

        # Get audience name
        audience_name = am.get_audience_name(
            self.database,
            self.audience_doc[db_c.ID],
        )

        self.assertTrue(audience_name is not None)
        self.assertEqual(audience_name, "My Audience")

    def test_update_audience_name(self):
        """Test update audience name."""

        self._setup_ingestion_succeeded_and_audience()

        # Update audience name
        new_name = "New name"
        doc = am.update_audience_name(
            self.database,
            self.audience_doc[db_c.ID],
            new_name,
        )

        self.assertTrue(doc is not None)
        self.assertTrue(db_c.AUDIENCE_NAME in doc)
        self.assertEqual(doc[db_c.AUDIENCE_NAME], new_name)

    def test_update_audience_filters(self):
        """Test update audience filters."""

        self._setup_ingestion_succeeded_and_audience()

        # Update audience filters
        new_filters = []
        doc = am.update_audience_filters(
            self.database,
            self.audience_doc[db_c.ID],
            new_filters,
        )

        self.assertTrue(doc is not None)
        self.assertTrue(db_c.AUDIENCE_FILTERS in doc)
        self.assertEqual(doc[db_c.AUDIENCE_FILTERS], new_filters)

    def test_get_ingestion_job_audience_ids(self):
        """Test get_ingestion_job_audience_ids."""

        self._setup_ingestion_succeeded_and_audience()

        # Get all audience IDs given an ingestion job
        audience_ids = am.get_ingestion_job_audience_ids(
            self.database,
            self.ingestion_job_doc[db_c.ID],
        )

        self.assertTrue(audience_ids is not None)

    def test_get_ingestion_job_audience_insights(self):
        """Test get_ingestion_job_audience_insights."""

        self._setup_ingestion_succeeded_and_audience()

        # Create insights
        audience_data, _ = am.get_audience(
            self.database,
            self.audience_doc[db_c.ID],
        )

        insights = am.append_audience_insights(
            self.database,
            self.audience_doc[db_c.ID],
            audience_data,
        )

        self.assertTrue(insights is not None)

        # Get all insights given an ingestion job
        all_insights = am.get_ingestion_job_audience_insights(
            self.database,
            self.ingestion_job_doc[db_c.ID],
        )

        self.assertTrue(all_insights is not None)
        self.assertEqual(len(all_insights), 1)
        self.assertEqual(
            all_insights[0][db_c.AUDIENCE_ID], self.audience_doc[db_c.ID]
        )

    def test_delete_audience_insights(self):
        """Test delete_job_audience_insights."""

        self._setup_ingestion_succeeded_and_audience()

        # Create insights
        audience_data, _ = am.get_audience(
            self.database,
            self.audience_doc[db_c.ID],
        )

        insights = am.append_audience_insights(
            self.database,
            self.audience_doc[db_c.ID],
            audience_data,
        )

        self.assertTrue(insights is not None)

        # Delete insights
        success_flag = am.delete_audience_insights(
            self.database,
            self.audience_doc[db_c.ID],
        )
        self.assertTrue(success_flag)

    def test_refresh_audience_insights(self):
        """Test refresh_job_audience_insights."""

        self._setup_ingestion_succeeded_and_audience()

        # Create insights
        audience_data, _ = am.get_audience(
            self.database,
            self.audience_doc[db_c.ID],
        )

        insights = am.append_audience_insights(
            self.database, self.audience_doc[db_c.ID], audience_data
        )

        self.assertTrue(insights is not None)

        # Refresh an audience's insights
        doc = am.refresh_audience_insights(
            self.database,
            self.audience_doc[db_c.ID],
        )
        self.assertTrue(doc is not None)

    def test_get_all_recent_audiences(self):
        """Test get_all_recent_audiences."""

        self._setup_ingestion_succeeded_and_audience()

        # Get audiences of all most recent ingestion jobs
        audiences = am.get_all_recent_audiences(self.database)

        self.assertIsNotNone(audiences)
        self.assertEqual(len(audiences), 1)
        self.assertFalse([a for a in audiences if db_c.DELETED in a])

    def test_get_all_audiences(self):
        """Test get_all_audiences."""

        self._setup_ingestion_succeeded_and_audience()

        # Get all existing audiences
        audiences = am.get_all_audiences(self.database)

        self.assertIsNotNone(audiences)
        self.assertEqual(len(audiences), 1)
        self.assertFalse([a for a in audiences if db_c.DELETED in a])

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_favorite_audience(self):
        """Test favorite_audience."""

        self._setup_ingestion_succeeded_and_audience()

        doc = am.favorite_audience(self.database, self.audience_doc[db_c.ID])

        self.assertTrue(doc is not None)
        self.assertTrue(db_c.FAVORITE in doc)
        self.assertTrue(doc[db_c.FAVORITE])

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_unfavorite_audience(self):
        """Test unfavorite_audience."""

        self._setup_ingestion_succeeded_and_audience()

        doc = am.unfavorite_audience(self.database, self.audience_doc[db_c.ID])

        self.assertTrue(doc is not None)
        self.assertTrue(db_c.FAVORITE in doc)
        self.assertTrue(not doc[db_c.FAVORITE])

    def test_update_audience_status(self):
        """Test update audience status."""

        self._setup_ingestion_succeeded_and_audience()

        # Update audience name
        doc = am.update_audience_status_for_delivery(
            self.database,
            self.audience_doc[db_c.ID],
            db_c.AUDIENCE_STATUS_DELIVERING,
        )

        self.assertIsNotNone(doc)
        self.assertIn(db_c.AUDIENCE_STATUS, doc)
        self.assertEqual(
            doc[db_c.AUDIENCE_STATUS], db_c.AUDIENCE_STATUS_DELIVERING
        )
