"""
purpose of this file is testing the snowflake client
"""
from unittest import TestCase
from unittest.mock import patch
from snowflake import connector
from huxunify.api.data_connectors.snowflake_client import SnowflakeClient

account = 'TEST_ACCOUNT'
warehouse = 'TEST_WAREHOUSE'
user = 'TEST_USERNAME'
password = 'TEST_PASSWORD'


class TestSnowflakeClient(TestCase):
    """
    Test snowflake client good and bad connections
    """

    def setUp(self) -> None:
        """
        Setup initial test client
        """
        self.client = SnowflakeClient(account=account, warehouse=warehouse, username=user, password=password)

    @patch('snowflake.connector.connect')
    def test_connection_good(self, mock_connect):
        """
        Tests a good connection to snowflake database
        """
        connection = self.client.connect()
        mock_connect.assert_called_once_with(account=account,
                                             warehouse=warehouse,
                                             user=user,
                                             password=password)

    @patch('snowflake.connector.connect', side_effect=connector.errors.DatabaseError("DB ERROR"))
    def test_connection_bad(self, mock_connect):
        """
        Tests a bad connection to snowflake database
        """
        self.assertRaises(connector.errors.DatabaseError, self.client.connect())
