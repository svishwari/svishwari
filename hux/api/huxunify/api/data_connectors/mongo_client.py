"""
purpose of this script is to house the mongo get db client.
"""
from pymongo import MongoClient
from huxunify.api import config


def get_db_client() -> MongoClient:
    """Get Mongo Client directly
    Args:
    Returns:
        MongoClient: A connected mongo client, pulling settings from the environment
    """
    # Set up the database client
    return MongoClient(
        config.MONGO_DB_HOST,
        config.MONGO_DB_PORT,
        w=1,
        username=config.MONGO_DB_USERNAME,
        password=config.MONGO_DB_PASSWORD,
        ssl=config.MONGO_DB_USE_SSL,
        ssl_ca_certs=config.MONGO_SSL_CERT,
    )
