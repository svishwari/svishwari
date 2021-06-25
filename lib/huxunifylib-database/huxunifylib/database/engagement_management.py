"""
This module enables functionality related to engagement management.
"""

import logging
import datetime
from typing import Union

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
    user_name: str,
    delivery_schedule: dict = None,
    deleted: bool = False,
) -> ObjectId:
    """A function to create an engagement

    Args:
        database (DatabaseClient): A database client.
        name (str): Name of the engagement.
        description (str): Description of the engagement.
        audiences (list): List of audiences assigned to the engagement.
        user_name (str): Name of the user creating the engagement.
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
        db_c.CREATED_BY: user_name,
        db_c.UPDATED_BY: "",
        db_c.UPDATE_TIME: datetime.datetime.utcnow(),
        db_c.DELETED: deleted,
        db_c.AUDIENCES: [
            {
                db_c.OBJECT_ID: x[db_c.OBJECT_ID],
                db_c.DESTINATIONS: x[db_c.DESTINATIONS],
            }
            for x in audiences
        ]
        if audiences
        else [],
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
def get_engagements_summary(database: DatabaseClient) -> Union[list, None]:
    """A function to get all engagements summary with all nested lookups

    Args:
        database (DatabaseClient): A database client.

    Returns:
        Union[list, None]: List of all engagement documents.

    """

    collection = database[db_c.DATA_MANAGEMENT_DATABASE][
        db_c.ENGAGEMENTS_COLLECTION
    ]

    pipeline = [
        # filter out the deleted engagements
        {"$match": {db_c.DELETED: False}},
        # unwind the audiences object so we can do the nested joins.
        {
            "$unwind": {
                "path": f"${db_c.AUDIENCES}",
                "preserveNullAndEmptyArrays": True,
            }
        },
        # lookup audience objects to the audience collection to get name.
        {
            "$lookup": {
                "from": db_c.AUDIENCES,
                "localField": "audiences.id",
                "foreignField": db_c.ID,
                "as": "audience",
            }
        },
        # unwind the found audiences to an object.
        {"$unwind": {"path": "$audience", "preserveNullAndEmptyArrays": True}},
        # add the audience name field to the nested audience object
        {
            "$addFields": {
                f"{db_c.AUDIENCES}.{db_c.NAME}": f"$audience.{db_c.NAME}"
            }
        },
        # remove the unused audience object fields.
        {"$project": {"audience": 0}},
        # unwind the destinations
        {
            "$unwind": {
                "path": f"${db_c.AUDIENCES}.{db_c.DESTINATIONS}",
                "preserveNullAndEmptyArrays": True,
            }
        },
        # lookup the embedded destinations
        {
            "$lookup": {
                "from": db_c.DELIVERY_PLATFORM_COLLECTION,
                "localField": f"{db_c.AUDIENCES}.{db_c.DESTINATIONS}.{db_c.OBJECT_ID}",
                "foreignField": db_c.ID,
                "as": "destination",
            }
        },
        # unwind the found destinations
        {
            "$unwind": {
                "path": "$destination",
                "preserveNullAndEmptyArrays": True,
            }
        },
        # add the destination name to the nested destinations.
        {
            "$addFields": {
                f"{db_c.AUDIENCES}.{db_c.DESTINATIONS}.{db_c.NAME}": f"$destination.{db_c.NAME}"
            }
        },
        # remove the found destination from the pipeline.
        {"$project": {"destination": 0}},
        # lookup the latest delivery job
        {
            "$lookup": {
                "from": db_c.DELIVERY_JOBS_COLLECTION,
                "localField": f"{db_c.AUDIENCES}.{db_c.DESTINATIONS}.{db_c.DELIVERY_JOB_ID}",
                "foreignField": db_c.ID,
                "as": "delivery_job",
            }
        },
        # unwind the found delivery job into objects.
        {
            "$unwind": {
                "path": "$delivery_job",
                "preserveNullAndEmptyArrays": True,
            }
        },
        # add the delivery object to the nested destination via latest_delivery
        {
            "$addFields": {
                f"{db_c.AUDIENCES}.{db_c.DESTINATIONS}.latest_delivery": "$delivery_job"
            }
        },
        # remove the found delivery job from the top level.
        {"$project": {"delivery_job": 0, db_c.DELETED: 0}},
    ]

    try:
        dad = list(collection.aggregate(pipeline))

        # document DB does not support $$ROOT syntax, so we will group dynamically here
        return dad
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_engagements(database: DatabaseClient) -> Union[list, None]:
    """A function to get all engagements

    Args:
        database (DatabaseClient): A database client.

    Returns:
        Union[list, None]: List of all engagement documents.

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
def get_engagement(
    database: DatabaseClient, engagement_id: ObjectId
) -> Union[dict, None]:
    """A function to get an engagement based on ID

    Args:
        database (DatabaseClient): A database client.
        engagement_id (ObjectId): ObjectId of the engagement

    Returns:
        Union[dict, None]: Dict of an engagement.

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
    user_name: str,
    name: str = None,
    description: str = None,
    audiences: list = None,
    delivery_schedule: dict = None,
) -> Union[dict, None]:
    """A function to update fields in an engagement

    Args:
        database (DatabaseClient): A database client.
        engagement_id (ObjectId): ObjectID of the engagement to be updated.
        user_name (str): Name of the user updating the engagement.
        name (str): Name of the engagement.
        description (str): Descriptions of the engagement.
        audiences (list): list of audiences.
        delivery_schedule (dict): delivery schedule dict.

    Returns:
        Union[dict, None]: dict object of the engagement that has been updated
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
        db_c.UPDATED_BY: user_name,
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
    user_name: str,
    audience_ids: list,
) -> Union[dict, None]:
    """A function to allow for removing audiences from an engagement.

    Args:
        database (DatabaseClient): A database client.
        engagement_id (ObjectId): ObjectID of the engagement to be updated.
        user_name (str): Name of the user removing the engaged audience.
        audience_ids (list): list of audience ObjectIds.

    Returns:
        Union[dict, None]: dict object of the engagement that has been updated
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
                    f"{db_c.AUDIENCES}": {
                        db_c.OBJECT_ID: {"$in": audience_ids}
                    }
                },
                "$set": {
                    db_c.UPDATE_TIME: datetime.datetime.utcnow(),
                    db_c.UPDATED_BY: user_name,
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
    user_name: str,
    audiences: list,
) -> Union[dict, None]:
    """A function to allow for appending audiences to an engagement.

    Args:
        database (DatabaseClient): A database client.
        engagement_id (ObjectId): ObjectID of the engagement to be updated.
        user_name (str): Name of the user attaching the audience.
        audiences (list): list of audiences.

    Returns:
        Union[dict, None]: dict object of the engagement that has been updated
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
                    db_c.UPDATED_BY: user_name,
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
        if db_c.OBJECT_ID not in audience:
            raise KeyError(f"Missing audience {db_c.OBJECT_ID}.")
        if not isinstance(audience[db_c.OBJECT_ID], ObjectId):
            raise ValueError("Must provide an ObjectId.")
        if not ObjectId(audience[db_c.OBJECT_ID]):
            raise ValueError("Invalid object id value.")


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_engagements_by_audience(
    database: DatabaseClient, audience_id: ObjectId
) -> Union[list, None]:
    """A function to get a list of engagements by audience_id

    Args:
        database (DatabaseClient): A database client.
        audience_id (ObjectId): ObjectId of an audience

    Returns:
        Union[list, None]: list of engagements.

    """

    collection = database[db_c.DATA_MANAGEMENT_DATABASE][
        db_c.ENGAGEMENTS_COLLECTION
    ]

    try:
        return list(
            collection.find(
                {
                    f"{db_c.AUDIENCES}.{db_c.OBJECT_ID}": audience_id,
                    db_c.DELETED: False,
                },
                {db_c.DELETED: 0},
            )
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


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


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def add_delivery_job(
    database: DatabaseClient,
    engagement_id: ObjectId,
    audience_id: ObjectId,
    destination_id: ObjectId,
    delivery_job_id: ObjectId,
) -> Union[dict, None]:
    """A function to update fields in an engagement

    Args:
        database (DatabaseClient): A database client.
        engagement_id (ObjectId): ObjectID of the engagement.
        audience_id (ObjectId): ObjectID of the audience.
        destination_id (ObjectId): ObjectID of the destination.
        delivery_job_id (ObjectId): ObjectID of the delivery job.

    Returns:
        Union[dict, None]: dict object of the engagement that has been updated
    """

    # get the engagement collection
    collection = database[db_c.DATA_MANAGEMENT_DATABASE][
        db_c.ENGAGEMENTS_COLLECTION
    ]

    try:
        return collection.find_one_and_update(
            {
                db_c.ID: engagement_id,
                db_c.DELETED: False,
                db_c.AUDIENCES: {
                    "$elemMatch": {
                        db_c.OBJECT_ID: audience_id,
                        db_c.DESTINATIONS: {
                            "$elemMatch": {db_c.OBJECT_ID: destination_id}
                        },
                    }
                },
            },
            {
                "$set": {
                    f"{db_c.AUDIENCES}.$[i].{db_c.DESTINATIONS}.$[j]."
                    f"{db_c.DELIVERY_JOB_ID}": delivery_job_id
                }
            },
            {db_c.DELETED: 0},
            array_filters=[
                {
                    "i.id": audience_id,
                },
                {"j.id": destination_id},
            ],
            upsert=False,
            new=True,
        )

    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


def group_engagements(engagements: list) -> list:
    """Group engagements by audience/destinations.
    DocumentDB does not support graph lookup and/or $root.
    easier to do this in python instead of Mongo.
    We still leverage mongo to do the lookups,
    but we handle the grouping and status rollup here

    Args:
        engagements (list): list of engagement documents.

    Returns:
          list: list of engagement documents

    """

    core_lk = {}
    for item in engagements:
        # check if we already have a record for the engagement ID
        if item[db_c.ID] not in core_lk:
            # shallow copy into the core lookup dict
            core_lk[item[db_c.ID]] = item.copy()
            # set the audience field to an empty list.
            core_lk[item[db_c.ID]][db_c.AUDIENCES] = []

        # if audience list has data proceed
        if not core_lk[item[db_c.ID]][db_c.AUDIENCES]:
            # if audience has nested destinations, proceed.
            if db_c.DESTINATIONS in item[db_c.AUDIENCES]:
                item[db_c.AUDIENCES][db_c.DESTINATIONS] = [
                    item[db_c.AUDIENCES][db_c.DESTINATIONS]
                ]
            else:
                item[db_c.AUDIENCES][db_c.DESTINATIONS] = []
            core_lk[item[db_c.ID]][db_c.AUDIENCES] += [item[db_c.AUDIENCES]]

            continue

        # group the nested destinations into a singular list
        # within the audience object.
        for audience in core_lk[item[db_c.ID]][db_c.AUDIENCES]:
            # add the audience
            if (
                audience[db_c.OBJECT_ID]
                == item[db_c.AUDIENCES][db_c.OBJECT_ID]
            ):
                # add destination
                audience[db_c.DESTINATIONS] += [
                    item[db_c.AUDIENCES][db_c.DESTINATIONS]
                ]

    return list(core_lk.values())
