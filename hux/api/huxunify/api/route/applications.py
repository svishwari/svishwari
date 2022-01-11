# pylint: disable=no-self-use
"""Paths for applications API"""
from http import HTTPStatus
from typing import Tuple
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
    FAILED_DEPENDENCY_424_RESPONSE,
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
        application[api_c.IS_ADDED] = True

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
