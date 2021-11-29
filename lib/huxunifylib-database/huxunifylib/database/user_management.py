"""This module enables functionality related to user management."""

import logging
import datetime
import re
from typing import Any, Union
from bson import ObjectId
import pymongo
from tenacity import retry, wait_fixed, retry_if_exception_type

import huxunifylib.database.db_exceptions as de
import huxunifylib.database.constants as db_c
from huxunifylib.database.client import DatabaseClient
from huxunifylib.database.utils import name_exists

USER_LOOKUP_PIPELINE = [
    # lookup the created by user to the user collection
    {
        "$lookup": {
            "from": db_c.USER_COLLECTION,
            "localField": db_c.CREATED_BY,
            "foreignField": db_c.ID,
            "as": "created_user",
        }
    },
    # lookup the updated by user to the user collection
    {
        "$lookup": {
            "from": db_c.USER_COLLECTION,
            "localField": db_c.UPDATED_BY,
            "foreignField": db_c.ID,
            "as": "updated_user",
        }
    },
    # extract the created and updated user
    {"$unwind": {"path": "$created_user", "preserveNullAndEmptyArrays": True}},
    {
        "$unwind": {
            "path": "$updated_user",
            "preserveNullAndEmptyArrays": True,
        },
    },
    # add two fields from the user object
    {
        "$addFields": {
            "created_by": {"$ifNull": ["$created_user.display_name", ""]},
            "updated_by": {"$ifNull": ["$updated_user.display_name", ""]},
        }
    },
    # exclude the leftover user object
    {"$project": {"created_user": 0, "updated_user": 0}},
]


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def set_user(
    database: DatabaseClient,
    okta_id: str,
    email_address: str,
    role: str = db_c.USER_ROLE_VIEWER,
    organization: str = "",
    subscriptions: list = None,
    display_name: str = "",
    profile_photo: str = "",
    pii_access: bool = False,
) -> Union[dict, None]:
    """A function to set a user.

    Args:
        database (DatabaseClient): A database client.
        okta_id (str): Okta user id.
        email_address (str): email address of a user.
        role (str): user role, defaults to a viewer role.
        organization (str): organization the user belongs to, defaults an empty
            string.
        subscriptions (list): subscription list, defaults to an empty list.
        display_name (str): display name for a user, defaults to the entered
            email address.
        profile_photo (str): a profile photo url for the user, defaults to an
            empty string.
        pii_access (bool): PII Access, defaults to False

    Returns:
        Union[dict, None]: MongoDB document for a user.

    Raises:
        DuplicateName: Error if an user with the same okta_id exists already.
    """

    # validate okta_id and email_address
    if (
        not isinstance(okta_id, str)
        or not isinstance(email_address, str)
        or not re.search(db_c.EMAIL_REGEX, email_address)
        or not okta_id
    ):
        return None

    # get collection
    collection = database[db_c.DATA_MANAGEMENT_DATABASE][db_c.USER_COLLECTION]

    # Get current time
    curr_time = datetime.datetime.utcnow()

    doc = {
        db_c.OKTA_ID: okta_id,
        db_c.USER_ROLE: role,
        db_c.USER_ORGANIZATION: organization,
        db_c.USER_SUBSCRIPTION: [] if subscriptions is None else subscriptions,
        db_c.S_TYPE_EMAIL: email_address,
        db_c.USER_DISPLAY_NAME: display_name,
        db_c.UPDATE_TIME: curr_time,
        db_c.CREATE_TIME: curr_time,
        db_c.USER_PROFILE_PHOTO: profile_photo,
        db_c.USER_LOGIN_COUNT: 0,
        db_c.USER_FAVORITES: {
            db_c.AUDIENCES: [],
            db_c.DESTINATIONS: [],
            db_c.CAMPAIGNS: [],
            db_c.ENGAGEMENTS: [],
        },
        db_c.USER_DASHBOARD_CONFIGURATION: {},
        db_c.USER_PII_ACCESS: pii_access,
    }

    # validate okta
    if name_exists(
        database,
        db_c.DATA_MANAGEMENT_DATABASE,
        db_c.USER_COLLECTION,
        db_c.OKTA_ID,
        okta_id,
    ):
        raise de.DuplicateName(okta_id)

    try:
        user_id = collection.insert_one(doc).inserted_id
        if user_id is not None:
            return collection.find_one({db_c.ID: user_id})
        logging.error("Failed to create a new user!")
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_user(database: DatabaseClient, okta_id: str) -> Union[dict, None]:
    """A function to get a user.

    Args:
        database (DatabaseClient): A database client.
        okta_id (str): id derived from okta authentication.

    Returns:
        Union[dict, None]: MongoDB document for a user.
    """

    collection = database[db_c.DATA_MANAGEMENT_DATABASE][db_c.USER_COLLECTION]

    try:
        return collection.find_one({db_c.OKTA_ID: okta_id})
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def get_all_users(database: DatabaseClient, filter_dict: dict = None) -> list:
    """A function to get all user documents.

    Args:
        database (DatabaseClient): A database client.
        filter_dict (dict): filter dictionary for adding custom filters.

    Returns:
        list: List of all user documents.
    """

    collection = database[db_c.DATA_MANAGEMENT_DATABASE][db_c.USER_COLLECTION]

    try:
        return list(collection.find(filter_dict if filter_dict else {}))
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return []


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def delete_user(
    database: DatabaseClient,
    okta_id: str,
) -> bool:
    """A function to delete a user.

    Args:
        database (DatabaseClient): A database client.
        okta_id (str): Okta ID of the user.

    Returns:
        bool: A flag indicating successful deletion.
    """

    collection = database[db_c.DATA_MANAGEMENT_DATABASE][db_c.USER_COLLECTION]

    try:
        return collection.delete_one({db_c.OKTA_ID: okta_id}).deleted_count > 0
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return False


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def update_user(
    database: DatabaseClient, okta_id: str, update_doc: dict
) -> Union[dict, None]:
    """A function to update a user.

    Args:
        database (DatabaseClient): A database client.
        okta_id (str): Okta ID of a user doc.
        update_doc (dict): Dict of key values to update.

    Returns:
        Union[dict, None]: Updated MongoDB document for a user.

    Raises:
        DuplicateFieldType: Error if a key that is passed in update_doc dict is
            not part of the allowed fields list.
    """

    # validate user input id
    if not okta_id or not update_doc or not isinstance(update_doc, dict):
        return None

    collection = database[db_c.DATA_MANAGEMENT_DATABASE][db_c.USER_COLLECTION]

    allowed_fields = [
        db_c.USER_ROLE,
        db_c.USER_ORGANIZATION,
        db_c.USER_SUBSCRIPTION,
        db_c.S_TYPE_EMAIL,
        db_c.USER_DISPLAY_NAME,
        db_c.USER_PROFILE_PHOTO,
        db_c.USER_FAVORITES,
        db_c.USER_DASHBOARD_CONFIGURATION,
        db_c.USER_LOGIN_COUNT,
        db_c.UPDATE_TIME,
        db_c.UPDATED_BY,
        db_c.USER_PII_ACCESS,
    ]

    # validate allowed fields, any invalid returns, raise error
    key_check = [key for key in update_doc.keys() if key not in allowed_fields]
    if any(key_check):
        raise de.DuplicateFieldType(",".join(key_check))

    # set the update time
    update_doc[db_c.UPDATE_TIME] = datetime.datetime.utcnow()

    try:
        return collection.find_one_and_update(
            {db_c.OKTA_ID: okta_id},
            {"$set": update_doc},
            upsert=False,
            return_document=pymongo.ReturnDocument.AFTER,
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def manage_user_favorites(
    database: DatabaseClient,
    okta_id: str,
    component_name: str,
    component_id: ObjectId,
    delete_flag: bool = False,
) -> Union[dict, None]:
    """A function to add a favorite component for a user.

    Args:
        database (DatabaseClient): A database client.
        okta_id (str): Okta ID of a user doc.
        component_name (ObjectId): name of the component (i.e campaigns,
            destinations, etc.).
        component_id (ObjectId): MongoDB ID of the input component.
        delete_flag (bool): Boolean that specifies to add/remove a favorite
            component, defaults to false.

    Returns:
        Union[dict, None]: Updated MongoDB document for a user.

    Raises:
        InvalidID: If the passed in component_id did not fetch a doc from the
            relevant db collections(audiences/engagements).
    """

    component_name = component_name.lower()

    # validate user input id and campaign id
    if (
        not okta_id
        or not isinstance(component_id, ObjectId)
        or component_name not in db_c.FAVORITE_COMPONENTS
    ):
        return None

    component_collection = {
        db_c.ENGAGEMENTS: db_c.ENGAGEMENTS_COLLECTION,
        db_c.AUDIENCES: db_c.AUDIENCES_COLLECTION,
        db_c.LOOKALIKE: db_c.LOOKALIKE_AUDIENCE_COLLECTION,
    }

    # TODO - validate input component ID if it exists
    #      - fill out when we have campaigns, destinations
    try:
        if not delete_flag and not database[db_c.DATA_MANAGEMENT_DATABASE][
            component_collection[component_name]
        ].find_one({db_c.ID: component_id}):
            raise de.InvalidID(component_id)
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    # grab the collection
    collection = database[db_c.DATA_MANAGEMENT_DATABASE][db_c.USER_COLLECTION]

    event = "$pull" if delete_flag else "$push"
    element_query = "$eq" if delete_flag else "$ne"

    # grab the favorite field
    config_field = f"{db_c.USER_FAVORITES}.{component_name}"

    try:
        return collection.find_one_and_update(
            {
                db_c.OKTA_ID: okta_id,
                config_field: {element_query: component_id},
            },
            {
                "$set": {
                    db_c.UPDATE_TIME: datetime.datetime.utcnow(),
                },
                event: {config_field: component_id},
            },
            upsert=False,
            return_document=pymongo.ReturnDocument.AFTER,
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def manage_user_dashboard_config(
    database: DatabaseClient,
    okta_id: str,
    config_key: str,
    config_value: Any,
    delete_flag: bool = False,
) -> Union[dict, None]:
    """A function to manage user dashboard configuration.

    Args:
        database (DatabaseClient): A database client.
        okta_id (str): Okta ID of a user doc.
        config_key (ObjectId): name of the config param.
        config_value (Any): value of the config key.
        delete_flag (bool): flag to delete the user config, defaults to false.

    Returns:
        Union[dict, None]: Updated MongoDB document for a user.
    """

    # validate user input id and config param
    if not okta_id or not isinstance(config_key, str):
        return None

    # grab the collection
    collection = database[db_c.DATA_MANAGEMENT_DATABASE][db_c.USER_COLLECTION]

    # grab the configuration field
    config_field = f"{db_c.USER_DASHBOARD_CONFIGURATION}.{config_key}"

    # set mongo query based on delete flag
    update_dict = {"$set": {db_c.UPDATE_TIME: datetime.datetime.utcnow()}}
    if delete_flag:
        update_dict["$unset"] = {config_field: config_value}
    else:
        update_dict["$set"][config_field] = config_value

    try:
        return collection.find_one_and_update(
            {db_c.OKTA_ID: okta_id},
            update_dict,
            upsert=False,
            return_document=pymongo.ReturnDocument.AFTER,
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None
