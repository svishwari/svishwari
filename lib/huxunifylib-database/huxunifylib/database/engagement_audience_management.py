"""
This module enables functionality related to engagement audience management.
"""

import logging
from typing import Union

import pymongo
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
