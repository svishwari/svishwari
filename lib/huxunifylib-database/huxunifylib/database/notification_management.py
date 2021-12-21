"""This module enables functionality related to notification management."""
import logging
import warnings
from datetime import datetime
from typing import Union, List, Any, Dict

import pymongo
from bson import ObjectId
from dateutil.relativedelta import relativedelta
from tenacity import retry, wait_fixed, retry_if_exception_type

import huxunifylib.database.constants as db_c
from huxunifylib.database.client import DatabaseClient
from huxunifylib.database.db_exceptions import (
    InvalidNotificationType,
    InvalidValueException,
    MissingValueException,
)


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def create_notification(
    database: DatabaseClient,
    notification_type: str,
    description: str,
    category: str = None,
    username: str = None,
) -> Union[dict, None]:
    """A function to create a new notification.

    Args:
        database (DatabaseClient): A database client.
        notification_type (str): type of notification to create.
        description (str): description of notification.
        category (str): category of notification.
        username (str): username of user performing an action for which the
            notification is created.

    Returns:
        Union[dict, None]: MongoDB document for a notification.

    Raises:
        InvalidNotificationType: Error if the passed in notification_type value
            is not valid.
    """

    # validate type
    if notification_type.lower() not in db_c.NOTIFICATION_TYPES:
        raise InvalidNotificationType(notification_type)

    if username is None:
        raise MissingValueException("username")

    # get collection
    collection = database[db_c.DATA_MANAGEMENT_DATABASE][
        db_c.NOTIFICATIONS_COLLECTION
    ]

    collection.create_index(
        [(db_c.TS, pymongo.ASCENDING)], expireAfterSeconds=0
    )

    # get current time
    current_time = datetime.utcnow()
    expire_time = current_time + relativedelta(months=3)

    # 3 months for critical, 1 month for informational
    if notification_type == db_c.NOTIFICATION_TYPE_INFORMATIONAL:
        expire_time = current_time + relativedelta(months=1)
    elif notification_type == db_c.NOTIFICATION_TYPE_SUCCESS:
        expire_time = current_time + relativedelta(months=6)
    elif notification_type == db_c.NOTIFICATION_TYPE_CRITICAL:
        expire_time = current_time + relativedelta(months=6)

    doc = {
        db_c.EXPIRE_AT: expire_time,
        db_c.NOTIFICATION_FIELD_TYPE: notification_type,
        db_c.NOTIFICATION_FIELD_DESCRIPTION: description,
        db_c.NOTIFICATION_FIELD_CREATED: current_time,
        db_c.DELETED: False,
        db_c.NOTIFICATION_FIELD_USERNAME: username,
    }

    if category:
        doc[db_c.NOTIFICATION_FIELD_CATEGORY] = category

    try:
        notification_id = collection.insert_one(doc).inserted_id
        if notification_id is not None:
            return collection.find_one({db_c.ID: notification_id})
        logging.error("Failed to create a notification")
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_notifications_batch(
    database: DatabaseClient,
    batch_size: int,
    sort_order: int,
    batch_number: int,
    notification_types: List[str],
    notification_categories: List[str],
    users: List[str],
    start_date: datetime,
    end_date: datetime,
) -> Union[dict, None]:
    """A function to get notifications per batch size.

    Args:
        end_date(datetime): End Date
        start_date(datetime): Start Date
        users(List[str]): List of User names
        notification_categories(List[str]): List of Notification Categories
        notification_types (List[str]): List of Type of Notifications
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
    collection = database[db_c.DATA_MANAGEMENT_DATABASE][
        db_c.NOTIFICATIONS_COLLECTION
    ]

    skips = batch_size * (batch_number - 1)
    query = dict({db_c.DELETED: False})  # type: Dict[str,Any]
    if notification_types:
        query.update({db_c.TYPE: {"$in": notification_types}})
    if notification_categories:
        query.update(
            {
                db_c.NOTIFICATION_FIELD_CATEGORY: {
                    "$in": notification_categories
                }
            }
        )
    if users:
        query.update({db_c.NOTIFICATION_FIELD_USERNAME: {"$in": users}})
    if start_date and end_date:
        # include notifications created on end_date
        end_date = end_date + relativedelta(days=1)

        query.update(
            {
                db_c.NOTIFICATION_FIELD_CREATED: {
                    "$gte": start_date,
                    "$lt": end_date,
                }
            }
        )
    if query:
        query = dict({"$and": [query]})
    try:
        return dict(
            total_records=collection.count_documents(query),
            notifications=list(
                collection.find(query)
                .sort(
                    [
                        (db_c.NOTIFICATION_FIELD_CREATED, -1),
                        (db_c.ID, sort_order),
                    ]
                )
                .skip(skips)
                .limit(batch_size)
            ),
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_notifications(
    database: DatabaseClient,
    query_filter: Union[dict, None] = None,
    sort_order: Union[dict, None] = None,
) -> Union[dict, None]:
    """A function to get notifications.

    Args:
        database (DatabaseClient): A database client.
        query_filter (Union[list[Tuple], None]): Mongo filter Query.
        sort_order (Tuple[str, int]): Mongo sort order.

    Returns:
        Union[dict, None]: MongoDB notification documents with total count of
            notifications.
    """

    # get collection
    collection = database[db_c.DATA_MANAGEMENT_DATABASE][
        db_c.NOTIFICATIONS_COLLECTION
    ]

    query_filter[db_c.DELETED] = False

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


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def delete_notification(
    database: DatabaseClient,
    notification_id: ObjectId,
    hard_delete: bool = False,
) -> bool:
    """A function to delete a notification using ID.

    Args:
        database (DatabaseClient): A database client.
        notification_id (ObjectId): Object Id of the notification.
        hard_delete (bool): hard deletes an notification if True.

    Returns:
        bool: Flag indicating successful operation.
    """

    collection = database[db_c.DATA_MANAGEMENT_DATABASE][
        db_c.NOTIFICATIONS_COLLECTION
    ]

    try:
        if hard_delete:
            collection.delete_one({db_c.ID: notification_id})
            return True
        doc = collection.find_one_and_update(
            {db_c.ID: notification_id},
            {"$set": {db_c.DELETED: True}},
            upsert=False,
            new=True,
        )
        return doc[db_c.DELETED]
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return False


def get_notification(
    database: DatabaseClient, notification_id: ObjectId
) -> Union[dict, None]:
    """To get notification

    Args:
        database (DatabaseClient): MongoDB Database Client
        notification_id (ObjectId): MongoDB Object Id

    Returns:
        Tuple[dict,None]:MongoDB Notification document else None

    """
    # get collection
    collection = database[db_c.DATA_MANAGEMENT_DATABASE][
        db_c.NOTIFICATIONS_COLLECTION
    ]

    try:
        return collection.find_one(
            {db_c.ID: notification_id, db_c.DELETED: False}
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None
