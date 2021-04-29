"""
purpose of this file is for housing the snowflake database client
"""
import logging
from typing import Optional
from snowflake import connector
from huxunify.api import config


class SnowflakeClient:
    """Snowflake client for handling operations on the database."""

    def __init__(
        self,
        account: Optional[str] = config.SNOWFLAKE_ACCOUNT,
        warehouse: Optional[str] = config.SNOWFLAKE_WAREHOUSE,
        username: Optional[str] = config.SNOWFLAKE_USERNAME,
        password: Optional[str] = config.SNOWFLAKE_PASSWORD,
    ) -> None:
        """Initialize a Snowflake database object.
        Args:
            account ((Optional(str)): Name of snowflake account.
            warehouse ((Optional(str)): Name of snowflake warehouse.
            username ((Optional(str)): Username for database
                authentication (optional).
            password (Optional(str)): Password for database
                authentication (optional).
        """
        self._account = account
        self._warehouse = warehouse
        self._username = username
        self._password = password

    @property
    def account(self):
        """Union[str, None]: name of the azure snowflake account"""
        return self._account

    @property
    def warehouse(self):
        """Union[str, None]: warehouse used for housing snowflake data"""
        return self._warehouse

    @property
    def username(self):
        """Union[str, None]: Username used when authenticating the client."""
        return self._username

    def connect(self) -> connector.connection:
        """Connect to the database.
        Returns:
            Snowflake connection object.
        """
        ctx = None
        try:
            # initialize the snowflake connection object
            ctx = connector.connect(
                user=self._username,
                password=self._password,
                account=self._account,
                warehouse=self._warehouse,
            )
        except connector.errors.DatabaseError as db_error:
            logging.error(db_error)
            raise Exception(db_error) from db_error
        return ctx
