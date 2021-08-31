"""
This module enables functionality related to engagement audience management.
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
    """A function to get engagement audiences and their destinations across engagements.

    Args:
        database (DatabaseClient): A database client.
        audience_ids (list): List of audience ids.

    Returns:
        Union[list, None]:  A list of engagements with delivery
            information for an audience
    """

    # check if any audience ids
    match_statement = {db_c.DELETED: False}
    if audience_ids:
        match_statement[db_c.ID] = {"$in": audience_ids}

    # use the audience pipeline to aggregate and get all unique
    # delivery platforms per audience.
    try:
        return list(
            database[db_c.DATA_MANAGEMENT_DATABASE][
                db_c.ENGAGEMENTS_COLLECTION
            ].aggregate(
                [
                    {"$match": match_statement},
                    {"$unwind": {"path": "$audiences"}},
                    {"$unwind": {"path": "$audiences.destinations"}},
                    {
                        "$group": {
                            "_id": "$audiences.id",
                            "destinations": {
                                "$addToSet": "$audiences.destinations.id"
                            },
                        }
                    },
                    {"$unwind": {"path": "$destinations"}},
                    {
                        "$lookup": {
                            "from": "delivery_platforms",
                            "localField": "destinations",
                            "foreignField": "_id",
                            "as": "delivery_platform",
                        }
                    },
                    {"$unwind": {"path": "$delivery_platform"}},
                    {
                        "$group": {
                            "_id": "$_id",
                            "destinations": {"$push": "$delivery_platform"},
                        }
                    },
                    {"$project": {"destinations.deleted": 0}},
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
def set_engagement_audience_destination_schedule(
    database: DatabaseClient,
    engagement_id: ObjectId,
    audience_id: ObjectId,
    destination_id: ObjectId,
    cron_expression: str,
    user_name: str,
) -> dict:
    """A function to set the destination cron expression.

    Args:
        database (DatabaseClient): A database client.
        engagement_id (ObjectId): MongoDB ID of the engagement.
        audience_id (ObjectId): MongoDB ID of the audience.
        destination_id (ObjectId): MongoDB ID of the destination.
        cron_expression (str): CRON expression of the delivery schedule.
        user_name (str): Name of the user updating the engagement.

    Returns:
        dict: updated engagement object

    """

    return database[db_c.DATA_MANAGEMENT_DATABASE][
        db_c.ENGAGEMENTS_COLLECTION
    ].find_one_and_update(
        {
            db_c.ID: engagement_id,
            "audiences.id": audience_id,
            "audiences.destinations.id": destination_id,
        },
        {
            "$set": {
                db_c.UPDATE_TIME: datetime.utcnow(),
                db_c.UPDATED_BY: user_name,
                f"audiences.$.destinations.$.{db_c.ENGAGEMENT_DELIVERY_SCHEDULE}": cron_expression,
            },
        },
    )


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def remove_engagement_audience_destination_schedule(
    database: DatabaseClient,
    engagement_id: ObjectId,
    audience_id: ObjectId,
    destination_id: ObjectId,
    user_name: str,
) -> dict:
    """A function to remove the destination cron expression.

    Args:
        database (DatabaseClient): A database client.
        engagement_id (ObjectId): MongoDB ID of the engagement.
        audience_id (ObjectId): MongoDB ID of the audience.
        destination_id (ObjectId): MongoDB ID of the destination.
        user_name (str): Name of the user updating the engagement.

    Returns:
        dict: updated engagement object

    """

    return database[db_c.DATA_MANAGEMENT_DATABASE][
        db_c.ENGAGEMENTS_COLLECTION
    ].find_one_and_update(
        {
            db_c.ID: engagement_id,
            "audiences.id": audience_id,
            "audiences.destinations.id": destination_id,
        },
        {
            "$set": {
                db_c.UPDATE_TIME: datetime.utcnow(),
                db_c.UPDATED_BY: user_name,
            },
            "$unset": {
                f"audiences.$.destinations.$.{db_c.ENGAGEMENT_DELIVERY_SCHEDULE}": 1
            },
        },
    )
