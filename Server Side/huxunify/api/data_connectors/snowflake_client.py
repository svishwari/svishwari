"""
purpose of this file is for housing the snowflake database client
"""
import logging
from os import getenv
from typing import Optional
from snowflake import connector


# get snowflake connection params
USERNAME = getenv("CDM_SNOWFLAKE_USER")
PASSWORD = getenv("CDM_SNOWFLAKE_PASSWORD")
ACCOUNT = getenv("CDM_SNOWFLAKE_ACCOUNT")
WAREHOUSE = "COMPUTE_WH"


class SnowflakeClient:
    """Snowflake client for handling operations on the database."""

    def __init__(
        self,
        account: Optional[str] = ACCOUNT,
        warehouse: Optional[str] = WAREHOUSE,
        username: Optional[str] = USERNAME,
        password: Optional[str] = PASSWORD,
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
        """Union[str, None]: name of the azure snowflake account
        """
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
                warehouse=self._warehouse
            )
        except connector.errors.DatabaseError as db_error:
            logging.error(db_error)
        return ctx
