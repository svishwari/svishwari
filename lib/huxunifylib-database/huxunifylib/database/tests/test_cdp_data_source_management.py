"""Database client cdp data source management tests"""
import string
import unittest
import mongomock
from bson import ObjectId
from hypothesis import given, strategies as st

import huxunifylib.database.cdp_data_source_management as dsmgmt
import huxunifylib.database.constants as c

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

        self.database.drop_database(c.DATA_MANAGEMENT_DATABASE)

        self.sample_data_source = {
            c.CDP_DATA_SOURCE_FIELD_NAME: "Amazon",
            c.CDP_DATA_SOURCE_FIELD_CATEGORY: "Web Events",
            c.CDP_DATA_SOURCE_FIELD_FEED_COUNT: 1,
            c.CDP_DATA_SOURCE_FIELD_STATUS: c.CDP_DATA_SOURCE_STATUS_ACTIVE,
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

        self.assertIsNotNone(data_source_docs)

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

    @given(description=st.text(), data_source_name=st.text())
    def test_update_data_source(
        self, description: str, data_source_name: str
    ) -> None:
        """Test update data source.

        Args:
            description (str): random text.
            data_source_name (str): random text.

        Returns:
            Response: None

        """

        # create data source first
        data_source = dsmgmt.create_data_source(
            self.database, data_source_name, description
        )
        self.assertTrue(data_source)
        self.assertFalse(data_source[c.ADDED])
        self.assertFalse(data_source[c.ENABLED])

        # update data sources
        update_body = {"added": True, "enabled": True}
        self.assertTrue(
            dsmgmt.update_data_sources(
                self.database, [data_source[c.ID]], update_body
            )
        )

        # test values
        data_source = dsmgmt.get_data_source(self.database, data_source[c.ID])
        self.assertTrue(data_source[c.ADDED])
        self.assertTrue(data_source[c.ENABLED])

    @given(description=st.text(), data_source_name=st.text())
    def test_update_data_sources(
        self, description: str, data_source_name: str
    ) -> None:
        """Test update data sources.

        Args:
            description (str): random text.
            data_source_name (str): random text.

        Returns:
            Response: None

        """

        # create data source first
        data_source_ids = []
        for dsx in range(3):
            data_source = dsmgmt.create_data_source(
                self.database, f"{data_source_name}{dsx}", description
            )
            self.assertTrue(data_source)
            self.assertFalse(data_source[c.ADDED])
            self.assertFalse(data_source[c.ENABLED])
            data_source_ids.append(data_source[c.ID])

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
            self.assertTrue(data_source[c.ADDED])
            self.assertTrue(data_source[c.ENABLED])

    @given(st.lists(st.one_of(st.text(), st.floats(), st.none())))
    def test_update_data_source_bad_id(self, text: list) -> None:
        """Test update data sources with a bad id.

        Args:
            text (list): hypothesis list of random data.

        Returns:
            Response: None

        """

        with self.assertRaises(ValueError):
            dsmgmt.update_data_sources(
                self.database, [text], {c.ENABLED: True}
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

        Returns:
            Response: None

        """

        # create data source first
        data_source = dsmgmt.create_data_source(
            self.database, "HypoDictTest", "Web Events"
        )
        self.assertTrue(data_source)
        self.assertFalse(data_source[c.ADDED])
        self.assertFalse(data_source[c.ENABLED])

        dsmgmt.update_data_sources(
            self.database, [data_source[c.ID]], update_body
        )

    def test_update_data_source_empty_list(self) -> None:
        """Test update data sources with an empty list.

        Args:

        Returns:
            Response: None

        """

        with self.assertRaises(AttributeError):
            dsmgmt.update_data_sources(self.database, [], {c.ENABLED: True})

    def test_update_data_source_empty_update_dict(self) -> None:
        """Test update data sources with an empty update dict.

        Returns:
            Response: None

        """

        self.assertFalse(
            dsmgmt.update_data_sources(self.database, [ObjectId()], {})
        )
