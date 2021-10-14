"""Test Module for Prepopulate Database Script"""
from unittest import TestCase, mock
import mongomock
from huxunifylib.database import constants as c
from huxunifylib.database.cdp_data_source_management import (
    get_all_data_sources,
)
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
        collection_names = self.database[
            c.DATA_MANAGEMENT_DATABASE
        ].list_collection_names()
        self.assertNotIn(c.DELIVERY_PLATFORM_COLLECTION, collection_names)

    def test_insert_data_sources(self):
        """Unit Test for set Indexes."""

        data_sources = [
            {
                c.DATA_SOURCE_NAME: "Bluecore",
                c.DATA_SOURCE_TYPE: "bluecore",
                c.STATUS: c.ACTIVE,
                c.ENABLED: True,
                c.ADDED: True,
            },
            {
                c.DATA_SOURCE_NAME: "NetSuite",
                c.DATA_SOURCE_TYPE: "netsuite",
                c.STATUS: c.PENDING,
                c.ENABLED: True,
                c.ADDED: False,
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
                c.DELIVERY_PLATFORM_NAME: "Salesforce Marketing Cloud",
                c.DELIVERY_PLATFORM_TYPE: c.DELIVERY_PLATFORM_SFMC,
                c.STATUS: c.ACTIVE,
                c.ENABLED: True,
                c.ADDED: False,
            },
            {
                c.DELIVERY_PLATFORM_NAME: "Facebook",
                c.DELIVERY_PLATFORM_TYPE: c.DELIVERY_PLATFORM_FACEBOOK,
                c.STATUS: c.ACTIVE,
                c.ENABLED: True,
                c.ADDED: False,
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
