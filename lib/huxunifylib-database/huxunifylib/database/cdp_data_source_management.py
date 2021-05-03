"""
This module enables functionality for data source management
"""
import logging
from bson import ObjectId
import pymongo
from tenacity import retry, wait_fixed, retry_if_exception_type

import huxunifylib.database.constants as c
from huxunifylib.database.client import DatabaseClient


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def create_data_source(
    database: DatabaseClient, name: str, category: str
) -> dict:
    """A function that creates a new data source

    Args:
        database (DatabaseClient): A database client.
        name (str): name of a data source
        category (str): category of the data source

    Returns:
        dict: MongoDB document for a data source

    """
    collection = database[c.DATA_MANAGEMENT_DATABASE][
        c.CDP_DATA_SOURCES_COLLECTION
    ]

    # TODO may need to know what the valid statuses are here
    # TODO update of statuses will be needed here after 5.0 release
    # TODO set to 1 for now until after 5.0 release
    doc = {
        c.CDP_DATA_SOURCE_FIELD_NAME: name,
        c.CDP_DATA_SOURCE_FIELD_CATEGORY: category,
        c.CDP_DATA_SOURCE_FIELD_FEED_COUNT: 1,
        c.CDP_DATA_SOURCE_FIELD_STATUS: "Pending",
    }

    try:
        data_source_id = collection.insert_one(doc).inserted_id
        if data_source_id is not None:
            return collection.find_one({c.ID: data_source_id})
        logging.error("Failed to create a new user!")
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_all_data_sources(database: DatabaseClient) -> list:
    """A function that returns all data sources

    Args:
        database (DatabaseClient): A database client.

    Returns:
        list: List of all data sources

    """
    collection = database[c.DATA_MANAGEMENT_DATABASE][
        c.CDP_DATA_SOURCES_COLLECTION
    ]

    try:
        return list(collection.find({}))
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_data_source(
    database: DatabaseClient, data_source_id: ObjectId
) -> dict:
    """A function to return a single data source based on a provided id

    Args:
        database (DatabaseClient): A database client.
        data_source_id (ObjectId): data source id.

    Returns:
        dict: MongoDB document for a data source

    """
    collection = database[c.DATA_MANAGEMENT_DATABASE][
        c.CDP_DATA_SOURCES_COLLECTION
    ]

    try:
        return collection.find_one({c.ID: data_source_id})
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def delete_data_source(
    database: DatabaseClient, data_source_id: ObjectId
) -> bool:
    """A function to delete a data source

    Args:
        database (DatabaseClient): A database client.
        data_source_id (ObjectId): data source id.

    Returns:
        bool: a flag indicating successful deletion

    """
    collection = database[c.DATA_MANAGEMENT_DATABASE][
        c.CDP_DATA_SOURCES_COLLECTION
    ]

    try:
        return collection.delete_one({c.ID: data_source_id}).deleted_count > 0
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return False
