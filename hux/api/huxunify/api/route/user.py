# pylint: disable=no-self-use
"""
Paths for the User API
"""
from http import HTTPStatus
from typing import Tuple

from connexion.exceptions import ProblemException
from flask import Blueprint
from flasgger import SwaggerView

from huxunifylib.util.general.logging import logger
from huxunifylib.database import constants as db_constants
from huxunifylib.database.user_management import (
    get_user,
    manage_user_favorites,
)
from huxunify.api.schema.errors import NotFoundError
from huxunify.api.route.utils import (
    add_view_to_blueprint,
    get_db_client,
    secured,
    api_error_handler,
)
from huxunify.api.schema.user import UserSchema
from huxunify.api.schema.utils import AUTH401_RESPONSE
from huxunify.api import constants as api_c


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
    """
    User Profile Class
    """

    responses = {
        HTTPStatus.OK.value: {
            "description": "Retrieve Individual User profile",
            "schema": UserSchema,
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
            Tuple[dict, int]: dict of user and http code

        """
        okta_id = None  # TODO : Fetch okta id from JWT Token (HUS-443)

        try:
            return (
                UserSchema().dump(get_user(get_db_client(), okta_id)),
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
    user_bp, "<component_name>/<component_id>/favorite", "AddUserFavorite"
)
class AddUserFavorite(SwaggerView):
    """
    Add user favorites class
    """

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
            component_name (str): Component name
            component_id (str): Component id

        Returns:
            Tuple[dict, int]: Configuration dict, HTTP status

        """

        okta_id = None  # TODO : Fetch okta id from JWT Token (HUS-443)

        if component_name not in db_constants.FAVORITE_COMPONENTS:
            logger.error(
                "Component name %s not in favorite components.", component_name
            )
            return {
                "message": api_c.INVALID_COMPONENT_NAME
            }, HTTPStatus.BAD_REQUEST

        response = manage_user_favorites(
            get_db_client(),
            okta_id=okta_id,
            component_name=component_name,
            component_id=component_id,
        )

        return response, HTTPStatus.CREATED


@add_view_to_blueprint(
    user_bp, "<component_name>/<component_id>/favorite", "DeleteUserFavorite"
)
class DeleteUserFavorite(SwaggerView):
    """
    Delete user favorites class
    """

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
            component_name (str): Component name
            component_id (str): Component id

        Returns:
            Tuple[dict, int]: Configuration dict, HTTP status

        """
        okta_id = None  # TODO : Fetch okta id from JWT Token (HUS-443)

        if component_name not in db_constants.FAVORITE_COMPONENTS:
            logger.error(
                "Component name %s not in favorite components.", component_name
            )
            return {
                "message": api_c.INVALID_COMPONENT_NAME
            }, HTTPStatus.BAD_REQUEST

        manage_user_favorites(
            get_db_client(),
            okta_id=okta_id,
            component_name=component_name,
            component_id=component_id,
            delete_flag=True,
        )
        logger.info("Successfully deleted user favorite %s.", component_name)
        return {"message": api_c.OPERATION_SUCCESS}, HTTPStatus.OK
