"""
This module enables functionality related to engagement management.
"""

import logging
import datetime
from bson import ObjectId
import pymongo
from tenacity import retry, wait_fixed, retry_if_exception_type

import huxunifylib.database.constants as db_constants
from huxunifylib.database.client import DatabaseClient


@retry(
    wait=wait_fixed(db_constants.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def create_engagement(database: DatabaseClient, engagement_name: str) -> str:
    """A function to create an engagement

    Args:
        database (DatabaseClient): A database client.
        engagement_name (str): Name of the engagement.

    Returns:
        str: id of the newly created engagement

    """

    collection = database[db_constants.DATA_MANAGEMENT_DATABASE][
        db_constants.ENGAGEMENTS_COLLECTION
    ]

    # TODO - implement after HUS-254 is done to grab user/okta_id
    user_id = ObjectId()

    doc = {
        db_constants.ENGAGEMENT_NAME: engagement_name,
        db_constants.ENGAGEMENT_AUDIENCES: [],
        db_constants.CREATE_TIME: datetime.datetime.utcnow(),
        db_constants.CREATED_BY: user_id,
        db_constants.ENGAGEMENT_DELIVERY_SCHEDULE: {},
        db_constants.UPDATE_TIME: datetime.datetime.utcnow(),
    }

    try:
        engagement_id = collection.insert_one(doc).inserted_id
        if engagement_id is not None:
            return engagement_id
        logging.error("Failed to create a new engagement!")
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


@retry(
    wait=wait_fixed(db_constants.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_all_engagements(database: DatabaseClient) -> list:
    """A function to get all engagements

    Args:
        database (DatabaseClient): A database client.

    Returns:
        list: List of all engagement documents.

    """

    collection = database[db_constants.DATA_MANAGEMENT_DATABASE][
        db_constants.ENGAGEMENTS_COLLECTION
    ]

    try:
        return list(collection.find())
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


@retry(
    wait=wait_fixed(db_constants.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_engagement(database: DatabaseClient, engagement_id: ObjectId) -> dict:
    """A function to get an engagement based on ID

    Args:
        database (DatabaseClient): A database client.
        engagement_id (str): Object Id of the engagement

    Returns:
        dict: Dict of an engagement.

    """

    collection = database[db_constants.DATA_MANAGEMENT_DATABASE][
        db_constants.ENGAGEMENTS_COLLECTION
    ]

    try:
        return collection.find_one({db_constants.ID: engagement_id})
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


@retry(
    wait=wait_fixed(db_constants.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def delete_engagement(
    database: DatabaseClient, engagement_id: ObjectId
) -> bool:
    """A function to delete an engagement based on ID

    Args:
        database (DatabaseClient): A database client.
        engagement_id (str): Object Id of the engagement

    Returns:
        dict: Dict of an engagement.

    """

    collection = database[db_constants.DATA_MANAGEMENT_DATABASE][
        db_constants.ENGAGEMENTS_COLLECTION
    ]

    try:
        return (
            collection.delete_one(
                {db_constants.ID: engagement_id}
            ).deleted_count
            > 0
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return False


@retry(
    wait=wait_fixed(db_constants.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def update_engagement(
    database: DatabaseClient,
    id: ObjectId,
    name: str = None,
    description: str = None,
    audiences: list = None,
    delivery_schedule: dict = None,
) -> dict:
    """A function to update fields in an engagement

    Args:
        database (DatabaseClient): A database client.
        id (ObjectId): ID of the engagement to be updated.
        name (str): Name of the engagement.
        description (str): Descriptions of the engagement.
        audiences (list): list of audience ObjectIds.
        delivery_schedule (dict): delivery schedule dict.

    Returns:
        dict: dict object of the engagement that has been updated
    """

    collection = database[db_constants.DATA_MANAGEMENT_DATABASE][
        db_constants.ENGAGEMENTS_COLLECTION
    ]

    
