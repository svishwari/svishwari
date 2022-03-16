"""This module enables functionality related to deliverability metrics
management."""
import logging
from datetime import datetime
from typing import Union

import pymongo
from pymongo import MongoClient

import huxunifylib.database.constants as db_c
from huxunifylib.database.utils import match_start_end_date_stmt


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
    start_end_filter = match_start_end_date_stmt(
        start_date=start_date, end_date=end_date, date_field=db_c.CREATE_TIME
    )
    if start_end_filter:
        pipeline.insert(1, start_end_filter)

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
                        for create_time, inbox_percentage in
                        daily_unique_data.items()
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


def get_deliverability_data_performance_metrics(
        database: MongoClient,
        domains: list = None,
        delivery_platforms=None,
        start_date: datetime = None,
        end_date: datetime = None,
        aggregate: bool = False,
        mock: bool = False,
) -> Union[list, None]:
    """Retrieves deliverability metrics data from performance metrics
    collection.

    Args:
        database (MongoClient): A database client.
        domains (list, Optional): List of domain names to be filtered.
        delivery_platforms (list, Optional): List of delivery platform names
            to filter on.
        start_date (datetime, Optional): Start date to get email deliverability
            metrics.
        end_date (datetime, Optional): End date to get email deliverability
            metrics.
        aggregate (bool, Optional): Aggreagate values if set to true.
        mock (bool, Optional): Flag set to true when using mongomock.
    Returns:
        Union[list, None]: Deliverability metrics aggregated daily.
    """

    if delivery_platforms is None:
        deliver_platforms = [db_c.DELIVERY_PLATFORM_SFMC]

    pipeline = [
        {"$match": {"delivery_platform_type": {"$in": deliver_platforms}}},
        # Need to do this since Document DB does not support dateTrunc
        {
            "$project": {
                "_id": 0,
                "end_date": {
                    "$dateFromString": {
                        "dateString": {
                            "$dateToString": {
                                "format": "%Y-%m-%d",
                                "date": "$end_time",
                            }
                        }
                    }
                },
                "domain_name": "$performance_metrics.from_addr",
                "sent": "$performance_metrics.sent",
                "delivered": "$performance_metrics.delivered",
                "opens": "$performance_metrics.opens",
                "clicks": "$performance_metrics.clicks",
                "bounces": "$performance_metrics.bounces",
                "hard_bounces": "$performance_metrics.hard_bounces",
                "unsubscribes": "$performance_metrics.unsubscribes",
                "complaints": "$performance_metrics.complaints",
            }
        },
        {
            "$addFields": {
                "date_domain": {
                    "end_date": "$end_date",
                    "domain_name": "$domain_name",
                }
            }
        },
        {
            "$group": {
                "_id": "$date_domain",
                "sent": {"$sum": "$sent"},
                "delivered": {"$sum": "$delivered"},
                "opens": {"$sum": "$opens"},
                "clicks": {"$sum": "$clicks"},
                "bounces": {"$sum": "$bounces"},
                "hard_bounces": {"$sum": "$hard_bounces"},
                "unsubscribes": {"$sum": "$unsubscribes"},
                "complaints": {"$sum": "$complaints"},
            }
        },
        {
            "$project": {
                "_id": 0,
                "domain_name": "$_id.domain_name",
                "end_date": "$_id.end_date",
                "sent": "$sent",
                "delivered": "$delivered",
                "opens": "$opens",
                "clicks": "$clicks",
                "bounces": "$bounces",
                "hard_bounces": "$hard_bounces",
                "unsubscribes": "$unsubscribes",
                "complaints": "$complaints",
            }
        },
        {
            "$group": {
                "_id": "$domain_name",
                "deliverability_metrics": {
                    "$addToSet": {
                        "date": "$end_date",
                        "sent": "$sent",
                        "delivered": "$delivered",
                        "soft_bounces": {"$subtract": ["$bounces", "$hard_bounces"]},
                        "hard_bounces": "$hard_bounces",
                        "opens": "$opens",
                        "clicks": "$clicks",
                        "complaints": "$complaints",
                        "unsubscribes": "$unsubscribes",
                    }
                },
            }
        },
        {
            "$project": {
                "_id": 0,
                "domain_name": "$_id",
                "deliverability_metrics": "$deliverability_metrics",
            }
        },
    ]

    if mock:
        # mongomock does not support $dateToString
        pipeline[1]["$project"]["end_date"] = "$end_time"

    if domains:
        pipeline.insert(
            1,
            {
                "$match": {
                    "$or": [
                        {
                            "performance_metrics.from_addr": {
                                "$regex": f".*@{domain}$"
                            }
                        }
                        for domain in domains
                    ]
                }
            },
        )

    start_end_filter = match_start_end_date_stmt(
        start_date=start_date, end_date=end_date, date_field=db_c.JOB_END_TIME
    )
    if start_end_filter:
        pipeline.insert(1, start_end_filter)

    if aggregate:
        pipeline = pipeline + [
            {"$unwind": {"path": "$deliverability_metrics"}},
            {
                "$group": {
                    "_id": "$domain_name",
                    "sent": {"$sum": "$deliverability_metrics.sent"},
                    "soft_bounces": {"$sum": "$deliverability_metrics.soft_bounces"},
                    "hard_bounces": {"$sum": "$deliverability_metrics.hard_bounces"},
                    "opens": "$opens",
                    "clicks": "$clicks",
                    "complaints": "$complaints",
                    "unsubscribes": "$unsubscribes",
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "domain_name": "$_id",
                    "sent": "$sent",
                    "bounce_rate": "$bounce_rate",
                    "open_rate": "$open_rate",
                    "click_rate": "$click_rate",
                }
            },
        ]

    try:
        return list(
            database[db_c.DATA_MANAGEMENT_DATABASE][
                db_c.PERFORMANCE_METRICS_COLLECTION
            ].aggregate(pipeline)
        )

    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


def get_campaign_aggregated_sent_count(
        database: MongoClient,
        domains: list = None,
        delivery_platforms=None,
        start_date: datetime = None,
        end_date: datetime = None,
) -> Union[list, None]:
    """Retrieves aggregated sent data based on campaigns at domain level.

    Args:
        database (MongoClient): A database client.
        domains (list, Optional): List of domain names to be filtered.
        delivery_platforms (list, Optional): List of delivery platform names
            to filter on.
        start_date (datetime, Optional): Start date to get email deliverability
            metrics.
        end_date (datetime, Optional): End date to get email deliverability
            metrics.
    Returns:
        Union[list, None]: Aggregated data for sent.
    """
    if delivery_platforms is None:
        delivery_platforms = [db_c.DELIVERY_PLATFORM_SFMC]

    pipeline = [
        {
            '$match': {
                'delivery_platform_type': {
                    '$in': delivery_platforms
                }
            }
        }, {
            '$addFields': {
                'domain_journey_id': {
                    'domain_name': '$performance_metrics.from_addr',
                    'campaign_id': '$performance_metrics.journey_id'
                }
            }
        }, {
            '$group': {
                '_id': '$domain_journey_id',
                'sent': {
                    '$sum': '$performance_metrics.sent'
                }
            }
        }, {
            '$project': {
                'domain_name': '$_id.domain_name',
                'campaign_id': '$_id.campaign_id',
                'sent': '$sent',
                '_id': 0
            }
        }
    ]
    if domains:
        pipeline.insert(
            1,
            {
                "$match": {
                    "$or": [
                        {
                            "performance_metrics.from_addr": {
                                "$regex": f".*@{domain}$"
                            }
                        }
                        for domain in domains
                    ]
                }
            },
        )

    start_end_filter = match_start_end_date_stmt(
        start_date=start_date, end_date=end_date, date_field=db_c.JOB_END_TIME
    )
    if start_end_filter:
        pipeline.insert(1, start_end_filter)

    try:
        return list(
            database[db_c.DATA_MANAGEMENT_DATABASE][
                db_c.PERFORMANCE_METRICS_COLLECTION
            ].aggregate(pipeline)
        )

    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None