"""
This module enables functionality related to engagement management.
"""

import logging
import datetime
from bson import ObjectId
import pymongo
from tenacity import retry, wait_fixed, retry_if_exception_type

import huxunifylib.database.db_exceptions as de
import huxunifylib.database.constants as db_c
from huxunifylib.database.client import DatabaseClient


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def set_engagement(
    database: DatabaseClient,
    name: str,
    description: str,
    audiences: list,
    delivery_schedule: dict,
) -> ObjectId:
    """A function to create an engagement

    Args:
        database (DatabaseClient): A database client.
        name (str): Name of the engagement.
        description (str): Description of the engagement.
        audiences (list): List of audience ObjectIds assigned to the engagement.
        delivery_schedule (dict): Delivery Schedule dict

    Returns:
        ObjectId: id of the newly created engagement

    """

    collection = database[db_c.DATA_MANAGEMENT_DATABASE][
        db_c.ENGAGEMENTS_COLLECTION
    ]

    # TODO - implement after HUS-254 is done to grab user/okta_id
    user_id = ObjectId()

    doc = {
        db_c.ENGAGEMENT_NAME: name,
        db_c.ENGAGEMENT_DESCRIPTION: description,
        db_c.ENGAGEMENT_AUDIENCES: audiences,
        db_c.ENGAGEMENT_DELIVERY_SCHEDULE: delivery_schedule,
        db_c.CREATE_TIME: datetime.datetime.utcnow(),
        db_c.CREATED_BY: user_id,
        db_c.UPDATE_TIME: datetime.datetime.utcnow(),
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
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_engagements(database: DatabaseClient) -> list:
    """A function to get all engagements

    Args:
        database (DatabaseClient): A database client.

    Returns:
        list: List of all engagement documents.

    """

    collection = database[db_c.DATA_MANAGEMENT_DATABASE][
        db_c.ENGAGEMENTS_COLLECTION
    ]

    try:
        return list(collection.find())
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_engagement(database: DatabaseClient, engagement_id: ObjectId) -> dict:
    """A function to get an engagement based on ID

    Args:
        database (DatabaseClient): A database client.
        engagement_id (ObjectId): ObjectId of the engagement

    Returns:
        dict: Dict of an engagement.

    """

    collection = database[db_c.DATA_MANAGEMENT_DATABASE][
        db_c.ENGAGEMENTS_COLLECTION
    ]

    try:
        return collection.find_one({db_c.ID: engagement_id})
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def delete_engagement(
    database: DatabaseClient, engagement_id: ObjectId
) -> bool:
    """A function to delete an engagement based on ID

    Args:
        database (DatabaseClient): A database client.
        engagement_id (ObjectId): Object Id of the engagement

    Returns:
        bool: Flag indicating successful operation.

    """

    collection = database[db_c.DATA_MANAGEMENT_DATABASE][
        db_c.ENGAGEMENTS_COLLECTION
    ]

    try:
        return (
            collection.delete_one({db_c.ID: engagement_id}).deleted_count > 0
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return False


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
# pylint: disable=too-many-arguments
def update_engagement(
    database: DatabaseClient,
    engagement_id: ObjectId,
    name: str = None,
    description: str = None,
    audiences: list = None,
    delivery_schedule: dict = None,
) -> dict:
    """A function to update fields in an engagement

    Args:
        database (DatabaseClient): A database client.
        engagement_id (ObjectId): ObjectID of the engagement to be updated.
        name (str): Name of the engagement.
        description (str): Descriptions of the engagement.
        audiences (list): list of audience ObjectIds.
        delivery_schedule (dict): delivery schedule dict.

    Returns:
        dict: dict object of the engagement that has been updated
    """

    collection = database[db_c.DATA_MANAGEMENT_DATABASE][
        db_c.ENGAGEMENTS_COLLECTION
    ]

    update_doc = {
        db_c.ENGAGEMENT_NAME: name,
        db_c.ENGAGEMENT_DESCRIPTION: description,
        db_c.ENGAGEMENT_AUDIENCES: audiences,
        db_c.ENGAGEMENT_DELIVERY_SCHEDULE: delivery_schedule,
        db_c.UPDATE_TIME: datetime.datetime.utcnow(),
    }

    # remove dict entries that are None
    update_doc = {k: v for k, v in update_doc.items() if v is not None}

    try:
        if update_doc:
            return collection.find_one_and_update(
                {db_c.ID: engagement_id},
                {"$set": update_doc},
                upsert=False,
                new=True,
            )
        else:
            raise de.NoUpdatesSpecified("engagement")

    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None
