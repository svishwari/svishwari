"""This module enables functionality related to engagement management."""

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


# pylint: disable=too-many-arguments
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
    """A function to create an engagement.

    Args:
        database (DatabaseClient): A database client.
        name (str): Name of the engagement.
        description (str): Description of the engagement.
        audiences (list): List of audiences assigned to the engagement.
        user_name (str): Name of the user creating the engagement.
        delivery_schedule (dict): Delivery Schedule dict.
        deleted (bool): if the engagement is deleted (soft-delete).

    Returns:
        ObjectId: id of the newly created engagement.

    Raises:
        DuplicateName: Error if an engagement with the same name exists
            already.
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
        db_c.STATUS: "Active",
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
def get_engagements_summary(
    database: DatabaseClient, engagement_ids: list = None
) -> Union[list, None]:
    """A function to get all engagements summary with all nested lookups.

    Args:
        database (DatabaseClient): A database client.
        engagement_ids (list): Optional engagement id filter list.

    Returns:
        Union[list, None]: List of all engagement documents.
    """

    collection = database[db_c.DATA_MANAGEMENT_DATABASE][
        db_c.ENGAGEMENTS_COLLECTION
    ]

    match_statement = {db_c.DELETED: False}
    if engagement_ids:
        match_statement[db_c.ID] = {"$in": engagement_ids}

    pipeline = [
        # filter out the deleted engagements
        {"$match": match_statement},
        # unwind the audiences object so we can do the nested joins.
        {
            "$unwind": {
                "path": "$audiences",
                "preserveNullAndEmptyArrays": True,
            }
        },
        # lookup audience objects to the audience collection to get name.
        {
            "$lookup": {
                "from": "audiences",
                "localField": "audiences.id",
                "foreignField": "_id",
                "as": "audience",
            }
        },
        # unwind the found audiences to an object.
        {"$unwind": {"path": "$audience", "preserveNullAndEmptyArrays": True}},
        # add the audience name field to the nested audience object
        {
            "$addFields": {
                "audiences.name": "$audience.name",
                "audiences.size": "$audience.size",
                "audiences.created_by": "$audience.created_by",
                "audiences.updated_by": "$audience.updated_by",
                "audiences.update_time": "$audience.update_time",
                "audiences.create_time": "$audience.create_time",
            }
        },
        # remove the unused audience object fields.
        {"$project": {"audience": 0}},
        # lookup audience objects to the lookalike_audience collection
        # to get lookalike_audience name.
        {
            "$lookup": {
                "from": "lookalike_audiences",
                "localField": "audiences.id",
                "foreignField": "_id",
                "as": "lookalikes",
            }
        },
        # unwind the found lookalike_audiences to an object.
        {
            "$unwind": {
                "path": "$lookalikes",
                "preserveNullAndEmptyArrays": True,
            }
        },
        # add the lookalike id field by assigning None directly. this is a workaround because
        # document DB does not support LET statements in pipelines.
        {
            "$addFields": {
                "lookalike_id": {"$ifNull": ["$lookalikes._id", None]}
            }
        },
        # coalesce the unwind of an audience with lookalikes
        {
            "$addFields": {
                "audiences": {
                    "$cond": [
                        {"$eq": ["$lookalike_id", None]},
                        "$audiences",
                        "$lookalikes",
                    ]
                }
            }
        },
        # add the lookalike flag, lookalike audience id and destination id
        {
            "$addFields": {
                "audiences.is_lookalike": {
                    "$cond": [{"$eq": ["$lookalike_id", None]}, False, True]
                },
                "audiences.id": {
                    "$ifNull": ["$audiences.id", "$audiences._id"]
                },
                "audiences.destinations": {
                    "$cond": [
                        {"$eq": ["$lookalike_id", None]},
                        "$audiences.destinations",
                        [{"id": "$lookalikes.delivery_platform_id"}],
                    ]
                },
            }
        },
        # remove the unused lookalike audience object fields.
        {"$project": {"lookalikes": 0, "lookalike_id": 0}},
        # unwind the destinations
        {
            "$unwind": {
                "path": "$audiences.destinations",
                "preserveNullAndEmptyArrays": True,
            }
        },
        # lookup the embedded destinations
        {
            "$lookup": {
                "from": "delivery_platforms",
                "localField": "audiences.destinations.id",
                "foreignField": "_id",
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
                "audiences.destinations.is_ad_platform": "$destination.is_ad_platform",
                "audiences.destinations.name": "$destination.name",
                "audiences.destinations.delivery_platform_type"
                "": "$destination.delivery_platform_type",
            }
        },
        # remove the found destination from the pipeline.
        {"$project": {"destination": 0}},
        # lookup the latest delivery job
        {
            "$lookup": {
                "from": "delivery_jobs",
                "localField": "audiences.destinations.delivery_job_id",
                "foreignField": "_id",
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
                "audiences.destinations.latest_delivery": "$delivery_job",
            }
        },
        # remove the found delivery job from the top level.
        {"$project": {"delivery_job": 0, "deleted": 0}},
        {
            # group by the nested array of destinations first.
            "$group": {
                "_id": {
                    "_id": "$_id",
                    "name": "$name",
                    "description": "$description",
                    "status": "$status",
                    "create_time": "$create_time",
                    "created_by": "$created_by",
                    "updated_by": "$updated_by",
                    "update_time": "$update_time",
                    # because the audience is a nested object, pull out the
                    # audience fields we need for later grouping
                    "audience_name": "$audiences.name",
                    "audience_id": "$audiences.id",
                    "audience_size": "$audiences.size",
                    "audience_created_by": "$audiences.created_by",
                    "audience_updated_by": "$audiences.updated_by",
                    "audience_update_time": "$audiences.update_time",
                    "audience_create_time": "$audiences.create_time",
                    "is_audience_lookalike": "$audiences.is_lookalike",
                    "delivery_schedule": {
                        "$ifNull": ["$delivery_schedule", ""]
                    },
                },
                # push the grouped destinations into an array
                "destinations": {
                    "$push": {
                        "id": "$audiences.destinations.id",
                        "name": "$audiences.destinations.name",
                        "is_ad_platform": "$audiences.destinations.is_ad_platform",
                        "delivery_platform_type": "$audiences.destinations.delivery_platform_type",
                        "delivery_job_id": "$audiences.destinations.delivery_job_id",
                        "delivery_schedule": {
                            "$ifNull": [
                                "$audiences.destinations.delivery_schedule",
                                "",
                            ]
                        },
                        "latest_delivery": {
                            "update_time": "$audiences.destinations.latest_delivery.update_time",
                            "status": {
                                "$ifNull": [
                                    "$audiences.destinations.latest_delivery.status",
                                    db_c.AUDIENCE_STATUS_NOT_DELIVERED,
                                ]
                            },
                            "size": "$audiences.destinations.latest_delivery."
                            "delivery_platform_audience_size",
                        },
                    }
                },
            }
        },
        {
            # group by the audiences now
            "$group": {
                "_id": {
                    "_id": "$_id._id",
                    "name": "$_id.name",
                    "description": "$_id.description",
                    "status": "$_id.status",
                    "create_time": "$_id.create_time",
                    "created_by": "$_id.created_by",
                    "updated_by": "$_id.updated_by",
                    "update_time": "$_id.update_time",
                    "delivery_schedule": "$_id.delivery_schedule",
                },
                # push all the audiences into an array
                "audiences": {
                    "$push": {
                        "id": "$_id.audience_id",
                        "name": "$_id.audience_name",
                        "size": "$_id.audience_size",
                        "created_by": "$_id.audience_created_by",
                        "updated_by": "$_id.audience_updated_by",
                        "update_time": "$_id.audience_update_time",
                        "create_time": "$_id.audience_create_time",
                        "destinations": "$destinations",
                        "is_lookalike": "$_id.is_audience_lookalike",
                    }
                },
                "size": {"$sum": "$_id.audience_size"},
            }
        },
        {
            # project the fields we need.
            "$project": {
                "_id": "$_id._id",
                "name": "$_id.name",
                "description": "$_id.description",
                "status": "$_id.status",
                "create_time": "$_id.create_time",
                "created_by": "$_id.created_by",
                "updated_by": "$_id.updated_by",
                "update_time": "$_id.update_time",
                "audiences": "$audiences",
                "delivery_schedule": "$_id.delivery_schedule",
                "size": "$size",
            }
        },
    ]

    try:
        return list(collection.aggregate(pipeline))
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_engagements(database: DatabaseClient) -> Union[list, None]:
    """A function to get all engagements.

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
    """A function to get an engagement based on ID.

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
    database: DatabaseClient,
    engagement_id: ObjectId,
    hard_delete: bool = False,
) -> bool:
    """A function to delete an engagement based on ID.

    Args:
        database (DatabaseClient): A database client.
        engagement_id (ObjectId): Object Id of the engagement.
        hard_delete (bool): hard deletes an engagement if True.

    Returns:
        bool: Flag indicating successful operation.
    """

    collection = database[db_c.DATA_MANAGEMENT_DATABASE][
        db_c.ENGAGEMENTS_COLLECTION
    ]

    try:
        if hard_delete:
            collection.delete_one({db_c.ID: engagement_id})
            return True
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
    status: str = None,
) -> Union[dict, None]:
    """A function to update fields in an engagement.

    Args:
        database (DatabaseClient): A database client.
        engagement_id (ObjectId): ObjectID of the engagement to be updated.
        user_name (str): Name of the user updating the engagement.
        name (str): Name of the engagement.
        description (str): Descriptions of the engagement.
        audiences (list): list of audiences.
        delivery_schedule (dict): delivery schedule dict.
        status (str): Engagement status.

    Returns:
        Union[dict, None]: dict object of the engagement that has been updated.

    Raises:
        NoUpdatesSpecified: Error if no updates were done to the engagement.
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
        db_c.STATUS: status,
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
        Union[dict, None]: dict object of the engagement that has been updated.
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
        Union[dict, None]: dict object of the engagement that has been updated.
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

    Raises:
        AttributeError: If check_empty is true and passed in audiences
            collection is empty.
        KeyError: If an audience object in the audiences collection does not
            have an ID field.
        ValueError: If ID field of an audience object is invalid.
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
    """A function to get a list of engagements by audience_id.

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

    Raises:
        AttributeError: If check_empty is true and passed in object_ids
            collection is empty.
        ValueError: If ID field of an audience object is invalid.
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
    """A function to update fields in an engagement.

    Args:
        database (DatabaseClient): A database client.
        engagement_id (ObjectId): ObjectID of the engagement.
        audience_id (ObjectId): ObjectID of the audience.
        destination_id (ObjectId): ObjectID of the destination.
        delivery_job_id (ObjectId): ObjectID of the delivery job.

    Returns:
        Union[dict, None]: dict object of the engagement that has been updated.
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


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def append_destination_to_engagement_audience(
    database: DatabaseClient,
    engagement_id: ObjectId,
    audience_id: ObjectId,
    destination: dict,
    user_name: str,
) -> dict:
    """A function to append destination to engagement audience.

    Args:
        database (DatabaseClient): A database client.
        engagement_id (ObjectId): MongoDB ID of the engagement.
        audience_id (ObjectId): MongoDB ID of the audience.
        destination (dict): Destination to add to engagement audience.
        user_name (str): Name of the user appending the destination to the
            audience.

    Returns:
        dict: updated engagement object.
    """

    collection = database[db_c.DATA_MANAGEMENT_DATABASE][
        db_c.ENGAGEMENTS_COLLECTION
    ]

    return collection.find_one_and_update(
        {db_c.ID: engagement_id, "audiences.id": audience_id},
        {
            "$set": {
                db_c.UPDATE_TIME: datetime.datetime.utcnow(),
                db_c.UPDATED_BY: user_name,
            },
            "$push": {"audiences.$.destinations": destination},
        },
    )


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def remove_destination_from_engagement_audience(
    database: DatabaseClient,
    engagement_id: ObjectId,
    audience_id: ObjectId,
    destination_id: ObjectId,
    user_name: str,
) -> dict:
    """A function to remove destination from engagement audience.

    Args:
        database (DatabaseClient): A database client.
        engagement_id (ObjectId): MongoDB ID of the engagement.
        audience_id (ObjectId): MongoDB ID of the audience.
        destination_id (ObjectId): MongoDB ID of the destination to be removed.
        user_name (str): Name of the user removing the destination from the
            audience.

    Returns:
        dict: updated engagement object.
    """

    collection = database[db_c.DATA_MANAGEMENT_DATABASE][
        db_c.ENGAGEMENTS_COLLECTION
    ]

    # workaround due to limitation in DocumentDB
    engagement_doc = collection.find_one(
        {
            db_c.ID: engagement_id,
            "audiences.id": audience_id,
            "audiences.destinations.id": destination_id,
        }
    )
    if not engagement_doc:
        return {}

    # Workaround cause DocumentDB does not support nested DB updates.
    change = False
    for audience in engagement_doc.get(db_c.AUDIENCES, []):
        if audience.get(db_c.OBJECT_ID) != audience_id:
            continue

        for i, destination in enumerate(audience.get(db_c.DESTINATIONS, [])):
            if destination.get(db_c.OBJECT_ID) != destination_id:
                continue

            audience[db_c.DESTINATIONS].pop(i)

            engagement_doc[db_c.UPDATE_TIME] = datetime.datetime.utcnow()
            engagement_doc[db_c.UPDATED_BY] = user_name
            change = True
            break

    # no changes, simply return.
    if not change:
        return {}

    # replace_one
    collection.replace_one(
        {
            db_c.ID: engagement_id,
        },
        engagement_doc,
    )

    return collection.find_one(
        {
            db_c.ID: engagement_id,
        }
    )


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def check_active_engagement_deliveries(
    database: DatabaseClient,
) -> Union[list, None]:
    """A function to get all the active engagement deliveries.

    Args:
        database (DatabaseClient): A database client.

    Returns:
        Union[list, None]: List of all engagement documents.
    """

    collection = database[db_c.DATA_MANAGEMENT_DATABASE][
        db_c.ENGAGEMENTS_COLLECTION
    ]

    pipeline = [
        {"$match": {"status": "Active", "deleted": False}},
        {
            "$unwind": {
                "path": "$audiences",
                "preserveNullAndEmptyArrays": False,
            }
        },
        {"$unwind": {"path": "$audiences.destinations"}},
        {
            "$match": {
                "audiences.destinations.delivery_job_id": {"$exists": True}
            }
        },
        {
            "$addFields": {
                "delivery_job_id": "$audiences.destinations.delivery_job_id"
            }
        },
        {
            "$lookup": {
                "from": "delivery_jobs",
                "localField": "delivery_job_id",
                "foreignField": "_id",
                "as": "delivery_job_id",
            }
        },
        {"$unwind": {"path": "$delivery_job_id"}},
        {"$match": {"delivery_job_id.status": "Delivered"}},
    ]

    try:
        return list(collection.aggregate(pipeline))
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None
