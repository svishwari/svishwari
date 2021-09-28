"""This module enables functionality related to notification management."""
import logging
from datetime import datetime
from typing import Union

import pymongo
from tenacity import retry, wait_fixed, retry_if_exception_type

import huxunifylib.database.constants as c
from huxunifylib.database.client import DatabaseClient
from huxunifylib.database.db_exceptions import InvalidNotificationType


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def create_notification(
    database: DatabaseClient,
    notification_type: str,
    description: str,
    category: str = None,
) -> Union[dict, None]:
    """A function to create a new notification.

    Args:
        database (DatabaseClient): A database client.
        notification_type (str): type of notification to create.
        description (str): description of notification.
        category (str): category of notification.

    Returns:
        Union[dict, None]: MongoDB document for a notification.

    Raises:
        InvalidNotificationType: Error if the passed in notification_type value
            is not valid.
    """

    # validate type
    if notification_type.lower() not in c.NOTIFICATION_TYPES:
        raise InvalidNotificationType(notification_type)

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

    if category:
        doc[c.NOTIFICATION_FIELD_CATEGORY] = category

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
def get_notifications_batch(
    database: DatabaseClient,
    batch_size: int,
    sort_order: int,
    batch_number: int,
) -> Union[dict, None]:
    """A function to get notifications per batch size.

    Args:
        database (DatabaseClient): A database client.
        batch_size (int): Number of notifications per batch.
        sort_order (int): dictate the order of the records that are returned.
            (pymongo.DESCENDING or pymongo.ASCENDING)
        batch_number (int): Number of which batch should be returned.

    Returns:
        Union[dict, None]: MongoDB notification documents with total count of
            notifications .
    """

    # get collection
    collection = database[c.DATA_MANAGEMENT_DATABASE][
        c.NOTIFICATIONS_COLLECTION
    ]

    skips = batch_size * (batch_number - 1)

    try:
        return dict(
            total_records=collection.count_documents({}),
            notifications=list(
                collection.find()
                .sort([(c.NOTIFICATION_FIELD_CREATED, -1), (c.ID, sort_order)])
                .skip(skips)
                .limit(batch_size)
            ),
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_notifications(
    database: DatabaseClient,
    query_filter: Union[dict, None] = None,
    sort_order: Union[dict, None] = None,
) -> Union[dict, None]:
    """A function to get notifications

    Args:
        database (DatabaseClient): A database client.
        query_filter (Union[list[Tuple], None]): Mongo filter Query.
        sort_order (Tuple[str, int]): Mongo sort order.

    Returns:
        Union[dict, None]: MongoDB notification documents with total count of notifications .

    """

    # get collection
    collection = database[c.DATA_MANAGEMENT_DATABASE][
        c.NOTIFICATIONS_COLLECTION
    ]

    try:
        return dict(
            total_records=collection.count_documents(query_filter),
            notifications=list(
                collection.find(query_filter if query_filter else {}).sort(
                    sort_order
                    if sort_order
                    else [("$natural", pymongo.ASCENDING)]
                )
            ),
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None
