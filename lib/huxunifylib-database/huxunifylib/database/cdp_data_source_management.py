"""This module enables functionality for data source management."""
import logging
from typing import Union, Optional
from bson import ObjectId
import pymongo
from tenacity import retry, wait_fixed, retry_if_exception_type

import huxunifylib.database.constants as db_c
from huxunifylib.database.client import DatabaseClient
import huxunifylib.database.db_exceptions as de
from huxunifylib.database.engagement_management import validate_object_id_list


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def create_data_source(
    database: DatabaseClient,
    name: str,
    category: str,
    added: bool = False,
    enabled: bool = False,
    source_type: str = None,
    status: str = db_c.CDP_DATA_SOURCE_STATUS_ACTIVE,
) -> Union[dict, None]:
    """A function that creates a new data source.

    Args:
        database (DatabaseClient): A database client.
        name (str): name of a data source.
        category (str): category of the data source.
        added (bool): data source is added.
        enabled (bool): data source is enabled.
        source_type (str): type of the data source.
        status (str): status of the data source.

    Returns:
        Union[dict, None]: MongoDB document for a data source or None.
    """

    collection = database[db_c.DATA_MANAGEMENT_DATABASE][
        db_c.CDP_DATA_SOURCES_COLLECTION
    ]

    # TODO - feed count to be updated per CDM in future tickets.
    doc = {
        db_c.CDP_DATA_SOURCE_FIELD_NAME: name,
        db_c.CDP_DATA_SOURCE_FIELD_CATEGORY: category,
        db_c.CDP_DATA_SOURCE_FIELD_FEED_COUNT: 1,
        db_c.CDP_DATA_SOURCE_FIELD_STATUS: status,
        db_c.ADDED: added,
        db_c.ENABLED: enabled,
    }

    if source_type:
        doc[db_c.DATA_SOURCE_TYPE] = source_type

    try:
        data_source_id = collection.insert_one(doc).inserted_id
        if data_source_id is not None:
            return collection.find_one({db_c.ID: data_source_id})
        logging.error("Failed to create a new data source!")
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def bulk_write_data_sources(
    database: DatabaseClient, data_sources: list
) -> Union[list, None]:
    """A function that creates new data sources

    Args:
        database (DatabaseClient): A database client.
        data_sources (list): List of data sources to create.

    Returns:
        Union[list, None]: List of MongoDB documents for data sources or None.
    """
    collection = database[db_c.DATA_MANAGEMENT_DATABASE][
        db_c.CDP_DATA_SOURCES_COLLECTION
    ]

    _ = [
        data_source.update({db_c.ADDED: True}) for data_source in data_sources
    ]

    try:
        data_source_ids = collection.insert_many(data_sources).inserted_ids
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return list(collection.find({db_c.ID: {"$in": data_source_ids}}))


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_all_data_sources(database: DatabaseClient) -> Union[list, None]:
    """A function that returns all data sources.

    Args:
        database (DatabaseClient): A database client.

    Returns:
        Union[list, None]: List of all data sources or None.
    """

    collection = database[db_c.DATA_MANAGEMENT_DATABASE][
        db_c.CDP_DATA_SOURCES_COLLECTION
    ]

    try:
        return list(collection.find({}))
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_data_source(
    database: DatabaseClient,
    data_source_id: Optional[ObjectId] = None,
    data_source_type: Optional[str] = None,
) -> Union[dict, None]:
    """A function to return a single data source based on a provided value.

    Args:
        database (DatabaseClient): A database client.
        data_source_id (Optional[ObjectId]): data source id.
        data_source_type (Optional[str]): data source type.

    Returns:
        Union[dict, None]: MongoDB document for a data source or None.

    Raises:
        InsufficientDataException: If the passed in information in
            data_source_id and data_source_type are insufficient to perform
            the mongo operation.
    """

    collection = database[db_c.DATA_MANAGEMENT_DATABASE][
        db_c.CDP_DATA_SOURCES_COLLECTION
    ]
    query = {}

    if data_source_id:
        query.update({db_c.ID: data_source_id})
    elif data_source_type:
        query.update({db_c.TYPE: data_source_type})
    else:
        raise de.InsufficientDataException("data source")

    try:
        return collection.find_one(query)
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def delete_data_source(
    database: DatabaseClient, data_source_id: ObjectId
) -> bool:
    """A function to delete a data source.

    Args:
        database (DatabaseClient): A database client.
        data_source_id (ObjectId): data source id.

    Returns:
        bool: a flag indicating successful deletion.
    """

    collection = database[db_c.DATA_MANAGEMENT_DATABASE][
        db_c.CDP_DATA_SOURCES_COLLECTION
    ]

    try:
        return (
            collection.delete_one({db_c.ID: data_source_id}).deleted_count > 0
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return False


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def bulk_delete_data_sources(
    database: DatabaseClient, data_source_types: list
) -> bool:
    """A function that deletes selected data sources

    Args:
        database (DatabaseClient): A database client.
        data_source_types (list): List of data source types to delete.
    Returns:
        bool: a flag indicating successful deletion.
    """
    collection = database[db_c.DATA_MANAGEMENT_DATABASE][
        db_c.CDP_DATA_SOURCES_COLLECTION
    ]

    try:
        return (
            collection.delete_many(
                {db_c.TYPE: {"$in": data_source_types}}
            ).deleted_count
            > 0
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return False


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def update_data_sources(
    database: DatabaseClient, data_source_ids: list, update_dict: dict
) -> bool:
    """A function to update data source(s) based on ObjectId(s).

    Args:
        database (DatabaseClient): A database client.
        data_source_ids (list): list of ObjectIds.
        update_dict (dict): update field dict.

    Returns:
        bool: Success flag.
    """

    if not update_dict:
        return False

    # validate list of object ids.
    validate_object_id_list(data_source_ids)

    # remove duplicates if any.
    data_source_ids = list(set(data_source_ids))

    collection = database[db_c.DATA_MANAGEMENT_DATABASE][
        db_c.CDP_DATA_SOURCES_COLLECTION
    ]

    try:
        result = collection.update_many(
            {db_c.ID: {"$in": data_source_ids}}, {"$set": update_dict}
        )
        return len(data_source_ids) == result.matched_count
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    except TypeError as exc:
        logging.error(exc)

    return False
