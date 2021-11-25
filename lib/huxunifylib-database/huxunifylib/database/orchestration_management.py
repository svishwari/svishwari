"""This module enables functionality related to
orchestration(audience/engagement) management.
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
from huxunifylib.database.user_management import USER_LOOKUP_PIPELINE


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
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
        destination_ids (list): List of destination/delivery platform ids
            attached to the audience.
        user_name (str): Name of the user creating / updating the audience.
        size (int): audience size.

    Returns:
        Union[list, None]: MongoDB audience doc.

    Raises:
        DuplicateName: Error if an audience with the same name exists
            already.
    """

    am_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    collection = am_db[db_c.AUDIENCES_COLLECTION]

    # Make sure the name will be unique
    try:
        if collection.find_one({db_c.AUDIENCE_NAME: name}):
            raise de.DuplicateName(name)
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    # Get current time
    curr_time = datetime.datetime.utcnow()

    audience_doc = {
        db_c.AUDIENCE_NAME: name,
        db_c.AUDIENCE_FILTERS: audience_filters,
        db_c.DESTINATIONS: destination_ids if destination_ids else [],
        db_c.CREATE_TIME: curr_time,
        db_c.UPDATE_TIME: curr_time,
        db_c.CREATED_BY: user_name,
        db_c.UPDATED_BY: user_name,
        db_c.FAVORITE: False,
        db_c.DELETED: False,
        db_c.SIZE: size,
    }

    try:
        audience_id = collection.insert_one(audience_doc).inserted_id
        if audience_id is not None:
            return collection.find_one(
                {db_c.ID: audience_id, db_c.DELETED: False}, {db_c.DELETED: 0}
            )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_audience_by_filter(
    database: DatabaseClient,
    filter_dict: dict = None,
    projection: dict = None,
    sort_list: list = None,
    limit: int = None,
) -> Union[list, None]:
    """A function to get all delivery platform lookalike audience
    configurations.

    Args:
        database (DatabaseClient): A database client.
        filter_dict (dict): filter dictionary for adding custom filters.
        projection (dict): Dict that specifies which fields to return or
            not return.
        sort_list (list): List of tuples to sort by.
            Example: [(db_c.CREATE_TIME, pymongo.DESCENDING)]
        limit (int): limit for number of audiences returned.

    Returns:
        Union[list, None]: List of all lookalike audience configurations.

    Raises:
        InvalidValueException: If passed in limit value is invalid.
    """

    collection = database[db_c.DATA_MANAGEMENT_DATABASE][db_c.AUDIENCES_COLLECTION]

    # if deleted is not included in the filters, add it.
    if filter_dict:
        filter_dict[db_c.DELETED] = False
    else:
        filter_dict = {db_c.DELETED: False}

    # exclude the deleted field from returning
    if projection:
        projection[db_c.DELETED] = 0
    else:
        projection = {db_c.DELETED: 0}

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
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
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

    Raises:
        InvalidID: If the passed in audience_id did not fetch a doc from the
            relevant db collection.
    """

    doc = None
    am_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    collection = am_db[db_c.AUDIENCES_COLLECTION]

    # Read the audience document which contains filtering rules
    try:
        if include_users:
            docs = list(
                collection.aggregate(
                    [
                        {"$match": {db_c.ID: audience_id, db_c.DELETED: False}},
                        {db_c.DELETED: 0},
                    ]
                    + USER_LOOKUP_PIPELINE
                )
            )
            return docs[0] if docs else None

        return collection.find_one(
            {db_c.ID: audience_id, db_c.DELETED: False}, {db_c.DELETED: 0}
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    if doc is None:
        raise de.InvalidID(audience_id)

    return doc


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_all_audiences(
    database: DatabaseClient,
    include_users: bool = False,
    filters: dict = None,
    audience_ids: list = None,
) -> Union[list, None]:
    """A function to get all existing audiences.

    Args:
        database (DatabaseClient): A database client.
        include_users (bool): Flag to include users.
        filters (dict, Optional): A dict of filters to be applied on the
        audience.
        audience_ids (list, Optional): A list of audience IDs.

    Returns:
        Union[list, None]: A list of all audiences.
    """
    am_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    collection = am_db[db_c.AUDIENCES_COLLECTION]

    if not filters:
        find_filters = {db_c.DELETED: False}
    else:
        find_filters = {}
        if filters.get(db_c.WORKED_BY):
            find_filters["$or"] = [
                {db_c.CREATED_BY: filters.get(db_c.WORKED_BY)},
                {db_c.UPDATED_BY: filters.get(db_c.WORKED_BY)},
            ]
        if filters.get(db_c.ATTRIBUTE):
            find_filters["$and"] = [
                {db_c.ATTRIBUTE_FILTER_FIELD: attribute}
                for attribute in filters.get(db_c.ATTRIBUTE)
            ]

    if audience_ids is not None:
        find_filters[db_c.ID] = {"$in": audience_ids}

    # Get audience configurations and add to list
    try:
        if include_users:
            # lookup to users
            return list(
                collection.aggregate(
                    [{"$match": {db_c.DELETED: False}}, {db_c.DELETED: 0}]
                    + USER_LOOKUP_PIPELINE
                )
            )

        return list(collection.find(find_filters, {db_c.DELETED: 0}))
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
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
        destination_ids (list): List of destination/delivery platform
            ids attached to the audience.
        user_name (str): Name of the user creating/updating the audience.

    Returns:
        Union[dict, None]: Updated audience configuration dict.

    Raises:
        InvalidID: If the passed in audience_id did not fetch a doc from the
            relevant db collection.
        DuplicateName: Error if an audience with the same name exists already.
    """

    am_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    collection = am_db[db_c.AUDIENCES_COLLECTION]

    try:
        audience_doc = collection.find_one(
            {db_c.ID: audience_id, db_c.DELETED: False}, {db_c.DELETED: 0}
        )
        if not audience_doc:
            raise de.InvalidID()
        if name is not None:
            duplicate_name_doc = collection.find_one(
                {db_c.AUDIENCE_NAME: name, db_c.DELETED: False}, {db_c.DELETED: 0}
            )
            if (
                duplicate_name_doc is not None
                and duplicate_name_doc[db_c.ID] != audience_id
            ):
                raise de.DuplicateName(name)
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    # Get current time
    curr_time = datetime.datetime.utcnow()

    updated_audience_doc = audience_doc
    if name is not None:
        updated_audience_doc[db_c.AUDIENCE_NAME] = name
    if audience_filters is not None:
        updated_audience_doc[db_c.AUDIENCE_FILTERS] = audience_filters
    if destination_ids is not None:
        updated_audience_doc[db_c.DESTINATIONS] = destination_ids
    if user_name:
        updated_audience_doc[db_c.UPDATED_BY] = user_name
    updated_audience_doc[db_c.UPDATE_TIME] = curr_time

    try:
        return collection.find_one_and_update(
            {db_c.ID: audience_id},
            {"$set": updated_audience_doc},
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
def delete_audience(
    database: DatabaseClient,
    audience_id: ObjectId,
) -> bool:
    """A function to delete an audience.

    Args:
        database (DatabaseClient): A database client.
        audience_id (ObjectId): The Mongo DB ID of the audience.

    Returns:
        bool: A flag to indicate successful deletion.
    """

    collection = database[db_c.DATA_MANAGEMENT_DATABASE][db_c.AUDIENCES_COLLECTION]

    try:
        return collection.delete_one({db_c.ID: audience_id}).deleted_count > 0
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return False


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
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
        Union[list, None]:  A list of engagements with delivery information for
            an audience.
    """

    am_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    collection = am_db[db_c.ENGAGEMENTS_COLLECTION]

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
                    {"$project": {"delivery_platforms.update_time": 0}},
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
                            "deliveries.is_ad_platform": "$destinations.is_ad_platform",
                            "deliveries.status": {
                                "$ifNull": [
                                    "$deliveries.status",
                                    db_c.AUDIENCE_STATUS_NOT_DELIVERED,
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


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_all_audiences_and_deliveries(
    database: DatabaseClient,
    filters: dict = None,
    audience_ids: list = None,
) -> Union[list, None]:
    """A function to get all audiences and their latest deliveries.

    Args:
        database (DatabaseClient): A database client.
        filters (dict, Optional): A dict of filters to be applied on the
        audience.
        audience_ids (list, Optional): A list of audience ids.

    Returns:
        Union[list, None]:  A list of engagements with delivery information for
            an audience.
    """

    am_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    collection = am_db[db_c.AUDIENCES_COLLECTION]
    pipeline = [
        {
            "$lookup": {
                "from": "delivery_jobs",
                "localField": "_id",
                "foreignField": "audience_id",
                "as": "delivery_jobs",
            }
        },
        {
            "$unwind": {
                "path": "$delivery_jobs",
                "preserveNullAndEmptyArrays": True,
            }
        },
        {
            "$lookup": {
                "from": "delivery_platforms",
                "localField": "delivery_jobs.delivery_platform_id",
                "foreignField": "_id",
                "as": "delivery",
            }
        },
        {
            "$unwind": {
                "path": "$delivery",
                "preserveNullAndEmptyArrays": True,
            }
        },
        {
            "$addFields": {
                "delivery_jobs.delivery_platform_name" "": "$delivery.name",
                "delivery_jobs.delivery_platform_type"
                "": "$delivery.delivery_platform_type",
            }
        },
        {"$sort": {"_id": 1, "delivery_job.update_time": -1}},
        {
            "$group": {
                "_id": "$_id",
                "deliveries": {"$push": "$delivery_jobs"},
                "last_delivered": {"$last": "$delivery_jobs.update_time"},
            }
        },
        {"$project": {"deliveries.deleted": 0}},
    ]
    stage_count_in_pipeline = 0

    if audience_ids is not None:
        pipeline.insert(
            stage_count_in_pipeline,
            {"$match": {db_c.ID: {"$in": audience_ids}}},
        )
    stage_count_in_pipeline += 1

    if filters:
        if filters.get(db_c.WORKED_BY):
            pipeline.insert(
                stage_count_in_pipeline,
                {
                    "$match": {
                        "$or": [
                            {db_c.CREATED_BY: filters.get(db_c.WORKED_BY)},
                            {db_c.UPDATED_BY: filters.get(db_c.WORKED_BY)},
                        ]
                    }
                },
            )
            stage_count_in_pipeline += 1
        if filters.get(db_c.ATTRIBUTE):
            pipeline.insert(
                stage_count_in_pipeline,
                {
                    "$match": {
                        "$and": [
                            {db_c.ATTRIBUTE_FILTER_FIELD: attribute}
                            for attribute in filters.get(db_c.ATTRIBUTE)
                        ]
                    }
                },
            )

    # use the audience pipeline to aggregate and join all the delivery data
    try:
        return list(collection.aggregate(pipeline))

    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None
