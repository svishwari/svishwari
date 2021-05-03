"""
This module enables functionality for data source management
"""
import logging
import datetime
import re
from typing import Any
from bson import ObjectId
import pymongo
from tenacity import retry, wait_fixed, retry_if_exception_type

import huxunifylib.database.db_exceptions as de
import huxunifylib.database.constants as c
from huxunifylib.database.client import DatabaseClient
from huxunifylib.database.utils import name_exists


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def create_data_source(database: DatabaseClient, name: str, category: str) -> dict:
    """A function that creates a new data source

    Args:
        database (DatabaseClient): A database client.
        name (str): name of a data source
        category (str): category of the data source

    Returns:
        dict: MongoDB document for a data source

    """
    collection = database[c.DATA_MANAGEMENT_DATABASE]["SOME COLLECTION NAME HERE"]
    doc = {
        c.FIELD_NAME: name,
        c.FIELD_CATEGORY: category,
        c.FIELD_FEED_COUNT: 1,  # TODO set to 1 for now until after 5.0 release
        c.FIELD_STATUS: "Pending"  # TODO may need to know what the valid statuses are here
    }

    return {}


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
    # TODO create a collection constant to get a db instance

    return []

# get one data source

# delete data source
