"""This module enables functionality related to audience management."""
# pylint: disable=C0302

import time
import logging
import datetime
from collections import defaultdict
from typing import Tuple, Generator, Union
import pandas as pd
from bson import ObjectId
import pymongo
from tenacity import retry, wait_fixed, retry_if_exception_type

import huxunifylib.database.db_exceptions as de
import huxunifylib.database.constants as c
import huxunifylib.database.data_management as dm
from huxunifylib.database.client import DatabaseClient
from huxunifylib.database.audience_data_management_util import (
    add_stats_to_update_dict,
    audience_name_exists,
    update_audience_doc,
)
from huxunifylib.database.utils import get_collection_count


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def create_audience(
    database: DatabaseClient,
    name: str,
    audience_filters: list,
    ingestion_job_id: ObjectId = None,
) -> Union[dict, None]:
    """A function to create and store audience rules.

    Args:
        database (DatabaseClient): A database client. Defaults to None.
        name (str): Name of the audience.
        audience_filters (list): List if audience filters.
        ingestion_job_id (ObjectId, optional): Mongo DB ID of the
            corresponding ingestion job. Defaults to None.

    Returns:
        Union[dict, None]: MongoDB audience doc or None

    Raises:
        DuplicateName: Error if an audience with the same name exists
            already.
        InvalidID: If the passed in ingestion_job_id did not fetch a doc from
            the relevant db collection.
    """

    ret_doc = None
    audience_id = None
    am_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = am_db[c.AUDIENCES_COLLECTION]

    # Make sure the name will be unique
    exists_flag = audience_name_exists(
        database,
        name,
    )

    if exists_flag:
        raise de.DuplicateName(name)

    # Validate ingestion job id
    doc = None
    if ingestion_job_id:
        doc = dm.get_ingestion_job(database, ingestion_job_id)

    if ingestion_job_id and doc is None:
        raise de.InvalidID(ingestion_job_id)

    # Get current time
    curr_time = datetime.datetime.utcnow()

    audience_doc = {
        c.AUDIENCE_NAME: name,
        c.AUDIENCE_FILTERS: audience_filters,
        c.ENABLED: True,
        c.CREATE_TIME: curr_time,
        c.UPDATE_TIME: curr_time,
        c.FAVORITE: False,
        c.DELETED: False,
    }

    if ingestion_job_id:
        audience_doc[c.JOB_ID] = ingestion_job_id

    try:
        audience_id = collection.insert_one(audience_doc).inserted_id
        collection.create_index([(c.JOB_ID, pymongo.ASCENDING)])
        if audience_id is not None:
            ret_doc = collection.find_one(
                {c.ID: audience_id, c.DELETED: False}, {c.DELETED: 0}
            )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return ret_doc


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
# pylint: disable=R0914
def get_ingested_data(
    database: DatabaseClient,
    query: dict,
    batch_size: int = 1000,
) -> Tuple[pd.DataFrame, ObjectId]:
    """A function to get ingested data given a query (filters).

    Args:
        database (DatabaseClient): A database client.
        query (dict): A query containing audience filters.
        batch_size (int): Batch size.

    Returns:
        Tuple[pd.DataFrame, ObjectId]:  A tuple of ingested data in
            Pandas format and next_start_id.

    Raises:
        OperationFailure: If an exception occurs during mongo operation.
    """

    # Get a cursor of ingested data
    dm_db = database[c.DATA_MANAGEMENT_DATABASE]
    data_collection = dm_db[c.INGESTED_DATA_COLLECTION]
    data_dict = defaultdict(list)
    next_start_id = None

    # TODO - per Greg Ronin, future we improve it to be a generator to avoid start_id
    #  and next_start_id. Maybe we need a ticket to evaluate that.

    # Read the audience documents and build a dict
    try:
        cursor = (
            data_collection.find(
                query,
                batch_size=batch_size,
            )
            .sort(c.ID, 1)
            .limit(batch_size)
        )

        data_cols = []
        for count, item in enumerate(cursor):
            ingested_data = item[c.INGESTED_DATA]

            for name in data_cols:
                data_dict[name].append(ingested_data.get(name))

            new_cols = list(set(ingested_data.keys()) - set(data_cols))
            for name in new_cols:
                data_dict[name] += count * [None] + [ingested_data[name]]

            data_cols += new_cols
            next_start_id = item[c.ID]

    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)
        raise

    # Build a data frame
    audience_data = pd.DataFrame(data_dict)

    return (audience_data, next_start_id)


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
# pylint: disable=R0912,R0914,R0915
def get_audience(
    database: DatabaseClient,
    audience_id: ObjectId,
    start_id: ObjectId = None,
    batch_size: int = 1000,
) -> Tuple[pd.DataFrame, ObjectId]:
    """A function to get an audience.

    Args:
        database (DatabaseClient): A database client.
        audience_id (ObjectId): The Mongo DB ID of the audience.
        start_id (ObjectId): The start ID of the batch.
        batch_size (int): Batch size.

    Returns:
        Tuple[pd.DataFrame, ObjectId]:  A tuple of audience data in
            Pandas format and next_start_id.

    Raises:
        InvalidID: If the passed in audience_id did not fetch a doc from the
            relevant db collection.
        IncorrectFilterValue: If the filters associated with the audience doc
            has incorrect filters.
    """

    # TODO - per Greg Ronin, future we improve it to be a generator to avoid start_id
    #  and next_start_id. Maybe we need a ticket to evaluate that.

    doc = None
    am_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = am_db[c.AUDIENCES_COLLECTION]

    # Read the audience document which contains filtering rules
    try:
        doc = collection.find_one({c.ID: audience_id, c.DELETED: False})
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    if doc is None:
        raise de.InvalidID(audience_id)

    # Get ingestion job ID and filters associated with the audience
    ingestion_job_id = doc[c.JOB_ID]
    audience_filters = doc.get(c.AUDIENCE_FILTERS, [])

    # Initialize queries list
    filter_queries = [{c.JOB_ID: ingestion_job_id}]

    # Apply start_id is not None
    if start_id is not None and ObjectId.is_valid(start_id):
        filter_queries.append({c.ID: {"$gt": start_id}})

    # Loop through the filters and apply them
    for item in audience_filters:
        if c.AUDIENCE_FILTER_FIELD not in item.keys():
            logging.error(
                "Expected %s in audience filter! Skipping the filter!",
                c.AUDIENCE_FILTER_FIELD,
            )
            continue

        if c.AUDIENCE_FILTER_TYPE not in item.keys():
            logging.error(
                "Expected %s in audience filter! Skipping the filter!",
                c.AUDIENCE_FILTER_TYPE,
            )
            continue

        if c.AUDIENCE_FILTER_VALUE not in item.keys():
            logging.error(
                "Expected %s in audience filter! Skipping the filter!",
                c.AUDIENCE_FILTER_VALUE,
            )
            continue

        filter_type = item[c.AUDIENCE_FILTER_TYPE]
        filter_field = f"{c.INGESTED_DATA}.{item[c.AUDIENCE_FILTER_FIELD]}"

        filter_value = item[c.AUDIENCE_FILTER_VALUE]

        if filter_type in [c.AUDIENCE_FILTER_MIN, c.AUDIENCE_FILTER_MAX]:
            if not isinstance(filter_value, (float, int)):
                raise de.IncorrectFilterValue(filter_type, filter_value)
        elif filter_type in [
            c.AUDIENCE_FILTER_INCLUDE,
            c.AUDIENCE_FILTER_EXCLUDE,
        ]:

            if not isinstance(filter_value, list):
                filter_value = [filter_value]
        elif filter_type == c.AUDIENCE_FILTER_EXISTS:
            if not isinstance(filter_value, bool):
                raise de.IncorrectFilterValue(filter_type, filter_value)

        if filter_type == c.AUDIENCE_FILTER_MIN:
            filter_queries.append({filter_field: {"$gte": filter_value}})
        elif filter_type == c.AUDIENCE_FILTER_MAX:
            filter_queries.append({filter_field: {"$lte": filter_value}})
        elif filter_type == c.AUDIENCE_FILTER_INCLUDE:
            filter_queries.append({filter_field: {"$in": filter_value}})
        elif filter_type == c.AUDIENCE_FILTER_EXCLUDE:
            filter_queries.append({filter_field: {"$nin": filter_value}})
        elif filter_type == c.AUDIENCE_FILTER_EXISTS:
            # If the field exists AND the field values is not None
            if filter_value:
                filter_queries.append(
                    {
                        "$and": [
                            {filter_field: {"$exists": True}},
                            {filter_field: {"$ne": None}},
                        ]
                    }
                )
            # If the field doesn't exist OR the field values is None
            else:
                filter_queries.append(
                    {
                        "$or": [
                            {filter_field: {"$exists": False}},
                            {filter_field: {"$eq": None}},
                        ]
                    }
                )
        else:
            logging.warning(
                "Unknown audience filter type %s! Skipping the filter",
                filter_type,
            )
            continue

    # Build mongo query by applying AND between the queries
    mongo_query = {"$and": filter_queries}

    # Get the ingested data in data frame format
    audience_data, next_start_id = get_ingested_data(
        database, mongo_query, batch_size
    )

    return (audience_data, next_start_id)


def get_audience_batches(
    database: DatabaseClient,
    audience_id: ObjectId,
    batch_size: int = 1000,
) -> Generator[pd.DataFrame, None, None]:
    """A function to get batches of audience data.

    Args:
        database (DatabaseClient): A database client.
        audience_id (ObjectId): The Mongo DB ID of the audience.
        batch_size (int): Batch size.

    Yields:
        Generator[pd.DataFrame, None, None]: A generator of audience data in
            pandas format.
    """

    start_id = None

    while True:

        audience_data_batch, start_id = get_audience(
            database, audience_id, start_id, batch_size
        )

        if start_id is None:
            break

        yield audience_data_batch


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_audience_config(
    database: DatabaseClient,
    audience_id: ObjectId,
) -> Union[dict, None]:
    """A function to get an audience configuration.

    Args:
        database (DatabaseClient): A database client.
        audience_id (ObjectId): The Mongo DB ID of the audience.

    Returns:
        Union[dict, None]: Configuration of the audience in Mongo DB or None.
    """

    doc = None
    am_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = am_db[c.AUDIENCES_COLLECTION]

    try:
        doc = collection.find_one(
            {c.ID: audience_id, c.DELETED: False}, {c.DELETED: 0}
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return doc


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_audience_insights(
    database: DatabaseClient, audience_id: ObjectId
) -> dict:
    """A function to get audience statistics based on audience id.

    Args:
        database (DatabaseClient): A database client.
        audience_id (ObjectId): MongoDB document ID of audience.

    Returns:
        dict: Stored audience insights.
    """

    dm_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = dm_db[c.AUDIENCE_INSIGHTS_COLLECTION]

    try:
        doc = collection.find_one({c.AUDIENCE_ID: audience_id})
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return doc


def get_audience_data_source_id(
    database: DatabaseClient,
    audience_id: ObjectId,
) -> ObjectId:
    """A function to get data source ID of an audience.

    Args:
        database (DatabaseClient): A database client.
        audience_id (ObjectId): MongoDB document ID of audience.

    Returns:
        ObjectId: MongoDB ID of data source.
    """

    data_source_id = None
    audience_doc = None
    ingestion_job_doc = None

    audience_doc = get_audience_config(
        database,
        audience_id,
    )

    if audience_doc is not None:
        ingestion_job_doc = dm.get_ingestion_job(
            database,
            audience_doc[c.JOB_ID],
        )

    if ingestion_job_doc is not None:
        data_source_id = ingestion_job_doc[c.DATA_SOURCE_ID]

    return data_source_id


def get_audience_non_breakdown_fields(
    database: DatabaseClient,
    audience_id: ObjectId,
) -> Union[list, None]:
    """A function to get non breakdown fields of an audience.

    Args:
        database (DatabaseClient): A database client.
        audience_id (ObjectId): MongoDB document ID of audience.

    Returns:
        Union[list,None]: A list of non breakdown fields or None.
    """

    non_breakdown_fields = None

    # Get data source ID
    data_source_id = get_audience_data_source_id(
        database,
        audience_id,
    )

    # Get existing non breakdown fields
    if data_source_id is not None:
        non_breakdown_fields = dm.get_data_source_non_breakdown_fields(
            database,
            data_source_id,
        )

    return non_breakdown_fields


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def append_audience_insights(
    database: DatabaseClient,
    audience_id: ObjectId,
    audience_data: pd.DataFrame,
    custom_breakdown_fields: list = None,
) -> Union[dict, None]:
    """A function to create insights for an audience.

    Args:
        database (DatabaseClient): A database client.
        audience_id (ObjectId): The Mongo DB ID of the audience.
        audience_data (pd.DataFrame): Audience data in Pandas DataFrame format.
        custom_breakdown_fields (list): A list of custom field names for which
            breakdowns should be calculated.

    Returns:
        Union[dict, None]: Stored audience insights or None.
    """

    beg_time = time.time()

    doc = None
    dm_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = dm_db[c.AUDIENCE_INSIGHTS_COLLECTION]

    # Get the existing doc (if applicable)
    old_insights_doc = get_audience_insights(database, audience_id)

    # Initialize update dict
    update_dict = {
        c.AUDIENCE_ID: audience_id,
    }

    # Add insights to update dict
    update_dict = add_stats_to_update_dict(
        update_dict,
        audience_data,
        old_insights_doc,
        custom_breakdown_fields,
    )

    # Update the doc. If no doc exists, a new doc will be created.
    try:
        doc = collection.find_one_and_update(
            {c.AUDIENCE_ID: audience_id},
            {"$set": update_dict},
            upsert=True,
            return_document=pymongo.ReturnDocument.AFTER,
        )
        collection.create_index([(c.AUDIENCE_ID, pymongo.ASCENDING)])
        tot_time = time.time() - beg_time
        logging.info(
            "Appending insights for %d records took %0.2f seconds",
            audience_data.shape[0],
            tot_time,
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return doc


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def delete_audience_insights(
    database: DatabaseClient,
    audience_id: ObjectId,
) -> bool:
    """A function to delete an audience's insights.

    Args:
        database (DatabaseClient): A database client.
        audience_id (ObjectId): The Mongo DB ID of the audience.

    Returns:
        bool: A flag indicating successful deletion.
    """

    success_flag = False
    am_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = am_db[c.AUDIENCE_INSIGHTS_COLLECTION]

    try:
        collection.delete_one({c.AUDIENCE_ID: audience_id})
        success_flag = True
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return success_flag


def refresh_audience_insights(
    database: DatabaseClient,
    audience_id: ObjectId,
    batch_size: int = 1000,
    custom_breakdown_fields: list = None,
) -> Union[dict, None]:
    """A function to refresh an audience's insights.

    Args:
        database (DatabaseClient): A database client.
        audience_id (ObjectId): The Mongo DB ID of the audience.
        batch_size (int): Batch size.
        custom_breakdown_fields (list): A list of custom field names for which
            breakdowns should be calculated.

    Returns:
        Union[dict, None]: Refreshed audience insights or None.
    """

    doc = None
    success_flag = False

    success_flag = delete_audience_insights(
        database,
        audience_id,
    )

    if success_flag:
        data_batches = get_audience_batches(
            database,
            audience_id,
            batch_size,
        )

        for audience_data in data_batches:
            doc = append_audience_insights(
                database,
                audience_id,
                audience_data,
                custom_breakdown_fields,
            )

    return doc


def get_audience_name(
    database: DatabaseClient,
    audience_id: ObjectId,
) -> Union[str, None]:
    """A function to get an audience name.

    Args:
        database (DatabaseClient): A database client.
        audience_id (ObjectId): The Mongo DB ID of the audience.

    Returns:
        Union[str,None]: Name of the audience in Mongo DB or None.
    """

    audience_name = None

    doc = get_audience_config(database, audience_id)

    if doc is not None and c.AUDIENCE_NAME in doc:
        audience_name = doc[c.AUDIENCE_NAME]

    return audience_name


def update_audience_name(
    database: DatabaseClient,
    audience_id: ObjectId,
    name: str,
) -> dict:
    """A function to update an audience name.

    Args:
        database (DatabaseClient): A database client.
        audience_id (ObjectId): MongoDB ID of the audience.
        name (str): New audience name.

    Returns:
        dict: Updated audience configuration dict.

    Raises:
        DuplicateName: Error if an audience with the same name exists
            already.
    """

    exists_flag = audience_name_exists(
        database,
        name,
    )

    if exists_flag:
        cur_doc = get_audience_config(database, audience_id)
        if cur_doc[c.AUDIENCE_NAME] == name:
            raise de.DuplicateName(name)

    # Update dict
    update_dict = {
        c.AUDIENCE_NAME: name,
        c.UPDATE_TIME: datetime.datetime.utcnow(),
    }

    return update_audience_doc(database, audience_id, update_dict)


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def update_audience_filters(
    database: DatabaseClient,
    audience_id: ObjectId,
    audience_filters: list,
    batch_size: int = 1000,
    custom_breakdown_fields: list = None,
) -> Union[dict, None]:
    """A function to update an audience filters.

    Args:
        database (DatabaseClient): A database client.
        audience_id (ObjectId): MongoDB ID of the audience.
        audience_filters (list): List if audience filters.
        batch_size (int): Batch size.
        custom_breakdown_fields (list): A list of custom field names for which
            breakdowns should be calculated.

    Returns:
        Union[dict, None]: Updated audience configuration dict or None.
    """

    doc = None
    am_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = am_db[c.AUDIENCES_COLLECTION]

    # Update dict
    update_dict = {
        c.AUDIENCE_FILTERS: audience_filters,
        c.UPDATE_TIME: datetime.datetime.utcnow(),
    }

    # Update the doc.
    try:
        doc = collection.find_one_and_update(
            {c.ID: audience_id, c.DELETED: False},
            {"$set": update_dict},
            {c.DELETED: 0},
            upsert=False,
            return_document=pymongo.ReturnDocument.AFTER,
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    # Update audience insights
    refresh_audience_insights(
        database,
        audience_id,
        batch_size,
        custom_breakdown_fields,
    )

    return doc


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_ingestion_job_audience_ids(
    database: DatabaseClient,
    ingestion_job_id: ObjectId,
) -> list:
    """A function to get the IDs of all audiences given an ingestion job.

    Args:
        database (DatabaseClient): A database client.
        ingestion_job_id (ObjectId): The Mongo DB ID of the ingestion job.

    Returns:
        list: A list of audience IDs.

    Raises:
        OperationFailure: If an exception occurs during mongo operation.
    """

    am_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = am_db[c.AUDIENCES_COLLECTION]

    # Read the audience documents
    try:
        cursor = collection.find(
            {c.JOB_ID: ingestion_job_id, c.DELETED: False}
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)
        raise

    audience_ids = [doc[c.ID] for doc in cursor]

    return audience_ids


def get_ingestion_job_audience_insights(
    database: DatabaseClient,
    ingestion_job_id: ObjectId,
) -> list:
    """A function to get the a list of all audience insights dicts
    given an ingestion job.

    Args:
        database (DatabaseClient): A database client.
        ingestion_job_id (ObjectId): The Mongo DB ID of the ingestion job.

    Returns:
        list: A list of audience insights.
    """

    all_audience_insights = []

    audience_ids = get_ingestion_job_audience_ids(
        database,
        ingestion_job_id,
    )

    if audience_ids is not None:
        for audience_id in audience_ids:
            insights_doc = get_audience_insights(
                database,
                audience_id,
            )
            if insights_doc is not None:
                all_audience_insights.append(insights_doc)

    return all_audience_insights


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_all_recent_audiences(
    database: DatabaseClient,
) -> list:
    """A function to get all audiences associated with the most recent
       ingestion jobs of data sources.

    Args:
        database (DatabaseClient): A database client.

    Returns:
        list: A list of all audience configuration dicts.
    """

    am_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = am_db[c.AUDIENCES_COLLECTION]
    audiences = []

    # Read all data source ids
    all_data_source_ids = dm.get_all_data_source_ids(database)

    for data_source_id in all_data_source_ids:

        # Get most recent ingestion job id for data source
        recent_ingestion_job_id = dm.get_data_source_recent_ingestion_job_id(
            database,
            data_source_id,
        )

        if recent_ingestion_job_id is None:
            continue

        # Get audience ids related to the most recent ingestion job
        audience_ids = get_ingestion_job_audience_ids(
            database,
            recent_ingestion_job_id,
        )

        if audience_ids is None:
            continue

        # Get audience configurations and add to list
        for audience_id in audience_ids:
            doc = None
            try:
                doc = collection.find_one(
                    {c.ID: audience_id, c.DELETED: False}, {c.DELETED: 0}
                )
            except pymongo.errors.OperationFailure as exc:
                logging.error(exc)

            if doc is not None:
                audiences.append(doc)

    return audiences


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_all_audiences(
    database: DatabaseClient,
) -> Union[list, None]:
    """A function to get all existing audiences in database.

    Args:
        database (DatabaseClient): A database client.

    Returns:
        Union[dict, None]: A list of all audience configuration dicts or None.
    """

    am_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = am_db[c.AUDIENCES_COLLECTION]
    audiences = None

    # Get audience configurations and add to list
    try:
        audiences = list(collection.find({c.DELETED: False}, {c.DELETED: 0}))
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return audiences


def favorite_audience(
    database: DatabaseClient,
    audience_id: ObjectId,
) -> dict:
    """A function to favorite an audience.

    Args:
        database (DatabaseClient): A database client.
        audience_id (ObjectId): MongoDB ID of the audience.

    Returns:
        dict: Updated audience configuration dict.
    """

    # Update dict
    update_dict = {
        c.FAVORITE: True,
        c.UPDATE_TIME: datetime.datetime.utcnow(),
    }

    return update_audience_doc(database, audience_id, update_dict)


def unfavorite_audience(
    database: DatabaseClient,
    audience_id: ObjectId,
) -> dict:
    """A function to unfavorite an audience.

    Args:
        database (DatabaseClient): A database client.
        audience_id (ObjectId): MongoDB ID of the audience.

    Returns:
        dict: Updated audience configuration dict.
    """

    update_dict = {
        c.FAVORITE: False,
        c.UPDATE_TIME: datetime.datetime.utcnow(),
    }

    return update_audience_doc(database, audience_id, update_dict)


def get_audiences_count(database: DatabaseClient) -> int:
    """A function to retrieve count of audiences documents.

    Args:
        database (DatabaseClient): A database client.

    Returns:
        int: Count of audiences documents.
    """

    return get_collection_count(
        database, c.DATA_MANAGEMENT_DATABASE, c.AUDIENCES_COLLECTION
    )


def set_ingestion_job_status(
    database: DatabaseClient,
    ingestion_job_id: ObjectId,
    job_status: str,
    status_msg: str = "",
) -> dict:
    """Set an ingestion job status.

    Args:
        database (DatabaseClient): A database client.
        ingestion_job_id (ObjectId): MongoDB document ID of ingestion job.
        job_status (str): Status of ingestion job. Can be Pending,
            In Progress, Failed, or Succeeded.
        status_msg (str): Additional details related to the current job status.

    Returns:
        dict: Updated ingestion job document.
    """

    ingestion_job_id_doc = dm.set_ingestion_job_status_no_default_audience(
        database,
        ingestion_job_id,
        job_status,
        status_msg,
    )
    return ingestion_job_id_doc


def update_audience_status_for_delivery(
    database: DatabaseClient,
    audience_id: ObjectId,
    status: str,
) -> dict:
    """A function to update audience status

    Args:
        database (DatabaseClient): A database client.
        audience_id (ObjectId): MongoDB ID of the audience.
        status (str): audience status.

    Returns:
        dict: Updated audience configuration dict.
    """

    # Update dict
    update_dict = {
        c.AUDIENCE_STATUS: status,
        c.UPDATE_TIME: datetime.datetime.utcnow(),
    }

    # set the last delivered time if status is successful
    if status == c.AUDIENCE_STATUS_DELIVERED:
        update_dict[c.AUDIENCE_LAST_DELIVERED] = update_dict[c.UPDATE_TIME]

    return update_audience_doc(database, audience_id, update_dict)
