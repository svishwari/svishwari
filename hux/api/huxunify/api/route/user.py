# pylint: disable=no-self-use
"""
Paths for the User API
"""
import logging
from http import HTTPStatus
from typing import Tuple

from bson import ObjectId
from connexion.exceptions import ProblemException
from flask import Blueprint, request
from flask_apispec import marshal_with
from flasgger import SwaggerView
from marshmallow import ValidationError
from pymongo import MongoClient

from huxunifylib.database import constants as db_constants
from huxunifylib.database.user_management import (
    get_all_users,
    get_user,
    manage_user_dashboard_config,
    manage_user_favorites,
)
from huxunify.api.schema.errors import NotFoundError
from huxunify.api.route.utils import add_view_to_blueprint
from huxunify.api.schema.user import UserSchema
from huxunify.api.schema.utils import AUTH401_RESPONSE
from huxunify.api import constants as api_c


USER_TAG = "user"
USER_DESCRIPTION = "USER API"
USER_ENDPOINT = "users"

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
    responses.update(AUTH401_RESPONSE)
    tags = [USER_TAG]

    @marshal_with(UserSchema(many=True))
    def get(self) -> Tuple[dict, int]:
        """Retrieves all users.

        ---

        Returns:
            Tuple[dict, int] dict of users and http code

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


@add_view_to_blueprint(
    user_bp, f"/{USER_ENDPOINT}/<user_id>", "IndividualUserSearch"
)
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
    responses.update(AUTH401_RESPONSE)
    tags = [USER_TAG]

    @marshal_with(UserSchema)
    def get(self, user_id: str) -> Tuple[dict, int]:
        """Retrieves a user by ID.

        ---
        Args:
            user_id (str): id of user

        Returns:
            Tuple[dict, int]: dict of user and http code

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
                detail=f"Unable to get user with ID {user_id}.",
            ) from exc


@add_view_to_blueprint(
    user_bp, f"/{USER_ENDPOINT}/<user_id>/preferences", "AddPreferences"
)
class AddPreferences(SwaggerView):
    """
    Add user preferences class
    """

    parameters = [
        {
            "name": db_constants.USER_ID,
            "in": "path",
            "type": "string",
            "description": "User ID.",
            "example": "5f5f7262997acad4bac4373b",
            "required": True,
        },
        {
            "name": "body",
            "in": "body",
            "type": "object",
            "description": api_c.PREFERENCE_BODY_DESCRIPTION,
            "example": {
                api_c.PREFERENCE_KEY: "configure hux",
                api_c.PREFERENCE_VALUE: True,
            },
            api_c.PREFERENCE_KEY: api_c.PREFERENCE_KEY_DESCRIPTION,
            api_c.PREFERENCE_VALUE: api_c.PREFERENCE_VALUE_DESCRIPTION,
        },
    ]

    responses = {
        HTTPStatus.CREATED.value: {
            "description": "User preferences added.",
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to update user preferences.",
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [USER_TAG]

    def post(self, user_id: str) -> Tuple[dict, int]:
        """Add a user's preferences

        ---
        Args:
            user_id (str): User id

        Returns:
            Tuple[dict, int]: profile dict, HTTP status

        """
        request_data = request.get_json()

        if ObjectId.is_valid(user_id):
            user_id = ObjectId(user_id)
        else:
            return {
                "message": f"Invalid user ID received {user_id}."
            }, HTTPStatus.BAD_REQUEST

        response = manage_user_dashboard_config(
            get_db_client(),
            user_id=user_id,
            config_key=request_data[api_c.PREFERENCE_KEY],
            config_value=request_data[api_c.PREFERENCE_VALUE],
        )

        return response, HTTPStatus.OK


@add_view_to_blueprint(
    user_bp, f"/{USER_ENDPOINT}/<user_id>/preferences", "EditPreferences"
)
class EditPreferences(SwaggerView):
    """
    Edit user preferences class
    """

    parameters = [
        {
            "name": db_constants.USER_ID,
            "in": "path",
            "type": "string",
            "description": "User ID.",
            "example": "5f5f7262997acad4bac4373b",
            "required": True,
        },
        {
            "name": "body",
            "in": "body",
            "type": "object",
            "description": api_c.PREFERENCE_BODY_DESCRIPTION,
            "example": {
                api_c.PREFERENCE_KEY: "configure hux",
                api_c.PREFERENCE_VALUE: True,
            },
            api_c.PREFERENCE_KEY: api_c.PREFERENCE_KEY_DESCRIPTION,
            api_c.PREFERENCE_VALUE: api_c.PREFERENCE_VALUE_DESCRIPTION,
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
    responses.update(AUTH401_RESPONSE)
    tags = [USER_TAG]

    def put(self, user_id: str) -> Tuple[dict, int]:
        """Edit a user's preferences

        ---
        Args:
            user_id (str): User id

        Returns:
            Tuple[dict, int]: profile dict, HTTP status

        """
        request_data = request.get_json()

        if ObjectId.is_valid(user_id):
            user_id = ObjectId(user_id)
        else:
            return {
                "message": f"Invalid user ID received {user_id}."
            }, HTTPStatus.BAD_REQUEST

        response = manage_user_dashboard_config(
            get_db_client(),
            user_id=user_id,
            config_key=request_data[api_c.PREFERENCE_KEY],
            config_value=request_data[api_c.PREFERENCE_VALUE],
        )

        return response, HTTPStatus.OK


@add_view_to_blueprint(
    user_bp, f"/{USER_ENDPOINT}/<user_id>/preferences", "DeletePreferences"
)
class DeletePreferences(SwaggerView):
    """
    Delete user preferences class
    """

    parameters = [
        {
            "name": db_constants.USER_ID,
            "in": "path",
            "type": "string",
            "description": "User ID.",
            "example": "5f5f7262997acad4bac4373b",
            "required": True,
        },
        {
            "name": "body",
            "in": "body",
            "type": "object",
            "description": api_c.PREFERENCE_BODY_DESCRIPTION,
            "example": {
                api_c.PREFERENCE_KEY: "configure hux",
                api_c.PREFERENCE_VALUE: True,
            },
            api_c.PREFERENCE_KEY: api_c.PREFERENCE_KEY_DESCRIPTION,
            api_c.PREFERENCE_VALUE: api_c.PREFERENCE_VALUE_DESCRIPTION,
        },
    ]

    responses = {
        HTTPStatus.OK.value: {
            "description": "User preferences deleted",
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to delete user preferences",
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [USER_TAG]

    def delete(self, user_id: str) -> Tuple[dict, int]:
        """Delete a user's preferences

        ---
        Args:
            user_id (str): User id

        Returns:
            Tuple[dict, int]: profile dict, HTTP status

        """
        request_data = request.get_json()

        if ObjectId.is_valid(user_id):
            user_id = ObjectId(user_id)
        else:
            return {
                "message": f"Invalid user ID received {user_id}."
            }, HTTPStatus.BAD_REQUEST

        manage_user_dashboard_config(
            get_db_client(),
            user_id=user_id,
            config_key=request_data[api_c.PREFERENCE_KEY],
            config_value=request_data[api_c.PREFERENCE_VALUE],
            delete_flag=True,
        )

        return {"message": api_c.OPERATION_SUCCESS}, HTTPStatus.OK


@add_view_to_blueprint(
    user_bp, f"/{USER_ENDPOINT}/<user_id>/favorites", "AddUserFavorite"
)
class AddUserFavorite(SwaggerView):
    """
    Add user favorites class
    """

    parameters = [
        {
            "name": db_constants.USER_ID,
            "in": "path",
            "type": "string",
            "description": "User ID.",
            "example": "5f5f7262997acad4bac4373b",
            "required": True,
        },
        {
            "name": "body",
            "in": "body",
            "type": "object",
            "description": api_c.FAVORITE_BODY_DESCRIPTION,
            "example": {
                db_constants.COMPONENT_NAME: "Audience",
                db_constants.COMPONENT_ID: "5f5f7262997acad4bac4364a",
            },
            db_constants.COMPONENT_NAME: "component name",
            db_constants.COMPONENT_ID: "id of favorite component",
        },
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
    responses.update(AUTH401_RESPONSE)
    tags = [USER_TAG]

    def post(self, user_id: str) -> Tuple[dict, int]:
        """Add a new favorite for a user

        ---
        Args:
            user_id (str): User id

        Returns:
            Tuple[dict, int]: Configuration dict, HTTP status

        """
        request_data = request.get_json()
        component_id = request_data["component_id"]
        component_name = request_data["component_name"]

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


@add_view_to_blueprint(
    user_bp, f"/{USER_ENDPOINT}/<user_id>/favorites", "EditUserFavorite"
)
class EditUserFavorite(SwaggerView):
    """
    Edit user favorites class
    """

    parameters = [
        {
            "name": db_constants.USER_ID,
            "in": "path",
            "type": "string",
            "description": "User ID.",
            "example": "5f5f7262997acad4bac4373b",
            "required": True,
        },
        {
            "name": "body",
            "in": "body",
            "type": "object",
            "description": api_c.FAVORITE_BODY_DESCRIPTION,
            "example": {
                db_constants.COMPONENT_NAME: "Audience",
                db_constants.COMPONENT_ID: "5f5f7262997acad4bac4364a",
            },
            db_constants.COMPONENT_NAME: "component name",
            db_constants.COMPONENT_ID: "id of favorite component",
        },
    ]
    responses = {
        HTTPStatus.OK.value: {
            "description": "User favorite edited",
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to edit user favorite",
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [USER_TAG]

    def put(self, user_id: str) -> Tuple[dict, int]:
        """Edit favorite for a user

        ---
        Args:
            user_id (str): User id

        Returns:
            Tuple[dict, int]: Configuration dict, HTTP status

        """
        request_data = request.get_json()
        component_id = request_data["component_id"]
        component_name = request_data["component_name"]

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


@add_view_to_blueprint(
    user_bp, f"/{USER_ENDPOINT}/<user_id>/favorites", "DeleteUserFavorite"
)
class DeleteUserFavorite(SwaggerView):
    """
    Delete user favorites class
    """

    parameters = [
        {
            "name": db_constants.USER_ID,
            "in": "path",
            "type": "string",
            "description": "User ID.",
            "example": "5f5f7262997acad4bac4373b",
            "required": True,
        },
        {
            "name": "body",
            "in": "body",
            "type": "object",
            "description": api_c.FAVORITE_BODY_DESCRIPTION,
            "example": {
                db_constants.COMPONENT_NAME: "audience",
                db_constants.COMPONENT_ID: "5f5f7262997acad4bac4364a",
            },
            db_constants.COMPONENT_NAME: "component name",
            db_constants.COMPONENT_ID: "id of favorite component",
        },
    ]
    responses = {
        HTTPStatus.OK.value: {
            "description": "User favorite deleted",
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to delete user favorite",
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [USER_TAG]

    def delete(self, user_id: str) -> Tuple[dict, int]:
        """Delete a favorite for a user

        ---
        Args:
            user_id (str): User id

        Returns:
            Tuple[dict, int]: Configuration dict, HTTP status

        """
        request_data = request.get_json()
        component_id = request_data["component_id"]
        component_name = request_data["component_name"]

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

        manage_user_favorites(
            get_db_client(),
            user_id=user_id,
            component_name=component_name,
            component_id=component_id,
            delete_flag=True,
        )

        return {"message": api_c.OPERATION_SUCCESS}, HTTPStatus.OK
