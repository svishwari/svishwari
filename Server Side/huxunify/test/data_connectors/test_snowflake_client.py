from unittest import TestCase
from unittest.mock import patch
from snowflake import connector
from huxunify.api.data_connectors.snowflake_client import SnowflakeClient


class TestSnowflakeClient(TestCase):

    @patch('snowflake.connector.connect')
    def test_connection_good(self, mock_connect):
        client = SnowflakeClient('TEST_ACCOUNT', 'TEST_WAREHOUSE', 'TEST_USERNAME', 'TEST_PASSWORD')
        connection = client.connect()

        mock_connect.assert_called_once_with(account='TEST_ACCOUNT',
                                             warehouse='TEST_WAREHOUSE',
                                             user='TEST_USERNAME',
                                             password='TEST_PASSWORD')

    @patch('snowflake.connector.connect', side_effect=connector.errors.DatabaseError("DB ERROR"))
    def test_connection_bad1(self, mock_connect):
        client = SnowflakeClient('TEST_ACCOUNT', 'TEST_WAREHOUSE', 'TEST_USERNAME', 'TEST_PASSWORD')
        self.assertRaises(connector.errors.DatabaseError, client.connect())
