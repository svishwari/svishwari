"""This module enables functionality related to engagement audience management.
"""
from datetime import datetime
import logging
from typing import Union

import pymongo
from bson import ObjectId
from tenacity import retry, wait_fixed, retry_if_exception_type

import huxunifylib.database.constants as db_c
from huxunifylib.database.client import DatabaseClient


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_all_engagement_audience_destinations(
    database: DatabaseClient, audience_ids: list = None
) -> Union[list, None]:
    """A function to get engagement audiences and their destinations
    across engagements.

    Args:
        database (DatabaseClient): A database client.
        audience_ids (list): List of audience ids.

    Returns:
        Union[list, None]:  A list of audiences with
            their unique destinations across engagements.
    """

    pipeline = [
        {"$match": {db_c.DELETED: False}},
        {"$unwind": {"path": "$audiences"}},
        {"$unwind": {"path": "$audiences.destinations"}},
        {
            "$addFields": {
                "data_added_destination": {
                    "destination_id": "$audiences.destinations.id",
                    "data_added": "$audiences.destinations.data_added",
                }
            }
        },
        {
            "$group": {
                "_id": "$audiences.id",
                "destinations": {"$addToSet": "$data_added_destination"},
            }
        },
        {"$unwind": {"path": "$destinations"}},
        {
            "$lookup": {
                "from": "delivery_platforms",
                "localField": "destinations.destination_id",
                "foreignField": "_id",
                "as": "delivery_platform",
            }
        },
        {"$unwind": {"path": "$delivery_platform"}},
        {"$addFields": {"delivery_platform.data_added": "$destinations.data_added"}},
        {
            "$group": {
                "_id": "$_id",
                "destinations": {"$push": "$delivery_platform"},
            }
        },
        {"$project": {"destinations.deleted": 0}},
    ]

    # check if audience filter was provided
    if audience_ids:
        # insert into the pipeline after the unwind of audience/destinations
        pipeline.insert(3, {"$match": {"audiences.id": {"$in": audience_ids}}})

    # use the audience pipeline to aggregate and get all unique
    # delivery platforms per audience.
    try:
        audience_delivery_platforms = list(
            database[db_c.DATA_MANAGEMENT_DATABASE][
                db_c.ENGAGEMENTS_COLLECTION
            ].aggregate(pipeline)
        )
        # Ensure no duplicates, since not using set while group by
        for audience in audience_delivery_platforms:
            encountered_destinations = {}
            for i, destination in enumerate(audience[db_c.DESTINATIONS]):
                if encountered_destinations.get(str(destination.get(db_c.ID, ""))):
                    audience[db_c.DESTINATIONS].pop(i)
                encountered_destinations[str(destination.get(db_c.ID))] = True

        return audience_delivery_platforms

    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def set_engagement_audience_destination_schedule(
    database: DatabaseClient,
    engagement_id: ObjectId,
    audience_id: ObjectId,
    destination_id: ObjectId,
    cron_expression: str,
    user_name: str,
    unset: bool = False,
) -> dict:
    """A function to set the destination cron expression.

    Args:
        database (DatabaseClient): A database client.
        engagement_id (ObjectId): MongoDB ID of the engagement.
        audience_id (ObjectId): MongoDB ID of the audience.
        destination_id (ObjectId): MongoDB ID of the destination.
        cron_expression (str): CRON expression of the delivery schedule.
        user_name (str): Name of the user updating the engagement.
        unset (bool): Option to remove the cron expression object.
    Returns:
        list: updated engagement objects
    """

    collection = database[db_c.DATA_MANAGEMENT_DATABASE][db_c.ENGAGEMENTS_COLLECTION]

    # get the engagement doc
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

        for destination in audience.get(db_c.DESTINATIONS, []):
            if destination.get(db_c.OBJECT_ID) != destination_id:
                continue

            if unset:
                destination.pop(db_c.ENGAGEMENT_DELIVERY_SCHEDULE, None)
            else:
                # set the cron expression
                destination[db_c.ENGAGEMENT_DELIVERY_SCHEDULE] = cron_expression

            engagement_doc[db_c.UPDATE_TIME] = datetime.utcnow()
            engagement_doc[db_c.UPDATED_BY] = user_name
            change = True

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
def get_all_engagement_audience_deliveries(
    database: DatabaseClient,
    audience_ids: list = None,
) -> Union[list, None]:
    """A function to get delivery jobs for all engagements and corresponding
    audiences nested within.

    Args:
        database (DatabaseClient): A database client.
        audience_ids (list, Optional): A list of audience ids.

    Returns:
        Union[list, None]:  A list of delivery job ids.
    """

    # pipeline to aggregate and fetch the delivery jobs from delivery_jobs
    # using engagement_id and audience_id from engagements
    pipeline = [
        {"$unwind": {"path": "$audiences", "preserveNullAndEmptyArrays": False}},
        {"$addFields": {"audience_id": "$audiences.id"}},
        {"$project": {"audience_id": 1}},
        {"$group": {"_id": {"_id": "$_id", "audience_id": "$audience_id"}}},
        {
            "$addFields": {
                "engagement_id": "$_id._id",
                "audience_id": "$_id.audience_id",
            }
        },
        {"$project": {"_id": 0, "engagement_id": 1, "audience_id": 1}},
        {
            "$lookup": {
                "from": "delivery_jobs",
                "localField": "engagement_id",
                "foreignField": "engagement_id",
                "as": "delivery_jobs",
            }
        },
        {"$unwind": {"path": "$delivery_jobs", "preserveNullAndEmptyArrays": False}},
        {
            "$redact": {
                "$cond": [
                    {"$eq": ["$audience_id", "$delivery_jobs.audience_id"]},
                    "$$KEEP",
                    "$$PRUNE",
                ]
            }
        },
        {"$project": {"audience_id": 1, "delivery_jobs": 1}},
        {
            "$lookup": {
                "from": "delivery_platforms",
                "localField": "delivery_jobs.delivery_platform_id",
                "foreignField": "_id",
                "as": "delivery_platform",
            }
        },
        {
            "$unwind": {
                "path": "$delivery_platform",
                "preserveNullAndEmptyArrays": False,
            }
        },
        {
            "$addFields": {
                "delivery_jobs.delivery_platform_name": "$delivery_platform.name",
                "delivery_jobs.delivery_platform_type": "$delivery_platform.delivery_platform_type",
            }
        },
        {"$project": {"audience_id": 1, "delivery_jobs": 1}},
        {"$sort": {"audience_id": 1, "delivery_jobs.update_time": -1}},
        {
            "$group": {
                "_id": "$audience_id",
                "deliveries": {"$push": "$delivery_jobs"},
                "last_delivered": {"$first": "$delivery_jobs.update_time"},
            }
        },
        {"$addFields": {"audience_id": "$_id"}},
        {
            "$project": {
                "_id": 0,
                "audience_id": 1,
                "deliveries": 1,
                "last_delivered": 1,
            }
        },
        {"$project": {"deliveries.deleted": 0}},
    ]

    stage_count_in_pipeline = 19
    if audience_ids is not None:
        pipeline.insert(
            stage_count_in_pipeline,
            {"$match": {db_c.AUDIENCE_ID: {"$in": audience_ids}}},
        )
        stage_count_in_pipeline += 1

    # use the engagement pipeline to aggregate and get all unique delivery jobs
    # per nested audience
    try:
        engagement_audience_deliveries = list(
            database[db_c.DATA_MANAGEMENT_DATABASE][
                db_c.ENGAGEMENTS_COLLECTION
            ].aggregate(pipeline)
        )

        return engagement_audience_deliveries

    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None
