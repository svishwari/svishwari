"""This module enables functionality related
to orchestration (audience/engagement) management.
"""

import logging
import datetime
from typing import Union

from bson import ObjectId
import pymongo
from tenacity import retry, wait_fixed, retry_if_exception_type

import huxunifylib.database.db_exceptions as de
import huxunifylib.database.constants as c
from huxunifylib.database.client import DatabaseClient
from huxunifylib.database.user_management import USER_LOOKUP_PIPELINE


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def create_audience(
    database: DatabaseClient,
    name: str,
    audience_filters: list,
    destination_ids: list = None,
    user_name: str = None,
    size: int = 0,
) -> Union[dict, None]:
    """A function to create an audience.

    Args:
        database (DatabaseClient): A database client.
        name (str): Name of the audience.
        audience_filters (list of list): Multiple sections of audience filters.
        These are aggregated using "OR".
        destination_ids (list): List of destination
            / delivery platform ids attached to the audience
        user_name (str): Name of the user creating / updating the audience
        size (int): audience size.

    Returns:
        Union[list, None]: MongoDB audience doc.
    """

    am_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = am_db[c.AUDIENCES_COLLECTION]

    # Make sure the name will be unique
    try:
        if collection.find_one({c.AUDIENCE_NAME: name}):
            raise de.DuplicateName(name)
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    # Get current time
    curr_time = datetime.datetime.utcnow()

    audience_doc = {
        c.AUDIENCE_NAME: name,
        c.AUDIENCE_FILTERS: audience_filters,
        c.DESTINATIONS: destination_ids if destination_ids else [],
        c.CREATE_TIME: curr_time,
        c.UPDATE_TIME: curr_time,
        c.CREATED_BY: user_name,
        c.UPDATED_BY: user_name,
        c.FAVORITE: False,
        c.DELETED: False,
        c.SIZE: size,
    }

    try:
        audience_id = collection.insert_one(audience_doc).inserted_id
        if audience_id is not None:
            return collection.find_one(
                {c.ID: audience_id, c.DELETED: False}, {c.DELETED: 0}
            )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_audience_by_filter(
    database: DatabaseClient,
    filter_dict: dict = None,
    projection: dict = None,
    sort_list: list = None,
    limit: int = None,
) -> Union[list, None]:
    """A function to get all delivery platform lookalike audience configurations.

    Args:
        database (DatabaseClient): A database client.
        filter_dict (dict): filter dictionary for adding custom filters.
        projection (dict): Dict that specifies which fields to return or not return.
        sort_list (list): List of tuples to sort by. Example: [(c.CREATE_TIME, pymongo.DESCENDING)]
        limit (int): limit for number of audiences returned.

    Returns:
        Union[list, None]: List of all lookalike audience configurations.

    """

    collection = database[c.DATA_MANAGEMENT_DATABASE][c.AUDIENCES_COLLECTION]

    # if deleted is not included in the filters, add it.
    if filter_dict:
        filter_dict[c.DELETED] = False
    else:
        filter_dict = {c.DELETED: False}

    # exclude the deleted field from returning
    if projection:
        projection[c.DELETED] = 0
    else:
        projection = {c.DELETED: 0}

    if not isinstance(limit, int) and limit is not None:
        raise de.InvalidValueException(limit)

    try:
        cursor = collection.find(filter_dict, projection)

        if sort_list:
            cursor = cursor.sort(sort_list)

        return list(cursor if limit else cursor.limit(limit))
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_audience(
    database: DatabaseClient,
    audience_id: ObjectId,
    include_users: bool = False,
) -> Union[dict, None]:
    """A function to get an audience.

    Args:
        database (DatabaseClient): A database client.
        audience_id (ObjectId): The Mongo DB ID of the audience.
        include_users (bool): Flag to include users.
    Returns:
        Union[dict, None]:  An audience document.

    """
    doc = None
    am_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = am_db[c.AUDIENCES_COLLECTION]

    # Read the audience document which contains filtering rules
    try:
        if include_users:
            docs = list(
                collection.aggregate(
                    [
                        {"$match": {c.ID: audience_id, c.DELETED: False}},
                        {c.DELETED: 0},
                    ]
                    + USER_LOOKUP_PIPELINE
                )
            )
            return docs[0] if docs else None

        return collection.find_one(
            {c.ID: audience_id, c.DELETED: False}, {c.DELETED: 0}
        )
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
    database: DatabaseClient, include_users: bool = False
) -> Union[list, None]:
    """A function to get all existing audiences.

    Args:
        database (DatabaseClient): A database client.
        include_users (bool): Flag to include users.

    Returns:
        Union[list, None]: A list of all audiences.

    """

    am_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = am_db[c.AUDIENCES_COLLECTION]

    # Get audience configurations and add to list
    try:
        if include_users:
            # lookup to users
            return list(
                collection.aggregate(
                    [{"$match": {c.DELETED: False}}, {c.DELETED: 0}]
                    + USER_LOOKUP_PIPELINE
                )
            )

        return list(collection.find({c.DELETED: False}, {c.DELETED: 0}))
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
    name: str = None,
    audience_filters: list = None,
    destination_ids: list = None,
    user_name: str = None,
) -> Union[dict, None]:
    """A function to update an audience.
    Args:
        database (DatabaseClient): A database client.
        audience_id (ObjectId): MongoDB ID of the audience.
        name (str): New audience name.
        audience_filters (list of list): Multiple sections of audience filters.
            These are aggregated using "OR".
        destination_ids (list): List of destination / delivery platform
            ids attached to the audience
        user_name (str): Name of the user creating / updating the audience
    Returns:
        Union[dict, None]: Updated audience configuration dict.
    """

    am_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = am_db[c.AUDIENCES_COLLECTION]

    try:
        audience_doc = collection.find_one(
            {c.ID: audience_id, c.DELETED: False}, {c.DELETED: 0}
        )
        if not audience_doc:
            raise de.InvalidID()
        if name is not None:
            duplicate_name_doc = collection.find_one(
                {c.AUDIENCE_NAME: name, c.DELETED: False}, {c.DELETED: 0}
            )
            if (
                duplicate_name_doc is not None
                and duplicate_name_doc[c.ID] != audience_id
            ):
                raise de.DuplicateName(name)
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    # Get current time
    curr_time = datetime.datetime.utcnow()

    updated_audience_doc = audience_doc
    if name is not None:
        updated_audience_doc[c.AUDIENCE_NAME] = name
    if audience_filters is not None:
        updated_audience_doc[c.AUDIENCE_FILTERS] = audience_filters
    if destination_ids is not None:
        updated_audience_doc[c.DESTINATIONS] = destination_ids
    if user_name:
        updated_audience_doc[c.UPDATED_BY] = user_name
    updated_audience_doc[c.UPDATE_TIME] = curr_time

    try:
        return collection.find_one_and_update(
            {c.ID: audience_id},
            {"$set": updated_audience_doc},
            upsert=False,
            return_document=pymongo.ReturnDocument.AFTER,
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_audience_insights(
    database: DatabaseClient,
    audience_id: ObjectId,
) -> Union[list, None]:
    """A function to get audience insights.

    Args:
        database (DatabaseClient): A database client.
        audience_id (ObjectId): The Mongo DB ID of the audience.

    Returns:
        Union[list, None]:  A list of engagements with delivery information for an audience

    """
    am_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = am_db[c.ENGAGEMENTS_COLLECTION]

    # use the audience pipeline to aggregate and join all the insight data
    try:
        return list(
            collection.aggregate(
                [
                    {"$match": {"audiences.id": audience_id}},
                    {
                        "$unwind": {
                            "path": "$audiences",
                            "preserveNullAndEmptyArrays": True,
                        }
                    },
                    {
                        "$unwind": {
                            "path": "$audiences.destinations",
                            "preserveNullAndEmptyArrays": True,
                        }
                    },
                    {"$match": {"audiences.id": audience_id}},
                    {
                        "$lookup": {
                            "from": "delivery_platforms",
                            "localField": "audiences.destinations.id",
                            "foreignField": "_id",
                            "as": "delivery_platforms",
                        }
                    },
                    {
                        "$unwind": {
                            "path": "$delivery_platforms",
                            "preserveNullAndEmptyArrays": True,
                        }
                    },
                    {
                        "$lookup": {
                            "from": "delivery_jobs",
                            "localField": "audiences.destinations.delivery_job_id",
                            "foreignField": "_id",
                            "as": "deliveries",
                        }
                    },
                    {
                        "$unwind": {
                            "path": "$deliveries",
                            "preserveNullAndEmptyArrays": True,
                        }
                    },
                    {
                        "$addFields": {
                            "deliveries": {
                                "$ifNull": [
                                    "$deliveries",
                                    "$delivery_platforms",
                                ]
                            }
                        }
                    },
                    {
                        "$addFields": {
                            "deliveries.delivery_platform_id": "$delivery_platforms._id"
                        }
                    },
                    {"$project": {"audiences": 0, "delivery_platforms": 0}},
                    {
                        "$lookup": {
                            "from": "delivery_platforms",
                            "localField": "deliveries.delivery_platform_id",
                            "foreignField": "_id",
                            "as": "destinations",
                        }
                    },
                    {
                        "$unwind": {
                            "path": "$destinations",
                            "preserveNullAndEmptyArrays": True,
                        }
                    },
                    {
                        "$addFields": {
                            "deliveries.delivery_platform_type"
                            "": "$destinations.delivery_platform_type",
                            "deliveries.name": "$destinations.name",
                            "deliveries.status": {
                                "$ifNull": [
                                    "$deliveries.status",
                                    c.AUDIENCE_STATUS_NOT_DELIVERED,
                                ]
                            },
                            "deliveries.id": "$destinations.id",
                        }
                    },
                    {
                        "$group": {
                            "_id": "$_id",
                            "deliveries": {"$push": "$deliveries"},
                            "last_delivered": {
                                "$last": "$deliveries.update_time"
                            },
                        }
                    },
                    {
                        "$lookup": {
                            "from": "engagements",
                            "localField": "_id",
                            "foreignField": "_id",
                            "as": "engagement",
                        }
                    },
                    {
                        "$project": {
                            "engagement.audiences": 0,
                            "engagement.deleted": 0,
                            "deliveries.deleted": 0,
                        }
                    },
                    {
                        "$unwind": {
                            "path": "$engagement",
                            "preserveNullAndEmptyArrays": True,
                        }
                    },
                ]
            )
        )

    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None
