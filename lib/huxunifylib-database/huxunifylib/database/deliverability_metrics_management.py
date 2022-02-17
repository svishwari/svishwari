"""This module enables functionality related to deliverability metrics
management."""
import logging
from datetime import datetime
from typing import Union

import pymongo
from pymongo import MongoClient

import huxunifylib.database.constants as db_c


def get_domain_wise_inbox_percentage_data(
    database: MongoClient,
    domain_name: list = None,
    start_date: datetime = None,
    end_date: datetime = None,
) -> Union[list, None]:
    """Fetch Domain wise inbox percentage data from DB.

    Args:
        database (MongoClient): A database client.
        domain_name (list): A list of domain names.
        start_date (datetime, Optional): Start date to get email deliverability
            metrics.
        end_date (datetime, Optional): End date to get email deliverability
            metrics.
    Returns:
        Union[list, None]: list of domains and their respective inbox
            percentage metrics.

    """
    pipeline = [
        {
            # To ensure only data with correct format is fetched
            "$match": {
                "deliverability_metrics.domain_inbox_percentage": {
                    "$type": "double"
                }
            }
        },
        {"$sort": {"create_time": -1}},
        {
            "$group": {
                "_id": "$domain",
                "inbox_percentage_data": {
                    "$addToSet": {
                        "create_time": "$create_time",
                        "inbox_percentage": "$deliverability_metrics.domain_inbox_percentage",
                    }
                },
            }
        },
        {
            "$project": {
                "_id": 0,
                "domain_name": "$_id",
                "inbox_percentage_data": "$inbox_percentage_data",
            }
        },
    ]

    if domain_name and isinstance(domain_name, list):
        pipeline[0]["$match"][db_c.DOMAIN] = {"$in": domain_name}

    # Optionally filter by date.
    if isinstance(start_date, datetime) and isinstance(end_date, datetime):
        pipeline.insert(
            1,
            {
                "$match": {
                    "create_time": {"$gte": start_date, "$lte": end_date}
                }
            },
        )

    elif isinstance(start_date, datetime):
        pipeline.insert(1, {"$match": {"create_time": {"$gte": start_date}}})

    elif isinstance(end_date, datetime):
        pipeline.insert(1, {"$match": {"create_time": {"$lte": end_date}}})

    try:
        inbox_percentage_data_no_repeat = []
        inbox_percentage_data = list(
            database[db_c.DATA_MANAGEMENT_DATABASE][
                db_c.DELIVERABILITY_METRICS_COLLECTION
            ].aggregate(pipeline)
        )

        for domain in inbox_percentage_data:
            daily_unique_data = {}
            for daily_data in domain.get(db_c.INBOX_PERCENTAGE_DATA):
                daily_unique_data[
                    daily_data.get(db_c.CREATE_TIME).date()
                ] = daily_data.get(db_c.INBOX_PERCENTAGE)

            inbox_percentage_data_no_repeat.append(
                {
                    db_c.DOMAIN_NAME: domain.get(db_c.DOMAIN_NAME),
                    db_c.INBOX_PERCENTAGE_DATA: [
                        {
                            db_c.CREATE_TIME: create_time,
                            db_c.INBOX_PERCENTAGE: inbox_percentage,
                        }
                        for create_time, inbox_percentage in daily_unique_data.items()
                    ],
                }
            )
        return inbox_percentage_data_no_repeat
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


def get_overall_inbox_rate(database: MongoClient) -> Union[float, None]:
    """Get overall inbox rate.
    Args:
        database (MongoClient): A database client.
    Returns:
        Union[float, None]: Overall inbox rate.
    """
    pipeline = [
        {
            "$match": {
                "deliverability_metrics.domain_inbox_percentage": {
                    "$type": "double"
                }
            }
        },
        {
            "$group": {
                "_id": None,
                "overall_inbox_rate": {
                    "$avg": "$deliverability_metrics.domain_inbox_percentage"
                },
            }
        },
        {"$project": {"overall_inbox_rate": "$overall_inbox_rate", "_id": 0}},
    ]
    try:
        return list(
            database[db_c.DATA_MANAGEMENT_DATABASE][
                db_c.DELIVERABILITY_METRICS_COLLECTION
            ].aggregate(pipeline)
        )[0].get(db_c.OVERALL_INBOX_RATE)

    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None
