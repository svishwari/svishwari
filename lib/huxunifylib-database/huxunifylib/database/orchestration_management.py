# pylint: disable=too-many-lines
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
from huxunifylib.database.utils import get_collection_count


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def create_audience(
    database: DatabaseClient,
    name: str,
    audience_filters: list,
    user_name: str,
    destination_ids: list = None,
    size: int = 0,
    audience_tags: Union[dict, None] = None,
) -> Union[dict, None]:
    """A function to create an audience.

    Args:
        database (DatabaseClient): A database client.
        name (str): Name of the audience.
        audience_filters (list of list): Multiple sections of audience filters.
            These are aggregated using "OR".
        user_name (str): Name of the user creating / updating the audience.
        destination_ids (list): List of destination/delivery platform ids
            attached to the audience.
        size (int): audience size.
        audience_tags (dict): A dict of different type of tags that the
            audience can be tagged with.

    Returns:
        Union[list, None]: MongoDB audience doc.

    Raises:
        DuplicateName: Error if an audience with the same name exists
            already.
        TypeError: Error if user_name is not a string.
    """
    if not isinstance(user_name, str):
        raise TypeError("user_name must be a string")
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

    if audience_tags is not None:
        audience_doc[db_c.TAGS] = audience_tags

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

    collection = database[db_c.DATA_MANAGEMENT_DATABASE][
        db_c.AUDIENCES_COLLECTION
    ]

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

        return list(cursor.limit(limit) if limit else cursor)
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
                        {
                            "$match": {
                                db_c.ID: audience_id,
                                db_c.DELETED: False,
                            }
                        },
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
    batch_size: int = 0,
    batch_number: int = 1,
) -> Union[list, None]:
    """A function to get all existing audiences.

    Args:
        database (DatabaseClient): A database client.
        include_users (bool): Flag to include users.
        filters (dict, Optional): A dict of filters to be applied on the
            audience.
        audience_ids (list, Optional): A list of audience IDs.
        batch_size (int): Number of audiences per batch.
        batch_number (int): Number of audiences batch to be returned.

    Returns:
        Union[list, None]: A list of all audiences.
    """

    am_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    collection = am_db[db_c.AUDIENCES_COLLECTION]

    find_filters = build_get_audiences_query_filter(filters, audience_ids)

    skips = batch_size * (batch_number - 1)

    # Get audience configurations and add to list
    try:
        if include_users:
            batch_offset_pipeline = []
            if skips > 0:
                batch_offset_pipeline.append({"$skip": skips})
            if batch_size > 0:
                batch_offset_pipeline.append({"$limit": batch_size})

            # lookup to users
            return list(
                collection.aggregate(
                    [{"$match": {db_c.DELETED: False}}]
                    + USER_LOOKUP_PIPELINE
                    + batch_offset_pipeline
                )
            )

        return list(
            collection.find(find_filters).skip(skips).limit(batch_size)
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


def build_get_audiences_query_filter(
    filters: dict = None, audience_ids: list = None
) -> dict:
    """A function to retrieve count of audiences documents.

    Args:
        filters (dict, Optional): A dict of filters to be applied on the
            audience.
        audience_ids (list, Optional): A list of audience IDs.

    Returns:
        dict: Query filter dict.
    """

    if not filters:
        query_filter = {db_c.DELETED: False}
    else:
        query_filter = {"$and": [{db_c.DELETED: False}]}

        if filters.get(db_c.WORKED_BY):
            query_filter["$and"].extend(
                [
                    {
                        "$or": [
                            {db_c.CREATED_BY: filters.get(db_c.WORKED_BY)},
                            {db_c.UPDATED_BY: filters.get(db_c.WORKED_BY)},
                        ]
                    }
                ]
            )

        if filters.get(db_c.ATTRIBUTE):
            query_filter["$and"].extend(
                [
                    {
                        "$and": [
                            {
                                db_c.ATTRIBUTE_FILTER_FIELD: {
                                    "$regex": rf"^{attribute}$",
                                    "$options": "i",
                                }
                            }
                            for attribute in filters.get(db_c.ATTRIBUTE)
                        ]
                    }
                ]
            )
        if filters.get(db_c.EVENT):
            query_filter["$and"].extend(
                [
                    {
                        "$and": [
                            {
                                db_c.EVENTS_FILTER_FIELD: {
                                    "$regex": rf"^{event_name}$",
                                    "$options": "i",
                                }
                            }
                            for event_name in filters.get(db_c.EVENT)
                        ]
                    }
                ]
            )
        if filters.get(db_c.INDUSTRY_TAG):
            query_filter["$and"].extend(
                [
                    {
                        "$or": [
                            {
                                db_c.INDUSTRY_TAG_FIELD: {
                                    "$regex": rf"^{industry_tag}$",
                                    "$options": "i",
                                }
                            }
                            for industry_tag in filters.get(db_c.INDUSTRY_TAG)
                        ]
                    }
                ]
            )

    if audience_ids is not None:
        query_filter[db_c.ID] = {"$in": audience_ids}

    return query_filter


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def update_audience(
    database: DatabaseClient,
    audience_id: ObjectId,
    user_name: str,
    name: str = None,
    audience_filters: list = None,
    destination_ids: list = None,
    audience_tags: Union[dict, None] = None,
) -> Union[dict, None]:
    """A function to update an audience.

    Args:
        database (DatabaseClient): A database client.
        audience_id (ObjectId): MongoDB ID of the audience.
        user_name (str): Name of the user creating/updating the audience.
        name (str): New audience name.
        audience_filters (list of list): Multiple sections of audience filters.
            These are aggregated using "OR".
        destination_ids (list): List of destination/delivery platform
            ids attached to the audience.
        audience_tags (dict): A dict of different type of tags that the
            audience can be tagged with.

    Returns:
        Union[dict, None]: Updated audience configuration dict.

    Raises:
        InvalidID: If the passed in audience_id did not fetch a doc from the
            relevant db collection.
        DuplicateName: Error if an audience with the same name exists already.
        TypeError: Error if user_name is not a string.
    """

    if not isinstance(user_name, str):
        raise TypeError("user_name must be a string")
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
                {db_c.AUDIENCE_NAME: name, db_c.DELETED: False},
                {db_c.DELETED: 0},
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
    if audience_tags is not None:
        updated_audience_doc[db_c.TAGS] = audience_tags
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
def update_lookalike_audience(
    database: DatabaseClient,
    audience_id: ObjectId,
    name: str = None,
    user_name: str = None,
    audience_tags: Union[dict, None] = None,
) -> Union[dict, None]:
    """A function to update an audience.

    Args:
        database (DatabaseClient): A database client.
        audience_id (ObjectId): MongoDB ID of the audience.
        name (str): New audience name.
        user_name (str): Name of the user creating/updating the audience.
        audience_tags (dict): A dict of different type of tags that the
            audience can be tagged with.

    Returns:
        Union[dict, None]: Updated audience configuration dict.

    Raises:
        InvalidID: If the passed in audience_id did not fetch a doc from the
            relevant db collection.
        DuplicateName: Error if an audience with the same name exists already.
    """

    collection = database[db_c.DATA_MANAGEMENT_DATABASE][
        db_c.LOOKALIKE_AUDIENCE_COLLECTION
    ]

    try:
        audience_doc = collection.find_one(
            {db_c.ID: audience_id, db_c.DELETED: False}, {db_c.DELETED: 0}
        )
        if not audience_doc:
            raise de.InvalidID()
        if name is not None:
            duplicate_name_doc = collection.find_one(
                {db_c.AUDIENCE_NAME: name, db_c.DELETED: False},
                {db_c.DELETED: 0},
            )
            if (
                duplicate_name_doc is not None
                and duplicate_name_doc[db_c.ID] != audience_id
            ):
                raise de.DuplicateName(name)
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    updated_audience_doc = audience_doc
    if name is not None:
        updated_audience_doc[db_c.AUDIENCE_NAME] = name
    if audience_tags is not None:
        updated_audience_doc[db_c.TAGS] = audience_tags
    if user_name:
        updated_audience_doc[db_c.UPDATED_BY] = user_name
    updated_audience_doc[db_c.UPDATE_TIME] = datetime.datetime.utcnow()

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

    collection = database[db_c.DATA_MANAGEMENT_DATABASE][
        db_c.AUDIENCES_COLLECTION
    ]

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
    platform: str = db_c.AWS_DOCUMENT_DB,
) -> Union[list, None]:
    """A function to get audience insights.

    Args:
        database (DatabaseClient): A database client.
        audience_id (ObjectId): The Mongo DB ID of the audience.
        platform (str): Underlying DB of the Mongo DB API.
    Returns:
        Union[list, None]:  A list of engagements with delivery information for
            an audience.
    """

    am_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    collection = am_db[db_c.ENGAGEMENTS_COLLECTION]

    pipeline = [
        {
            "$match": {
                "audiences.id": audience_id,
                db_c.DELETED: False,
            }
        },
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
                "last_delivered": {"$last": "$deliveries.update_time"},
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
    if platform == db_c.AZURE_COSMOS_DB:
        pipeline[10] = {
            "$addFields": {
                "deliveries.delivery_platform_id": {
                    "$ifNull": ["$delivery_platforms._id", None]
                }
            }
        }

        pipeline.append(
            {
                "$addFields": {
                    "first_delivery": {"$arrayElemAt": ["$deliveries", 0]}
                }
            }
        )

        pipeline.append(
            {
                "$project": {
                    "deliveries": {
                        "$cond": {
                            "if": {
                                "$eq": [
                                    "$first_delivery.delivery_platform_id",
                                    None,
                                ]
                            },
                            "then": {},
                            "else": "$deliveries",
                        }
                    },
                    "engagement": 1,
                    "last_delivered": 1,
                }
            }
        )

    # use the audience pipeline to aggregate and join all the insight data
    try:
        return list(collection.aggregate(pipeline))

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
                            {
                                db_c.ATTRIBUTE_FILTER_FIELD: {
                                    "$regex": rf"^{attribute}$",
                                    "$options": "i",
                                }
                            }
                            for attribute in filters.get(db_c.ATTRIBUTE)
                        ]
                    }
                },
            )
            stage_count_in_pipeline += 1

    # use the audience pipeline to aggregate and join all the delivery data
    try:
        return list(collection.aggregate(pipeline))

    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


def get_audiences_count(
    database: DatabaseClient, filters: dict = None, audience_ids: list = None
) -> int:
    """A function to retrieve count of audiences documents.

    Args:
        database (DatabaseClient): A database client.
        filters (Union[dict[Tuple], None]): Mongo filter query.
        audience_ids (list, Optional): A list of audience IDs.

    Returns:
        int: Count of audiences documents.
    """

    return get_collection_count(
        database,
        db_c.DATA_MANAGEMENT_DATABASE,
        db_c.AUDIENCES_COLLECTION,
        build_get_audiences_query_filter(
            filters=filters, audience_ids=audience_ids
        ),
    )


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def remove_destination_from_all_audiences(
    database: DatabaseClient, destination_id: ObjectId, user_name: str
) -> bool:
    """Remove a destination from all audience documents.

    Args:
        database (DatabaseClient): A database client.
        destination_id (ObjectId): MongoDB ID of the destination.
        user_name (str): Name of the user removing the destination from the
            audience.

    Returns:
        bool: Boolean flag indicating if the destination has been removed from
            all audiences.
    """

    collection = database[db_c.DATA_MANAGEMENT_DATABASE][
        db_c.AUDIENCES_COLLECTION
    ]

    try:
        collection.update_many(
            filter={f"{db_c.DESTINATIONS}.{db_c.OBJECT_ID}": destination_id},
            update={
                "$pull": {
                    f"{db_c.DESTINATIONS}": {
                        db_c.OBJECT_ID: {"$in": [destination_id]}
                    }
                },
                "$set": {
                    db_c.UPDATE_TIME: datetime.datetime.utcnow(),
                    db_c.UPDATED_BY: user_name,
                },
            },
        )

        return True
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return False


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def append_destination_to_standalone_audience(
    database: DatabaseClient,
    audience_id: ObjectId,
    destination: dict,
    user_name: str,
) -> dict:
    """A function to append destination to standalone audience.

    Args:
        database (DatabaseClient): A database client.
        audience_id (ObjectId): MongoDB ID of the audience.
        destination (dict): Destination to add to engagement audience.
        user_name (str): Name of the user appending the destination to the
            audience.

    Returns:
        dict: updated audience object.
    Raises:
        TypeError: Error user name is not a string.
    """
    if not isinstance(user_name, str):
        raise TypeError("user_name must be a string")

    collection = database[db_c.DATA_MANAGEMENT_DATABASE][
        db_c.AUDIENCES_COLLECTION
    ]

    try:
        audience = collection.find_one_and_update(
            {
                db_c.ID: audience_id,
            },
            {
                "$push": {"destinations": destination},
                "$set": {
                    db_c.UPDATE_TIME: datetime.datetime.utcnow(),
                    db_c.UPDATED_BY: user_name,
                },
            },
            return_document=pymongo.ReturnDocument.AFTER,
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return audience


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def remove_destination_from_audience(
    database: DatabaseClient,
    audience_id: ObjectId,
    destination_id: ObjectId,
    user_name: str,
) -> dict:
    """A function to remove destination from audience.

    Args:
        database (DatabaseClient): A database client.
        audience_id (ObjectId): MongoDB ID of the audience.
        destination_id (ObjectId): MongoDB ID of the destination to be removed.
        user_name (str): Name of the user removing the destination from the
            audience.

    Returns:
        dict: updated audience object.

    Raises:
        TypeError: Error user name is not a string.
    """

    if not isinstance(user_name, str):
        raise TypeError("user_name must be a string")

    collection = database[db_c.DATA_MANAGEMENT_DATABASE][
        db_c.AUDIENCES_COLLECTION
    ]
    try:
        audience = collection.find_one_and_update(
            {
                db_c.ID: audience_id,
            },
            {
                "$pull": {"destinations": {db_c.OBJECT_ID: destination_id}},
                "$set": {
                    db_c.UPDATE_TIME: datetime.datetime.utcnow(),
                    db_c.UPDATED_BY: user_name,
                },
            },
            return_document=pymongo.ReturnDocument.AFTER,
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return audience
