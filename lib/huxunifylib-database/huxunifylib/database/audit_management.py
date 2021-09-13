"""This module enables functionality related to audit data"""
import logging
from datetime import datetime
from typing import Union

import pymongo
from bson import ObjectId

from tenacity import retry, wait_fixed, retry_if_exception_type

from huxunifylib.database import constants as c
from huxunifylib.database.client import DatabaseClient


@retry(
    wait=wait_fixed(c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def create_audience_audit(
    database: DatabaseClient,
    audience_id: str,
    download_type: str,
    file_name: str,
    user_name: str = None,
) -> Union[dict, None]:
    """
    Creating Audience audit log
    Args:
        database(DatabaseClient): MongoDB Client
        user_name(str): User name
        audience_id(str): Audience Id
        download_type: Type of audience file downloaded
        file_name (str): Uploaded file name

    Returns:
        Union[dict,None]: Audit doc or None, if errors
    """
    dm_db = database[c.DATA_MANAGEMENT_DATABASE]
    collection = dm_db[c.AUDIENCE_AUDIT_COLLECTION]

    doc = {
        c.USER_NAME: user_name if user_name else "",
        c.AUDIENCE_ID: ObjectId(audience_id),
        c.DOWNLOAD_TIME: datetime.now(),
        c.DOWNLOAD_TYPE: download_type,
        c.FILE_NAME: file_name,
    }

    try:
        audit_id = collection.insert_one(doc).inserted_id
        if audit_id is not None:
            ret_doc = collection.find_one({c.ID: audit_id})
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)
        return None
    return ret_doc
