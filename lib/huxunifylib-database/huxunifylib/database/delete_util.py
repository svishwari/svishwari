"""Utilities for deletion."""
import logging
from typing import Union

from bson import ObjectId

import pymongo
from tenacity import retry, wait_fixed, retry_if_exception_type

import huxunifylib.database.data_management as dm
import huxunifylib.database.audience_management as am
import huxunifylib.database.delivery_platform_management as dpm

import huxunifylib.database.constants as db_c
from huxunifylib.database.client import DatabaseClient


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_docs_bulk(
    database: DatabaseClient,
    mongo_ids: list,
    collection_name: str,
    field_name: str,
    ids_only: bool = False,
) -> Union[list, None]:
    """A function to get a list of documents.

    Args:
        database (DatabaseClient): A database client.
        mongo_ids (list): A list of MongoDB IDs.
        collection_name (str): Name of collection.
        field_name (str): Name of corresponding field.
        ids_only (bool): If True, only include IDs in the documents.

    Returns:
        list: A list of documents.
    """

    am_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    collection = am_db[collection_name]
    ret_list = None

    proj_dict = {db_c.DELETED: 0}

    if ids_only:
        proj_dict[db_c.ID] = 1

    try:
        cursor = collection.find(
            {field_name: {"$in": mongo_ids}, db_c.DELETED: False},
            projection=proj_dict,
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    if cursor is not None:
        ret_list = list(cursor)

    return ret_list


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def delete_lookalike_audience(
    database: DatabaseClient,
    lookalike_audience_id: ObjectId,
    soft_delete: bool = True,
) -> bool:
    """A function to soft or hard delete a lookalike audience.

    Args:
        database (DatabaseClient): A database client.
        lookalike_audience_id (ObjectId): The Mongo ID of lookalike audience.
        soft_delete (bool): Flag indicating if the document has to be either
            soft or hard deleted from lookalike_audiences collection.

    Returns:
        bool: A flag indicating successful deletion.
    """

    platform_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[db_c.LOOKALIKE_AUDIENCE_COLLECTION]

    try:
        if soft_delete:
            update_doc = {db_c.DELETED: True}

            if collection.find_one_and_update(
                {db_c.ID: lookalike_audience_id},
                {"$set": update_doc},
                upsert=False,
                return_document=pymongo.ReturnDocument.AFTER,
            ):
                return True
        else:
            return (
                collection.delete_one(
                    {db_c.ID: lookalike_audience_id}
                ).deleted_count
                > 0
            )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return False


def delete_data_source_ingestion_jobs(
    database: DatabaseClient,
    data_source_id: ObjectId,
) -> bool:
    """A function to soft delete all ingestion jobs of a data source.

    Args:
        database (DatabaseClient): A database client.
        data_source_id (ObjectId): MongoDB ID of data source.

    Returns:
        bool: A flag indicating successful deletion.
    """

    ingestion_jobs = dm.get_data_source_ingestion_jobs(
        database, data_source_id
    )
    for doc in ingestion_jobs:
        if not delete_ingestion_job(database, doc[db_c.ID]):
            return False
    return True


def delete_data_source(
    database: DatabaseClient,
    data_source_id: ObjectId,
) -> bool:
    """A function to soft delete a data source.

    Args:
        database (DatabaseClient): A database client.
        data_source_id (ObjectId): MongoDB ID of data source.

    Returns:
        bool: A flag indicating successful deletion.
    """

    if delete_data_source_ingestion_jobs(database, data_source_id):
        if dm.update_data_source_param(
            database,
            data_source_id,
            db_c.ENABLED,
            False,
        ):
            return True
    return False


def delete_ingestion_job_audiences(
    database: DatabaseClient,
    ingestion_job_id: ObjectId,
) -> bool:
    """A function to soft delete all audiences given an ingestion job.

    Args:
        database (DatabaseClient): A database client.
        ingestion_job_id (ObjectId): The Mongo DB ID of the ingestion job.

    Returns:
        bool: A flag indicating successful deletion.
    """

    audience_ids = am.get_ingestion_job_audience_ids(
        database,
        ingestion_job_id,
    )
    for audience_id in audience_ids:
        if not delete_audience(database, audience_id):
            return False
    return True


def delete_delivery_job_lookalike_audiences(
    database: DatabaseClient,
    delivery_job_id: ObjectId,
) -> bool:
    """A function to soft delete delivery job lookalike audiences.

    Args:
        database (DatabaseClient): A database client.
        delivery_job_id (ObjectId): The Mongo DB ID of the delivery job.

    Returns:
        bool: A flag indicating successful deletion.
    """

    doc = dpm.get_delivery_job(database, delivery_job_id)

    if doc:
        lookalike_ids = doc.get(db_c.DELIVERY_PLATFORM_LOOKALIKE_AUDS, [])

        for lookalike_id in lookalike_ids:
            if not delete_lookalike_audience(database, lookalike_id):
                return False
    return True


def delete_delivery_platform_delivery_jobs(
    database: DatabaseClient, delivery_platform_id: ObjectId
) -> bool:
    """A function to soft delete all delivery jobs given a delivery platform.

    Args:
        database (DatabaseClient): A database client.
        delivery_platform_id (ObjectId): Delivery platform id.

    Returns:
        bool: A flag indicating successful deletion.
    """

    delivery_jobs = dpm.get_delivery_platform_delivery_jobs(
        database, delivery_platform_id
    )

    for delivery_job in delivery_jobs:
        if not delete_delivery_job(database, delivery_job[db_c.ID]):
            return False
    return True


def delete_audience_delivery_jobs(
    database: DatabaseClient, audience_id: ObjectId
) -> bool:
    """A function to soft delete all audience delivery jobs given an audience.

    Args:
        database (DatabaseClient): A database client.
        audience_id (ObjectId): Audience id.

    Returns:
        bool: A flag indicating successful deletion.
    """

    delivery_jobs = dpm.get_delivery_jobs(database, audience_id)
    return all(
        delete_delivery_job(database, delivery_job[db_c.ID])
        for delivery_job in delivery_jobs
    )


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def delete_delivery_job(
    database: DatabaseClient,
    delivery_job_id: ObjectId,
    hard_delete: bool = False,
) -> bool:
    """A function to soft delete a delivery job.

    Args:
        database (DatabaseClient): A database client.
        delivery_job_id (ObjectId): MongoDB document ID of delivery job.
        hard_delete (bool): hard deletes delivery_job if True.

    Returns:
        bool: A flag indicating successful deletion.
    """

    am_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    collection = am_db[db_c.DELIVERY_JOBS_COLLECTION]

    if delete_delivery_job_lookalike_audiences(
        database,
        delivery_job_id,
    ):
        update_doc = {db_c.DELETED: True}

        try:
            if hard_delete:
                collection.delete_one({db_c.ID: delivery_job_id})
                return True
            if collection.find_one_and_update(
                {db_c.ID: delivery_job_id},
                {"$set": update_doc},
                upsert=False,
                return_document=pymongo.ReturnDocument.AFTER,
            ):
                return True
        except pymongo.errors.OperationFailure as exc:
            logging.error(exc)

    return False


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def delete_performance_metrics_by_delivery_job_id(
    database: DatabaseClient,
    delivery_job_id: ObjectId,
) -> bool:
    """A function to hard delete performance metrics associated with the given
    delivery_job_id.

    Args:
        database (DatabaseClient): A database client.
        delivery_job_id (ObjectId): MongoDB document ID of delivery job.

    Returns:
        bool: A flag indicating successful deletion.
    """

    am_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    perf_metrics_collection = am_db[db_c.PERFORMANCE_METRICS_COLLECTION]

    try:
        perf_metrics_collection.delete_one(
            {db_c.DELIVERY_JOB_ID: delivery_job_id}
        )
        return True
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return False


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def delete_campaign_activity_by_delivery_job_id(
    database: DatabaseClient,
    delivery_job_id: ObjectId,
) -> bool:
    """A function to hard delete campaign activity associated with the given
    delivery_job_id.

    Args:
        database (DatabaseClient): A database client.
        delivery_job_id (ObjectId): MongoDB document ID of delivery job.

    Returns:
        bool: A flag indicating successful deletion.
    """

    am_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    campaign_activity_collection = am_db[db_c.CAMPAIGN_ACTIVITY_COLLECTION]

    try:
        campaign_activity_collection.delete_one(
            {db_c.DELIVERY_JOB_ID: delivery_job_id}
        )
        return True
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return False


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def delete_delivery_platform(
    database: DatabaseClient,
    delivery_platform_id: ObjectId,
) -> bool:
    """A function to soft delete a delivery platform.

    Args:
        database (DatabaseClient): A database client.
        delivery_platform_id (ObjectId): The MongoDB ID of delivery platform.

    Returns:
        bool: A flag indicating successful deletion.
    """

    platform_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[db_c.DELIVERY_PLATFORM_COLLECTION]

    if delete_delivery_platform_delivery_jobs(
        database,
        delivery_platform_id,
    ):
        update_doc = {db_c.DELETED: True}

        try:
            if collection.find_one_and_update(
                {db_c.ID: delivery_platform_id},
                {"$set": update_doc},
                upsert=False,
                return_document=pymongo.ReturnDocument.AFTER,
            ):
                return True
        except pymongo.errors.OperationFailure as exc:
            logging.error(exc)

    return False


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def delete_audience(
    database: DatabaseClient,
    audience_id: ObjectId,
) -> bool:
    """A function to soft delete an audience.

    Args:
        database (DatabaseClient): A database client.
        audience_id (ObjectId): MongoDB ID of the audience.

    Returns:
        bool: A flag indicating successful deletion.
    """

    am_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    collection = am_db[db_c.AUDIENCES_COLLECTION]

    if delete_audience_delivery_jobs(database, audience_id):
        update_dict = {db_c.DELETED: True}

        try:
            if collection.find_one_and_update(
                {db_c.ID: audience_id},
                {"$set": update_dict},
                upsert=False,
                return_document=pymongo.ReturnDocument.AFTER,
            ):
                return True
        except pymongo.errors.OperationFailure as exc:
            logging.error(exc)

    return False


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def delete_ingestion_job(
    database: DatabaseClient,
    ingestion_job_id: ObjectId,
) -> bool:
    """A function to soft delete an ingestion job.

    Args:
        database (DatabaseClient): A database client.
        ingestion_job_id (ObjectId): MongoDB ID of ingestion job.

    Returns:
        bool: A flag indicating successful deletion.
    """

    dm_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    collection = dm_db[db_c.INGESTION_JOBS_COLLECTION]

    if delete_ingestion_job_audiences(database, ingestion_job_id):
        update_doc = {db_c.DELETED: True}

        try:
            if collection.find_one_and_update(
                {db_c.ID: ingestion_job_id},
                {"$set": update_doc},
                upsert=False,
                return_document=pymongo.ReturnDocument.AFTER,
            ):
                return True
        except pymongo.errors.OperationFailure as exc:
            logging.error(exc)

    return False


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def delete_bulk(
    database: DatabaseClient,
    mongo_ids: list,
    collection_name: str,
) -> bool:
    """A function to soft delete a list of objects.

    Args:
        database (DatabaseClient): A database client.
        mongo_ids (list): A list of Mongo IDs.
        collection_name (str): Name of collection.

    Returns:
        bool: A flag indicating successful deletion.
    """

    platform_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[collection_name]

    update_doc = {db_c.DELETED: True}

    try:
        if collection.update_many(
            {db_c.ID: {"$in": mongo_ids}},
            {"$set": update_doc},
            upsert=False,
        ):
            return True
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return False


def delete_lookalike_audiences_bulk(
    database: DatabaseClient,
    lookalike_audience_ids: list,
) -> bool:
    """A function to soft delete a list of delivery platform lookalike audiences.

    Args:
        database (DatabaseClient): A database client.
        lookalike_audience_ids (list): A list of lookalike audience Mongo IDs.

    Returns:
        bool: A flag indicating successful deletion.
    """

    return delete_bulk(
        database, lookalike_audience_ids, db_c.LOOKALIKE_AUDIENCE_COLLECTION
    )


def delete_audiences_bulk(
    database: DatabaseClient,
    audience_ids: list,
) -> bool:
    """A function to soft delete a list of audiences.

    Args:
        database (DatabaseClient): A database client.
        audience_ids (list): A list of audience MongoDB IDs.

    Returns:
        bool: A flag indicating successful deletion.
    """

    # Delete dependent delivery jobs
    delivery_jobs = get_docs_bulk(
        database,
        audience_ids,
        db_c.DELIVERY_JOBS_COLLECTION,
        db_c.AUDIENCE_ID,
        False,
    )

    delivery_job_ids = [doc[db_c.ID] for doc in delivery_jobs]

    if delete_bulk(database, delivery_job_ids, db_c.DELIVERY_JOBS_COLLECTION):
        # Delete dependent lookalike audiences
        all_lookalike_ids = []
        for delivery_doc in delivery_jobs:
            lookalike_ids = delivery_doc.get(
                db_c.DELIVERY_PLATFORM_LOOKALIKE_AUDS
            )
            if lookalike_ids is not None:
                all_lookalike_ids += lookalike_ids

        if delete_lookalike_audiences_bulk(database, all_lookalike_ids):
            # Delete audiences
            if delete_bulk(database, audience_ids, db_c.AUDIENCES_COLLECTION):
                return True
    return False


def delete_delivery_platforms_bulk(
    database: DatabaseClient,
    delivery_platform_ids: list,
) -> bool:
    """A function to soft delete a list of delivery platforms.

    Args:
        database (DatabaseClient): A database client.
        delivery_platform_ids (list): A list of delivery platform MongoDB IDs.

    Returns:
        bool: A flag indicating successful deletion.
    """

    # Delete dependent delivery jobs
    delivery_jobs = get_docs_bulk(
        database,
        delivery_platform_ids,
        db_c.DELIVERY_JOBS_COLLECTION,
        db_c.DELIVERY_PLATFORM_ID,
        False,
    )

    delivery_job_ids = [doc[db_c.ID] for doc in delivery_jobs]

    if delete_bulk(database, delivery_job_ids, db_c.DELIVERY_JOBS_COLLECTION):
        # Delete dependent lookalike audiences
        all_lookalike_ids = []
        for delivery_doc in delivery_jobs:
            lookalike_ids = delivery_doc.get(
                db_c.DELIVERY_PLATFORM_LOOKALIKE_AUDS
            )
            if lookalike_ids:
                all_lookalike_ids += lookalike_ids

        if delete_lookalike_audiences_bulk(database, all_lookalike_ids):
            # Delete delivery platforms
            if delete_bulk(
                database,
                delivery_platform_ids,
                db_c.DELIVERY_PLATFORM_COLLECTION,
            ):
                return True
    return False


def delete_data_sources_bulk(
    database: DatabaseClient,
    data_source_ids: list,
) -> bool:
    """A function to soft delete a list of data sources.

    Args:
        database (DatabaseClient): A database client.
        data_source_ids (list): A list of data source MongoDB IDs.

    Returns:
        bool: A flag indicating successful deletion.
    """

    ingestion_jobs = get_docs_bulk(
        database,
        data_source_ids,
        db_c.INGESTION_JOBS_COLLECTION,
        db_c.DATA_SOURCE_ID,
        True,
    )

    ingestion_job_ids = [doc[db_c.ID] for doc in ingestion_jobs]

    if delete_bulk(
        database, ingestion_job_ids, db_c.INGESTION_JOBS_COLLECTION
    ):
        if delete_bulk(
            database, data_source_ids, db_c.DATA_SOURCES_COLLECTION
        ):
            return True

    return False
