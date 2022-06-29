"""This module enables functionality related to data management."""
# pylint: disable=C0302

import logging
import datetime
from typing import Union, Optional
import pandas as pd
from bson import ObjectId
import pymongo
from tenacity import retry, wait_fixed, retry_if_exception_type

import huxunifylib.database.db_exceptions as de
import huxunifylib.database.constants as db_c
from huxunifylib.database.client import DatabaseClient
from huxunifylib.database.utils import name_exists
from huxunifylib.database.audience_data_management_util import (
    add_stats_to_update_dict,
    validate_data_source_fields,
    clean_dataframe_types,
)


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def set_data_source(
    database: DatabaseClient,
    data_source_name: str,
    data_source_type: int,
    data_source_format: str,
    location_type: str,
    location_details: dict,
    fields: list,
) -> Union[dict, None]:
    """A function to set a data source.

    Args:
        database (DatabaseClient): A database client.
        data_source_name (str): Name of data source.
        data_source_type (int): Type of data source.
        data_source_format (str): Format of data source.
        location_type (str): Type of locations (e.g. S3).
        location_details (dict): Details of location (e.g. S3 bucket and key).
        fields (list): A list of fields of data source.

    Returns:
        Union[dict, None]: MongoDB document.

    Raises:
        DuplicateName: Error if a data source with the same data_source_name
            exists already.
    """

    data_source_doc = None
    data_source_id = None
    dm_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    collection = dm_db[db_c.DATA_SOURCES_COLLECTION]

    # Validate fields
    if fields:
        validate_data_source_fields(fields)

    # Get current time
    curr_time = datetime.datetime.utcnow()

    doc = {
        db_c.DATA_SOURCE_NAME: data_source_name,
        db_c.DATA_SOURCE_TYPE: data_source_type,
        db_c.DATA_SOURCE_FORMAT: data_source_format,
        db_c.DATA_SOURCE_LOCATION_TYPE: location_type,
        db_c.DATA_SOURCE_LOCATION_DETAILS: location_details,
        db_c.DATA_SOURCE_FIELDS: fields,
        db_c.DATA_SOURCE_NON_BREAKDOWN_FIELDS: [],
        db_c.ENABLED: True,
        db_c.CREATE_TIME: curr_time,
        db_c.UPDATE_TIME: curr_time,
        db_c.FAVORITE: False,
        db_c.DELETED: False,
    }

    exists_flag = name_exists(
        database,
        db_c.DATA_MANAGEMENT_DATABASE,
        db_c.DATA_SOURCES_COLLECTION,
        db_c.DATA_SOURCE_NAME,
        data_source_name,
    )

    if exists_flag:
        raise de.DuplicateName(data_source_name)

    try:
        data_source_id = collection.insert_one(doc).inserted_id
        if data_source_id is not None:
            data_source_doc = collection.find_one(
                {db_c.ID: data_source_id, db_c.DELETED: False},
                {db_c.DELETED: 0},
            )
        else:
            logging.error("Failed to create a new data source!")
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return data_source_doc


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_data_source(
    database: DatabaseClient, data_source_id: ObjectId
) -> Union[dict, None]:
    """A function to get a data source.

    Args:
        database (DatabaseClient): A database client.
        data_source_id (ObjectId): MongoDB document ID of data source.

    Returns:
        Union[dict, None]: Data source configuration.
    """

    doc = None
    dm_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    collection = dm_db[db_c.DATA_SOURCES_COLLECTION]

    try:
        doc = collection.find_one(
            {db_c.ID: data_source_id, db_c.DELETED: False}, {db_c.DELETED: 0}
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return doc


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_all_data_sources(database: DatabaseClient) -> list:
    """A function to get all data source configurations.

    Args:
        database (DatabaseClient): A database client.

    Returns:
        list: List of all data source configurations.
    """

    dm_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    collection = dm_db[db_c.DATA_SOURCES_COLLECTION]

    try:
        docs = list(collection.find({db_c.DELETED: False}, {db_c.DELETED: 0}))
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return docs


def get_data_source_non_breakdown_fields(
    database: DatabaseClient,
    data_source_id: ObjectId,
) -> list:
    """A function to get a list of non breakdown fields of a data source.

    Args:
        database (DatabaseClient): A database client.
        data_source_id (ObjectId): MongoDB ID of data source.

    Returns:
        list: A list of no breakdown fields.
    """

    # Get the current no breakdown list
    cur_doc = get_data_source(database, data_source_id)

    non_breakdown_fields = []
    if (
        cur_doc is not None
        and db_c.DATA_SOURCE_NON_BREAKDOWN_FIELDS in cur_doc
    ):
        non_breakdown_fields = cur_doc[db_c.DATA_SOURCE_NON_BREAKDOWN_FIELDS]

    return non_breakdown_fields


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def update_data_source_param(
    database: DatabaseClient,
    data_source_id: ObjectId,
    param_name: str,
    param_value: Union[str, dict, list, bool],
) -> Union[dict, None]:
    """A function to update a data source parameter.

    Args:
        database (DatabaseClient): A database client.
        data_source_id (ObjectId): MongoDB ID of data source.
        param_name (str): Name of the parameter.
        param_value (Union[str, dict, list])): Updated value of the parameter.

    Returns:
        Union[dict, None]: Updated data source configuration.

    Raises:
        DataSourceLocked: Error if the data source is not mutable and is not
            allowed to be updated.
    """

    doc = None
    dm_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    collection = dm_db[db_c.DATA_SOURCES_COLLECTION]

    allowed_fields = [
        db_c.DATA_SOURCE_RECENT_JOB_ID,
        db_c.DATA_SOURCE_NON_BREAKDOWN_FIELDS,
        db_c.RECENT_INGESTION_JOB_STATUS,
        db_c.FAVORITE,
        db_c.ENABLED,
    ]

    # Do not update if data source is associated to an ingestion job
    mutable = is_data_source_mutable(database, data_source_id)

    if not mutable and param_name not in allowed_fields:
        raise de.DataSourceLocked(data_source_id)

    update_doc = {
        param_name: param_value,
        db_c.UPDATE_TIME: datetime.datetime.utcnow(),
    }

    try:
        doc = collection.find_one_and_update(
            {db_c.ID: data_source_id, db_c.DELETED: False},
            {"$set": update_doc},
            upsert=False,
            return_document=pymongo.ReturnDocument.AFTER,
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return doc


def update_data_source_name(
    database: DatabaseClient,
    data_source_id: ObjectId,
    name: str,
) -> Union[dict, None]:
    """A function to update data source name.

    Args:
        database (DatabaseClient): A database client.
        data_source_id (ObjectId): MongoDB ID of data source.
        name (str): New name of the data source.

    Returns:
        Union[dict, None]: Updated data source configuration.

    Raises:
        DuplicateName: Error if a data source with the same data_source_name
            exists already.
    """

    # Make sure the name will be unique
    exists_flag = name_exists(
        database,
        db_c.DATA_MANAGEMENT_DATABASE,
        db_c.DATA_SOURCES_COLLECTION,
        db_c.DATA_SOURCE_NAME,
        name,
    )

    if exists_flag:
        cur_doc = get_data_source(database, data_source_id)

        if cur_doc[db_c.DATA_SOURCE_NAME] != name:
            raise de.DuplicateName(name)

    return update_data_source_param(
        database,
        data_source_id,
        db_c.DATA_SOURCE_NAME,
        name,
    )


def update_data_source_format(
    database: DatabaseClient,
    data_source_id: ObjectId,
    data_source_format: str,
) -> Union[dict, None]:
    """A function to update data source format.

    Args:
        database (DatabaseClient): A database client.
        data_source_id (ObjectId): MongoDB ID of data source.
        data_source_format (str): New data source format.

    Returns:
        Union[dict, None]: Updated data source configuration.
    """

    return update_data_source_param(
        database,
        data_source_id,
        db_c.DATA_SOURCE_FORMAT,
        data_source_format,
    )


def update_data_source_location_type(
    database: DatabaseClient,
    data_source_id: ObjectId,
    location_type: str,
) -> Union[dict, None]:
    """A function to update data source location type.

    Args:
        database (DatabaseClient): A database client.
        data_source_id (ObjectId): MongoDB ID of data source.
        location_type (str): New data source location type.

    Returns:
        Union[dict, None]: Updated data source configuration.
    """

    return update_data_source_param(
        database,
        data_source_id,
        db_c.DATA_SOURCE_LOCATION_TYPE,
        location_type,
    )


def update_data_source_location_details(
    database: DatabaseClient,
    data_source_id: ObjectId,
    location_details: dict,
) -> Union[dict, None]:
    """A function to update data source location details.

    Args:
        database (DatabaseClient): A database client.
        data_source_id (ObjectId): MongoDB ID of data source.
        location_details (dict): New data source location details.

    Returns:
        Union[dict, None]: Updated data source configuration.
    """

    return update_data_source_param(
        database,
        data_source_id,
        db_c.DATA_SOURCE_LOCATION_DETAILS,
        location_details,
    )


def update_data_source_fields(
    database: DatabaseClient,
    data_source_id: ObjectId,
    fields: list,
) -> Union[dict, None]:
    """A function to update data source fields.

    Args:
        database (DatabaseClient): A database client.
        data_source_id (ObjectId): MongoDB ID of data source.
        fields (list): New data source fields.

    Returns:
        Union[dict, None]: Updated data source configuration.
    """

    # Validate fields
    if fields:
        validate_data_source_fields(fields)

    return update_data_source_param(
        database,
        data_source_id,
        db_c.DATA_SOURCE_FIELDS,
        fields,
    )


def update_data_source_recent_ingestion_job_id(
    database: DatabaseClient,
    data_source_id: ObjectId,
    recent_ingestion_job_id: ObjectId,
) -> Union[dict, None]:
    """A function to update data source recent ingestion job ID.

    Args:
        database (DatabaseClient): A database client.
        data_source_id (ObjectId): MongoDB ID of data source.
        recent_ingestion_job_id (ObjectId): MongoDB ID of the most recent
            ingestion job.

    Returns:
        Union[dict, None]: Updated data source configuration.
    """

    return update_data_source_param(
        database,
        data_source_id,
        db_c.DATA_SOURCE_RECENT_JOB_ID,
        recent_ingestion_job_id,
    )


def update_data_source_recent_ingestion_job_status(
    database: DatabaseClient,
    data_source_id: ObjectId,
    recent_ingestion_job_status: str,
) -> Union[dict, None]:
    """A function to update the status of a data source's
    most recent ingestion job.

    Args:
        database (DatabaseClient): A database client.
        data_source_id (ObjectId): MongoDB ID of data source.
        recent_ingestion_job_status (str): Status of the  most recent ingestion
            job.

    Returns:
        Union[dict, None]: Updated data source configuration.
    """

    return update_data_source_param(
        database,
        data_source_id,
        db_c.RECENT_INGESTION_JOB_STATUS,
        recent_ingestion_job_status,
    )


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def update_data_source_non_breakdown_fields(
    database: DatabaseClient,
    data_source_id: ObjectId,
    non_breakdown_fields: list,
) -> Union[dict, None]:
    """A function to update non breakdown fields for a data source.

    Args:
        database (DatabaseClient): A database client.
        data_source_id (ObjectId): MongoDB ID of data source.
        non_breakdown_fields (list): List of non breakdown fields.

    Returns:
        Union[dict, None]: Updated data source configuration.
    """

    return update_data_source_param(
        database,
        data_source_id,
        db_c.DATA_SOURCE_NON_BREAKDOWN_FIELDS,
        non_breakdown_fields,
    )


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def update_data_source(
    database: DatabaseClient,
    data_source_id: ObjectId,
    name: str = None,
    data_source_format: str = None,
    location_type: str = None,
    location_details: dict = None,
    fields: list = None,
) -> Union[dict, None]:
    """A function to update data source configuration.

    Args:
        database (DatabaseClient): A database client.
        data_source_id (ObjectId): MongoDB ID of data source.
        name (str): Updated name for the data source.
        data_source_format (str): Updated data source format.
        location_type (str): Updated data source location type.
        location_details (dict): Updated data source location details.
        fields (list): Updated data source field definition.

    Returns:
        Union[dict, None]: Updated data source configuration.

    Raises:
        DuplicateName: Error if a data source with the same data_source_name
            exists already.
        DataSourceLocked: Error if the data source is not mutable and is not
            allowed to be updated.
        NoUpdatesSpecified: Error if no updates were done to the data source.
    """

    doc = None
    dm_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    collection = dm_db[db_c.DATA_SOURCES_COLLECTION]

    # Validate fields
    if fields:
        validate_data_source_fields(fields)

    # Make sure the name will be unique
    if name_exists(
        database,
        db_c.DATA_MANAGEMENT_DATABASE,
        db_c.DATA_SOURCES_COLLECTION,
        db_c.DATA_SOURCE_NAME,
        name,
    ):
        cur_doc = get_data_source(database, data_source_id)
        if cur_doc[db_c.DATA_SOURCE_NAME] != name:
            raise de.DuplicateName(name)

    # Do not update if data source is associated to an ingestion job
    if not is_data_source_mutable(database, data_source_id):
        raise de.DataSourceLocked(data_source_id)

    update_doc = {
        db_c.DATA_SOURCE_NAME: name,
        db_c.DATA_SOURCE_FORMAT: data_source_format,
        db_c.DATA_SOURCE_LOCATION_TYPE: location_type,
        db_c.DATA_SOURCE_LOCATION_DETAILS: location_details,
        db_c.DATA_SOURCE_FIELDS: fields,
        db_c.UPDATE_TIME: datetime.datetime.utcnow(),
    }

    for item in list(update_doc):
        if update_doc[item] is None:
            del update_doc[item]

    try:
        if update_doc:
            doc = collection.find_one_and_update(
                {db_c.ID: data_source_id, db_c.DELETED: False},
                {"$set": update_doc},
                upsert=False,
                return_document=pymongo.ReturnDocument.AFTER,
            )
        else:
            raise de.NoUpdatesSpecified("data source")
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return doc


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def set_ingestion_job(
    database: DatabaseClient, data_source_id: ObjectId
) -> Union[dict, None]:
    """A function to set an ingestion job.

    Args:
        database (DatabaseClient): A database client.
        data_source_id (ObjectId): MongoDB document ID of data source.

    Returns:
        Union[dict, None]: Ingestion job configuration.
    """

    ingestion_job_doc = None
    ingestion_job_id = None
    dm_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    collection = dm_db[db_c.INGESTION_JOBS_COLLECTION]

    curr_time = datetime.datetime.utcnow()

    doc = {
        db_c.DATA_SOURCE_ID: data_source_id,
        db_c.CREATE_TIME: curr_time,
        db_c.UPDATE_TIME: curr_time,
        db_c.JOB_STATUS: db_c.STATUS_PENDING,
        db_c.STATUS_MESSAGE: "",
        db_c.DELETED: False,
    }

    try:
        ingestion_job_id = collection.insert_one(doc).inserted_id
        collection.create_index([(db_c.DATA_SOURCE_ID, pymongo.ASCENDING)])
        if ingestion_job_id is not None:
            ingestion_job_doc = collection.find_one(
                {db_c.ID: ingestion_job_id, db_c.DELETED: False},
                {db_c.DELETED: 0},
            )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    # Update recent ingestion job info of the data source
    if ingestion_job_id is not None:
        doc = update_data_source_recent_ingestion_job_id(
            database,
            data_source_id,
            ingestion_job_id,
        )

        update_data_source_recent_ingestion_job_status(
            database=database,
            data_source_id=data_source_id,
            recent_ingestion_job_status=ingestion_job_doc[db_c.JOB_STATUS],
        )

    return ingestion_job_doc


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_ingestion_job(
    database: DatabaseClient, ingestion_job_id: ObjectId
) -> dict:
    """A function to get an ingestion job.

    Args:
        database (DatabaseClient): A database client.
        ingestion_job_id (ObjectId): Ingestion job id.

    Returns:
        dict: Ingestion job configuration.
    """

    dm_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    collection = dm_db[db_c.INGESTION_JOBS_COLLECTION]

    try:
        doc = collection.find_one(
            {db_c.ID: ingestion_job_id, db_c.DELETED: False}, {db_c.DELETED: 0}
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return doc


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_data_source_ingestion_jobs(
    database: DatabaseClient, data_source_id: ObjectId
) -> list:
    """A function to get all ingestion jobs associated with a data source.

    Args:
        database (DatabaseClient): A database client.
        data_source_id (ObjectId): MongoDB ID of data source.

    Returns:
        list: List of corresponding ingestion job configurations.
    """

    dm_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    collection = dm_db[db_c.INGESTION_JOBS_COLLECTION]

    try:
        docs = list(
            collection.find(
                {db_c.DATA_SOURCE_ID: data_source_id, db_c.DELETED: False},
                {db_c.DELETED: 0},
            )
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return docs


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def is_data_source_mutable(
    database: DatabaseClient, data_source_id: ObjectId
) -> bool:
    """Determine if a data source us mutable.

    Args:
        database (DatabaseClient): A database client.
        data_source_id (ObjectId): MongoDB ID of data source.

    Returns:
        bool: A flag indicating that the data source is mutable.
    """

    dm_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    collection = dm_db[db_c.INGESTION_JOBS_COLLECTION]
    count = 0
    mutable = True

    try:
        count = collection.count_documents(
            {
                db_c.DATA_SOURCE_ID: data_source_id,
                db_c.ENABLED: True,
                db_c.JOB_STATUS: {"$ne": db_c.STATUS_FAILED},
            },
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    if count > 0:
        mutable = False

    return mutable


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def set_ingestion_job_status_no_default_audience(
    database: DatabaseClient,
    ingestion_job_id: ObjectId,
    job_status: str,
    status_msg: str,
) -> Union[dict, None]:

    """Set ingestion job status, but do not create default adience when
    ingestion job succeeded.

    Args:
        database (DatabaseClient): A database client.
        ingestion_job_id (ObjectId): MongoDB document ID of ingestion job.
        job_status (str): Status of ingestion job. Can be Pending,
            In Progress, Failed, or Succeeded.
        status_msg (str): Additional details related to the current job status.

    Returns:
        Union[dict, None]: Updated ingestion job configuration.
    """

    doc = None
    dm_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    collection = dm_db[db_c.INGESTION_JOBS_COLLECTION]
    curr_time = datetime.datetime.utcnow()

    # Update ingestion job
    update_dict = {}
    update_dict[db_c.UPDATE_TIME] = curr_time

    if job_status == db_c.AUDIENCE_STATUS_DELIVERING:
        update_dict[db_c.JOB_START_TIME] = curr_time
    elif job_status in (db_c.STATUS_SUCCEEDED, db_c.STATUS_FAILED):
        update_dict[db_c.JOB_END_TIME] = curr_time

    update_dict[db_c.JOB_STATUS] = job_status

    update_dict[db_c.STATUS_MESSAGE] = status_msg

    data_source_id = get_ingestion_job(
        database,
        ingestion_job_id,
    )[db_c.DATA_SOURCE_ID]

    recent_ingestion_job_id = get_data_source_recent_ingestion_job_id(
        database, data_source_id
    )

    if ingestion_job_id == recent_ingestion_job_id:
        update_data_source_recent_ingestion_job_status(
            database=database,
            data_source_id=data_source_id,
            recent_ingestion_job_status=job_status,
        )

    try:
        doc = collection.find_one_and_update(
            {db_c.ID: ingestion_job_id, db_c.DELETED: False},
            {"$set": update_dict},
            upsert=False,
            new=True,
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return doc


def get_ingestion_job_status(
    database: DatabaseClient, ingestion_job_id: ObjectId
) -> tuple:
    """A function to get an ingestion job status.

    Args:
        database (DatabaseClient): A database client.
        ingestion_job_id (ObjectId): MongoDB document ID of ingestion job.

    Returns:
        tuple: A tuple containing the status of the ingestion job and status
            message. Status can be Pending, In Progress, Failed, or Succeeded.
    """

    doc = get_ingestion_job(database, ingestion_job_id)

    return (doc.get(db_c.JOB_STATUS), doc.get(db_c.STATUS_MESSAGE))


def get_ingestion_job_data_source_fields(
    database: DatabaseClient,
    ingestion_job_id: ObjectId,
) -> list:
    """A function to get ingestion job data source fields.

    Args:
        database (DatabaseClient): A database client.
        ingestion_job_id (ObjectId): The MongoDB ID of the ingestion job.

    Returns:
        list: A list of field names of the data source.
    """

    data_source_id = None
    data_source_fields = []
    fields_list = []

    job_doc = get_ingestion_job(database, ingestion_job_id)

    if job_doc is not None and db_c.DATA_SOURCE_ID in job_doc:
        data_source_id = job_doc[db_c.DATA_SOURCE_ID]

    if data_source_id is not None:
        data_source_doc = get_data_source(database, data_source_id)

    if (
        data_source_doc is not None
        and db_c.DATA_SOURCE_FIELDS in data_source_doc
    ):
        fields_list = data_source_doc[db_c.DATA_SOURCE_FIELDS]

    for field_doc in fields_list:
        if (
            db_c.FIELD_SPECIAL_TYPE in field_doc
            and field_doc[db_c.FIELD_SPECIAL_TYPE] is not None
        ):
            data_source_fields.append(field_doc[db_c.FIELD_SPECIAL_TYPE])
        elif db_c.FIELD_HEADER in field_doc:
            data_source_fields.append(field_doc[db_c.FIELD_HEADER])

    return data_source_fields


def get_ingestion_job_custom_fields(
    database: DatabaseClient,
    ingestion_job_id: ObjectId,
) -> list:
    """A function to get a list of custom fields of a ingestion job.

    Args:
        database (DatabaseClient): A database client.
        ingestion_job_id (ObjectId): MongoDB ID of data source.

    Returns:
        list: A list of custom fields.
    """

    data_source_id = None
    fields_list = []
    custom_fields = []

    job_doc = get_ingestion_job(database, ingestion_job_id)

    if job_doc is not None and db_c.DATA_SOURCE_ID in job_doc:
        data_source_id = job_doc[db_c.DATA_SOURCE_ID]

    if data_source_id is not None:
        data_source_doc = get_data_source(database, data_source_id)

    if (
        data_source_doc is not None
        and db_c.DATA_SOURCE_FIELDS in data_source_doc
    ):
        fields_list = data_source_doc[db_c.DATA_SOURCE_FIELDS]

    for field_doc in fields_list:
        if field_doc.get(db_c.FIELD_SPECIAL_TYPE) is None:
            custom_fields.append(field_doc[db_c.FIELD_HEADER])

    return custom_fields


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def append_ingested_data(
    database: DatabaseClient,
    ingestion_job_id: ObjectId,
    ingested_data: pd.DataFrame,
) -> bool:
    """A function to store ingested data.

    Args:
        database (DatabaseClient): A database client.
        ingestion_job_id (ObjectId): MongoDB document ID of ingestion job.
        ingested_data (pd.DataFrame): Ingested data in Pandas DataFrame format.

    Returns:
        bool: Success flag.
    """

    ingested_data = clean_dataframe_types(ingested_data)

    dm_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    collection = dm_db[db_c.INGESTED_DATA_COLLECTION]

    # Add internal customer IDs
    if db_c.S_TYPE_CUSTOMER_ID not in ingested_data.columns:
        ingested_data[db_c.S_TYPE_CUSTOMER_ID] = None

    ingested_data[db_c.S_TYPE_CUSTOMER_ID] = ingested_data[
        db_c.S_TYPE_CUSTOMER_ID
    ].apply(lambda x: ObjectId() if x is None else x)

    # Add docs to the batch
    batch_docs = []
    for _, row_item in ingested_data.iterrows():
        batch_docs.append(
            {
                db_c.JOB_ID: ingestion_job_id,
                db_c.INGESTED_DATA: dict(row_item),
            }
        )

    # Insert the batch into the Mongo db
    try:
        # Create a unique compound index on ingestion_job_id and nested field
        # ingested_data.customer_id
        field_str = f"{db_c.INGESTED_DATA}.{db_c.S_TYPE_CUSTOMER_ID}"
        collection.create_index(
            [(field_str, pymongo.ASCENDING), (db_c.JOB_ID, pymongo.ASCENDING)],
            unique=True,
        )
        collection.insert_many(batch_docs, ordered=False)
        collection.create_index([(db_c.JOB_ID, pymongo.ASCENDING)])
        return True
    except pymongo.errors.BulkWriteError as exc:
        for err in exc.details["writeErrors"]:
            if err["code"] == db_c.DUPLICATE_ERR_CODE:
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


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_ingested_data_stats(
    database: DatabaseClient, ingestion_job_id: ObjectId
) -> dict:
    """A function to get data statistics based on the corresponding ingestion
    job.

    Args:
        database (DatabaseClient): A database client.
        ingestion_job_id (ObjectId): MongoDB document ID of ingestion job.

    Returns:
        dict: Stored data statistics.
    """

    dm_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    collection = dm_db[db_c.INGESTED_DATA_STATS_COLLECTION]

    try:
        doc = collection.find_one(
            {db_c.JOB_ID: ingestion_job_id, db_c.DELETED: False},
            {db_c.DELETED: 0},
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return doc


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def append_ingested_data_stats(
    database: DatabaseClient,
    ingestion_job_id: ObjectId,
    ingested_data: pd.DataFrame,
    custom_breakdown_fields: list = None,
) -> dict:
    """A function to store ingested data statistics.

    Args:
        database (DatabaseClient): A database client.
        ingestion_job_id (ObjectId): MongoDB document ID of ingestion job.
        ingested_data (pd.DataFrame): Ingested data in Pandas DataFrame format.
        custom_breakdown_fields (list): A list of custom field names for which
            breakdowns should be calculated.

    Returns:
        dict: Stats MongoDB doc.
    """

    dm_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    collection = dm_db[db_c.INGESTED_DATA_STATS_COLLECTION]

    # Get the existing doc (if applicable)
    old_stats_doc = get_ingested_data_stats(database, ingestion_job_id)

    # Initialize update dict
    update_dict = {
        db_c.JOB_ID: ingestion_job_id,
    }

    # Get ingestion job data source fields
    data_source_fields = get_ingestion_job_data_source_fields(
        database, ingestion_job_id
    )

    # Get the intersection with what is available in the inbgested data
    ingested_data_fields = []

    for field_name in ingested_data.columns:
        if field_name not in data_source_fields:
            continue
        ingested_data_fields.append(field_name)

    # Add statistics to update dict
    update_dict = add_stats_to_update_dict(
        update_dict,
        ingested_data[ingested_data_fields],
        old_stats_doc,
        custom_breakdown_fields,
    )

    # Update the doc. If no doc exists, a new doc will be created.
    try:
        doc = collection.find_one_and_update(
            {db_c.JOB_ID: ingestion_job_id, db_c.DELETED: False},
            {"$set": update_dict},
            upsert=True,
            return_document=pymongo.ReturnDocument.AFTER,
        )
        collection.create_index([(db_c.JOB_ID, pymongo.ASCENDING)])
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return doc


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_all_data_source_ids(
    database: DatabaseClient,
) -> Union[list, None]:
    """A function to get all existing data source IDs.

    Args:
        database (DatabaseClient): A database client.

    Returns:
        Union[list, None]: A list of all data source ids or None.
    """

    dm_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    collection = dm_db[db_c.DATA_SOURCES_COLLECTION]
    all_data_source_ids = None

    # Read all data source ids
    try:
        cursor = collection.find({db_c.ENABLED: True}, {db_c.ID: True})
        all_data_source_ids = [doc[db_c.ID] for doc in cursor]
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return all_data_source_ids


def get_data_source_recent_ingestion_job_id(
    database: DatabaseClient,
    data_source_id: ObjectId,
) -> Optional[ObjectId]:
    """A function to get the most recent ingestion job ID of a data source.

    Args:
        database (DatabaseClient): A database client.
        data_source_id (ObjectId): MongoDB document ID of data source.

    Returns:
        ObjectId: The ID of the most recent ingestion job.
    """

    job_id = None

    doc = get_data_source(database, data_source_id)

    if db_c.DATA_SOURCE_RECENT_JOB_ID in doc:
        job_id = doc[db_c.DATA_SOURCE_RECENT_JOB_ID]

    return job_id


def favorite_data_source(
    database: DatabaseClient,
    data_source_id: ObjectId,
) -> Union[dict, None]:
    """A function to favorite a data source.

    Args:
        database (DatabaseClient): A database client.
        data_source_id (ObjectId): MongoDB ID of data source.

    Returns:
        Union[dict, None]: Updated data source configuration.
    """

    return update_data_source_param(
        database,
        data_source_id,
        db_c.FAVORITE,
        True,
    )


def unfavorite_data_source(
    database: DatabaseClient,
    data_source_id: ObjectId,
) -> Union[dict, None]:
    """A function to unfavorite a data source.

    Args:
        database (DatabaseClient): A database client.
        data_source_id (ObjectId): MongoDB ID of data source.

    Returns:
        Union[dict, None]: Updated data source configuration.
    """

    return update_data_source_param(
        database,
        data_source_id,
        db_c.FAVORITE,
        False,
    )


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_data_sources_count(database: DatabaseClient) -> int:
    """A function to retrieve count of data sources documents.

    Args:
        database (DatabaseClient): A database client.

    Returns:
        int: Count of data sources documents.
    """

    dm_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    collection = dm_db[db_c.DATA_SOURCES_COLLECTION]
    count = 0

    try:
        count = collection.count_documents(
            {
                db_c.ENABLED: True,
            }
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return count
