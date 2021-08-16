"""
Purpose of this file is for storing the cache management.
"""
import datetime
import logging
from typing import Union
import pymongo
from tenacity import retry, wait_fixed, retry_if_exception_type

import huxunifylib.database.constants as c
from huxunifylib.database.client import DatabaseClient


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def create_cache_entry(
    database: DatabaseClient,
    cache_key: str,
    cache_value: str,
    expire_after_seconds: int = 86400,
) -> None:
    """A function that creates a new cache entry

    Args:
        database (DatabaseClient): A database client.
        cache_key (str): name of the cache key.
        cache_value (str): name of the cache key value.
        expire_after_seconds (int): Time for the document to expire in seconds.

    Returns:

    """
    collection = database[c.DATA_MANAGEMENT_DATABASE][c.CACHE_COLLECTION]

    try:
        collection.ensure_index(
            c.CREATE_TIME, expireAfterSeconds=expire_after_seconds
        )
        collection.update_one(
            {c.CONSTANT_KEY: cache_key},
            {
                "$set": {
                    c.CONSTANT_VALUE: cache_value,
                    c.CREATE_TIME: datetime.datetime.utcnow(),
                }
            },
            upsert=True,
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_cache_entry(
    database: DatabaseClient, cache_key: str
) -> Union[dict, None]:
    """A function that creates a new cache entry

    Args:
        database (DatabaseClient): A database client.
        cache_key (str): name of the cache key.

    Returns:
        Union[dict, None]: MongoDB document for a cache entry.

    """
    collection = database[c.DATA_MANAGEMENT_DATABASE][c.CACHE_COLLECTION]

    try:
        result = collection.find_one({c.CONSTANT_KEY: cache_key})
        return result[c.CONSTANT_VALUE] if result else {}
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None
