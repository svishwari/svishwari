"""
This module enables functionality related to notification management
"""
import logging
from datetime import datetime

import pymongo
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
        return None

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

    return {}

# TODO should this return a list of a dict that contains all the notifications?
@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_notifications(
    database: DatabaseClient,
    page_num: int,
    page_size: int,
    order_by: str,
    order: int,
) -> list:
    """A function to get notifications

    Args:
        database (DatabaseClient): A database client.
        page_num (int): page number.
        page_size (int): number of notifications per page.
        order_by (str): order the notification by 'timestamp' or 'type'
        order (str): dictate the order of the records that are returned. (pymongo.DESCENDING or pymongo.ASCENDING)

    Returns:
        dict: MongoDB document for a notification.

    """
    # get collection
    collection = database[c.DATA_MANAGEMENT_DATABASE][
        c.NOTIFICATIONS_COLLECTION
    ]

    skips = page_size * (page_num - 1)

    try:
        return list(
            collection.find()
            .sort(order_by, order)
            .skip(skips)
            .limit(page_size)
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return []
