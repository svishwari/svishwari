"""Test Module for Pre-populate Database Script."""
from unittest import TestCase, mock
import mongomock
from huxunifylib.database import constants as db_c
from huxunifylib.database.cdp_data_source_management import (
    get_all_data_sources,
)
from huxunifylib.database.collection_management import get_documents
from huxunifylib.database.delivery_platform_management import (
    get_all_delivery_platforms,
)
import database.prepopulate_database as pd


class TestPrepopulateDatabase(TestCase):
    """Test the DB Indexes creation"""

    def setUp(self):
        """Initial Test Case Setup."""

        mongo_patch = mongomock.patch(servers=(("localhost", 27017),))
        mongo_patch.start()

        # setup the mock DB client
        self.database = mongomock.MongoClient("localhost", 27017)

        self.addCleanup(mock.patch.stopall)

    def test_drop_collection(self):
        """Unit Test for set Indexes."""

        pd.drop_collections(self.database)
        collections = self.database[
            db_c.DATA_MANAGEMENT_DATABASE
        ].list_collection_names()

        self.assertNotIn(db_c.DATA_SOURCES_COLLECTION, collections)

    def test_insert_data_sources(self):
        """Unit Test for set Indexes."""

        data_sources = [
            {
                db_c.DATA_SOURCE_NAME: "Bluecore",
                db_c.DATA_SOURCE_TYPE: "bluecore",
                db_c.STATUS: db_c.ACTIVE,
                db_c.ENABLED: True,
                db_c.ADDED: True,
            },
            {
                db_c.DATA_SOURCE_NAME: "NetSuite",
                db_c.DATA_SOURCE_TYPE: "netsuite",
                db_c.STATUS: db_c.PENDING,
                db_c.ENABLED: True,
                db_c.ADDED: False,
            },
        ]

        pd.insert_data_sources(self.database, data_sources)
        list_sources = get_all_data_sources(self.database)

        list_src_names = [x["name"] for x in list_sources]
        _ = [self.assertIn(x["name"], list_src_names) for x in data_sources]

    def test_insert_delivery_platforms(self):
        """Unit Test for set Indexes."""

        delivery_platforms = [
            {
                db_c.DELIVERY_PLATFORM_NAME: "Salesforce Marketing Cloud",
                db_c.DELIVERY_PLATFORM_TYPE: db_c.DELIVERY_PLATFORM_SFMC,
                db_c.STATUS: db_c.ACTIVE,
                db_c.ENABLED: True,
                db_c.ADDED: False,
            },
            {
                db_c.DELIVERY_PLATFORM_NAME: "Facebook",
                db_c.DELIVERY_PLATFORM_TYPE: db_c.DELIVERY_PLATFORM_FACEBOOK,
                db_c.STATUS: db_c.ACTIVE,
                db_c.ENABLED: True,
                db_c.ADDED: False,
            },
        ]

        pd.insert_delivery_platforms(self.database, delivery_platforms)

        list_delivery_platforms = get_all_delivery_platforms(self.database)
        list_delivery_platform_names = [
            x["name"] for x in list_delivery_platforms
        ]
        _ = [
            self.assertIn(x["name"], list_delivery_platform_names)
            for x in delivery_platforms
        ]

    def test_empty_collection_creation(self):
        """Test creation of empty collection."""

        collection_names = [
            db_c.AUDIENCE_CUSTOMERS_COLLECTION,
            db_c.AUDIENCE_INSIGHTS_COLLECTION,
            db_c.AUDIENCES_COLLECTION,
            db_c.AUDIENCE_AUDIT_COLLECTION,
            db_c.CACHE_COLLECTION,
            db_c.CAMPAIGN_ACTIVITY_COLLECTION,
            db_c.DELIVERABILITY_METRICS_COLLECTION,
            db_c.DELIVERY_JOBS_COLLECTION,
            db_c.ENGAGEMENTS_COLLECTION,
            db_c.INGESTED_DATA_COLLECTION,
            db_c.INGESTED_DATA_STATS_COLLECTION,
            db_c.INGESTION_JOBS_COLLECTION,
            db_c.LOOKALIKE_AUDIENCE_COLLECTION,
            db_c.NOTIFICATIONS_COLLECTION,
            db_c.PERFORMANCE_METRICS_COLLECTION,
            db_c.SURVEY_METRICS_COLLECTION,
            db_c.USER_COLLECTION,
        ]
        pd.create_empty_collections(
            mongo_client=self.database, collection_names=collection_names
        )

        collections = self.database[
            db_c.DATA_MANAGEMENT_DATABASE
        ].list_collection_names()

        self.assertTrue(collections)

        for collection_name in collection_names:
            self.assertIn(collection_name, collections)

        for collection_name in collection_names:
            documents = get_documents(self.database, collection_name)
            self.assertEqual(0, documents["total_records"])
