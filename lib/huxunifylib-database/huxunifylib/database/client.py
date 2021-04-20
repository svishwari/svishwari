"""This module enables functionality related to database clients."""

from typing import Optional, Union
import pymongo


class DatabaseClient:
    """Database client for handling operations on the database."""

    def __init__(
        self,
        host: Union[str, list],
        port: Optional[int] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ) -> None:
        """Initialize a DatabaseClient object.

        Args:
            host (Union[str, list]): Host name or list of host names.
            port (Optional(int)): Port number (optional).
            username ((Optional(str)): Username for database
                authentication (optional).
            password (Optional(str)): Password for database
                authentication (optional).

        """
        self._host = host
        self._port = port
        self._username = username
        self._password = password

    @property
    def host(self):
        """Union[str, list]: Host name or list of host names used to
        initialize the client.
        """
        return self._host

    @property
    def port(self):
        """Union[int, None]: Port number used to initialize the client."""
        return self._port

    @property
    def username(self):
        """Union[str, None]: Username used when authenticating the client."""
        return self._username

    def connect(self) -> pymongo.MongoClient:
        """Connect to the database.

        Returns:
            MongoClient object.
        """

        # initialize a MongoClient object, passing in server and
        # authentication information and using the default
        # write concern to ensure acknowledgement of the write
        # to at least one database member (w=1)
        client = pymongo.MongoClient(
            self._host,
            self._port,
            w=1,
            username=self._username,
            password=self._password,
        )

        return client
