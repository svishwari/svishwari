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
from huxunifylib.database.aggregation_pipelines import (
    trust_id_overview_pipeline,
    trust_id_attribute_ratings_pipeline,
)


def frame_match_query(filters: list) -> dict:
    """Frame the match query based on the selected filters

    Args:
        filters(list): List of selected filters

    Returns:
         (dict): match query
    """
    return {
        "$match": {
            "$and": [
                {
                    "$or": [
                        {
                            f"responses.{x['description']}": {
                                "$regex": val,
                                "$options": "i",
                            }
                        }
                        for val in x["values"]
                    ]
                }
                for x in filters
            ]
        }
    }


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

    # Check validity of delivery_platform_id
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
                db_c.URL: url,
                db_c.SURVEY_RESPONSE_DATE: response_date,
            }
        ).inserted_id
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
    """Method to store bulk survey responses.

    Args:
        database (DatabaseClient): A database client.
        survey_responses_docs (list): A list containing survey response
            documents.

    Returns:
        dict: dict containing insert_status & list of inserted ids.
    """

    platform_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[db_c.SURVEY_METRICS_COLLECTION]

    insert_result = {db_c.INSERT_STATUS: False}

    try:
        result = collection.insert_many(survey_responses_docs, ordered=True)

        if result.acknowledged:
            insert_result[db_c.INSERT_STATUS] = True
            insert_result[db_c.INSERTED_IDS] = result.inserted_ids

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


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_survey_responses(
    database: DatabaseClient,
    filters: list = None,
) -> Union[list, None]:
    """Method to retrieve survey responses.

    Args:
        database (DatabaseClient): A database client.
        filters (list): Filters to apply, default None.

    Returns:
        Union[list, None]: List of survey responses, default None.
    """

    platform_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[db_c.SURVEY_METRICS_COLLECTION]

    match_query_filters = (
        {
            "$and": [
                {
                    "$or": [
                        {
                            f"responses.{x['description']}": {
                                "$regex": val,
                                "$options": "i",
                            }
                        }
                        for val in x["values"]
                    ]
                }
                for x in filters
            ]
        }
        if filters
        else {}
    )

    pipeline = [
        {"$match": match_query_filters},
        {
            "$project": {
                "factors": "$responses.factors",
            }
        },
    ]
    try:
        return list(collection.aggregate(pipeline))

    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_trust_id_overview(
    database: DatabaseClient,
    filters: list = None,
) -> Union[dict, None]:
    """Method to retrieve overview of survey responses.

    Args:
        database (DatabaseClient): A database client.
        filters (list): Filters to apply, default None.

    Returns:
        Union[dict, None]: Dict of survey responses overview, default None.
    """

    collection = database[db_c.DATA_MANAGEMENT_DATABASE][
        db_c.SURVEY_METRICS_COLLECTION
    ]

    pipeline = trust_id_overview_pipeline
    if filters:
        match_query = frame_match_query(filters)
        pipeline.insert(0, match_query)

    try:
        data = list(collection.aggregate(pipeline))
        if data:
            return data[0]

    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_trust_id_attributes(
    database: DatabaseClient,
    filters: list = None,
) -> Union[dict, None]:
    """Method to retrieve attribute ratings of survey responses.

    Args:
        database (DatabaseClient): A database client.
        filters (list): Filters to apply, default None.

    Returns:
        Union[dict, None]: Dict of survey responses overview, default None.
    """
    collection = database[db_c.DATA_MANAGEMENT_DATABASE][
        db_c.SURVEY_METRICS_COLLECTION
    ]

    pipeline = trust_id_attribute_ratings_pipeline
    if filters:
        pipeline.insert(0, frame_match_query(filters))

    try:
        data = list(collection.aggregate(pipeline))
        if data:
            return data[0]

    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def delete_survey_responses(
    database: DatabaseClient,
    query: dict = None,
) -> dict:
    """Method to delete survey responses based on query parameter.

    Args:
        database (DatabaseClient): A database client.
        query (dict): A dict containing query params & conditions

    Returns:
        dict: dict containing insert_status & list of inserted ids.
    """

    platform_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    collection = platform_db[db_c.SURVEY_METRICS_COLLECTION]

    remove_status = {}

    try:

        if query:
            query_result = collection.find(query)

            if not list(query_result):
                remove_status[db_c.STATUS] = False
                remove_status[db_c.STATUS_MESSAGE] = "Incorrect query"
                return remove_status

        else:
            query = {}

        remove_result = collection.remove(query)
        if remove_result["n"]:
            remove_status[db_c.STATUS] = True
            remove_status[
                db_c.STATUS_MESSAGE
            ] = "Total records deleted: " + str(remove_result["n"])

        else:
            remove_status[db_c.STATUS] = False
            remove_status[db_c.STATUS_MESSAGE] = "Failed to delete records"

    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return remove_status
