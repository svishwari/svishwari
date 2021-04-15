"""
purpose of this file is testing the snowflake client
"""
from unittest import TestCase
from unittest.mock import patch, MagicMock
from snowflake import connector
from huxunify.api.data_connectors.snowflake_client import SnowflakeClient

ACCOUNT = "TEST_ACCOUNT"
WAREHOUSE = "TEST_WAREHOUSE"
USER = "TEST_USERNAME"
PASSWORD = "TEST_PASSWORD"


class TestSnowflakeClient(TestCase):
    """
    Test snowflake client good and bad connections
    """

    def setUp(self) -> None:
        """Setup initial test client
        Args:

        Returns:
            None
        """
        self.client = SnowflakeClient(
            account=ACCOUNT, warehouse=WAREHOUSE, username=USER, password=PASSWORD
        )

    @patch("snowflake.connector.connect")
    def test_connection_good(self, mock_connect: MagicMock) -> None:
        """Tests a good connection to snowflake database
        Args:
            mock_connect: MagicMock of snowflake connection
        Returns:
            None
        """
        self.client.connect()
        mock_connect.assert_called_once_with(
            account=ACCOUNT, warehouse=WAREHOUSE, user=USER, password=PASSWORD
        )

    @patch("snowflake.connector.connect")
    def test_connection_bad(self, mock_connect: MagicMock) -> None:
        """Tests a bad connection to snowflake database
        Args:
            mock_connect: MagicMock of snowflake connection
        Returns:
            None
        """
        # apply side effect
        connector.connect.side_effect = connector.errors.DatabaseError("DB ERROR")

        # test that base exception is raised
        with self.assertRaises(BaseException):
            self.client.connect()
        mock_connect.assert_called_once_with(
            account=ACCOUNT, warehouse=WAREHOUSE, user=USER, password=PASSWORD
        )
