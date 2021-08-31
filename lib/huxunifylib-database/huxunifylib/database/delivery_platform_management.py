"""
This module enables functionality related to delivery platform management.
"""
# pylint: disable=C0302

import logging
from functools import partial
import datetime
from operator import itemgetter
from typing import Union

from bson import ObjectId
import pymongo
from tenacity import retry, wait_fixed, retry_if_exception_type

import huxunifylib.database.db_exceptions as de
import huxunifylib.database.constants as c
from huxunifylib.database.client import DatabaseClient
from huxunifylib.database.utils import name_exists, get_collection_count
import huxunifylib.database.audience_management as am


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
# pylint: disable=R0914
def set_delivery_platform(
    database: DatabaseClient,
    delivery_platform_type: str,
    name: str,
    authentication_details: dict = None,
    status: str = c.STATUS_PENDING,
    enabled: bool = False,
    added: bool = False,
    deleted: bool = False,
    user_name: str = None,
    configuration: dict = None,
    is_ad_platform: bool = False,
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
    Returns:
        Union[dict, None]: MongoDB audience doc.
    """

    platform_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[c.DELIVERY_PLATFORM_COLLECTION]

    # Make sure the name will be unique
    exists_flag = name_exists(
        database,
        c.DATA_MANAGEMENT_DATABASE,
        c.DELIVERY_PLATFORM_COLLECTION,
        c.DELIVERY_PLATFORM_NAME,
        name,
    )

    if exists_flag:
        raise de.DuplicateName(name)

    if delivery_platform_type.upper() not in [
        x.upper() for x in c.SUPPORTED_DELIVERY_PLATFORMS
    ]:
        raise de.UnknownDeliveryPlatformType(delivery_platform_type)

    # Get current time
    curr_time = datetime.datetime.utcnow()

    doc = {
        c.DELIVERY_PLATFORM_TYPE: delivery_platform_type,
        c.DELIVERY_PLATFORM_NAME: name,
        c.DELIVERY_PLATFORM_STATUS: status,
        c.ENABLED: enabled,
        c.ADDED: added,
        c.DELETED: deleted,
        c.CREATE_TIME: curr_time,
        c.UPDATE_TIME: curr_time,
        c.FAVORITE: False,
        c.IS_AD_PLATFORM: is_ad_platform,
    }
    if authentication_details is not None:
        doc[c.DELIVERY_PLATFORM_AUTH] = authentication_details

    if configuration is not None:
        doc[c.CONFIGURATION] = configuration

    # Add user name only if it is available
    if user_name:
        doc[c.CREATED_BY] = user_name
        doc[c.UPDATED_BY] = user_name

    try:
        delivery_platform_id = collection.insert_one(doc).inserted_id
        if delivery_platform_id is not None:
            return collection.find_one(
                {
                    c.ID: delivery_platform_id,
                    c.ENABLED: enabled,
                    c.DELETED: False,
                },
                {c.DELETED: 0},
            )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_delivery_platforms_by_id(
    database: DatabaseClient,
    delivery_platform_ids: list,
) -> Union[list, None]:
    """A function to get a list of delivery platforms by id.

    Args:
        database (DatabaseClient): A database client.
        delivery_platform_ids (list[ObjectId]):
            List of Delivery platform object ids.

    Returns:
        Union[list, None]: Delivery platform configuration.
    """

    platform_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[c.DELIVERY_PLATFORM_COLLECTION]

    try:
        return list(
            collection.find(
                {c.ID: {"$in": delivery_platform_ids}, c.DELETED: False},
                {c.DELETED: 0},
            )
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_delivery_platform(
    database: DatabaseClient,
    delivery_platform_id: ObjectId,
) -> Union[dict, None]:
    """A function to get a delivery platform.

    Args:
        database (DatabaseClient): A database client.
        delivery_platform_id (ObjectId): The MongoDB ID of the delivery platform.

    Returns:
        Union[dict, None]: Delivery platform configuration.
    """

    platform_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[c.DELIVERY_PLATFORM_COLLECTION]

    try:
        return collection.find_one(
            {c.ID: delivery_platform_id, c.DELETED: False}, {c.DELETED: 0}
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
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

    platform_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[c.DELIVERY_PLATFORM_COLLECTION]
    try:
        return collection.find_one(
            {
                c.DELIVERY_PLATFORM_TYPE: delivery_platform_type,
                c.DELETED: False,
            },
            {c.DELETED: 0},
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_all_delivery_platforms(
    database: DatabaseClient,
) -> Union[list, None]:
    """A function to get all configured delivery platforms.

    Args:
        database (DatabaseClient): A database client.

    Returns:
        Union[list, None]: A list of all delivery platform configuration dicts.
    """

    doc = None
    platform_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[c.DELIVERY_PLATFORM_COLLECTION]

    try:
        doc = list(collection.find({c.DELETED: False}, {c.DELETED: 0}))
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return doc


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
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
        delivery_platform_id (ObjectId): MongoDB document ID of delivery platform.
        connection_status: Status of connection to delivery platform. Can be Pending,
            In progress, Failed, or Succeeded.

    Returns:
        Union[dict, None]: Updated delivery platform configuration.
    """

    doc = None
    platform_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[c.DELIVERY_PLATFORM_COLLECTION]

    update_doc = {}
    update_doc[c.DELIVERY_PLATFORM_STATUS] = connection_status
    update_doc[c.UPDATE_TIME] = datetime.datetime.utcnow()

    try:
        doc = collection.find_one_and_update(
            {c.ID: delivery_platform_id, c.DELETED: False},
            {"$set": update_doc},
            {c.DELETED: 0},
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
        Union[str, None]: Status of delivery platform connection. Can be Pending,
          In Progress, Failed, or Succeeded.
    """

    connection_status = None

    doc = get_delivery_platform(database, delivery_platform_id)

    if c.DELIVERY_PLATFORM_STATUS in doc:
        connection_status = doc[c.DELIVERY_PLATFORM_STATUS]

    return connection_status


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
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
        authentication_details (dict): A dict containing delivery platform authentication details.

    Returns:
        Union[dict, None]: Updated delivery platform configuration.
    """

    doc = None
    platform_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[c.DELIVERY_PLATFORM_COLLECTION]

    update_doc = {}
    update_doc[c.DELIVERY_PLATFORM_AUTH] = authentication_details
    update_doc[c.UPDATE_TIME] = datetime.datetime.utcnow()

    try:
        doc = collection.find_one_and_update(
            {c.ID: delivery_platform_id, c.DELETED: False},
            {"$set": update_doc},
            {c.DELETED: 0},
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

    if c.DELIVERY_PLATFORM_AUTH in doc:
        auth_dict = doc[c.DELIVERY_PLATFORM_AUTH]

    return auth_dict


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
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
    """

    doc = None
    platform_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[c.DELIVERY_PLATFORM_COLLECTION]

    # Make sure the name will be unique
    exists_flag = name_exists(
        database,
        c.DATA_MANAGEMENT_DATABASE,
        c.DELIVERY_PLATFORM_COLLECTION,
        c.DELIVERY_PLATFORM_NAME,
        name,
    )

    if exists_flag:
        cur_doc = get_delivery_platform(
            database,
            delivery_platform_id,
        )
        if cur_doc[c.DELIVERY_PLATFORM_NAME] != name:
            raise de.DuplicateName(name)

    update_doc = {
        c.DELIVERY_PLATFORM_NAME: name,
        c.UPDATE_TIME: datetime.datetime.utcnow(),
    }

    try:
        doc = collection.find_one_and_update(
            {c.ID: delivery_platform_id, c.DELETED: False},
            {"$set": update_doc},
            {c.DELETED: 0},
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

    if c.DELIVERY_PLATFORM_NAME in doc:
        name = doc[c.DELIVERY_PLATFORM_NAME]

    return name


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
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
    """

    if delivery_platform_type.upper() not in [
        x.upper() for x in c.SUPPORTED_DELIVERY_PLATFORMS
    ]:
        raise de.UnknownDeliveryPlatformType(delivery_platform_type)

    doc = None
    platform_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[c.DELIVERY_PLATFORM_COLLECTION]

    update_doc = {
        c.DELIVERY_PLATFORM_TYPE: delivery_platform_type,
        c.UPDATE_TIME: datetime.datetime.utcnow(),
    }

    try:
        doc = collection.find_one_and_update(
            {c.ID: delivery_platform_id, c.DELETED: False},
            {"$set": update_doc},
            {c.DELETED: 0},
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

    if c.DELIVERY_PLATFORM_TYPE in doc:
        delivery_platform_type = doc[c.DELIVERY_PLATFORM_TYPE]

    return delivery_platform_type


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
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
    is_ad_platform: bool = None,
) -> Union[dict, None]:
    """A function to update delivery platform configuration.

    Args:
        database (DatabaseClient): A database client.
        delivery_platform_id (ObjectId): The MongoDB ID of delivery platform.
        name (str): Delivery platform name.
        delivery_platform_type (str): Delivery platform type.
        authentication_details (dict): A dict containing delivery platform authentication details.
        added (bool): if the delivery platform is added.
        user_name (str): Name of the user updating the delivery platform.
            This is Optional.
        enabled (bool): if the delivery platform is enabled.
        deleted (bool): if the delivery platform is deleted (soft-delete).
        performance_de (dict): Performance Data Extension for only SFMC.
        is_ad_platform (bool): If the delivery platform is an AD platform.
    Returns:
        Union[dict, None]: Updated delivery platform configuration.
    """

    if delivery_platform_type.upper() not in [
        x.upper() for x in c.SUPPORTED_DELIVERY_PLATFORMS
    ]:
        raise de.UnknownDeliveryPlatformType(delivery_platform_type)

    doc = None
    platform_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[c.DELIVERY_PLATFORM_COLLECTION]

    # Make sure the name will be unique
    exists_flag = name_exists(
        database,
        c.DATA_MANAGEMENT_DATABASE,
        c.DELIVERY_PLATFORM_COLLECTION,
        c.DELIVERY_PLATFORM_NAME,
        name,
    )
    cur_doc = None
    if exists_flag:
        cur_doc = get_delivery_platform(database, delivery_platform_id)
        if cur_doc[c.DELIVERY_PLATFORM_NAME] != name:
            raise de.DuplicateName(name)

    update_doc = {
        c.DELIVERY_PLATFORM_NAME: name,
        c.DELIVERY_PLATFORM_TYPE: delivery_platform_type,
        c.DELIVERY_PLATFORM_AUTH: authentication_details,
        c.UPDATE_TIME: datetime.datetime.utcnow(),
    }

    if (
        cur_doc is not None
        and cur_doc[c.DELIVERY_PLATFORM_TYPE] == c.DELIVERY_PLATFORM_SFMC
    ):
        update_doc[c.PERFORMANCE_METRICS_DATA_EXTENSION] = performance_de

    if added is not None:
        update_doc[c.ADDED] = added
        update_doc[c.DELIVERY_PLATFORM_STATUS] = c.STATUS_SUCCEEDED

    if enabled is not None:
        update_doc[c.ENABLED] = enabled

    if deleted is not None:
        update_doc[c.DELETED] = deleted

    # Add user name only if it is available
    if user_name:
        update_doc[c.UPDATED_BY] = user_name

    if is_ad_platform:
        update_doc[c.IS_AD_PLATFORM] = is_ad_platform

    for item in list(update_doc):
        if update_doc[item] is None:
            del update_doc[item]

    try:
        if update_doc:
            doc = collection.find_one_and_update(
                {c.ID: delivery_platform_id, c.DELETED: False},
                {"$set": update_doc},
                {c.DELETED: 0},
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
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def create_delivery_platform_lookalike_audience(
    database: DatabaseClient,
    delivery_platform_id: ObjectId,
    source_audience_id: ObjectId,
    name: str,
    audience_size_percentage: float,
    country: str = None,
    user_name: str = "",
    audience_size: int = 0,
) -> Union[dict, None]:
    """A function to create a delivery platform lookalike audience.

    Args:
        database (DatabaseClient): A database client.
        delivery_platform_id (ObjectId): The Mongo ID of delivery platform.
        source_audience_id (ObjectId): The Mongo ID of source audience.
        name (str): Name of the lookalike audience.
        audience_size_percentage (float): Size percentage of the lookalike audience.
        country (str): Country of the lookalike audience.
        user_name (str): Name of the user creating the lookalike.
        audience_size (int): Size of the audience at creation.

    Returns:
        Union[dict, None]: The lookalike audience configuration.
    """

    ret_doc = None
    platform_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[c.LOOKALIKE_AUDIENCE_COLLECTION]

    # Validate delivery platform id
    if get_delivery_platform(database, delivery_platform_id) is None:
        raise de.InvalidID(delivery_platform_id)

    # Validate source audience id
    if am.get_audience_config(database, source_audience_id) is None:
        raise de.InvalidID(source_audience_id)

    # Make sure the name will be unique
    if name_exists(
        database,
        c.DATA_MANAGEMENT_DATABASE,
        c.LOOKALIKE_AUDIENCE_COLLECTION,
        c.LOOKALIKE_AUD_NAME,
        name,
    ):
        raise de.DuplicateName(name)

    # Get current time
    curr_time = datetime.datetime.utcnow()

    doc = {
        c.DELIVERY_PLATFORM_ID: delivery_platform_id,
        c.LOOKALIKE_SOURCE_AUD_ID: source_audience_id,
        c.LOOKALIKE_AUD_NAME: name,
        c.LOOKALIKE_AUD_COUNTRY: country,
        c.LOOKALIKE_AUD_SIZE_PERCENTAGE: audience_size_percentage,
        c.DELETED: False,
        c.CREATE_TIME: curr_time,
        c.UPDATE_TIME: curr_time,
        c.SIZE: audience_size,
        c.CREATED_BY: user_name,
        c.UPDATED_BY: user_name,
    }

    try:
        inserted_id = collection.insert_one(doc).inserted_id

        recent_delivery_job = get_audience_recent_delivery_job(
            database, source_audience_id, delivery_platform_id
        )

        if recent_delivery_job:
            lookalike_auds = recent_delivery_job.get(
                c.DELIVERY_PLATFORM_LOOKALIKE_AUDS, []
            )
            lookalike_auds.append(inserted_id)
            set_delivery_job_lookalike_audiences(
                database, recent_delivery_job[c.ID], lookalike_auds
            )

        ret_doc = collection.find_one(
            {c.ID: inserted_id, c.DELETED: False}, {c.DELETED: 0}
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return ret_doc


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
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
    platform_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[c.LOOKALIKE_AUDIENCE_COLLECTION]

    try:
        ret_doc = collection.find_one(
            {c.ID: lookalike_audience_id, c.DELETED: False}, {c.DELETED: 0}
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return ret_doc


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_all_delivery_platform_lookalike_audiences(
    database: DatabaseClient,
    filter_dict: dict = None,
    projection: dict = None,
) -> Union[list, None]:
    """A function to get all delivery platform lookalike audience configurations.

    Args:
        database (DatabaseClient): A database client.
        filter_dict (dict): filter dictionary for adding custom filters.
        projection (dict): Dict that specifies which fields to return or not return.

    Returns:
        Union[list, None]: List of all lookalike audience configurations.

    """

    collection = database[c.DATA_MANAGEMENT_DATABASE][
        c.LOOKALIKE_AUDIENCE_COLLECTION
    ]

    # if deleted is not included in the filters, add it.
    if filter_dict:
        filter_dict[c.DELETED] = False
    else:
        filter_dict = {c.DELETED: False}

    # exclude the deleted field from returning
    if projection:
        projection[c.DELETED] = 0
    else:
        projection = {c.DELETED: 0}

    try:
        return list(collection.find(filter_dict, projection))
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
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
    """

    ret_doc = None
    platform_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[c.LOOKALIKE_AUDIENCE_COLLECTION]

    # Make sure the name will be unique
    exists_flag = name_exists(
        database,
        c.DATA_MANAGEMENT_DATABASE,
        c.LOOKALIKE_AUDIENCE_COLLECTION,
        c.LOOKALIKE_AUD_NAME,
        name,
    )

    if exists_flag:
        cur_doc = get_delivery_platform_lookalike_audience(
            database,
            lookalike_audience_id,
        )
        if cur_doc[c.LOOKALIKE_AUD_NAME] != name:
            raise de.DuplicateName(name)

    update_doc = {
        c.LOOKALIKE_AUD_NAME: name,
        c.UPDATE_TIME: datetime.datetime.utcnow(),
    }

    try:
        ret_doc = collection.find_one_and_update(
            {c.ID: lookalike_audience_id, c.DELETED: False},
            {"$set": update_doc},
            upsert=False,
            new=True,
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return ret_doc


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
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
        audience_size_percentage (float): The new size percentage of the lookalike audience.

    Returns:
        Union[dict, None]: The updated lookalike audience configuration.
    """

    ret_doc = None
    platform_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[c.LOOKALIKE_AUDIENCE_COLLECTION]

    update_doc = {
        c.LOOKALIKE_AUD_SIZE_PERCENTAGE: audience_size_percentage,
        c.UPDATE_TIME: datetime.datetime.utcnow(),
    }

    try:
        ret_doc = collection.find_one_and_update(
            {c.ID: lookalike_audience_id, c.DELETED: False},
            {"$set": update_doc},
            upsert=False,
            new=True,
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return ret_doc


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
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
        audience_size_percentage (float): The new size percentage of the lookalike audience.
        country (str): Updated lookalike audience country.
        user_name (str): Username of the user updating the audience.
        audience_size (int): Size of the audience at update time.

    Returns:
        Union[dict, None]: The updated lookalike audience configuration.
    """
    ret_doc = None
    platform_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[c.LOOKALIKE_AUDIENCE_COLLECTION]

    # Make sure the name will be unique
    exists_flag = name_exists(
        database,
        c.DATA_MANAGEMENT_DATABASE,
        c.LOOKALIKE_AUDIENCE_COLLECTION,
        c.LOOKALIKE_AUD_NAME,
        name,
    )

    if exists_flag:
        cur_doc = get_delivery_platform_lookalike_audience(
            database,
            lookalike_audience_id,
        )
        if cur_doc[c.LOOKALIKE_AUD_NAME] != name:
            raise de.DuplicateName(name)

    update_doc = {
        c.LOOKALIKE_AUD_NAME: name,
        c.LOOKALIKE_AUD_COUNTRY: country,
        c.LOOKALIKE_AUD_SIZE_PERCENTAGE: audience_size_percentage,
        c.UPDATE_TIME: datetime.datetime.utcnow(),
        c.UPDATED_BY: user_name,
    }

    if audience_size:
        update_doc[c.SIZE] = audience_size

    for item in list(update_doc):
        if update_doc[item] is None:
            del update_doc[item]

    try:
        if update_doc:
            ret_doc = collection.find_one_and_update(
                {c.ID: lookalike_audience_id, c.DELETED: False},
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
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def set_delivery_job(
    database: DatabaseClient,
    audience_id: ObjectId,
    delivery_platform_id: ObjectId,
    delivery_platform_generic_campaigns: list,
    engagement_id: ObjectId = None,
    delivery_platform_config: dict = None,
) -> Union[dict, None]:
    """A function to set an audience delivery job.

    Args:
        database (DatabaseClient): A database client.
        audience_id (ObjectId): MongoDB ID of the delivered audience.
        delivery_platform_id (ObjectId): Delivery platform ID.
        delivery_platform_generic_campaigns (list): generic campaign IDs.
        engagement_id (ObjectId): Engagement ID.
        delivery_platform_config (dict): the delivery platform config
            object that holds the data extensions
    Returns:
        Union[dict, None]: Delivery job configuration.

    """

    dp_doc = get_delivery_platform(database, delivery_platform_id)

    if dp_doc is None:
        raise de.InvalidID(delivery_platform_id)

    dp_status = get_connection_status(database, delivery_platform_id)

    if dp_status != c.STATUS_SUCCEEDED:
        raise de.NoDeliveryPlatformConnection(delivery_platform_id)

    am_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = am_db[c.DELIVERY_JOBS_COLLECTION]

    curr_time = datetime.datetime.utcnow()

    doc = {
        c.AUDIENCE_ID: audience_id,
        c.CREATE_TIME: curr_time,
        c.UPDATE_TIME: curr_time,
        c.JOB_STATUS: c.AUDIENCE_STATUS_DELIVERING,
        c.DELIVERY_PLATFORM_ID: delivery_platform_id,
        c.DELIVERY_PLATFORM_GENERIC_CAMPAIGNS: (
            delivery_platform_generic_campaigns
        ),
        c.DELETED: False,
        c.DELIVERY_PLATFORM_AUD_SIZE: 0,
    }
    if engagement_id is not None:
        doc[c.ENGAGEMENT_ID] = engagement_id

    if delivery_platform_config is not None:
        doc[c.DELIVERY_PLATFORM_CONFIG] = delivery_platform_config

    try:
        delivery_job_id = collection.insert_one(doc).inserted_id
        collection.create_index(
            [
                (c.AUDIENCE_ID, pymongo.ASCENDING),
                (c.DELIVERY_PLATFORM_ID, pymongo.ASCENDING),
            ]
        )

        if delivery_job_id is not None:
            return collection.find_one(
                {c.ID: delivery_job_id, c.DELETED: False}, {c.DELETED: 0}
            )

    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
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

    am_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = am_db[c.DELIVERY_JOBS_COLLECTION]

    try:
        # set mongo_filter based on engagement id
        mongo_filter = {c.ID: delivery_job_id, c.DELETED: False}
        if engagement_id is not None:
            mongo_filter[c.ENGAGEMENT_ID] = engagement_id

        return collection.find_one(mongo_filter, {c.DELETED: 0})
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_delivery_jobs_using_metadata(
    database: DatabaseClient,
    engagement_id: ObjectId = None,
    audience_id: ObjectId = None,
    delivery_platform_id: ObjectId = None,
) -> Union[list, None]:
    """A function to get delivery jobs based on engagement details.
    Args:
        database (DatabaseClient): A database client.
        engagement_id (ObjectId): Engagement id.
        audience_id (ObjectId): Audience id.
        delivery_platform_id (ObjectId): Delivery platform id.
    Returns:
        Union[list, None]: List of matching delivery jobs, if any.
    """

    if (
        engagement_id is None
        and audience_id is None
        and delivery_platform_id is None
    ):
        raise de.InvalidID()

    am_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = am_db[c.DELIVERY_JOBS_COLLECTION]

    try:

        mongo_filter = {c.DELETED: False}
        if audience_id:
            mongo_filter[c.AUDIENCE_ID] = audience_id
        if engagement_id:
            mongo_filter[c.ENGAGEMENT_ID] = engagement_id
        if delivery_platform_id:
            mongo_filter[c.DELIVERY_PLATFORM_ID] = delivery_platform_id

        return list(collection.find(mongo_filter, {c.DELETED: 0}))
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
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
    am_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = am_db[c.DELIVERY_JOBS_COLLECTION]
    curr_time = datetime.datetime.utcnow()

    update_doc = {}
    update_doc[c.JOB_STATUS] = job_status
    update_doc[c.UPDATE_TIME] = curr_time

    if job_status in (c.AUDIENCE_STATUS_DELIVERED, c.STATUS_FAILED):
        update_doc[c.JOB_END_TIME] = curr_time
    elif job_status == c.AUDIENCE_STATUS_DELIVERING:
        update_doc[c.JOB_START_TIME] = curr_time

    try:
        doc = collection.find_one_and_update(
            {c.ID: delivery_job_id, c.DELETED: False},
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

    if c.JOB_STATUS in doc:
        job_status = doc[c.JOB_STATUS]

    return job_status


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
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
    am_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = am_db[c.DELIVERY_JOBS_COLLECTION]

    # Set update dict
    update_dict = {
        c.DELIVERY_PLATFORM_AUD_SIZE: audience_size,
    }

    # Update the doc.
    try:
        doc = collection.find_one_and_update(
            {c.ID: delivery_job_id, c.DELETED: False},
            {"$set": update_dict},
            upsert=False,
            return_document=pymongo.ReturnDocument.AFTER,
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return doc


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
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
    am_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = am_db[c.DELIVERY_JOBS_COLLECTION]

    # Set update dict
    update_dict = {
        c.DELIVERY_PLATFORM_LOOKALIKE_AUDS: lookalike_audiences,
    }

    # Update the doc.
    try:
        doc = collection.find_one_and_update(
            {c.ID: delivery_job_id, c.DELETED: False},
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

    if c.DELIVERY_PLATFORM_AUD_SIZE in doc:
        audience_size = doc[c.DELIVERY_PLATFORM_AUD_SIZE]

    return audience_size


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
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

    """
    am_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = am_db[c.DELIVERY_JOBS_COLLECTION]

    try:
        mongo_filter = {c.DELETED: False}
        if audience_id:
            mongo_filter[c.AUDIENCE_ID] = audience_id
        if engagement_id:
            mongo_filter[c.ENGAGEMENT_ID] = engagement_id

        cursor = collection.find(
            mongo_filter,
            {c.ENABLED: False} if audience_id else {c.ID: True},
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)
        raise

    return list(cursor)


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
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

    collection = database[c.DATA_MANAGEMENT_DATABASE][
        c.DELIVERY_JOBS_COLLECTION
    ]

    # if deleted is not included in the filters, add it.
    if filter_dict:
        filter_dict[c.DELETED] = False
    else:
        filter_dict = {c.DELETED: False}

    # exclude the deleted field from returning
    if projection:
        projection[c.DELETED] = 0
    else:
        projection = {c.DELETED: 0}

    # if sort list is none, set to default, otherwise set to the passed in list.
    # note, if an empty list is passed in, no sorting will happen.
    sort_list = (
        [(c.CREATE_TIME, pymongo.DESCENDING)]
        if sort_list is None
        else sort_list
    )

    try:
        cursor = collection.find(filter_dict, projection)
        if sort_list:
            cursor = cursor.sort(sort_list)

        # apply limit if set.
        return list(cursor if isinstance(limit, int) else cursor.limit(limit))
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
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
        Union[dict, None]: Most recent delivery job stored associated
        with the audience and delivery platform.
    """

    recent_delivery_job = None
    am_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = am_db[c.DELIVERY_JOBS_COLLECTION]

    # retrieve the delivery jobs associated with the audience
    # and delivery platform
    try:
        cursor = collection.find(
            {
                c.AUDIENCE_ID: audience_id,
                c.DELIVERY_PLATFORM_ID: delivery_platform_id,
                c.DELETED: False,
            },
            {c.DELETED: 0},
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    # get the list of delivery jobs
    delivery_jobs = list(cursor)

    # if delivery jobs were retrieved
    if len(delivery_jobs) > 0:
        # sort the list by the delivery job ID and return the
        # most recent ID
        delivery_jobs.sort(key=itemgetter(c.ID), reverse=True)
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
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
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
    """

    if get_delivery_job(database, delivery_job_id) is None:
        raise de.InvalidID(delivery_job_id)

    platform_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[c.DELIVERY_JOBS_COLLECTION]

    try:
        return collection.find_one_and_update(
            {c.ID: delivery_job_id, c.DELETED: False},
            {
                "$set": {
                    c.DELIVERY_PLATFORM_GENERIC_CAMPAIGNS: generic_campaign
                }
            },
            upsert=False,
            new=True,
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
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

    platform_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[c.DELIVERY_JOBS_COLLECTION]

    try:
        return collection.update_many(
            {c.ID: {"$in": delivery_job_ids}, c.DELETED: False},
            {"$set": {c.DELIVERY_PLATFORM_GENERIC_CAMPAIGNS: []}},
            upsert=False,
        ).modified_count
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return 0


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
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
    platform_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[c.DELIVERY_PLATFORM_COLLECTION]

    update_doc = {
        c.FAVORITE: True,
        c.UPDATE_TIME: datetime.datetime.utcnow(),
    }

    try:
        doc = collection.find_one_and_update(
            {c.ID: delivery_platform_id, c.DELETED: False},
            {"$set": update_doc},
            upsert=False,
            new=True,
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return doc


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
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
    platform_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[c.DELIVERY_PLATFORM_COLLECTION]

    update_doc = {
        c.FAVORITE: False,
        c.UPDATE_TIME: datetime.datetime.utcnow(),
    }

    try:
        doc = collection.find_one_and_update(
            {c.ID: delivery_platform_id, c.DELETED: False},
            {"$set": update_doc},
            upsert=False,
            new=True,
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return doc


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
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
    platform_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[c.LOOKALIKE_AUDIENCE_COLLECTION]

    update_doc = {
        c.FAVORITE: True,
        c.UPDATE_TIME: datetime.datetime.utcnow(),
    }

    try:
        ret_doc = collection.find_one_and_update(
            {c.ID: lookalike_audience_id, c.DELETED: False},
            {"$set": update_doc},
            upsert=False,
            new=True,
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return ret_doc


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
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
    platform_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[c.LOOKALIKE_AUDIENCE_COLLECTION]

    update_doc = {
        c.FAVORITE: False,
        c.UPDATE_TIME: datetime.datetime.utcnow(),
    }

    try:
        ret_doc = collection.find_one_and_update(
            {c.ID: lookalike_audience_id, c.DELETED: False},
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

    """

    am_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = am_db[c.DELIVERY_JOBS_COLLECTION]

    try:
        cursor = collection.find(
            {c.DELIVERY_PLATFORM_ID: delivery_platform_id, c.DELETED: False},
            {c.DELETED: 0},
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
        database, c.DATA_MANAGEMENT_DATABASE, c.DELIVERY_PLATFORM_COLLECTION
    )


def get_lookalike_audiences_count(database: DatabaseClient) -> int:
    """A function to retrieve count of lookalike audiences documents.

    Args:
        database (DatabaseClient): A database client.

    Returns:
        int: Count of lookalike audiences documents.

    """
    return get_collection_count(
        database, c.DATA_MANAGEMENT_DATABASE, c.LOOKALIKE_AUDIENCE_COLLECTION
    )


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def set_performance_metrics(
    database: DatabaseClient,
    delivery_platform_id: ObjectId,
    delivery_platform_type: str,
    delivery_job_id: ObjectId,
    generic_campaigns: list,
    metrics_dict: dict,
    start_time: datetime.datetime,
    end_time: datetime.datetime,
) -> Union[dict, None]:
    """Store campaign performance metrics.

    Args:
        database (DatabaseClient): A database client.
        delivery_platform_id (ObjectId): delivery platform ID
        delivery_platform_type (str): delivery platform type
        delivery_job_id (ObjectId): The delivery job ID of audience.
        generic_campaigns: (dict): generic campaigns
        metrics_dict (dict): A dict containing performance metrics.
        start_time (datetime): Start time of metrics.
        end_time (datetime): End time of metrics.

    Returns:
        Union[dict, None]: MongoDB metrics doc.
    """

    platform_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[c.PERFORMANCE_METRICS_COLLECTION]

    # Check validity of delivery job ID
    if not get_delivery_job(database, delivery_job_id):
        raise de.InvalidID(delivery_job_id)

    # Get current time
    curr_time = datetime.datetime.utcnow()

    doc = {
        c.METRICS_DELIVERY_PLATFORM_ID: delivery_platform_id,
        c.METRICS_DELIVERY_PLATFORM_TYPE: delivery_platform_type,
        c.DELIVERY_JOB_ID: delivery_job_id,
        c.CREATE_TIME: curr_time,
        c.METRICS_START_TIME: start_time,
        c.METRICS_END_TIME: end_time,
        c.DELIVERY_PLATFORM_GENERIC_CAMPAIGNS: generic_campaigns,
        c.PERFORMANCE_METRICS: metrics_dict,
        # By default not transferred for feedback to CDM yet
        c.STATUS_TRANSFERRED_FOR_FEEDBACK: False,
    }

    try:
        metrics_id = collection.insert_one(doc).inserted_id
        collection.create_index([(c.DELIVERY_JOB_ID, pymongo.ASCENDING)])
        if metrics_id:
            return collection.find_one({c.ID: metrics_id})
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_performance_metrics(
    database: DatabaseClient,
    delivery_job_id: ObjectId,
    min_start_time: datetime.datetime = None,
    max_end_time: datetime.datetime = None,
    pending_transfer_for_feedback: bool = False,
) -> Union[list, None]:
    """Retrieve campaign performance metrics.

    Args:
        database (DatabaseClient): database client.
        delivery_job_id (ObjectId): delivery job ID.
        min_start_time (datetime.datetime, optional):
            Min start time of metrics. Defaults to None.
        max_end_time (datetime.datetime, optional):
            Max start time of metrics. Defaults to None.
        pending_transfer_for_feedback (bool): If True, retrieve only
            metrics that have not been transferred for feedback. Defaults to False.

    Raises:
        de.InvalidID: Invalid ID for delivery job.

    Returns:
        Union[list, None]: list of metrics.
    """

    platform_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[c.PERFORMANCE_METRICS_COLLECTION]

    # Check validity of delivery job ID
    doc = get_delivery_job(database, delivery_job_id)
    if not doc:
        raise de.InvalidID(delivery_job_id)

    metric_queries = [{c.DELIVERY_JOB_ID: delivery_job_id}]

    if min_start_time:
        metric_queries.append({c.METRICS_START_TIME: {"$gte": min_start_time}})

    if max_end_time:
        metric_queries.append({c.METRICS_END_TIME: {"$lte": max_end_time}})

    if pending_transfer_for_feedback:
        metric_queries.append(
            {c.STATUS_TRANSFERRED_FOR_FEEDBACK: {"$eq": False}}
        )

    mongo_query = {"$and": metric_queries}

    try:
        cursor = collection.find(mongo_query)
        return list(cursor)
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
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

    Raises:
        de.InvalidID: Invalid ID for engagement.

    Returns:
        Union[list, None]: list of metrics or None
    """

    platform_db = database[c.DATA_MANAGEMENT_DATABASE]

    # Get delivery jobs using engagement id
    collection = platform_db[c.DELIVERY_JOBS_COLLECTION]

    try:
        delivery_jobs = collection.find(
            {
                c.ENGAGEMENT_ID: engagement_id,
                c.DELIVERY_PLATFORM_ID: {"$in": destination_ids},
            }
        )
        # Get performance metrics for all delivery jobs
        collection = platform_db[c.PERFORMANCE_METRICS_COLLECTION]
        delivery_job_ids = [x[c.ID] for x in delivery_jobs]
        return list(
            collection.find({c.DELIVERY_JOB_ID: {"$in": delivery_job_ids}})
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def _set_performance_metrics_status(
    database: DatabaseClient,
    performance_metrics_id: ObjectId,
    performance_metrics_status: str,
) -> Union[dict, None]:
    """Set performance metrics status.

    Args:
        database (DatabaseClient): database client.
        performance_metrics_id (ObjectId): performance metrics ID.
        performance_metrics_status (str): performance metrics status.

    Returns:
        Union[dict, None]: performance metrics document.
    """
    platform_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[c.PERFORMANCE_METRICS_COLLECTION]

    # TODO Below is also designed to accommodate
    # "transferred for reporting" status in the future
    update_doc = {}
    if performance_metrics_status == c.STATUS_TRANSFERRED_FOR_FEEDBACK:
        update_doc.update({c.STATUS_TRANSFERRED_FOR_FEEDBACK: True})

    if update_doc:
        try:
            doc = collection.find_one_and_update(
                {c.ID: performance_metrics_id},
                {"$set": update_doc},
                upsert=False,
                new=True,
            )
            return doc
        except pymongo.errors.OperationFailure as exc:
            logging.error(exc)

    return None


set_transferred_for_feedback = partial(
    _set_performance_metrics_status,
    performance_metrics_status=c.STATUS_TRANSFERRED_FOR_FEEDBACK,
)


def get_all_performance_metrics(
    database: DatabaseClient,
    pending_transfer_for_feedback: bool = False,
) -> Union[list, None]:
    """Retrieve all campaign performance metrics.

    Args:
        database (DatabaseClient): database client.
        pending_transfer_for_feedback (bool): If True, retrieve only
            metrics that have not been transferred for feedback. Defaults to False.

    Returns:
        Union[list, None]: list of performance metrics.
    """

    metric_docs = None

    platform_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[c.PERFORMANCE_METRICS_COLLECTION]
    try:
        if pending_transfer_for_feedback:
            metric_docs = list(
                collection.find(
                    {c.STATUS_TRANSFERRED_FOR_FEEDBACK: {"$eq": False}}
                )
            )
        else:
            metric_docs = list(collection.find())
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return metric_docs


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def set_campaign_activity(
    database: DatabaseClient,
    delivery_platform_id: ObjectId,
    delivery_platform_name: str,
    delivery_job_id: ObjectId,
    generic_campaigns: dict,
    event_details: dict,
) -> Union[dict, None]:
    """Store campaign activity data.

    Args:
        database (DatabaseClient): A database client.
        delivery_platform_id (ObjectId): delivery platform ID
        delivery_platform_name (str): delivery platform name
        delivery_job_id (ObjectId): The delivery job ID of audience.
        generic_campaigns: (dict): generic campaigns
        event_dict (dict): A dict containing campaign activity data.

    Returns:
        Union[dict, None]: Campaign Activity document.
    """

    platform_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[c.CAMPAIGN_ACTIVITY_COLLECTION]

    # Check validity of delivery job ID
    if not get_delivery_job(database, delivery_job_id):
        raise de.InvalidID(delivery_job_id)

    doc = {
        c.METRICS_DELIVERY_PLATFORM_ID: delivery_platform_id,
        c.METRICS_DELIVERY_PLATFORM_NAME: delivery_platform_name,
        c.DELIVERY_JOB_ID: delivery_job_id,
        c.CREATE_TIME: datetime.datetime.utcnow(),
        c.DELIVERY_PLATFORM_GENERIC_CAMPAIGNS: generic_campaigns,
        c.EVENT_DETAILS: event_details,
        # By default not transferred for feedback to CDM yet
        c.STATUS_TRANSFERRED_FOR_FEEDBACK: False,
    }

    try:
        event_doc_id = collection.insert_one(doc).inserted_id
        collection.create_index([(c.DELIVERY_JOB_ID, pymongo.ASCENDING)])
        if event_doc_id:
            return collection.find_one({c.ID: event_doc_id})
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_campaign_activity(
    database: DatabaseClient,
    delivery_job_id: ObjectId,
    pending_transfer_for_feedback: bool = False,
) -> Union[list, None]:
    """Retrieve campaign activity data.

    Args:
        database (DatabaseClient): database client.
        delivery_job_id (ObjectId): delivery job ID.
        pending_transfer_for_feedback (bool): If True, retrieve only
            those campaign activties that have not been transferred for feedback.
            Defaults to False.

    Raises:
        de.InvalidID: Invalid ID for delivery job.

    Returns:
        Union[list, None]: list of campaign activity documents.
    """

    platform_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[c.CAMPAIGN_ACTIVITY_COLLECTION]

    # Check validity of delivery job ID
    if not get_delivery_job(database, delivery_job_id):
        raise de.InvalidID(delivery_job_id)

    event_queries = [{c.DELIVERY_JOB_ID: delivery_job_id}]

    if pending_transfer_for_feedback:
        event_queries.append(
            {c.STATUS_TRANSFERRED_FOR_FEEDBACK: {"$eq": False}}
        )

    try:
        return list(collection.find({"$and": event_queries}))
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def set_campaign_activities(
    database: DatabaseClient,
    campaign_activity_docs: list,
) -> bool:
    """Store many campaign activities data.

    Args:
        database (DatabaseClient): A database client.
        campaign_activity_docs (list): A list containing campaign activity documents.

    Returns:
        bool: Success flag.
    """

    platform_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[c.CAMPAIGN_ACTIVITY_COLLECTION]
    # Insert the batch into the Mongo db
    try:
        collection.insert_many(campaign_activity_docs, ordered=True)
        collection.create_index([(c.DELIVERY_JOB_ID, pymongo.ASCENDING)])
        return True
    except pymongo.errors.BulkWriteError as exc:
        for err in exc.details["writeErrors"]:
            if err["code"] == c.DUPLICATE_ERR_CODE:
                logging.warning(
                    "Ignoring %s due to duplicate unique field!",
                    str(err["op"]),
                )
                continue

            logging.error(exc)
            return False
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)
        return False

    return True


def get_all_feedback_campaign_activities(
    database: DatabaseClient,
) -> Union[list, None]:
    """Retrieve all campaign activities with feedback false.

    Args:
        database (DatabaseClient): database client.

    Returns:
        Union[list, None]: list of campaign activities docs.
    """

    campaign_activities_docs = None

    platform_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[c.CAMPAIGN_ACTIVITY_COLLECTION]
    try:
        campaign_activities_docs = list(
            collection.find(
                {c.STATUS_TRANSFERRED_FOR_FEEDBACK: {"$eq": False}}
            )
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return campaign_activities_docs


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def _set_campaign_activity_feedback_status(
    database: DatabaseClient,
    campaign_activity_id: ObjectId,
    campaign_activity_feedback_status: str,
) -> Union[dict, None]:
    """Set campaign activity feedback status.

    Args:
        database (DatabaseClient): database client.
        campaign_activity_id (ObjectId): campaign activity ID.
        campaign_activity_feedback_status (str): campaign_activity feedback status.

    Returns:
        Union[dict, None]: campaign activitiy document.
    """
    platform_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[c.CAMPAIGN_ACTIVITY_COLLECTION]

    update_doc = {}
    if campaign_activity_feedback_status == c.STATUS_TRANSFERRED_FOR_FEEDBACK:
        update_doc.update({c.STATUS_TRANSFERRED_FOR_FEEDBACK: True})

    if update_doc:
        try:
            doc = collection.find_one_and_update(
                {c.ID: campaign_activity_id},
                {"$set": update_doc},
                upsert=False,
                new=True,
            )
            return doc
        except pymongo.errors.OperationFailure as exc:
            logging.error(exc)

    return None


set_campaign_activity_transferred_for_feedback = partial(
    _set_campaign_activity_feedback_status,
    campaign_activity_feedback_status=c.STATUS_TRANSFERRED_FOR_FEEDBACK,
)


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
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
        customer_list (list): List of customer ID processed during the delivery job.

    Returns:
        Union[dict, None]: MongoDB audience doc or None
    """

    ret_doc = None
    am_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = am_db[c.AUDIENCE_CUSTOMERS_COLLECTION]

    audience_customers_doc = {
        c.DELIVERY_JOB_ID: delivery_job_id,
        c.AUDIENCE_CUSTOMER_LIST: customer_list,
    }

    try:
        audience_customers_doc_id = collection.insert_one(
            audience_customers_doc
        ).inserted_id
        collection.create_index([(c.DELIVERY_JOB_ID, pymongo.ASCENDING)])
        if audience_customers_doc_id is not None:
            ret_doc = collection.find_one({c.ID: audience_customers_doc_id})
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return ret_doc


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_all_audience_customers(
    database: DatabaseClient,
    delivery_job_id: ObjectId,
) -> Union[list, None]:
    """A function to fetch all audience customers docs for a delivery job.

    Args:
        database (DatabaseClient): A database client. Defaults to None.
        delivery_job_id (ObjectId): Delivery job ID.

    Returns:
        Union[list, None]: A list of all audience customers docs or None
    """

    audience_customers_docs = None
    am_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = am_db[c.AUDIENCE_CUSTOMERS_COLLECTION]

    try:
        audience_customers_docs = list(
            collection.find({c.DELIVERY_JOB_ID: delivery_job_id})
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return audience_customers_docs


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def set_performance_metrics_bulk(
    database: DatabaseClient,
    performance_metric_docs: list,
) -> dict:
    """Store bulk performance metrics data.

    Args:
        database (DatabaseClient): A database client.
        performance_metric_docs (list): A list containing performance metrics documents.

    Returns:
        dict: dict containing insert_status & list of inserted ids.
    """

    platform_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[c.PERFORMANCE_METRICS_COLLECTION]

    insert_result = {"insert_status": False}

    try:
        result = collection.insert_many(performance_metric_docs, ordered=True)

        if result.acknowledged:
            insert_result["insert_status"] = True
            insert_result["inserted_ids"] = result.inserted_ids

        collection.create_index([(c.DELIVERY_JOB_ID, pymongo.ASCENDING)])

        return insert_result
    except pymongo.errors.BulkWriteError as exc:
        for err in exc.details["writeErrors"]:
            if err["code"] == c.DUPLICATE_ERR_CODE:
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

    return insert_result


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_most_recent_performance_metric_by_delivery_job(
    database: DatabaseClient,
    delivery_job_id: ObjectId,
) -> Union[dict, None]:
    """Retrieve the most recent campaign performance
    metrics associated with a given delivery job ID.

    Args:
        database (DatabaseClient): database client.
        delivery_job_id (ObjectId): delivery job ID.

    Raises:
        de.InvalidID: Invalid ID for delivery job.

    Returns:
        Union[dict, None]: most recent performance metric.
    """

    platform_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[c.PERFORMANCE_METRICS_COLLECTION]

    # Check validity of delivery job ID
    doc = get_delivery_job(database, delivery_job_id)
    if not doc:
        raise de.InvalidID(delivery_job_id)

    try:
        cursor = list(
            collection.find({c.DELIVERY_JOB_ID: delivery_job_id})
            .sort([(c.JOB_END_TIME, -1)])
            .limit(1)
        )
        if len(cursor) > 0:
            return cursor[0]

    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_most_recent_campaign_activity_by_delivery_job(
    database: DatabaseClient,
    delivery_job_id: ObjectId,
) -> Union[dict, None]:
    """Retrieve the most recent campaign activity
    event associated with a given delivery job ID.

    Args:
        database (DatabaseClient): database client.
        delivery_job_id (ObjectId): delivery job ID.

    Raises:
        de.InvalidID: Invalid ID for delivery job.

    Returns:
        Union[dict, None]: most recent performance metric.
    """

    platform_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[c.CAMPAIGN_ACTIVITY_COLLECTION]

    # Check validity of delivery job ID
    doc = get_delivery_job(database, delivery_job_id)
    if not doc:
        return None

    try:
        cursor = list(
            collection.find({c.DELIVERY_JOB_ID: delivery_job_id})
            .sort([(f"{c.EVENT_DETAILS}.{c.EVENT_DATE}", -1)])
            .limit(1)
        )
        if len(cursor) > 0:
            return cursor[0]

    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None
