# pylint: disable=no-self-use
"""Paths for the User API"""
import datetime
import random
from http import HTTPStatus
from typing import Tuple
from faker import Faker

from bson import ObjectId
from connexion.exceptions import ProblemException
from flask import Blueprint, request, jsonify
from flasgger import SwaggerView

from huxunifylib.util.general.logging import logger
from huxunifylib.database import constants as db_constants
from huxunifylib.database.user_management import (
    get_user,
    manage_user_favorites,
    get_all_users,
    update_user,
)
from huxunify.api.schema.errors import NotFoundError
from huxunify.api.route.decorators import (
    add_view_to_blueprint,
    secured,
    api_error_handler,
    get_user_name,
)
from huxunify.api.route.utils import (
    get_db_client,
)
from huxunify.api.schema.user import UserSchema, UserPatchSchema
from huxunify.api.schema.utils import AUTH401_RESPONSE
from huxunify.api import constants as api_c
from huxunify.api.data_connectors.okta import (
    get_token_from_request,
    introspect_token,
)

# setup the cdm blueprint
user_bp = Blueprint(api_c.USER_ENDPOINT, import_name=__name__)


@user_bp.before_request
@secured()
def before_request():
    """Protect all of the user endpoints."""

    pass  # pylint: disable=unnecessary-pass


@add_view_to_blueprint(
    user_bp, f"{api_c.USER_ENDPOINT}/profile", "IndividualUserSearch"
)
class UserProfile(SwaggerView):
    """User Profile Class."""

    responses = {
        HTTPStatus.OK.value: {
            "description": "Retrieve Individual User profile",
            "schema": UserSchema,
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to get user details from request."
        },
        HTTPStatus.NOT_FOUND.value: {
            "schema": NotFoundError,
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.USER_TAG]

    @api_error_handler()
    def get(self) -> Tuple[dict, int]:
        """Retrieves a user profile.

        ---
        security:
            - Bearer: ["Authorization"]

        Returns:
            Tuple[dict, int]: dict of user, HTTP status code.

        Raises:
            ProblemException: Any exception raised during endpoint execution.
        """

        okta_id = introspect_token(get_token_from_request(request)[0]).get(
            api_c.OKTA_USER_ID
        )

        try:
            database = get_db_client()
            user = get_user(database, okta_id)

            # return NOT_FOUND if no corresponding user record is found in DB.
            if user is None:
                return {
                    api_c.MESSAGE: api_c.USER_NOT_FOUND
                }, HTTPStatus.NOT_FOUND

            # update user record's login_count and update_time in DB and return
            # the updated record.
            user = update_user(
                database,
                okta_id=okta_id,
                update_doc={
                    db_constants.USER_LOGIN_COUNT: (
                        user.get(db_constants.USER_LOGIN_COUNT, 0) + 1
                    )
                },
            )

            return (
                UserSchema().dump(user),
                HTTPStatus.OK,
            )
        except Exception as exc:
            logger.error(
                "%s: %s.",
                exc.__class__,
                exc,
            )
            raise ProblemException(
                status=int(HTTPStatus.BAD_REQUEST.value),
                title=HTTPStatus.BAD_REQUEST.description,
                detail="Unable to get user profile.",
            ) from exc


@add_view_to_blueprint(
    user_bp,
    f"{api_c.USER_ENDPOINT}/<component_name>/<component_id>/favorite",
    "AddUserFavorite",
)
class AddUserFavorite(SwaggerView):
    """Add user favorites class."""

    parameters = [
        {
            "name": db_constants.COMPONENT_ID,
            "in": "path",
            "type": "string",
            "description": "Component ID.",
            "example": "5f5f7262997acad4bac4373b",
            "required": True,
        },
        {
            "name": db_constants.COMPONENT_NAME,
            "in": "path",
            "type": "string",
            "description": "Component name.",
            "example": "audiences",
            "required": True,
        },
    ]
    responses = {
        HTTPStatus.CREATED.value: {
            "description": "User favorite created",
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to add user favorite",
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.USER_TAG]

    @api_error_handler()
    def post(self, component_name: str, component_id: str) -> Tuple[dict, int]:
        """Creates a user favorite.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            component_name (str): Component name.
            component_id (str): Component ID.

        Returns:
            Tuple[dict, int]: Configuration dict, HTTP status code.
        """

        okta_id = introspect_token(get_token_from_request(request)[0]).get(
            api_c.OKTA_USER_ID
        )

        if component_name not in db_constants.FAVORITE_COMPONENTS:
            logger.error(
                "Component name %s not in favorite components.", component_name
            )
            return {
                "message": api_c.INVALID_COMPONENT_NAME
            }, HTTPStatus.BAD_REQUEST

        component_id = ObjectId(component_id)

        user_details = manage_user_favorites(
            get_db_client(),
            okta_id=okta_id,
            component_name=component_name,
            component_id=component_id,
        )
        if user_details:
            return {"message": api_c.OPERATION_SUCCESS}, HTTPStatus.CREATED

        return {
            "message": f"{str(component_id)} already in favorites."
        }, HTTPStatus.OK


@add_view_to_blueprint(
    user_bp,
    f"{api_c.USER_ENDPOINT}/<component_name>/<component_id>/favorite",
    "DeleteUserFavorite",
)
class DeleteUserFavorite(SwaggerView):
    """Delete user favorites class."""

    parameters = [
        {
            "name": db_constants.COMPONENT_ID,
            "in": "path",
            "type": "string",
            "description": "Component ID.",
            "example": "5f5f7262997acad4bac4373b",
            "required": True,
        },
        {
            "name": db_constants.COMPONENT_NAME,
            "in": "path",
            "type": "string",
            "description": "Component name.",
            "example": "audiences",
            "required": True,
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
    tags = [api_c.USER_TAG]

    @api_error_handler()
    def delete(
        self, component_name: str, component_id: str
    ) -> Tuple[dict, int]:
        """Deletes a user favorite.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            component_name (str): Component name.
            component_id (str): Component ID.

        Returns:
            Tuple[dict, int]: Configuration dict, HTTP status code.
        """

        okta_id = introspect_token(get_token_from_request(request)[0]).get(
            api_c.OKTA_USER_ID
        )

        if component_name not in db_constants.FAVORITE_COMPONENTS:
            logger.error(
                "Component name %s not in favorite components.", component_name
            )
            return {
                "message": api_c.INVALID_COMPONENT_NAME
            }, HTTPStatus.BAD_REQUEST

        user_details = manage_user_favorites(
            get_db_client(),
            okta_id=okta_id,
            component_name=component_name,
            component_id=ObjectId(component_id),
            delete_flag=True,
        )
        if user_details:
            logger.info(
                "Successfully deleted user favorite %s.", component_name
            )
            return {"message": api_c.OPERATION_SUCCESS}, HTTPStatus.OK

        return {
            "message": f"{component_id} not part of user favorites"
        }, HTTPStatus.OK


@add_view_to_blueprint(user_bp, api_c.USER_ENDPOINT, "UserView")
class UserView(SwaggerView):
    """User view class."""

    responses = {
        HTTPStatus.OK.value: {
            "description": "List of all Users.",
            "schema": {"type": "array", "items": UserSchema},
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to get all Users."
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.USER_TAG]

    @api_error_handler()
    def get(self) -> Tuple[list, int]:  # pylint: disable=no-self-use
        """Retrieves all users.

        ---
        security:
            - Bearer: ["Authorization"]

        Returns:
            Tuple[list, int]: list of users, HTTP status code.
        """

        # get all users
        users = get_all_users(get_db_client())

        # generate random phone number and user access level
        for user in users:
            user[api_c.USER_PHONE_NUMBER] = Faker().phone_number()
            user[api_c.USER_ACCESS_LEVEL] = random.choice(
                ["Edit", "View-only", "Admin"]
            )

        return (
            jsonify(UserSchema().dump(users, many=True)),
            HTTPStatus.OK.value,
        )


@add_view_to_blueprint(
    user_bp,
    f"{api_c.USER_ENDPOINT}/<destination_id>",
    "UserPatchView",
)
class UserPatchView(SwaggerView):
    """Destination Patch class."""

    parameters = [
        {
            "name": api_c.DESTINATION_ID,
            "description": "Destination ID.",
            "type": "string",
            "in": "path",
            "required": "true",
            "example": "5f5f7262997acad4bac4373b",
        },
        {
            "name": "body",
            "in": "body",
            "type": "object",
            "description": "Input Destination body.",
            "example": {db_constants.ENABLED: False},
        },
    ]

    responses = {
        HTTPStatus.OK.value: {
            "description": "User updated.",
            "schema": UserSchema,
        },
        HTTPStatus.UNPROCESSABLE_ENTITY.value: {
            "description": "Failed to patch user data.",
            "schema": {
                "example": {
                    "message": api_c.DESTINATION_INVALID_PATCH_MESSAGE
                },
            },
        },
    }

    responses.update(AUTH401_RESPONSE)
    tags = [api_c.DESTINATIONS_TAG]

    # pylint: disable=unexpected-keyword-arg
    # pylint: disable=too-many-return-statements
    @api_error_handler()
    @get_user_name()
    def patch(self, user_name: str) -> Tuple[dict, int]:
        """Updates a destination.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            user_name (str): user_name extracted from Okta.

        Returns:
            Tuple[dict, int]: User doc, HTTP status code.
        """

        okta_id = introspect_token(get_token_from_request(request)[0]).get(
            api_c.OKTA_USER_ID
        )

        UserPatchSchema.validate(request.get_json())

        # update the document
        return (
            UserSchema().dump(
                update_user(
                    get_db_client(),
                    okta_id,
                    {
                        **request.get_json(),
                        **{
                            db_constants.UPDATED_BY: user_name,
                            db_constants.UPDATE_TIME: datetime.datetime.utcnow(),
                        },
                    },
                )
            ),
            HTTPStatus.OK,
        )
