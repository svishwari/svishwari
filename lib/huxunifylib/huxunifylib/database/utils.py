"""This module is for the external database utilities."""

import logging
from bson import ObjectId
import pymongo
from tenacity import retry, wait_fixed, retry_if_exception_type

import huxunifylib.database.constants as c
import huxunifylib.database.data_management as dm
import huxunifylib.database.audience_management as am
import huxunifylib.database.delivery_platform_management as dpm
from huxunifylib.database.client import DatabaseClient
from huxunifylib.database.db_utils import get_docs_bulk


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def delete_lookalike_audience(
    database: DatabaseClient,
    lookalike_audience_id: ObjectId,
) -> bool:
    """A function to soft delete a delivery platform lookalike audience.

    Args:
        database (DatabaseClient): A database client.
        lookalike_audience_id (ObjectId): The Mongo ID of lookalike audience.

    Returns:
        bool: A flag indicating successful deletion.

    """

    success_flag = False
    ret_doc = None
    platform_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[c.LOOKALIKE_AUDIENCE_COLLECTION]

    update_doc = {c.ENABLED: False}

    try:
        ret_doc = collection.find_one_and_update(
            {c.ID: lookalike_audience_id},
            {"$set": update_doc},
            upsert=False,
            return_document=pymongo.ReturnDocument.AFTER,
        )
        if ret_doc is not None:
            success_flag = True
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return success_flag


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
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
    success_flag = True
    lookalike_ids = None

    doc = dpm.get_delivery_job(
        database,
        delivery_job_id,
    )

    if doc is not None:
        lookalike_ids = doc.get(c.DELIVERY_PLATFORM_LOOKALIKE_AUDS)

    if lookalike_ids is not None:
        for lookalike_id in lookalike_ids:
            doc = delete_lookalike_audience(
                database,
                lookalike_id,
            )
            if doc is None:
                success_flag = False
                break

    return success_flag


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def delete_delivery_job(
    database: DatabaseClient,
    delivery_job_id: ObjectId,
) -> bool:
    """A function to soft delete a delivery job.

    Args:
        database (DatabaseClient): A database client.
        delivery_job_id (ObjectId): MongoDB document ID of delivery job.

    Returns:
        bool: A flag indicating successful deletion.

    """

    success_flag = False
    doc = None
    am_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = am_db[c.DELIVERY_JOBS_COLLECTION]

    if delete_delivery_job_lookalike_audiences(
        database,
        delivery_job_id,
    ):
        update_doc = {c.ENABLED: False}

        try:
            doc = collection.find_one_and_update(
                {c.ID: delivery_job_id},
                {"$set": update_doc},
                upsert=False,
                return_document=pymongo.ReturnDocument.AFTER,
            )
            if doc is not None:
                success_flag = True
        except pymongo.errors.OperationFailure as exc:
            logging.error(exc)

    return success_flag


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
    success_flag = True
    delivery_jobs = dpm.get_delivery_platform_delivery_jobs(
        database, delivery_platform_id
    )

    if delivery_jobs is not None or len(delivery_jobs) > 0:
        for delivery_job in delivery_jobs:
            doc = delete_delivery_job(database, delivery_job[c.ID])
            if doc is None:
                success_flag = False
                break

    return success_flag


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
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

    success_flag = False
    doc = None
    platform_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[c.DELIVERY_PLATFORM_COLLECTION]

    if delete_delivery_platform_delivery_jobs(
        database,
        delivery_platform_id,
    ):
        update_doc = {c.ENABLED: False}

        try:
            doc = collection.find_one_and_update(
                {c.ID: delivery_platform_id},
                {"$set": update_doc},
                upsert=False,
                return_document=pymongo.ReturnDocument.AFTER,
            )
            if doc is not None:
                success_flag = True
        except pymongo.errors.OperationFailure as exc:
            logging.error(exc)

    return success_flag


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
    success_flag = True
    delivery_jobs = dpm.get_audience_delivery_jobs(database, audience_id)

    if delivery_jobs is not None and len(delivery_jobs) > 0:
        for delivery_job in delivery_jobs:
            doc = delete_delivery_job(database, delivery_job[c.ID])
            if doc is None:
                success_flag = False
                break

    return success_flag


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
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
    success_flag = False
    doc = None
    am_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = am_db[c.AUDIENCES_COLLECTION]

    if delete_audience_delivery_jobs(
        database,
        audience_id,
    ):
        update_dict = {c.ENABLED: False}

        try:
            doc = collection.find_one_and_update(
                {c.ID: audience_id},
                {"$set": update_dict},
                upsert=False,
                return_document=pymongo.ReturnDocument.AFTER,
            )
            if doc is not None:
                success_flag = True
        except pymongo.errors.OperationFailure as exc:
            logging.error(exc)

    return success_flag


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
    success_flag = True

    audience_ids = am.get_ingestion_job_audience_ids(
        database,
        ingestion_job_id,
    )

    if audience_ids is not None and len(audience_ids) > 0:
        for audience_id in audience_ids:
            tmp_flag = delete_audience(database, audience_id)
            if not tmp_flag:
                success_flag = False
                break

    return success_flag


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
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

    success_flag = False
    dm_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = dm_db[c.INGESTION_JOBS_COLLECTION]

    if delete_ingestion_job_audiences(database, ingestion_job_id):
        update_doc = {c.ENABLED: False}

        try:
            doc = collection.find_one_and_update(
                {c.ID: ingestion_job_id},
                {"$set": update_doc},
                upsert=False,
                return_document=pymongo.ReturnDocument.AFTER,
            )
            if doc is not None:
                success_flag = True
        except pymongo.errors.OperationFailure as exc:
            logging.error(exc)

    return success_flag


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
    success_flag = True

    ingestion_jobs = dm.get_data_source_ingestion_jobs(database, data_source_id)

    if ingestion_jobs is not None and len(ingestion_jobs) > 0:
        for doc in ingestion_jobs:
            doc = delete_ingestion_job(database, doc[c.ID])
            if doc is None:
                success_flag = False
                break

    return success_flag


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

    success_flag = False

    if delete_data_source_ingestion_jobs(database, data_source_id):
        doc = dm.update_data_source_param(
            database,
            data_source_id,
            c.ENABLED,
            False,
        )

        if doc is not None:
            success_flag = True

    return success_flag


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
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

    Returns:
        bool: A flag indicating successful deletion.

    """

    success_flag = False
    update_result = None
    platform_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[collection_name]

    update_doc = {c.ENABLED: False}

    try:
        update_result = collection.update_many(
            {c.ID: {"$in": mongo_ids}},
            {"$set": update_doc},
            upsert=False,
        )
        if update_result is not None:
            success_flag = True
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return success_flag


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
        database, lookalike_audience_ids, c.LOOKALIKE_AUDIENCE_COLLECTION
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

    success_flag = False

    # Delete dependent delivery jobs
    delivery_jobs = get_docs_bulk(
        database,
        audience_ids,
        c.DELIVERY_JOBS_COLLECTION,
        c.AUDIENCE_ID,
        False,
    )

    delivery_job_ids = [doc[c.ID] for doc in delivery_jobs]

    success_flag = delete_bulk(database, delivery_job_ids, c.DELIVERY_JOBS_COLLECTION)

    # Delete dependent lookalike audiences
    if success_flag:
        all_lookalike_ids = []
        for delivery_doc in delivery_jobs:
            lookalike_ids = delivery_doc.get(c.DELIVERY_PLATFORM_LOOKALIKE_AUDS)
            if lookalike_ids is not None:
                all_lookalike_ids += lookalike_ids

        if len(all_lookalike_ids) > 0:
            success_flag = delete_lookalike_audiences_bulk(
                database,
                all_lookalike_ids,
            )

    # Delete audiences
    if success_flag:
        success_flag = delete_bulk(database, audience_ids, c.AUDIENCES_COLLECTION)

    return success_flag


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

    success_flag = False

    # Delete dependent delivery jobs
    delivery_jobs = get_docs_bulk(
        database,
        delivery_platform_ids,
        c.DELIVERY_JOBS_COLLECTION,
        c.DELIVERY_PLATFORM_ID,
        False,
    )

    delivery_job_ids = [doc[c.ID] for doc in delivery_jobs]

    success_flag = delete_bulk(database, delivery_job_ids, c.DELIVERY_JOBS_COLLECTION)

    # Delete dependent lookalike audiences
    if success_flag:
        all_lookalike_ids = []
        for delivery_doc in delivery_jobs:
            lookalike_ids = delivery_doc.get(c.DELIVERY_PLATFORM_LOOKALIKE_AUDS)
            if lookalike_ids is not None:
                all_lookalike_ids += lookalike_ids

        if len(all_lookalike_ids) > 0:
            success_flag = delete_lookalike_audiences_bulk(
                database,
                all_lookalike_ids,
            )

    # Delete delivery platforms
    if success_flag:
        success_flag = delete_bulk(
            database,
            delivery_platform_ids,
            c.DELIVERY_PLATFORM_COLLECTION,
        )

    return success_flag


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

    success_flag = False

    ingestion_jobs = get_docs_bulk(
        database,
        data_source_ids,
        c.INGESTION_JOBS_COLLECTION,
        c.DATA_SOURCE_ID,
        True,
    )

    ingestion_job_ids = [doc[c.ID] for doc in ingestion_jobs]

    success_flag = delete_bulk(database, ingestion_job_ids, c.INGESTION_JOBS_COLLECTION)

    if success_flag:
        success_flag = delete_bulk(database, data_source_ids, c.DATA_SOURCES_COLLECTION)

    return success_flag
