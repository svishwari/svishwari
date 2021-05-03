"""Database client cdp data source management tests"""

import unittest
import mongomock

import huxunifylib.database.cdp_data_source_management as dsmgmt
import huxunifylib.database.constants as c

from huxunifylib.database.client import DatabaseClient


class TestCdpDataSourceManagement(unittest.TestCase):
    """ Test cdp data source management module. """

    def setUp(self) -> None:
        # init mongo patch initially
        mongo_patch = mongomock.patch(servers=(("localhost", 27017),))
        mongo_patch.start()

        # Connect
        self.database = DatabaseClient(
            "localhost", 27017, None, None
        ).connect()

        self.database.drop_database(c.DATA_MANAGEMENT_DATABASE)

        self.sample_data_source = {
            c.CDP_DATA_SOURCE_FIELD_NAME: "Amazon",
            c.CDP_DATA_SOURCE_FIELD_CATEGORY: "Web Events",
            c.CDP_DATA_SOURCE_FIELD_FEED_COUNT: 1,
            c.CDP_DATA_SOURCE_FIELD_STATUS: "Pending",
        }

        # set a sample data source
        self.data_source_doc = dsmgmt.create_data_source(
            database=self.database,
            name=self.sample_data_source[c.CDP_DATA_SOURCE_FIELD_NAME],
            category=self.sample_data_source[c.CDP_DATA_SOURCE_FIELD_CATEGORY],
        )

    def test_create_data_source(self) -> None:
        """Test create data source routine

        Returns:
            Response: None

        """

        data_source_doc = dsmgmt.create_data_source(
            self.database, "Facebook", "Web Events"
        )

        self.assertTrue(data_source_doc is not None)

    def test_get_all_data_sources(self) -> None:
        """Test get all data sources routine

        Returns:
            Response: None
        """

        data_source_docs = dsmgmt.get_all_data_sources(self.database)

        self.assertIsNotNone(dsmgmt)

    def test_get_data_source(self) -> None:
        """Test get data source based on id

        Returns:
            Response: None
        """

        data_source_doc = dsmgmt.get_data_source(
            self.database, self.data_source_doc[c.ID]
        )

        self.assertTrue(data_source_doc is not None)
        self.assertEqual(
            data_source_doc[c.CDP_DATA_SOURCE_FIELD_NAME],
            self.data_source_doc[c.CDP_DATA_SOURCE_FIELD_NAME],
        )

    def test_delete_data_source(self) -> None:
        """Test delete data source based on id

        Returns:
            Response: None
        """

        # create a data source
        data_source_doc = dsmgmt.create_data_source(
            self.database, "Facebook", "Web Events"
        )

        self.assertTrue(c.ID in data_source_doc)

        # remove the data source
        success_flag = dsmgmt.delete_data_source(
            self.database, data_source_doc[c.ID]
        )
        self.assertTrue(success_flag)

        data_source_doc = dsmgmt.get_data_source(
            self.database, data_source_doc[c.ID]
        )
        self.assertIsNone(data_source_doc)
