"""This module enables functionality related to database clients."""

from typing import Optional, Union
from pathlib import Path
import pymongo


# pylint: disable=too-many-instance-attributes
class DatabaseClient:
    """Database client for handling operations on the database."""

    def __init__(
            self,
            connection_string: Optional[str] = None,
            host: Union[str, list, None] = None,
            port: Optional[int] = None,
            username: Optional[str] = None,
            password: Optional[str] = None,
            ssl_cert_path: Optional[str] = None,
            ssl_flag: Optional[bool] = None,
            tls_cert_key_file: Optional[str] = None,
            tls_ca_cert_key_file: Optional[str] = None
    ) -> None:
        """Initialize a DatabaseClient object.

        Args:
            connection_string (Optional(str)): Connection string of database.
            host (Union[str, list]): Host name or list of host names.
            port (Optional(int)): Port number (optional).
            username ((Optional(str)): Username for database
                authentication (optional).
            password (Optional(str)): Password for database
                authentication (optional).
            ssl_cert_path (Optional(str)): SSL Certificate path for
                connecting to MongoDB (optional).
            ssl_flag (Optional(bool)): SSL flag for database
                connecting to MongoDB (optional).
            tls_cert_key_file (Optional(str)): TLS Client certificates.
            tls_ca_cert_key_file(Optional(str)):TLS CA Client Certificates

        """

        self._connection_string = connection_string
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._use_ssl = True
        self._ssl_cert_path = ssl_cert_path
        self._use_ssl_flag = ssl_flag
        self._tls_cert_key_file = tls_cert_key_file
        self._tls_ca_cert_key_file = tls_ca_cert_key_file

    @property
    def connection_string(self) -> Union[str, None]:
        """Get the connection string.

        Returns:
            Union[str, None]: Connection string to connect to mongo instance.
        """

        return self._connection_string

    @property
    def host(self) -> Union[str, list, None]:
        """Get the host name or list of host names.

        Returns:
            Union[str, list]: Host name or list of host names used to
                initialize the client.
        """

        return self._host

    @property
    def port(self) -> Union[int, None]:
        """Get the port number.

        Returns:
            Union[int, None]: Port number used to initialize the client.
        """

        return self._port

    @property
    def username(self) -> Union[str, None]:
        """Get the username.

        Returns:
            Union[str, None]: Username used when authenticating the client.
        """

        return self._username

    @property
    def ssl_cert_path(self) -> Union[str, None]:
        """Get the SSL certeficate used to authenticate the client.

        Returns:
            Union[str, None]: SSL Certificate used when authenticating the
                client.
        """

        return self._ssl_cert_path

    @property
    def tls_cert_key_file(self) -> Union[str, None]:
        """Get the client certificates for self-signed certificates.

        Returns:
            Union[str, None]: TLS Certificate, Key used by the client.
        """

        return self._tls_cert_key_file

    @property
    def tls_ca_cert_key_file(self) -> Union[str, None]:
        """Get the TLS CA client certificates for self-signed certificates.

        Returns:
            Union[str, None]: TLS CA Certificate, Key used by the client.
        """

        return self._tls_ca_cert_key_file

    @property
    def ssl_flag(self):
        """Union[bool, None]: SSL flag used when authenticating the client."""
        return self._use_ssl_flag

    def connect(self) -> pymongo.MongoClient:
        """Connect to the database.

        Returns:
            MongoClient object.
        """

        # initialize a MongoClient object, passing in server and
        # authentication information and using the default
        # write concern to ensure acknowledgement of the write
        # to at least one database member (w=1)
        if self._connection_string:
            return pymongo.MongoClient(self._connection_string)

        mongo_args = {
            "host": self._host,
            "port": self._port,
            "w": 1,
            "username": self._username,
            "password": self._password,
        }
        if self._use_ssl:
            mongo_args["ssl"] = True
            mongo_args["ssl_ca_certs"] = self._ssl_cert_path
            mongo_args["tlsCertificateKeyFile"] = self._tls_cert_key_file
            mongo_args["tlsCAFile"] = self._tls_ca_cert_key_file
        elif self._use_ssl_flag:
            mongo_args["ssl"] = True
            mongo_args["retrywrites"] = False

        return pymongo.MongoClient(**mongo_args)
