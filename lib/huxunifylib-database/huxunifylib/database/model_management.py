"""This module enables functionality related to collection management."""
import logging
from datetime import datetime
from typing import Union

import pymongo
from tenacity import retry, wait_fixed, retry_if_exception_type

import huxunifylib.database.constants as db_c
from huxunifylib.database.client import DatabaseClient


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def create_model(
    database: DatabaseClient,
    model_doc: dict,
    username: str = "unknown",
) -> Union[dict, None]:
    """A function to create a new document.

    Args:
        database (DatabaseClient): A database client.
        model_doc (dict): Document to be created.
        username (str): Username.

    Returns:
        Union[dict, None]: MongoDB document for a collection.

    """

    # get collection
    coll = database[db_c.DATA_MANAGEMENT_DATABASE][db_c.MODELS_COLLECTION]

    model_doc[db_c.CREATE_TIME] = datetime.utcnow()
    model_doc[db_c.CREATED_BY] = username
    model_doc[db_c.DELETED] = False

    try:
        document_id = coll.insert_one(model_doc).inserted_id
        if document_id is not None:
            return coll.find_one({db_c.ID: document_id})
        logging.error(
            "Failed to create a document in collection : %s",
            db_c.MODELS_COLLECTION,
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None
