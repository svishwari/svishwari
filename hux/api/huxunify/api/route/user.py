"""
Paths for the User API
"""
from enum import Enum
from http import HTTPStatus
from typing import List, Tuple

from bson import ObjectId
import json
from flask import Blueprint, request
from flask_apispec import marshal_with
from flasgger import SwaggerView, swag_from
from marshmallow.fields import Int
from pymongo import MongoClient

from huxunify.api.schema.errors import NotFoundError
from huxunify.api.route.utils import add_view_to_blueprint
from huxunify.api.schema.user import User
from huxunifylib.database.user_management import *

USER_TAG = "user"
USER_DESCRIPTION = "USER API"
USER_ENDPOINT = "user"

# setup the cdm blueprint
user_bp = Blueprint("user", import_name=__name__)


# TODO convert posts/puts to swagger views


def get_db_client() -> MongoClient:
    """Get DB client.
    Returns:
        MongoClient: DB client
    """
    # TODO - hook-up when ORCH-94 HUS-262 are completed
    return MongoClient()


@add_view_to_blueprint(user_bp, f"/{USER_ENDPOINT}", "UserSearch")
class UserSearch(SwaggerView):
    """
    User Search Class
    """

    parameters = []
    responses = {
        HTTPStatus.OK.value: {"description": "List of users.", "schema": List[User]},
    }
    tags = [USER_TAG]

    @marshal_with(User)
    def get(self) -> List[User]:
        """Retrieves all users.

        ---

        Returns:
            Response: Returns all users

        """
        try:
            data = get_all_users(get_db_client())

            if not data:
                error = NotFoundError().dump({"message": "No Users found"})
                return error, error["code"]

            return data, HTTPStatus.OK.value

        except error:
            return error, error["code"]


@add_view_to_blueprint(user_bp, f"/{USER_ENDPOINT}/<id>", "IndividualUserSearch")
class IndividualUserSearch(SwaggerView):
    """
    Individual User Search Class
    """

    parameters = [{"id": "id of user"}]
    responses = {
        HTTPStatus.OK.value: {
            "description": "Retrieve Individual User",
            "schema": User,
        },
        HTTPStatus.NOT_FOUND.value: {
            "schema": NotFoundError,
        },
    }
    tags = [USER_TAG]

    # TODO doc str fix
    @marshal_with(User)
    def get(self, user_id: str) -> Tuple[dict, int]:
        """Retrieves a user by ID.

        ---
        Args:
            user_id (str): id of user

        Returns:
            Tuple[dict, int]: dict of user and user enum

        """
        try:
            data = get_user(get_db_client(), okta_id=user_id)

            if not data:
                error = NotFoundError().dump({"message": "User not found"})
                return error, error["code"]

            return data, HTTPStatus.OK

        except error:
            return error, error["code"]


@add_view_to_blueprint(
    user_bp, f"/{USER_ENDPOINT}/update-dashboard", "UserDashboardConfiguration"
)
class UserDashboardConfiguration(SwaggerView):
    """
    Update user's dashboard configuration
    """

    parameters = [
        {"user_id": "user_id", "config_key": "key name", "config_value": "value"}
    ]
    responses = {
        HTTPStatus.OK.value: {
            "description": "User dashboard configuration updated",
        },
        HTTPStatus.CREATED.value: {
            "description": "User dashboard configuration created",
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to update user dashboard configuration",
        },
    }

    tags = [USER_TAG]

    def put(self, user_id: str, config_key: str, config_value: Any) -> Tuple[dict, int]:
        """Put a user's dashboard configuration

        ---
        Args:
            user_id (str): User id
            config_key (str): Key for configuration parameter
            config_value (Any): Value for configuration parameter

        Returns:
            Tuple[dict, int]: Configuration dict, HTTP status

        """
        if ObjectId.is_valid(user_id):
            user_id = ObjectId(user_id)
        else:
            return {
                "message": "Invalid user ID received {user_id}."
            }, HTTPStatus.BAD_REQUEST

        response = manage_user_dashboard_config(
            get_db_client(),
            user_id=user_id,
            config_key=config_key,
            config_value=config_value,
        )

        return response, HTTPStatus.OK

    def post(self) -> Tuple[dict, int]:
        pass

    def delete(self) -> Tuple[dict, int]:
        pass


@add_view_to_blueprint(user_bp, f"/{USER_ENDPOINT}/<id>/preferences", "Preferences")
class Preferences:
    """
    Update user preferences
    """

    parameters = [{"user_id": "user_id", "update_doc": "update doc"}]

    responses = {
        HTTPStatus.OK.value: {
            "description": "User preferences updated",
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to update user preferences",
        },
    }

    tags = [USER_TAG]

    def put(self, user_id: str, update_doc: str) -> Tuple[dict, int]:
        """Put a user's dashboard configuration

        ---
        Args:
            user_id (str): User id
            update_doc (str): update document for user profile

        Returns:
            Tuple[dict, int]: profile dict, HTTP status

        """
        if ObjectId.is_valid(user_id):
            user_id = ObjectId(user_id)
        else:
            return {
                "message": "Invalid user ID received {user_id}."
            }, HTTPStatus.BAD_REQUEST

        update_doc = json.loads(update_doc)

        response = update_user(get_db_client(), user_id=user_id, update_doc=update_doc)

        return response, HTTPStatus.OK

    def post(self, user_id: str, update_doc: str) -> Tuple[dict, int]:
        """Put a user's dashboard configuration

        ---
        Args:
            user_id (str): User id
            update_doc (str): update document for user profile

        Returns:
            Tuple[dict, int]: profile dict, HTTP status

        """
        if ObjectId.is_valid(user_id):
            user_id = ObjectId(user_id)
        else:
            return {
                "message": "Invalid user ID received {user_id}."
            }, HTTPStatus.BAD_REQUEST

        update_doc = json.loads(update_doc)

        response = update_user(get_db_client(), user_id=user_id, update_doc=update_doc)

        return response, HTTPStatus.OK

    def delete(self, user_id: str, update_doc: str) -> Tuple[dict, int]:
        """Put a user's dashboard configuration

        ---
        Args:
            user_id (str): User id
            update_doc (str): update document for user profile

        Returns:
            Tuple[dict, int]: profile dict, HTTP status

        """
        if ObjectId.is_valid(user_id):
            user_id = ObjectId(user_id)
        else:
            return {
                "message": "Invalid user ID received {user_id}."
            }, HTTPStatus.BAD_REQUEST

        update_doc = json.loads(update_doc)

        # TODO update user will need to be updated to support delete functionality
        response = update_user(get_db_client(), user_id=user_id, update_doc=update_doc)

        return response, HTTPStatus.OK


@add_view_to_blueprint(user_bp, f"/{USER_ENDPOINT}/<id>/favorites", "AddUserFavorite")
class UserFavorite:
    """
    Add a new favorite for a user
    """

    parameters = [
        {
            "user_id": "user_id",
            "component_name": "component name",
            "component_id": "id of favorite component",
        }
    ]
    responses = {
        HTTPStatus.CREATED.value: {
            "description": "User favorite created",
        },
        HTTPStatus.OK.value: {
            "description": "User favorite edited",
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to add user favorite",
        },
    }

    tags = [USER_TAG]

    def post(
        self, user_id: str, component_name: str, component_id: str
    ) -> Tuple[dict, int]:
        """Add a new favorite for a user

        ---
        Args:
            user_id (str): User id
            component_name (str): name of component
            component_id (str): id of the new favorite component

        Returns:
            Tuple[dict, int]: Configuration dict, HTTP status

        """

        if ObjectId.is_valid(user_id):
            user_id = ObjectId(user_id)
        else:
            return {
                "message": "Invalid user ID received {user_id}."
            }, HTTPStatus.BAD_REQUEST

        if ObjectId.is_valid(component_id):
            component_id = ObjectId(component_id)
        else:
            return {
                "message": "Invalid component ID received {component_id}."
            }, HTTPStatus.BAD_REQUEST

        response = manage_user_favorites(
            get_db_client(),
            user_id=user_id,
            component_name=component_name,
            component_id=component_id,
        )

        return response, HTTPStatus.CREATED

    def put(
        self, user_id: str, component_name: str, component_id: str
    ) -> Tuple[dict, int]:
        """Add a new favorite for a user

        ---
        Args:
            user_id (str): User id
            component_name (str): name of component
            component_id (str): id of the new favorite component

        Returns:
            Tuple[dict, int]: Configuration dict, HTTP status

        """

        if ObjectId.is_valid(user_id):
            user_id = ObjectId(user_id)
        else:
            return {
                "message": "Invalid user ID received {user_id}."
            }, HTTPStatus.BAD_REQUEST

        if ObjectId.is_valid(component_id):
            component_id = ObjectId(component_id)
        else:
            return {
                "message": "Invalid component ID received {component_id}."
            }, HTTPStatus.BAD_REQUEST

        response = manage_user_favorites(
            get_db_client(),
            user_id=user_id,
            component_name=component_name,
            component_id=component_id,
        )

        return response, HTTPStatus.OK

    def delete(
        self, user_id: str, component_name: str, component_id: str
    ) -> Tuple[dict, int]:
        """Remove a favorite for a user

        ---
        Args:
            user_id (str): User id
            component_name (str): name of component
            component_id (str): id of the new favorite component

        Returns:
            Tuple[dict, int]: Configuration dict, HTTP status

        """

        if ObjectId.is_valid(user_id):
            user_id = ObjectId(user_id)
        else:
            return {
                "message": "Invalid user ID received {user_id}."
            }, HTTPStatus.BAD_REQUEST

        if ObjectId.is_valid(component_id):
            component_id = ObjectId(component_id)
        else:
            return {
                "message": "Invalid component ID received {component_id}."
            }, HTTPStatus.BAD_REQUEST

        response = manage_user_favorites(
            get_db_client(),
            user_id=user_id,
            component_name=component_name,
            component_id=component_id,
            delete_flag=True,
        )

        return response, HTTPStatus.OK
