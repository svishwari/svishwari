"""This module enables functionality related to delivery platform management.
"""
# pylint: disable=C0302

import logging
from functools import partial
import datetime
from operator import itemgetter
from typing import Union, Optional, List

from bson import ObjectId
import pymongo
from pymongo.cursor import Cursor
from tenacity import retry, wait_fixed, retry_if_exception_type

import huxunifylib.database.db_exceptions as de
import huxunifylib.database.constants as db_c
from huxunifylib.database.client import DatabaseClient
from huxunifylib.database.utils import name_exists, get_collection_count
import huxunifylib.database.audience_management as am


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
# pylint: disable=R0914
def set_delivery_platform(
    database: DatabaseClient,
    delivery_platform_type: str,
    name: str,
    authentication_details: dict = None,
    status: str = db_c.STATUS_PENDING,
    enabled: bool = False,
    added: bool = False,
    deleted: bool = False,
    user_name: str = None,
    configuration: dict = None,
    is_ad_platform: bool = False,
    category: str = db_c.CATEGORY_UNKNOWN,
    link: str = "",
) -> Union[dict, None]:
    """A function to create a delivery platform.

    Args:
        database (DatabaseClient): A database client.
        delivery_platform_type (str): The type of delivery platform
            (Facebook, Amazon, or Google).
        name (str): Name of the delivery platform.
        authentication_details (dict): A dict containing delivery platform
            authentication details.
        status (str): status of the delivery platform.
        enabled (bool): if the delivery platform is enabled.
        added (bool): if the delivery platform is added.
        deleted (bool): if the delivery platform is deleted (soft-delete).
        user_name (str): Name of the user creating the delivery platform.
            This is Optional.
        configuration (dict): A dictionary consisting of any platform
            specific configurations.
        is_ad_platform (bool): If the delivery platform is an AD platform.
        category (str): Category of the delivery platform.
        link (str): Url to the sign in page for the delivery platform

    Returns:
        Union[dict, None]: MongoDB audience doc.

    Raises:
        DuplicateName: Error if a delivery platform with the same name exists
            already.
        UnknownDeliveryPlatformType: If delivery platform type is unknown.
    """

    platform_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[db_c.DELIVERY_PLATFORM_COLLECTION]

    # Make sure the name will be unique
    exists_flag = name_exists(
        database,
        db_c.DATA_MANAGEMENT_DATABASE,
        db_c.DELIVERY_PLATFORM_COLLECTION,
        db_c.DELIVERY_PLATFORM_NAME,
        name,
    )

    if exists_flag:
        raise de.DuplicateName(name)

    # Get current time
    curr_time = datetime.datetime.utcnow()

    doc = {
        db_c.DELIVERY_PLATFORM_TYPE: delivery_platform_type,
        db_c.DELIVERY_PLATFORM_NAME: name,
        db_c.DELIVERY_PLATFORM_STATUS: status,
        db_c.ENABLED: enabled,
        db_c.ADDED: added,
        db_c.DELETED: deleted,
        db_c.CREATE_TIME: curr_time,
        db_c.UPDATE_TIME: curr_time,
        db_c.FAVORITE: False,
        db_c.IS_AD_PLATFORM: is_ad_platform,
        db_c.CATEGORY: category,
        db_c.LINK: link,
    }
    if authentication_details is not None:
        doc[db_c.DELIVERY_PLATFORM_AUTH] = authentication_details

    if configuration is not None:
        doc[db_c.CONFIGURATION] = configuration

    # Add user name only if it is available
    if user_name:
        doc[db_c.CREATED_BY] = user_name
        doc[db_c.UPDATED_BY] = user_name

    try:
        delivery_platform_id = collection.insert_one(doc).inserted_id
        if delivery_platform_id is not None:
            return collection.find_one(
                {
                    db_c.ID: delivery_platform_id,
                    db_c.ENABLED: enabled,
                    db_c.DELETED: False,
                },
                {db_c.DELETED: 0},
            )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_delivery_platforms_by_id(
    database: DatabaseClient,
    delivery_platform_ids: list,
) -> Union[list, None]:
    """A function to get a list of delivery platforms by id.

    Args:
        database (DatabaseClient): A database client.
        delivery_platform_ids (list[ObjectId]): List of Delivery platform
            object ids.

    Returns:
        Union[list, None]: Delivery platform configuration.
    """

    platform_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[db_c.DELIVERY_PLATFORM_COLLECTION]

    try:
        return list(
            collection.find(
                {db_c.ID: {"$in": delivery_platform_ids}, db_c.DELETED: False},
                {db_c.DELETED: 0},
            )
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_delivery_platform(
    database: DatabaseClient,
    delivery_platform_id: ObjectId,
) -> Union[dict, None]:
    """A function to get a delivery platform.

    Args:
        database (DatabaseClient): A database client.
        delivery_platform_id (ObjectId): The MongoDB ID of the delivery
            platform.

    Returns:
        Union[dict, None]: Delivery platform configuration.
    """

    platform_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[db_c.DELIVERY_PLATFORM_COLLECTION]

    try:
        return collection.find_one(
            {db_c.ID: delivery_platform_id, db_c.DELETED: False},
            {db_c.DELETED: 0},
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_delivery_platform_by_type(
    database: DatabaseClient,
    delivery_platform_type: str,
) -> Union[dict, None]:
    """A function to get a delivery platform by type.

    Args:
        database (DatabaseClient): A database client.
        delivery_platform_type (str): The delivery platform type.

    Returns:
        Union[dict, None]: Delivery platform configuration.
    """

    platform_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[db_c.DELIVERY_PLATFORM_COLLECTION]
    try:
        return collection.find_one(
            {
                db_c.DELIVERY_PLATFORM_TYPE: delivery_platform_type,
                db_c.DELETED: False,
            },
            {db_c.DELETED: 0},
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_all_delivery_platforms(
    database: DatabaseClient,
    enabled: bool = None,
) -> Union[list, None]:
    """A function to get all configured delivery platforms.

    Args:
        database (DatabaseClient): A database client.
        enabled (Boolean): Enabled flag.

    Returns:
        Union[list, None]: A list of all delivery platform configuration dicts.
    """

    doc = None
    platform_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[db_c.DELIVERY_PLATFORM_COLLECTION]

    query_filter = {db_c.DELETED: False}
    if enabled is not None:
        query_filter[db_c.ENABLED] = enabled

    try:
        doc = list(collection.find(query_filter, {db_c.DELETED: 0}))
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return doc


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def set_connection_status(
    database: DatabaseClient,
    delivery_platform_id: ObjectId,
    connection_status: str,
) -> Union[dict, None]:
    """A function to set the status of connection to a delivery platform.

    Args:
        database (DatabaseClient): A database client.
        delivery_platform_id (ObjectId): MongoDB document ID of delivery
            platform.
        connection_status: Status of connection to delivery platform. Can be
            Pending, In progress, Failed, or Succeeded.

    Returns:
        Union[dict, None]: Updated delivery platform configuration.
    """

    doc = None
    platform_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[db_c.DELIVERY_PLATFORM_COLLECTION]

    update_doc = {}
    update_doc[db_c.DELIVERY_PLATFORM_STATUS] = connection_status
    update_doc[db_c.UPDATE_TIME] = datetime.datetime.utcnow()

    try:
        doc = collection.find_one_and_update(
            {db_c.ID: delivery_platform_id, db_c.DELETED: False},
            {"$set": update_doc},
            {db_c.DELETED: 0},
            upsert=False,
            new=True,
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return doc


def get_connection_status(
    database: DatabaseClient, delivery_platform_id: ObjectId
) -> Union[str, None]:
    """A function to get status of connection to delivery platform.

    Args:
        database (DatabaseClient): A database client.
        delivery_platform_id (ObjectId): MongoDB document ID of delivery
          platform.

    Returns:
        Union[str, None]: Status of delivery platform connection. Can be
            Pending, In Progress, Failed, or Succeeded.
    """

    connection_status = None

    doc = get_delivery_platform(database, delivery_platform_id)

    if db_c.DELIVERY_PLATFORM_STATUS in doc:
        connection_status = doc[db_c.DELIVERY_PLATFORM_STATUS]

    return connection_status


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def set_authentication_details(
    database: DatabaseClient,
    delivery_platform_id: ObjectId,
    authentication_details: dict,
) -> Union[dict, None]:
    """A function to set delivery platform authentication details.

    Args:
        database (DatabaseClient): A database client.
        delivery_platform_id (ObjectId): The MongoDB ID of delivery platform.
        authentication_details (dict): A dict containing delivery platform
            authentication details.

    Returns:
        Union[dict, None]: Updated delivery platform configuration.
    """

    doc = None
    platform_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[db_c.DELIVERY_PLATFORM_COLLECTION]

    update_doc = {}
    update_doc[db_c.DELIVERY_PLATFORM_AUTH] = authentication_details
    update_doc[db_c.UPDATE_TIME] = datetime.datetime.utcnow()

    try:
        doc = collection.find_one_and_update(
            {db_c.ID: delivery_platform_id, db_c.DELETED: False},
            {"$set": update_doc},
            {db_c.DELETED: 0},
            upsert=False,
            new=True,
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return doc


def get_authentication_details(
    database: DatabaseClient, delivery_platform_id: ObjectId
) -> Union[dict, None]:
    """A function to get authentication details of a delivery platform.

    Args:
        database (DatabaseClient): A database client.
        delivery_platform_id (ObjectId): MongoDB document ID of delivery
          platform.

    Returns:
        Union[dict, None]: Delivery authentication details.
    """

    auth_dict = None

    doc = get_delivery_platform(database, delivery_platform_id)

    if db_c.DELIVERY_PLATFORM_AUTH in doc:
        auth_dict = doc[db_c.DELIVERY_PLATFORM_AUTH]

    return auth_dict


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def set_name(
    database: DatabaseClient,
    delivery_platform_id: ObjectId,
    name: str,
) -> Union[dict, None]:
    """A function to set delivery platform name.

    Args:
        database (DatabaseClient): A database client.
        delivery_platform_id (ObjectId): The MongoDB ID of delivery platform.
        name (str): Delivery platform name.

    Returns:
        Union[dict, None]: Updated delivery platform configuration.

    Raises:
        DuplicateName: Error if a delivery platform with the same name exists
            already.
    """

    doc = None
    platform_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[db_c.DELIVERY_PLATFORM_COLLECTION]

    # Make sure the name will be unique
    exists_flag = name_exists(
        database,
        db_c.DATA_MANAGEMENT_DATABASE,
        db_c.DELIVERY_PLATFORM_COLLECTION,
        db_c.DELIVERY_PLATFORM_NAME,
        name,
    )

    if exists_flag:
        cur_doc = get_delivery_platform(
            database,
            delivery_platform_id,
        )
        if cur_doc[db_c.DELIVERY_PLATFORM_NAME] != name:
            raise de.DuplicateName(name)

    update_doc = {
        db_c.DELIVERY_PLATFORM_NAME: name,
        db_c.UPDATE_TIME: datetime.datetime.utcnow(),
    }

    try:
        doc = collection.find_one_and_update(
            {db_c.ID: delivery_platform_id, db_c.DELETED: False},
            {"$set": update_doc},
            {db_c.DELETED: 0},
            upsert=False,
            new=True,
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return doc


def get_name(
    database: DatabaseClient, delivery_platform_id: ObjectId
) -> Union[str, None]:
    """A function to get name of a delivery platform.

    Args:
        database (DatabaseClient): A database client.
        delivery_platform_id (ObjectId): MongoDB document ID of delivery
            platform.

    Returns:
        Union[str, None]: Delivery platform name.
    """

    name = None

    doc = get_delivery_platform(database, delivery_platform_id)

    if db_c.DELIVERY_PLATFORM_NAME in doc:
        name = doc[db_c.DELIVERY_PLATFORM_NAME]

    return name


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def set_platform_type(
    database: DatabaseClient,
    delivery_platform_id: ObjectId,
    delivery_platform_type: str,
) -> Union[dict, None]:
    """A function to set delivery platform type.

    Args:
        database (DatabaseClient): A database client.
        delivery_platform_id (ObjectId): The MongoDB ID of delivery platform.
        delivery_platform_type (str): Delivery platform type.

    Returns:
        Union[dict, None]: Updated delivery platform configuration.

    Raises:
        UnknownDeliveryPlatformType: If the delivery platform type is unknown.
    """

    if delivery_platform_type.upper() not in [
        x.upper() for x in db_c.SUPPORTED_DELIVERY_PLATFORMS
    ]:
        raise de.UnknownDeliveryPlatformType(delivery_platform_type)

    doc = None
    platform_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[db_c.DELIVERY_PLATFORM_COLLECTION]

    update_doc = {
        db_c.DELIVERY_PLATFORM_TYPE: delivery_platform_type,
        db_c.UPDATE_TIME: datetime.datetime.utcnow(),
    }

    try:
        doc = collection.find_one_and_update(
            {db_c.ID: delivery_platform_id, db_c.DELETED: False},
            {"$set": update_doc},
            {db_c.DELETED: 0},
            upsert=False,
            new=True,
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return doc


def get_platform_type(
    database: DatabaseClient, delivery_platform_id: ObjectId
) -> Union[str, None]:
    """A function to get the delivery platform type.

    Args:
        database (DatabaseClient): A database client.
        delivery_platform_id (ObjectId): MongoDB document ID of delivery
          platform.

    Returns:
        Union[str, None]: Delivery platform type.
    """

    delivery_platform_type = None

    doc = get_delivery_platform(database, delivery_platform_id)

    if db_c.DELIVERY_PLATFORM_TYPE in doc:
        delivery_platform_type = doc[db_c.DELIVERY_PLATFORM_TYPE]

    return delivery_platform_type


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
# pylint: disable=too-many-locals,too-many-branches
def update_delivery_platform(
    database: DatabaseClient,
    delivery_platform_id: ObjectId,
    name: str = None,
    delivery_platform_type: str = None,
    authentication_details: dict = None,
    added: bool = None,
    user_name: str = None,
    enabled: bool = None,
    deleted: bool = None,
    performance_de: dict = None,
    campaign_de: dict = None,
    is_ad_platform: bool = None,
    status: str = None,
    link: str = None,
) -> Union[dict, None]:
    """A function to update delivery platform configuration.

    Args:
        database (DatabaseClient): A database client.
        delivery_platform_id (ObjectId): The MongoDB ID of delivery platform.
        name (str): Delivery platform name.
        delivery_platform_type (str): Delivery platform type.
        authentication_details (dict): A dict containing delivery platform
            authentication details.
        added (bool): if the delivery platform is added.
        user_name (str): Name of the user updating the delivery platform.
            This is Optional.
        enabled (bool): if the delivery platform is enabled.
        deleted (bool): if the delivery platform is deleted (soft-delete).
        performance_de (dict): Performance Data Extension for only SFMC.
        campaign_de (dict): Campaign Data Extension for only SFMC.
        is_ad_platform (bool): If the delivery platform is an AD platform.
        status (str): Connection status
        link (str): Destination URL

    Returns:
        Union[dict, None]: Updated delivery platform configuration.

    Raises:
        UnknownDeliveryPlatformType: If the delivery platform type is unknown.
        DuplicateName: Error if a delivery platform with the same name exists
            already.
        NoUpdatesSpecified: Error if no updates were done to the delivery
            platform.
    """

    if delivery_platform_type.upper() not in [
        x.upper() for x in db_c.SUPPORTED_DELIVERY_PLATFORMS
    ]:
        raise de.UnknownDeliveryPlatformType(delivery_platform_type)

    doc = None
    platform_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[db_c.DELIVERY_PLATFORM_COLLECTION]

    # Make sure the name will be unique
    exists_flag = name_exists(
        database,
        db_c.DATA_MANAGEMENT_DATABASE,
        db_c.DELIVERY_PLATFORM_COLLECTION,
        db_c.DELIVERY_PLATFORM_NAME,
        name,
    )
    cur_doc = None
    if exists_flag:
        cur_doc = get_delivery_platform(database, delivery_platform_id)
        if cur_doc[db_c.DELIVERY_PLATFORM_NAME] != name:
            raise de.DuplicateName(name)

    update_doc = {
        db_c.DELIVERY_PLATFORM_NAME: name,
        db_c.DELIVERY_PLATFORM_TYPE: delivery_platform_type,
        db_c.DELIVERY_PLATFORM_AUTH: authentication_details,
        db_c.UPDATE_TIME: datetime.datetime.utcnow(),
    }

    if link:
        update_doc[db_c.LINK] = link

    if (
        cur_doc is not None
        and cur_doc[db_c.DELIVERY_PLATFORM_TYPE] == db_c.DELIVERY_PLATFORM_SFMC
    ):
        update_doc[db_c.CONFIGURATION] = {
            db_c.PERFORMANCE_METRICS_DATA_EXTENSION: performance_de,
            db_c.CAMPAIGN_ACTIVITY_DATA_EXTENSION: campaign_de,
        }

    if added is not None:
        update_doc[db_c.ADDED] = added

    if status is not None:
        update_doc[db_c.DELIVERY_PLATFORM_STATUS] = status

    if enabled is not None:
        update_doc[db_c.ENABLED] = enabled

    if deleted is not None:
        update_doc[db_c.DELETED] = deleted

    # Add user name only if it is available
    if user_name:
        update_doc[db_c.UPDATED_BY] = user_name

    if is_ad_platform:
        update_doc[db_c.IS_AD_PLATFORM] = is_ad_platform

    for item in list(update_doc):
        if update_doc[item] is None:
            del update_doc[item]

    try:
        if update_doc:
            doc = collection.find_one_and_update(
                {db_c.ID: delivery_platform_id, db_c.DELETED: False},
                {"$set": update_doc},
                {db_c.DELETED: 0},
                upsert=False,
                new=True,
            )
        else:
            raise de.NoUpdatesSpecified("delivery platform")

    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return doc


# pylint: disable=too-many-locals
@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def create_delivery_platform_lookalike_audience(
    database: DatabaseClient,
    delivery_platform_id: ObjectId,
    source_audience: dict,
    name: str,
    audience_size_percentage: float,
    country: str = None,
    user_name: str = "",
    audience_size: int = 0,
    status: str = db_c.AUDIENCE_STATUS_DELIVERING,
) -> Union[dict, None]:
    """A function to create a delivery platform lookalike audience.

    Args:
        database (DatabaseClient): A database client.
        delivery_platform_id (ObjectId): The Mongo ID of delivery platform.
        source_audience (dict): The source audience.
        name (str): Name of the lookalike audience.
        audience_size_percentage (float): Size percentage of the lookalike
            audience.
        country (str): Country of the lookalike audience.
        user_name (str): Name of the user creating the lookalike.
        audience_size (int): Size of the audience at creation.
        status (str): Status of the lookalike, default is delivering.

    Returns:
        Union[dict, None]: The lookalike audience configuration.

    Raises:
        InvalidID: If the passed in delivery_platform_id did not fetch a doc
            from the relevant db collection.
        DuplicateName: Error if a lookalike audience with the same name exists
            already.
    """

    ret_doc = None
    platform_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[db_c.LOOKALIKE_AUDIENCE_COLLECTION]

    # Validate delivery platform id
    if get_delivery_platform(database, delivery_platform_id) is None:
        raise de.InvalidID(delivery_platform_id)

    # set the source_audience_id from source_audience
    source_audience_id = source_audience[db_c.ID]

    # Validate source audience id
    if am.get_audience_config(database, source_audience_id) is None:
        raise de.InvalidID(source_audience_id)

    # Make sure the name will be unique
    if name_exists(
        database,
        db_c.DATA_MANAGEMENT_DATABASE,
        db_c.LOOKALIKE_AUDIENCE_COLLECTION,
        db_c.LOOKALIKE_AUD_NAME,
        name,
    ):
        raise de.DuplicateName(name)

    # Get current time
    curr_time = datetime.datetime.utcnow()

    doc = {
        db_c.DELIVERY_PLATFORM_ID: delivery_platform_id,
        db_c.LOOKALIKE_SOURCE_AUD_ID: source_audience_id,
        db_c.LOOKALIKE_AUD_NAME: name,
        db_c.LOOKALIKE_SOURCE_AUD_NAME: source_audience.get(db_c.NAME, ""),
        db_c.LOOKALIKE_SOURCE_AUD_SIZE: source_audience.get(db_c.SIZE, 0),
        db_c.LOOKALIKE_SOURCE_AUD_FILTERS: source_audience.get(
            db_c.AUDIENCE_FILTERS, []
        ),
        db_c.LOOKALIKE_AUD_COUNTRY: country,
        db_c.LOOKALIKE_AUD_SIZE_PERCENTAGE: audience_size_percentage,
        db_c.DELETED: False,
        db_c.CREATE_TIME: curr_time,
        db_c.UPDATE_TIME: curr_time,
        db_c.SIZE: audience_size,
        db_c.CREATED_BY: user_name,
        db_c.UPDATED_BY: user_name,
        db_c.STATUS: status,
    }

    if db_c.TAGS in source_audience:
        doc[db_c.TAGS] = source_audience[db_c.TAGS]

    try:
        inserted_id = collection.insert_one(doc).inserted_id

        recent_delivery_job = get_audience_recent_delivery_job(
            database, source_audience_id, delivery_platform_id
        )

        if recent_delivery_job:
            lookalike_auds = recent_delivery_job.get(
                db_c.DELIVERY_PLATFORM_LOOKALIKE_AUDS, []
            )
            lookalike_auds.append(inserted_id)
            set_delivery_job_lookalike_audiences(
                database, recent_delivery_job[db_c.ID], lookalike_auds
            )

        ret_doc = collection.find_one(
            {db_c.ID: inserted_id, db_c.DELETED: False}, {db_c.DELETED: 0}
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return ret_doc


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_delivery_platform_lookalike_audience(
    database: DatabaseClient,
    lookalike_audience_id: ObjectId,
) -> Union[dict, None]:
    """A function to get a delivery platform lookalike audience.

    Args:
        database (DatabaseClient): A database client.
        lookalike_audience_id (ObjectId): The Mongo ID of lookalike audience.

    Returns:
        Union[dict, None]: The lookalike audience configuration.
    """

    ret_doc = None
    platform_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[db_c.LOOKALIKE_AUDIENCE_COLLECTION]

    try:
        ret_doc = collection.find_one(
            {db_c.ID: lookalike_audience_id, db_c.DELETED: False},
            {db_c.DELETED: 0},
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return ret_doc


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_all_delivery_platform_lookalike_audiences(
    database: DatabaseClient,
    filter_dict: dict = None,
    projection: dict = None,
) -> Union[list, None]:
    """A function to get all delivery platform lookalike audience
    configurations.

    Args:
        database (DatabaseClient): A database client.
        filter_dict (dict): filter dictionary for adding custom filters.
        projection (dict): Dict that specifies which fields to return or not
            return.

    Returns:
        Union[list, None]: List of all lookalike audience configurations.
    """

    collection = database[db_c.DATA_MANAGEMENT_DATABASE][
        db_c.LOOKALIKE_AUDIENCE_COLLECTION
    ]

    # if deleted is not included in the filters, add it.
    if filter_dict:
        filter_dict[db_c.DELETED] = False
    else:
        filter_dict = {db_c.DELETED: False}

    # exclude the deleted field from returning
    if projection:
        projection[db_c.DELETED] = 0
    else:
        projection = {db_c.DELETED: 0}

    try:
        return list(collection.find(filter_dict, projection))
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def update_lookalike_audience_name(
    database: DatabaseClient,
    lookalike_audience_id: ObjectId,
    name: str,
) -> Union[dict, None]:
    """A function to update a delivery platform lookalike audience name.

    Args:
        database (DatabaseClient): A database client.
        lookalike_audience_id (ObjectId): The Mongo ID of lookalike audience.
        name (str): The new name of the lookalike audience.

    Returns:
        Union[dict, None]: The updated lookalike audience configuration.

    Raises:
        DuplicateName: Error if a lookalike audience with the same name exists
            already.
    """

    ret_doc = None
    platform_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[db_c.LOOKALIKE_AUDIENCE_COLLECTION]

    # Make sure the name will be unique
    exists_flag = name_exists(
        database,
        db_c.DATA_MANAGEMENT_DATABASE,
        db_c.LOOKALIKE_AUDIENCE_COLLECTION,
        db_c.LOOKALIKE_AUD_NAME,
        name,
    )

    if exists_flag:
        cur_doc = get_delivery_platform_lookalike_audience(
            database,
            lookalike_audience_id,
        )
        if cur_doc[db_c.LOOKALIKE_AUD_NAME] != name:
            raise de.DuplicateName(name)

    update_doc = {
        db_c.LOOKALIKE_AUD_NAME: name,
        db_c.UPDATE_TIME: datetime.datetime.utcnow(),
    }

    try:
        ret_doc = collection.find_one_and_update(
            {db_c.ID: lookalike_audience_id, db_c.DELETED: False},
            {"$set": update_doc},
            upsert=False,
            new=True,
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return ret_doc


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def update_lookalike_audience_size_percentage(
    database: DatabaseClient,
    lookalike_audience_id: ObjectId,
    audience_size_percentage: float,
) -> Union[dict, None]:
    """A function to update lookalike audience size percentage.

    Args:
        database (DatabaseClient): A database client.
        lookalike_audience_id (ObjectId): The Mongo ID of lookalike audience.
        audience_size_percentage (float): The new size percentage of the
            lookalike audience.

    Returns:
        Union[dict, None]: The updated lookalike audience configuration.
    """

    ret_doc = None
    platform_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[db_c.LOOKALIKE_AUDIENCE_COLLECTION]

    update_doc = {
        db_c.LOOKALIKE_AUD_SIZE_PERCENTAGE: audience_size_percentage,
        db_c.UPDATE_TIME: datetime.datetime.utcnow(),
    }

    try:
        ret_doc = collection.find_one_and_update(
            {db_c.ID: lookalike_audience_id, db_c.DELETED: False},
            {"$set": update_doc},
            upsert=False,
            new=True,
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return ret_doc


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def update_lookalike_audience(
    database: DatabaseClient,
    lookalike_audience_id: ObjectId,
    name: str = None,
    audience_size_percentage: float = None,
    country: str = None,
    user_name: str = "",
    audience_size: int = None,
) -> Union[dict, None]:
    """A function to update lookalike audience.

    Args:
        database (DatabaseClient): A database client.
        lookalike_audience_id (ObjectId): The Mongo ID of lookalike audience.
        name (str): The new name of the lookalike audience.
        audience_size_percentage (float): The new size percentage of the
            lookalike audience.
        country (str): Updated lookalike audience country.
        user_name (str): Username of the user updating the audience.
        audience_size (int): Size of the audience at update time.

    Returns:
        Union[dict, None]: The updated lookalike audience configuration.

    Raises:
        DuplicateName: Error if a lookalike audience with the same name exists
            already.
        NoUpdatesSpecified: Error if no updates were done to the lookalike
            audience collection.
    """

    ret_doc = None
    platform_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[db_c.LOOKALIKE_AUDIENCE_COLLECTION]

    # Make sure the name will be unique
    exists_flag = name_exists(
        database,
        db_c.DATA_MANAGEMENT_DATABASE,
        db_c.LOOKALIKE_AUDIENCE_COLLECTION,
        db_c.LOOKALIKE_AUD_NAME,
        name,
    )

    if exists_flag:
        cur_doc = get_delivery_platform_lookalike_audience(
            database,
            lookalike_audience_id,
        )
        if cur_doc[db_c.LOOKALIKE_AUD_NAME] != name:
            raise de.DuplicateName(name)

    update_doc = {
        db_c.LOOKALIKE_AUD_NAME: name,
        db_c.LOOKALIKE_AUD_COUNTRY: country,
        db_c.LOOKALIKE_AUD_SIZE_PERCENTAGE: audience_size_percentage,
        db_c.UPDATE_TIME: datetime.datetime.utcnow(),
        db_c.UPDATED_BY: user_name,
    }

    if audience_size:
        update_doc[db_c.SIZE] = audience_size

    for item in list(update_doc):
        if update_doc[item] is None:
            del update_doc[item]

    try:
        if update_doc:
            ret_doc = collection.find_one_and_update(
                {db_c.ID: lookalike_audience_id, db_c.DELETED: False},
                {"$set": update_doc},
                upsert=False,
                new=True,
            )
        else:
            raise de.NoUpdatesSpecified("lookalike audience")
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return ret_doc


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def set_delivery_job(
    database: DatabaseClient,
    audience_id: ObjectId,
    delivery_platform_id: ObjectId,
    delivery_platform_generic_campaigns: list,
    username: str,
    replace_audience: bool = False,
    engagement_id: ObjectId = None,
    delivery_platform_config: dict = None,
    status=db_c.AUDIENCE_STATUS_DELIVERING,
) -> Union[dict, None]:
    """A function to set an audience delivery job.

    Args:
        database (DatabaseClient): A database client.
        audience_id (ObjectId): MongoDB ID of the delivered audience.
        delivery_platform_id (ObjectId): Delivery platform ID.
        delivery_platform_generic_campaigns (list): generic campaign IDs.
        username (str): Username of user requesting to deliver an audience.
        replace_audience(bool): Audience replacement flag
        engagement_id (ObjectId): Engagement ID.
        delivery_platform_config (dict): the delivery platform config
            object that holds the data extensions.
        status (str): Delivery job status.

    Returns:
        Union[dict, None]: Delivery job configuration.

    Raises:
        MissingValueException: Raised if the username is missing.
        InvalidID: If the passed in delivery_platform_id did not fetch a doc
            from the relevant db collection.
        NoDeliveryPlatformConnection: If the delivery platform connection is
            not successful.
    """

    if username is None:
        raise de.MissingValueException("username")

    dp_doc = get_delivery_platform(database, delivery_platform_id)

    if dp_doc is None:
        raise de.InvalidID(delivery_platform_id)

    dp_status = get_connection_status(database, delivery_platform_id)

    if dp_status != db_c.STATUS_SUCCEEDED:
        raise de.NoDeliveryPlatformConnection(delivery_platform_id)

    am_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    collection = am_db[db_c.DELIVERY_JOBS_COLLECTION]

    curr_time = datetime.datetime.utcnow()

    doc = {
        db_c.AUDIENCE_ID: audience_id,
        db_c.CREATE_TIME: curr_time,
        db_c.UPDATE_TIME: curr_time,
        db_c.JOB_STATUS: status,
        db_c.DELIVERY_PLATFORM_ID: delivery_platform_id,
        db_c.DELIVERY_PLATFORM_GENERIC_CAMPAIGNS: (
            delivery_platform_generic_campaigns
        ),
        db_c.DELETED: False,
        db_c.DELIVERY_PLATFORM_AUD_SIZE: 0,
        db_c.USERNAME: username,
        db_c.REPLACE_AUDIENCE: replace_audience,
    }
    if engagement_id is not None:
        doc[db_c.ENGAGEMENT_ID] = engagement_id

    if delivery_platform_config is not None:
        doc[db_c.DELIVERY_PLATFORM_CONFIG] = delivery_platform_config

    try:
        delivery_job_id = collection.insert_one(doc).inserted_id
        collection.create_index(
            [
                (db_c.AUDIENCE_ID, pymongo.ASCENDING),
                (db_c.DELIVERY_PLATFORM_ID, pymongo.ASCENDING),
            ]
        )
        collection.create_index(
            [
                (db_c.AUDIENCE_ID, pymongo.ASCENDING),
                (db_c.ENGAGEMENT_ID, pymongo.ASCENDING),
            ],
            name="audience_engagement_index",
        )

        if delivery_job_id is not None:
            return collection.find_one(
                {db_c.ID: delivery_job_id, db_c.DELETED: False},
                {db_c.DELETED: 0},
            )

    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_delivery_job(
    database: DatabaseClient,
    delivery_job_id: ObjectId,
    engagement_id: ObjectId = None,
) -> Union[dict, None]:
    """A function to get an audience delivery job.

    Args:
        database (DatabaseClient): A database client.
        delivery_job_id (ObjectId): Delivery job id.
        engagement_id (ObjectId): Engagement id.

    Returns:
        Union[dict, None]: Delivery job configuration.
    """

    am_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    collection = am_db[db_c.DELIVERY_JOBS_COLLECTION]

    try:
        # set mongo_filter based on engagement id
        mongo_filter = {db_c.ID: delivery_job_id, db_c.DELETED: False}
        if engagement_id is not None:
            mongo_filter[db_c.ENGAGEMENT_ID] = engagement_id

        return collection.find_one(mongo_filter, {db_c.DELETED: 0})
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_delivery_jobs_using_metadata(
    database: DatabaseClient,
    engagement_id: ObjectId = None,
    audience_id: ObjectId = None,
    delivery_platform_id: ObjectId = None,
    delivery_platform_ids: list = None,
    engagement_ids: list = None,
    audience_ids: list = None,
) -> Union[list, None]:
    """A function to get delivery jobs based on engagement details.

    Args:
        database (DatabaseClient): A database client.
        engagement_id (ObjectId): Engagement id.
        audience_id (ObjectId): Audience id.
        delivery_platform_id (ObjectId): Delivery platform id.
        delivery_platform_ids (list): List of Delivery platform ids.
        engagement_ids (list): List of engagement ids.
        audience_ids (list): List of audience ids.
    Returns:
        Union[list, None]: List of matching delivery jobs, if any.

    Raises:
        InvalidID: If the passed in audience_id, engagement_id,
            delivery_platform_id is None.
    """

    if (
        engagement_id is None
        and audience_id is None
        and delivery_platform_id is None
    ):
        raise de.InvalidID()

    am_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    collection = am_db[db_c.DELIVERY_JOBS_COLLECTION]

    try:

        mongo_filter = {db_c.DELETED: False}
        if audience_id:
            mongo_filter[db_c.AUDIENCE_ID] = audience_id
        if engagement_id:
            mongo_filter[db_c.ENGAGEMENT_ID] = engagement_id
        if delivery_platform_id:
            mongo_filter[db_c.DELIVERY_PLATFORM_ID] = delivery_platform_id
        if delivery_platform_ids:
            mongo_filter[db_c.DELIVERY_PLATFORM_ID] = {
                "$in": delivery_platform_ids
            }
        if engagement_ids:
            mongo_filter[db_c.ENGAGEMENT_ID] = {"$in": engagement_ids}
        if audience_ids:
            mongo_filter[db_c.AUDIENCE_ID] = {"$in": audience_ids}
        return list(collection.find(mongo_filter, {db_c.DELETED: 0}))
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def set_delivery_job_status(
    database: DatabaseClient, delivery_job_id: ObjectId, job_status: str
) -> Union[dict, None]:
    """A function to set an delivery job status.

    Args:
        database (DatabaseClient): A database client.
        delivery_job_id (ObjectId): MongoDB document ID of delivery job.
        job_status: Status of delivery job. Can be Pending,
            In Progress, Failed, or Succeeded.

    Returns:
        Union[dict, None]: Updated delivery job configuration.
    """

    doc = None
    am_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    collection = am_db[db_c.DELIVERY_JOBS_COLLECTION]
    curr_time = datetime.datetime.utcnow()

    update_doc = {}
    update_doc[db_c.JOB_STATUS] = job_status
    update_doc[db_c.UPDATE_TIME] = curr_time

    if job_status in (db_c.AUDIENCE_STATUS_DELIVERED, db_c.STATUS_FAILED):
        update_doc[db_c.JOB_END_TIME] = curr_time
    elif job_status == db_c.AUDIENCE_STATUS_DELIVERING:
        update_doc[db_c.JOB_START_TIME] = curr_time

    try:
        doc = collection.find_one_and_update(
            {db_c.ID: delivery_job_id, db_c.DELETED: False},
            {"$set": update_doc},
            upsert=False,
            new=True,
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return doc


def get_delivery_job_status(
    database: DatabaseClient, delivery_job_id: ObjectId
) -> Union[str, None]:
    """A function to get an delivery job status.

    Args:
        database (DatabaseClient): A database client.
        delivery_job_id (ObjectId): MongoDB document ID of delivery
          job.

    Returns:
        Union[str, None]: Status of delivery job. Can be Pending,
          In Progress, Failed, or Succeeded.
    """

    job_status = None

    doc = get_delivery_job(database, delivery_job_id)

    if db_c.JOB_STATUS in doc:
        job_status = doc[db_c.JOB_STATUS]

    return job_status


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def set_delivery_job_audience_size(
    database: DatabaseClient,
    delivery_job_id: ObjectId,
    audience_size: int,
) -> Union[dict, None]:
    """A function to store delivery job audience size.

    Args:
        database (DatabaseClient): A database client.
        delivery_job_id (ObjectId): The Mongo DB ID of the delivery job.
        audience_size (int): Size of audience in delivery platform.

    Returns:
        Union[dict, None]: Stored delivery job configuration.
    """

    doc = None
    am_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    collection = am_db[db_c.DELIVERY_JOBS_COLLECTION]

    # Set update dict
    update_dict = {
        db_c.DELIVERY_PLATFORM_AUD_SIZE: audience_size,
    }

    # Update the doc.
    try:
        doc = collection.find_one_and_update(
            {db_c.ID: delivery_job_id, db_c.DELETED: False},
            {"$set": update_dict},
            upsert=False,
            return_document=pymongo.ReturnDocument.AFTER,
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return doc


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def set_delivery_job_lookalike_audiences(
    database: DatabaseClient,
    delivery_job_id: ObjectId,
    lookalike_audiences: list,
) -> Union[dict, None]:
    """A function to store delivery job lookalike audiences.

    Args:
        database (DatabaseClient): A database client.
        delivery_job_id (ObjectId): The Mongo DB ID of the delivery job.
        lookalike_audiences (list): List of lookalike audiences.

    Returns:
        Union[dict, None]: Stored delivery job configuration.
    """

    doc = None
    am_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    collection = am_db[db_c.DELIVERY_JOBS_COLLECTION]

    # Set update dict
    update_dict = {
        db_c.DELIVERY_PLATFORM_LOOKALIKE_AUDS: lookalike_audiences,
    }

    # Update the doc.
    try:
        doc = collection.find_one_and_update(
            {db_c.ID: delivery_job_id, db_c.DELETED: False},
            {"$set": update_dict},
            upsert=False,
            return_document=pymongo.ReturnDocument.AFTER,
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return doc


def get_delivery_job_audience_size(
    database: DatabaseClient, delivery_job_id: ObjectId
) -> Union[int, None]:
    """A function to get delivery job audience size.

    Args:
        database (DatabaseClient): A database client.
        delivery_job_id (ObjectId): MongoDB document ID of delivery job.

    Returns:
        Union[int, None]: Delivery platform audience size.
    """

    audience_size = None

    doc = get_delivery_job(
        database,
        delivery_job_id,
    )

    if db_c.DELIVERY_PLATFORM_AUD_SIZE in doc:
        audience_size = doc[db_c.DELIVERY_PLATFORM_AUD_SIZE]

    return audience_size


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_delivery_jobs(
    database: DatabaseClient,
    audience_id: ObjectId = None,
    engagement_id: ObjectId = None,
) -> list:
    """Get audience delivery jobs if audience_id is specified, otherwise,
    get all delivery jobs. In the latter case only ID field is returned
    per delivery job.

    Args:
        database (DatabaseClient): database client.
        audience_id (ObjectId, optional): audience ID. Defaults to None.
        engagement_id (ObjectId, optional): engagement ID. Defaults to None.

    Returns:
        list: List of delivery jobs.

    Raises:
        OperationFailure: If an exception occurs during mongo operation.
    """

    am_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    collection = am_db[db_c.DELIVERY_JOBS_COLLECTION]

    try:
        mongo_filter = {db_c.DELETED: False}
        if audience_id:
            mongo_filter[db_c.AUDIENCE_ID] = audience_id
        if engagement_id:
            mongo_filter[db_c.ENGAGEMENT_ID] = engagement_id

        cursor = collection.find(
            mongo_filter,
            {db_c.ENABLED: False} if audience_id else {db_c.ID: True},
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)
        raise

    return list(cursor)


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_all_delivery_jobs(
    database: DatabaseClient,
    filter_dict: dict = None,
    projection: dict = None,
    sort_list: list = None,
    limit: int = None,
) -> Union[list, None]:
    """A function to get all delivery jobs based on the args provided.

    Args:
        database (DatabaseClient): A database client.
        filter_dict (dict): filter dictionary for adding custom filters.
        projection (dict): Dict that specifies which fields to return or not return.
        sort_list (list): Sort list for mongo.
        limit (int): the number of documents to return in the query.

    Returns:
        Union[list, None]: List of n delivery jobs.
    """

    collection = database[db_c.DATA_MANAGEMENT_DATABASE][
        db_c.DELIVERY_JOBS_COLLECTION
    ]

    # if deleted is not included in the filters, add it.
    if filter_dict:
        filter_dict[db_c.DELETED] = False
    else:
        filter_dict = {db_c.DELETED: False}

    # exclude the deleted field from returning
    if projection:
        projection[db_c.DELETED] = 0
    else:
        projection = {db_c.DELETED: 0}

    # if sort list is none, set to default, otherwise set to the passed in list.
    # note, if an empty list is passed in, no sorting will happen.
    sort_list = (
        [(db_c.CREATE_TIME, pymongo.DESCENDING)]
        if sort_list is None
        else sort_list
    )

    try:
        cursor = collection.find(filter_dict, projection)
        if sort_list:
            cursor = cursor.sort(sort_list)

        # apply limit if set.
        return list(cursor.limit(limit) if isinstance(limit, int) else cursor)
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_audience_recent_delivery_job(
    database: DatabaseClient,
    audience_id: ObjectId,
    delivery_platform_id: ObjectId,
) -> Union[dict, None]:
    """A function to get the most recent delivery job associated with
    a given audience and delivery platform.

    Args:
        database (DatabaseClient): A database client.
        audience_id (ObjectId): The MongoDB ID of an audience.
        delivery_platform_id (ObjectId): The MongoDB ID of a delivery platform.

    Returns:
        Union[dict, None]: Most recent delivery job stored associated with the
            audience and delivery platform.
    """

    recent_delivery_job = None
    am_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    collection = am_db[db_c.DELIVERY_JOBS_COLLECTION]

    # retrieve the delivery jobs associated with the audience
    # and delivery platform
    try:
        cursor = collection.find(
            {
                db_c.AUDIENCE_ID: audience_id,
                db_c.DELIVERY_PLATFORM_ID: delivery_platform_id,
                db_c.DELETED: False,
            },
            {db_c.DELETED: 0},
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    # get the list of delivery jobs
    delivery_jobs = list(cursor)

    # if delivery jobs were retrieved
    if len(delivery_jobs) > 0:
        # sort the list by the delivery job ID and return the
        # most recent ID
        delivery_jobs.sort(key=itemgetter(db_c.ID), reverse=True)
        recent_delivery_job = delivery_jobs[0]

    return recent_delivery_job


def get_ingestion_job_audience_delivery_jobs(
    database: DatabaseClient,
    ingestion_job_id: ObjectId,
) -> list:
    """A function to get a list of of all audience deliveries given
    an ingestion job.

    Args:
        database (DatabaseClient): A database client.
        ingestion_job_id (ObjectId): The Mongo DB ID of the ingestion job.

    Returns:
        List: A list of audience deliveries.
    """

    all_delivery_jobs = []

    audience_ids = am.get_ingestion_job_audience_ids(
        database,
        ingestion_job_id,
    )

    if audience_ids:
        for audience_id in audience_ids:
            delivery_jobs = get_delivery_jobs(
                database,
                audience_id,
            )
            if delivery_jobs:
                all_delivery_jobs += delivery_jobs

    return all_delivery_jobs


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def create_delivery_job_generic_campaigns(
    database: DatabaseClient,
    delivery_job_id: ObjectId,
    generic_campaign: list,
) -> Union[dict, None]:
    """A function to create/update delivery platform generic campaigns.

    Args:
        database (DatabaseClient): A database client.
        delivery_job_id (ObjectId): MongoDB document ID of delivery job.
        generic_campaign (list): generic campaign details to be added.

    Returns:
        Union[dict, None]: Updated delivery job configuration.

    Raises:
        InvalidID: If the passed in delivery_job_id did not fetch a doc from
            the relevant db collection.
    """

    if get_delivery_job(database, delivery_job_id) is None:
        raise de.InvalidID(delivery_job_id)

    collection = database[db_c.DATA_MANAGEMENT_DATABASE][
        db_c.DELIVERY_JOBS_COLLECTION
    ]

    try:
        return collection.find_one_and_update(
            {db_c.ID: delivery_job_id, db_c.DELETED: False},
            {
                "$set": {
                    db_c.DELIVERY_PLATFORM_GENERIC_CAMPAIGNS: generic_campaign
                }
            },
            upsert=False,
            new=True,
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def delete_delivery_job_generic_campaigns(
    database: DatabaseClient,
    delivery_job_ids: list,
) -> int:
    """A function to update delivery platform generic campaigns.

    Args:
        database (DatabaseClient): A database client.
        delivery_job_ids (list): List of delivery job ids

    Returns:
         int: count of deleted records.
    """

    platform_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[db_c.DELIVERY_JOBS_COLLECTION]

    try:
        return collection.update_many(
            {db_c.ID: {"$in": delivery_job_ids}, db_c.DELETED: False},
            {"$set": {db_c.DELIVERY_PLATFORM_GENERIC_CAMPAIGNS: []}},
            upsert=False,
        ).modified_count
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return 0


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def favorite_delivery_platform(
    database: DatabaseClient,
    delivery_platform_id: ObjectId,
) -> Union[dict, None]:
    """A function to favorite a delivery platform.

    Args:
        database (DatabaseClient): A database client.
        delivery_platform_id (ObjectId): The ID of delivery platform.

    Returns:
        Union[dict, None]: Updated delivery platform configuration.
    """

    doc = None
    platform_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[db_c.DELIVERY_PLATFORM_COLLECTION]

    update_doc = {
        db_c.FAVORITE: True,
        db_c.UPDATE_TIME: datetime.datetime.utcnow(),
    }

    try:
        doc = collection.find_one_and_update(
            {db_c.ID: delivery_platform_id, db_c.DELETED: False},
            {"$set": update_doc},
            upsert=False,
            new=True,
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return doc


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def unfavorite_delivery_platform(
    database: DatabaseClient,
    delivery_platform_id: ObjectId,
) -> Union[dict, None]:
    """A function to unfavorite a delivery platform.

    Args:
        database (DatabaseClient): A database client.
        delivery_platform_id (ObjectId): The ID of delivery platform.

    Returns:
        Union[dict, None]: Updated delivery platform configuration.
    """

    doc = None
    platform_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[db_c.DELIVERY_PLATFORM_COLLECTION]

    update_doc = {
        db_c.FAVORITE: False,
        db_c.UPDATE_TIME: datetime.datetime.utcnow(),
    }

    try:
        doc = collection.find_one_and_update(
            {db_c.ID: delivery_platform_id, db_c.DELETED: False},
            {"$set": update_doc},
            upsert=False,
            new=True,
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return doc


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def favorite_lookalike_audience(
    database: DatabaseClient,
    lookalike_audience_id: ObjectId,
) -> Union[dict, None]:
    """A function to favorite a delivery platform lookalike audience.

    Args:
        database (DatabaseClient): A database client.
        lookalike_audience_id (ObjectId): The ID of lookalike audience.

    Returns:
        Union[dict, None]: The updated lookalike audience configuration.
    """

    ret_doc = None
    platform_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[db_c.LOOKALIKE_AUDIENCE_COLLECTION]

    update_doc = {
        db_c.FAVORITE: True,
        db_c.UPDATE_TIME: datetime.datetime.utcnow(),
    }

    try:
        ret_doc = collection.find_one_and_update(
            {db_c.ID: lookalike_audience_id, db_c.DELETED: False},
            {"$set": update_doc},
            upsert=False,
            new=True,
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return ret_doc


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def unfavorite_lookalike_audience(
    database: DatabaseClient,
    lookalike_audience_id: ObjectId,
) -> Union[dict, None]:
    """A function to unfavorite a delivery platform lookalike audience.

    Args:
        database (DatabaseClient): A database client.
        lookalike_audience_id (ObjectId): The ID of lookalike audience.

    Returns:
        Union[dict, None]: The updated lookalike audience configuration.
    """

    ret_doc = None
    platform_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[db_c.LOOKALIKE_AUDIENCE_COLLECTION]

    update_doc = {
        db_c.FAVORITE: False,
        db_c.UPDATE_TIME: datetime.datetime.utcnow(),
    }

    try:
        ret_doc = collection.find_one_and_update(
            {db_c.ID: lookalike_audience_id, db_c.DELETED: False},
            {"$set": update_doc},
            upsert=False,
            new=True,
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return ret_doc


def get_delivery_platform_delivery_jobs(
    database: DatabaseClient, delivery_platform_id: ObjectId
) -> list:
    """A function to get all delivery jobs given a delivery platform.

    Args:
        database (DatabaseClient): A database client.
        delivery_platform_id (ObjectId): Delivery platform id.

    Returns:
        list: List of delivery jobs for a delivery platform.

    Raises:
        OperationFailure: If an exception occurs during mongo operation.
    """

    am_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    collection = am_db[db_c.DELIVERY_JOBS_COLLECTION]

    try:
        cursor = collection.find(
            {
                db_c.DELIVERY_PLATFORM_ID: delivery_platform_id,
                db_c.DELETED: False,
            },
            {db_c.DELETED: 0},
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)
        raise

    return list(cursor)


def get_delivery_platforms_count(database: DatabaseClient) -> int:
    """A function to retrieve count of delivery platforms documents.

    Args:
        database (DatabaseClient): A database client.

    Returns:
        int: Count of delivery platforms documents.
    """

    return get_collection_count(
        database,
        db_c.DATA_MANAGEMENT_DATABASE,
        db_c.DELIVERY_PLATFORM_COLLECTION,
    )


def get_lookalike_audiences_count(database: DatabaseClient) -> int:
    """A function to retrieve count of lookalike audiences documents.

    Args:
        database (DatabaseClient): A database client.

    Returns:
        int: Count of lookalike audiences documents.
    """

    return get_collection_count(
        database,
        db_c.DATA_MANAGEMENT_DATABASE,
        db_c.LOOKALIKE_AUDIENCE_COLLECTION,
    )


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def _set_performance_metrics(
    database: DatabaseClient,
    collection_name: str,
    delivery_platform_id: ObjectId,
    delivery_platform_type: str,
    delivery_job_id: ObjectId,
    generic_campaigns: list,
    metrics_dict: dict,
    event_details: dict,
    start_time: datetime.datetime,
    end_time: datetime.datetime,
) -> Union[dict, None]:
    """Store campaign performance metrics helper function to accommodate
        differences in metric types across different delivery platforms.

    Args:
        database (DatabaseClient): A database client.
        collection_name (str): Name of collection in which operation is
            performed.
        delivery_platform_id (ObjectId): delivery platform ID
        delivery_platform_type (str): delivery platform type
        delivery_job_id (ObjectId): The delivery job ID of audience.
        generic_campaigns: (dict): generic campaigns
        metrics_dict (dict): A dict containing performance metrics.
        event_details (dict): A dict containing campaign activity data.
        start_time (datetime): Start time of metrics.
        end_time (datetime): End time of metrics.

    Returns:
        Union[dict, None]: MongoDB metrics doc.

    Raises:
        InvalidID: If the passed in delivery_job_id did not fetch a doc from
            the relevant db collection.
        OperationFailure: If an exception occurs during mongo operation.
    """

    platform_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[collection_name]

    # Check validity of delivery job ID
    if not get_delivery_job(database, delivery_job_id):
        raise de.InvalidID(delivery_job_id)

    doc = {
        db_c.METRICS_DELIVERY_PLATFORM_ID: delivery_platform_id,
        db_c.METRICS_DELIVERY_PLATFORM_TYPE: delivery_platform_type,
        db_c.DELIVERY_JOB_ID: delivery_job_id,
        db_c.CREATE_TIME: datetime.datetime.utcnow(),
        db_c.DELIVERY_PLATFORM_GENERIC_CAMPAIGNS: generic_campaigns,
        # By default not transferred for feedback to CDM or reporting yet
        db_c.STATUS_TRANSFERRED_FOR_FEEDBACK: False,
        db_c.STATUS_TRANSFERRED_FOR_REPORT: False,
    }

    doc.update(
        {
            db_c.METRICS_START_TIME: start_time,
            db_c.METRICS_END_TIME: end_time,
            db_c.PERFORMANCE_METRICS: metrics_dict,
        }
        if collection_name == db_c.PERFORMANCE_METRICS_COLLECTION
        else {db_c.EVENT_DETAILS: event_details}
    )

    try:
        metrics_id = collection.insert_one(doc).inserted_id
        collection.create_index([(db_c.DELIVERY_JOB_ID, pymongo.ASCENDING)])
        if metrics_id:
            return collection.find_one({db_c.ID: metrics_id})
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)
        raise

    return None


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def set_deliverability_metrics(
    database: DatabaseClient,
    delivery_platform_id: ObjectId,
    delivery_platform_type: str,
    domain: str,
    metrics_dict: dict,
    start_time: datetime.datetime,
    end_time: datetime.datetime,
) -> Union[dict, None]:
    """Store deliverability metrics in the deliverability metrics collection.
    Args:
        database (DatabaseClient): A database client.
        delivery_platform_id (ObjectId): delivery platform ID
        delivery_platform_type (str): delivery platform type
        domain (str): Domain name.
        metrics_dict (dict): A dict containing deliverability metrics.
        start_time (datetime): Start time of metrics.
        end_time (datetime): End time of metrics.
    Returns:
        Union[dict, None]: MongoDB metrics doc.
    Raises:
        InvalidID: If the passed in delivery_platform_id did not fetch a doc from
            the relevant db collection.
        OperationFailure: If an exception occurs during mongo operation.
    """

    platform_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[db_c.DELIVERABILITY_METRICS_COLLECTION]

    # Check validity of delivery job ID
    if not get_delivery_platform(database, delivery_platform_id):
        raise de.InvalidID(delivery_platform_id)

    try:
        metrics_id = collection.insert_one(
            {
                db_c.METRICS_START_TIME: start_time,
                db_c.METRICS_END_TIME: end_time,
                db_c.CREATE_TIME: datetime.datetime.utcnow(),
                db_c.DOMAIN: domain,
                db_c.DELIVERABILITY_METRICS: metrics_dict,
                db_c.METRICS_DELIVERY_PLATFORM_ID: delivery_platform_id,
                db_c.METRICS_DELIVERY_PLATFORM_TYPE: delivery_platform_type,
                # By default not transferred for  reporting yet
                db_c.STATUS_TRANSFERRED_FOR_REPORT: False,
            }
        ).inserted_id
        collection.create_index(
            [(db_c.DELIVERY_PLATFORM_ID, pymongo.ASCENDING)]
        )
        if metrics_id:
            return collection.find_one({db_c.ID: metrics_id})
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)
        raise

    return None


set_performance_metrics = partial(
    _set_performance_metrics,
    collection_name=db_c.PERFORMANCE_METRICS_COLLECTION,
    event_details=None,
)

set_campaign_activity = partial(
    _set_performance_metrics,
    collection_name=db_c.CAMPAIGN_ACTIVITY_COLLECTION,
    metrics_dict=None,
    start_time=None,
    end_time=None,
)


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def _get_performance_metrics(
    database: DatabaseClient,
    collection_name: str,
    delivery_job_id: ObjectId = None,
    min_start_time: datetime.datetime = None,
    max_end_time: datetime.datetime = None,
    delivery_platform_id: ObjectId = None,
    domain: str = None,
    pending_transfer_for_feedback: bool = False,
    pending_transfer_for_report: bool = False,
) -> Optional[List[dict]]:
    """Helper method to retrieve campaign performance metrics or activities.

    Args:
        database (DatabaseClient): database client.
        collection_name (str): Name of collection in which operation is
            performed.
        delivery_job_id (ObjectId): delivery job ID.
        min_start_time (datetime.datetime, optional): Min start time of
            metrics. Defaults to None.
        max_end_time (datetime.datetime, optional): Max start time of metrics.
            Defaults to None.
        delivery_platform_id (ObjectId): delivery platform ID.
        domain (str): Domain Name.
        pending_transfer_for_feedback (bool): If True, retrieve only metrics
            that have not been transferred for feedback. Defaults to False.
        pending_transfer_for_report (bool): If True, retrieve only metrics
            that have not been transferred for report. Defaults to False.

    Returns:
        Optional[List[dict]]: list of metrics.

    Raises:
        InvalidID: If the passed in delivery_job_id did not fetch a doc from
            the relevant db collection.
        OperationFailure: If an exception occurs during mongo operation.
    """

    platform_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[collection_name]

    # Check validity of delivery job ID
    if (
        not get_delivery_job(database, delivery_job_id)
        and collection_name != db_c.DELIVERABILITY_METRICS_COLLECTION
    ):
        logging.info("Delivery job with ID <%s> not found.", delivery_job_id)
        raise de.InvalidID(delivery_job_id)

    if (
        delivery_platform_id
        and not get_delivery_platform(database, delivery_platform_id)
        and collection_name == db_c.DELIVERABILITY_METRICS_COLLECTION
    ):
        logging.info(
            "Delivery platform with ID <%s> not found.", delivery_platform_id
        )
        raise de.InvalidID(delivery_platform_id)

    metric_queries = [{db_c.DELIVERY_JOB_ID: delivery_job_id}]

    if min_start_time:
        metric_queries.append(
            {db_c.METRICS_START_TIME: {"$gte": min_start_time}}
        )

    if max_end_time:
        metric_queries.append({db_c.METRICS_END_TIME: {"$lte": max_end_time}})

    if collection_name == db_c.DELIVERABILITY_METRICS_COLLECTION:
        metric_queries.append(
            {
                db_c.DELIVERY_PLATFORM_ID: delivery_platform_id,
                db_c.DOMAIN: domain,
            }
        )

    if pending_transfer_for_feedback:
        metric_queries.append(
            {db_c.STATUS_TRANSFERRED_FOR_FEEDBACK: {"$eq": False}}
        )

    if pending_transfer_for_report:
        metric_queries.append(
            {db_c.STATUS_TRANSFERRED_FOR_REPORT: {"$eq": False}}
        )

    try:
        return list(collection.find({"$and": metric_queries}))
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)
        raise

    return None


get_deliverability_metrics = partial(
    _get_performance_metrics,
    collection_name=db_c.DELIVERABILITY_METRICS_COLLECTION,
    min_start_time=None,
    max_end_time=None,
)

get_performance_metrics = partial(
    _get_performance_metrics,
    collection_name=db_c.PERFORMANCE_METRICS_COLLECTION,
)

get_campaign_activity = partial(
    _get_performance_metrics,
    collection_name=db_c.CAMPAIGN_ACTIVITY_COLLECTION,
    min_start_time=None,
    max_end_time=None,
)


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_performance_metrics_by_engagement_details(
    database: DatabaseClient,
    engagement_id: ObjectId,
    destination_ids: list,
) -> Union[list, None]:
    """Retrieve campaign performance metrics using engagement id.

    Args:
        database (DatabaseClient): database client.
        engagement_id (ObjectId): Engagement ID.
        destination_ids (list): Destination IDs.

    Returns:
        Union[list, None]: list of metrics or None.

    Raises:
        InvalidID: If the passed in engagement_id did not fetch a doc from the
            relevant db collection.
    """

    platform_db = database[db_c.DATA_MANAGEMENT_DATABASE]

    # Get delivery jobs using engagement id
    collection = platform_db[db_c.DELIVERY_JOBS_COLLECTION]

    try:
        delivery_jobs = collection.find(
            {
                db_c.ENGAGEMENT_ID: engagement_id,
                db_c.DELIVERY_PLATFORM_ID: {"$in": destination_ids},
            }
        )
        # Get performance metrics for all delivery jobs
        collection = platform_db[db_c.PERFORMANCE_METRICS_COLLECTION]
        delivery_job_ids = [x[db_c.ID] for x in delivery_jobs]
        return list(
            collection.find({db_c.DELIVERY_JOB_ID: {"$in": delivery_job_ids}})
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def _set_performance_metrics_status(
    database: DatabaseClient,
    collection_name: str,
    performance_metrics_id: ObjectId,
    performance_metrics_status: str,
) -> Union[dict, None]:
    """Helper to set performance metrics status.

    Args:
        database (DatabaseClient): database client.
        collection_name (str): Name of collection in which operation is
            performed.
        performance_metrics_id (ObjectId): performance metrics ID.
        performance_metrics_status (str): performance metrics status.

    Returns:
        Union[dict, None]: performance metrics document.
    """

    platform_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[collection_name]

    # TODO Below is also designed to accommodate
    # "transferred for reporting" status in the future
    update_doc = {}
    if performance_metrics_status == db_c.STATUS_TRANSFERRED_FOR_FEEDBACK:
        update_doc.update({db_c.STATUS_TRANSFERRED_FOR_FEEDBACK: True})

    if performance_metrics_status == db_c.STATUS_TRANSFERRED_FOR_REPORT:
        update_doc.update({db_c.STATUS_TRANSFERRED_FOR_REPORT: True})

    if update_doc:
        try:
            doc = collection.find_one_and_update(
                {db_c.ID: performance_metrics_id},
                {"$set": update_doc},
                upsert=False,
                new=True,
            )
            return doc
        except pymongo.errors.OperationFailure as exc:
            logging.error(exc)

    return None


set_metrics_transferred_for_feedback = partial(
    _set_performance_metrics_status,
    collection_name=db_c.PERFORMANCE_METRICS_COLLECTION,
    performance_metrics_status=db_c.STATUS_TRANSFERRED_FOR_FEEDBACK,
)

set_metrics_transferred_for_report = partial(
    _set_performance_metrics_status,
    collection_name=db_c.PERFORMANCE_METRICS_COLLECTION,
    performance_metrics_status=db_c.STATUS_TRANSFERRED_FOR_REPORT,
)

set_campaign_activity_transferred_for_feedback = partial(
    _set_performance_metrics_status,
    collection_name=db_c.CAMPAIGN_ACTIVITY_COLLECTION,
    performance_metrics_status=db_c.STATUS_TRANSFERRED_FOR_FEEDBACK,
)

set_campaign_activity_transferred_for_report = partial(
    _set_performance_metrics_status,
    collection_name=db_c.CAMPAIGN_ACTIVITY_COLLECTION,
    performance_metrics_status=db_c.STATUS_TRANSFERRED_FOR_REPORT,
)

set_deliverability_metrics_transferred_for_report = partial(
    _set_performance_metrics_status,
    collection_name=db_c.DELIVERABILITY_METRICS_COLLECTION,
    performance_metrics_status=db_c.STATUS_TRANSFERRED_FOR_REPORT,
)


def _get_all_performance_metrics(
    database: DatabaseClient,
    collection_name: str,
    pending_transfer_for_feedback: bool = False,
    pending_transfer_for_report: bool = False,
) -> Union[list, None]:
    """Helper to retrieve all campaign performance metrics or activity
    depending on delivery platform. Optionally the result can be filtered by
    metrics that are pending transfer either for feedback or reporting, but
    not both at the same time.

    Args:
        database (DatabaseClient): database client.
        collection_name (str): Name of collection in which operation is
            performed.
        pending_transfer_for_feedback (bool): If True, retrieve only metrics
            that have not been transferred for feedback. Defaults to False.
        pending_transfer_for_report (bool): If True, retrieve only metrics
            that have not been transferred for reporting. Defaults to False.

    Returns:
        Union[list, None]: list of performance metrics.

    Raises:
        ValueError: Error indicating flags pending_transfer_for_feedback and
            pending_transfer_for_report cannot both be True at the same time.
        OperationFailure: If an exception occurs during mongo operation.
    """

    platform_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[collection_name]

    if pending_transfer_for_feedback and pending_transfer_for_report:
        raise ValueError(
            "get_all_performance_metrics: Flags pending_transfer_for_feedback "
            "and pending_transfer_for_report cannot both be True at the "
            "same time."
        )

    try:
        if pending_transfer_for_feedback:
            return list(
                collection.find(
                    {db_c.STATUS_TRANSFERRED_FOR_FEEDBACK: {"$eq": False}}
                )
            )
        if pending_transfer_for_report:
            return list(
                collection.find(
                    {db_c.STATUS_TRANSFERRED_FOR_REPORT: {"$eq": False}}
                )
            )
        return list(collection.find())
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)
        raise


get_all_performance_metrics = partial(
    _get_all_performance_metrics,
    collection_name=db_c.PERFORMANCE_METRICS_COLLECTION,
)

get_all_campaign_activities = partial(
    _get_all_performance_metrics,
    collection_name=db_c.CAMPAIGN_ACTIVITY_COLLECTION,
)


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def set_audience_customers(
    database: DatabaseClient,
    delivery_job_id: ObjectId,
    customer_list: list,
) -> Union[dict, None]:
    """A function to set audience customer list for a delivery job.

    Args:
        database (DatabaseClient): A database client. Defaults to None.
        delivery_job_id (ObjectId): Delivery job ID.
        customer_list (list): List of customer ID processed during the
            delivery job.

    Returns:
        Union[dict, None]: MongoDB audience doc or None
    """

    ret_doc = None
    am_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    collection = am_db[db_c.AUDIENCE_CUSTOMERS_COLLECTION]

    audience_customers_doc = {
        db_c.DELIVERY_JOB_ID: delivery_job_id,
        db_c.AUDIENCE_CUSTOMER_LIST: customer_list,
    }

    try:
        audience_customers_doc_id = collection.insert_one(
            audience_customers_doc
        ).inserted_id
        collection.create_index([(db_c.DELIVERY_JOB_ID, pymongo.ASCENDING)])
        if audience_customers_doc_id is not None:
            ret_doc = collection.find_one({db_c.ID: audience_customers_doc_id})
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return ret_doc


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_all_audience_customers(
    database: DatabaseClient,
    delivery_job_id: ObjectId,
) -> Optional[Cursor]:
    """A function to fetch all audience customers docs for a delivery job.

    Args:
        database (DatabaseClient): A database client. Defaults to None.
        delivery_job_id (ObjectId): Delivery job ID.

    Returns:
        Cursor: An iterable cursor of customer lists.
    """

    audience_customers_docs = None
    am_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    collection = am_db[db_c.AUDIENCE_CUSTOMERS_COLLECTION]

    try:
        audience_customers_docs = collection.find(
            {db_c.DELIVERY_JOB_ID: delivery_job_id}
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return audience_customers_docs


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def _set_performance_metrics_bulk(
    database: DatabaseClient,
    collection_name: str,
    performance_metric_docs: list,
) -> dict:
    """Helper to store bulk campaign performance metrics or activities data
    depending on delivery platform.

    Args:
        database (DatabaseClient): A database client.
        collection_name (str): Name of collection in which operation is
            performed.
        performance_metric_docs (list): A list containing performance metrics
            documents.

    Returns:
        dict: dict containing insert_status & list of inserted ids.
    """

    platform_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[collection_name]

    insert_result = {"insert_status": False}

    try:
        result = collection.insert_many(performance_metric_docs, ordered=True)

        if result.acknowledged:
            insert_result["insert_status"] = True
            insert_result["inserted_ids"] = result.inserted_ids

        collection.create_index([(db_c.DELIVERY_JOB_ID, pymongo.ASCENDING)])

        return insert_result
    except pymongo.errors.BulkWriteError as exc:
        for err in exc.details["writeErrors"]:
            if err["code"] == db_c.DUPLICATE_ERR_CODE:
                logging.warning(
                    "Ignoring %s due to duplicate unique field!",
                    str(err["op"]),
                )
                continue
            logging.error(exc)
            return insert_result
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return insert_result


set_performance_metrics_bulk = partial(
    _set_performance_metrics_bulk,
    collection_name=db_c.PERFORMANCE_METRICS_COLLECTION,
)

set_campaign_activities = partial(
    _set_performance_metrics_bulk,
    collection_name=db_c.CAMPAIGN_ACTIVITY_COLLECTION,
)


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_most_recent_performance_metric_by_delivery_job(
    database: DatabaseClient,
    delivery_job_id: ObjectId,
) -> Union[dict, None]:
    """Retrieve the most recent campaign performance metrics associated with a
    given delivery job ID.

    Args:
        database (DatabaseClient): database client.
        delivery_job_id (ObjectId): delivery job ID.

    Returns:
        Union[dict, None]: most recent performance metric.

    Raises:
        InvalidID: If the passed in delivery_job_id did not fetch a doc from
            the relevant db collection.
    """

    platform_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[db_c.PERFORMANCE_METRICS_COLLECTION]

    # Check validity of delivery job ID
    doc = get_delivery_job(database, delivery_job_id)
    if not doc:
        raise de.InvalidID(delivery_job_id)

    try:
        cursor = list(
            collection.find({db_c.DELIVERY_JOB_ID: delivery_job_id})
            .sort([(db_c.JOB_END_TIME, -1)])
            .limit(1)
        )
        if len(cursor) > 0:
            return cursor[0]

    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_most_recent_deliverability_metric_by_domain(
    database: DatabaseClient,
    delivery_platform_id: ObjectId,
    domain: str,
) -> Union[list, None]:
    """Retrieve the most recent deliverability metrics associated with a
    given platform ID and domain.
    Args:
        database (DatabaseClient): database client.
        delivery_platform_id (ObjectId): delivery platform ID.
        domain (str): Domain Name.
    Returns:
        Union[list, None]: most recent deliverability metric.
    Raises:
        InvalidID: If the passed in platform_id did not fetch a doc from
            the relevant db collection.
    """

    platform_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[db_c.DELIVERABILITY_METRICS_COLLECTION]

    # Check validity of platform ID
    doc = get_delivery_platform(database, delivery_platform_id)
    if not doc:
        raise de.InvalidID(delivery_platform_id)

    try:

        cursor = list(
            collection.find(
                {
                    db_c.DELIVERY_PLATFORM_ID: delivery_platform_id,
                    db_c.DOMAIN: domain,
                }
            )
            .sort([(db_c.JOB_END_TIME, -1)])
            .limit(1)
        )
        if len(cursor) > 0:
            return cursor[0]

    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_most_recent_campaign_activity_by_delivery_job(
    database: DatabaseClient,
    delivery_job_id: ObjectId,
) -> Union[dict, None]:
    """Retrieve the most recent campaign activity event associated with a given
     delivery job ID.

    Args:
        database (DatabaseClient): database client.
        delivery_job_id (ObjectId): delivery job ID.

    Returns:
        Union[dict, None]: most recent performance metric.

    Raises:
        InvalidID: If the passed in delivery_job_id did not fetch a doc from
            the relevant db collection.
    """

    platform_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[db_c.CAMPAIGN_ACTIVITY_COLLECTION]

    # Check validity of delivery job ID
    doc = get_delivery_job(database, delivery_job_id)
    if not doc:
        return None

    try:
        cursor = list(
            collection.find({db_c.DELIVERY_JOB_ID: delivery_job_id})
            .sort([(f"{db_c.EVENT_DETAILS}.{db_c.EVENT_DATE}", -1)])
            .limit(1)
        )
        if len(cursor) > 0:
            return cursor[0]

    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def update_delivery_platform_doc(
    database: DatabaseClient,
    delivery_platform_id: ObjectId,
    update_dict: dict,
) -> Union[dict, None]:
    """Update MongoDb document.

    Args:
        database (DatabaseClient): database client.
        delivery_platform_id (ObjectId): MongoDB delivery platform ID.
        update_dict (dict): updating dictionary.

    Returns:
        dict: updated document.
    """

    try:
        return database[db_c.DATA_MANAGEMENT_DATABASE][
            db_c.DELIVERY_PLATFORM_COLLECTION
        ].find_one_and_update(
            {db_c.ID: delivery_platform_id},
            {"$set": update_dict},
            upsert=False,
            return_document=pymongo.ReturnDocument.AFTER,
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def update_pending_delivery_jobs(database: DatabaseClient) -> int:
    """Updates status of a delivery job for jobs with status as pending.
    Args:
        database (DatabaseClient): database client.
    Returns:
        int: Count of updated delivery jobs.
    """
    delivering_expire_time = datetime.datetime.utcnow() - datetime.timedelta(
        minutes=db_c.DELIVERY_JOB_TIMEOUT
    )
    try:
        updated_doc = database[db_c.DATA_MANAGEMENT_DATABASE][
            db_c.DELIVERY_JOBS_COLLECTION
        ].update_many(
            {
                db_c.STATUS: db_c.AUDIENCE_STATUS_DELIVERING,
                db_c.CREATE_TIME: {"$lt": delivering_expire_time},
            },
            {"$set": {db_c.STATUS: db_c.AUDIENCE_STATUS_ERROR}},
        )
        logging.info(
            "Updated %d delivery job status.", updated_doc.modified_count
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)
    return updated_doc.modified_count
