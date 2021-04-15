"""This module enables functionality related to delivery platform management."""
# pylint: disable=C0302

import logging
import datetime
from operator import itemgetter
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
def get_delivery_platform(
    database: DatabaseClient,
    delivery_platform_id: ObjectId,
) -> dict:
    """A function to get a delivery platform.

    Args:
        database (DatabaseClient): A database client.
        delivery_platform_id (ObjectId): The MongoDB ID of the delivery platform.

    Returns:
        dict: Delivery platform configuration.
    """

    doc = None
    platform_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[c.DELIVERY_PLATFORM_COLLECTION]

    try:
        doc = collection.find_one(
            {c.ID: delivery_platform_id, c.ENABLED: True}, {c.ENABLED: 0}
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return doc


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def set_delivery_platform(
    database: DatabaseClient,
    delivery_platform_type: str,
    name: str,
    authentication_details: dict,
    user: str = None,
) -> dict:
    """A function to create a delivery platform.

    Args:
        database (DatabaseClient): A database client.
        delivery_platform_type (str): The type of delivery platform (Facebook, Amazon, or Google).
        name (str): Name of the delivery platform.
        user (str): User object ID or email.
        authentication_details (dict): A dict containing delivery platform authentication details.

    Returns:
        dict: MongoDB audience doc.
    """

    if delivery_platform_type not in [
        c.DELIVERY_PLATFORM_FACEBOOK,
        c.DELIVERY_PLATFORM_AMAZON,
        c.DELIVERY_PLATFORM_GOOGLE,
        c.DELIVERY_PLATFORM_SFMC,
    ]:
        raise de.UnknownDeliveryPlatformType(delivery_platform_type)

    delivery_platform_doc = None
    delivery_platform_id = None
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

    # Get current time
    curr_time = datetime.datetime.utcnow()

    doc = {
        c.DELIVERY_PLATFORM_TYPE: delivery_platform_type,
        c.DELIVERY_PLATFORM_NAME: name,
        c.DELIVERY_PLATFORM_STATUS: c.STATUS_PENDING,
        c.DELIVERY_PLATFORM_AUTH: authentication_details,
        c.ENABLED: True,
        c.CREATE_TIME: curr_time,
        c.UPDATE_TIME: curr_time,
        c.FAVORITE: False,
    }

    # Add user object only if it is available
    if user is not None:
        doc[c.CREATED_BY] = user
        doc[c.UPDATED_BY]: user

    try:
        delivery_platform_id = collection.insert_one(doc).inserted_id
        if delivery_platform_id is not None:
            delivery_platform_doc = collection.find_one(
                {c.ID: delivery_platform_id, c.ENABLED: True},
                {c.ENABLED: 0},
            )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return delivery_platform_doc


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_all_delivery_platforms(
    database: DatabaseClient,
) -> list:
    """A function to get all configured delivery platforms.

    Args:
        database (DatabaseClient): A database client.

    Returns:
        List: A list of all delivery platform configuration dicts.
    """

    doc = None
    platform_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[c.DELIVERY_PLATFORM_COLLECTION]

    try:
        doc = list(collection.find({c.ENABLED: True}, {c.ENABLED: 0}))
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
) -> dict:

    """A function to set the status of connection to a delivery platform.

    Args:
        database (DatabaseClient): A database client.
        delivery_platform_id (ObjectId): MongoDB document ID of delivery platform.
        connection_status: Status of connection to delivery platform. Can be Pending,
            In progress, Failed, or Succeeded.

    Returns:
        dict: Updated delivery platform configuration.
    """

    doc = None
    platform_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[c.DELIVERY_PLATFORM_COLLECTION]

    update_doc = {}
    update_doc[c.DELIVERY_PLATFORM_STATUS] = connection_status
    update_doc[c.UPDATE_TIME] = datetime.datetime.utcnow()

    try:
        doc = collection.find_one_and_update(
            {c.ID: delivery_platform_id, c.ENABLED: True},
            {"$set": update_doc},
            upsert=False,
            new=True,
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return doc


def get_connection_status(
    database: DatabaseClient, delivery_platform_id: ObjectId
) -> str:
    """A function to get status of connection to delivery platform.

    Args:
        database (DatabaseClient): A database client.
        delivery_platform_id (ObjectId): MongoDB document ID of delivery
          platform.

    Returns:
        str: Status of delivery platform connection. Can be Pending,
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
) -> dict:
    """A function to set delivery platform authentication details.

    Args:
        database (DatabaseClient): A database client.
        delivery_platform_id (ObjectId): The MongoDB ID of delivery platform.
        authentication_details (dict): A dict containing delivery platform authentication details.

    Returns:
        dict: Updated delivery platform configuration.
    """

    doc = None
    platform_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[c.DELIVERY_PLATFORM_COLLECTION]

    update_doc = {}
    update_doc[c.DELIVERY_PLATFORM_AUTH] = authentication_details
    update_doc[c.UPDATE_TIME] = datetime.datetime.utcnow()

    try:
        doc = collection.find_one_and_update(
            {c.ID: delivery_platform_id, c.ENABLED: True},
            {"$set": update_doc},
            upsert=False,
            new=True,
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return doc


def get_authentication_details(
    database: DatabaseClient, delivery_platform_id: ObjectId
) -> dict:
    """A function to get authentication details of a delivery platform.

    Args:
        database (DatabaseClient): A database client.
        delivery_platform_id (ObjectId): MongoDB document ID of delivery
          platform.

    Returns:
        dict: Delivery authentication details.
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
) -> dict:
    """A function to set delivery platform name.

    Args:
        database (DatabaseClient): A database client.
        delivery_platform_id (ObjectId): The MongoDB ID of delivery platform.
        name (str): Delivery platform name.

    Returns:
        dict: Updated delivery platform configuration.
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
            {c.ID: delivery_platform_id, c.ENABLED: True},
            {"$set": update_doc},
            upsert=False,
            new=True,
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return doc


def get_name(database: DatabaseClient, delivery_platform_id: ObjectId) -> str:
    """A function to get name of a delivery platform.

    Args:
        database (DatabaseClient): A database client.
        delivery_platform_id (ObjectId): MongoDB document ID of delivery
          platform.

    Returns:
        str: Delivery platform name.
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
) -> dict:
    """A function to set delivery platform type.

    Args:
        database (DatabaseClient): A database client.
        delivery_platform_id (ObjectId): The MongoDB ID of delivery platform.
        delivery_platform_type (str): Delivery platform type.

    Returns:
        dict: Updated delivery platform configuration.
    """

    if delivery_platform_type not in [
        c.DELIVERY_PLATFORM_FACEBOOK,
        c.DELIVERY_PLATFORM_AMAZON,
        c.DELIVERY_PLATFORM_GOOGLE,
        c.DELIVERY_PLATFORM_SFMC,
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
            {c.ID: delivery_platform_id, c.ENABLED: True},
            {"$set": update_doc},
            upsert=False,
            new=True,
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return doc


def get_platform_type(
    database: DatabaseClient, delivery_platform_id: ObjectId
) -> str:
    """A function to get the delivery platform type.

    Args:
        database (DatabaseClient): A database client.
        delivery_platform_id (ObjectId): MongoDB document ID of delivery
          platform.

    Returns:
        str: Delivery platform type.
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
def update_delivery_platform(
    database: DatabaseClient,
    delivery_platform_id: ObjectId,
    name: str = None,
    delivery_platform_type: str = None,
    authentication_details: dict = None,
) -> dict:
    """A function to update delivery platform configuration.

    Args:
        database (DatabaseClient): A database client.
        delivery_platform_id (ObjectId): The MongoDB ID of delivery platform.
        name (str): Delivery platform name.
        delivery_platform_type (str): Delivery platform type.
        authentication_details (dict): A dict containing delivery platform authentication details.

    Returns:
        dict: Updated delivery platform configuration.
    """

    if delivery_platform_type not in [
        c.DELIVERY_PLATFORM_FACEBOOK,
        c.DELIVERY_PLATFORM_AMAZON,
        c.DELIVERY_PLATFORM_GOOGLE,
        c.DELIVERY_PLATFORM_SFMC,
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

    for item in list(update_doc):
        if update_doc[item] is None:
            del update_doc[item]

    try:
        if update_doc:
            doc = collection.find_one_and_update(
                {c.ID: delivery_platform_id, c.ENABLED: True},
                {"$set": update_doc},
                upsert=False,
                new=True,
            )
        else:
            raise de.NoUpdatesSpecified("delivery platform")

    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return doc


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
) -> dict:
    """A function to create a delivery platform lookalike audience.

    Args:
        database (DatabaseClient): A database client.
        delivery_platform_id (ObjectId): The Mongo ID of delivery platform.
        source_audience_id (ObjectId): The Mongo ID of source audience.
        name (str): Name of the lookalike audience.
        audience_size_percentage (float): Size percentage of the lookalike audience.
        country (str): Country of the lookalike audience.

    Returns:
        dict: The lookalike audience configuration.
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
        c.ENABLED: True,
        c.CREATE_TIME: curr_time,
        c.UPDATE_TIME: curr_time,
        c.FAVORITE: False,
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
            {c.ID: inserted_id, c.ENABLED: True}, {c.ENABLED: 0}
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
) -> dict:
    """A function to get a delivery platform lookalike audience.

    Args:
        database (DatabaseClient): A database client.
        lookalike_audience_id (ObjectId): The Mongo ID of lookalike audience.

    Returns:
        dict: The lookalike audience configuration.
    """

    ret_doc = None
    platform_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[c.LOOKALIKE_AUDIENCE_COLLECTION]

    try:
        ret_doc = collection.find_one(
            {c.ID: lookalike_audience_id, c.ENABLED: True}, {c.ENABLED: 0}
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
) -> list:
    """A function to get all delivery platform lookalike audience configurations.

    Args:
        database (DatabaseClient): A database client.

    Returns:
        list: List of all lookalike audience configurations.

    """

    ret_docs = None
    platform_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[c.LOOKALIKE_AUDIENCE_COLLECTION]

    try:
        ret_docs = list(collection.find({c.ENABLED: True}, {c.ENABLED: 0}))
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return ret_docs


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def update_lookalike_audience_name(
    database: DatabaseClient,
    lookalike_audience_id: ObjectId,
    name: str,
) -> dict:
    """A function to update a delivery platform lookalike audience name.

    Args:
        database (DatabaseClient): A database client.
        lookalike_audience_id (ObjectId): The Mongo ID of lookalike audience.
        name (str): The new name of the lookalike audience.

    Returns:
        dict: The updated lookalike audience configuration.
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
            {c.ID: lookalike_audience_id, c.ENABLED: True},
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
) -> dict:
    """A function to update lookalike audience size percentage.

    Args:
        database (DatabaseClient): A database client.
        lookalike_audience_id (ObjectId): The Mongo ID of lookalike audience.
        audience_size_percentage (float): The new size percentage of the lookalike audience.

    Returns:
        dict: The updated lookalike audience configuration.
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
            {c.ID: lookalike_audience_id, c.ENABLED: True},
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
) -> dict:
    """A function to update lookalike audience.

    Args:
        database (DatabaseClient): A database client.
        lookalike_audience_id (ObjectId): The Mongo ID of lookalike audience.
        name (str): The new name of the lookalike audience.
        audience_size_percentage (float): The new size percentage of the lookalike audience.
        country (str): Updated lookalike audience country.

    Returns:
        dict: The updated lookalike audience configuration.
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
    }

    for item in list(update_doc):
        if update_doc[item] is None:
            del update_doc[item]

    try:
        if update_doc:
            ret_doc = collection.find_one_and_update(
                {c.ID: lookalike_audience_id, c.ENABLED: True},
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
) -> dict:
    """A function to set an audience delivery job.

    Args:
        database (DatabaseClient): A database client.
        audience_id (ObjectId): MongoDB ID of the delivered audience.
        delivery_platform_id (ObjectId): Delivery platform ID.

    Returns:
        dict: Delivery job configuration.

    """

    delivery_job_doc = None
    delivery_job_id = None

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
        c.JOB_STATUS: c.STATUS_PENDING,
        c.DELIVERY_PLATFORM_ID: delivery_platform_id,
        c.ENABLED: True,
    }

    try:
        delivery_job_id = collection.insert_one(doc).inserted_id
        collection.create_index(
            [
                (c.AUDIENCE_ID, pymongo.ASCENDING),
                (c.DELIVERY_PLATFORM_ID, pymongo.ASCENDING),
            ]
        )

        if delivery_job_id is not None:
            delivery_job_doc = collection.find_one(
                {c.ID: delivery_job_id, c.ENABLED: True}, {c.ENABLED: 0}
            )

    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return delivery_job_doc


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_delivery_job(
    database: DatabaseClient, delivery_job_id: ObjectId
) -> dict:
    """A function to get an audience delivery job.

    Args:
        database (DatabaseClient): A database client.
        delivery_job_id (ObjectId): Delivery job id.

    Returns:
        dict: Delivery job configuration.

    """

    am_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = am_db[c.DELIVERY_JOBS_COLLECTION]

    try:
        doc = collection.find_one(
            {c.ID: delivery_job_id, c.ENABLED: True}, {c.ENABLED: 0}
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return doc


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def set_delivery_job_status(
    database: DatabaseClient, delivery_job_id: ObjectId, job_status: str
) -> dict:
    """A function to set an delivery job status.

    Args:
        database (DatabaseClient): A database client.
        delivery_job_id (ObjectId): MongoDB document ID of delivery job.
        job_status: Status of delivery job. Can be Pending,
            In Progress, Failed, or Succeeded.

    Returns:
        dict: Updated delivery job configuration.
    """

    doc = None
    am_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = am_db[c.DELIVERY_JOBS_COLLECTION]
    curr_time = datetime.datetime.utcnow()

    update_doc = {}
    update_doc[c.JOB_STATUS] = job_status
    update_doc[c.UPDATE_TIME] = curr_time

    if job_status in (c.STATUS_SUCCEEDED, c.STATUS_FAILED):
        update_doc[c.JOB_END_TIME] = curr_time
    elif job_status == c.STATUS_IN_PROGRESS:
        update_doc[c.JOB_START_TIME] = curr_time

    try:
        doc = collection.find_one_and_update(
            {c.ID: delivery_job_id, c.ENABLED: True},
            {"$set": update_doc},
            upsert=False,
            new=True,
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return doc


def get_delivery_job_status(
    database: DatabaseClient, delivery_job_id: ObjectId
) -> str:
    """A function to get an delivery job status.

    Args:
        database (DatabaseClient): A database client.
        delivery_job_id (ObjectId): MongoDB document ID of delivery
          job.

    Returns:
        str: Status of delivery job. Can be Pending,
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
) -> dict:
    """A function to store delivery job audience size.

    Args:
        database (DatabaseClient): A database client.
        delivery_job_id (ObjectId): The Mongo DB ID of the delivery job.
        audience_size (int): Size of audience in delivery platform.

    Returns:
        dict: Stored delivery job configuration.

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
            {c.ID: delivery_job_id, c.ENABLED: True},
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
) -> dict:
    """A function to store delivery job lookalike audiences.

    Args:
        database (DatabaseClient): A database client.
        delivery_job_id (ObjectId): The Mongo DB ID of the delivery job.
        lookalike_audiences (list): List of lookalike audiences.

    Returns:
        dict: Stored delivery job configuration.

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
            {c.ID: delivery_job_id, c.ENABLED: True},
            {"$set": update_dict},
            upsert=False,
            return_document=pymongo.ReturnDocument.AFTER,
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return doc


def get_delivery_job_audience_size(
    database: DatabaseClient, delivery_job_id: ObjectId
) -> int:
    """A function to get delivery job audience size.

    Args:
        database (DatabaseClient): A database client.
        delivery_job_id (ObjectId): MongoDB document ID of delivery job.

    Returns:
        int: Delivery platform audience size.

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
def get_audience_delivery_jobs(
    database: DatabaseClient, audience_id: ObjectId
) -> list:
    """A function to get all audience delivery jobs given an audience.

    Args:
        database (DatabaseClient): A database client.
        audience_id (ObjectId): Audience id.

    Returns:
        list: List of delivery jobs for an audience.

    """

    am_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = am_db[c.DELIVERY_JOBS_COLLECTION]

    try:
        cursor = collection.find(
            {c.AUDIENCE_ID: audience_id, c.ENABLED: True}, {c.ENABLED: 0}
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return list(cursor)


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_audience_recent_delivery_job(
    database: DatabaseClient,
    audience_id: ObjectId,
    delivery_platform_id: ObjectId,
) -> dict:
    """A function to get the most recent delivery job associated with
    a given audience and delivery platform.

    Args:
        database (DatabaseClient): A database client.
        audience_id (ObjectId): The MongoDB ID of an audience.
        delivery_platform_id (ObjectId): The MongoDB ID of a delivery platform.

    Returns:
        dict: Most recent delivery job stored associated with the audience and
            delivery platform.
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
                c.ENABLED: True,
            },
            {c.ENABLED: 0},
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

    if audience_ids is not None:
        for audience_id in audience_ids:
            delivery_jobs = get_audience_delivery_jobs(
                database,
                audience_id,
            )
            if delivery_jobs is not None:
                all_delivery_jobs += delivery_jobs

    return all_delivery_jobs


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def favorite_delivery_platform(
    database: DatabaseClient,
    delivery_platform_id: ObjectId,
) -> dict:
    """A function to favorite a delivery platform.

    Args:
        database (DatabaseClient): A database client.
        delivery_platform_id (ObjectId): The ID of delivery platform.

    Returns:
        dict: Updated delivery platform configuration.
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
            {c.ID: delivery_platform_id, c.ENABLED: True},
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
) -> dict:
    """A function to unfavorite a delivery platform.

    Args:
        database (DatabaseClient): A database client.
        delivery_platform_id (ObjectId): The ID of delivery platform.

    Returns:
        dict: Updated delivery platform configuration.
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
            {c.ID: delivery_platform_id, c.ENABLED: True},
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
) -> dict:
    """A function to favorite a delivery platform lookalike audience.

    Args:
        database (DatabaseClient): A database client.
        lookalike_audience_id (ObjectId): The ID of lookalike audience.

    Returns:
        dict: The updated lookalike audience configuration.
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
            {c.ID: lookalike_audience_id, c.ENABLED: True},
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
) -> dict:
    """A function to unfavorite a delivery platform lookalike audience.

    Args:
        database (DatabaseClient): A database client.
        lookalike_audience_id (ObjectId): The ID of lookalike audience.

    Returns:
        dict: The updated lookalike audience configuration.
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
            {c.ID: lookalike_audience_id, c.ENABLED: True},
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
            {c.DELIVERY_PLATFORM_ID: delivery_platform_id, c.ENABLED: True},
            {c.ENABLED: 0},
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
def set_delivered_audience_performance_metrics(
    database: DatabaseClient,
    delivery_job_id: ObjectId,
    delivery_platform_campaign_id: str,
    delivery_platform_ad_set_id: str,
    metrics_dict: dict,
    start_time: datetime.datetime,
    end_time: datetime.datetime,
) -> dict:
    """A function to store the delivered audience performance metrics.

    Args:
        database (DatabaseClient): A database client.
        delivery_job_id (ObjectId): The delivery job ID of audience.
        delivery_platform_campaign_id (str): ID of corresponding campaign on delivery platform.
        delivery_ad_set_id (str): ID of corresponding ad set on delivery platform.
        metrics_dict (dict): A dict containing performance metrics.
        start_time (datetime): Start time of metrics.
        end_time (datetime): End time of metrics.

    Returns:
        dict: MongoDB metrics doc.
    """

    metrics_doc = None
    platform_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[c.PERFORMANCE_METRICS_COLLECTION]

    # Check validity of delivery job ID
    doc = get_delivery_job(database, delivery_job_id)

    if doc is None:
        raise de.InvalidID(delivery_job_id)

    # Get current time
    curr_time = datetime.datetime.utcnow()

    doc = {
        c.DELIVERY_JOB_ID: delivery_job_id,
        c.DELIVERY_PLATFORM_CAMPAIGN_ID: delivery_platform_campaign_id,
        c.DELIVERY_PLATFORM_AD_SET_ID: delivery_platform_ad_set_id,
        c.CREATE_TIME: curr_time,
        c.METRICS_START_TIME: start_time,
        c.METRICS_END_TIME: end_time,
        c.PERFORMANCE_METRICS: metrics_dict,
    }

    try:
        metrics_id = collection.insert_one(doc).inserted_id
        collection.create_index([(c.DELIVERY_JOB_ID, pymongo.ASCENDING)])
        if metrics_id is not None:
            metrics_doc = collection.find_one({c.ID: metrics_id})
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return metrics_doc


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_delivered_audience_performance_metrics(
    database: DatabaseClient,
    delivery_job_id: ObjectId,
    min_start_time: datetime.datetime = None,
    max_end_time: datetime.datetime = None,
) -> list:
    """A function to get the delivered audience performance metrics.

    Args:
        database (DatabaseClient): A database client.
        delivery_job_id (ObjectId): The delivery job ID of audience.
        min_start_time (datetime): Min start time of metrics.
        max_end_time (datetime): Max end time of metrics.

    Returns:
        list: A list of metrics.
    """

    metrics_list = None
    platform_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[c.PERFORMANCE_METRICS_COLLECTION]

    # Check validity of delivery job ID
    doc = get_delivery_job(database, delivery_job_id)

    if doc is None:
        raise de.InvalidID(delivery_job_id)

    metric_queries = [{c.DELIVERY_JOB_ID: delivery_job_id}]

    if min_start_time is not None:
        metric_queries.append({c.METRICS_START_TIME: {"$gte": min_start_time}})

    if max_end_time is not None:
        metric_queries.append({c.METRICS_END_TIME: {"$lte": max_end_time}})

    mongo_query = {"$and": metric_queries}

    try:
        cursor = collection.find(mongo_query)
        metrics_list = list(cursor)
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return metrics_list
