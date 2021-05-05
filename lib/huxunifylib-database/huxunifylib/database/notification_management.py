"""
This module enables functionality related to notification management
"""
import logging
from datetime import datetime

import pymongo
from marshmallow import ValidationError
from tenacity import retry, wait_fixed, retry_if_exception_type

import huxunifylib.database.constants as c
from huxunifylib.database.client import DatabaseClient


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def create_notification(
    database: DatabaseClient, notification_type: str, description: str
) -> dict:
    """A function to create a new notification

    Args:
        database (DatabaseClient): A database client.
        notification_type (str): type of notification to create.
        description (str): description of notification.

    Returns:
        dict: MongoDB document for a notification.

    """

    # validate type
    if not notification_type.lower() not in c.NOTIFICATION_TYPES:
        raise ValidationError(
            f"Invalid notification type received: {notification_type}. Must be one of {c.NOTIFICATION_TYPES}"
        )

    # get collection
    collection = database[c.DATA_MANAGEMENT_DATABASE][
        c.NOTIFICATIONS_COLLECTION
    ]

    # get current time
    current_time = datetime.utcnow()

    doc = {
        c.NOTIFICATION_FIELD_TYPE: notification_type,
        c.NOTIFICATION_FIELD_DESCRIPTION: description,
        c.NOTIFICATION_FIELD_CREATED: current_time,
    }

    try:
        notification_id = collection.insert_one(doc).inserted_id
        if notification_id is not None:
            return collection.find_one({c.ID: notification_id})
        logging.error("Failed to create a notification")
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


# TODO should this return a list of a dict that contains all the notifications?
@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_notifications(
    database: DatabaseClient,
    page_size: int,
    order: int,
    start_id: str = None,
) -> list:
    """A function to get notifications

    Args:
        database (DatabaseClient): A database client.
        page_size (int): number of notifications per page.
        order (int): dictate the order of the records that are returned.
                    (pymongo.DESCENDING or pymongo.ASCENDING)
        start_id (str): start id for pagination

    Returns:
        dict: MongoDB document for a notification.

    """
    # get collection
    collection = database[c.DATA_MANAGEMENT_DATABASE][
        c.NOTIFICATIONS_COLLECTION
    ]

    try:
        if start_id is None:
            return list(collection.find().sort({c.ID: order}).limit(page_size + 1))
        else:
            return list(
                collection.find({{c.ID: {"$gt": start_id}}, {c.ID: True}})
                .sort({c.ID: order})
                .limit(page_size + 1)
            )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None
