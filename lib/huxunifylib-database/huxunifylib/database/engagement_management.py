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
    audiences: list,
    user_id: ObjectId,
    delivery_schedule: dict = None,
    deleted: bool = False,
) -> ObjectId:
    """A function to create an engagement

    Args:
        database (DatabaseClient): A database client.
        name (str): Name of the engagement.
        description (str): Description of the engagement.
        audiences (list): List of audiences assigned to the engagement.
        user_id (ObjectId): ObjectID of user.
        delivery_schedule (dict): Delivery Schedule dict
        deleted (bool): if the engagement is deleted (soft-delete).
    Returns:
        ObjectId: id of the newly created engagement

    """

    # validate audiences
    validate_audiences(audiences, check_empty=False)

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
        db_c.DELETED: deleted,
        db_c.AUDIENCES: [],
    }

    # attach the audiences to the engagement
    for audience in audiences:
        doc[db_c.AUDIENCES].append(
            {
                db_c.API_ID: audience[db_c.API_ID],
                db_c.DESTINATIONS: audience[db_c.DESTINATIONS],
            }
        )

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
        return list(collection.find({db_c.DELETED: False}, {db_c.DELETED: 0}))
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
            {db_c.ID: engagement_id, db_c.DELETED: False}, {db_c.DELETED: 0}
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
            {"$set": {db_c.DELETED: True}},
            upsert=False,
            new=True,
        )
        return doc[db_c.DELETED]
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
    audiences: list = None,
    delivery_schedule: dict = None,
) -> dict:
    """A function to update fields in an engagement

    Args:
        database (DatabaseClient): A database client.
        engagement_id (ObjectId): ObjectID of the engagement to be updated.
        user_id (ObjectId): ObjectID of user.
        name (str): Name of the engagement.
        description (str): Descriptions of the engagement.
        audiences (list): list of audiences.
        delivery_schedule (dict): delivery schedule dict.

    Returns:
        dict: dict object of the engagement that has been updated
    """

    if audiences:
        validate_audiences(audiences, check_empty=True)

    collection = database[db_c.DATA_MANAGEMENT_DATABASE][
        db_c.ENGAGEMENTS_COLLECTION
    ]

    update_doc = {
        db_c.ENGAGEMENT_NAME: name,
        db_c.ENGAGEMENT_DESCRIPTION: description,
        db_c.AUDIENCES: audiences,
        db_c.ENGAGEMENT_DELIVERY_SCHEDULE: delivery_schedule,
        db_c.UPDATE_TIME: datetime.datetime.utcnow(),
        db_c.UPDATED_BY: user_id,
    }

    # remove dict entries that are None
    update_doc = {k: v for k, v in update_doc.items() if v is not None}

    try:
        if update_doc:
            return collection.find_one_and_update(
                {db_c.ID: engagement_id, db_c.DELETED: False},
                {"$set": update_doc},
                {db_c.DELETED: 0},
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
# pylint: disable=too-many-arguments
# pylint: disable=no-else-return
def remove_audiences_from_engagement(
    database: DatabaseClient,
    engagement_id: ObjectId,
    user_id: ObjectId,
    audience_ids: list,
) -> dict:
    """A function to allow for removing audiences from an engagement.

    Args:
        database (DatabaseClient): A database client.
        engagement_id (ObjectId): ObjectID of the engagement to be updated.
        user_id (ObjectId): ObjectID of user.
        audience_ids (list): list of audience ObjectIds.

    Returns:
        dict: dict object of the engagement that has been updated
    """

    # validate audiences
    validate_object_id_list(audience_ids)

    collection = database[db_c.DATA_MANAGEMENT_DATABASE][
        db_c.ENGAGEMENTS_COLLECTION
    ]

    try:
        return collection.find_one_and_update(
            {db_c.ID: engagement_id},
            {
                "$pull": {
                    f"{db_c.AUDIENCES}": {db_c.API_ID: {"$in": audience_ids}}
                },
                "$set": {
                    db_c.UPDATE_TIME: datetime.datetime.utcnow(),
                    db_c.UPDATED_BY: user_id,
                },
            },
            upsert=False,
            return_document=pymongo.ReturnDocument.AFTER,
        )

    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
# pylint: disable=too-many-arguments
# pylint: disable=no-else-return
def append_audiences_to_engagement(
    database: DatabaseClient,
    engagement_id: ObjectId,
    user_id: ObjectId,
    audiences: list,
) -> dict:
    """A function to allow for appending audiences to an engagement.

    Args:
        database (DatabaseClient): A database client.
        engagement_id (ObjectId): ObjectID of the engagement to be updated.
        user_id (ObjectId): ObjectID of user.
        audiences (list): list of audiences.

    Returns:
        dict: dict object of the engagement that has been updated
    """

    # validate audiences
    validate_audiences(audiences)

    collection = database[db_c.DATA_MANAGEMENT_DATABASE][
        db_c.ENGAGEMENTS_COLLECTION
    ]

    try:
        return collection.find_one_and_update(
            {db_c.ID: engagement_id},
            {
                "$set": {
                    db_c.UPDATE_TIME: datetime.datetime.utcnow(),
                    db_c.UPDATED_BY: user_id,
                },
                "$push": {db_c.AUDIENCES: {"$each": audiences}},
            },
            upsert=False,
            return_document=pymongo.ReturnDocument.AFTER,
        )

    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


def validate_audiences(audiences: list, check_empty: bool = True) -> None:
    """A function for validating a list of audience objects.

    Args:
        audiences (list): list of audiences.
        check_empty (bool): check empty list.
    Returns:

    """
    if not audiences and check_empty:
        raise AttributeError("A minimum of one audience is required.")

    # validate the audience has an ID
    for audience in audiences:
        if not isinstance(audience, dict):
            raise AttributeError("Audience must be a dict.")
        if db_c.API_ID not in audience:
            raise KeyError(f"Missing audience {db_c.API_ID}.")
        if not isinstance(audience[db_c.API_ID], ObjectId):
            raise ValueError("Must provide an ObjectId.")
        if not ObjectId(audience[db_c.API_ID]):
            raise ValueError("Invalid object id value.")


def validate_object_id_list(
    object_ids: list, check_empty: bool = True
) -> None:
    """A function for validating a list of object ids.

    Args:
        object_ids (list): list of object ids.
        check_empty (bool): check empty list.

    Returns:

    """
    if not object_ids and check_empty:
        raise AttributeError("A minimum of one item is required.")

    # validate the list
    for object_id in object_ids:
        if not isinstance(object_id, ObjectId):
            raise ValueError("Must provide an ObjectId.")
