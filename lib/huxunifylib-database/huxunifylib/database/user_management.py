"""This module enables functionality related to user management."""

import logging
import datetime
import re
from typing import Any, Union
from bson import ObjectId
import pymongo
from pymongo import ReturnDocument
from tenacity import retry, wait_fixed, retry_if_exception_type

import huxunifylib.database.db_exceptions as de
import huxunifylib.database.constants as db_c
from huxunifylib.database.client import DatabaseClient
from huxunifylib.database.utils import name_exists
from huxunifylib.database.collection_management import get_document

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
    seen_notifications: bool = False,
    last_seen_alert_time: datetime.datetime = None,
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
        seen_notifications (bool): Seen Notifications Flag, defaults to False
        last_seen_alert_time (datetime): Last Seen Alert Timestamp

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
            db_c.ENGAGEMENTS: [],
            db_c.LOOKALIKE: [],
        },
        db_c.USER_DASHBOARD_CONFIGURATION: {},
        db_c.USER_APPLICATIONS: [],
        db_c.USER_PII_ACCESS: pii_access,
        db_c.SEEN_NOTIFICATIONS: seen_notifications,
        db_c.LAST_SEEN_ALERT_TIME: last_seen_alert_time,
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
def get_all_users(
    database: DatabaseClient,
    filter_dict: dict = None,
    project_dict: dict = None,
) -> list:
    """A function to get all user documents.

    Args:
        database (DatabaseClient): A database client.
        filter_dict (dict): filter dictionary for adding custom filters.
        project_dict(dict): project dictionary to return specific fields.

    Returns:
        list: List of all user documents.
    """

    collection = database[db_c.DATA_MANAGEMENT_DATABASE][db_c.USER_COLLECTION]

    try:
        return list(
            collection.find(
                filter_dict if filter_dict else {},
                projection=project_dict if project_dict else {db_c.DELETED: 0},
            )
        )
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
        db_c.USER_APPLICATIONS,
        db_c.USER_DASHBOARD_CONFIGURATION,
        db_c.USER_LOGIN_COUNT,
        db_c.UPDATE_TIME,
        db_c.UPDATED_BY,
        db_c.USER_PII_ACCESS,
        db_c.USER_ALERTS,
        db_c.SEEN_NOTIFICATIONS,
        db_c.LAST_SEEN_ALERT_TIME,
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
def delete_favorite_from_all_users(
    database: DatabaseClient, component_name: str, component_id: ObjectId
) -> bool:
    """Deletes the an id from all lists in the favorites for a user

    Args:
        database (DatabaseClient): A database client.
        component_name (str): name of the component.
        component_id (ObjectId): MongoDB ID of the input component.

    Returns:
        bool: Indicates success or failure.
    """

    collection = database[db_c.DATA_MANAGEMENT_DATABASE][db_c.USER_COLLECTION]
    component_name = component_name.lower()
    favorites_list = f"{db_c.USER_FAVORITES}.{component_name}"

    try:
        collection.update_many(
            {
                favorites_list: {"$eq": component_id},
            },
            {
                "$set": {
                    db_c.UPDATE_TIME: datetime.datetime.utcnow(),
                },
                "$pull": {favorites_list: component_id},
            },
            upsert=False,
        )
        return True
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return False


def update_all_users(
    database: DatabaseClient, update_doc: dict
) -> Union[dict, None]:
    """Function to update all users.

    Args:
        database (DatabaseClient): A database client.
        update_doc (dict): Dict of key values to update.

    Returns:
        Union[dict, None]: Updated MongoDB document for a user.

    Raises:
        DuplicateFieldType: Error if a key that is passed in update_doc dict is
            not part of the allowed fields list.
    """

    collection = database[db_c.DATA_MANAGEMENT_DATABASE][db_c.USER_COLLECTION]

    allowed_fields = [
        db_c.USER_ROLE,
        db_c.USER_ORGANIZATION,
        db_c.USER_SUBSCRIPTION,
        db_c.S_TYPE_EMAIL,
        db_c.USER_DISPLAY_NAME,
        db_c.USER_PROFILE_PHOTO,
        db_c.USER_FAVORITES,
        db_c.USER_APPLICATIONS,
        db_c.USER_DASHBOARD_CONFIGURATION,
        db_c.USER_LOGIN_COUNT,
        db_c.UPDATE_TIME,
        db_c.UPDATED_BY,
        db_c.USER_PII_ACCESS,
        db_c.USER_ALERTS,
        db_c.SEEN_NOTIFICATIONS,
    ]

    # validate allowed fields, any invalid returns, raise error
    key_check = [key for key in update_doc.keys() if key not in allowed_fields]
    if any(key_check):
        raise de.DuplicateFieldType(",".join(key_check))

    # set the update time
    update_doc[db_c.UPDATE_TIME] = datetime.datetime.utcnow()

    try:
        return collection.update_many(
            {},
            {"$set": update_doc},
            upsert=False,
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
        component_name (str): name of the component.
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

    id_filter = {db_c.ID: component_id}

    try:
        # if adding and the resource DNE then raise error
        if not delete_flag and not get_document(
            database, component_collection[component_name], id_filter
        ):
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


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def update_user_applications(
    database: DatabaseClient,
    okta_id: str,
    application_id: ObjectId,
    url: str = None,
    is_added: bool = True,
) -> Union[dict, None]:
    """A function to update user applications.

    Args:
        database (DatabaseClient): A database client.
        okta_id (str): Okta ID of a user doc.
        application_id (ObjectId): ID of the application.
        url (Optional, str): URL to be updated.
        is_added (bool): flag for soft delete if False, defaults to True.

    Returns:
        Union[dict, None]: Updated document for a user.
    """
    update_dict = {"applications.$.added": is_added}
    if url:
        update_dict["applications.$.url"] = url

    collection = database[db_c.DATA_MANAGEMENT_DATABASE][db_c.USER_COLLECTION]
    try:
        return collection.find_one_and_update(
            filter={
                db_c.OKTA_ID: okta_id,
                db_c.USER_APPLICATIONS: {
                    "$elemMatch": {"id": ObjectId(application_id)}
                },
            },
            update={"$set": update_dict},
            return_document=ReturnDocument.AFTER,
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)
    return None


@retry(
    wait=wait_fixed(db_c.CONNECT_RETRY_INTERVAL),
    retry=retry_if_exception_type(pymongo.errors.AutoReconnect),
)
def add_applications_to_users(
    database: DatabaseClient,
    okta_id: str,
    application_id: ObjectId,
    url: str = None,
) -> Union[dict, None]:
    """A function to add user applications.

    Args:
        database (DatabaseClient): A database client.
        okta_id (str): Okta ID of a user doc.
        application_id (ObjectId): ID of the application.
        url (Optional, str): URL to be updated.

    Returns:
        Union[dict, None]: Updated document for a user.
    """
    collection = database[db_c.DATA_MANAGEMENT_DATABASE][db_c.USER_COLLECTION]
    try:
        return collection.find_one_and_update(
            filter={
                "okta_id": okta_id,
                "applications": {
                    "$not": {
                        "$elemMatch": {
                            "id": application_id,
                        }
                    }
                },
            },
            update={
                "$push": {
                    "applications": {
                        db_c.OBJECT_ID: application_id,
                        db_c.URL: url,
                        db_c.ADDED: True,
                    }
                }
            },
            return_document=ReturnDocument.AFTER,
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


def get_user_applications(
    database: DatabaseClient, okta_id: str
) -> Union[list, None]:
    """A function to fetch user applications.

    Args:
        database (DatabaseClient): A database client.
        okta_id (str): Okta ID of a user doc.

    Returns:
        Union[list, None]: List of applications for a user.
    """
    collection = database[db_c.DATA_MANAGEMENT_DATABASE][db_c.USER_COLLECTION]
    pipeline = [
        {"$match": {"okta_id": okta_id}},
        {
            "$unwind": {
                "path": "$applications",
                "preserveNullAndEmptyArrays": False,
            }
        },
        {
            "$addFields": {
                "application_id": "$applications.id",
                "application_url": "$applications.url",
                "application_added": "$applications.added",
            }
        },
        {
            "$lookup": {
                "from": "applications",
                "localField": "application_id",
                "foreignField": "_id",
                "as": "application",
            }
        },
        {
            "$unwind": {
                "path": "$application",
                "preserveNullAndEmptyArrays": False,
            }
        },
        {
            "$project": {
                "_id": "$application._id",
                "name": "$application.name",
                "category": "$application.category",
                "type": "$application.type",
                "icon": "$application.icon",
                "enabled": "$application.enabled",
                "create_time": "$application.create_time",
                "created_by": "$application.created_by",
                "deleted": "$application.deleted",
                "url": {
                    "$cond": {
                        "if": {"$eq": ["$application_url", None]},
                        "then": "",
                        "else": "$application_url",
                    }
                },
                "is_added": {
                    "$cond": {
                        "if": {"$eq": ["$application_added", None]},
                        "then": True,
                        "else": "$application_added",
                    }
                },
            }
        },
    ]

    try:
        return list(collection.aggregate(pipeline))
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


def add_user_trust_id_segments(
    database: DatabaseClient, okta_id: str, segment: dict
) -> Union[list, None]:
    """A function to add trust id segments for a user.

    Args:
        database (DatabaseClient): A database client.
        okta_id (str): Okta ID of a user doc.
        segment (dict): Segment to be added.

    Returns:
        Union[list, None]: List of trust id segments for a user.
    """
    collection = database[db_c.DATA_MANAGEMENT_DATABASE][db_c.USER_COLLECTION]

    try:
        return collection.find_one_and_update(
            {db_c.OKTA_ID: okta_id},
            {
                "$push": {db_c.TRUST_ID_SEGMENTS: segment},
                "$set": {
                    db_c.UPDATE_TIME: datetime.datetime.utcnow(),
                },
            },
            return_document=pymongo.ReturnDocument.AFTER,
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


def remove_user_trust_id_segments(
    database: DatabaseClient, okta_id: str, segment_name: str
) -> Union[list, None]:
    """A function to fetch trust id segments for a user.

    Args:
        database (DatabaseClient): A database client.
        okta_id (str): Okta ID of a user doc.
        segment_name (str): Name of segment.

    Returns:
        Union[list, None]: List of trust id segments for a user.
    """
    collection = database[db_c.DATA_MANAGEMENT_DATABASE][db_c.USER_COLLECTION]

    try:
        return collection.find_one_and_update(
            {db_c.OKTA_ID: okta_id},
            {
                "$pull": {
                    db_c.TRUST_ID_SEGMENTS: {db_c.SEGMENT_NAME: segment_name}
                },
                "$set": {
                    db_c.UPDATE_TIME: datetime.datetime.utcnow(),
                },
            },
            return_document=pymongo.ReturnDocument.AFTER,
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None


def get_user_trust_id_segments(
    database: DatabaseClient, okta_id: str
) -> Union[list, None]:
    """A function to fetch trust id segments for a user.

    Args:
        database (DatabaseClient): A database client.
        okta_id (str): Okta ID of a user doc.

    Returns:
        Union[list, None]: List of trust id segments for a user.
    """
    collection = database[db_c.DATA_MANAGEMENT_DATABASE][db_c.USER_COLLECTION]

    try:
        return list(
            collection.find_one({db_c.OKTA_ID: okta_id}).get(
                db_c.TRUST_ID_SEGMENTS, []
            )
        )
    except pymongo.errors.OperationFailure as exc:
        logging.error(exc)

    return None
