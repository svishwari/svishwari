"""This module enables functionality related to engagement audience management.
"""
from datetime import datetime
import logging
from typing import Union, Dict, Any

import pymongo
from bson import ObjectId
from tenacity import retry, wait_fixed, retry_if_exception_type

import huxunifylib.database.constants as db_c
from huxunifylib.database.client import DatabaseClient
from huxunifylib.database.delivery_platform_management import (
    get_all_delivery_platforms,
)


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
        {
            "$addFields": {
                "delivery_platform.data_added": "$destinations.data_added"
            }
        },
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
                if encountered_destinations.get(
                    str(destination.get(db_c.ID, ""))
                ):
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

    collection = database[db_c.DATA_MANAGEMENT_DATABASE][
        db_c.ENGAGEMENTS_COLLECTION
    ]

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
                destination[
                    db_c.ENGAGEMENT_DELIVERY_SCHEDULE
                ] = cron_expression

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


def set_replace_audience_flag(
    database: DatabaseClient,
    engagement_id: ObjectId,
    audience_id: ObjectId,
    destination_id: ObjectId,
    replace_audience: bool,
    user_name: str,
) -> dict:
    """Method for toggling replace_audience flag

    Args:
        database(DatabaseClient): A database client
        engagement_id(ObjectId):  MongoDB ID of the engagement.
        audience_id(ObjectId): MongoDB ID of the audience.
        destination_id(ObjectId): MongoDB ID of the destination.
        replace_audience(bool): Audience replacement flag.
        user_name(str): User name

    Returns:
        dict: Updated Engagement object
    """
    collection = database[db_c.DATA_MANAGEMENT_DATABASE][
        db_c.ENGAGEMENTS_COLLECTION
    ]

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

            destination[db_c.REPLACE_AUDIENCE] = replace_audience

        engagement_doc.update(
            {db_c.UPDATE_TIME: datetime.now(), db_c.UPDATED_BY: user_name}
        )
        change = True

    # no changes, simply return.
    if not change:
        return {}

    return collection.update(
        {
            db_c.ID: engagement_id,
        },
        {"$set": engagement_doc},
        upsert=True,
    )


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def set_engagement_audience_schedule(
    database: DatabaseClient,
    engagement_id: ObjectId,
    audience_id: ObjectId,
    delivery_schedule: dict,
    user_name: str,
    unset: bool = False,
) -> Union[dict, None]:
    """A function to set the engagement audience delivery schedule.

    Args:
        database (DatabaseClient): A database client.
        engagement_id (ObjectId): MongoDB ID of the engagement.
        audience_id (ObjectId): MongoDB ID of the audience.
        delivery_schedule (dict): Dict object containing delivery_schedule.
        user_name (str): Name of the user updating the engagement.
        unset (bool): Option to remove the delivery schedule object.

    Returns:
        dict: Updated engagement object.
    """

    collection = database[db_c.DATA_MANAGEMENT_DATABASE][
        db_c.ENGAGEMENTS_COLLECTION
    ]

    # get the engagement doc
    engagement_doc = collection.find_one(
        {
            db_c.ID: engagement_id,
            "audiences.id": audience_id,
        }
    )

    if not engagement_doc:
        return None

    # workaround cause DocumentDB does not support nested DB updates
    for audience in engagement_doc.get(db_c.AUDIENCES, []):
        if audience.get(db_c.OBJECT_ID) != audience_id:
            continue

        if unset:
            audience.pop(db_c.ENGAGEMENT_DELIVERY_SCHEDULE, None)
        else:
            # set the delivery schedule
            audience[db_c.ENGAGEMENT_DELIVERY_SCHEDULE] = delivery_schedule

        engagement_doc[db_c.UPDATE_TIME] = datetime.utcnow()
        engagement_doc[db_c.UPDATED_BY] = user_name
        # break out of the loop as soon as the single audience is found
        # to be updated.
        break
    # no changes, simply return empty dict
    else:
        return {}

    # replace one
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
def get_all_audience_engagement_id_pairs(
    database: DatabaseClient,
    audience_ids: list = None,
) -> Union[list, None]:
    """A function to get all audience and engagement pairs.

    Args:
        database (DatabaseClient): A database client.
        audience_ids (list, Optional): A list of audience ids.

    Returns:
        Union[list, None]:  A list of audience/engagement ids.
    """

    pipeline = [
        {
            "$unwind": {
                "path": "$audiences",
                "preserveNullAndEmptyArrays": False,
            }
        },
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
    ]

    if audience_ids is not None:
        pipeline.append(
            {"$match": {db_c.AUDIENCE_ID: {"$in": audience_ids}}},
        )

    # use the engagement pipeline to aggregate and get all unique delivery jobs
    # per nested audience
    try:
        engagement_audience_pairs = list(
            database[db_c.DATA_MANAGEMENT_DATABASE][
                db_c.ENGAGEMENTS_COLLECTION
            ].aggregate(pipeline)
        )

        return engagement_audience_pairs

    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


def align_audience_engagement_deliveries(
    database, audience_delivery_jobs: list, audience_ids: list
) -> dict:
    """A function to align and match audience deliveries.

    Args:
        database (DatabaseClient): A database client.
        audience_delivery_jobs (list): A list of audience delivery jobs.
        audience_ids (list): A list of audience ids.

    Returns:
        dict:  A dict of audiences and the nested delivery history.
    """

    # get all delivery platforms and convert to dict
    delivery_platform_dict = {
        x[db_c.ID]: x for x in get_all_delivery_platforms(database)
    }

    # process each audience delivery job
    matched_delivery_jobs = []
    for delivery_job in audience_delivery_jobs:
        # match the delivery platform, otherwise set to unknown.
        matched_delivery_platform = delivery_platform_dict.get(
            delivery_job[db_c.DELIVERY_PLATFORM_ID],
            {
                db_c.DELIVERY_PLATFORM_TYPE: db_c.CATEGORY_UNKNOWN,
                db_c.DELIVERY_PLATFORM_NAME: db_c.CATEGORY_UNKNOWN,
            },
        )

        # update the delivery job params per the matched platform.
        matched_delivery_jobs.append(
            {
                **delivery_job,
                db_c.DELIVERY_PLATFORM_TYPE: matched_delivery_platform[
                    db_c.DELIVERY_PLATFORM_TYPE
                ],
                db_c.METRICS_DELIVERY_PLATFORM_NAME: matched_delivery_platform[
                    db_c.DELIVERY_PLATFORM_NAME
                ],
            }
        )

    # set the stage for grouping each audience
    # set the nested deliveries list and last delivered.
    audience_grouped_jobs = {}
    for audience_id in audience_ids:

        # set the base dict.
        delivery_dict = {
            db_c.AUDIENCE_LAST_DELIVERED: None,
            db_c.DELIVERIES: [],
        }

        # match each job, use last iterated index due to sort.
        for delivery_job in matched_delivery_jobs:

            # ensure audience and engagement ID match.
            if delivery_job.get(db_c.AUDIENCE_ID) != audience_id:
                continue

            # if first index, assume the most recent time.
            if not delivery_dict[db_c.DELIVERIES]:
                delivery_dict[db_c.AUDIENCE_LAST_DELIVERED] = delivery_job[
                    db_c.UPDATE_TIME
                ]

            # append the delivery jbo to the list of deliveries for the audience.
            delivery_dict[db_c.DELIVERIES].append(delivery_job)

        # only append if the audience has any deliveries.
        if delivery_dict[db_c.DELIVERIES]:
            audience_grouped_jobs[audience_id] = delivery_dict

    # return the dict of audience grouped jobs.
    return audience_grouped_jobs


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_all_audience_engagement_latest_deliveries(
    database: DatabaseClient,
    audience_engagement_ids: list = None,
) -> Union[list, None]:
    """A function to get all audience and engagement pairs.

    Args:
        database (DatabaseClient): A database client.
        audience_engagement_ids (list, Optional): A list of
            audience/engagements ids.

    Returns:
        Union[list, None]:  A list of delivery job ids.
    """

    # filter on deliver job status
    # filter on engagement_audience_match
    # 10 most recent jobs for the combination
    # get all engagements that match the audiences.

    # Handle case when audience_engagement_ids are not passed
    if not audience_engagement_ids:
        return []

    pipeline = [
        {
            "$match": {
                "$or": [
                    {
                        "audience_id": x["audience_id"],
                        "engagement_id": x["engagement_id"],
                    }
                    for x in audience_engagement_ids
                ],
            },
        },
        {"$sort": {"audience_id": 1, "engagement_id": 1, "update_time": -1}},
    ]

    # use the engagement pipeline to aggregate and get all unique delivery jobs
    # per nested audience
    try:
        return list(
            database[db_c.DATA_MANAGEMENT_DATABASE][
                db_c.DELIVERY_JOBS_COLLECTION
            ].aggregate(pipeline)
        )

    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


def get_all_engagement_audience_deliveries(
    database: DatabaseClient,
    audience_ids: list = None,
) -> Dict[Any, Any]:
    """A function to get delivery jobs for all engagements and corresponding
    audiences nested within. This function is really just a work around
    cause DocumentDB does not support inline pipeline functions.

    Args:
        database (DatabaseClient): A database client.
        audience_ids (list, Optional): A list of audience ids.

    Returns:
        Dict[Any, Any]:  A dict of audiences and the nested delivery history.
    """

    # get the audience engagement pairs
    audience_engagement_pairs = get_all_audience_engagement_id_pairs(
        database, audience_ids
    )

    # get recent deliveries for each engagement pair.
    recent_deliveries = get_all_audience_engagement_latest_deliveries(
        database, audience_engagement_pairs
    )

    # align the audience engagement deliveries
    return align_audience_engagement_deliveries(
        database, recent_deliveries, audience_ids
    )
