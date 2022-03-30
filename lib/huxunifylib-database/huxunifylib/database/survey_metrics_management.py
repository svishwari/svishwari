"""This module enables functionality related to trust id survey metrics
management."""
import logging
from datetime import datetime
from typing import Union
from bson import ObjectId

import pymongo
from tenacity import retry, wait_fixed, retry_if_exception_type
from huxunifylib.database.client import DatabaseClient
import huxunifylib.database.db_exceptions as de

import huxunifylib.database.constants as db_c
import huxunifylib.database.delivery_platform_management as dm


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def set_survey_response(
    database: DatabaseClient,
    delivery_platform_id: ObjectId,
    delivery_platform_type: str,
    customer_id: str,
    url: str,
    response_date: str,
    survey_id: str,
    responses_dict: dict,
) -> Union[dict, None]:
    """Store survey response in the survey metrics collection.
    Args:
        database (DatabaseClient): A database client.
        delivery_platform_id (ObjectId): delivery platform ID
        delivery_platform_type (str): delivery platform type
        responses_dict (dict): A dict containing survey responses.
        customer_id (str): Customer Id
        url (str): survey url
        survey_id (str): survey id
        response_date (str): response date
    Returns:
        Union[dict, None]: MongoDB metrics doc.
    Raises:
        InvalidID: If the passed in delivery_platform_id did not fetch a doc from
            the relevant db collection.
        OperationFailure: If an exception occurs during mongo operation.
    """

    platform_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[db_c.SURVEY_METRICS_COLLECTION]

    # Check validity of delivery job ID
    if not dm.get_delivery_platform(database, delivery_platform_id):
        raise de.InvalidID(delivery_platform_id)

    try:
        metrics_id = collection.insert_one(
            {
                db_c.CREATE_TIME: datetime.utcnow(),
                db_c.SURVEY_RESPONSES: responses_dict,
                db_c.METRICS_DELIVERY_PLATFORM_ID: delivery_platform_id,
                db_c.METRICS_DELIVERY_PLATFORM_TYPE: delivery_platform_type,
                db_c.SURVEY_ID: survey_id,
                db_c.S_TYPE_SURVEY_CUSTOMER_ID: customer_id,
                db_c.SURVEY_URL: url,
                db_c.SURVEY_RESPONSE_DATE: response_date,
            }
        ).inserted_id
        collection.create_index(
            [
                (db_c.S_TYPE_SURVEY_CUSTOMER_ID, pymongo.ASCENDING),
                (db_c.DELIVERY_PLATFORM_ID, pymongo.ASCENDING),
                (db_c.SURVEY_ID, pymongo.ASCENDING),
            ]
        )
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
def set_survey_responses_bulk(
    database: DatabaseClient,
    survey_responses_docs: list,
) -> dict:
    """Helper to store bulk suvey responses.

    Args:
        database (DatabaseClient): A database client.
        collection_name (str): Name of collection in which operation is
            performed.
        survey_responses_docs (list): A list containing survey response
            documents.

    Returns:
        dict: dict containing insert_status & list of inserted ids.
    """

    platform_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[db_c.SURVEY_METRICS_COLLECTION]

    insert_result = {"insert_status": False}

    try:
        result = collection.insert_many(survey_responses_docs, ordered=True)

        if result.acknowledged:
            insert_result["insert_status"] = True
            insert_result["inserted_ids"] = result.inserted_ids

        collection.create_index(
            [
                (db_c.S_TYPE_SURVEY_CUSTOMER_ID, pymongo.ASCENDING),
                (db_c.DELIVERY_PLATFORM_ID, pymongo.ASCENDING),
                (db_c.SURVEY_ID, pymongo.ASCENDING),
            ]
        )
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
