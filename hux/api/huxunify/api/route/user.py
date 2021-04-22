# pylint: disable=no-self-use
"""
Paths for the User API
"""
import logging
from http import HTTPStatus
from typing import Tuple

import json
from bson import ObjectId
from connexion.exceptions import ProblemException
from flask import Blueprint
from flask_apispec import marshal_with
from flasgger import SwaggerView
from marshmallow import ValidationError
from pymongo import MongoClient

from huxunify.api.schema.errors import NotFoundError
from huxunify.api.route.utils import add_view_to_blueprint
from huxunify.api.schema.user import UserSchema
from huxunifylib.database import constants as db_constants
from huxunifylib.database.user_management import (
    get_all_users,
    get_user,
    delete_user,
    update_user,
    manage_user_favorites,
)

USER_TAG = "user"
USER_DESCRIPTION = "USER API"
USER_ENDPOINT = "user"

# setup the cdm blueprint
user_bp = Blueprint(USER_ENDPOINT, import_name=__name__)


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
        HTTPStatus.OK.value: {
            "description": "List of users.",
            "schema": {"type": "array", "items": UserSchema},
        },
    }
    tags = [USER_TAG]

    @marshal_with(UserSchema)
    def get(self) -> Tuple[dict, int]:
        """Retrieves all users.

        ---

        Returns:
            Response: Returns all users

        """
        try:
            return get_all_users(get_db_client()), HTTPStatus.OK.value

        except Exception as exc:

            logging.error(
                "%s: %s.",
                exc.__class__,
                exc,
            )

            raise ProblemException(
                status=int(HTTPStatus.BAD_REQUEST.value),
                title=HTTPStatus.BAD_REQUEST.description,
                detail="Unable to get users.",
            ) from exc


@add_view_to_blueprint(user_bp, f"/{USER_ENDPOINT}/<user_id>", "IndividualUserSearch")
class IndividualUserSearch(SwaggerView):
    """
    Individual User Search Class
    """

    parameters = [
        {
            "name": db_constants.USER_ID,
            "description": "User ID.",
            "type": "string",
            "in": "path",
            "required": True,
            "example": "5f5f7262997acad4bac4373b",
        },
    ]
    responses = {
        HTTPStatus.OK.value: {
            "description": "Retrieve Individual User",
            "schema": UserSchema,
        },
        HTTPStatus.NOT_FOUND.value: {
            "schema": NotFoundError,
        },
    }
    tags = [USER_TAG]

    @marshal_with(UserSchema)
    def get(self, user_id: str) -> Tuple[dict, int]:
        """Retrieves a user by ID.

        ---
        Args:
            user_id (str): id of user

        Returns:
            Tuple[dict, int]: dict of user and user enum

        """

        # validate the id
        try:
            valid_id = (
                UserSchema()
                .load({db_constants.USER_ID: user_id}, partial=True)
                .get(db_constants.USER_ID)
            )
        except ValidationError as validation_error:
            return validation_error.messages, HTTPStatus.BAD_REQUEST

        try:
            return get_user(get_db_client(), okta_id=valid_id), HTTPStatus.OK

        except Exception as exc:

            logging.error(
                "%s: %s.",
                exc.__class__,
                exc,
            )

            raise ProblemException(
                status=int(HTTPStatus.BAD_REQUEST.value),
                title=HTTPStatus.BAD_REQUEST.description,
                detail=f"Unable to get user {user_id}.",
            ) from exc


@add_view_to_blueprint(
    user_bp, f"/{USER_ENDPOINT}/<user_id>/preferences", "Preferences"
)
class Preferences(SwaggerView):
    """
    Update user preferences
    """

    parameters = [
        {
            "name": db_constants.USER_ID,
            "description": "User ID.",
            "type": "string",
            "in": "path",
            "required": True,
            "example": "5f5f7262997acad4bac4373b",
        },
    ]

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
        """Edit a user's preferences

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
        """Add a user's preferences

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
                "message": f"Invalid user ID received {user_id}."
            }, HTTPStatus.BAD_REQUEST

        update_doc = json.loads(update_doc)

        response = update_user(get_db_client(), user_id=user_id, update_doc=update_doc)

        return response, HTTPStatus.OK

    def delete(self, user_id: str) -> Tuple[dict, int]:
        """Remove a user's preferences

        ---
        Args:
            user_id (str): User id

        Returns:
            Tuple[dict, int]: profile dict, HTTP status

        """
        if ObjectId.is_valid(user_id):
            user_id = ObjectId(user_id)
        else:
            return {
                "message": f"Invalid user ID received {user_id}."
            }, HTTPStatus.BAD_REQUEST

        response = delete_user(get_db_client(), user_id=user_id)

        return response, HTTPStatus.OK


@add_view_to_blueprint(
    user_bp, f"/{USER_ENDPOINT}/<user_id>/favorites", "AddUserFavorite"
)
class UserFavorite(SwaggerView):
    """
    User favorites class
    """

    parameters = [
        {
            db_constants.USER_ID: db_constants.USER_ID,
            db_constants.COMPONENT_NAME: "component name",
            db_constants.COMPONENT_ID: "id of favorite component",
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
                "message": f"Invalid user ID received {user_id}."
            }, HTTPStatus.BAD_REQUEST

        if ObjectId.is_valid(component_id):
            component_id = ObjectId(component_id)
        else:
            return {
                "message": f"Invalid component ID received {component_id}."
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
        """Edit favorite for a user

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
                "message": f"Invalid user ID received {user_id}."
            }, HTTPStatus.BAD_REQUEST

        if ObjectId.is_valid(component_id):
            component_id = ObjectId(component_id)
        else:
            return {
                "message": f"Invalid component ID received {component_id}."
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
                "message": f"Invalid user ID received {user_id}."
            }, HTTPStatus.BAD_REQUEST

        if ObjectId.is_valid(component_id):
            component_id = ObjectId(component_id)
        else:
            return {
                "message": f"Invalid component ID received {component_id}."
            }, HTTPStatus.BAD_REQUEST

        response = manage_user_favorites(
            get_db_client(),
            user_id=user_id,
            component_name=component_name,
            component_id=component_id,
            delete_flag=True,
        )

        return response, HTTPStatus.OK
