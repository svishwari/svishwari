"""This module enables functionality related
to orchestration (audience/engagement) management.
"""

import logging
import datetime
from bson import ObjectId
import pymongo
from tenacity import retry, wait_fixed, retry_if_exception_type

import huxunifylib.database.db_exceptions as de
import huxunifylib.database.constants as c
from huxunifylib.database.client import DatabaseClient


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def create_audience(
    database: DatabaseClient,
    name: str,
    audience_filters: list,
    destination_ids: list = None,
    engagement_ids: list = None,  # pylint: disable=W0613
    user_id: ObjectId = None,
) -> dict:
    """A function to create an audience.

    Args:
        database (DatabaseClient): A database client.
        name (str): Name of the audience.
        audience_filters (list of list): Multiple sections of audience filters.
        These are aggregated using "OR".
        destination_ids (list): List of destination
            / delivery platform ids attached to the audience
        engagement_ids (list): List of engagement ids attached to the audience
        user_id (ObjectId): Object id of user creating / updating the audience

    Returns:
        dict: MongoDB audience doc.
    """

    am_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = am_db[c.AUDIENCES_COLLECTION]

    # Make sure the name will be unique
    try:
        doc = collection.find_one({c.AUDIENCE_NAME: name})
        if doc:
            raise de.DuplicateName(name)
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    # Get current time
    curr_time = datetime.datetime.utcnow()

    audience_doc = {
        c.AUDIENCE_NAME: name,
        c.AUDIENCE_FILTERS: audience_filters,
        c.DESTINATIONS: destination_ids,
        c.CREATE_TIME: curr_time,
        c.UPDATE_TIME: curr_time,
        c.CREATED_BY: user_id,
        c.UPDATED_BY: user_id,
    }

    # TODO: Set Engagement IDs once the engagement table is ready
    try:
        audience_id = collection.insert_one(audience_doc).inserted_id
        if audience_id is not None:
            return collection.find_one({c.ID: audience_id})
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_audience(database: DatabaseClient, audience_id: ObjectId) -> dict:
    """A function to get an audience.

    Args:
        database (DatabaseClient): A database client.
        audience_id (ObjectId): The Mongo DB ID of the audience.

    Returns:
        dict:  An audience document.

    """
    doc = None
    am_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = am_db[c.AUDIENCES_COLLECTION]

    # Read the audience document which contains filtering rules
    try:
        doc = collection.find_one({c.ID: audience_id})
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    if doc is None:
        raise de.InvalidID(audience_id)

    return doc


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_all_audiences(
    database: DatabaseClient,
) -> list:
    """A function to get all existing audiences.

    Args:
        database (DatabaseClient): A database client.

    Returns:
        List: A list of all audiences.

    """

    am_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = am_db[c.AUDIENCES_COLLECTION]

    # Get audience configurations and add to list
    try:
        return list(collection.find())
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def update_audience(
    database: DatabaseClient,
    audience_id: ObjectId,
    name: str,
    audience_filters: list = None,
    destination_ids: list = None,
    engagement_ids: list = None,  # pylint: disable=W0613
    user_id: ObjectId = None,
) -> dict:
    """A function to update an audience.

    Args:
        database (DatabaseClient): A database client.
        audience_id (ObjectId): MongoDB ID of the audience.
        name (str): New audience name.
        audience_filters (list of list): Multiple sections of audience filters.
            These are aggregated using "OR".
        destination_ids (list): List of destination / delivery platform
            ids attached to the audience
        engagement_ids (list): List of engagement ids attached to the audience
        user_id (ObjectId): Object id of user creating / updating the audience

    Returns:
        dict: Updated audience configuration dict.

    """

    am_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = am_db[c.AUDIENCES_COLLECTION]

    try:
        audience_doc = collection.find_one({c.ID: audience_id})
        if not audience_doc:
            raise de.InvalidID()
        if name is None:
            raise de.InvalidName()

        duplicate_name_doc = collection.find_one({c.AUDIENCE_NAME: name})
        if (
            duplicate_name_doc is not None
            and duplicate_name_doc[c.ID] != audience_id
        ):
            raise de.DuplicateName(name)
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    # Get current time
    curr_time = datetime.datetime.utcnow()

    updated_audience_doc = {
        c.AUDIENCE_NAME: name,
        c.AUDIENCE_FILTERS: audience_filters,
        c.DESTINATIONS: destination_ids,
        c.UPDATE_TIME: curr_time,
        c.UPDATED_BY: user_id,
    }

    # TODO: Delete and Update Engagement IDs once the engagement table is ready
    try:
        audience_doc = collection.find_one_and_update(
            {c.ID: audience_id},
            {"$set": updated_audience_doc},
            upsert=False,
            return_document=pymongo.ReturnDocument.AFTER,
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return audience_doc
