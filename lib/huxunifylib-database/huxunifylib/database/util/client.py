"""File for DB Clients."""

from pymongo import MongoClient

from huxunifylib.database.client import DatabaseClient
from huxunifylib.database.util.resource_factory import ResourceFactory


def get_mongodb_client(
    connection_string: str = None,
    host: str = None,
    port: int = None,
    username: str = None,
    password: str = None,
    ssl_cert_path: str = None,
    ssl_flag: bool = None,
    tls_cert_key_file: str = None,
    tls_ca_cert_key_file:str=None,
) -> MongoClient:
    """Get connected Pymongo client.
    Args:
        connection_string (str, optional): MongoDB connection string.
            Defaults to None.
        host (str, optional): MongoDB host. Defaults to None.
        port (int, optional): MongoDB port. Defaults to None.
        username (str, optional): MongoDB username. Defaults to None.
        password (str, optional): MongoDB password. Defaults to None.
        ssl_cert_path (str, optional): MongoDB ssl cert path. Defaults to None.
        ssl_flag (bool, optional): MongoDB ssl flag. Defaults to None.
        tls_cert_key_file (str, optional): TLS Client certificates.
            Defaults to None.
        tls_ca_cert_key_file(str,optional): TLS CA Client Certificates defaults to None

    Returns:
        pymongo.MongoClient: Connected Pymongo client.
    """
    mongo_db_client = DatabaseClient(
        connection_string=connection_string,
        host=host,
        port=port,
        username=username,
        password=password,
        ssl_cert_path=ssl_cert_path,
        ssl_flag=ssl_flag,
        tls_cert_key_file=tls_cert_key_file,
        tls_ca_cert_key_file=tls_ca_cert_key_file
    )
    return mongo_db_client.connect()


db_client_factory = ResourceFactory(get_mongodb_client)
