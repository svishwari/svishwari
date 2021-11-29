"""Database client cdp data source management tests"""
import string
import unittest
import mongomock
from bson import ObjectId
from hypothesis import given, strategies as st

import huxunifylib.database.cdp_data_source_management as dsmgmt
import huxunifylib.database.constants as db_c

from huxunifylib.database.client import DatabaseClient


class TestCdpDataSourceManagement(unittest.TestCase):
    """Test CDP data source management module."""

    def setUp(self) -> None:
        # init mongo patch initially
        mongo_patch = mongomock.patch(servers=(("localhost", 27017),))
        mongo_patch.start()

        # Connect
        self.database = DatabaseClient(
            "localhost", 27017, None, None
        ).connect()

        self.database.drop_database(db_c.DATA_MANAGEMENT_DATABASE)

        self.sample_data_source = {
            db_c.CDP_DATA_SOURCE_FIELD_NAME: "Amazon",
            db_c.CDP_DATA_SOURCE_FIELD_CATEGORY: "Web Events",
            db_c.CDP_DATA_SOURCE_FIELD_FEED_COUNT: 1,
            db_c.CDP_DATA_SOURCE_FIELD_STATUS: db_c.CDP_DATA_SOURCE_STATUS_ACTIVE,
            db_c.DATA_SOURCE_TYPE: "Marketing",
        }

        # set a sample data source
        self.data_source_doc = dsmgmt.create_data_source(
            database=self.database,
            name=self.sample_data_source[db_c.CDP_DATA_SOURCE_FIELD_NAME],
            category=self.sample_data_source[db_c.CDP_DATA_SOURCE_FIELD_CATEGORY],
            source_type=self.sample_data_source[db_c.DATA_SOURCE_TYPE],
        )

    def test_create_data_source(self) -> None:
        """Test create data source routine"""

        data_source_doc = dsmgmt.create_data_source(
            self.database, "Facebook", "Web Events"
        )

        self.assertTrue(data_source_doc is not None)

    def test_get_all_data_sources(self) -> None:
        """Test get all data sources routine"""

        data_source_docs = dsmgmt.get_all_data_sources(self.database)

        self.assertIsNotNone(data_source_docs)

    def test_get_data_source(self) -> None:
        """Test get data source based on id"""

        data_source_doc = dsmgmt.get_data_source(
            self.database, self.data_source_doc[db_c.ID]
        )

        self.assertTrue(data_source_doc is not None)
        self.assertEqual(
            data_source_doc[db_c.CDP_DATA_SOURCE_FIELD_NAME],
            self.data_source_doc[db_c.CDP_DATA_SOURCE_FIELD_NAME],
        )
        data_source_doc = dsmgmt.get_data_source(
            self.database, data_source_type=self.data_source_doc[db_c.TYPE]
        )
        self.assertIsNotNone(data_source_doc)
        self.assertEqual(
            data_source_doc[db_c.CDP_DATA_SOURCE_FIELD_NAME],
            self.data_source_doc[db_c.CDP_DATA_SOURCE_FIELD_NAME],
        )

    def test_delete_data_source(self) -> None:
        """Test delete data source based on id"""

        # create a data source
        data_source_doc = dsmgmt.create_data_source(
            self.database, "Facebook", "Web Events"
        )

        self.assertTrue(db_c.ID in data_source_doc)

        # remove the data source
        success_flag = dsmgmt.delete_data_source(
            self.database, data_source_doc[db_c.ID]
        )
        self.assertTrue(success_flag)

        data_source_doc = dsmgmt.get_data_source(
            self.database, data_source_doc[db_c.ID]
        )
        self.assertIsNone(data_source_doc)

    @given(description=st.text(), data_source_name=st.text())
    def test_update_data_source(
        self, description: str, data_source_name: str
    ) -> None:
        """Test update data source.

        Args:
            description (str): random text.
            data_source_name (str): random text.

        """

        # create data source first
        data_source = dsmgmt.create_data_source(
            self.database, data_source_name, description
        )
        self.assertTrue(data_source)
        self.assertFalse(data_source[db_c.ADDED])
        self.assertFalse(data_source[db_c.ENABLED])

        # update data sources
        update_body = {"added": True, "enabled": True}
        self.assertTrue(
            dsmgmt.update_data_sources(
                self.database, [data_source[db_c.ID]], update_body
            )
        )

        # test values
        data_source = dsmgmt.get_data_source(self.database, data_source[db_c.ID])
        self.assertTrue(data_source[db_c.ADDED])
        self.assertTrue(data_source[db_c.ENABLED])

    @given(description=st.text(), data_source_name=st.text())
    def test_update_data_sources(
        self, description: str, data_source_name: str
    ) -> None:
        """Test update data sources.

        Args:
            description (str): random text.
            data_source_name (str): random text.

        """

        # create data source first
        data_source_ids = []
        for dsx in range(3):
            data_source = dsmgmt.create_data_source(
                self.database, f"{data_source_name}{dsx}", description
            )
            self.assertTrue(data_source)
            self.assertFalse(data_source[db_c.ADDED])
            self.assertFalse(data_source[db_c.ENABLED])
            data_source_ids.append(data_source[db_c.ID])

        # update data sources
        update_body = {"added": True, "enabled": True}
        self.assertTrue(
            dsmgmt.update_data_sources(
                self.database, data_source_ids, update_body
            )
        )

        # test values
        for data_source_id in data_source_ids:
            data_source = dsmgmt.get_data_source(self.database, data_source_id)
            self.assertTrue(data_source[db_c.ADDED])
            self.assertTrue(data_source[db_c.ENABLED])

    @given(st.lists(st.one_of(st.text(), st.floats(), st.none())))
    def test_update_data_source_bad_id(self, text: list) -> None:
        """Test update data sources with a bad id.

        Args:
            text (list): hypothesis list of random data.

        """

        with self.assertRaises(ValueError):
            dsmgmt.update_data_sources(
                self.database, [text], {db_c.ENABLED: True}
            )

    @given(
        st.dictionaries(
            keys=st.text(alphabet=string.ascii_letters),
            values=st.one_of(st.text(), st.floats()),
        )
    )
    def test_update_data_source_bad_update_dict(
        self, update_body: dict
    ) -> None:
        """Test update data sources with a bad data.

        Args:
            update_body (dict): hypothesis dict of random data.

        """

        # create data source first
        data_source = dsmgmt.create_data_source(
            self.database, "HypoDictTest", "Web Events"
        )
        self.assertTrue(data_source)
        self.assertFalse(data_source[db_c.ADDED])
        self.assertFalse(data_source[db_c.ENABLED])

        dsmgmt.update_data_sources(
            self.database, [data_source[db_c.ID]], update_body
        )

    def test_update_data_source_empty_list(self) -> None:
        """Test update data sources with an empty list."""

        with self.assertRaises(AttributeError):
            dsmgmt.update_data_sources(self.database, [], {db_c.ENABLED: True})

    def test_update_data_source_empty_update_dict(self) -> None:
        """Test update data sources with an empty update dict."""

        self.assertFalse(
            dsmgmt.update_data_sources(self.database, [ObjectId()], {})
        )

    def test_bulk_write_data_sources(self) -> None:
        """Test bulk write data sources"""

        data_sources = [
            {
                db_c.NAME: "Data source 1",
                db_c.TYPE: "dataSource1",
                db_c.STATUS: "Active",
            },
            {
                db_c.NAME: "Data source 2",
                db_c.TYPE: "dataSource2",
                db_c.STATUS: "Pending",
            },
        ]

        # create data sources
        created_data_sources = dsmgmt.bulk_write_data_sources(
            self.database, data_sources
        )

        self.assertCountEqual(created_data_sources, data_sources)

        for data_source in created_data_sources:
            self.assertIn(db_c.NAME, data_source)
            self.assertIn(db_c.TYPE, data_source)
            self.assertIn(db_c.STATUS, data_source)
            self.assertIn(db_c.ADDED, data_source)
            self.assertTrue(db_c.ADDED)

    def test_bulk_delete_data_sources(self) -> None:
        """Test bulk delete data sources"""
        # create data source first
        data_sources = [
            {
                db_c.NAME: "Data source 1",
                db_c.TYPE: "dataSource1",
                db_c.STATUS: "Active",
            },
            {
                db_c.NAME: "Data source 2",
                db_c.TYPE: "dataSource2",
                db_c.STATUS: "Pending",
            },
        ]

        # create data sources
        created_data_sources = dsmgmt.bulk_write_data_sources(
            self.database, data_sources
        )

        self.assertTrue(
            dsmgmt.bulk_delete_data_sources(
                self.database, [x[db_c.TYPE] for x in created_data_sources]
            )
        )
