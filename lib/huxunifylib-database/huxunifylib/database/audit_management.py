"""This module enables functionality related to audit data."""
import logging
import datetime
from typing import Union

import pymongo
from bson import ObjectId
from tenacity import retry, wait_fixed, retry_if_exception_type

from huxunifylib.database import constants as db_c
from huxunifylib.database.client import DatabaseClient


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def create_audience_audit(
    database: DatabaseClient,
    audience_id: ObjectId,
    download_type: str,
    file_name: str,
    user_name: str = None,
) -> Union[dict, None]:
    """Creating Audience audit log.

    Args:
        database (DatabaseClient): MongoDB Client.
        audience_id (ObjectId): Audience Id.
        download_type (str): Type of audience file downloaded.
        file_name (str): Uploaded file name.
        user_name (str): User name.

    Returns:
        Union[dict,None]: Audit doc or None, if errors.
    """

    dm_db = database[db_c.DATA_MANAGEMENT_DATABASE]
    collection = dm_db[db_c.AUDIENCE_AUDIT_COLLECTION]

    doc = {
        db_c.USER_NAME: user_name if user_name else "",
        db_c.AUDIENCE_ID: audience_id,
        db_c.DOWNLOAD_TIME: datetime.datetime.utcnow(),
        db_c.DOWNLOAD_TYPE: download_type,
        db_c.FILE_NAME: file_name,
    }

    try:
        audit_id = collection.insert_one(doc).inserted_id
        if audit_id is not None:
            ret_doc = collection.find_one({db_c.ID: audit_id})
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)
        return None
    return ret_doc
