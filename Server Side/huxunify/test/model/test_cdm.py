"""
Purpose of this file is testing the cdm model class
"""
from unittest import TestCase
from unittest.mock import patch, MagicMock
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
        print("Initializing ....")
        self.model = CdmModel()

    # @patch('snowflake.connector.connect.cursor')
    @patch('huxunify.api.data_connectors.snowflake_client.SnowflakeClient')
    def test_get_datasources(self, mock_client):
        """
        Successfully retrieve datasources
        """
        # mock_cursor.fetchall = MagicMock(return_value=('test_src', 'test_file', 'test_count'))
        data_sources = self.model.get_data_sources()
        print(data_sources)
        self.assertEqual(len(data_sources), 1)

    @patch('huxunify.api.data_connectors.snowflake_client.SnowflakeClient')
    def test_read_datafeeds(self, mock_client):
        """
        Successfully retrieve datafeeds
        """
        feeds = [('feed1', 'feed_type', 'source1', 'data_type', '.test', 'Y', 'false'),
                 ('feed2', 'feed_type', 'source2', 'data_type', '.test', 'Y', 'false')]
        # mock_cursor.execute = MagicMock(return_value=feeds)
        # need to know what function to mock. No method called on cursor to retrieve results
        returned_feeds = self.model.read_datafeeds()
        print(returned_feeds)
        self.assertEqual(len(returned_feeds), 2)

    @patch('huxunify.api.data_connectors.snowflake_client.SnowflakeClient')
    def test_read_datafeeds_by_id(self):
        """
        Successfully retrieve single datafeed
        """
        feed = ('feed1', 'feed_type', 'source1', 'data_type', '.test', 'Y', 'false')

        # mock_cursor.fetchone = MagicMock(return_value=feeds)
        # need to know what function to mock. No method called on cursor to retrieve results
        returned_feed = self.model.read_datafeed_by_id(1)
        print(returned_feed)
        self.assertEqual(len(returned_feed), 1)