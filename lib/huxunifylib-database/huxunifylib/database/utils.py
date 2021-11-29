"""This module is for the external database utilities."""

import logging
import pymongo
import pandas as pd
from tenacity import retry, wait_fixed, retry_if_exception_type

import huxunifylib.database.constants as db_c
from huxunifylib.database.client import DatabaseClient


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def name_exists(
    database: DatabaseClient,
    database_name: str,
    collection_name: str,
    name_field: str,
    name: str,
) -> bool:
    """A function to ensure uniqueness of an entity name.

    Args:
        database (DatabaseClient): A database client.
        database_name (str): Name of database.
        collection_name (str): Name of collection.
        name_field (str): Field used to store name of the entity.
        name (str): Name of the entity.

    Returns:
        bool: A flag indicating existence of an entity name in database.
    """

    doc = None
    dm_db = database[database_name]
    collection = dm_db[collection_name]

    try:
        doc = collection.find_one({name_field: name})
        if doc:
            return True
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return False


def detect_non_breakdown_fields(
    new_data: pd.DataFrame,
    fields: list,
) -> list:
    """A function to detect non breakdown fields based on a batch of
       data. These are fields with values that contain "$" or ".". As MongoDB
       does not allow keys that contain these two characters, we cannot store
       breakdowns for them.

    Args:
        new_data (pd.DataFrame): New data in Pandas DataFrame format.
        fields (list): List of fields to check.

    Returns:
        list: List of detected no breakdown fields.
    """

    new_non_breakdown_fields = []

    fields = list(set(fields).intersection(set(new_data.columns)))

    for field in fields:
        if new_data[field].dropna().str.contains("\\$|\\.").any():
            new_non_breakdown_fields.append(field)

    return new_non_breakdown_fields


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_collection_count(
    database: DatabaseClient, database_name: str, collection_name: str
) -> int:
    """Returns collection count.

    Args:
        database (DatabaseClient): database client.
        database_name (str): database name.
        collection_name (str): collection name.

    Returns:
        int: collection count.
    """

    collection = database[database_name][collection_name]

    try:
        return collection.count_documents(
            {
                db_c.DELETED: False,
            }
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return 0
