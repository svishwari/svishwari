"""This module enables functionality related to collection management."""
import logging
from datetime import datetime
from typing import Union

import pymongo
from bson import ObjectId
from tenacity import retry, wait_fixed, retry_if_exception_type

import huxunifylib.database.constants as db_c
from huxunifylib.database.client import DatabaseClient
import huxunifylib.database.db_exceptions as de


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def create_document(
    database: DatabaseClient,
    collection: str,
    new_doc: dict,
    username: str = "unknown",
) -> Union[dict, None]:
    """A function to create a new document.

    Args:
        database (DatabaseClient): A database client.
        collection (str): Collection name.
        new_doc (dict): Document to be created.
        username (str): Username.

    Returns:
        Union[dict, None]: MongoDB document for a collection.

    Raises:
        InvalidValueException: Error if the passed in value
            is not valid.
        DuplicateDocument: Error if the document is duplicate
    """

    if collection not in db_c.ALLOWED_COLLECTIONS:
        raise de.InvalidValueException("Collection not supported")

    # get collection
    coll = database[db_c.DATA_MANAGEMENT_DATABASE][collection]

    # validate allowed fields, any invalid returns, raise error
    key_check = [
        key
        for key in new_doc.keys()
        if key not in db_c.ALLOWED_FIELDS[collection]
    ]
    if any(key_check):
        raise de.InvalidValueException(",".join(key_check))

    key_check = [
        key
        for key in db_c.REQUIRED_FIELDS[collection]
        if key not in new_doc.keys()
    ]
    if any(key_check):
        raise de.InvalidValueException(",".join(key_check))

    # Make sure the data is unique
    doc_check = {}
    for key in db_c.REQUIRED_FIELDS[collection]:
        doc_check[key] = new_doc[key]

    try:
        if coll.find_one(doc_check):
            raise de.DuplicateDocument(doc_check)
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    new_doc[db_c.CREATE_TIME] = datetime.utcnow()
    new_doc[db_c.CREATED_BY] = username
    new_doc[db_c.DELETED] = False

    try:
        document_id = coll.insert_one(new_doc).inserted_id
        if document_id is not None:
            return coll.find_one({db_c.ID: document_id})
        logging.error(
            "Failed to create a document in collection : %s", collection
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def update_document(
    database: DatabaseClient,
    collection: str,
    document_id: ObjectId,
    update_doc: dict,
    username: str = "unknown",
) -> Union[dict, None]:
    """A function to update a document.

    Args:
        database (DatabaseClient): A database client.
        collection (str): Collection name.
        document_id (ObjectId): Document ID of a doc.
        update_doc (dict): Dict of key values to update.
        username (str): Username.

    Returns:
        Union[dict, None]: Updated MongoDB document for a document.

    Raises:
        InvalidValueException: Error if the passed in value
            is not valid.
    """

    if collection not in db_c.ALLOWED_COLLECTIONS:
        raise de.InvalidValueException("Collection not supported")

    # validate input id
    if not document_id or not update_doc or not isinstance(update_doc, dict):
        return None

    coll = database[db_c.DATA_MANAGEMENT_DATABASE][collection]

    # validate allowed fields, any invalid returns, raise error
    key_check = [
        key
        for key in update_doc.keys()
        if key not in db_c.ALLOWED_FIELDS[collection]
    ]
    if any(key_check):
        raise de.InvalidValueException(",".join(key_check))

    update_doc[db_c.UPDATE_TIME] = datetime.utcnow()
    update_doc[db_c.UPDATED_BY] = username

    try:
        return coll.find_one_and_update(
            {db_c.ID: document_id},
            {"$set": update_doc},
            upsert=False,
            return_document=pymongo.ReturnDocument.AFTER,
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


def get_document(
    database: DatabaseClient,
    collection: str,
    query_filter: dict,
    include_deleted: bool = False,
) -> Union[dict, None]:
    """Get document by ID

    Args:
        database (DatabaseClient): MongoDB Database Client
        collection (str): Collection name.
        query_filter (dict): Query to filter documents on.
        include_deleted (bool): Flag to specify whether to fetch deleted docs,
            defaults to False

    Returns:
        Tuple[dict,None]:MongoDB collection document else None

    Raises:
        InvalidValueException: Error if the passed in value
            is not valid.
    """

    if collection not in db_c.ALLOWED_COLLECTIONS:
        raise de.InvalidValueException("Collection not supported")

    # get collection
    coll = database[db_c.DATA_MANAGEMENT_DATABASE][collection]

    query = query_filter if query_filter else {}
    if not include_deleted:
        query[db_c.DELETED] = False

    try:
        return coll.find_one(query)
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_documents(
    database: DatabaseClient,
    collection: str,
    query_filter: Union[dict, None] = None,
    projection: Union[dict, None] = None,
    sort_order: Union[dict, None] = None,
    batch_size: int = 100,
    batch_number: int = 1,
) -> Union[dict, None]:
    """A function to get documents from a collection.

    Args:
        database (DatabaseClient): A database client.
        collection (str): Collection name.
        query_filter (Union[dict[Tuple], None]): Mongo filter Query.
        projection (Union[dict[Tuple], None]): Dict that specifies
        which fields to return or not return. .
        sort_order (Tuple[str, int]): Mongo sort order.
        batch_size (int): Number of documents per batch.
        batch_number (int): Number of which batch should be returned.

    Returns:
        Union[dict, None]: Collection documents with total count.

    Raises:
        InvalidValueException: Error if the passed in value
            is not valid.
    """

    if collection not in db_c.ALLOWED_COLLECTIONS:
        raise de.InvalidValueException("Collection not supported")

    # get collection
    coll = database[db_c.DATA_MANAGEMENT_DATABASE][collection]

    skips = batch_size * (batch_number - 1)

    query_filter = query_filter if query_filter else {}
    if db_c.DELETED not in query_filter:
        query_filter[db_c.DELETED] = False

    projection = projection if projection else {}
    if db_c.DELETED not in projection:
        projection[db_c.DELETED] = 0

    try:
        return dict(
            total_records=coll.count_documents(query_filter),
            documents=list(
                coll.find(query_filter, projection)
                .sort(
                    sort_order
                    if sort_order
                    else [("$natural", pymongo.ASCENDING)]
                )
                .skip(skips)
                .limit(batch_size)
            ),
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def delete_document(
    database: DatabaseClient,
    collection: str,
    query_filter: dict,
    hard_delete: bool = True,
    username: str = "unknown",
) -> bool:
    """A function to delete a document using ID.

    Args:
        database (DatabaseClient): A database client.
        collection (str): Collection name.
        query_filter (dict): MongoDB query filter.
        hard_delete (bool): hard deletes an document if True.
        username (str): Username.

    Returns:
        bool: Flag indicating successful operation.

    Raises:
        InvalidValueException: Error if the passed in value
            is not valid.
    """

    if collection not in db_c.ALLOWED_COLLECTIONS:
        raise de.InvalidValueException("Collection not supported")

    coll = database[db_c.DATA_MANAGEMENT_DATABASE][collection]

    try:
        if hard_delete:
            return coll.delete_one(query_filter).deleted_count > 0
        doc = coll.find_one_and_update(
            query_filter,
            {
                "$set": {
                    db_c.DELETED: True,
                    db_c.UPDATED_BY: username,
                    db_c.UPDATE_TIME: datetime.utcnow(),
                }
            },
            upsert=False,
            new=True,
        )
        if doc:
            return doc[db_c.DELETED]
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return False


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_distinct_values(
    database: DatabaseClient,
    collection: str,
    field_name: str,
    query_filter: dict = None,
) -> Union[list, None]:
    """A function to get distinct values of a field from a collection.

    Args:
        database (DatabaseClient): A database client.
        collection (str): Collection name.
        field_name (str): Field name to get distinct values for.
        query_filter (dict, Optional): MongoDB query filter.

    Returns:
        Union[list, None]: List of distinct values.

    Raises:
        InvalidValueException: Error if the passed in value
            is not valid.
    """

    if collection not in db_c.ALLOWED_COLLECTIONS:
        raise de.InvalidValueException("Collection not supported")

    coll = database[db_c.DATA_MANAGEMENT_DATABASE][collection]
    query_filter = query_filter if query_filter else {}

    try:
        return list(coll.distinct(field_name, query_filter))
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None
