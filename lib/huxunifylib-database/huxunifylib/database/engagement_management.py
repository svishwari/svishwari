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
from huxunifylib.database.utils import name_exists


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def set_engagement(
    database: DatabaseClient,
    name: str,
    description: str,
    user_id: ObjectId,
    delivery_schedule: dict = None,
) -> ObjectId:
    """A function to create an engagement

    Args:
        database (DatabaseClient): A database client.
        name (str): Name of the engagement.
        description (str): Description of the engagement.
        user_id (ObjectId): ID of the user creating the document.
        delivery_schedule (dict): Delivery Schedule dict

    Returns:
        ObjectId: id of the newly created engagement

    """

    collection = database[db_c.DATA_MANAGEMENT_DATABASE][
        db_c.ENGAGEMENTS_COLLECTION
    ]

    if name_exists(
        database,
        db_c.DATA_MANAGEMENT_DATABASE,
        db_c.ENGAGEMENTS_COLLECTION,
        db_c.ENGAGEMENT_NAME,
        name,
    ):
        raise de.DuplicateName(name)

    doc = {
        db_c.ENGAGEMENT_NAME: name,
        db_c.ENGAGEMENT_DESCRIPTION: description,
        db_c.CREATE_TIME: datetime.datetime.utcnow(),
        db_c.CREATED_BY: user_id,
        db_c.UPDATE_TIME: datetime.datetime.utcnow(),
        db_c.ENABLED: True,
    }
    if delivery_schedule:
        doc[db_c.ENGAGEMENT_DELIVERY_SCHEDULE] = delivery_schedule

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
        return list(collection.find({db_c.ENABLED: True}))
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
        return collection.find_one(
            {db_c.ID: engagement_id, db_c.ENABLED: True}
        )
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
        doc = collection.find_one_and_update(
            {db_c.ID: engagement_id},
            {"$set": {db_c.ENABLED: False}},
            upsert=False,
            new=True,
        )
        return not doc[db_c.ENABLED]
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return False


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
# pylint: disable=too-many-arguments
# pylint: disable=no-else-return
def update_engagement(
    database: DatabaseClient,
    engagement_id: ObjectId,
    user_id: ObjectId,
    name: str = None,
    description: str = None,
    delivery_schedule: dict = None,
) -> dict:
    """A function to update fields in an engagement

    Args:
        database (DatabaseClient): A database client.
        engagement_id (ObjectId): ObjectID of the engagement to be updated.
        name (str): Name of the engagement.
        description (str): Descriptions of the engagement.
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
        db_c.UPDATED_BY: user_id,
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


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def create_engagement_audience(
    database: DatabaseClient,
    audience_id: ObjectId,
    engagement_id: ObjectId,
    destination_ids: list,
) -> dict:
    """A function to create an engagement audience.

    Args:
        database (DatabaseClient): A database client.
        audience_id (str): audience id.
        engagement_id (str): engagement id.
        destination_ids (list): List of destination ids attached
            to the engagement

    Returns:
        dict: MongoDB engagement audience doc.
    """

    # check for a valid object id
    if not isinstance(audience_id, ObjectId):
        raise TypeError(f"Invalid Audience ID Provided {audience_id}.")

    # check for a valid object id
    if not isinstance(engagement_id, ObjectId):
        raise TypeError(f"Invalid Engagement ID Provided {engagement_id}.")

    # validate the destination IDs
    if not all(isinstance(x, ObjectId) for x in destination_ids):
        raise TypeError("Invalid Destination IDs Provided.")

    am_db = database[db_c.DATA_MANAGEMENT_DATABASE]

    # check if the engagement id exists
    engagements = am_db[db_c.ENGAGEMENTS_COLLECTION]
    if engagements.count_documents({db_c.ID: engagement_id}, limit=1) == 0:
        raise Exception(f"Engagement does not exist {engagement_id}.")

    # check if the audience id exists
    audiences = am_db[db_c.AUDIENCES_COLLECTION]
    if audiences.count_documents({db_c.ID: audience_id}, limit=1) == 0:
        raise Exception(f"Audience does not exist {audience_id}.")

    # check if the all the destination ids exists
    destinations = am_db[db_c.DELIVERY_PLATFORM_COLLECTION]
    for dest_id in destination_ids:
        if destinations.count_documents({db_c.ID: dest_id}, limit=1) == 0:
            raise Exception(f"Destination does not exist {dest_id}.")

    # get the engagement collection
    collection = am_db[db_c.ENGAGEMENT_AUDIENCES_COLLECTION]

    # check if existing engagement audience.
    try:
        engagement_audience = collection.find_one(
            {db_c.ENGAGEMENT_ID: engagement_id, db_c.AUDIENCE_ID: audience_id}
        )
        if engagement_audience:
            raise Exception(
                f"Engagement Audience Exists {engagement_audience[db_c.ID]}."
            )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    engagement_audience = {
        db_c.ENGAGEMENT_ID: engagement_id,
        db_c.AUDIENCE_ID: audience_id,
        db_c.DESTINATIONS: destination_ids,
        db_c.ENABLED: True,
    }

    try:
        engagement_audience_id = collection.insert_one(
            engagement_audience
        ).inserted_id
        if engagement_audience_id is not None:
            return collection.find_one({db_c.ID: engagement_audience_id})
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_engagement_audiences(
    database: DatabaseClient, engagement_ids: list, enabled: bool = True
) -> list:
    """A function to get engagement audiences based on ID

    Args:
        database (DatabaseClient): A database client.
        engagement_ids (list): list of engagement audiences.

    Returns:
        list: list of engagements.

    """

    if not engagement_ids:
        return None

    if not all(isinstance(x, ObjectId) for x in engagement_ids):
        raise TypeError("Invalid Engagement IDs Provided.")

    collection = database[db_c.DATA_MANAGEMENT_DATABASE][
        db_c.ENGAGEMENT_AUDIENCES_COLLECTION
    ]

    try:
        return list(
            collection.find(
                {db_c.ID: {"$in": engagement_ids}, db_c.ENABLED: enabled}
            )
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def delete_engagement_audiences(
    database: DatabaseClient, engagement_ids: list
) -> list:
    """A function to delete engagement audiences based on ID.

    Args:
        database (DatabaseClient): A database client.
        engagement_ids (list): list of engagement audiences.

    Returns:
        list: List of deleted engagement audiences.

    """

    if not engagement_ids:
        return None

    if not all(not isinstance(x, ObjectId) for x in engagement_ids):
        raise TypeError("Invalid Engagement IDs Provided.")

    collection = database[db_c.DATA_MANAGEMENT_DATABASE][
        db_c.ENGAGEMENT_AUDIENCES_COLLECTION
    ]

    update_doc = {db_c.ENABLED: False}

    try:
        # soft-delete
        delete_ids = collection.update_many(
            {db_c.ID: {"$in": engagement_ids}}, {"$set": update_doc}
        )
        return list(delete_ids)
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None
