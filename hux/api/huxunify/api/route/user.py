"""
Paths for the User API
"""

from http import HTTPStatus
from typing import List, Tuple

from bson import ObjectId
from flask import Blueprint, request
from marshmallow.exceptions import ValidationError
from flask_apispec import marshal_with
from flasgger import SwaggerView, swag_from
from huxunify.api.model.cdm import CdmModel
from huxunify.api.model.user import UserModel
from huxunify.api.schema.errors import NotFoundError, RequestError
from huxunify.api.schema.cdm import Datafeed, Fieldmapping, ProcessedData
from huxunify.api.route.utils import add_view_to_blueprint
from huxunify.api.schema.user import User

USER_TAG = "user"
USER_DESCRIPTION = "USER API"
USER_TAG = "user"
USER_ENDPOINT = "user"

# setup the cdm blueprint
user_bp = Blueprint("user", import_name=__name__)


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
            data = UserModel().get_all_users()

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

    parameters = [{"id": "okta id of user"}]
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

    @marshal_with(User)
    def get(self, okta_id: ObjectId) -> User:
        """Retrieves a user by ID.

        ---

        Returns:
            Response: Returns a user

        """
        try:
            # TODO validation for id?
            data = UserModel().get_user(okta_id=okta_id)

            if not data:
                error = NotFoundError().dump({"message": "User not found"})
                return error, error["code"]

            return data, HTTPStatus.OK.value

        except error:
            return error, error["code"]


@user_bp.route("/users/update-dashboard", methods=["POST"])
@swag_from(
    {
        "parameters": [
            {"user_id": "user_id", "config_key": "key name", "config_value": "value"}
        ]
    }
)
def update_user_dashboard_configuration():
    """
    Update user's dashboard configuration
    """
    try:
        # TODO validation?
        request_data = request.get_json()

        user_id = request_data["user_id"]
        config_key = request_data["config_key"]
        config_value = request_data["config_value"]

        data = UserModel().update_user_dashboard(
            user_id=user_id, config_key=config_key, config_value=config_value
        )

        return data, HTTPStatus.OK.value
    except:
        pass


# TODO update-profile vs update user. Whats the different user cases?
@user_bp.route("/users/update-profile", methods=["POSTS"])
@swag_from({"parameters": [{"user_id": "user_id", "update_doc": "update doc"}]})
def update_user_profile():
    """
    Update User Profile
    """
    try:
        # TODO validation?
        request_data = request.get_json()

        user_id = request_data["user_id"]
        update_doc = request_data["user_id"]

        data = UserModel().update_user(user_id=user_id, update_doc=update_doc)

        return data, HTTPStatus.OK.value
    except:
        pass


@user_bp.route("/users/add-favorite", methods=["POSTS"])
@swag_from(
    {
        "parameters": [
            {
                "user_id": "user_id",
                "component_name": "component name",
                "component_id": "component_id",
            }
        ]
    }
)
def add_user_favorite():
    """
    Add a new favorite for a user
    """
    try:
        # TODO validation?
        request_data = request.get_json()

        user_id = request_data["user_id"]
        component_name = request_data["component_name"]
        component_id = request_data["component_id"]

        data = UserModel().update_user_favorites(
            user_id=user_id,
            component_name=component_name,
            component_id=component_id,
            delete=False,
        )

        return data, HTTPStatus.OK.value
    except:
        pass


@user_bp.route("/users/remove-favorite", methods=["POSTS"])
@swag_from(
    {
        "parameters": [
            {
                "user_id": "user_id",
                "component_name": "component name",
                "component_id": "component_id",
            }
        ]
    }
)
def remove_user_favorite():
    """
    Remove a favorite for a user
    """
    try:
        # TODO validation?
        request_data = request.get_json()

        user_id = request_data["user_id"]
        component_name = request_data["component_name"]
        component_id = request_data["component_id"]

        data = UserModel().update_user_favorites(
            user_id=user_id,
            component_name=component_name,
            component_id=component_id,
            delete=True,
        )

        return data, HTTPStatus.OK.value
    except:
        pass
