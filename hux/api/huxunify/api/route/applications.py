# pylint: disable=no-self-use
"""Paths for applications API"""
from http import HTTPStatus
from typing import Tuple

from bson import ObjectId
from flask import Blueprint, jsonify, request
from flasgger import SwaggerView

from huxunifylib.util.general.logging import logger
from huxunifylib.database import (
    constants as db_c,
    collection_management,
)
from huxunify.api.schema.applications import (
    ApplicationsGETSchema,
    ApplicationsPostSchema,
    ApplicationsPatchSchema,
)
from huxunify.api.route.decorators import (
    add_view_to_blueprint,
    secured,
    api_error_handler,
    requires_access_levels,
)
from huxunify.api.route.utils import get_db_client
from huxunify.api import constants as api_c

from huxunify.api.schema.utils import (
    AUTH401_RESPONSE,
)

# setup the applications blueprint
applications_bp = Blueprint(api_c.APPLICATIONS_ENDPOINT, import_name=__name__)


@applications_bp.before_request
@secured()
def before_request():
    """Protect all of the applications endpoints."""

    pass  # pylint: disable=unnecessary-pass


@add_view_to_blueprint(
    applications_bp,
    api_c.APPLICATIONS_ENDPOINT,
    "ApplicationsPostView",
)
class ApplicationsPostView(SwaggerView):
    """Applications Post view class."""

    parameters = [
        {
            "name": "body",
            "in": "body",
            "type": "object",
            "description": "Input Applications body.",
            "example": {
                api_c.CATEGORY: "uncategorized",
                api_c.TYPE: "custom-application",
                api_c.NAME: "Custom Application",
                api_c.URL: "URL_Link",
            },
            "required": True,
        },
    ]

    responses = {
        HTTPStatus.CREATED.value: {
            "schema": ApplicationsGETSchema,
            "description": "Application created.",
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to create application.",
        },
        HTTPStatus.FORBIDDEN.value: {
            "description": "Application already exists.",
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.APPLICATIONS_TAG]

    # pylint: disable=too-many-return-statements
    # pylint: disable=too-many-branches
    # pylint: disable=no-self-use
    @api_error_handler()
    @requires_access_levels(api_c.USER_ROLE_ALL)
    def post(self, user: dict) -> Tuple[dict, int]:
        """Creates a new application.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            user (dict): user object.

        Returns:
            Tuple[dict, int]: Created application, HTTP status code.
        """

        application = ApplicationsPostSchema().load(
            request.get_json(),
        )
        database = get_db_client()

        application[api_c.STATUS] = api_c.STATUS_PENDING
        application[db_c.ADDED] = True

        document = collection_management.create_document(
            database,
            db_c.APPLICATIONS_COLLECTION,
            application,
            user[api_c.USER_NAME],
        )
        logger.info(
            "Successfully created application %s.", application.get(db_c.NAME)
        )

        return (
            jsonify(ApplicationsGETSchema().dump(document)),
            HTTPStatus.CREATED.value,
        )


@add_view_to_blueprint(
    applications_bp,
    f"{api_c.APPLICATIONS_ENDPOINT}/<application_id>",
    "ApplicationsPatchView",
)
class ApplicationsPatchView(SwaggerView):
    """Applications Patch view class."""

    parameters = [
        {
            "name": api_c.APPLICATION_ID,
            "description": "Application ID.",
            "type": "string",
            "in": "path",
            "required": True,
            "example": "5f5f7262997acad4bac4373b",
        },
        {
            "name": "body",
            "in": "body",
            "type": "object",
            "description": "Input Application's fields to edit.",
            "example": {
                api_c.URL: "URL_Link",
            },
        },
    ]

    responses = {
        HTTPStatus.OK.value: {
            "schema": ApplicationsGETSchema,
            "description": "Application patched.",
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to patch application.",
        },
        HTTPStatus.NOT_FOUND.value: {
            "description": "Failed to find application.",
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.APPLICATIONS_TAG]

    # pylint: disable=too-many-return-statements
    # pylint: disable=too-many-branches
    # pylint: disable=no-self-use
    @api_error_handler()
    @requires_access_levels([api_c.EDITOR_LEVEL, api_c.ADMIN_LEVEL])
    def patch(self, application_id: str, user: dict) -> Tuple[dict, int]:
        """Modifies an existing application.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            application_id (str): application
            user (dict): user object.

        Returns:
            Tuple[dict, int]: Updated application, HTTP status code.
        """
        if not request.get_json():
            logger.info("Could not patch application.")
            return {"message": "No body provided."}, HTTPStatus.BAD_REQUEST

        ApplicationsPatchSchema().validate(
            request.get_json(),
        )
        database = get_db_client()

        if not collection_management.get_document(
            database,
            db_c.APPLICATIONS_COLLECTION,
            {db_c.ID: ObjectId(application_id)},
        ):
            return {
                "message": f"Application {application_id} not found"
            }, HTTPStatus.NOT_FOUND

        updated_application = collection_management.update_document(
            database,
            db_c.APPLICATIONS_COLLECTION,
            ObjectId(application_id),
            request.get_json(),
            user[api_c.USER_NAME],
        )

        logger.info(
            "Successfully updated application %s.",
            updated_application.get(db_c.NAME),
        )

        return (
            jsonify(ApplicationsGETSchema().dump(updated_application)),
            HTTPStatus.OK.value,
        )
