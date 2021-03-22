"""
Purpose of this file is testing the cdm model class
"""
from unittest import TestCase
from unittest.mock import Mock

from huxunify.api.data_connectors.snowflake_client import SnowflakeClient
from huxunify.api.model.cdm import CdmModel


class CdmTest(TestCase):
    """
    Test CDM database querying
    """

    def setUp(self):
        """
        Setup initial model and database connection
        """
        mock_client = Mock(spec=SnowflakeClient)
        self.model = CdmModel(mock_client)

    def test_get_datasources(self):
        """
        Successfully retrieve datasources
        """
        self.model.ctx.cursor().fetchall.return_value = [
            ["test_src", "test_file", "test_count"]
        ]
        data_sources = self.model.get_data_sources()
        self.assertEqual(len(data_sources), 1)

    def test_read_datafeeds(self):
        """
        Successfully retrieve datafeeds
        """
        feeds = [
            ["feed1", "feed_type1", "source1", "data_type1", ".test1", "Y", "false"],
            ["feed2", "feed_type2", "source2", "data_type2", ".test2", "Y", "false"],
        ]

        self.model.ctx.cursor().fetchall.return_value = feeds
        returned_feeds = self.model.read_datafeeds()
        self.assertEqual(2, len(returned_feeds))
        self.assertEqual("feed_type1", returned_feeds[0]["feed_type"])
        self.assertEqual("feed_type2", returned_feeds[1]["feed_type"])

    def test_read_datafeeds_by_id(self):
        """
        Successfully retrieve single datafeed
        """
        feed = ["feed1", "feed_type1", "source1", "data_type1", ".test2", "Y", "false"]
        self.model.ctx.cursor().fetchone.return_value = feed

        returned_feed = self.model.read_datafeed_by_id(1)
        self.assertEqual("feed_type1", returned_feed["feed_type"])

    def test_read_fieldmappings(self):
        """
        Successfully retrieve field mappings
        """
        mappings = [
            ["id1", "name1", "variation1", "True"],
            ["id2", "name2", "variation2", "True"],
        ]
        self.model.ctx.cursor().fetchall.return_value = mappings

        returned_mappings = self.model.read_fieldmappings()
        self.assertEqual(2, len(returned_mappings))
        self.assertEqual("id1", returned_mappings[0]["field_id"])
        self.assertEqual("id2", returned_mappings[1]["field_id"])

    def test_read_fieldmappings_by_id(self):
        """
        Succesfully retrieve field mappings by id
        """
        mapping = ["id1", "name1", "variation1", "True"]
        self.model.ctx.cursor().fetchone.return_value = mapping

        returned_mapping = self.model.read_fieldmapping_by_id(1)
        self.assertEqual("id1", returned_mapping["field_id"])
